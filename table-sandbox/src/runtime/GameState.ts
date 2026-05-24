/**
 * GameState — authoritative runtime state.
 *
 * Живёт вне Phaser. Phaser — только renderer/input layer.
 * Единственный source of truth для всего runtime.
 *
 * Расширен до минимальной first-slice структуры в Phase 3 (Runtime/Data Bootstrap).
 * Данные загружаются из canonical fixtures: table-sandbox/src/fixtures/tiny-module/
 */

// ---- Map topology ----

export interface SpaceState {
  spaceId: string;
  name: string;
  x: number;
  y: number;
  type: string;
}

export interface ConnectionState {
  connectionId: string;
  fromSpaceId: string;
  toSpaceId: string;
  type: string;
}

// ---- Pieces ----

export interface PieceState {
  pieceId: string;
  pieceDefId: string;
  locationId: string;
  ownerId: string;
  count: number;
}

// ---- Turn / Phase ----

export interface TurnState {
  round: number;
  phaseId: string;
  activeActorId: string;
}

// ---- Bootstrap metadata ----

export interface BootstrapMeta {
  source: string;
  projectId: string;
  moduleId: string;
  mapId: string;
  scenarioId: string;
  loadedFiles: string[];
}

// ---- Control state ----

/**
 * Control state — runtime ownership of spaces.
 * Живёт в runtime, не в map.json.
 * Ключ: spaceId, значение: ownerId или null (нет контроля).
 */
export type ControlState = Record<string, string | null>;

// ---- Core GameState ----

export interface GameState {
  /** Монотонная версия состояния — увеличивается при каждом коммите */
  version: number;

  /** Время создания/последнего обновления */
  lastUpdated: number;

  /** Bootstrap identity */
  projectId: string;
  moduleId: string;
  mapId: string;
  scenarioId: string;

  /** Map topology (from map.json) */
  spaces: SpaceState[];
  connections: ConnectionState[];

  /** Current piece instances (from scenario.basic.json setup) */
  pieces: PieceState[];

  /** Runtime control state: spaceId → ownerId (null = no control) */
  controlState: ControlState;

  /** Current turn/phase info */
  turn: TurnState;

  /** Evidence: откуда пришёл bootstrap */
  bootstrapMeta: BootstrapMeta;
}

/** Создать пустой placeholder GameState (для тестов или fallback) */
export function createEmptyGameState(): GameState {
  return {
    version: 0,
    lastUpdated: Date.now(),
    projectId: "",
    moduleId: "",
    mapId: "",
    scenarioId: "",
    spaces: [],
    connections: [],
    pieces: [],
    controlState: {},
    turn: { round: 0, phaseId: "", activeActorId: "" },
    bootstrapMeta: {
      source: "empty-placeholder",
      projectId: "",
      moduleId: "",
      mapId: "",
      scenarioId: "",
      loadedFiles: [],
    },
  };
}
