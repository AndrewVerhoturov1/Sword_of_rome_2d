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
  if (action.type === "move_piece_requested") {
    const { pieceId, fromLocationId, toLocationId } = action.payload;
    if (!pieceId || !fromLocationId || !toLocationId) {
      return {
        status: "block",
        reasonCode: "move_piece_requested_missing_payload",
      };
    }
    if (state) {
      const piece = state.pieces.find((p) => p.pieceId === pieceId);
      if (!piece) {
        return {
          status: "block",
          reasonCode: "move_piece_requested_unknown_piece",
        };
      }
      if (piece.locationId !== fromLocationId) {
        return {
          status: "warn",
          reasonCode: "move_piece_requested_location_mismatch",
        };
      }
    }
    return {
      status: "allow",
      reasonCode: "move_piece_requested_permissive_allow",
    };
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
    default:
      // Неизвестный action type — нет proposed events.
      // Runtime не должен коммитить ничего.
      return [];
  }
}
