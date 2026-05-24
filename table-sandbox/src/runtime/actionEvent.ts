/**
 * Action/Event runtime seam — first Action/Event Spine slice (0011).
 *
 * Action  = запрос / намерение.
 * Event   = подтверждённый факт.
 *
 * Правило: ни один Phaser scene object не создаёт Action/Event напрямую.
 * Только runtime (вне Phaser) может создавать Action и коммитить Event.
 *
 * Handoff 0012: validateAction перенесён в RulesHooks (rulesHooks.ts).
 * Runtime теперь спрашивает rules shim для validate и resolve,
 * а сам коммитит event и применяет reducer.
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

/** Создать Action типа create_piece_requested */
export function createCreatePieceAction(
  spaceId: string,
  pieceDefId: string,
  ownerId: string,
  actorId: string
): Action {
  return createAction("create_piece_requested", actorId, {
    spaceId,
    pieceDefId,
    ownerId,
  });
}

/** Создать Action типа delete_piece_requested */
export function createDeletePieceAction(
  pieceId: string,
  actorId: string
): Action {
  return createAction("delete_piece_requested", actorId, {
    pieceId,
  });
}

/** Создать Action типа change_control_requested */
export function createChangeControlAction(
  spaceId: string,
  newOwnerId: string | null,
  actorId: string
): Action {
  return createAction("change_control_requested", actorId, {
    spaceId,
    newOwnerId,
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

/**
 * Сбросить _eventSeq до указанного значения.
 * Используется при restore из snapshot, чтобы следующие новые события
 * продолжали монотонную нумерацию.
 */
export function resetEventSeq(nextSeq: number): void {
  _eventSeq = nextSeq;
}

/**
 * Сбросить _actionSeq до указанного значения.
 * Используется при restore из snapshot.
 */
export function resetActionSeq(nextSeq: number): void {
  _actionSeq = nextSeq;
}

/**
 * Создать committed Event из Action.
 *
 * Если payload передан явно, используется он.
 * Иначе payload копируется из action.payload (поведение по умолчанию).
 *
 * Это позволяет RulesHooks.resolveAction(...) предлагать свой payload,
 * отличный от action.payload, если нужно.
 */
export function createEvent(
  action: Action,
  eventType: string,
  payload?: Record<string, unknown>
): Event {
  _eventSeq++;
  return {
    eventId: `event-${_eventSeq}`,
    seq: _eventSeq,
    type: eventType,
    payload: payload ?? { ...action.payload },
    causedByActionId: action.actionId,
    timestamp: Date.now(),
  };
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

    case "piece_created": {
      const { pieceId, pieceDefId, locationId, ownerId, count } = event.payload;
      if (
        typeof pieceId !== "string" ||
        typeof pieceDefId !== "string" ||
        typeof locationId !== "string" ||
        typeof ownerId !== "string"
      ) {
        return state;
      }
      const countNum = typeof count === "number" ? count : 1;
      const newPiece = {
        pieceId,
        pieceDefId,
        locationId,
        ownerId,
        count: countNum,
      };
      return {
        ...state,
        version: state.version + 1,
        lastUpdated: Date.now(),
        pieces: [...state.pieces, newPiece],
      };
    }

    case "piece_deleted": {
      const { pieceId } = event.payload;
      if (typeof pieceId !== "string") {
        return state;
      }
      return {
        ...state,
        version: state.version + 1,
        lastUpdated: Date.now(),
        pieces: state.pieces.filter((p) => p.pieceId !== pieceId),
      };
    }

    case "control_changed": {
      const { spaceId, newOwnerId } = event.payload;
      if (typeof spaceId !== "string") {
        return state;
      }
      // newOwnerId может быть null (сброс контроля)
      const owner =
        typeof newOwnerId === "string" ? newOwnerId : null;
      return {
        ...state,
        version: state.version + 1,
        lastUpdated: Date.now(),
        controlState: {
          ...state.controlState,
          [spaceId]: owner,
        },
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
