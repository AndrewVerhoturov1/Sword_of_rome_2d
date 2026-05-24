import { useEffect, useRef } from "react";
import Phaser from "phaser";
import { TableSandboxScene, SceneCallbacks } from "./phaserScene";
import type { GameState } from "../runtime/GameState";

/**
 * PhaserStage — React-компонент, который монтирует Phaser game instance
 * внутрь div-контейнера.
 *
 * Phaser живёт ТОЛЬКО внутри этого компонента.
 * Никакой Phaser-объект не пролезает в остальной React shell.
 *
 * Принимает GameState для рендера и selection для подсветки.
 * Передаёт клики по spaces и drag release наружу через callbacks.
 *
 * Handoff 0016: добавлен onPieceDragRelease для smart drag move.
 */
interface PhaserStageProps {
  gameState: GameState;
  selectedPieceId: string | null;
  selectedSpaceId: string | null;
  onSpaceClick: (spaceId: string) => void;
  onSpaceRightClick: (spaceId: string) => void;
  onPieceDragRelease: (pieceId: string, targetSpaceId: string | null) => void;
}

export function PhaserStage({
  gameState,
  selectedPieceId,
  selectedSpaceId,
  onSpaceClick,
  onSpaceRightClick,
  onPieceDragRelease,
}: PhaserStageProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const gameRef = useRef<Phaser.Game | null>(null);
  const sceneRef = useRef<TableSandboxScene | null>(null);

  // ---- Mount / unmount ----

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    // StrictMode-safe: всегда удаляем остатки предыдущего game instance.
    if (gameRef.current) {
      gameRef.current.destroy(true);
      gameRef.current = null;
    }

    // Синхронно удаляем оставшийся canvas (StrictMode double-mount fix).
    const leftoverCanvas = container.querySelector("canvas");
    if (leftoverCanvas) leftoverCanvas.remove();

    const callbacks: SceneCallbacks = {
      onSpaceClick,
      onSpaceRightClick,
      onPieceDragRelease,
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
      physics: {
        default: "arcade",
        arcade: { gravity: { x: 0, y: 0 } },
      },
    };

    const game = new Phaser.Game(config);
    gameRef.current = game;

    // Передать callbacks и дождаться создания сцены
    game.events.on("ready", () => {
      const scene = game.scene.getScene(
        "TableSandboxScene"
      ) as TableSandboxScene;
      if (scene && scene.scene.isActive()) {
        scene.setCallbacks(callbacks);
        sceneRef.current = scene;
        // Первый рендер из state
        scene.updateFromState(gameState, selectedPieceId, selectedSpaceId);
      }
    });

    return () => {
      sceneRef.current = null;
      game.destroy(true);
      gameRef.current = null;
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // ---- Обновление callbacks при перерендере ----

  useEffect(() => {
    if (!gameRef.current) return;
    const scene = gameRef.current.scene.getScene(
      "TableSandboxScene"
    ) as TableSandboxScene;
    if (scene && scene.scene.isActive()) {
      scene.setCallbacks({ onSpaceClick, onSpaceRightClick, onPieceDragRelease });
    }
  }, [onSpaceClick, onSpaceRightClick, onPieceDragRelease]);

  // ---- Обновление рендера при изменении GameState или selection ----

  useEffect(() => {
    if (!gameRef.current) return;
    const scene = gameRef.current.scene.getScene(
      "TableSandboxScene"
    ) as TableSandboxScene;
    if (scene && scene.scene.isActive()) {
      scene.updateFromState(gameState, selectedPieceId, selectedSpaceId);
    }
  }, [gameState, selectedPieceId, selectedSpaceId]);

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
