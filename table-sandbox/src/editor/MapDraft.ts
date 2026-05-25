/**
 * MapDraft — authoring draft state for Map Authoring 0.1.
 *
 * Живёт ОТДЕЛЬНО от runtime GameState.
 * GameState — authoritative runtime state (read-only для editor).
 * MapDraft — editable authoring state.
 *
 * Preview: MapDraft → временный GameState (через draftToGameState).
 * Обратного пути нет: GameState не пишет в MapDraft.
 *
 * Borrowed pattern: prototype's flat space/connection arrays,
 * но без layers/zones/styling.
 */

export interface SpaceDraft {
  spaceId: string;
  name: string;
  x: number;
  y: number;
  type: string;
}

export interface ConnectionDraft {
  connectionId: string;
  fromSpaceId: string;
  toSpaceId: string;
  type: string;
}

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
}

/** Загрузить MapDraft из fixture map.json. */
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
