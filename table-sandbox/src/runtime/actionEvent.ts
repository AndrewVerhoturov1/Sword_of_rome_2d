/**
 * Action/Event runtime seam — placeholder для Phase 1 Technical Bootstrap.
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

/** Создать committed Event из Action (placeholder — без валидации в bootstrap) */
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

// ---- Validation placeholder ----

export type ValidationStatus = "allow" | "warn" | "block";

export interface ValidationResult {
  status: ValidationStatus;
  reasonCode: string;
}

/**
 * Placeholder-валидатор: всегда allow в bootstrap.
 * Реальная валидация появится в Phase 4 (Action/Event Spine).
 */
export function validateAction(_action: Action): ValidationResult {
  return { status: "allow", reasonCode: "bootstrap_permissive" };
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
