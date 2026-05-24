/**
 * Action/Event runtime seam — first Action/Event Spine slice (0011).
 *
 * Action  = запрос / намерение.
 * Event   = подтверждённый факт.
 *
 * Правило: ни один Phaser scene object не создаёт Action/Event напрямую.
 * Только runtime (вне Phaser) может создавать Action и коммитить Event.
 *
 * Полный контракт описан в:
 * .ai/plans/master/action_event_contract.md
 */

import type { GameState } from "./GameState";

// ---- Action ----

export interface Action {
  actionId: string;
  type: string;
  actorId: string;
  payload: Record<string, unknown>;
  timestamp: number;
}

/** Создать actionId (временный sequential для bootstrap) */
let _actionSeq = 0;
export function createAction(
  type: string,
  actorId: string,
  payload: Record<string, unknown>
): Action {
  _actionSeq++;
  return {
    actionId: `action-${_actionSeq}`,
    type,
    actorId,
    payload,
    timestamp: Date.now(),
  };
}

// ---- Canonical action helpers ----

/** Создать Action типа move_piece_requested */
export function createMovePieceAction(
  pieceId: string,
  fromLocationId: string,
  toLocationId: string,
  actorId: string
): Action {
  return createAction("move_piece_requested", actorId, {
    pieceId,
    fromLocationId,
    toLocationId,
  });
}

// ---- Event ----

export interface Event {
  eventId: string;
  seq: number;
  type: string;
  payload: Record<string, unknown>;
  causedByActionId: string;
  timestamp: number;
}

/** Монотонный счётчик коммитов */
let _eventSeq = 0;

/** Создать committed Event из Action */
export function createEvent(action: Action, eventType: string): Event {
  _eventSeq++;
  return {
    eventId: `event-${_eventSeq}`,
    seq: _eventSeq,
    type: eventType,
    payload: { ...action.payload },
    causedByActionId: action.actionId,
    timestamp: Date.now(),
  };
}

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
 * В будущем валидация будет передана RulesHooks.
 */
export function validateAction(
  action: Action,
  state?: GameState
): ValidationResult {
  if (action.type === "move_piece_requested") {
    const { pieceId, fromLocationId, toLocationId } = action.payload;
    if (!pieceId || !fromLocationId || !toLocationId) {
      return { status: "block", reasonCode: "move_piece_requested_missing_payload" };
    }
    if (state) {
      const piece = state.pieces.find((p) => p.pieceId === pieceId);
      if (!piece) {
        return { status: "block", reasonCode: "move_piece_requested_unknown_piece" };
      }
      if (piece.locationId !== fromLocationId) {
        return {
          status: "warn",
          reasonCode: "move_piece_requested_location_mismatch",
        };
      }
    }
    return { status: "allow", reasonCode: "move_piece_requested_permissive_allow" };
  }

  // Все остальные типы — permissive allow
  return { status: "allow", reasonCode: "bootstrap_permissive" };
}

// ---- Reducer ----

/**
 * Применить committed Event к GameState.
 *
 * Единственный путь мутации GameState — через этот reducer.
 * Phaser, RulesHooks и UI-компоненты не мутируют GameState напрямую.
 */
export function reduceEvent(state: GameState, event: Event): GameState {
  switch (event.type) {
    case "piece_moved": {
      const { pieceId, toLocationId } = event.payload;
      if (typeof pieceId !== "string" || typeof toLocationId !== "string") {
        return state; // некорректный payload — не мутируем
      }
      return {
        ...state,
        version: state.version + 1,
        lastUpdated: Date.now(),
        pieces: state.pieces.map((p) =>
          p.pieceId === pieceId ? { ...p, locationId: toLocationId } : p
        ),
      };
    }
    default:
      return state;
  }
}

// ---- Event Log ----

export interface EventLog {
  events: Event[];
}

export function createEventLog(): EventLog {
  return { events: [] };
}

export function appendEvent(log: EventLog, event: Event): void {
  log.events.push(event);
}
