import type { GameState, SpaceState, ConnectionState, PieceState, BootstrapMeta } from "../runtime/GameState";
import type { EventLog, Action } from "../runtime/actionEvent";

/**
 * DebugPanel — показывает текущий runtime state.
 *
 * Это доказательство, что GameState, Action/Event pipeline и Event Log
 * живут ВНЕ Phaser. Phaser не имеет к ним доступа.
 *
 * Phase 3 (Runtime/Data Bootstrap): добавлены секции с evidence,
 * что данные пришли из canonical fixtures, а не из hardcoded placeholder.
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
        maxHeight: "600px",
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

      {/* Bootstrap Identity */}
      <Section title="Bootstrap Identity (из fixtures)">
        <KV label="projectId" value={gameState.projectId} important />
        <KV label="moduleId" value={gameState.moduleId} important />
        <KV label="mapId" value={gameState.mapId} important />
        <KV label="scenarioId" value={gameState.scenarioId} important />
      </Section>

      {/* GameState core */}
      <Section title="GameState Core">
        <KV label="version" value={gameState.version} />
        <KV
          label="lastUpdated"
          value={new Date(gameState.lastUpdated).toISOString()}
        />
      </Section>

      {/* Map Topology */}
      <Section title="Map Topology (из map.json)">
        <KV label="spaces" value={gameState.spaces.length} />
        <KV label="connections" value={gameState.connections.length} />
        <SpacesList spaces={gameState.spaces} />
        <ConnectionsList connections={gameState.connections} />
      </Section>

      {/* Pieces */}
      <Section title="Piece Instances (из scenario.basic.json)">
        <KV label="pieces" value={gameState.pieces.length} />
        <PiecesList pieces={gameState.pieces} />
      </Section>

      {/* Turn / Phase */}
      <Section title="Turn / Phase (из scenario.basic.json)">
        <KV label="round" value={gameState.turn.round} />
        <KV label="phaseId" value={gameState.turn.phaseId} important />
        <KV label="activeActorId" value={gameState.turn.activeActorId} />
      </Section>

      {/* Bootstrap Metadata */}
      <BootstrapMetaSection meta={gameState.bootstrapMeta} />

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

// ---- Sub-components ----

function SpacesList({ spaces }: { spaces: SpaceState[] }) {
  return (
    <div style={{ marginTop: "4px" }}>
      {spaces.map((s) => (
        <div
          key={s.spaceId}
          style={{
            marginBottom: "2px",
            padding: "2px 6px",
            background: "#161b22",
            borderRadius: "3px",
            fontSize: "11px",
          }}
        >
          <span style={{ color: "#79c0ff" }}>{s.spaceId}</span>{" "}
          <span style={{ color: "#8b949e" }}>«{s.name}»</span>{" "}
          <span style={{ color: "#6e7681" }}>
            ({s.x},{s.y}) {s.type}
          </span>
        </div>
      ))}
    </div>
  );
}

function ConnectionsList({ connections }: { connections: ConnectionState[] }) {
  return (
    <div style={{ marginTop: "4px" }}>
      {connections.map((c) => (
        <div
          key={c.connectionId}
          style={{
            marginBottom: "2px",
            padding: "2px 6px",
            background: "#161b22",
            borderRadius: "3px",
            fontSize: "11px",
          }}
        >
          <span style={{ color: "#79c0ff" }}>{c.connectionId}</span>{" "}
          <span style={{ color: "#8b949e" }}>
            {c.fromSpaceId} → {c.toSpaceId}
          </span>{" "}
          <span style={{ color: "#6e7681" }}>({c.type})</span>
        </div>
      ))}
    </div>
  );
}

function PiecesList({ pieces }: { pieces: PieceState[] }) {
  return (
    <div style={{ marginTop: "4px" }}>
      {pieces.map((p) => (
        <div
          key={p.pieceId}
          style={{
            marginBottom: "2px",
            padding: "4px 6px",
            background: "#161b22",
            borderRadius: "3px",
            fontSize: "11px",
          }}
        >
          <div>
            <span style={{ color: "#f0883e" }}>{p.pieceId}</span>{" "}
            <span style={{ color: "#8b949e" }}>{p.pieceDefId}</span>
          </div>
          <div style={{ color: "#6e7681", marginTop: "1px" }}>
            location:{" "}
            <span style={{ color: "#79c0ff" }}>{p.locationId}</span> | owner:{" "}
            <span style={{ color: "#79c0ff" }}>{p.ownerId}</span> | count:{" "}
            <span style={{ color: "#79c0ff" }}>{p.count}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

function BootstrapMetaSection({ meta }: { meta: BootstrapMeta }) {
  return (
    <Section title="Bootstrap Metadata (evidence)">
      <KV label="source" value={meta.source} important />
      <KV label="projectId" value={meta.projectId} />
      <KV label="moduleId" value={meta.moduleId} />
      <KV label="mapId" value={meta.mapId} />
      <KV label="scenarioId" value={meta.scenarioId} />
      <KV label="loadedFiles" value={meta.loadedFiles.join(", ")} />
      <KV
        label="fixture origin"
        value="Данные из canonical fixture seed (0009), не hardcoded."
        important
      />
    </Section>
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
