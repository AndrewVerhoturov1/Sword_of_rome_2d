/**
 * snapshot.ts — minimal runtime snapshot save/load through localStorage.
 *
 * Handoff 0014: самый узкий persistence step.
 *
 * Сохраняет только:
 *   - GameState
 *   - EventLog
 *
 * Не делает:
 *   - save slots
 *   - autosave
 *   - import/export
 *   - migration/versioning subsystem
 *   - Phaser state или UI layout state
 *
 * Storage key: table-sandbox.snapshot.v1
 */

import type { GameState } from "./GameState";
import type { EventLog } from "./actionEvent";

const STORAGE_KEY = "table-sandbox.snapshot.v1";

/** Snapshot shape as written to localStorage */
export interface Snapshot {
  schemaVersion: "0.1";
  savedAt: string;
  gameState: GameState;
  eventLog: EventLog;
}

/** Результат операции save */
export interface SaveResult {
  ok: boolean;
  message: string;
}

/** Результат операции load */
export interface LoadResult {
  ok: boolean;
  snapshot: Snapshot | null;
  message: string;
}

/**
 * Сохранить текущий runtime snapshot в localStorage.
 *
 * Перезаписывает предыдущий snapshot (один слот).
 */
export function saveSnapshot(
  gameState: GameState,
  eventLog: EventLog
): SaveResult {
  try {
    const snapshot: Snapshot = {
      schemaVersion: "0.1",
      savedAt: new Date().toISOString(),
      gameState,
      eventLog,
    };
    const json = JSON.stringify(snapshot);
    localStorage.setItem(STORAGE_KEY, json);
    return { ok: true, message: "Сохранено" };
  } catch (err) {
    const reason = err instanceof Error ? err.message : String(err);
    return { ok: false, message: `Ошибка сохранения: ${reason}` };
  }
}

/**
 * Загрузить runtime snapshot из localStorage.
 *
 * Возвращает null, если snapshot отсутствует.
 * Возвращает ошибку, если snapshot есть, но сломан.
 */
export function loadSnapshot(): LoadResult {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw === null) {
      return {
        ok: false,
        snapshot: null,
        message: "Нет сохранённого снимка",
      };
    }

    const parsed: unknown = JSON.parse(raw);

    if (!isSnapshot(parsed)) {
      return {
        ok: false,
        snapshot: null,
        message: "Снимок повреждён — неверная структура",
      };
    }

    return {
      ok: true,
      snapshot: parsed,
      message: "Загружено",
    };
  } catch (err) {
    const reason = err instanceof Error ? err.message : String(err);
    return {
      ok: false,
      snapshot: null,
      message: `Ошибка загрузки: ${reason}`,
    };
  }
}

/**
 * Удалить snapshot из localStorage.
 */
export function clearSnapshot(): void {
  localStorage.removeItem(STORAGE_KEY);
}

/**
 * Проверить, есть ли сохранённый snapshot.
 */
export function hasSnapshot(): boolean {
  return localStorage.getItem(STORAGE_KEY) !== null;
}

// ---- Type guard ----

function isSnapshot(value: unknown): value is Snapshot {
  if (value === null || typeof value !== "object") return false;
  const obj = value as Record<string, unknown>;
  return (
    obj.schemaVersion === "0.1" &&
    typeof obj.savedAt === "string" &&
    typeof obj.gameState === "object" &&
    obj.gameState !== null &&
    typeof obj.eventLog === "object" &&
    obj.eventLog !== null
  );
}
