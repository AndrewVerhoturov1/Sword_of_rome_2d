import { useState, useCallback } from "react";
import { PhaserStage } from "./renderer/PhaserStage";
import { DebugPanel } from "./debug/DebugPanel";
import { type GameState } from "./runtime/GameState";
import { bootstrapGameState } from "./runtime/bootstrap";
import {
  createAction,
  createEvent,
  validateAction,
  createEventLog,
  appendEvent,
  type Action,
  type EventLog,
} from "./runtime/actionEvent";
import "./App.css";

/**
 * App — корневой React-компонент Table Sandbox 0.1.
 *
 * Владеет:
 *   - GameState (authoritative runtime state)
 *   - Action/Event pipeline
 *   - EventLog
 *
 * GameState инициализируется из canonical fixtures
 * (table-sandbox/src/fixtures/tiny-module/), не из placeholder.
 *
 * PhaserStage — только renderer/input, не владеет состоянием.
 */

export default function App() {
  const [gameState, setGameState] = useState<GameState>(bootstrapGameState);
  const [lastAction, setLastAction] = useState<Action | null>(null);
  const [eventLog, setEventLog] = useState<EventLog>(createEventLog);
  const [lastClick, setLastClick] = useState<{
    x: number;
    y: number;
  } | null>(null);

  /**
   * Обработчик клика из Phaser.
   * Phaser ТОЛЬКО передаёт координаты.
   * Runtime (этот код) создаёт Action → валидирует → коммитит Event.
   *
   * При обновлении GameState сохраняются все bootstrap-поля
   * (projectId, spaces, pieces, turn и т.д.).
   */
  const handleTableClick = useCallback(
    (x: number, y: number) => {
      setLastClick({ x: Math.round(x), y: Math.round(y) });

      // 1. Runtime создаёт Action (НЕ Phaser)
      const action = createAction("table_click", "user", {
        x: Math.round(x),
        y: Math.round(y),
      });

      // 2. Валидация
      const validation = validateAction(action);
      if (validation.status === "block") {
        setLastAction(action);
        return; // Заблокировано — не коммитим
      }

      // 3. Runtime коммитит Event
      const event = createEvent(action, "table_clicked");

      // 4. Обновляем EventLog
      setEventLog((prev) => {
        const updated = { events: [...prev.events] };
        appendEvent(updated, event);
        return updated;
      });

      // 5. Обновляем GameState (авторитетно, вне Phaser)
      // Сохраняем все bootstrap-поля, инкрементируем только version/lastUpdated.
      setGameState((prev) => ({
        ...prev,
        version: prev.version + 1,
        lastUpdated: Date.now(),
      }));

      setLastAction(action);
    },
    []
  );

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Table Sandbox 0.1</h1>
        <span className="app-badge">
          {gameState.projectId}/{gameState.scenarioId}
        </span>
      </header>

      <main className="app-main">
        <div className="table-area">
          <h2 className="area-label">Table Surface (Phaser Renderer)</h2>
          <PhaserStage onTableClick={handleTableClick} />
          <p className="area-hint">
            Кликни по таблице — runtime создаст Action, скоммитит Event и
            обновит GameState. Всё вне Phaser.
          </p>
        </div>

        <aside className="debug-area">
          <DebugPanel
            gameState={gameState}
            lastAction={lastAction}
            eventLog={eventLog}
            lastClick={lastClick}
          />
        </aside>
      </main>

      <footer className="app-footer">
        <span>GameState version: {gameState.version}</span>
        <span className="footer-sep">|</span>
        <span>
          {gameState.projectId}/{gameState.moduleId}/{gameState.mapId}/
          {gameState.scenarioId}
        </span>
        <span className="footer-sep">|</span>
        <span>Events: {eventLog.events.length}</span>
        <span className="footer-sep">|</span>
        <span>Источник истины: Runtime (React state), НЕ Phaser</span>
      </footer>
    </div>
  );
}
