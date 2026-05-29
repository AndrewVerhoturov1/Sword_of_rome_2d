#!/usr/bin/env python3
"""
Validate a V3 artifact package: structure, manifest, checksums, and paths.

P2 fixes (2026-05-29): #1 forbidden paths defaults, #2 strict write_policy,
#3 acceptance_criteria/known_risks hard-fail, #4 POST_IMPORT_TEST_PROMPT hardened,
#6 reject top-level ZIP files, #10 binary file check.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]


V3_ID_RE = r"^V3-\d{8}-\d{6}-[a-z0-9][a-z0-9-]*[a-z0-9]$"

REQUIRED_ROOT_ITEMS = frozenset({
    "manifest.yaml", "README_FOR_KILO.md", "README_FOR_CODEX.md",
    "checksums.sha256", "files/",
})

ALLOWED_CONTROL_FILES = frozenset({
    "manifest.yaml", "README_FOR_KILO.md", "README_FOR_CODEX.md",
    "checksums.sha256", "POST_IMPORT_TEST_PROMPT.md",
})

ALLOWED_ACTIONS = frozenset({"create"})
ALLOWED_SCOPES = frozenset({"docs_only", "workflow_docs", "schemas", "scripts", "product_code"})
ALLOWED_TESTING_MODES = frozenset({"required", "optional", "waived"})

# Issue #1: contract defaults with lock-files
DEFAULT_FORBIDDEN_PREFIXES = (
    ".git/", ".github/", "node_modules/", "dist/", "build/", "coverage/",
    ".env", ".env.local", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
)

# Issue #4: required prompt section headings (case-insensitive)
REQUIRED_PROMPT_SECTIONS = (
    "execution split proposal", "machine checks",
    "human checks", "machine-check report output",
)

BINARY_CHECK_BYTES = 4096


def _fail(msg: str, code: int = 1) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(code)


def _ok(msg: str) -> None:
    print(f"  OK: {msg}")


def _info(msg: str) -> None:
    print(f" INFO: {msg}")


def _warn(msg: str) -> None:
    print(f" WARN: {msg}")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_yaml(path: Path):
    if yaml is None:
        _fail("PyYAML not installed. Install: pip install pyyaml")
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _is_safe_relative(target: str) -> bool:
    p = Path(target)
    if p.is_absolute() or ".." in p.parts:
        return False
    return True


def _match_prefixes(target: str, prefixes: list[str]) -> bool:
    target_norm = target.replace("\\", "/")
    for prefix in prefixes:
        prefix_norm = prefix.replace("\\", "/")
        if target_norm == prefix_norm.rstrip("/") or target_norm.startswith(prefix_norm):
            return True
    return False


def _is_binary_file(path: Path) -> bool:
    """Issue #10: null-byte heuristic."""
    try:
        with open(path, "rb") as fh:
            return b"\x00" in fh.read(BINARY_CHECK_BYTES)
    except OSError:
        return True


def _is_safe_zip_member(name: str) -> bool:
    """Issue #6: reject dangerous ZIP paths."""
    if name.startswith("/") or ".." in Path(name).parts:
        return False
    if "\\" in name:
        return False
    if len(name) >= 2 and name[1] == ":":
        return False
    return True


def _zip_members_by_root(names: list[str]) -> dict[str, list[str]]:
    """Issue #6: group by root, reject top-level files."""
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
        _fail(f"ZIP contains top-level files outside root folder: "
              + ", ".join(f"`{f}`" for f in top_level))
    return roots


def _validate_structure(root_dir: Path) -> str:
    import re
    dir_name = root_dir.name
    if not re.match(V3_ID_RE, dir_name):
        _fail(f"Root folder name `{dir_name}` does not match V3-YYYYMMDD-HHMMSS-<slug>.")
    actual: set[str] = set()
    for item in root_dir.iterdir():
        key = item.name
        if item.is_dir():
            key += "/"
        actual.add(key)
    missing = REQUIRED_ROOT_ITEMS - actual
    if missing:
        _fail(f"Missing required items in package root: {sorted(missing)}")
    extra_control = actual - REQUIRED_ROOT_ITEMS - {"POST_IMPORT_TEST_PROMPT.md"}
    for entry_name in sorted(extra_control):
        if entry_name in ALLOWED_CONTROL_FILES:
            continue
        _fail(f"Unexpected item in package root: `{entry_name}`")
    _ok("Package structure: all required items present.")
    return dir_name


def _validate_manifest(manifest_path: Path) -> dict:
    data = _load_yaml(manifest_path)
    import re

    for field in ("v3_id", "task_title", "generated_by", "action", "scope"):
        if field not in data or not isinstance(data[field], str) or not data[field].strip():
            _fail(f"manifest.yaml: missing or empty required field `{field}`.")
    v3_id = data["v3_id"]
    if not re.match(V3_ID_RE, v3_id):
        _fail(f"manifest.yaml: `v3_id` `{v3_id}` does not match V3-YYYYMMDD-HHMMSS-<slug>.")
    if data["action"] not in ALLOWED_ACTIONS:
        _fail(f"manifest.yaml: unsupported action `{data['action']}`.")
    if data["scope"] not in ALLOWED_SCOPES:
        _fail(f"manifest.yaml: unknown scope `{data['scope']}`.")

    # Issue #2: strict write_policy
    wp = data.get("write_policy")
    if not isinstance(wp, dict):
        _fail("manifest.yaml: `write_policy` block missing or not a dict.")
    for field in ("mode", "require_codex_review", "require_human_review", "allow_overwrite"):
        if field not in wp:
            _fail(f"manifest.yaml: `write_policy.{field}` is missing.")
    if wp["mode"] != "create_only":
        _fail("manifest.yaml: `write_policy.mode` must be `create_only`.")
    if wp["require_codex_review"] is not True:
        _fail("manifest.yaml: `write_policy.require_codex_review` must be true.")
    if wp["require_human_review"] is not True:
        _fail("manifest.yaml: `write_policy.require_human_review` must be true.")
    if wp["allow_overwrite"] is not False:
        _fail("manifest.yaml: `write_policy.allow_overwrite` must be false.")

    allowed_paths = data.get("allowed_paths")
    if not isinstance(allowed_paths, list) or len(allowed_paths) == 0:
        _fail("manifest.yaml: `allowed_paths` must be a non-empty list.")

    # Issue #1: fixed forbidden_paths
    raw_forbidden = data.get("forbidden_paths")
    if raw_forbidden is None:
        forbidden = list(DEFAULT_FORBIDDEN_PREFIXES)
        _info("manifest.yaml: `forbidden_paths` absent, using contract defaults.")
    elif isinstance(raw_forbidden, list):
        if len(raw_forbidden) == 0:
            forbidden = list(DEFAULT_FORBIDDEN_PREFIXES)
            _info("manifest.yaml: `forbidden_paths` is empty, defaults applied for safety.")
        else:
            forbidden = list(raw_forbidden)
    else:
        forbidden = list(DEFAULT_FORBIDDEN_PREFIXES)

    files_list = data.get("files")
    if not isinstance(files_list, list) or len(files_list) == 0:
        _fail("manifest.yaml: `files` block must be a non-empty list.")

    for idx, item in enumerate(files_list, 1):
        if not isinstance(item, dict):
            _fail(f"manifest.yaml: files[{idx}] is not a dict.")
        for field in ("path", "source_in_zip", "action", "required", "sha256", "purpose"):
            if field not in item:
                _fail(f"manifest.yaml: files[{idx}] — missing field `{field}`.")
        if item["action"] not in ALLOWED_ACTIONS:
            _fail(f"manifest.yaml: files[{idx}] — unsupported action `{item['action']}`.")
        pth = item["path"]
        if not _is_safe_relative(pth):
            _fail(f"manifest.yaml: files[{idx}] — unsafe path `{pth}`.")
        if not _match_prefixes(pth, allowed_paths):
            _fail(f"manifest.yaml: files[{idx}] — path `{pth}` not in `allowed_paths`.")
        if _match_prefixes(pth, forbidden):
            _fail(f"manifest.yaml: files[{idx}] — path `{pth}` falls into `forbidden_paths`.")

    testing = data.get("post_import_testing")
    if isinstance(testing, dict):
        mode = testing.get("mode", "waived")
        if mode not in ALLOWED_TESTING_MODES:
            _fail(f"manifest.yaml: unknown `post_import_testing.mode` `{mode}`.")

    # Issue #3: hard-fail
    ac = data.get("acceptance_criteria")
    if not isinstance(ac, list) or len(ac) == 0:
        _fail("manifest.yaml: `acceptance_criteria` must be a non-empty list.")
    kr = data.get("known_risks")
    if not isinstance(kr, list):
        _fail("manifest.yaml: `known_risks` must be a list (empty if no known risks).")

    _ok("manifest.yaml: all required fields valid.")
    return data


def _validate_files_crosscheck(root_dir: Path, manifest: dict) -> dict[str, str]:
    files_dir = root_dir / "files"
    if not files_dir.is_dir():
        _fail("`files/` directory not found in package root.")
    manifest_files: dict[str, str] = {}
    for item in manifest["files"]:
        manifest_files[item["source_in_zip"]] = item["sha256"]
    actual_files: set[str] = set()
    for f in files_dir.rglob("*"):
        if f.is_file():
            actual_files.add("files/" + f.relative_to(files_dir).as_posix())
    manifest_set = set(manifest_files.keys())
    missing_on_disk = manifest_set - actual_files
    if missing_on_disk:
        _fail("Files in manifest missing from `files/`: "
              + ", ".join(f"`{f}`" for f in sorted(missing_on_disk)))
    extra_on_disk = actual_files - manifest_set
    if extra_on_disk:
        _fail("Files in `files/` not listed in manifest: "
              + ", ".join(f"`{f}`" for f in sorted(extra_on_disk)))
    _ok("Cross-check manifest <-> files/: all files accounted for.")
    # Issue #10: binary check
    binary_found = [src for src in manifest_files
                    if (root_dir / src).is_file() and _is_binary_file(root_dir / src)]
    if binary_found:
        _fail("Binary files detected in `files/` (not allowed without explicit request): "
              + ", ".join(f"`{f}`" for f in binary_found))
    _ok("Binary file check: no binary files detected.")
    return manifest_files


def _validate_checksums(root_dir: Path, manifest_files: dict[str, str]) -> None:
    checksum_path = root_dir / "checksums.sha256"
    if not checksum_path.is_file():
        _fail("`checksums.sha256` not found.")
    expected: dict[str, str] = {}
    with open(checksum_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                _fail(f"checksums.sha256: invalid line `{line}`.")
            expected[parts[1]] = parts[0]
    mismatch: list[str] = []
    for src, manifest_sha in manifest_files.items():
        actual_sha = _sha256(root_dir / src)
        expected_sha = expected.get(src, "")
        if actual_sha != expected_sha:
            mismatch.append(f"`{src}`: checksums={expected_sha[:12]}, actual={actual_sha[:12]}")
        if manifest_sha != actual_sha:
            mismatch.append(f"`{src}`: manifest-sha256={manifest_sha[:12]}, actual={actual_sha[:12]}")
    for src in expected:
        if src not in manifest_files:
            _warn(f"checksums.sha256: entry for `{src}` not in manifest.")
    if mismatch:
        _fail("Checksum mismatch:\n  " + "\n  ".join(mismatch))
    _ok("checksums.sha256: all hashes match.")


def _validate_testing_prompt(root_dir: Path, manifest: dict) -> None:
    testing = manifest.get("post_import_testing")
    mode = testing.get("mode", "waived") if isinstance(testing, dict) else "waived"
    # Issue #4: resolve prompt filename from manifest
    prompt_filename = "POST_IMPORT_TEST_PROMPT.md"
    if isinstance(testing, dict):
        prompt_filename = testing.get("prompt_file", "POST_IMPORT_TEST_PROMPT.md")
    prompt_path = root_dir / prompt_filename
    prompt_present = prompt_path.is_file()

    if mode == "required" and not prompt_present:
        _fail(f"`post_import_testing.mode = required` but `{prompt_filename}` missing from root.")

    # Issue #4: prompt must NOT be in files/
    files_dir = root_dir / "files"
    if files_dir.is_dir() and prompt_present:
        try:
            prompt_path.relative_to(files_dir)
            _fail(f"`{prompt_filename}` found inside `files/`. Must be at package root.")
        except ValueError:
            pass

    # Issue #4: prompt must NOT be in manifest.files
    manifest_targets = {item["path"] for item in manifest.get("files", [])}
    if prompt_filename in manifest_targets:
        _fail(f"`{prompt_filename}` listed in manifest.files. It is a control file, not a target.")

    if mode == "waived" and prompt_present:
        _info(f"`post_import_testing.mode = waived` — `{prompt_filename}` will be ignored.")
    if mode == "optional":
        _info(f"`post_import_testing.mode = optional`, prompt {'present' if prompt_present else 'absent'}.")

    # Issue #4: content validation
    if mode in ("required", "optional") and prompt_present:
        _validate_prompt_content(prompt_path)


def _validate_prompt_content(prompt_path: Path) -> None:
    """Issue #4: validate required section headings."""
    try:
        text = prompt_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        _fail(f"`{prompt_path.name}` is not valid UTF-8 text.")
        return
    lines_lower = [line.strip().lower() for line in text.splitlines()]
    found = {s for s in REQUIRED_PROMPT_SECTIONS
             for line in lines_lower if s in line and line.startswith("#")}
    missing = set(REQUIRED_PROMPT_SECTIONS) - found
    if missing:
        _fail(f"`{prompt_path.name}` missing required section(s): "
              + ", ".join(f"`{s}`" for s in sorted(missing))
              + ". Required 4-section structure per v3_artifact_package_contract.md.")
    _ok(f"`{prompt_path.name}`: all {len(REQUIRED_PROMPT_SECTIONS)} required sections found.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Validate V3 artifact package.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--package", help="Path to V3 ZIP.")
    src.add_argument("--staging", help="Path to extracted staging dir (package root).")
    p.add_argument("--quiet", action="store_true", help="Show errors only.")
    return p


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    args = build_parser().parse_args()

    if args.package:
        zip_path = Path(args.package)
        if not zip_path.is_file():
            _fail(f"ZIP file not found: {zip_path}")
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            roots_map = _zip_members_by_root(names)  # Issue #6
            if len(roots_map) != 1:
                _fail(f"ZIP must contain exactly one root folder. Found: {sorted(roots_map.keys())}")
            root_name = list(roots_map.keys())[0]
            import tempfile
            with tempfile.TemporaryDirectory(prefix="v3validate_") as tmp:
                zf.extractall(tmp)
                _run_checks(Path(tmp) / root_name, quiet=args.quiet)
    else:
        staging_dir = Path(args.staging)
        if not staging_dir.is_dir():
            _fail(f"Staging directory not found: {staging_dir}")
        _run_checks(staging_dir, quiet=args.quiet)
    print("\nPASS: V3 package is valid.")
    return 0


def _run_checks(package_root: Path, *, quiet: bool = False) -> None:
    if not quiet:
        print(f"V3 validate: {package_root}")
    v3_id = _validate_structure(package_root)
    manifest = _validate_manifest(package_root / "manifest.yaml")
    if manifest["v3_id"] != v3_id:
        _fail(f"manifest.yaml `v3_id` `{manifest['v3_id']}` != folder name `{v3_id}`.")
    manifest_files = _validate_files_crosscheck(package_root, manifest)
    _validate_checksums(package_root, manifest_files)
    _validate_testing_prompt(package_root, manifest)


if __name__ == "__main__":
    raise SystemExit(main())
