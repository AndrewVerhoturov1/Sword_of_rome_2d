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

// ---- Coordinate transform helpers (Map Plane Alignment 0.1) ----

/**
 * Преобразует map-local координаты в world-координаты
 * с учётом underlay offset, scale и rotation.
 *
 * Используется единообразно для spaces, connections, pieces и map bounds
 * в play/test renderer. Матчит transform из MapDraft.ts (mapLocalToWorld),
 * но работает только с MapRenderUnderlay (не тянет MapDraft в renderer).
 *
 * Если underlay === null — координаты возвращаются без изменений.
 */
export function mapLocalToWorld(
  localX: number,
  localY: number,
  underlay: MapRenderUnderlay | null
): { x: number; y: number } {
  if (!underlay) return { x: localX, y: localY };

  const cx = underlay.naturalWidth / 2;
  const cy = underlay.naturalHeight / 2;
  const s = underlay.scale || 1;
  const rad = (underlay.rotationDeg * Math.PI) / 180;
  const cos = Math.cos(rad);
  const sin = Math.sin(rad);

  // Center-based forward transform: translate(-cx,-cy), rotate, scale, translate(cx,cy), translate(ox,oy)
  const dx = localX - cx;
  const dy = localY - cy;
  const rx = dx * cos - dy * sin;
  const ry = dx * sin + dy * cos;

  return {
    x: rx * s + cx + underlay.offsetX,
    y: ry * s + cy + underlay.offsetY,
  };
}
