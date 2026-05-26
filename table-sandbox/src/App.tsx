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
import { validateBootstrap, formatSanityIssues } from "./runtime/sanityCheck";
import "./App.css";
import EditorSurface from "./editor/EditorSurface";
import { type MapDraft, loadMapDraft } from "./editor/MapDraft";
import { type SpaceState, type ConnectionState } from "./runtime/GameState";
import { type MapRenderModel, type MapRenderUnderlay } from "./map/MapRenderModel";
import mapData from "./fixtures/tiny-module/modules/tiny-module/map.json";

/**
 * App — корневой React-компонент Table Sandbox 0.1 (Action/Event Spine).
 *
 * Владеет:
 *   - GameState (authoritative runtime state)
 *   - Action/Event pipeline
 *   - EventLog
 *   - Selection state (selectedPieceId, selectedSpaceId)
 *
 * GameState инициализируется из canonical fixtures
 * (table-sandbox/src/fixtures/tiny-module/), не из placeholder.
 *
 * PhaserStage — только renderer/input, не владеет состоянием.
 *
 * Handoff 0012: rules boundary стала явной.
 * Flow: runtime asks rules.validateAction → rules.resolveAction → runtime commits.
 *
 * Handoff 0017 (Play Sandbox Readiness Pack):
 *   - stack/selection readiness: циклический выбор + информация о stack в панели
 *   - scenario reset: полный сброс к fixture-based initial state
 *   - lightweight sanity check: проверка ссылок после bootstrap
 *   - save/load regression: проверено для всех поддерживаемых действий
 *
 * Первый move slice UX:
 *   1. Клик по space с фишкой → выбор фишки (подсветка)
 *   2. Клик по другому space → move_piece_requested → validate → resolve → piece_moved → redraw
 */

export default function App() {
  // Bootstrap + sanity check
  const initialGS = bootstrapGameState();
  const initialSanityIssues = validateBootstrap({
    spaces: initialGS.spaces,
    pieces: initialGS.pieces,
    controlState: initialGS.controlState,
    scenarioMapId: initialGS.mapId,
    mapMapId: initialGS.mapId,
  });
  const initialSanityMsg = formatSanityIssues(initialSanityIssues);

  const [gameState, setGameState] = useState<GameState>(initialGS);
  const [lastAction, setLastAction] = useState<Action | null>(null);
  const [eventLog, setEventLog] = useState<EventLog>(createEventLog);
  const [selectedPieceId, setSelectedPieceId] = useState<string | null>(null);
  const [selectedSpaceId, setSelectedSpaceId] = useState<string | null>(null);
  const [snapshotStatus, setSnapshotStatus] = useState<string | null>(null);
  const [validationMessage, setValidationMessage] = useState<string | null>(null);
  const [bootstrapSanityMessage, setBootstrapSanityMessage] = useState<string | null>(initialSanityMsg);

  /** Режим приложения: editor или play */
  const [appMode, setAppMode] = useState<"editor" | "play">("editor");

  /** Editor draft — живёт в App, переживает переключение режимов */
  const [editorDraft, setEditorDraft] = useState<MapDraft>(() => loadMapDraft(mapData));

  /**
   * Handoff 0029: MapRenderModel — display-only visual contract.
   * Отдельный от GameState. При preview строится из редакторского draft.
   * null означает «нет authored map visual» (fixture/load flow).
   */
  const [mapVisual, setMapVisual] = useState<MapRenderModel | null>(null);

  /** Монотонный счётчик для генерации pieceId */
  const nextPieceSeqRef = useRef<number>(3);

  /**
   * Handoff 0029: конвертирует MapDraft в MapRenderModel (visual contract).
   * Не трогает GameState. Только display-only поля.
   */
  const draftToMapRenderModel = useCallback((draft: MapDraft): MapRenderModel => {
    const underlay: MapRenderUnderlay | null = draft.underlay
      ? {
          src: draft.underlay.src,
          offsetX: draft.underlay.offsetX,
          offsetY: draft.underlay.offsetY,
          scale: draft.underlay.scale,
          rotationDeg: draft.underlay.rotation,
          opacityPercent: draft.underlay.opacity,
          visible: draft.underlay.visible,
          naturalWidth: draft.underlay.naturalWidth,
          naturalHeight: draft.underlay.naturalHeight,
        }
      : null;

    return {
      source: "editor-preview",
      mapId: draft.mapId,
      name: draft.name,
      coordinateSystem: {
        type: "pixel",
        width: draft.coordinateSystem.width,
        height: draft.coordinateSystem.height,
      },
      underlay,
    };
  }, []);

  /**
   * Конвертирует MapDraft в GameState для preview.
   * Draft НЕ мутируется. GameState НЕ пишет обратно в draft.
   */
  const draftToGameState = useCallback((draft: MapDraft): GameState => {
    const spaces: SpaceState[] = draft.spaces.map((s) => ({
      spaceId: s.spaceId,
      name: s.name,
      x: s.x,
      y: s.y,
      type: s.type,
    }));
    const connections: ConnectionState[] = draft.connections.map((c) => ({
      connectionId: c.connectionId,
      fromSpaceId: c.fromSpaceId,
      toSpaceId: c.toSpaceId,
      type: c.type,
    }));
    return {
      ...initialGS,
      version: 0,
      lastUpdated: Date.now(),
      mapId: draft.mapId,
      spaces,
      connections,
      pieces: [],
      controlState: {},
      turn: { round: 0, phaseId: "setup", activeActorId: "none" },
      bootstrapMeta: {
        ...initialGS.bootstrapMeta,
        source: "editor-preview",
        mapId: draft.mapId,
      },
    };
  }, [initialGS]);

  /** Переход из редактора в preview: устанавливает GameState и mapVisual из draft */
  const handlePreview = useCallback((draft: MapDraft) => {
    const gs = draftToGameState(draft);
    const visual = draftToMapRenderModel(draft);
    setGameState(gs);
    setMapVisual(visual);
    setEventLog(createEventLog());
    setLastAction(null);
    setAppMode("play");
    setSelectedPieceId(null);
    setSelectedSpaceId(null);
    setValidationMessage(null);
    setSnapshotStatus(null);
    resetActionSeq(0);
    resetEventSeq(0);
    nextPieceSeqRef.current = 3;
  }, [draftToGameState, draftToMapRenderModel]);

  /**
   * Сбросить всё к исходному fixture-based состоянию.
   *
   * Reset rule (Handoff 0017):
   *   - GameState: пересоздаётся из fixtures (bootstrapGameState)
   *   - EventLog: очищается до пустого
   *   - Selection: сбрасывается
   *   - Messages: очищаются
   *   - Action/Event seq: сбрасываются в 0
   *   - nextPieceSeq: сбрасывается в 3 (исходные piece-1 и piece-2)
   *   - Sanity check: перезапускается
   *   - Fixture files НЕ мутируются
   *   - localStorage НЕ трогается (пользователь сам сохраняет/загружает)
   */
  const handleReset = useCallback(() => {
    const freshGS = bootstrapGameState();
    const freshSanityIssues = validateBootstrap({
      spaces: freshGS.spaces,
      pieces: freshGS.pieces,
      controlState: freshGS.controlState,
      scenarioMapId: freshGS.mapId,
      mapMapId: freshGS.mapId,
    });

    setGameState(freshGS);
    setMapVisual(null); // Handoff 0029: очистка stale editor visual
    setEventLog(createEventLog());
    setLastAction(null);
    setSelectedPieceId(null);
    setSelectedSpaceId(null);
    setValidationMessage(null);
    setSnapshotStatus(null);
    setBootstrapSanityMessage(formatSanityIssues(freshSanityIssues));
    resetActionSeq(0);
    resetEventSeq(0);
    nextPieceSeqRef.current = 3;
  }, []);

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
      setMapVisual(null); // Handoff 0029: очистка stale editor visual при load
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
   * Stack selection UX (Handoff 0017):
   *   - Если на точке несколько фишек — повторный ЛКМ перебирает их по очереди.
   *   - После всех фишек — выбор самой точки. Ещё раз — сброс всего.
   *   - Выбранная фишка в stack явно видна в selection panel.
   *   - Drag применяется именно к выбранной фишке.
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
   * Drag release — завершение smart drag левой кнопкой.
   *
   * Вызывается из Phaser при отпускании piece после drag.
   * Если targetSpaceId не null — создаём move_piece_requested Action
   * и пропускаем через существующий pipeline.
   * Если targetSpaceId null (invalid/no-target) — показываем сообщение,
   * GameState не мутируется.
   */
  const handlePieceDragRelease = useCallback(
    (pieceId: string, targetSpaceId: string | null) => {
      if (!targetSpaceId) {
        // Invalid/no-target drop — rollback, GameState не меняется
        setValidationMessage("Перемещение: не удалось определить целевую точку. Отпусти фишку над точкой на карте.");
        return;
      }

      const piece = gameState.pieces.find((p) => p.pieceId === pieceId);
      if (!piece) {
        setValidationMessage("Перемещение: перетаскиваемая фишка больше не существует.");
        return;
      }

      if (piece.locationId === targetSpaceId) {
        // Drag на ту же точку — не ошибка, просто бездействие
        setValidationMessage(null);
        return;
      }

      const action = createMovePieceAction(
        piece.pieceId,
        piece.locationId,
        targetSpaceId,
        "user"
      );

      const ok = commitAction(action);
      if (ok) {
        setSelectedPieceId(null);
        setValidationMessage(null);
      }
      // Если blocked — commitAction уже выставил validationMessage
    },
    [gameState.pieces, commitAction]
  );

  /**
   * ПКМ по space — попытка перемещения выбранной фишки (fallback).
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
    <div className={`app-shell ${appMode === "editor" ? "editor-mode" : ""}`}>
      <header className="app-header">
        <h1>
          {appMode === "editor"
            ? "Редактор карты 0.1 — Spaces & Connections"
            : "Table Sandbox 0.1 — Play Sandbox Ready (0017)"}
        </h1>
        <span className="app-badge">
          {appMode === "editor" ? "editor" : `${gameState.projectId}/${gameState.scenarioId}`}
        </span>
        <button
          className="mode-switch-btn"
          onClick={() => {
            if (appMode === "editor") {
              // Handoff 0029: прямой переход в fixture play — очистка stale editor visual
              setMapVisual(null);
              setAppMode("play");
            } else {
              setAppMode("editor");
            }
          }}
          title={appMode === "editor" ? "Перейти в песочницу (текущий fixture state)" : "Вернуться в редактор карты"}
        >
          {appMode === "editor" ? "🎮 Играть (fixture)" : "✏ Редактор"}
        </button>
      </header>

      {appMode === "editor" ? (
        <EditorSurface
          draft={editorDraft}
          onDraftChange={setEditorDraft}
          onPreview={handlePreview}
        />
      ) : (
        <>
          {bootstrapSanityMessage && (
            <div className="sanity-banner">
              <span className="sanity-icon">⚠</span>
              <span>{bootstrapSanityMessage}</span>
            </div>
          )}

          <main className="app-main">
            <div className="table-area">
              <h2 className="area-label">Table Surface (Phaser Renderer)</h2>
              <PhaserStage
                gameState={gameState}
                mapVisual={mapVisual}
                selectedPieceId={selectedPieceId}
                selectedSpaceId={selectedSpaceId}
                onSpaceClick={handleSpaceClick}
                onSpaceRightClick={handleSpaceRightClick}
                onPieceDragRelease={handlePieceDragRelease}
              />
              <p className="area-hint">
                {selectedPieceId
                  ? (() => {
                      const selPiece = gameState.pieces.find(p => p.pieceId === selectedPieceId);
                      const locId = selPiece?.locationId ?? "";
                      const stackCount = gameState.pieces.filter(p => p.locationId === locId).length;
                      const stackIndex = gameState.pieces.filter(p => p.locationId === locId).findIndex(p => p.pieceId === selectedPieceId) + 1;
                      const stackInfo = stackCount > 1 ? ` (${stackIndex}/${stackCount} в stack)` : "";
                      return `Выбрана фишка: ${selectedPieceId}${stackInfo} в точке «${getSpaceName(locId)}». Тяни левой кнопкой — переместить. ПКМ по точке — тоже переместить.`;
                    })()
                  : selectedSpaceId
                    ? `Выбрана точка: «${getSpaceName(selectedSpaceId)}». ЛКМ — выбрать, тяни фишку — переместить.`
                    : "ЛКМ по точке — выбрать. Зажми фишку левой кнопкой и тяни — переместить."}
              </p>
            </div>

            <aside className="sidebar-area">
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
                    {(() => {
                      const selPiece = gameState.pieces.find(p => p.pieceId === selectedPieceId);
                      const locId = selPiece?.locationId;
                      if (!locId) return null;
                      const stackPieces = gameState.pieces.filter(p => p.locationId === locId);
                      if (stackPieces.length <= 1) return null;
                      const stackIdx = stackPieces.findIndex(p => p.pieceId === selectedPieceId) + 1;
                      return (
                        <div className="sel-row sel-stack-row">
                          <span className="sel-label">Stack:</span>
                          <span className="sel-value sel-stack">
                            {stackIdx}/{stackPieces.length} — {stackPieces.map(p => p.pieceId === selectedPieceId ? `[${p.pieceId}]` : p.pieceId).join(", ")}
                          </span>
                        </div>
                      );
                    })()}
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

              <div className="action-panel">
                <h3 className="panel-title">Действия</h3>
                <div className="action-group">
                  <span className="action-group-label">Создать фишку:</span>
                  <div className="action-btn-row">
                    <button className="action-btn action-create" onClick={() => handleCreatePiece("tiny-red")}>Создать (красные)</button>
                    <button className="action-btn action-create" onClick={() => handleCreatePiece("tiny-blue")}>Создать (синие)</button>
                  </div>
                </div>
                <div className="action-group">
                  <button className="action-btn action-delete" onClick={handleDeletePiece}>Удалить фишку</button>
                </div>
                <div className="action-group">
                  <span className="action-group-label">Контроль точки:</span>
                  <div className="action-btn-row">
                    <button className="action-btn action-control" onClick={() => handleChangeControl("tiny-red")}>Красные</button>
                    <button className="action-btn action-control" onClick={() => handleChangeControl("tiny-blue")}>Синие</button>
                    <button className="action-btn action-control-neutral" onClick={() => handleChangeControl(null)}>Сброс</button>
                  </div>
                </div>
              </div>

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
              <button className="snapshot-btn reset-btn" onClick={handleReset}>Сброс</button>
              <button className="snapshot-btn save-btn" onClick={handleSave}>Сохранить</button>
              <button className="snapshot-btn load-btn" onClick={handleLoad}>Загрузить</button>
              {snapshotStatus && <span className="snapshot-status">{snapshotStatus}</span>}
            </div>
          </footer>
        </>
      )}
    </div>
  );
}
