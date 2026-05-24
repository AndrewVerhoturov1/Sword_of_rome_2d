import type { GameState } from "../runtime/GameState";
import type { EventLog, Action } from "../runtime/actionEvent";

/**
 * DebugPanel — показывает текущий runtime state.
 *
 * Это доказательство, что GameState, Action/Event pipeline и Event Log
 * живут ВНЕ Phaser. Phaser не имеет к ним доступа.
 *
 * В bootstrap-режиме показывает только placeholder-данные.
 */

interface DebugPanelProps {
  gameState: GameState;
  lastAction: Action | null;
  eventLog: EventLog;
  lastClick: { x: number; y: number } | null;
}

export function DebugPanel({
  gameState,
  lastAction,
  eventLog,
  lastClick,
}: DebugPanelProps) {
  return (
    <div
      style={{
        background: "#0d1117",
        border: "1px solid #30363d",
        borderRadius: "6px",
        padding: "12px 16px",
        fontFamily: "monospace",
        fontSize: "12px",
        color: "#c9d1d9",
        maxHeight: "500px",
        overflowY: "auto",
      }}
    >
      <h3 style={{ margin: "0 0 8px", color: "#58a6ff", fontSize: "14px" }}>
        Runtime Debug Panel
      </h3>
      <p
        style={{
          margin: "0 0 12px",
          color: "#8b949e",
          fontSize: "11px",
          fontStyle: "italic",
        }}
      >
        Все данные ниже живут в React runtime, ВНЕ Phaser.
      </p>

      {/* GameState */}
      <Section title="GameState (authoritative)">
        <KV label="version" value={gameState.version} />
        <KV
          label="lastUpdated"
          value={new Date(gameState.lastUpdated).toISOString()}
        />
        <KV label="description" value={gameState.description} />
      </Section>

      {/* Last click from Phaser */}
      <Section title="Phaser Input (последний клик)">
        {lastClick ? (
          <KV
            label="coords"
            value={`x=${lastClick.x}, y=${lastClick.y}`}
          />
        ) : (
          <KV label="coords" value="— (нет кликов)" />
        )}
        <KV
          label="важно"
          value="Phaser только передал input. State не мутировал."
        />
      </Section>

      {/* Last Action */}
      <Section title="Action (последний запрос)">
        {lastAction ? (
          <>
            <KV label="actionId" value={lastAction.actionId} />
            <KV label="type" value={lastAction.type} />
            <KV label="actorId" value={lastAction.actorId} />
            <KV
              label="payload"
              value={JSON.stringify(lastAction.payload)}
            />
          </>
        ) : (
          <KV label="status" value="— action ещё не создан" />
        )}
        <KV
          label="важно"
          value="Action создан runtime'ом, не Phaser."
        />
      </Section>

      {/* Event Log */}
      <Section title={`Event Log (${eventLog.events.length} событий)`}>
        {eventLog.events.length === 0 ? (
          <KV label="status" value="— лог пуст" />
        ) : (
          eventLog.events.map((evt) => (
            <div
              key={evt.eventId}
              style={{
                marginBottom: "4px",
                padding: "4px 8px",
                background: "#161b22",
                borderRadius: "3px",
                fontSize: "11px",
              }}
            >
              [{evt.seq}] {evt.type} ← {evt.causedByActionId}
            </div>
          ))
        )}
        <KV
          label="важно"
          value="Event Log — append-only, живёт вне Phaser."
        />
      </Section>

      {/* Boundary confirmation */}
      <Section title="Boundary Check">
        <KV
          label="Phaser = source of truth?"
          value="НЕТ"
          important
        />
        <KV
          label="Runtime = source of truth?"
          value="ДА"
          important
        />
        <KV
          label="Граница"
          value="React shell → runtime state ↔ renderer input. Phaser только renderer."
        />
      </Section>
    </div>
  );
}

/** Маленький хелпер для строки ключ-значение */
function KV({
  label,
  value,
  important,
}: {
  label: string;
  value: string | number;
  important?: boolean;
}) {
  return (
    <div
      style={{
        display: "flex",
        gap: "8px",
        marginBottom: "2px",
        color: important ? "#f0883e" : undefined,
      }}
    >
      <span style={{ color: "#8b949e", minWidth: "100px", flexShrink: 0 }}>
        {label}:
      </span>
      <span
        style={{
          wordBreak: "break-all",
          fontWeight: important ? "bold" : undefined,
        }}
      >
        {String(value)}
      </span>
    </div>
  );
}

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div style={{ marginBottom: "12px" }}>
      <div
        style={{
          borderBottom: "1px solid #21262d",
          paddingBottom: "4px",
          marginBottom: "6px",
          color: "#79c0ff",
          fontWeight: "bold",
          fontSize: "12px",
        }}
      >
        {title}
      </div>
      {children}
    </div>
  );
}
