/**
 * sanityCheck.ts — lightweight bootstrap validation (Handoff 0017).
 *
 * Проверяет базовую согласованность загруженных fixture-данных
 * ПОСЛЕ bootstrap, но ДО того как GameState попадёт в React.
 *
 * Это не schema framework. Только минимальные проверки:
 *   - pieces ссылаются на существующие spaces;
 *   - controlBySpace ссылается на существующие spaces;
 *   - scenario.mapId совпадает с map.mapId.
 *
 * При обнаружении проблем возвращает русские сообщения.
 * App не падает — сообщения показываются в UI.
 */

import type { SpaceState, PieceState, ControlState } from "./GameState";

export interface SanityIssue {
  level: "error" | "warning";
  /** Русское сообщение для пользователя */
  message: string;
}

/**
 * Проверить согласованность загруженных данных.
 * Вызывается один раз после bootstrapGameState().
 */
export function validateBootstrap(args: {
  spaces: SpaceState[];
  pieces: PieceState[];
  controlState: ControlState;
  scenarioMapId: string;
  mapMapId: string;
}): SanityIssue[] {
  const issues: SanityIssue[] = [];
  const spaceIds = new Set(args.spaces.map((s) => s.spaceId));

  // 1. Каждая piece должна быть на существующем space
  for (const p of args.pieces) {
    if (!spaceIds.has(p.locationId)) {
      issues.push({
        level: "error",
        message: `Фишка «${p.pieceId}» ссылается на несуществующую точку «${p.locationId}».`,
      });
    }
  }

  // 2. Каждый ключ controlBySpace должен быть существующим space
  for (const spaceId of Object.keys(args.controlState)) {
    if (!spaceIds.has(spaceId)) {
      issues.push({
        level: "warning",
        message: `Контроль задан для несуществующей точки «${spaceId}».`,
      });
    }
  }

  // 3. scenario.mapId должен совпадать с map.mapId
  if (args.scenarioMapId !== args.mapMapId) {
    issues.push({
      level: "warning",
      message: `Сценарий ссылается на карту «${args.scenarioMapId}», но загружена карта «${args.mapMapId}».`,
    });
  }

  return issues;
}

/**
 * Форматировать список проблем в одну строку для показа пользователю.
 * Возвращает null если проблем нет.
 */
export function formatSanityIssues(issues: SanityIssue[]): string | null {
  if (issues.length === 0) return null;

  const errors = issues.filter((i) => i.level === "error");
  const warnings = issues.filter((i) => i.level === "warning");

  const parts: string[] = [];
  if (errors.length > 0) {
    parts.push(
      `Ошибок загрузки: ${errors.length}. ${errors.map((e) => e.message).join(" ")}`
    );
  }
  if (warnings.length > 0) {
    parts.push(
      `Предупреждений: ${warnings.length}. ${warnings.map((w) => w.message).join(" ")}`
    );
  }
  return parts.join(" ");
}
