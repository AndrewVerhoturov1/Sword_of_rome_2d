/**
 * bootstrap.ts — загружает GameState из canonical fixture data.
 *
 * Использует статические JSON-импорты (Vite/ESNext).
 * Bootstrap source: table-sandbox/src/fixtures/tiny-module/
 *
 * Load path: project.json → module.json → map.json → scenario.basic.json
 * savegame.empty.json НЕ используется как bootstrap source;
 * это runtime/save artifact для будущего save/load слоя.
 */

import projectData from "../fixtures/tiny-module/project.json";
import moduleData from "../fixtures/tiny-module/modules/tiny-module/module.json";
import mapData from "../fixtures/tiny-module/modules/tiny-module/map.json";
import scenarioData from "../fixtures/tiny-module/modules/tiny-module/scenario.basic.json";
import type {
  GameState,
  SpaceState,
  ConnectionState,
  PieceState,
  TurnState,
  BootstrapMeta,
} from "./GameState";

/** Нормализовать space из fixture в runtime SpaceState */
function loadSpaces(): SpaceState[] {
  return mapData.spaces.map((s) => ({
    spaceId: s.spaceId,
    name: s.name,
    x: s.x,
    y: s.y,
    type: s.type,
  }));
}

/** Нормализовать connection из fixture в runtime ConnectionState */
function loadConnections(): ConnectionState[] {
  return mapData.connections.map((c) => ({
    connectionId: c.connectionId,
    fromSpaceId: c.fromSpaceId,
    toSpaceId: c.toSpaceId,
    type: c.type,
  }));
}

/** Нормализовать piece из scenario setup в runtime PieceState */
function loadPieces(): PieceState[] {
  return scenarioData.setup.pieces.map((p) => ({
    pieceId: p.pieceId,
    pieceDefId: p.pieceDefId,
    locationId: p.locationId,
    ownerId: p.ownerId,
    count: p.count,
  }));
}

/** Извлечь turn/phase из scenario setup */
function loadTurn(): TurnState {
  return {
    round: scenarioData.setup.turnState.round,
    phaseId: scenarioData.setup.turnState.phaseId,
    activeActorId: scenarioData.setup.turnState.activeActorId,
  };
}

/** Собрать bootstrap metadata */
function buildBootstrapMeta(): BootstrapMeta {
  return {
    source: "table-sandbox/src/fixtures/tiny-module/",
    projectId: projectData.projectId,
    moduleId: moduleData.moduleId,
    mapId: mapData.mapId,
    scenarioId: scenarioData.scenarioId,
    loadedFiles: [
      "project.json",
      "module.json",
      "map.json",
      "scenario.basic.json",
    ],
  };
}

/**
 * Главная bootstrap-функция.
 * Собирает GameState из canonical fixture data (project/module/map/scenario).
 * savegame.empty.json не используется — это runtime/save артефакт.
 */
export function bootstrapGameState(): GameState {
  const projectId = projectData.projectId;
  const moduleId = moduleData.moduleId;
  const mapId = mapData.mapId;
  const scenarioId = scenarioData.scenarioId;

  return {
    version: 0,
    lastUpdated: Date.now(),
    projectId,
    moduleId,
    mapId,
    scenarioId,
    spaces: loadSpaces(),
    connections: loadConnections(),
    pieces: loadPieces(),
    controlState: {},
    turn: loadTurn(),
    bootstrapMeta: buildBootstrapMeta(),
  };
}
