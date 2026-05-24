import { useEffect, useRef } from "react";
import Phaser from "phaser";
import { TableSandboxScene, SceneCallbacks } from "./phaserScene";

/**
 * PhaserStage — React-компонент, который монтирует Phaser game instance
 * внутрь div-контейнера.
 *
 * Phaser живёт ТОЛЬКО внутри этого компонента.
 * Никакой Phaser-объект не пролезает в остальной React shell.
 *
 * Props:
 *   onTableClick — callback при клике внутри Phaser canvas
 */
interface PhaserStageProps {
  onTableClick: (x: number, y: number) => void;
}

export function PhaserStage({ onTableClick }: PhaserStageProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const gameRef = useRef<Phaser.Game | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container || gameRef.current) return;

    // StrictMode guard: если Phaser уже вмонтировал canvas в контейнер —
    // значит это повторный mount после simulated unmount, не бутстрапим заново.
    if (container.querySelector("canvas")) return;

    const callbacks: SceneCallbacks = {
      onTableClick,
    };

    const config: Phaser.Types.Core.GameConfig = {
      type: Phaser.AUTO,
      width: 800,
      height: 500,
      parent: container,
      backgroundColor: "#1a1a2e",
      scene: TableSandboxScene,
      scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH,
      },
      // Никакого physics — чистый рендеринг
      physics: {
        default: "arcade",
        arcade: { gravity: { x: 0, y: 0 } },
      },
    };

    const game = new Phaser.Game(config);
    gameRef.current = game;

    // Передать callbacks в сцену после её создания
    game.events.on("ready", () => {
      const scene = game.scene.getScene(
        "TableSandboxScene"
      ) as TableSandboxScene;
      if (scene && scene.scene.isActive()) {
        scene.setCallbacks(callbacks);
      }
    });

    return () => {
      game.destroy(true);
      gameRef.current = null;
    };
  }, []);

  // Обновление callback при перерендере
  useEffect(() => {
    if (!gameRef.current) return;
    const scene = gameRef.current.scene.getScene(
      "TableSandboxScene"
    ) as TableSandboxScene;
    if (scene && scene.scene.isActive()) {
      scene.setCallbacks({ onTableClick });
    }
  }, [onTableClick]);

  return (
    <div
      ref={containerRef}
      style={{
        width: "100%",
        minHeight: "500px",
        border: "1px solid #4a4a6a",
        borderRadius: "4px",
        overflow: "hidden",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "#1a1a2e",
      }}
    />
  );
}
