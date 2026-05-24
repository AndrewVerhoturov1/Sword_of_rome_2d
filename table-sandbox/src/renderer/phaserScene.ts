import Phaser from "phaser";
import type { GameState } from "../runtime/GameState";

/**
 * TableSandboxScene — Phaser-сцена для Action/Event Spine + Smart Drag Move (0016).
 *
 * ПРАВИЛО: Эта сцена НЕ хранит authoritative runtime state.
 * Она только:
 *   - рендерит spaces, connections и pieces из GameState;
 *   - принимает pointer input;
 *   - обрабатывает left-button drag для pieces;
 *   - передаёт structured input наружу через callback (не мутируя GameState).
 *
 * Source of truth — GameState вне Phaser.
 */

export interface SceneCallbacks {
  /** Вызывается при ЛКМ на space — выбор space/piece */
  onSpaceClick: (spaceId: string) => void;
  /** Вызывается при ПКМ на space — попытка перемещения */
  onSpaceRightClick: (spaceId: string) => void;
  /** Вызывается при отпускании drag — pieceId + targetSpaceId (null если invalid/no-target) */
  onPieceDragRelease: (pieceId: string, targetSpaceId: string | null) => void;
}

/** Радиус попадания в space (пиксели) */
const SPACE_HIT_RADIUS = 35;

/** Радиус отрисовки space-круга */
const SPACE_RADIUS = 24;

/** Порог начала drag (пиксели) — чтобы отличить клик от перетаскивания */
const DRAG_THRESHOLD = 5;

/** Snap-радиус: если курсор ближе этого расстояния к центру space — магнит */
const SNAP_RADIUS = 48;

/** Размер piece-прямоугольника */
const PIECE_SIZE = 28;

/** Смещение piece относительно центра space */
const PIECE_OFFSET_X = 18;

// ---- Drag state (transient, lives in Phaser only) ----

interface DragState {
  pieceId: string;
  sourceSpaceId: string;
  startX: number;
  startY: number;
  /** Координаты source space (для tail line) */
  sourceSpaceX: number;
  sourceSpaceY: number;
}

export class TableSandboxScene extends Phaser.Scene {
  private callbacks: SceneCallbacks | null = null;
  private spaceCircles: Map<string, Phaser.GameObjects.Arc> = new Map();
  private spaceLabels: Map<string, Phaser.GameObjects.Text> = new Map();
  private connectionLines: Phaser.GameObjects.Graphics | null = null;
  private pieceMarkers: Map<string, Phaser.GameObjects.Container> = new Map();
  private selectionHighlight: Phaser.GameObjects.Arc | null = null;

  /** Кэшированное состояние для hit-теста spaces */
  private cachedSpaces: { spaceId: string; x: number; y: number }[] = [];

  /** Кэшированные bounding-boxes pieces для drag hit-теста */
  private cachedPieceBoxes: { pieceId: string; x: number; y: number; w: number; h: number }[] = [];

  /** pieceId → spaceId mapping (для selected-piece-aware drag) */
  private pieceSpaceMap: Map<string, string> = new Map();

  /** Текущий selectedPieceId из React (для drag-target resolution) */
  private currentSelectedPieceId: string | null = null;

  // ---- Drag transient state ----
  private dragState: DragState | null = null;
  /** true когда реально начали drag (превысили порог) */
  private isDragging: boolean = false;
  /** Потенциальный drag начат, но ещё не превысили порог */
  private dragPending: boolean = false;
  /** Координаты pointerdown для проверки порога */
  private dragPendingX: number = 0;
  private dragPendingY: number = 0;

  // ---- Drag visual objects ----
  private dragGhost: Phaser.GameObjects.Container | null = null;
  private dragTailLine: Phaser.GameObjects.Graphics | null = null;
  private snapHighlightRing: Phaser.GameObjects.Arc | null = null;

  constructor() {
    super({ key: "TableSandboxScene" });
  }

  /** Установить callbacks после создания сцены */
  setCallbacks(cb: SceneCallbacks): void {
    this.callbacks = cb;
  }

  create(): void {
    const { width, height } = this.scale;

    // Фон — тёмно-зелёный, имитация стола
    this.cameras.main.setBackgroundColor("#2d5a1e");

    // Заголовок внутри canvas
    this.add
      .text(width / 2, 16, "Table Sandbox 0.1 — Smart Drag Move", {
        fontSize: "13px",
        color: "#cccccc",
        fontFamily: "monospace",
      })
      .setOrigin(0.5, 0);

    // Инициализируем graphics для соединений
    this.connectionLines = this.add.graphics();

    // Индикатор: Phaser не source of truth
    this.add
      .text(
        width / 2,
        height - 14,
        "Phaser = renderer/input only. State → outside.",
        {
          fontSize: "10px",
          color: "#6a6a4a",
          fontFamily: "monospace",
        }
      )
      .setOrigin(0.5, 1);

    // ---- Pointer handlers ----

    // pointerdown: определяем hit (piece → потенциальный drag / space → click)
    this.input.on("pointerdown", (pointer: Phaser.Input.Pointer) => {
      if (!this.callbacks) return;

      if (pointer.button === 0) {
        // Левая кнопка
        const pieceHit = this.findPieceAt(pointer.x, pointer.y);
        if (pieceHit) {
          // Попали в piece — начинаем потенциальный drag.
          // НЕ вызываем onSpaceClick — даём жесту разрешиться:
          //   без движения → click (циклический выбор)
          //   с движением → drag (перетаскивание)

          // Определяем source space
          const space = this.findSpaceAt(pointer.x, pointer.y);
          const sourceSpaceId = space ?? this.pieceSpaceMap.get(pieceHit) ?? "";

          // Selected-piece-aware drag target:
          // если selectedPieceId в том же sourceSpaceId — тянем выбранную фишку,
          // иначе тянем ту, по которой попали (верхнюю).
          let dragPieceId = pieceHit;
          if (this.currentSelectedPieceId) {
            const selPieceSpace = this.pieceSpaceMap.get(this.currentSelectedPieceId);
            if (selPieceSpace && selPieceSpace === sourceSpaceId) {
              dragPieceId = this.currentSelectedPieceId;
            }
          }

          this.dragPending = true;
          this.dragPendingX = pointer.x;
          this.dragPendingY = pointer.y;
          this.dragState = {
            pieceId: dragPieceId,
            sourceSpaceId: sourceSpaceId,
            startX: pointer.x,
            startY: pointer.y,
            sourceSpaceX: 0, // будет уточнено при начале drag
            sourceSpaceY: 0,
          };

          // Ждём pointerup (click) или pointermove (drag)
          return;
        }

        // Не piece — обычный клик по space
        const spaceId = this.findSpaceAt(pointer.x, pointer.y);
        if (spaceId) {
          this.callbacks.onSpaceClick(spaceId);
        }
      } else if (pointer.button === 2) {
        // Правая кнопка — перемещение (fallback)
        const spaceId = this.findSpaceAt(pointer.x, pointer.y);
        if (spaceId) {
          this.callbacks.onSpaceRightClick(spaceId);
        }
      }
    });

    // pointermove: drag tracking
    this.input.on("pointermove", (pointer: Phaser.Input.Pointer) => {
      if (!this.dragPending || !this.dragState) return;

      const dx = pointer.x - this.dragPendingX;
      const dy = pointer.y - this.dragPendingY;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (!this.isDragging && dist >= DRAG_THRESHOLD) {
        // Переход в реальный drag
        this.isDragging = true;
        this.beginDragVisuals();
      }

      if (this.isDragging) {
        this.updateDragVisuals(pointer.x, pointer.y);
      }
    });

    // pointerup: завершение drag или click
    this.input.on("pointerup", (pointer: Phaser.Input.Pointer) => {
      if (pointer.button !== 0) return;

      if (this.isDragging && this.dragState && this.callbacks) {
        // Drag завершён — ищем nearest space для snap
        const nearest = this.findNearestSpace(pointer.x, pointer.y);
        let targetSpaceId: string | null = null;
        if (nearest) {
          const d = Math.sqrt(
            (pointer.x - nearest.x) ** 2 + (pointer.y - nearest.y) ** 2
          );
          if (d <= SNAP_RADIUS) {
            targetSpaceId = nearest.spaceId;
          }
        }
        this.callbacks.onPieceDragRelease(this.dragState.pieceId, targetSpaceId);
        this.clearDrag();
        return;
      }

      if (this.dragPending && !this.isDragging) {
        // Был pointerdown на piece, но не двигали → это клик
        const spaceId = this.findSpaceAt(pointer.x, pointer.y);
        if (spaceId && this.callbacks) {
          this.callbacks.onSpaceClick(spaceId);
        }
        this.clearDrag();
      }
    });

    // Запретить стандартное контекстное меню на canvas
    this.input.mouse?.disableContextMenu();
  }

  /**
   * Обновить отрисовку из GameState.
   * Вызывается из React при каждом изменении GameState или selection.
   */
  updateFromState(
    state: GameState,
    selectedPieceId: string | null,
    selectedSpaceId: string | null
  ): void {
    // Сохраняем selectedPieceId для drag-target resolution
    this.currentSelectedPieceId = selectedPieceId;

    // Если drag активен — не сбрасываем его и не перерисовываем.
    // Перерисовка случится после commit (drag уже будет сброшен к тому моменту).
    if (this.isDragging && this.dragState) {
      const pieceStillExists = state.pieces.some(
        (p) => p.pieceId === this.dragState!.pieceId
      );
      if (!pieceStillExists) {
        // Dragged piece исчезла — сбрасываем drag
        this.clearDrag();
      }
      // В любом случае не перерисовываем во время активного drag
      return;
    }

    // Штатный путь: сброс и полная перерисовка
    this.clearDrag();
    this.clearAllDynamic();

    this.drawConnections(state);
    this.drawSpaces(state, selectedSpaceId, state.controlState);
    this.drawPieces(state, selectedPieceId);
  }

  // ---- Hit test: pieces ----

  private findPieceAt(x: number, y: number): string | null {
    for (const box of this.cachedPieceBoxes) {
      if (
        x >= box.x &&
        x <= box.x + box.w &&
        y >= box.y &&
        y <= box.y + box.h
      ) {
        return box.pieceId;
      }
    }
    return null;
  }

  // ---- Hit test: spaces ----

  private findSpaceAt(x: number, y: number): string | null {
    for (const s of this.cachedSpaces) {
      const dx = x - s.x;
      const dy = y - s.y;
      if (dx * dx + dy * dy <= SPACE_HIT_RADIUS * SPACE_HIT_RADIUS) {
        return s.spaceId;
      }
    }
    return null;
  }

  // ---- Nearest space (для snap) ----

  private findNearestSpace(
    x: number,
    y: number
  ): { spaceId: string; x: number; y: number } | null {
    let nearest: { spaceId: string; x: number; y: number } | null = null;
    let nearestDist = Infinity;
    for (const s of this.cachedSpaces) {
      const d = Math.sqrt((x - s.x) ** 2 + (y - s.y) ** 2);
      if (d < nearestDist) {
        nearestDist = d;
        nearest = s;
      }
    }
    return nearest;
  }

  // ---- Drag visuals ----

  private beginDragVisuals(): void {
    if (!this.dragState) return;

    // Уточняем sourceSpaceX/Y из cachedSpaces
    const srcSpace = this.cachedSpaces.find(
      (s) => s.spaceId === this.dragState!.sourceSpaceId
    );
    if (srcSpace) {
      this.dragState.sourceSpaceX = srcSpace.x;
      this.dragState.sourceSpaceY = srcSpace.y;
    }

    // Делаем оригинальный piece полупрозрачным
    const origMarker = this.pieceMarkers.get(this.dragState.pieceId);
    if (origMarker) {
      origMarker.setAlpha(0.3);
    }

    // Создаём ghost (копию piece, следующую за курсором)
    this.dragGhost = this.createDragGhost();
    // Ставим ghost на текущую позицию
    if (this.dragGhost) {
      this.dragGhost.setPosition(this.dragState.startX, this.dragState.startY);
    }

    // Создаём tail line (от source space к текущей позиции)
    this.dragTailLine = this.add.graphics();
    this.dragTailLine.setDepth(10);

    // Создаём snap highlight ring (пока скрыт)
    this.snapHighlightRing = this.add.circle(0, 0, SPACE_RADIUS + 10);
    this.snapHighlightRing.setStrokeStyle(3, 0xf0c040, 0.8);
    this.snapHighlightRing.setFillStyle(0xf0c040, 0.1);
    this.snapHighlightRing.setDepth(9);
    this.snapHighlightRing.setVisible(false);
  }

  private createDragGhost(): Phaser.GameObjects.Container | null {
    // Нам нужен цвет piece. Мы не храним ownerId в cachedPieceBoxes,
    // поэтому создаём простой ghost-прямоугольник нейтрального цвета.
    // Приоритет — square 28×28 с жёлтой обводкой и текстом pieceId.
    const rect = this.add.rectangle(0, 0, PIECE_SIZE, PIECE_SIZE, 0x888888, 0.9);
    rect.setStrokeStyle(3, 0xf0c040, 1);

    const idText = this.add
      .text(0, -18, this.dragState!.pieceId, {
        fontSize: "10px",
        color: "#f0c040",
        fontFamily: "monospace",
      })
      .setOrigin(0.5, 1);

    const countText = this.add
      .text(0, 2, "1", {
        fontSize: "10px",
        color: "#ffffff",
        fontFamily: "monospace",
      })
      .setOrigin(0.5);

    const container = this.add.container(0, 0, [rect, idText, countText]);
    container.setDepth(20);
    return container;
  }

  private updateDragVisuals(pointerX: number, pointerY: number): void {
    // Обновляем позицию ghost
    if (this.dragGhost) {
      this.dragGhost.setPosition(pointerX, pointerY);
    }

    // Обновляем tail line
    if (this.dragTailLine && this.dragState) {
      this.dragTailLine.clear();
      this.dragTailLine.lineStyle(2, 0xf0c040, 0.6);
      this.dragTailLine.lineBetween(
        this.dragState.sourceSpaceX,
        this.dragState.sourceSpaceY,
        pointerX,
        pointerY
      );
    }

    // Обновляем snap highlight
    if (this.snapHighlightRing && this.cachedSpaces.length > 0) {
      const nearest = this.findNearestSpace(pointerX, pointerY);
      if (nearest) {
        const d = Math.sqrt(
          (pointerX - nearest.x) ** 2 + (pointerY - nearest.y) ** 2
        );
        if (d <= SNAP_RADIUS) {
          this.snapHighlightRing.setPosition(nearest.x, nearest.y);
          this.snapHighlightRing.setVisible(true);
        } else {
          this.snapHighlightRing.setVisible(false);
        }
      } else {
        this.snapHighlightRing.setVisible(false);
      }
    }
  }

  private clearDrag(): void {
    // Восстановить alpha оригинального piece
    if (this.dragState) {
      const origMarker = this.pieceMarkers.get(this.dragState.pieceId);
      if (origMarker) {
        origMarker.setAlpha(1);
      }
    }

    // Уничтожить drag visuals
    if (this.dragGhost) {
      this.dragGhost.destroy();
      this.dragGhost = null;
    }
    if (this.dragTailLine) {
      this.dragTailLine.destroy();
      this.dragTailLine = null;
    }
    if (this.snapHighlightRing) {
      this.snapHighlightRing.destroy();
      this.snapHighlightRing = null;
    }

    this.dragState = null;
    this.isDragging = false;
    this.dragPending = false;
  }

  // ---- Очистка ----

  private clearAllDynamic(): void {
    for (const c of this.spaceCircles.values()) c.destroy();
    for (const l of this.spaceLabels.values()) l.destroy();
    for (const m of this.pieceMarkers.values()) m.destroy();
    if (this.selectionHighlight) {
      this.selectionHighlight.destroy();
      this.selectionHighlight = null;
    }
    this.spaceCircles.clear();
    this.spaceLabels.clear();
    this.pieceMarkers.clear();
    this.cachedPieceBoxes = [];
    this.pieceSpaceMap.clear();
    if (this.connectionLines) {
      this.connectionLines.clear();
    }
  }

  // ---- Рендер соединений ----

  private drawConnections(state: GameState): void {
    if (!this.connectionLines) return;
    const g = this.connectionLines;
    g.lineStyle(2, 0xc4a46c, 0.7);

    for (const conn of state.connections) {
      const from = state.spaces.find((s) => s.spaceId === conn.fromSpaceId);
      const to = state.spaces.find((s) => s.spaceId === conn.toSpaceId);
      if (from && to) {
        g.lineBetween(from.x, from.y, to.x, to.y);
      }
    }
  }

  // ---- Рендер spaces ----

  private drawSpaces(
    state: GameState,
    selectedSpaceId: string | null,
    controlState: Record<string, string | null>
  ): void {
    for (const space of state.spaces) {
      this.cachedSpaces.push({
        spaceId: space.spaceId,
        x: space.x,
        y: space.y,
      });

      const isSelected = space.spaceId === selectedSpaceId;
      const controlOwner = controlState[space.spaceId] ?? null;

      // Цвет круга зависит от контроля
      let fillColor = 0x3a6b3a; // default green
      let strokeColor = 0x8b7355;
      let strokeWidth = 2;

      if (controlOwner === "tiny-red") {
        fillColor = 0x6b2a2a; // dark red
        strokeColor = 0xcc4444;
      } else if (controlOwner === "tiny-blue") {
        fillColor = 0x2a3a6b; // dark blue
        strokeColor = 0x4488cc;
      }

      if (isSelected) {
        strokeColor = 0xf0c040;
        strokeWidth = 3;
      }

      // Круг space
      const circle = this.add.circle(space.x, space.y, SPACE_RADIUS, fillColor, 0.8);
      circle.setStrokeStyle(strokeWidth, strokeColor, 0.9);
      this.spaceCircles.set(space.spaceId, circle);

      // Подпись
      const label = this.add
        .text(space.x, space.y - SPACE_RADIUS - 8, space.name, {
          fontSize: "11px",
          color: "#c4a46c",
          fontFamily: "monospace",
        })
        .setOrigin(0.5, 1);
      this.spaceLabels.set(space.spaceId, label);
    }
  }

  // ---- Рендер pieces ----

  private drawPieces(state: GameState, selectedPieceId: string | null): void {
    // Сортируем: выбранная фишка — последней (сверху), остальные по порядку
    const sorted = [...state.pieces].sort((a, b) => {
      if (a.pieceId === selectedPieceId) return 1;
      if (b.pieceId === selectedPieceId) return -1;
      return 0;
    });

    for (const piece of sorted) {
      const space = state.spaces.find((s) => s.spaceId === piece.locationId);
      if (!space) continue;

      const isSelected = piece.pieceId === selectedPieceId;

      // Смещение относительно центра space — чтобы piece был виден рядом
      const px = space.x + PIECE_OFFSET_X;
      const py = space.y;

      // Кэшируем bounding box для drag hit-теста
      this.cachedPieceBoxes.push({
        pieceId: piece.pieceId,
        x: px - PIECE_SIZE / 2,
        y: py - PIECE_SIZE / 2,
        w: PIECE_SIZE,
        h: PIECE_SIZE,
      });

      // Кэшируем piece → space для selected-piece-aware drag
      this.pieceSpaceMap.set(piece.pieceId, space.spaceId);

      // Маркер piece — квадрат 28×28, цвет заливки по ownerId
      let fillColor: number;
      if (piece.ownerId === "tiny-red") {
        fillColor = 0xcc3333; // красный
      } else if (piece.ownerId === "tiny-blue") {
        fillColor = 0x3366cc; // синий
      } else {
        fillColor = 0xe06030; // оранжевый — неизвестный
      }

      const rect = this.add.rectangle(0, 0, PIECE_SIZE, PIECE_SIZE, fillColor, 1);

      // Выделение — только контур, без смены заливки
      if (isSelected) {
        rect.setStrokeStyle(3, 0xf0c040, 1); // толстый жёлтый контур
      } else {
        rect.setStrokeStyle(2, 0xffffff, 0.7); // тонкий белый контур
      }

      // ID piece
      const idText = this.add
        .text(0, -18, piece.pieceId, {
          fontSize: "10px",
          color: isSelected ? "#f0c040" : "#e0e0e0",
          fontFamily: "monospace",
        })
        .setOrigin(0.5, 1);

      // Количество
      const countText = this.add
        .text(0, 2, String(piece.count), {
          fontSize: "10px",
          color: "#ffffff",
          fontFamily: "monospace",
        })
        .setOrigin(0.5);

      const container = this.add.container(px, py, [rect, idText, countText]);
      this.pieceMarkers.set(piece.pieceId, container);
    }
  }
}
