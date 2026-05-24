/**
 * RulesHooks — minimal permissive rules shim (Handoff 0012).
 *
 * Runtime asks; rules answer; runtime commits and applies.
 *
 * Этот файл — boundary между universal runtime и module-specific rules.
 * Для Table Sandbox 0.1 пока содержит только permissive-логику.
 *
 * Полный контракт описан в:
 * .ai/plans/master/rules_hooks_interface.md
 * .ai/plans/master/action_event_contract.md
 */

import type { Action } from "./actionEvent";
import type { GameState } from "./GameState";

// ---- Validation ----

export type ValidationStatus = "allow" | "warn" | "block";

export interface ValidationResult {
  status: ValidationStatus;
  reasonCode: string;
}

/**
 * Permissive-валидатор для первого Action/Event Spine slice.
 *
 * Для move_piece_requested проверяет:
 *  - наличие pieceId, fromLocationId, toLocationId в payload;
 *  - piece существует в GameState.
 *
 * Для всех остальных action — permissive allow.
 *
 * В будущем эта функция будет расширена для более строгих проверок
 * (graph-aware, phase-aware и т.д.).
 */
export function validateAction(
  action: Action,
  state?: GameState
): ValidationResult {
  // ---- move_piece_requested ----
  if (action.type === "move_piece_requested") {
    const { pieceId, fromLocationId, toLocationId } = action.payload;
    if (
      typeof pieceId !== "string" ||
      typeof fromLocationId !== "string" ||
      typeof toLocationId !== "string"
    ) {
      return {
        status: "block",
        reasonCode: "move_piece_requested_missing_payload",
      };
    }

    if (!state) {
      return {
        status: "allow",
        reasonCode: "move_piece_requested_permissive_allow",
      };
    }

    const piece = state.pieces.find((p) => p.pieceId === pieceId);
    if (!piece) {
      return {
        status: "block",
        reasonCode: "move_piece_requested_unknown_piece",
      };
    }

    if (piece.locationId !== fromLocationId) {
      return {
        status: "block",
        reasonCode: "move_piece_requested_location_mismatch",
      };
    }

    const fromSpaceExists = state.spaces.some(
      (space) => space.spaceId === fromLocationId
    );
    if (!fromSpaceExists) {
      return {
        status: "block",
        reasonCode: "move_piece_requested_unknown_from_space",
      };
    }

    const toSpaceExists = state.spaces.some(
      (space) => space.spaceId === toLocationId
    );
    if (!toSpaceExists) {
      return {
        status: "block",
        reasonCode: "move_piece_requested_unknown_to_space",
      };
    }

    const hasConnection = state.connections.some(
      (connection) =>
        (connection.fromSpaceId === fromLocationId &&
          connection.toSpaceId === toLocationId) ||
        (connection.fromSpaceId === toLocationId &&
          connection.toSpaceId === fromLocationId)
    );
    if (!hasConnection) {
      return {
        status: "block",
        reasonCode: "move_piece_requested_no_connection",
      };
    }

    return {
      status: "allow",
      reasonCode: "move_piece_requested_graph_allow",
    };
  }

  // ---- create_piece_requested ----
  if (action.type === "create_piece_requested") {
    const { spaceId, pieceDefId, ownerId } = action.payload;
    if (
      typeof spaceId !== "string" ||
      typeof pieceDefId !== "string" ||
      typeof ownerId !== "string"
    ) {
      return {
        status: "block",
        reasonCode: "create_piece_requested_missing_payload",
      };
    }

    if (!state) {
      return { status: "allow", reasonCode: "create_piece_requested_permissive_allow" };
    }

    const spaceExists = state.spaces.some((s) => s.spaceId === spaceId);
    if (!spaceExists) {
      return {
        status: "block",
        reasonCode: "create_piece_requested_unknown_space",
      };
    }

    return { status: "allow", reasonCode: "create_piece_requested_allow" };
  }

  // ---- delete_piece_requested ----
  if (action.type === "delete_piece_requested") {
    const { pieceId } = action.payload;
    if (typeof pieceId !== "string") {
      return {
        status: "block",
        reasonCode: "delete_piece_requested_missing_payload",
      };
    }

    if (!state) {
      return { status: "allow", reasonCode: "delete_piece_requested_permissive_allow" };
    }

    const piece = state.pieces.find((p) => p.pieceId === pieceId);
    if (!piece) {
      return {
        status: "block",
        reasonCode: "delete_piece_requested_unknown_piece",
      };
    }

    return { status: "allow", reasonCode: "delete_piece_requested_allow" };
  }

  // ---- change_control_requested ----
  if (action.type === "change_control_requested") {
    const { spaceId } = action.payload;
    if (typeof spaceId !== "string") {
      return {
        status: "block",
        reasonCode: "change_control_requested_missing_payload",
      };
    }
    // newOwnerId может быть null — это допустимо (сброс контроля)

    if (!state) {
      return { status: "allow", reasonCode: "change_control_requested_permissive_allow" };
    }

    const spaceExists = state.spaces.some((s) => s.spaceId === spaceId);
    if (!spaceExists) {
      return {
        status: "block",
        reasonCode: "change_control_requested_unknown_space",
      };
    }

    return { status: "allow", reasonCode: "change_control_requested_allow" };
  }

  // Все остальные типы — permissive allow
  return { status: "allow", reasonCode: "bootstrap_permissive" };
}

// ---- Resolution ----

export interface ProposedEvent {
  /** Тип события (например, "piece_moved") */
  eventType: string;
  /** Опциональный payload. Если не указан, runtime использует action.payload. */
  payload?: Record<string, unknown>;
}

/**
 * Permissive-resolver: преобразует валидированный Action в proposed events.
 *
 * Rules layer возвращает proposed events, но НЕ коммитит их.
 * Runtime сам создаёт Event из proposed, коммитит и применяет reducer.
 *
 * Для move_piece_requested: возвращает один proposed event "piece_moved"
 * с сохранением исходного action.payload.
 */
export function resolveAction(
  action: Action,
  _state: GameState
): ProposedEvent[] {
  switch (action.type) {
    case "move_piece_requested": {
      return [{ eventType: "piece_moved" }];
    }
    case "create_piece_requested": {
      // pieceId генерируется снаружи (App), передаётся через payload
      // rules layer не генерирует pieceId
      return [{ eventType: "piece_created" }];
    }
    case "delete_piece_requested": {
      return [{ eventType: "piece_deleted" }];
    }
    case "change_control_requested": {
      return [{ eventType: "control_changed" }];
    }
    default:
      // Неизвестный action type — нет proposed events.
      // Runtime не должен коммитить ничего.
      return [];
  }
}
