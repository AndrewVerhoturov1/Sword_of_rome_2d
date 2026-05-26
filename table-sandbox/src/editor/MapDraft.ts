/**
 * MapDraft — authoring draft state for Map Authoring 0.1+ (Handoff 0020).
 *
 * Живёт ОТДЕЛЬНО от runtime GameState.
 * GameState — authoritative runtime state (read-only для editor).
 * MapDraft — editable authoring state.
 *
 * Preview: MapDraft → временный GameState (через draftToGameState).
 * Обратного пути нет: GameState не пишет в MapDraft.
 *
 * 0020: добавлен UnderlayState, EditorSettings, map-plane transform model,
 * undo/redo snapshot types.
 *
 * Borrowed pattern: prototype's layer transform, grid/snap, undo/redo,
 * но без layers/zones/rich styling.
 */

// ---- Space / Connection (0018 baseline) ----

export interface SpaceDraft {
  spaceId: string;
  name: string;
  /** map-local X (inside map-plane) */
  x: number;
  /** map-local Y (inside map-plane) */
  y: number;
  type: string;
}

export interface ConnectionDraft {
  connectionId: string;
  fromSpaceId: string;
  toSpaceId: string;
  type: string;
}

// ---- Underlay state (0020) ----

/**
 * Underlay / terrain image под spaces и connections.
 *
 * Borrowed from prototype: Layer model (kind, src, x, y, width, height,
 * rotation, opacity, visible, locked), но упрощён до одной underlay.
 */
export interface UnderlayState {
  /** image data URL или null (placeholder) */
  src: string | null;
  /** map-plane offset X (в координатах canvas/workspace) */
  offsetX: number;
  /** map-plane offset Y */
  offsetY: number;
  /** uniform scale (1 = original size) */
  scale: number;
  /** rotation in degrees */
  rotation: number;
  /** opacity 0–100 */
  opacity: number;
  /** show/hide underlay */
  visible: boolean;
  /** lock underlay (запрет move/scale/rotate) */
  locked: boolean;
  /** natural image width (для placeholder = 720) */
  naturalWidth: number;
  /** natural image height (для placeholder = 460) */
  naturalHeight: number;
}

// ---- Editor settings (0020) ----

export interface EditorSettings {
  gridVisible: boolean;
  snapToGrid: boolean;
  gridSize: number;
}

// ---- MapDraft (updated for 0020) ----

export interface MapDraft {
  mapId: string;
  name: string;
  coordinateSystem: {
    type: "pixel";
    width: number;
    height: number;
  };
  spaces: SpaceDraft[];
  connections: ConnectionDraft[];
  /** 0020: underlay / terrain image */
  underlay: UnderlayState | null;
  /** 0020: editor settings (grid, snap) */
  editorSettings: EditorSettings;
}

// ---- Undo/redo snapshot (0020) ----

/**
 * Полный снимок MapDraft для undo/redo.
 * Borrowed from prototype: snapshot()/restore() pattern.
 */
export interface DraftSnapshot {
  mapId: string;
  name: string;
  coordinateSystem: { type: "pixel"; width: number; height: number };
  spaces: SpaceDraft[];
  connections: ConnectionDraft[];
  underlay: UnderlayState | null;
  editorSettings: EditorSettings;
}

export function takeSnapshot(draft: MapDraft): DraftSnapshot {
  return {
    mapId: draft.mapId,
    name: draft.name,
    coordinateSystem: { ...draft.coordinateSystem },
    spaces: draft.spaces.map((s) => ({ ...s })),
    connections: draft.connections.map((c) => ({ ...c })),
    underlay: draft.underlay ? { ...draft.underlay } : null,
    editorSettings: { ...draft.editorSettings },
  };
}

export function restoreSnapshot(snapshot: DraftSnapshot): MapDraft {
  return {
    mapId: snapshot.mapId,
    name: snapshot.name,
    coordinateSystem: { ...snapshot.coordinateSystem },
    spaces: snapshot.spaces.map((s) => ({ ...s })),
    connections: snapshot.connections.map((c) => ({ ...c })),
    underlay: snapshot.underlay ? { ...snapshot.underlay } : null,
    editorSettings: { ...snapshot.editorSettings },
  };
}

/** Максимальная глубина undo-истории */
export const HISTORY_LIMIT = 20;

export function pushHistory(
  past: DraftSnapshot[],
  draft: MapDraft
): DraftSnapshot[] {
  return [...past, takeSnapshot(draft)].slice(-HISTORY_LIMIT);
}

// ---- Map-plane transform helpers (0020) ----

/**
 * Преобразовать world-точку (canvas coordinate) в map-local (relative to underlay).
 *
 * 0020 correction: center-based inverse transform matching SVG render:
 *   render = translate(ox,oy) translate(cx,cy) scale(s) rotate(r) translate(-cx,-cy)
 *   inverse = translate(-ox,-oy) translate(-cx,-cy) scale(1/s) rotate(-r) translate(cx,cy)
 */
export function worldToMapLocal(
  worldX: number,
  worldY: number,
  underlay: UnderlayState | null
): { x: number; y: number } {
  if (!underlay) return { x: worldX, y: worldY };

  const cx = underlay.naturalWidth / 2;
  const cy = underlay.naturalHeight / 2;
  const s = underlay.scale || 1;
  const rad = (-underlay.rotation * Math.PI) / 180;
  const cos = Math.cos(rad);
  const sin = Math.sin(rad);

  // Inverse: undo translate(ox,oy) and translate(cx,cy), then scale, then rotate
  const tx = (worldX - underlay.offsetX - cx) / s;
  const ty = (worldY - underlay.offsetY - cy) / s;

  // Rotate by -rotation
  const rx = tx * cos - ty * sin;
  const ry = tx * sin + ty * cos;

  // Undo translate(-cx,-cy): add cx, cy
  return { x: rx + cx, y: ry + cy };
}

/**
 * Преобразовать map-local точку в world coordinate.
 *
 * 0020 correction: center-based forward transform matching SVG render.
 */
export function mapLocalToWorld(
  localX: number,
  localY: number,
  underlay: UnderlayState | null
): { x: number; y: number } {
  if (!underlay) return { x: localX, y: localY };

  const cx = underlay.naturalWidth / 2;
  const cy = underlay.naturalHeight / 2;
  const s = underlay.scale || 1;
  const rad = (underlay.rotation * Math.PI) / 180;
  const cos = Math.cos(rad);
  const sin = Math.sin(rad);

  // Forward: translate(-cx,-cy), rotate(r), scale(s), translate(cx,cy), translate(ox,oy)
  const dx = localX - cx;
  const dy = localY - cy;

  // Rotate
  const rx = dx * cos - dy * sin;
  const ry = dx * sin + dy * cos;

  // Scale and translate
  return {
    x: rx * s + cx + underlay.offsetX,
    y: ry * s + cy + underlay.offsetY,
  };
}

// ---- Default underlay factory (0020) ----

export const DEFAULT_UNDERLAY: UnderlayState = {
  src: null,
  offsetX: 260,
  offsetY: 180,
  scale: 1,
  rotation: 0,
  opacity: 94,
  visible: true,
  locked: false,
  naturalWidth: 720,
  naturalHeight: 460,
};

export const DEFAULT_EDITOR_SETTINGS: EditorSettings = {
  gridVisible: false,
  snapToGrid: false,
  gridSize: 28,
};

// ---- Загрузить MapDraft из fixture map.json (0018) ----

export function loadMapDraft(raw: {
  mapId: string;
  name: string;
  coordinateSystem: { type: string; width: number; height: number };
  spaces: Array<{
    spaceId: string;
    name: string;
    x: number;
    y: number;
    type: string;
  }>;
  connections: Array<{
    connectionId: string;
    fromSpaceId: string;
    toSpaceId: string;
    type: string;
  }>;
}): MapDraft {
  return {
    mapId: raw.mapId,
    name: raw.name,
    coordinateSystem: {
      type: "pixel",
      width: raw.coordinateSystem.width,
      height: raw.coordinateSystem.height,
    },
    spaces: raw.spaces.map((s) => ({
      spaceId: s.spaceId,
      name: s.name,
      x: s.x,
      y: s.y,
      type: s.type,
    })),
    connections: raw.connections.map((c) => ({
      connectionId: c.connectionId,
      fromSpaceId: c.fromSpaceId,
      toSpaceId: c.toSpaceId,
      type: c.type,
    })),
    // 0020: default underlay + editor settings
    underlay: { ...DEFAULT_UNDERLAY },
    editorSettings: { ...DEFAULT_EDITOR_SETTINGS },
  };
}

/** Утилита: сгенерировать уникальный ID с префиксом. */
export function uniqueId(
  prefix: string,
  existingIds: string[]
): string {
  const used = new Set(existingIds);
  if (!used.has(prefix)) return prefix;
  let i = 2;
  while (used.has(`${prefix}-${i}`)) i += 1;
  return `${prefix}-${i}`;
}

/** Результат валидации draft map. */
export interface MapValidation {
  errors: string[];
  warnings: string[];
}

/** Lightweight validation: duplicate IDs, broken refs, empty map. */
export function validateMapDraft(draft: MapDraft): MapValidation {
  const errors: string[] = [];
  const warnings: string[] = [];

  // Empty map check
  if (draft.spaces.length === 0) {
    warnings.push("Карта пуста: нет ни одной точки.");
  }

  // Duplicate space IDs
  const spaceIds = new Set<string>();
  for (const s of draft.spaces) {
    if (spaceIds.has(s.spaceId)) {
      errors.push(`Точка: повторяется ID «${s.spaceId}».`);
    }
    spaceIds.add(s.spaceId);
  }

  // Duplicate connection IDs
  const connIds = new Set<string>();
  for (const c of draft.connections) {
    if (connIds.has(c.connectionId)) {
      errors.push(`Связь: повторяется ID «${c.connectionId}».`);
    }
    connIds.add(c.connectionId);
  }

  // Broken connection refs
  for (const c of draft.connections) {
    if (!spaceIds.has(c.fromSpaceId)) {
      errors.push(
        `Связь «${c.connectionId}» ссылается на несуществующую точку «${c.fromSpaceId}».`
      );
    }
    if (!spaceIds.has(c.toSpaceId)) {
      errors.push(
        `Связь «${c.connectionId}» ссылается на несуществующую точку «${c.toSpaceId}».`
      );
    }
    if (c.fromSpaceId === c.toSpaceId) {
      errors.push(
        `Связь «${c.connectionId}» соединяет точку «${c.fromSpaceId}» саму с собой.`
      );
    }
  }

  return { errors, warnings };
}
