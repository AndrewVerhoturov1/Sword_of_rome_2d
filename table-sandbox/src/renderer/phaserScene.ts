import Phaser from "phaser";

/**
 * TableSandboxScene — минимальная Phaser-сцена для Technical Bootstrap.
 *
 * ПРАВИЛО: Эта сцена НЕ хранит authoritative runtime state.
 * Она только:
 *   - рендерит визуальную table area;
 *   - принимает pointer input;
 *   - передаёт input наружу через callback (не мутируя GameState).
 *
 * Source of truth — GameState вне Phaser.
 */

export interface SceneCallbacks {
  /** Вызывается при клике на table area — передаёт координаты наружу */
  onTableClick: (x: number, y: number) => void;
}

export class TableSandboxScene extends Phaser.Scene {
  private callbacks: SceneCallbacks | null = null;

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
      .text(width / 2, 16, "Table Sandbox 0.1 — Phaser Renderer", {
        fontSize: "14px",
        color: "#cccccc",
        fontFamily: "monospace",
      })
      .setOrigin(0.5, 0);

    // Разметка table area
    const tableLeft = 60;
    const tableRight = width - 60;
    const tableTop = 50;
    const tableBottom = height - 50;

    const tableGraphics = this.add.graphics();
    tableGraphics.lineStyle(1, 0x8b7355, 0.6);
    tableGraphics.strokeRect(
      tableLeft,
      tableTop,
      tableRight - tableLeft,
      tableBottom - tableTop
    );

    // Подпись внутри table area
    this.add
      .text(width / 2, height / 2, "Table Area\n(Phaser renderer only)", {
        fontSize: "18px",
        color: "#8b7355",
        fontFamily: "monospace",
        align: "center",
      })
      .setOrigin(0.5);

    // Сетка
    const gridGraphics = this.add.graphics();
    gridGraphics.lineStyle(1, 0x4a7a3a, 0.15);
    const step = 40;
    for (let x = tableLeft; x <= tableRight; x += step) {
      gridGraphics.lineBetween(x, tableTop, x, tableBottom);
    }
    for (let y = tableTop; y <= tableBottom; y += step) {
      gridGraphics.lineBetween(tableLeft, y, tableRight, y);
    }

    // Индикатор: Phaser не source of truth
    this.add
      .text(width / 2, height - 14, "Phaser = renderer/input only. State → outside.", {
        fontSize: "10px",
        color: "#6a6a4a",
        fontFamily: "monospace",
      })
      .setOrigin(0.5, 1);

    // Обработка кликов — передача наружу
    this.input.on("pointerdown", (pointer: Phaser.Input.Pointer) => {
      if (this.callbacks) {
        this.callbacks.onTableClick(pointer.x, pointer.y);
      }
    });
  }
}
