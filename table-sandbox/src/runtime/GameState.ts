/**
 * GameState — authoritative runtime state.
 *
 * Живёт вне Phaser. Phaser — только renderer/input layer.
 * Единственный source of truth для всего runtime.
 *
 * Это placeholder для Phase 1 Technical Bootstrap.
 * Реальная структура будет расширена в Phase 3 (Runtime/Data Bootstrap).
 */

export interface GameState {
  /** Монотонная версия состояния — увеличивается при каждом коммите */
  version: number;

  /** Время создания/последнего обновления */
  lastUpdated: number;

  /** Описание текущего состояния (для debug) */
  description: string;
}

/** Создать начальный placeholder GameState */
export function createInitialGameState(): GameState {
  return {
    version: 0,
    lastUpdated: Date.now(),
    description:
      "Table Sandbox 0.1 — Technical Bootstrap. " +
      "Runtime state живёт здесь, вне Phaser. " +
      "Phaser только рендерит и принимает input.",
  };
}
