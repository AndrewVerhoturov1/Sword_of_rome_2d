import { useState, useCallback } from "react";
import { PhaserStage } from "./renderer/PhaserStage";
import { DebugPanel } from "./debug/DebugPanel";
import { type GameState } from "./runtime/GameState";
import { bootstrapGameState } from "./runtime/bootstrap";
import {
  createMovePieceAction,
  createEvent,
  validateAction,
  reduceEvent,
  createEventLog,
  appendEvent,
  type Action,
  type EventLog,
} from "./runtime/actionEvent";
import "./App.css";

/**
 * App — корневой React-компонент Table Sandbox 0.1 (Action/Event Spine).
 *
 * Владеет:
 *   - GameState (authoritative runtime state)
 *   - Action/Event pipeline
 *   - EventLog
 *   - Selection state (selectedPieceId)
 *
 * GameState инициализируется из canonical fixtures
 * (table-sandbox/src/fixtures/tiny-module/), не из placeholder.
 *
 * PhaserStage — только renderer/input, не владеет состоянием.
 *
 * Первый move slice UX:
 *   1. Клик по space с фишкой → выбор фишки (подсветка)
 *   2. Клик по другому space → move_piece_requested → piece_moved → redraw
 */

export default function App() {
  const [gameState, setGameState] = useState<GameState>(bootstrapGameState);
  const [lastAction, setLastAction] = useState<Action | null>(null);
  const [eventLog, setEventLog] = useState<EventLog>(createEventLog);
  const [selectedPieceId, setSelectedPieceId] = useState<string | null>(null);

  /**
   * Обработчик клика по space из Phaser.
   *
   * Двухшаговый UX:
   *   Шаг 1 — если фишка не выбрана и кликнутый space содержит фишку:
   *            выбрать эту фишку.
   *   Шаг 2 — если фишка уже выбрана и кликнут другой space:
   *            создать move_piece_requested → провалидировать →
   *            скоммитить piece_moved → reduce GameState → обновить event log.
   *
   * Phaser НЕ мутирует GameState. Только runtime коммитит события.
   */
  const handleSpaceClick = useCallback(
    (spaceId: string) => {
      // Шаг 1: ничего не выбрано — проверить, есть ли фишка в этом space
      if (!selectedPieceId) {
        const pieceOnSpace = gameState.pieces.find(
          (p) => p.locationId === spaceId
        );
        if (pieceOnSpace) {
          setSelectedPieceId(pieceOnSpace.pieceId);
        }
        return;
      }

      // Шаг 2: фишка выбрана
      const piece = gameState.pieces.find(
        (p) => p.pieceId === selectedPieceId
      );
      if (!piece) {
        setSelectedPieceId(null);
        return;
      }

      // Клик по тому же space — отмена выбора
      if (piece.locationId === spaceId) {
        setSelectedPieceId(null);
        return;
      }

      // Создать move_piece_requested Action
      const action = createMovePieceAction(
        piece.pieceId,
        piece.locationId,
        spaceId,
        "user"
      );

      // Валидация
      const validation = validateAction(action, gameState);
      if (validation.status === "block") {
        setLastAction(action);
        setSelectedPieceId(null);
        return;
      }

      // Коммитим piece_moved Event
      const event = createEvent(action, "piece_moved");

      // Обновляем EventLog
      setEventLog((prev) => {
        const updated = { events: [...prev.events] };
        appendEvent(updated, event);
        return updated;
      });

      // Reducer: применяем event к GameState (единственный путь мутации)
      setGameState((prev) => reduceEvent(prev, event));

      setLastAction(action);
      setSelectedPieceId(null);
    },
    [gameState, selectedPieceId]
  );

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Table Sandbox 0.1 — Action/Event Spine</h1>
        <span className="app-badge">
          {gameState.projectId}/{gameState.scenarioId}
        </span>
      </header>

      <main className="app-main">
        <div className="table-area">
          <h2 className="area-label">Table Surface (Phaser Renderer)</h2>
          <PhaserStage
            gameState={gameState}
            selectedPieceId={selectedPieceId}
            onSpaceClick={handleSpaceClick}
          />
          <p className="area-hint">
            {selectedPieceId
              ? `Выбрана фишка: ${selectedPieceId}. Кликни по другому space для перемещения.`
              : "Кликни по space с фишкой, чтобы выбрать её, затем по целевому space для перемещения."}
          </p>
        </div>

        <aside className="debug-area">
          <DebugPanel
            gameState={gameState}
            lastAction={lastAction}
            eventLog={eventLog}
            selectedPieceId={selectedPieceId}
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
