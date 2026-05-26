/**
 * MapRenderModel — display-only visual contract для Editor → Play continuity.
 *
 * Handoff 0029: первый MapRenderModel Contract Wire-Up.
 *
 * Не является runtime source of truth.
 * Не зависит от editor (MapDraft) и от runtime (GameState).
 *
 * Живёт отдельно: App.tsx — bridge point, который создаёт MapRenderModel
 * из MapDraft при preview и передаёт его в PhaserStage → TableSandboxScene.
 */

export interface MapRenderModel {
  /** Источник: editor-preview (пока единственный) */
  source: "editor-preview";
  /** Идентификатор карты */
  mapId: string;
  /** Человекочитаемое имя карты */
  name: string;
  /** Система координат (пока только pixel) */
  coordinateSystem: MapRenderCoordinateSystem;
  /** Underlay / terrain image (null — без подложки) */
  underlay: MapRenderUnderlay | null;
}

export interface MapRenderCoordinateSystem {
  type: "pixel";
  /** Ширина карты в пикселях (native coordinate space) */
  width: number;
  /** Высота карты в пикселях (native coordinate space) */
  height: number;
}

export interface MapRenderUnderlay {
  /** image data URL или null (placeholder) */
  src: string | null;
  /** Смещение X в world-координатах */
  offsetX: number;
  /** Смещение Y в world-координатах */
  offsetY: number;
  /** Uniform scale (1 = original size) */
  scale: number;
  /** Rotation in degrees (не radians — явно) */
  rotationDeg: number;
  /** Opacity 0–100 (не 0–1 Phaser alpha) */
  opacityPercent: number;
  /** Показывать или скрывать подложку */
  visible: boolean;
  /** Natural image width (пиксели) */
  naturalWidth: number;
  /** Natural image height (пиксели) */
  naturalHeight: number;
}
