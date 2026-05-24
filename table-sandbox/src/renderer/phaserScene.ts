import Phaser from "phaser";
import type { GameState } from "../runtime/GameState";

/**
 * TableSandboxScene — Phaser-сцена для первого Action/Event Spine slice (0011).
 *
 * ПРАВИЛО: Эта сцена НЕ хранит authoritative runtime state.
 * Она только:
 *   - рендерит spaces, connections и pieces из GameState;
 *   - принимает pointer input;
 *   - передаёт structured input наружу через callback (не мутируя GameState).
 *
 * Source of truth — GameState вне Phaser.
 */

export interface SceneCallbacks {
  /** Вызывается при клике на space — передаёт spaceId наружу */
  onSpaceClick: (spaceId: string) => void;
}

/** Радиус попадания в space (пиксели) */
const SPACE_HIT_RADIUS = 35;

/** Радиус отрисовки space-круга */
const SPACE_RADIUS = 24;

export class TableSandboxScene extends Phaser.Scene {
  private callbacks: SceneCallbacks | null = null;
  private spaceCircles: Map<string, Phaser.GameObjects.Arc> = new Map();
  private spaceLabels: Map<string, Phaser.GameObjects.Text> = new Map();
  private connectionLines: Phaser.GameObjects.Graphics | null = null;
  private pieceMarkers: Map<string, Phaser.GameObjects.Container> = new Map();
  private selectionHighlight: Phaser.GameObjects.Arc | null = null;

  /** Кэшированное состояние для hit-теста */
  private cachedSpaces: { spaceId: string; x: number; y: number }[] = [];

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
      .text(width / 2, 16, "Table Sandbox 0.1 — Action/Event Spine", {
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

    // Обработка кликов — hit-test по spaces
    this.input.on("pointerdown", (pointer: Phaser.Input.Pointer) => {
      const spaceId = this.findSpaceAt(pointer.x, pointer.y);
      if (spaceId && this.callbacks) {
        this.callbacks.onSpaceClick(spaceId);
      }
    });
  }

  /**
   * Обновить отрисовку из GameState.
   * Вызывается из React при каждом изменении GameState или selection.
   */
  updateFromState(state: GameState, selectedPieceId: string | null): void {
    this.clearAllDynamic();
    this.cachedSpaces = [];

    this.drawConnections(state);
    this.drawSpaces(state);
    this.drawPieces(state, selectedPieceId);
  }

  // ---- Hit test ----

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

  private drawSpaces(state: GameState): void {
    for (const space of state.spaces) {
      this.cachedSpaces.push({
        spaceId: space.spaceId,
        x: space.x,
        y: space.y,
      });

      // Круг space
      const circle = this.add.circle(space.x, space.y, SPACE_RADIUS, 0x3a6b3a, 0.8);
      circle.setStrokeStyle(2, 0x8b7355, 0.9);
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
    for (const piece of state.pieces) {
      const space = state.spaces.find((s) => s.spaceId === piece.locationId);
      if (!space) continue;

      const isSelected = piece.pieceId === selectedPieceId;

      // Смещение относительно центра space — чтобы piece был виден рядом
      const offsetX = 18;
      const px = space.x + offsetX;
      const py = space.y;

      // Подсветка space, если piece на нём выбран
      if (isSelected) {
        const hl = this.add.circle(space.x, space.y, SPACE_RADIUS + 3, 0x000000, 0);
        hl.setStrokeStyle(3, 0xf0c040, 1);
        this.selectionHighlight = hl;
      }

      // Маркер piece — маленький квадрат
      const markerColor = isSelected ? 0xf0c040 : 0xe06030;
      const rect = this.add.rectangle(0, 0, 14, 14, markerColor, 1);
      rect.setStrokeStyle(1, 0xffffff, 0.6);

      // ID piece
      const idText = this.add
        .text(0, -12, piece.pieceId, {
          fontSize: "10px",
          color: isSelected ? "#f0c040" : "#e0e0e0",
          fontFamily: "monospace",
        })
        .setOrigin(0.5, 1);

      // Количество
      const countText = this.add
        .text(0, 2, String(piece.count), {
          fontSize: "9px",
          color: "#ffffff",
          fontFamily: "monospace",
        })
        .setOrigin(0.5);

      const container = this.add.container(px, py, [rect, idText, countText]);
      this.pieceMarkers.set(piece.pieceId, container);
    }
  }
}
