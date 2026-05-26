import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  type ConnectionDraft,
  type DraftSnapshot,
  type EditorSettings,
  HISTORY_LIMIT,
  type MapDraft,
  type MapValidation,
  type SpaceDraft,
  type UnderlayState,
  uniqueId,
  validateMapDraft,
  worldToMapLocal,
  mapLocalToWorld,
  takeSnapshot,
  restoreSnapshot,
  pushHistory,
  DEFAULT_UNDERLAY,
  DEFAULT_EDITOR_SETTINGS,
} from "./MapDraft";
import "./Editor.css";

const STORAGE_KEY = "table-sandbox-editor-draft";
const SPACE_RADIUS = 8;
const HANDLE_SIZE = 10;
const ROTATE_HANDLE_DISTANCE = 36;

type Tool = "select" | "space" | "connection" | "pan";

interface EditorSurfaceProps {
  draft: MapDraft;
  onDraftChange: (draft: MapDraft) => void;
  onPreview: (draft: MapDraft) => void;
}

interface ViewState {
  zoom: number;
  panX: number;
  panY: number;
}

interface WorldPoint {
  x: number;
  y: number;
}

type ContextMenuState =
  | {
      type: "canvas";
      x: number;
      y: number;
      worldX: number;
      worldY: number;
    }
  | {
      type: "space" | "connection" | "underlay";
      x: number;
      y: number;
      id: string;
    };

type DragState =
  | {
      type: "spaceMove";
      id: string;
      startWorldX: number;
      startWorldY: number;
      originX: number;
      originY: number;
    }
  | {
      type: "pan";
      startClientX: number;
      startClientY: number;
      originPanX: number;
      originPanY: number;
    }
  | {
      type: "underlayMove";
      startWorldX: number;
      startWorldY: number;
      originOffsetX: number;
      originOffsetY: number;
    }
  | {
      type: "underlayRotate";
      startWorldX: number;
      startWorldY: number;
      originRotation: number;
      centerWorldX: number;
      centerWorldY: number;
    }
  | {
      /** 0026 correction: center-radial scale (V2 review) */
      type: "underlayScale";
      startWorldX: number;
      startWorldY: number;
      originScale: number;
      /** world-space center of underlay at drag start */
      centerWorldX: number;
      centerWorldY: number;
      /** distance from center to start pointer */
      startDistance: number;
    };

/** Вычислить угол от central point к (x,y) в градусах (borrowed from prototype) */
function angleDeg(cx: number, cy: number, x: number, y: number): number {
  return (Math.atan2(y - cy, x - cx) * 180) / Math.PI;
}

/** Snap value to grid (borrowed from prototype snap()) */
function snapValue(v: number, gridSize: number, on: boolean): number {
  if (!on) return Math.round(v);
  return Math.round(v / gridSize) * gridSize;
}

export default function EditorSurface({
  draft,
  onDraftChange,
  onPreview,
}: EditorSurfaceProps) {
  const [tool, setTool] = useState<Tool>("select");
  const [selection, setSelection] = useState<{
    type: "space" | "connection" | "underlay" | null;
    id: string | null;
  }>({ type: null, id: null });
  const [validation, setValidation] = useState<MapValidation | null>(null);
  const [linkStart, setLinkStart] = useState<string | null>(null);
  const [message, setMessage] = useState("Готово");
  const [contextMenu, setContextMenu] = useState<ContextMenuState | null>(null);
  const [view, setView] = useState<ViewState>({ zoom: 1, panX: 0, panY: 0 });

  // 0020: undo/redo history
  const [history, setHistory] = useState<{
    past: DraftSnapshot[];
    future: DraftSnapshot[];
  }>({ past: [], future: [] });

  const dragRef = useRef<DragState | null>(null);
  const canvasRef = useRef<HTMLDivElement>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const underlay = draft.underlay;
  const editorSettings = draft.editorSettings;

  /** Active map-plane size from draft (0020 correction: not fixed fixture constants) */
  const mapW = draft.coordinateSystem.width;
  const mapH = draft.coordinateSystem.height;

  const spacesById = useMemo(
    () => Object.fromEntries(draft.spaces.map((space) => [space.spaceId, space])),
    [draft.spaces]
  );

  const selectedObject =
    selection.type === "space"
      ? draft.spaces.find((space) => space.spaceId === selection.id) ?? null
      : selection.type === "connection"
        ? draft.connections.find(
            (connection) => connection.connectionId === selection.id
          ) ?? null
        : selection.type === "underlay"
          ? underlay
          : null;

  // 0020 correction: expand map plane to fit underlay if underlay is larger
  useEffect(() => {
    if (!underlay) return;
    const uw = underlay.naturalWidth;
    const uh = underlay.naturalHeight;
    if (uw > draft.coordinateSystem.width || uh > draft.coordinateSystem.height) {
      onDraftChange({
        ...draft,
        coordinateSystem: {
          type: "pixel",
          width: Math.max(draft.coordinateSystem.width, uw),
          height: Math.max(draft.coordinateSystem.height, uh),
        },
      });
    }
  }, [underlay?.naturalWidth, underlay?.naturalHeight]); // eslint-disable-line react-hooks/exhaustive-deps

  const stageWidth = mapW * view.zoom;
  const stageHeight = mapH * view.zoom;

  const nextSpaceOrdinal = useCallback(
    () => draft.spaces.length + 1,
    [draft.spaces.length]
  );

  const nextConnectionOrdinal = useCallback(
    () => draft.connections.length + 1,
    [draft.connections.length]
  );

  /** 0026 correction: raw workspace point, no early clamping (V2 review) */
  const getWorldPoint = useCallback(
    (clientX: number, clientY: number): WorldPoint => {
      const rect = canvasRef.current?.getBoundingClientRect();
      if (!rect) {
        return { x: 0, y: 0 };
      }

      return {
        x: (clientX - rect.left - view.panX) / view.zoom,
        y: (clientY - rect.top - view.panY) / view.zoom,
      };
    },
    [view.panX, view.panY, view.zoom]
  );

  /** 0026 correction: clamp map-local point to underlay image bounds (V2 review) */
  const clampMapLocal = useCallback((local: WorldPoint): WorldPoint => {
    if (!underlay) return local;
    return {
      x: Math.max(0, Math.min(underlay.naturalWidth, local.x)),
      y: Math.max(0, Math.min(underlay.naturalHeight, local.y)),
    };
  }, [underlay]);

  const setToolWithMessage = useCallback((nextTool: Tool) => {
    setTool(nextTool);
    setLinkStart(null);
    setMessage(
      nextTool === "connection" ? "Выберите первую точку." : "Готово"
    );
  }, []);

  // ---- Draft mutation helpers (0020: with undo history) ----

  const commitDraft = useCallback(
    (nextDraft: MapDraft) => {
      setHistory((h) => ({
        past: pushHistory(h.past, draft),
        future: [],
      }));
      onDraftChange(nextDraft);
    },
    [draft, onDraftChange]
  );

  /** Undo: restore previous snapshot (borrowed from prototype undo()) */
  const undo = useCallback(() => {
    setHistory((h) => {
      if (!h.past.length) return h;
      const current = takeSnapshot(draft);
      const prev = h.past[h.past.length - 1];
      onDraftChange(restoreSnapshot(prev));
      setMessage("Действие отменено");
      return {
        past: h.past.slice(0, -1),
        future: [current, ...h.future].slice(0, HISTORY_LIMIT),
      };
    });
  }, [draft, onDraftChange]);

  /** Redo: restore next snapshot (borrowed from prototype redo()) */
  const redo = useCallback(() => {
    setHistory((h) => {
      if (!h.future.length) return h;
      const current = takeSnapshot(draft);
      const next = h.future[0];
      onDraftChange(restoreSnapshot(next));
      setMessage("Действие повторено");
      return {
        past: [...h.past, current].slice(-HISTORY_LIMIT),
        future: h.future.slice(1),
      };
    });
  }, [draft, onDraftChange]);

  // 0020: keyboard shortcuts Ctrl+Z / Ctrl+Y (borrowed from prototype)
  useEffect(() => {
    const key = (e: KeyboardEvent) => {
      const mod = e.ctrlKey || e.metaKey;
      if (mod && e.key.toLowerCase() === "z") {
        e.preventDefault();
        if (e.shiftKey) {
          redo();
        } else {
          undo();
        }
      }
      if (mod && e.key.toLowerCase() === "y") {
        e.preventDefault();
        redo();
      }
    };
    window.addEventListener("keydown", key);
    return () => window.removeEventListener("keydown", key);
  }, [undo, redo]);

  // ---- Underlay mutation (0020) ----

  const updateUnderlay = useCallback(
    (patch: Partial<UnderlayState>) => {
      if (!underlay) return;
      commitDraft({
        ...draft,
        underlay: { ...underlay, ...patch },
      });
    },
    [draft, underlay, commitDraft]
  );

  const updateEditorSettings = useCallback(
    (patch: Partial<EditorSettings>) => {
      commitDraft({
        ...draft,
        editorSettings: { ...editorSettings, ...patch },
      });
    },
    [draft, editorSettings, commitDraft]
  );

  const resetUnderlayRotation = useCallback(() => {
    if (!underlay) return;
    commitDraft({
      ...draft,
      underlay: { ...underlay, rotation: 0 },
    });
    setMessage("Поворот подложки сброшен");
  }, [draft, underlay, commitDraft]);

  const resetUnderlayTransform = useCallback(() => {
    if (!underlay) return;
    commitDraft({
      ...draft,
      underlay: {
        ...underlay,
        offsetX: DEFAULT_UNDERLAY.offsetX,
        offsetY: DEFAULT_UNDERLAY.offsetY,
        scale: DEFAULT_UNDERLAY.scale,
        rotation: DEFAULT_UNDERLAY.rotation,
      },
    });
    setMessage("Трансформация подложки сброшена");
  }, [draft, underlay, commitDraft]);

  // 0020 correction: load terrain image — also resize map plane to image size
  const handleUnderlayImageLoad = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (!file || !underlay) return;
      const reader = new FileReader();
      reader.onload = () => {
        const img = new Image();
        img.onload = () => {
          commitDraft({
            ...draft,
            coordinateSystem: {
              type: "pixel" as const,
              width: img.naturalWidth,
              height: img.naturalHeight,
            },
            underlay: {
              ...underlay,
              src: String(reader.result),
              naturalWidth: img.naturalWidth,
              naturalHeight: img.naturalHeight,
              offsetX: 0,
              offsetY: 0,
              scale: 1,
              rotation: 0,
            },
          });
          setMessage(`Карта загружена: ${img.naturalWidth}×${img.naturalHeight}px — размер карты обновлён`);
        };
        img.src = String(reader.result);
      };
      reader.readAsDataURL(file);
      e.target.value = "";
    },
    [draft, underlay, commitDraft]
  );

  // ---- Space/connection operations (0018 baseline, adapted 0020) ----

  /** 0020: addSpace конвертирует world → map-local, применяет snap, clamp 0026 */
  const addSpace = useCallback(
    (worldX: number, worldY: number) => {
      const local = worldToMapLocal(worldX, worldY, underlay);
      const clamped = clampMapLocal(local);
      const snappedX = snapValue(clamped.x, editorSettings.gridSize, editorSettings.snapToGrid);
      const snappedY = snapValue(clamped.y, editorSettings.gridSize, editorSettings.snapToGrid);

      const ordinal = nextSpaceOrdinal();
      const spaceId = uniqueId(
        `space-${ordinal}`,
        draft.spaces.map((space) => space.spaceId)
      );

      const nextDraft: MapDraft = {
        ...draft,
        spaces: [
          ...draft.spaces,
          { spaceId, name: `Точка ${ordinal}`, x: snappedX, y: snappedY, type: "region" },
        ],
      };

      setHistory((h) => ({ past: pushHistory(h.past, draft), future: [] }));
      onDraftChange(nextDraft);
      setSelection({ type: "space", id: spaceId });
      setMessage("Точка добавлена.");
    },
    [draft, nextSpaceOrdinal, onDraftChange, underlay, editorSettings, clampMapLocal]
  );

  /** 0020: moveSpace работает в map-local координатах, применяет snap */
  const moveSpace = useCallback(
    (spaceId: string, mapLocalX: number, mapLocalY: number) => {
      const snappedX = snapValue(mapLocalX, editorSettings.gridSize, editorSettings.snapToGrid);
      const snappedY = snapValue(mapLocalY, editorSettings.gridSize, editorSettings.snapToGrid);
      onDraftChange({
        ...draft,
        spaces: draft.spaces.map((space) =>
          space.spaceId === spaceId ? { ...space, x: snappedX, y: snappedY } : space
        ),
      });
    },
    [draft, onDraftChange, editorSettings]
  );

  const renameSpace = useCallback(
    (spaceId: string, name: string) => {
      commitDraft({
        ...draft,
        spaces: draft.spaces.map((space) =>
          space.spaceId === spaceId ? { ...space, name } : space
        ),
      });
    },
    [draft, commitDraft]
  );

  const deleteSpace = useCallback(
    (spaceId: string) => {
      commitDraft({
        ...draft,
        spaces: draft.spaces.filter((space) => space.spaceId !== spaceId),
        connections: draft.connections.filter(
          (connection) => connection.fromSpaceId !== spaceId && connection.toSpaceId !== spaceId
        ),
      });
      setSelection({ type: null, id: null });
      setMessage("Точка и связи удалены.");
    },
    [draft, commitDraft]
  );

  const createConnection = useCallback(
    (fromSpaceId: string, toSpaceId: string) => {
      const ordinal = nextConnectionOrdinal();
      const connectionId = uniqueId(
        `conn-${ordinal}`,
        draft.connections.map((connection) => connection.connectionId)
      );
      commitDraft({
        ...draft,
        connections: [
          ...draft.connections,
          { connectionId, fromSpaceId, toSpaceId, type: "land" },
        ],
      });
      setSelection({ type: "connection", id: connectionId });
      setMessage("Связь добавлена.");
    },
    [draft, nextConnectionOrdinal, commitDraft]
  );

  const deleteConnection = useCallback(
    (connectionId: string) => {
      commitDraft({
        ...draft,
        connections: draft.connections.filter(
          (connection) => connection.connectionId !== connectionId
        ),
      });
      setSelection({ type: null, id: null });
      setMessage("Связь удалена.");
    },
    [draft, commitDraft]
  );

  const runValidation = useCallback(() => {
    const result = validateMapDraft(draft);
    setValidation(result);
    setMessage(result.errors.length > 0 ? "Есть ошибки." : "Проверка пройдена.");
  }, [draft]);

  const saveDraft = useCallback(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(draft));
    setMessage("Черновик сохранён.");
  }, [draft]);

  const loadDraft = useCallback(() => {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) { setMessage("Нет сохранённого черновика."); return; }
    try {
      const parsed = JSON.parse(raw) as MapDraft;
      if (!parsed.underlay) parsed.underlay = { ...DEFAULT_UNDERLAY };
      if (!parsed.editorSettings) parsed.editorSettings = { ...DEFAULT_EDITOR_SETTINGS };
      // 0020 correction: expand coordinateSystem to fit underlay
      if (parsed.underlay) {
        const uw = parsed.underlay.naturalWidth;
        const uh = parsed.underlay.naturalHeight;
        if (uw > parsed.coordinateSystem.width || uh > parsed.coordinateSystem.height) {
          parsed.coordinateSystem = { type: "pixel", width: Math.max(parsed.coordinateSystem.width, uw), height: Math.max(parsed.coordinateSystem.height, uh) };
        }
      }
      onDraftChange(parsed);
      setHistory({ past: [], future: [] });
      setMessage("Черновик загружен.");
    } catch {
      setMessage("Не удалось загрузить черновик.");
    }
  }, [onDraftChange]);

  const handleWheel = useCallback(
    (event: React.WheelEvent<HTMLDivElement>) => {
      event.preventDefault();

      const oldZoom = view.zoom;
      const nextZoom = Math.max(
        0.2,
        Math.min(3, oldZoom * (event.deltaY > 0 ? 0.92 : 1.08))
      );
      const rect = canvasRef.current?.getBoundingClientRect();
      if (!rect) {
        return;
      }

      const anchorWorldX = (event.clientX - rect.left - view.panX) / oldZoom;
      const anchorWorldY = (event.clientY - rect.top - view.panY) / oldZoom;

      setView({
        zoom: Math.round(nextZoom * 100) / 100,
        panX: event.clientX - rect.left - anchorWorldX * nextZoom,
        panY: event.clientY - rect.top - anchorWorldY * nextZoom,
      });
    },
    [view]
  );

  const handleCanvasMouseDown = useCallback(
    (event: React.MouseEvent<HTMLDivElement>) => {
      const worldPoint = getWorldPoint(event.clientX, event.clientY);
      if (tool === "space") { addSpace(worldPoint.x, worldPoint.y); return; }
      if (tool === "pan") {
        event.preventDefault();
        dragRef.current = {
          type: "pan",
          startClientX: event.clientX, startClientY: event.clientY,
          originPanX: view.panX, originPanY: view.panY,
        };
        return;
      }
      if (tool === "select") {
        setSelection({ type: null, id: null });
        setContextMenu(null);
        setLinkStart(null);
      }
    },
    [addSpace, getWorldPoint, tool, view.panX, view.panY]
  );

  // 0020: underlay mouse handlers
  // 0020: underlay mouse handlers (accept any Element for SVG/HTML compatibility)
  const handleUnderlayMouseDown = useCallback(
    (event: React.MouseEvent<Element>) => {
      event.stopPropagation();
      if (!underlay || underlay.locked) return;
      if (tool !== "select") return; // only select tool interacts with underlay
      setSelection({ type: "underlay", id: "underlay" });
      const wp = getWorldPoint(event.clientX, event.clientY);
      dragRef.current = {
        type: "underlayMove",
        startWorldX: wp.x, startWorldY: wp.y,
        originOffsetX: underlay.offsetX, originOffsetY: underlay.offsetY,
      };
    },
    [getWorldPoint, underlay, tool]
  );

  const handleUnderlayContextMenu = useCallback(
    (event: React.MouseEvent<Element>) => {
      event.preventDefault(); event.stopPropagation();
      setSelection({ type: "underlay", id: "underlay" });
      setContextMenu({ type: "underlay", id: "underlay", x: event.clientX, y: event.clientY });
    }, []
  );

  /** 0026 correction: center-radial scale — corner param kept for UI but unused (V2 review) */
  const handleScaleHandleMouseDown = useCallback(
    (event: React.MouseEvent<Element>, _corner: "nw" | "ne" | "sw" | "se") => {
      event.stopPropagation(); event.preventDefault();
      if (!underlay || underlay.locked) return;
      const wp = getWorldPoint(event.clientX, event.clientY);
      const originUnderlay = { ...underlay };
      const cx = underlay.naturalWidth / 2;
      const cy = underlay.naturalHeight / 2;
      const center = mapLocalToWorld(cx, cy, originUnderlay);
      const startDist = Math.sqrt((wp.x - center.x) ** 2 + (wp.y - center.y) ** 2);
      dragRef.current = {
        type: "underlayScale",
        startWorldX: wp.x, startWorldY: wp.y,
        originScale: underlay.scale,
        centerWorldX: center.x, centerWorldY: center.y,
        startDistance: Math.max(1, startDist),
      };
    }, [getWorldPoint, underlay]
  );

  const handleRotateHandleMouseDown = useCallback(
    (event: React.MouseEvent<Element>) => {
      event.stopPropagation(); event.preventDefault();
      if (!underlay || underlay.locked) return;
      const cx = underlay.offsetX + (underlay.naturalWidth * underlay.scale) / 2;
      const cy = underlay.offsetY + (underlay.naturalHeight * underlay.scale) / 2;
      const wp = getWorldPoint(event.clientX, event.clientY);
      dragRef.current = {
        type: "underlayRotate",
        startWorldX: wp.x, startWorldY: wp.y,
        originRotation: underlay.rotation,
        centerWorldX: cx, centerWorldY: cy,
      };
    }, [getWorldPoint, underlay]
  );

  const handleSpaceMouseDown = useCallback(
    (event: React.MouseEvent<SVGGElement>, spaceId: string) => {
      event.stopPropagation();
      if (tool === "connection") {
        if (!linkStart) {
          setLinkStart(spaceId); setSelection({ type: "space", id: spaceId });
          setMessage("Выберите вторую точку."); return;
        }
        if (linkStart === spaceId) { setMessage("Нельзя связать точку саму с собой."); return; }
        createConnection(linkStart, spaceId); setLinkStart(null); setTool("select"); return;
      }
      if (tool === "select") {
        setSelection({ type: "space", id: spaceId }); setLinkStart(null);
        const space = spacesById[spaceId];
        if (!space) return;
        // 0020: drag в map-local координатах
        const wp = getWorldPoint(event.clientX, event.clientY);
        const local = worldToMapLocal(wp.x, wp.y, underlay);
        dragRef.current = {
          type: "spaceMove", id: spaceId,
          startWorldX: local.x, startWorldY: local.y,
          originX: space.x, originY: space.y,
        };
        return;
      }
      if (tool === "space") { setSelection({ type: "space", id: spaceId }); setLinkStart(null); }
    },
    [createConnection, getWorldPoint, linkStart, spacesById, tool, underlay]
  );

  const handleSpaceContextMenu = useCallback(
    (event: React.MouseEvent<SVGGElement>, spaceId: string) => {
      event.preventDefault();
      event.stopPropagation();
      setSelection({ type: "space", id: spaceId });
      setContextMenu({
        type: "space",
        id: spaceId,
        x: event.clientX,
        y: event.clientY,
      });
    },
    []
  );

  const handleConnectionMouseDown = useCallback(
    (event: React.MouseEvent<SVGLineElement>, connectionId: string) => {
      event.stopPropagation();
      if (tool === "select") {
        setSelection({ type: "connection", id: connectionId });
        setLinkStart(null);
      }
    },
    [tool]
  );

  const handleConnectionContextMenu = useCallback(
    (event: React.MouseEvent<SVGLineElement>, connectionId: string) => {
      event.preventDefault();
      event.stopPropagation();
      setSelection({ type: "connection", id: connectionId });
      setContextMenu({
        type: "connection",
        id: connectionId,
        x: event.clientX,
        y: event.clientY,
      });
    },
    []
  );

  const handleMouseMove = useCallback(
    (event: React.MouseEvent<HTMLDivElement>) => {
      const drag = dragRef.current;
      if (!drag) return;
      if (drag.type === "spaceMove") {
        const wp = getWorldPoint(event.clientX, event.clientY);
        const local = worldToMapLocal(wp.x, wp.y, underlay);
        moveSpace(drag.id, drag.originX + (local.x - drag.startWorldX), drag.originY + (local.y - drag.startWorldY));
        return;
      }
      if (drag.type === "pan") {
        setView((prev) => ({
          ...prev,
          panX: drag.originPanX + (event.clientX - drag.startClientX),
          panY: drag.originPanY + (event.clientY - drag.startClientY),
        }));
        return;
      }
      // 0020: underlay drag
      if (drag.type === "underlayMove" && underlay) {
        const wp = getWorldPoint(event.clientX, event.clientY);
        const dx = wp.x - drag.startWorldX; const dy = wp.y - drag.startWorldY;
        onDraftChange({
          ...draft,
          underlay: {
            ...underlay,
            offsetX: snapValue(drag.originOffsetX + dx, editorSettings.gridSize, editorSettings.snapToGrid),
            offsetY: snapValue(drag.originOffsetY + dy, editorSettings.gridSize, editorSettings.snapToGrid),
          },
        });
        return;
      }
      /** 0026 correction: center-radial scale from V2 review — rotation-invariant */
      if (drag.type === "underlayScale" && underlay) {
        const wp = getWorldPoint(event.clientX, event.clientY);
        const currentDist = Math.sqrt(
          (wp.x - drag.centerWorldX) ** 2 + (wp.y - drag.centerWorldY) ** 2
        );
        const nextScale = Math.max(
          0.1,
          Math.round((drag.originScale * currentDist) / drag.startDistance * 100) / 100
        );
        onDraftChange({
          ...draft,
          underlay: { ...underlay, scale: nextScale },
        });
        return;
      }
      if (drag.type === "underlayRotate" && underlay) {
        const wp = getWorldPoint(event.clientX, event.clientY);
        const sa = angleDeg(drag.centerWorldX, drag.centerWorldY, drag.startWorldX, drag.startWorldY);
        const ca = angleDeg(drag.centerWorldX, drag.centerWorldY, wp.x, wp.y);
        let nr = drag.originRotation + (ca - sa);
        if (event.shiftKey) nr = Math.round(nr / 15) * 15;
        nr = Math.round(nr * 100) / 100;
        onDraftChange({ ...draft, underlay: { ...underlay, rotation: nr } });
        return;
      }
    },
    [getWorldPoint, moveSpace, underlay, editorSettings, draft, onDraftChange]
  );

  const stopDragging = useCallback(() => {
    if (dragRef.current) {
      setHistory((h) => ({ past: pushHistory(h.past, draft), future: [] }));
    }
    dragRef.current = null;
  }, [draft]);

  const closeContextMenu = useCallback(() => {
    setContextMenu(null);
  }, []);

  const getSpacePosition = useCallback(
    (spaceId: string): WorldPoint | null => {
      const space = spacesById[spaceId];
      return space ? { x: space.x, y: space.y } : null;
    },
    [spacesById]
  );

  const isSelectedSpace = useCallback(
    (spaceId: string) => selection.type === "space" && selection.id === spaceId,
    [selection.id, selection.type]
  );

  const isSelectedConnection = useCallback(
    (connectionId: string) =>
      selection.type === "connection" && selection.id === connectionId,
    [selection.id, selection.type]
  );

  const toolIcon = (currentTool: Tool): string =>
    ({ select: "⬚", space: "➕", connection: "🔗", pan: "✋" })[currentTool];

  const toolLabel = (currentTool: Tool): string =>
    ({
      select: "Выбрать",
      space: "Точка",
      connection: "Связь",
      pan: "Двигать",
    })[currentTool];

  return (
    <div
      className="editor-shell"
      onMouseMove={handleMouseMove}
      onMouseUp={stopDragging}
      onMouseLeave={stopDragging}
      onClick={closeContextMenu}
    >
      <header className="editor-header">
        <h2 className="editor-title">Редактор карты — {draft.name}</h2>

        <div className="editor-toolbar">
          {(["select", "space", "connection", "pan"] as Tool[]).map(
            (currentTool) => (
              <button
                key={currentTool}
                className={`editor-tool-pill ${tool === currentTool ? "editor-tool-pill-active" : ""}`}
                onClick={() => setToolWithMessage(currentTool)}
              >
                {toolIcon(currentTool)} {toolLabel(currentTool)}
              </button>
            )
          )}

          <span className="editor-toolbar-sep">|</span>

          {/* 0020: Grid + Snap toggles */}
          <button
            className={`editor-tool-pill ${editorSettings.gridVisible ? "editor-tool-pill-active" : ""}`}
            onClick={() => updateEditorSettings({ gridVisible: !editorSettings.gridVisible })}
            title="Сетка"
          >▦ Сетка</button>
          <button
            className={`editor-tool-pill ${editorSettings.snapToGrid ? "editor-tool-pill-active" : ""}`}
            onClick={() => updateEditorSettings({ snapToGrid: !editorSettings.snapToGrid })}
            title="Привязка к сетке"
          >⊞ Snap</button>

          <span className="editor-toolbar-sep">|</span>

          {/* 0020: Undo / Redo */}
          <button className="editor-btn" onClick={undo} disabled={history.past.length === 0} title="Отменить (Ctrl+Z)">↩</button>
          <button className="editor-btn" onClick={redo} disabled={history.future.length === 0} title="Повторить (Ctrl+Y)">↪</button>

          <span className="editor-toolbar-sep">|</span>

          {/* 0020: Underlay visibility/lock/reset */}
          {underlay && (<>
            <button
              className={`editor-tool-pill ${underlay.visible ? "editor-tool-pill-active" : ""}`}
              onClick={() => commitDraft({ ...draft, underlay: { ...underlay, visible: !underlay.visible } })}
              title="Показать/скрыть подложку"
            >👁</button>
            <button
              className={`editor-tool-pill ${underlay.locked ? "editor-tool-pill-active" : ""}`}
              onClick={() => commitDraft({ ...draft, underlay: { ...underlay, locked: !underlay.locked } })}
              title="Закрепить/освободить подложку"
            >{underlay.locked ? "🔒" : "🔓"}</button>
            <button className="editor-btn" onClick={resetUnderlayRotation} title="Сбросить поворот">↺</button>
            <button className="editor-btn" onClick={resetUnderlayTransform} title="Сбросить трансформацию">⟲</button>
          </>)}

          <span className="editor-toolbar-sep">|</span>

          <button className="editor-btn editor-btn-validate" onClick={runValidation}>✅</button>
          <button className="editor-btn editor-btn-preview" onClick={() => onPreview(draft)}>▶</button>
          <button className="editor-btn editor-btn-save" onClick={saveDraft}>💾</button>
          <button className="editor-btn editor-btn-load" onClick={loadDraft}>📂</button>
        </div>

        <span className="editor-status">{message}</span>
      </header>

      <div className="editor-body">
        <aside className="editor-left-panel">
          <TreeSection
            title="Точки"
            count={draft.spaces.length}
            defaultOpen={true}
          >
            {draft.spaces.map((space) => (
              <TreeItem
                key={space.spaceId}
                name={space.name}
                meta={space.spaceId}
                active={isSelectedSpace(space.spaceId)}
                onClick={() => {
                  setSelection({ type: "space", id: space.spaceId });
                  setLinkStart(null);
                }}
                onDelete={() => deleteSpace(space.spaceId)}
              />
            ))}
          </TreeSection>

          <TreeSection
            title="Связи"
            count={draft.connections.length}
            defaultOpen={true}
          >
            {draft.connections.map((connection) => (
              <TreeItem
                key={connection.connectionId}
                name={`${connection.fromSpaceId} → ${connection.toSpaceId}`}
                meta={connection.connectionId}
                active={isSelectedConnection(connection.connectionId)}
                onClick={() => { setSelection({ type: "connection", id: connection.connectionId }); setLinkStart(null); }}
                onDelete={() => deleteConnection(connection.connectionId)}
              />
            ))}
          </TreeSection>

          {/* 0020: Underlay in object tree */}
          {underlay && (
            <TreeSection title="Подложка" count={1} defaultOpen={true}>
              <TreeItem
                name="Карта-подложка"
                meta={underlay.src ? "изображение" : "placeholder"}
                active={selection.type === "underlay"}
                onClick={() => setSelection({ type: "underlay", id: "underlay" })}
                onDelete={() => { commitDraft({ ...draft, underlay: null }); setSelection({ type: null, id: null }); }}
              />
            </TreeSection>
          )}
        </aside>

        <div
          className={`editor-canvas ${
            tool === "pan"
              ? "editor-canvas-pan"
              : tool === "space"
                ? "editor-canvas-space"
                : ""
          }`}
          ref={canvasRef}
          onMouseDown={handleCanvasMouseDown}
          onContextMenu={(event) => {
            event.preventDefault();
            const worldPoint = getWorldPoint(event.clientX, event.clientY);
            setContextMenu({
              type: "canvas",
              x: event.clientX,
              y: event.clientY,
              worldX: worldPoint.x,
              worldY: worldPoint.y,
            });
          }}
          onWheel={handleWheel}
        >
          <div
            className="editor-stage"
            style={{
              width: stageWidth,
              height: stageHeight,
              left: view.panX,
              top: view.panY,
            }}
          >
            {/* 0020: SVG — underlay, grid, connections, spaces, handles all in ONE map-plane transform group */}
            <svg
              className="editor-svg-root"
              width={stageWidth}
              height={stageHeight}
              viewBox={`0 0 ${mapW} ${mapH}`}
            >
              <rect x={0} y={0} width={mapW} height={mapH} className="editor-map-bounds" />

              {/* 0020: Defs (shared) */}
              <defs>
                <linearGradient id="underlay-placeholder-grad" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#1a2a1a" />
                  <stop offset="100%" stopColor="#0d1a0d" />
                </linearGradient>
                <pattern id="editor-grid" width={editorSettings.gridSize} height={editorSettings.gridSize} patternUnits="userSpaceOnUse">
                  <rect width={editorSettings.gridSize} height={editorSettings.gridSize} fill="none" />
                  <path d={`M ${editorSettings.gridSize} 0 L 0 0 0 ${editorSettings.gridSize}`} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="0.5" />
                </pattern>
              </defs>

              {/* 0020: Map-plane transform group */}
              <g transform={underlay && underlay.visible
                ? `translate(${underlay.offsetX}, ${underlay.offsetY}) translate(${underlay.naturalWidth / 2}, ${underlay.naturalHeight / 2}) scale(${underlay.scale}) rotate(${underlay.rotation}) translate(${-underlay.naturalWidth / 2}, ${-underlay.naturalHeight / 2})`
                : undefined}>

                {/* 0020 correction: Grid inside map-plane group — map-plane grid */}
                {editorSettings.gridVisible && (
                  <rect x={-10000} y={-10000} width={20000} height={20000} fill="url(#editor-grid)" />
                )}

                {/* ---- Underlay layer ---- */}
                {underlay && underlay.visible && (
                  <>
                    {underlay.src ? (
                      <image href={underlay.src} x={0} y={0}
                        width={underlay.naturalWidth} height={underlay.naturalHeight}
                        opacity={underlay.opacity / 100}
                        preserveAspectRatio="none" />
                    ) : (
                      <g opacity={underlay.opacity / 100}>
                        <rect x={0} y={0} width={underlay.naturalWidth} height={underlay.naturalHeight}
                          fill="url(#underlay-placeholder-grad)" stroke="rgba(255,255,255,0.12)" strokeWidth="2" strokeDasharray="8 4" />
                        <text x={underlay.naturalWidth / 2} y={underlay.naturalHeight / 2 - 8}
                          textAnchor="middle" fill="rgba(255,255,255,0.25)" fontSize="14" fontFamily="Georgia, serif">Карта-подложка</text>
                        <text x={underlay.naturalWidth / 2} y={underlay.naturalHeight / 2 + 10}
                          textAnchor="middle" fill="rgba(255,255,255,0.15)" fontSize="10" fontFamily="Georgia, serif">подложка редактора</text>
                      </g>
                    )}
                    {/* Selection outline */}
                    {selection.type === "underlay" && (
                      <rect x={0} y={0} width={underlay.naturalWidth} height={underlay.naturalHeight}
                        fill="none" stroke="rgba(88,166,255,0.7)" strokeWidth="2" strokeDasharray="4 2" />
                    )}
                    {/* Hit rect: only intercepts clicks in select mode, passes through for space tool */}
                    <rect x={0} y={0} width={underlay.naturalWidth} height={underlay.naturalHeight}
                      fill="transparent"
                      style={{ cursor: underlay.locked ? "default" : (tool === "select" ? "move" : "crosshair"), pointerEvents: tool === "select" ? "all" : "none" }}
                      onMouseDown={handleUnderlayMouseDown}
                      onContextMenu={handleUnderlayContextMenu} />
                  </>
                )}

                {/* ---- Connections ---- */}
                {draft.connections.map((connection) => {
                  const from = getSpacePosition(connection.fromSpaceId);
                  const to = getSpacePosition(connection.toSpaceId);
                  if (!from || !to) return null;
                  const selected = isSelectedConnection(connection.connectionId);
                  return (
                    <g key={connection.connectionId}>
                      <line x1={from.x} y1={from.y} x2={to.x} y2={to.y} className="editor-connection-hit"
                        onMouseDown={(event) => handleConnectionMouseDown(event, connection.connectionId)}
                        onContextMenu={(event) => handleConnectionContextMenu(event, connection.connectionId)} />
                      <line x1={from.x} y1={from.y} x2={to.x} y2={to.y}
                        className={selected ? "editor-connection editor-connection-selected" : "editor-connection"} />
                    </g>
                  );
                })}

                {/* ---- Spaces ---- */}
                {draft.spaces.map((space) => {
                  const selected = isSelectedSpace(space.spaceId);
                  const linkSource = linkStart === space.spaceId;
                  return (
                    <g key={space.spaceId} className="editor-space-group"
                      onMouseDown={(event) => handleSpaceMouseDown(event, space.spaceId)}
                      onContextMenu={(event) => handleSpaceContextMenu(event, space.spaceId)}>
                      <circle cx={space.x} cy={space.y} r={SPACE_RADIUS + 8} className="editor-space-hit" />
                      <circle cx={space.x} cy={space.y} r={SPACE_RADIUS}
                        className={`editor-space-node ${selected ? "editor-space-node-selected" : ""} ${linkSource ? "editor-space-node-link-from" : ""}`} />
                      <text x={space.x + 16} y={space.y + 3}
                        className={`editor-space-text ${selected ? "editor-space-text-selected" : ""}`}>{space.name}</text>
                    </g>
                  );
                })}

                {/* ---- Underlay handles (SVG, inside map-plane, geometry matches underlay) ---- */}
                {underlay && underlay.visible && selection.type === "underlay" && !underlay.locked && (
                  <g style={{ pointerEvents: "all" }}>
                    {/* Scale handles at 4 corners */}
                    <rect x={-HANDLE_SIZE/2} y={-HANDLE_SIZE/2} width={HANDLE_SIZE} height={HANDLE_SIZE}
                      fill="#58a6ff" stroke="#0d1117" strokeWidth="1" style={{ cursor: "nw-resize" }}
                      onMouseDown={(e) => handleScaleHandleMouseDown(e as any, "nw")} />
                    <rect x={underlay.naturalWidth - HANDLE_SIZE/2} y={-HANDLE_SIZE/2} width={HANDLE_SIZE} height={HANDLE_SIZE}
                      fill="#58a6ff" stroke="#0d1117" strokeWidth="1" style={{ cursor: "ne-resize" }}
                      onMouseDown={(e) => handleScaleHandleMouseDown(e as any, "ne")} />
                    <rect x={-HANDLE_SIZE/2} y={underlay.naturalHeight - HANDLE_SIZE/2} width={HANDLE_SIZE} height={HANDLE_SIZE}
                      fill="#58a6ff" stroke="#0d1117" strokeWidth="1" style={{ cursor: "sw-resize" }}
                      onMouseDown={(e) => handleScaleHandleMouseDown(e as any, "sw")} />
                    <rect x={underlay.naturalWidth - HANDLE_SIZE/2} y={underlay.naturalHeight - HANDLE_SIZE/2} width={HANDLE_SIZE} height={HANDLE_SIZE}
                      fill="#58a6ff" stroke="#0d1117" strokeWidth="1" style={{ cursor: "se-resize" }}
                      onMouseDown={(e) => handleScaleHandleMouseDown(e as any, "se")} />
                    {/* Rotate handle + line */}
                    <line x1={underlay.naturalWidth / 2} y1={0} x2={underlay.naturalWidth / 2} y2={-ROTATE_HANDLE_DISTANCE}
                      stroke="rgba(240,192,64,0.4)" strokeWidth="1" />
                    <circle cx={underlay.naturalWidth / 2} cy={-ROTATE_HANDLE_DISTANCE} r={HANDLE_SIZE/2}
                      fill="#f0c040" stroke="#0d1117" strokeWidth="1" style={{ cursor: "grab" }}
                      onMouseDown={handleRotateHandleMouseDown} />
                  </g>
                )}
              </g>
            </svg>
          </div>

          {draft.spaces.length === 0 && (
            <div className="editor-canvas-hint">
              ➕ Точка — клик на холст. ✋ — двигать. Колёсико — зум.
            </div>
          )}
        </div>

        <aside className="editor-right-panel">
          {selectedObject && selection.type === "space" ? (
            <SpaceInspector space={selectedObject as SpaceDraft} onRename={renameSpace} onDelete={deleteSpace} />
          ) : selectedObject && selection.type === "connection" ? (
            <ConnectionInspector connection={selectedObject as ConnectionDraft} spacesById={spacesById} onDelete={deleteConnection} />
          ) : selection.type === "underlay" && underlay ? (
            <UnderlayInspector underlay={underlay} onUpdate={updateUnderlay}
              onDelete={() => { commitDraft({ ...draft, underlay: null }); setSelection({ type: null, id: null }); }}
              fileRef={fileRef} onImageLoad={handleUnderlayImageLoad} />
          ) : (
            <div className="editor-inspector-empty">
              <Section title="Инспектор">
                <p className="editor-empty-text">Выберите точку, связь или подложку.</p>
              </Section>
            </div>
          )}
        </aside>
      </div>

      {validation && (
        <ValidationPanel
          result={validation}
          onClose={() => setValidation(null)}
        />
      )}

      {contextMenu && (
        <ContextMenu
          contextMenu={contextMenu}
          onClose={closeContextMenu}
          onAdd={(x, y) => { addSpace(x, y); closeContextMenu(); }}
          onDeleteSpace={() => { if (contextMenu.type === "space") { deleteSpace(contextMenu.id); } closeContextMenu(); }}
          onDeleteConnection={() => { if (contextMenu.type === "connection") { deleteConnection(contextMenu.id); } closeContextMenu(); }}
          onToggleUnderlayVisibility={() => { if (underlay) { updateUnderlay({ visible: !underlay.visible }); } closeContextMenu(); }}
          onToggleUnderlayLock={() => { if (underlay) { updateUnderlay({ locked: !underlay.locked }); } closeContextMenu(); }}
        />
      )}
    </div>
  );
}

function TreeSection({
  title,
  count,
  defaultOpen,
  children,
}: {
  title: string;
  count: number;
  defaultOpen: boolean;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div className="editor-tree-section">
      <div className="editor-tree-header" onClick={() => setOpen(!open)}>
        <span className="editor-tree-caret">{open ? "▼" : "▶"}</span>
        <span className="editor-tree-title">{title}</span>
        <span className="editor-tree-count">{count}</span>
      </div>
      {open && <div className="editor-tree-body">{children}</div>}
    </div>
  );
}

function TreeItem({
  name,
  meta,
  active,
  onClick,
  onDelete,
}: {
  name: string;
  meta: string;
  active: boolean;
  onClick: () => void;
  onDelete: () => void;
}) {
  return (
    <div
      className={`editor-tree-item ${
        active ? "editor-tree-item-active" : ""
      }`}
      onClick={onClick}
    >
      <span className="editor-tree-item-name">{name}</span>
      <span className="editor-tree-item-meta">{meta}</span>
      <button
        className="editor-tree-item-delete"
        onClick={(event) => {
          event.stopPropagation();
          onDelete();
        }}
        title="Удалить"
      >
        ×
      </button>
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
    <div className="editor-section">
      <h4 className="editor-section-title">{title}</h4>
      <div className="editor-section-body">{children}</div>
    </div>
  );
}

function Field({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div className="editor-field">
      <label className="editor-field-label">{label}</label>
      <div className="editor-field-value">{children}</div>
    </div>
  );
}

function SpaceInspector({
  space,
  onRename,
  onDelete,
}: {
  space: SpaceDraft;
  onRename: (spaceId: string, name: string) => void;
  onDelete: (spaceId: string) => void;
}) {
  return (
    <div className="editor-inspector">
      <Section title="Точка">
        <Field label="ID">
          <span className="editor-mono">{space.spaceId}</span>
        </Field>
        <Field label="Название">
          <input
            className="editor-input"
            value={space.name}
            onChange={(event) => onRename(space.spaceId, event.target.value)}
          />
        </Field>
        <Field label="X">
          <span className="editor-mono">{space.x}</span>
        </Field>
        <Field label="Y">
          <span className="editor-mono">{space.y}</span>
        </Field>
        <Field label="Тип">
          <span className="editor-mono">{space.type}</span>
        </Field>
      </Section>
      <Section title="Действия">
        <button
          className="editor-btn editor-btn-delete"
          onClick={() => onDelete(space.spaceId)}
        >
          🗑 Удалить точку
        </button>
      </Section>
    </div>
  );
}

function ConnectionInspector({
  connection,
  spacesById,
  onDelete,
}: {
  connection: ConnectionDraft;
  spacesById: Record<string, SpaceDraft>;
  onDelete: (connectionId: string) => void;
}) {
  const fromName = spacesById[connection.fromSpaceId]?.name ?? connection.fromSpaceId;
  const toName = spacesById[connection.toSpaceId]?.name ?? connection.toSpaceId;
  return (
    <div className="editor-inspector">
      <Section title="Связь">
        <Field label="ID"><span className="editor-mono">{connection.connectionId}</span></Field>
        <Field label="От"><span className="editor-mono">{fromName}</span></Field>
        <Field label="До"><span className="editor-mono">{toName}</span></Field>
        <Field label="Тип"><span className="editor-mono">{connection.type}</span></Field>
      </Section>
      <Section title="Действия">
        <button className="editor-btn editor-btn-delete" onClick={() => onDelete(connection.connectionId)}>🗑 Удалить связь</button>
      </Section>
    </div>
  );
}

/** 0020: Underlay inspector (right panel) */
function UnderlayInspector({
  underlay,
  onUpdate,
  onDelete,
  fileRef,
  onImageLoad,
}: {
  underlay: UnderlayState;
  onUpdate: (patch: Partial<UnderlayState>) => void;
  onDelete: () => void;
  fileRef: React.RefObject<HTMLInputElement>;
  onImageLoad: (e: React.ChangeEvent<HTMLInputElement>) => void;
}) {
  return (
    <div className="editor-inspector">
      <Section title="Подложка">
        <Field label="Тип"><span className="editor-mono">{underlay.src ? "изображение" : "placeholder"}</span></Field>
        <Field label="X"><span className="editor-mono">{Math.round(underlay.offsetX)}</span></Field>
        <Field label="Y"><span className="editor-mono">{Math.round(underlay.offsetY)}</span></Field>
        <Field label="Масштаб"><span className="editor-mono">{Math.round(underlay.scale * 100)}%</span></Field>
        <Field label="Поворот"><span className="editor-mono">{Math.round(underlay.rotation)}°</span></Field>
        <Field label="Размер"><span className="editor-mono">{underlay.naturalWidth}×{underlay.naturalHeight}</span></Field>
      </Section>
      <Section title="Прозрачность">
        <Field label="Opacity">
          <input className="editor-input" type="range" min={0} max={100} value={underlay.opacity}
            onChange={(e) => onUpdate({ opacity: Number(e.target.value) })} />
          <span className="editor-mono">{underlay.opacity}%</span>
        </Field>
      </Section>
      <Section title="Состояние">
        <Field label="Видима">
          <button className="editor-btn" onClick={() => onUpdate({ visible: !underlay.visible })}>{underlay.visible ? "👁 Да" : "🚫 Нет"}</button>
        </Field>
        <Field label="Закреплена">
          <button className="editor-btn" onClick={() => onUpdate({ locked: !underlay.locked })}>{underlay.locked ? "🔒 Да" : "🔓 Нет"}</button>
        </Field>
      </Section>
      <Section title="Трансформация">
        <Field label="Смещение X">
          <input className="editor-input" type="number" value={Math.round(underlay.offsetX)}
            onChange={(e) => onUpdate({ offsetX: Number(e.target.value) })} />
        </Field>
        <Field label="Смещение Y">
          <input className="editor-input" type="number" value={Math.round(underlay.offsetY)}
            onChange={(e) => onUpdate({ offsetY: Number(e.target.value) })} />
        </Field>
        <Field label="Масштаб %">
          <input className="editor-input" type="number" min={10} max={1000} value={Math.round(underlay.scale * 100)}
            onChange={(e) => onUpdate({ scale: Math.max(0.1, Number(e.target.value) / 100) })} />
        </Field>
        <Field label="Поворот °">
          <input className="editor-input" type="number" value={Math.round(underlay.rotation)}
            onChange={(e) => onUpdate({ rotation: Number(e.target.value) })} />
        </Field>
        <Field label="Сброс">
          <button className="editor-btn" onClick={() => onUpdate({
            offsetX: DEFAULT_UNDERLAY.offsetX, offsetY: DEFAULT_UNDERLAY.offsetY,
            scale: DEFAULT_UNDERLAY.scale, rotation: DEFAULT_UNDERLAY.rotation,
          })}>⟲ Сбросить всё</button>
        </Field>
      </Section>
      <Section title="Действия">
        <Field label="Изображение">
          <input ref={fileRef} type="file" accept="image/*" style={{ display: "none" }}
            onChange={onImageLoad} />
          <button className="editor-btn" onClick={() => fileRef.current?.click()}
            style={{ borderColor: "#4a4a8a" }}>📁 Загрузить карту</button>
        </Field>
        <button className="editor-btn editor-btn-delete" onClick={onDelete}>🗑 Удалить подложку</button>
      </Section>
    </div>
  );
}

function ValidationPanel({
  result,
  onClose,
}: {
  result: MapValidation;
  onClose: () => void;
}) {
  return (
    <div className="editor-validation-overlay" onClick={onClose}>
      <div
        className="editor-validation-panel"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="editor-validation-header">
          <span className="editor-validation-title">
            {result.errors.length > 0 ? "⚠ Ошибки" : "✅ OK"}
          </span>
          <button className="editor-validation-close" onClick={onClose}>
            ×
          </button>
        </div>

        {result.errors.length === 0 && result.warnings.length === 0 && (
          <p className="editor-validation-ok">Ошибок нет.</p>
        )}

        {result.errors.length > 0 && (
          <div className="editor-validation-errors">
            <h4>Ошибки</h4>
            <ul>
              {result.errors.map((message, index) => (
                <li key={index}>{message}</li>
              ))}
            </ul>
          </div>
        )}

        {result.warnings.length > 0 && (
          <div className="editor-validation-warnings">
            <h4>Предупреждения</h4>
            <ul>
              {result.warnings.map((message, index) => (
                <li key={index}>{message}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

function ContextMenu({
  contextMenu,
  onClose,
  onAdd,
  onDeleteSpace,
  onDeleteConnection,
  onToggleUnderlayVisibility,
  onToggleUnderlayLock,
}: {
  contextMenu: ContextMenuState;
  onClose: () => void;
  onAdd: (x: number, y: number) => void;
  onDeleteSpace: () => void;
  onDeleteConnection: () => void;
  onToggleUnderlayVisibility: () => void;
  onToggleUnderlayLock: () => void;
}) {
  return (
    <div className="editor-context-menu" onClick={onClose}>
      <div className="editor-context-menu-inner" style={{ left: contextMenu.x, top: contextMenu.y }}
        onClick={(event) => event.stopPropagation()}>
        {contextMenu.type === "canvas" && (
          <div className="editor-context-item" onClick={() => onAdd(contextMenu.worldX, contextMenu.worldY)}>📍 Добавить точку</div>
        )}
        {contextMenu.type === "space" && (
          <div className="editor-context-item" onClick={onDeleteSpace}>🗑 Удалить точку</div>
        )}
        {contextMenu.type === "connection" && (
          <div className="editor-context-item" onClick={onDeleteConnection}>🗑 Удалить связь</div>
        )}
        {contextMenu.type === "underlay" && (<>
          <div className="editor-context-item" onClick={onToggleUnderlayVisibility}>👁 Показать/скрыть</div>
          <div className="editor-context-item" onClick={onToggleUnderlayLock}>🔒 Закрепить/освободить</div>
        </>)}
        <div className="editor-context-separator" />
        <div className="editor-context-item" onClick={onClose}>✕ Закрыть</div>
      </div>
    </div>
  );
}
