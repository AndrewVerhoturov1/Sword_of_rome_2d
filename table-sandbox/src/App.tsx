import { useState, useCallback, useRef } from "react";
import { PhaserStage } from "./renderer/PhaserStage";
import { DebugPanel } from "./debug/DebugPanel";
import { type GameState } from "./runtime/GameState";
import { bootstrapGameState } from "./runtime/bootstrap";
import {
  createMovePieceAction,
  createCreatePieceAction,
  createDeletePieceAction,
  createChangeControlAction,
  createEvent,
  reduceEvent,
  createEventLog,
  appendEvent,
  resetActionSeq,
  resetEventSeq,
  type Action,
  type EventLog,
} from "./runtime/actionEvent";
import { validateAction, resolveAction } from "./runtime/rulesHooks";
import { saveSnapshot, loadSnapshot } from "./runtime/snapshot";
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
 * Handoff 0012: rules boundary стала явной.
 * Flow: runtime asks rules.validateAction → rules.resolveAction → runtime commits.
 *
 * Первый move slice UX:
 *   1. Клик по space с фишкой → выбор фишки (подсветка)
 *   2. Клик по другому space → move_piece_requested → validate → resolve → piece_moved → redraw
 */

export default function App() {
  const [gameState, setGameState] = useState<GameState>(bootstrapGameState);
  const [lastAction, setLastAction] = useState<Action | null>(null);
  const [eventLog, setEventLog] = useState<EventLog>(createEventLog);
  const [selectedPieceId, setSelectedPieceId] = useState<string | null>(null);
  const [selectedSpaceId, setSelectedSpaceId] = useState<string | null>(null);
  const [snapshotStatus, setSnapshotStatus] = useState<string | null>(null);
  const [validationMessage, setValidationMessage] = useState<string | null>(null);

  /** Монотонный счётчик для генерации pieceId */
  const nextPieceSeqRef = useRef<number>(2);

  /** Русский текст для reasonCode */
  const getValidationMessage = useCallback((reasonCode: string): string => {
    const map: Record<string, string> = {
      "move_piece_requested_missing_payload": "Перемещение: не указана фишка или точка.",
      "move_piece_requested_unknown_piece": "Перемещение: фишка не найдена.",
      "move_piece_requested_location_mismatch": "Перемещение: фишка не в той точке.",
      "move_piece_requested_unknown_from_space": "Перемещение: исходная точка не существует.",
      "move_piece_requested_unknown_to_space": "Перемещение: целевая точка не существует.",
      "move_piece_requested_no_connection": "Перемещение: нет пути между точками.",
      "create_piece_requested_missing_payload": "Создание фишки: не указаны точка, тип или владелец.",
      "create_piece_requested_unknown_space": "Создание фишки: точка не существует. Сначала выбери точку на карте.",
      "delete_piece_requested_missing_payload": "Удаление фишки: не указана фишка.",
      "delete_piece_requested_unknown_piece": "Удаление фишки: фишка не найдена. Сначала выбери фишку.",
      "change_control_requested_missing_payload": "Смена контроля: не указана точка.",
      "change_control_requested_unknown_space": "Смена контроля: точка не существует. Сначала выбери точку на карте.",
    };
    return map[reasonCode] ?? `Ошибка: ${reasonCode}`;
  }, []);

  /**
   * Выполнить полный цикл Action → validate → resolve → commit.
   * Возвращает true если действие было выполнено, false если заблокировано.
   */
  const commitAction = useCallback(
    (action: Action, pieceIdForCreate?: string, ownerForCreate?: string): boolean => {
      const validation = validateAction(action, gameState);
      if (validation.status === "block") {
        setLastAction(action);
        setValidationMessage(getValidationMessage(validation.reasonCode));
        return false;
      }

      const proposedEvents = resolveAction(action, gameState);

      for (const proposed of proposedEvents) {
        // Для piece_created дополняем payload: маппим spaceId → locationId,
        // добавляем pieceId и count.
        let payload: Record<string, unknown> | undefined;
        if (proposed.eventType === "piece_created" && pieceIdForCreate && ownerForCreate) {
          payload = {
            ...action.payload,
            locationId: action.payload.spaceId,
            pieceId: pieceIdForCreate,
            count: 1,
          };
        }

        const event = createEvent(action, proposed.eventType, payload);

        setEventLog((prev) => {
          const updated = { events: [...prev.events] };
          appendEvent(updated, event);
          return updated;
        });

        setGameState((prev) => reduceEvent(prev, event));
      }

      setLastAction(action);
      setValidationMessage(null);
      return true;
    },
    [gameState, getValidationMessage]
  );

  /**
   * Сохранить текущий runtime snapshot в localStorage.
   */
  const handleSave = useCallback(() => {
    const result = saveSnapshot(gameState, eventLog);
    setSnapshotStatus(result.message);
  }, [gameState, eventLog]);

  /**
   * Загрузить runtime snapshot из localStorage.
   *
   * Восстанавливает GameState и EventLog.
   * Сбрасывает монотонные счётчики.
   * Мигрирует старые snapshot без controlState (P1).
   * Восстанавливает nextPieceSeq из всей истории (pieces + event log) (P2).
   */
  const handleLoad = useCallback(() => {
    const result = loadSnapshot();
    setSnapshotStatus(result.message);

    if (result.ok && result.snapshot) {
      const { gameState: loadedGS, eventLog: loadedEL } = result.snapshot;

      // P1: миграция старого snapshot без controlState (handoff 0014)
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      if (!(loadedGS as any).controlState) {
        (loadedGS as any).controlState = {};
      }

      // Сброс монотонных счётчиков на максимум из загруженного лога
      if (loadedEL.events.length > 0) {
        const maxSeq = Math.max(...loadedEL.events.map((e) => e.seq));
        resetActionSeq(maxSeq);
        resetEventSeq(maxSeq);
      }

      // P2: восстановить nextPieceSeq из всей истории (pieces + event log)
      let maxPieceNum = 0;
      // Из живых pieces
      for (const p of loadedGS.pieces) {
        const match = p.pieceId.match(/^piece-(\d+)$/);
        if (match) {
          maxPieceNum = Math.max(maxPieceNum, parseInt(match[1], 10));
        }
      }
      // Из истории событий (включая удалённые фишки)
      for (const evt of loadedEL.events) {
        if (evt.type === "piece_created" && typeof evt.payload.pieceId === "string") {
          const match = (evt.payload.pieceId as string).match(/^piece-(\d+)$/);
          if (match) {
            maxPieceNum = Math.max(maxPieceNum, parseInt(match[1], 10));
          }
        }
      }
      nextPieceSeqRef.current = maxPieceNum + 1;

      setGameState(loadedGS);
      setEventLog(loadedEL);
      setLastAction(null);
      setSelectedPieceId(null);
      setSelectedSpaceId(null);
      setValidationMessage(null);
    }
  }, []);

  /**
   * ЛКМ по space — циклический выбор: фишки на точке → точка → сброс.
   *
   * Если на точке несколько фишек — повторный ЛКМ перебирает их по очереди.
   * После всех фишек — выбор самой точки. Ещё раз — сброс всего.
   */
  const handleSpaceClick = useCallback(
    (spaceId: string) => {
      setValidationMessage(null);

      // Все фишки на этой точке (в порядке pieces[])
      const piecesOnSpace = gameState.pieces.filter(
        (p) => p.locationId === spaceId
      );

      // Случай 1: на точке есть фишки
      if (piecesOnSpace.length > 0) {
        // Если сейчас выбрана точка (не фишка) — выбрать первую фишку
        if (selectedSpaceId === spaceId && selectedPieceId === null) {
          setSelectedPieceId(piecesOnSpace[0].pieceId);
          setSelectedSpaceId(null);
          return;
        }

        // Если сейчас выбрана одна из фишек на этой точке — найти следующую
        const currentIndex = piecesOnSpace.findIndex(
          (p) => p.pieceId === selectedPieceId
        );
        if (currentIndex >= 0) {
          const nextIndex = currentIndex + 1;
          if (nextIndex < piecesOnSpace.length) {
            // Есть следующая фишка — выбрать её
            setSelectedPieceId(piecesOnSpace[nextIndex].pieceId);
            setSelectedSpaceId(null);
          } else {
            // Все фишки перебрали — выбрать точку
            setSelectedPieceId(null);
            setSelectedSpaceId(spaceId);
          }
          return;
        }

        // Ни одна фишка с этой точки не выбрана (выбрана фишка с другой точки или ничего)
        // → выбрать первую фишку на этой точке
        setSelectedPieceId(piecesOnSpace[0].pieceId);
        setSelectedSpaceId(null);
        return;
      }

      // Случай 2: на точке нет фишек
      if (selectedSpaceId === spaceId && selectedPieceId === null) {
        // Уже выбрана — сбросить
        setSelectedSpaceId(null);
        setSelectedPieceId(null);
        return;
      }
      // Выбрать точку
      setSelectedSpaceId(spaceId);
      setSelectedPieceId(null);
    },
    [gameState.pieces, selectedPieceId, selectedSpaceId]
  );

  /**
   * ПКМ по space — попытка перемещения выбранной фишки.
   * Если фишка не выбрана — показывает подсказку.
   */
  const handleSpaceRightClick = useCallback(
    (spaceId: string) => {
      if (!selectedPieceId) {
        setValidationMessage("Перемещение: сначала выбери фишку левой кнопкой.");
        return;
      }

      const piece = gameState.pieces.find(
        (p) => p.pieceId === selectedPieceId
      );
      if (!piece) {
        setSelectedPieceId(null);
        setValidationMessage("Перемещение: выбранная фишка больше не существует.");
        return;
      }

      if (piece.locationId === spaceId) {
        // ПКМ по той же точке — отмена выбора
        setSelectedPieceId(null);
        setValidationMessage(null);
        return;
      }

      const action = createMovePieceAction(
        piece.pieceId,
        piece.locationId,
        spaceId,
        "user"
      );

      const ok = commitAction(action);
      if (ok) {
        setSelectedPieceId(null);
      }
    },
    [gameState.pieces, selectedPieceId, commitAction]
  );

  /** Создать новую фишку. Пространство: selectedSpaceId или location выбранной фишки. */
  const handleCreatePiece = useCallback(
    (ownerId: string) => {
      // Определяем целевой space: либо выбранный напрямую, либо через фишку
      let targetSpaceId = selectedSpaceId;
      if (!targetSpaceId && selectedPieceId) {
        const selPiece = gameState.pieces.find((p) => p.pieceId === selectedPieceId);
        targetSpaceId = selPiece?.locationId ?? null;
      }

      if (!targetSpaceId) {
        setValidationMessage("Создание фишки: сначала выбери точку на карте.");
        return;
      }

      const pieceDefId = "infantry";
      const pieceId = `piece-${nextPieceSeqRef.current}`;

      const action = createCreatePieceAction(
        targetSpaceId,
        pieceDefId,
        ownerId,
        "user"
      );

      const ok = commitAction(action, pieceId, ownerId);
      if (ok) {
        nextPieceSeqRef.current++;
        setSelectedPieceId(pieceId);
        setSelectedSpaceId(null);
      }
    },
    [selectedSpaceId, selectedPieceId, gameState.pieces, commitAction]
  );

  /** Удалить выбранную фишку */
  const handleDeletePiece = useCallback(() => {
    if (!selectedPieceId) {
      setValidationMessage("Удаление фишки: сначала выбери фишку на карте.");
      return;
    }

    const action = createDeletePieceAction(selectedPieceId, "user");
    const ok = commitAction(action);
    if (ok) {
      setSelectedPieceId(null);
    }
  }, [selectedPieceId, commitAction]);

  /** Сменить контроль. Пространство: selectedSpaceId или location выбранной фишки. */
  const handleChangeControl = useCallback(
    (newOwnerId: string | null) => {
      let targetSpaceId = selectedSpaceId;
      if (!targetSpaceId && selectedPieceId) {
        const selPiece = gameState.pieces.find((p) => p.pieceId === selectedPieceId);
        targetSpaceId = selPiece?.locationId ?? null;
      }

      if (!targetSpaceId) {
        setValidationMessage("Смена контроля: сначала выбери точку на карте.");
        return;
      }

      const action = createChangeControlAction(
        targetSpaceId,
        newOwnerId,
        "user"
      );

      commitAction(action);
    },
    [selectedSpaceId, selectedPieceId, gameState.pieces, commitAction]
  );

  /** Получить имя space по spaceId */
  const getSpaceName = (spaceId: string): string => {
    const s = gameState.spaces.find((sp) => sp.spaceId === spaceId);
    return s ? s.name : spaceId;
  };

  /** Получить текущий контроль space */
  const getControlOwner = (spaceId: string): string | null => {
    return gameState.controlState[spaceId] ?? null;
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Table Sandbox 0.1 — Manual Sandbox Action Pack 1</h1>
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
            selectedSpaceId={selectedSpaceId}
            onSpaceClick={handleSpaceClick}
            onSpaceRightClick={handleSpaceRightClick}
          />
          <p className="area-hint">
            {selectedPieceId
              ? `Выбрана фишка: ${selectedPieceId} в точке «${getSpaceName(gameState.pieces.find(p => p.pieceId === selectedPieceId)?.locationId ?? "")}». ПКМ по другой точке — переместить.`
              : selectedSpaceId
                ? `Выбрана точка: «${getSpaceName(selectedSpaceId)}». ЛКМ — выбрать, ПКМ — переместить.`
                : "ЛКМ по точке — выбрать. ПКМ по точке — переместить выбранную фишку."}
          </p>
        </div>

        <aside className="sidebar-area">
          {/* Панель выбранного объекта — либо фишка, либо точка */}
          <div className="selection-panel">
            <h3 className="panel-title">Выбранный объект</h3>
            {selectedPieceId ? (
              <div className="selection-info">
                <div className="sel-row">
                  <span className="sel-label">Фишка:</span>
                  <span className="sel-value sel-piece">{selectedPieceId}</span>
                </div>
                <div className="sel-row">
                  <span className="sel-label">Владелец:</span>
                  <span className={`sel-value ${gameState.pieces.find(p => p.pieceId === selectedPieceId)?.ownerId === "tiny-red" ? "sel-owner" : "sel-owner-blue"}`}>
                    {gameState.pieces.find(p => p.pieceId === selectedPieceId)?.ownerId ?? "—"}
                  </span>
                </div>
                <div className="sel-row">
                  <span className="sel-label">На точке:</span>
                  <span className="sel-value">
                    {(() => { const loc = gameState.pieces.find(p => p.pieceId === selectedPieceId)?.locationId; return loc ? `«${getSpaceName(loc)}»` : "—"; })()}
                  </span>
                </div>
              </div>
            ) : selectedSpaceId ? (
              <div className="selection-info">
                <div className="sel-row">
                  <span className="sel-label">Точка:</span>
                  <span className="sel-value">{selectedSpaceId}</span>
                  <span className="sel-name">«{getSpaceName(selectedSpaceId)}»</span>
                </div>
                <div className="sel-row">
                  <span className="sel-label">Контроль:</span>
                  <span className={`sel-value ${getControlOwner(selectedSpaceId) ? "sel-owner" : "sel-none"}`}>
                    {getControlOwner(selectedSpaceId) ?? "нет"}
                  </span>
                </div>
                <div className="sel-row">
                  <span className="sel-label">Фишки:</span>
                  <span className="sel-value">{gameState.pieces.filter(p => p.locationId === selectedSpaceId).length > 0 ? gameState.pieces.filter(p => p.locationId === selectedSpaceId).map(p => p.pieceId).join(", ") : "нет"}</span>
                </div>
              </div>
            ) : (
              <p className="sel-empty">Ничего не выбрано. Кликни по точке на карте.</p>
            )}
          </div>

          {/* Кнопки действий */}
          <div className="action-panel">
            <h3 className="panel-title">Действия</h3>

            <div className="action-group">
              <span className="action-group-label">Создать фишку:</span>
              <div className="action-btn-row">
                <button
                  className="action-btn action-create"
                  onClick={() => handleCreatePiece("tiny-red")}
                  title="Создать фишку красных на выбранной точке"
                >
                  Создать (красные)
                </button>
                <button
                  className="action-btn action-create"
                  onClick={() => handleCreatePiece("tiny-blue")}
                  title="Создать фишку синих на выбранной точке"
                >
                  Создать (синие)
                </button>
              </div>
            </div>

            <div className="action-group">
              <button
                className="action-btn action-delete"
                onClick={handleDeletePiece}
                title="Удалить выбранную фишку"
              >
                Удалить фишку
              </button>
            </div>

            <div className="action-group">
              <span className="action-group-label">Контроль точки:</span>
              <div className="action-btn-row">
                <button
                  className="action-btn action-control"
                  onClick={() => handleChangeControl("tiny-red")}
                  title="Установить контроль красных над точкой"
                >
                  Красные
                </button>
                <button
                  className="action-btn action-control"
                  onClick={() => handleChangeControl("tiny-blue")}
                  title="Установить контроль синих над точкой"
                >
                  Синие
                </button>
                <button
                  className="action-btn action-control-neutral"
                  onClick={() => handleChangeControl(null)}
                  title="Сбросить контроль точки"
                >
                  Сброс
                </button>
              </div>
            </div>
          </div>

          {/* Сообщения валидации */}
          {validationMessage && (
            <div className="validation-message">
              <span className="validation-icon">⚠</span>
              <span>{validationMessage}</span>
            </div>
          )}
        </aside>

        <aside className="debug-area">
          <DebugPanel
            gameState={gameState}
            lastAction={lastAction}
            eventLog={eventLog}
            selectedPieceId={selectedPieceId}
            selectedSpaceId={selectedSpaceId}
          />
        </aside>
      </main>

      <footer className="app-footer">
        <div className="footer-left">
          <span>GameState version: {gameState.version}</span>
          <span className="footer-sep">|</span>
          <span>Spaces: {gameState.spaces.length}</span>
          <span className="footer-sep">|</span>
          <span>Pieces: {gameState.pieces.length}</span>
          <span className="footer-sep">|</span>
          <span>Events: {eventLog.events.length}</span>
          <span className="footer-sep">|</span>
          <span>Источник истины: Runtime (React state), НЕ Phaser</span>
        </div>
        <div className="footer-actions">
          <button
            className="snapshot-btn save-btn"
            onClick={handleSave}
            title="Сохранить текущее состояние в локальное хранилище браузера"
          >
            Сохранить
          </button>
          <button
            className="snapshot-btn load-btn"
            onClick={handleLoad}
            title="Загрузить сохранённое состояние из локального хранилища браузера"
          >
            Загрузить
          </button>
          {snapshotStatus && (
            <span className="snapshot-status">{snapshotStatus}</span>
          )}
        </div>
      </footer>
    </div>
  );
}
