#!/usr/bin/env python3
"""
Stage a V3 artifact package into the repo-local staging area.

P2 fixes (2026-05-29):
- #5: fixed double-nesting — extract stripping root folder
- #6: ZIP path safety — validate all member paths
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent


def _fail(msg: str, code: int = 1) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(code)


def _ok(msg: str) -> None:
    print(f"  OK: {msg}")


def _info(msg: str) -> None:
    print(f" INFO: {msg}")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _repo_root() -> Path:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, cwd=THIS_DIR, check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        _fail("Cannot determine git repo root. Ensure script runs inside a git repository.")
    return Path(result.stdout.strip())


# Issue #6: ZIP path safety
def _is_safe_zip_member(name: str) -> bool:
    if name.startswith("/") or ".." in Path(name).parts:
        return False
    if "\\" in name:
        return False
    if len(name) >= 2 and name[1] == ":":
        return False
    return True


def _v3_id_from_zip(zip_path: Path) -> str:
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        roots: dict[str, list[str]] = {}
        top_level: list[str] = []
        for name in names:
            if not _is_safe_zip_member(name):
                _fail(f"Unsafe ZIP member path: `{name}`")
            parts = name.split("/")
            if len(parts) == 1 and name and not name.endswith("/"):
                top_level.append(name)
                continue
            root = parts[0]
            if root:
                roots.setdefault(root, []).append(name)
        if top_level:
            _fail("ZIP contains top-level files outside root folder: "
                  + ", ".join(f"`{f}`" for f in top_level))
        if len(roots) != 1:
            _fail(f"ZIP must contain exactly one root folder. Found: {sorted(roots.keys())}")
        return list(roots.keys())[0]


def _run_validate(zip_path: Path) -> None:
    validate_script = THIS_DIR / "validate_v3_package.py"
    if not validate_script.is_file():
        _fail("`scripts/v3/validate_v3_package.py` not found.")
    result = subprocess.run(
        [sys.executable, str(validate_script), "--package", str(zip_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        _fail("V3 package validation failed. Staging stopped.")
    print(result.stdout.rstrip())


def _build_staging_report(staging_dir: Path, v3_id: str, zip_path: Path, zip_sha: str) -> str:
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        f"# Staging Report — {v3_id}\n\n"
        f"- V3 ID: `{v3_id}`\n"
        f"- Source ZIP: `{zip_path}`\n"
        f"- ZIP SHA-256: `{zip_sha}`\n"
        f"- Staged at: {now_utc}\n"
        f"- Staging directory: `{staging_dir}`\n"
        f"- Status: `staged`\n\n"
        "## Notes\n\n"
        "Package validated and extracted into staging area.\n"
        "Files NOT written to project target paths.\n"
        "Journal NOT created.\n"
        "Lifecycle/navigation NOT updated.\n"
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Stage V3 ZIP: validate + extract into .ai/v3/staging/<V3-ID>/.")
    p.add_argument("--package", required=True, help="Path to V3 artifact package ZIP.")
    p.add_argument("--root", default=None, help="Git repo root. Default: git rev-parse --show-toplevel.")
    p.add_argument("--skip-validate", action="store_true", help="Skip validation (debug only).")
    return p


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    args = build_parser().parse_args()
    zip_path = Path(args.package).resolve()
    if not zip_path.is_file():
        _fail(f"ZIP file not found: {zip_path}")

    root = Path(args.root).resolve() if args.root else _repo_root()
    v3_id = _v3_id_from_zip(zip_path)
    _info(f"V3 ID: {v3_id}")

    staging_area = root / ".ai" / "v3" / "staging"
    staging_dir = staging_area / v3_id

    if staging_dir.exists():
        _fail(f"Staging directory already exists: `{staging_dir}`.")

    if not args.skip_validate:
        _info("Running validation...")
        _run_validate(zip_path)
    else:
        _info("Validation skipped (--skip-validate).")

    zip_sha = _sha256_file(zip_path)
    _info(f"ZIP SHA-256: {zip_sha}")

    staging_dir.mkdir(parents=True, exist_ok=True)
    _info(f"Extracting to: {staging_dir}")

    # Issue #5: extract stripping root folder to avoid double-nesting
    # Issue #6: validate every member path
    prefix = v3_id + "/"
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.infolist():
            name = member.filename
            if not _is_safe_zip_member(name):
                _fail(f"Unsafe ZIP member during extraction: `{name}`")

            if name == prefix or name == v3_id:
                continue  # skip root dir entry

            if not name.startswith(prefix):
                _fail(f"ZIP member `{name}` outside root folder `{v3_id}/`.")

            rel = name[len(prefix):]
            if not rel:
                continue  # trailing slash = directory marker

            target = staging_dir / rel

            # Safety: ensure target stays inside staging_dir
            try:
                target.resolve().relative_to(staging_dir.resolve())
            except ValueError:
                _fail(f"Path traversal detected: `{name}` → `{target}` would escape staging.")

            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as src, open(target, "wb") as dst:
                    dst.write(src.read())

    report_path = staging_dir / "STAGING_REPORT.md"
    report_text = _build_staging_report(staging_dir, v3_id, zip_path, zip_sha)
    report_path.write_text(report_text, encoding="utf-8")
    _ok(f"Staging report: {report_path}")

    print(f"\nPASS: V3 package staged.")
    print(f"V3 ID: {v3_id}")
    print(f"Staging dir: {staging_dir}")
    print(f"Report: {report_path}")
    print("Project files NOT modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
