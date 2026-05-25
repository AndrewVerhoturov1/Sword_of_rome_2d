import { useCallback, useMemo, useRef, useState } from "react";
import mapData from "../fixtures/tiny-module/modules/tiny-module/map.json";
import {
  type ConnectionDraft,
  type MapDraft,
  type MapValidation,
  type SpaceDraft,
  uniqueId,
  validateMapDraft,
} from "./MapDraft";
import "./Editor.css";

const CANVAS_W = mapData.coordinateSystem.width;
const CANVAS_H = mapData.coordinateSystem.height;
const STORAGE_KEY = "table-sandbox-editor-draft";
const SPACE_RADIUS = 8;

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
      type: "space" | "connection";
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
    };

export default function EditorSurface({
  draft,
  onDraftChange,
  onPreview,
}: EditorSurfaceProps) {
  const [tool, setTool] = useState<Tool>("select");
  const [selection, setSelection] = useState<{
    type: "space" | "connection" | null;
    id: string | null;
  }>({ type: null, id: null });
  const [validation, setValidation] = useState<MapValidation | null>(null);
  const [linkStart, setLinkStart] = useState<string | null>(null);
  const [message, setMessage] = useState("Готово");
  const [contextMenu, setContextMenu] = useState<ContextMenuState | null>(null);
  const [view, setView] = useState<ViewState>({ zoom: 1, panX: 0, panY: 0 });

  const dragRef = useRef<DragState | null>(null);
  const canvasRef = useRef<HTMLDivElement>(null);

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
        : null;

  const stageWidth = CANVAS_W * view.zoom;
  const stageHeight = CANVAS_H * view.zoom;

  const nextSpaceOrdinal = useCallback(
    () => draft.spaces.length + 1,
    [draft.spaces.length]
  );

  const nextConnectionOrdinal = useCallback(
    () => draft.connections.length + 1,
    [draft.connections.length]
  );

  const clampWorldPoint = useCallback((point: WorldPoint): WorldPoint => {
    return {
      x: Math.max(0, Math.min(CANVAS_W, point.x)),
      y: Math.max(0, Math.min(CANVAS_H, point.y)),
    };
  }, []);

  const getWorldPoint = useCallback(
    (clientX: number, clientY: number): WorldPoint => {
      const rect = canvasRef.current?.getBoundingClientRect();
      if (!rect) {
        return { x: 0, y: 0 };
      }

      return clampWorldPoint({
        x: (clientX - rect.left - view.panX) / view.zoom,
        y: (clientY - rect.top - view.panY) / view.zoom,
      });
    },
    [clampWorldPoint, view.panX, view.panY, view.zoom]
  );

  const setToolWithMessage = useCallback((nextTool: Tool) => {
    setTool(nextTool);
    setLinkStart(null);
    setMessage(
      nextTool === "connection" ? "Выберите первую точку." : "Готово"
    );
  }, []);

  const addSpace = useCallback(
    (x: number, y: number) => {
      const ordinal = nextSpaceOrdinal();
      const spaceId = uniqueId(
        `space-${ordinal}`,
        draft.spaces.map((space) => space.spaceId)
      );

      const nextDraft: MapDraft = {
        ...draft,
        spaces: [
          ...draft.spaces,
          {
            spaceId,
            name: `Точка ${ordinal}`,
            x: Math.round(x),
            y: Math.round(y),
            type: "region",
          },
        ],
      };

      onDraftChange(nextDraft);
      setSelection({ type: "space", id: spaceId });
      setMessage("Точка добавлена.");
    },
    [draft, nextSpaceOrdinal, onDraftChange]
  );

  const moveSpace = useCallback(
    (spaceId: string, x: number, y: number) => {
      const clamped = clampWorldPoint({ x, y });
      onDraftChange({
        ...draft,
        spaces: draft.spaces.map((space) =>
          space.spaceId === spaceId
            ? {
                ...space,
                x: Math.round(clamped.x),
                y: Math.round(clamped.y),
              }
            : space
        ),
      });
    },
    [clampWorldPoint, draft, onDraftChange]
  );

  const renameSpace = useCallback(
    (spaceId: string, name: string) => {
      onDraftChange({
        ...draft,
        spaces: draft.spaces.map((space) =>
          space.spaceId === spaceId ? { ...space, name } : space
        ),
      });
    },
    [draft, onDraftChange]
  );

  const deleteSpace = useCallback(
    (spaceId: string) => {
      onDraftChange({
        ...draft,
        spaces: draft.spaces.filter((space) => space.spaceId !== spaceId),
        connections: draft.connections.filter(
          (connection) =>
            connection.fromSpaceId !== spaceId &&
            connection.toSpaceId !== spaceId
        ),
      });
      setSelection({ type: null, id: null });
      setMessage("Точка и связи удалены.");
    },
    [draft, onDraftChange]
  );

  const createConnection = useCallback(
    (fromSpaceId: string, toSpaceId: string) => {
      const ordinal = nextConnectionOrdinal();
      const connectionId = uniqueId(
        `conn-${ordinal}`,
        draft.connections.map((connection) => connection.connectionId)
      );

      onDraftChange({
        ...draft,
        connections: [
          ...draft.connections,
          {
            connectionId,
            fromSpaceId,
            toSpaceId,
            type: "land",
          },
        ],
      });
      setSelection({ type: "connection", id: connectionId });
      setMessage("Связь добавлена.");
    },
    [draft, nextConnectionOrdinal, onDraftChange]
  );

  const deleteConnection = useCallback(
    (connectionId: string) => {
      onDraftChange({
        ...draft,
        connections: draft.connections.filter(
          (connection) => connection.connectionId !== connectionId
        ),
      });
      setSelection({ type: null, id: null });
      setMessage("Связь удалена.");
    },
    [draft, onDraftChange]
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
    if (!raw) {
      setMessage("Нет сохранённого черновика.");
      return;
    }

    try {
      onDraftChange(JSON.parse(raw) as MapDraft);
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

      if (tool === "space") {
        addSpace(worldPoint.x, worldPoint.y);
        return;
      }

      if (tool === "pan") {
        event.preventDefault();
        dragRef.current = {
          type: "pan",
          startClientX: event.clientX,
          startClientY: event.clientY,
          originPanX: view.panX,
          originPanY: view.panY,
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

  const handleSpaceMouseDown = useCallback(
    (event: React.MouseEvent<SVGGElement>, spaceId: string) => {
      event.stopPropagation();

      if (tool === "connection") {
        if (!linkStart) {
          setLinkStart(spaceId);
          setSelection({ type: "space", id: spaceId });
          setMessage("Выберите вторую точку.");
          return;
        }

        if (linkStart === spaceId) {
          setMessage("Нельзя связать точку саму с собой.");
          return;
        }

        createConnection(linkStart, spaceId);
        setLinkStart(null);
        setTool("select");
        return;
      }

      if (tool === "select") {
        setSelection({ type: "space", id: spaceId });
        setLinkStart(null);

        const space = spacesById[spaceId];
        if (!space) {
          return;
        }

        const worldPoint = getWorldPoint(event.clientX, event.clientY);
        dragRef.current = {
          type: "spaceMove",
          id: spaceId,
          startWorldX: worldPoint.x,
          startWorldY: worldPoint.y,
          originX: space.x,
          originY: space.y,
        };
        return;
      }

      if (tool === "space") {
        setSelection({ type: "space", id: spaceId });
        setLinkStart(null);
      }
    },
    [createConnection, getWorldPoint, linkStart, spacesById, tool]
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
      if (!drag) {
        return;
      }

      if (drag.type === "spaceMove") {
        const worldPoint = getWorldPoint(event.clientX, event.clientY);
        moveSpace(
          drag.id,
          drag.originX + (worldPoint.x - drag.startWorldX),
          drag.originY + (worldPoint.y - drag.startWorldY)
        );
        return;
      }

      if (drag.type === "pan") {
        setView((prev) => ({
          ...prev,
          panX: drag.originPanX + (event.clientX - drag.startClientX),
          panY: drag.originPanY + (event.clientY - drag.startClientY),
        }));
      }
    },
    [getWorldPoint, moveSpace]
  );

  const stopDragging = useCallback(() => {
    dragRef.current = null;
  }, []);

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
                className={`editor-tool-pill ${
                  tool === currentTool ? "editor-tool-pill-active" : ""
                }`}
                onClick={() => setToolWithMessage(currentTool)}
              >
                {toolIcon(currentTool)} {toolLabel(currentTool)}
              </button>
            )
          )}

          <span className="editor-toolbar-sep">|</span>
          <button
            className="editor-btn editor-btn-validate"
            onClick={runValidation}
          >
            ✅
          </button>
          <button
            className="editor-btn editor-btn-preview"
            onClick={() => onPreview(draft)}
          >
            ▶
          </button>
          <button className="editor-btn editor-btn-save" onClick={saveDraft}>
            💾
          </button>
          <button className="editor-btn editor-btn-load" onClick={loadDraft}>
            📂
          </button>
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
                onClick={() => {
                  setSelection({
                    type: "connection",
                    id: connection.connectionId,
                  });
                  setLinkStart(null);
                }}
                onDelete={() => deleteConnection(connection.connectionId)}
              />
            ))}
          </TreeSection>
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
            <svg
              className="editor-svg-root"
              width={stageWidth}
              height={stageHeight}
              viewBox={`0 0 ${CANVAS_W} ${CANVAS_H}`}
            >
              <rect
                x={0}
                y={0}
                width={CANVAS_W}
                height={CANVAS_H}
                className="editor-map-bounds"
              />

              {draft.connections.map((connection) => {
                const from = getSpacePosition(connection.fromSpaceId);
                const to = getSpacePosition(connection.toSpaceId);
                if (!from || !to) {
                  return null;
                }

                const selected = isSelectedConnection(connection.connectionId);

                return (
                  <g key={connection.connectionId}>
                    <line
                      x1={from.x}
                      y1={from.y}
                      x2={to.x}
                      y2={to.y}
                      className="editor-connection-hit"
                      onMouseDown={(event) =>
                        handleConnectionMouseDown(event, connection.connectionId)
                      }
                      onContextMenu={(event) =>
                        handleConnectionContextMenu(
                          event,
                          connection.connectionId
                        )
                      }
                    />
                    <line
                      x1={from.x}
                      y1={from.y}
                      x2={to.x}
                      y2={to.y}
                      className={
                        selected
                          ? "editor-connection editor-connection-selected"
                          : "editor-connection"
                      }
                    />
                  </g>
                );
              })}

              {draft.spaces.map((space) => {
                const selected = isSelectedSpace(space.spaceId);
                const linkSource = linkStart === space.spaceId;

                return (
                  <g
                    key={space.spaceId}
                    className="editor-space-group"
                    onMouseDown={(event) =>
                      handleSpaceMouseDown(event, space.spaceId)
                    }
                    onContextMenu={(event) =>
                      handleSpaceContextMenu(event, space.spaceId)
                    }
                  >
                    <circle
                      cx={space.x}
                      cy={space.y}
                      r={SPACE_RADIUS + 8}
                      className="editor-space-hit"
                    />
                    <circle
                      cx={space.x}
                      cy={space.y}
                      r={SPACE_RADIUS}
                      className={`editor-space-node ${
                        selected ? "editor-space-node-selected" : ""
                      } ${linkSource ? "editor-space-node-link-from" : ""}`}
                    />
                    <text
                      x={space.x + 16}
                      y={space.y + 3}
                      className={`editor-space-text ${
                        selected ? "editor-space-text-selected" : ""
                      }`}
                    >
                      {space.name}
                    </text>
                  </g>
                );
              })}
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
            <SpaceInspector
              space={selectedObject as SpaceDraft}
              onRename={renameSpace}
              onDelete={deleteSpace}
            />
          ) : selectedObject && selection.type === "connection" ? (
            <ConnectionInspector
              connection={selectedObject as ConnectionDraft}
              spacesById={spacesById}
              onDelete={deleteConnection}
            />
          ) : (
            <div className="editor-inspector-empty">
              <Section title="Инспектор">
                <p className="editor-empty-text">
                  Выберите точку или связь.
                </p>
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
          onAdd={(x, y) => {
            addSpace(x, y);
            closeContextMenu();
          }}
          onDeleteSpace={() => {
            if (contextMenu.type === "space") {
              deleteSpace(contextMenu.id);
            }
            closeContextMenu();
          }}
          onDeleteConnection={() => {
            if (contextMenu.type === "connection") {
              deleteConnection(contextMenu.id);
            }
            closeContextMenu();
          }}
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
  const fromName =
    spacesById[connection.fromSpaceId]?.name ?? connection.fromSpaceId;
  const toName = spacesById[connection.toSpaceId]?.name ?? connection.toSpaceId;

  return (
    <div className="editor-inspector">
      <Section title="Связь">
        <Field label="ID">
          <span className="editor-mono">{connection.connectionId}</span>
        </Field>
        <Field label="От">
          <span className="editor-mono">{fromName}</span>
        </Field>
        <Field label="До">
          <span className="editor-mono">{toName}</span>
        </Field>
        <Field label="Тип">
          <span className="editor-mono">{connection.type}</span>
        </Field>
      </Section>
      <Section title="Действия">
        <button
          className="editor-btn editor-btn-delete"
          onClick={() => onDelete(connection.connectionId)}
        >
          🗑 Удалить связь
        </button>
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
}: {
  contextMenu: ContextMenuState;
  onClose: () => void;
  onAdd: (x: number, y: number) => void;
  onDeleteSpace: () => void;
  onDeleteConnection: () => void;
}) {
  return (
    <div className="editor-context-menu" onClick={onClose}>
      <div
        className="editor-context-menu-inner"
        style={{ left: contextMenu.x, top: contextMenu.y }}
        onClick={(event) => event.stopPropagation()}
      >
        {contextMenu.type === "canvas" && (
          <div
            className="editor-context-item"
            onClick={() => onAdd(contextMenu.worldX, contextMenu.worldY)}
          >
            📍 Добавить точку
          </div>
        )}

        {contextMenu.type === "space" && (
          <div className="editor-context-item" onClick={onDeleteSpace}>
            🗑 Удалить точку
          </div>
        )}

        {contextMenu.type === "connection" && (
          <div className="editor-context-item" onClick={onDeleteConnection}>
            🗑 Удалить связь
          </div>
        )}

        <div className="editor-context-separator" />
        <div className="editor-context-item" onClick={onClose}>
          ✕ Закрыть
        </div>
      </div>
    </div>
  );
}
