import math
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt

from models.placeholder_models import LogisticSafetyModel, RandomForestSafetyModel
from config import safeRouteConfig, unsafeZoneConfig


unsafeZoneModelInstance: Optional[LogisticSafetyModel] = None
sosRiskModelInstance: Optional[RandomForestSafetyModel] = None


def getUnsafeZoneModel() -> LogisticSafetyModel:
    global unsafeZoneModelInstance
    if unsafeZoneModelInstance is None:
        unsafeZoneModelInstance = LogisticSafetyModel()
    return unsafeZoneModelInstance


def getSosRiskModel() -> RandomForestSafetyModel:
    global sosRiskModelInstance
    if sosRiskModelInstance is None:
        sosRiskModelInstance = RandomForestSafetyModel()
    return sosRiskModelInstance


def parseTimestamp(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value))
    except Exception:
        return None


def haversineDistanceKm(latOne: float, lngOne: float, latTwo: float, lngTwo: float) -> float:
    radiusKm = 6371.0
    phiOne, phiTwo = math.radians(latOne), math.radians(latTwo)
    deltaPhi = math.radians(latTwo - latOne)
    deltaLambda = math.radians(lngTwo - lngOne)

    valueA = math.sin(deltaPhi / 2.0) ** 2 + math.cos(phiOne) * math.cos(phiTwo) * math.sin(deltaLambda / 2.0) ** 2
    valueC = 2.0 * math.atan2(math.sqrt(valueA), math.sqrt(1.0 - valueA))
    return radiusKm * valueC


def normalizeScore(value: float, minValue: float = 0.0, maxValue: float = 1.0) -> float:
    if maxValue == minValue:
        return 0.0
    normalized = (value - minValue) / (maxValue - minValue)
    return max(0.0, min(1.0, normalized))


def generateDummyHeatmap(
    points: List[Tuple[float, float, float]],
    gridSize: Optional[int] = None,
    bounds: Optional[Tuple[float, float, float, float]] = None,
) -> Dict[str, Any]:
    if gridSize is None:
        gridSize = unsafeZoneConfig.heatmapGridSize

    if not points:
        emptyGrid = [[0.0 for _ in range(gridSize)] for _ in range(gridSize)]
        return {
            "grid": emptyGrid,
            "bounds": bounds or (0.0, 1.0, 0.0, 1.0),
            "gridSize": gridSize,
        }

    latValues = [point[0] for point in points]
    lngValues = [point[1] for point in points]

    if bounds is None:
        minLat, maxLat = min(latValues), max(latValues)
        minLng, maxLng = min(lngValues), max(lngValues)
    else:
        minLat, maxLat, minLng, maxLng = bounds

    if maxLat == minLat:
        maxLat += 1e-6
    if maxLng == minLng:
        maxLng += 1e-6

    grid = [[0.0 for _ in range(gridSize)] for _ in range(gridSize)]
    counts = [[0 for _ in range(gridSize)] for _ in range(gridSize)]

    for latValue, lngValue, score in points:
        rowIndex = int((latValue - minLat) / (maxLat - minLat) * (gridSize - 1))
        colIndex = int((lngValue - minLng) / (maxLng - minLng) * (gridSize - 1))
        rowIndex = max(0, min(gridSize - 1, rowIndex))
        colIndex = max(0, min(gridSize - 1, colIndex))
        grid[rowIndex][colIndex] += score
        counts[rowIndex][colIndex] += 1

    for rowIndex in range(gridSize):
        for colIndex in range(gridSize):
            if counts[rowIndex][colIndex] > 0:
                grid[rowIndex][colIndex] /= counts[rowIndex][colIndex]

    figure, axis = plt.subplots()
    axis.imshow(grid, origin="lower")
    plt.close(figure)

    return {
        "grid": grid,
        "bounds": (minLat, maxLat, minLng, maxLng),
        "gridSize": gridSize,
    }


Node = Tuple[float, float]
Graph = Dict[Node, List[Tuple[Node, float]]]


def addUndirectedEdge(graph: Graph, nodeA: Node, nodeB: Node, weight: float) -> None:
    graph.setdefault(nodeA, []).append((nodeB, weight))
    graph.setdefault(nodeB, []).append((nodeA, weight))


def dijkstraShortestPath(graph: Graph, source: Node, target: Node) -> Tuple[float, List[Node]]:
    import heapq

    queue: List[Tuple[float, Node, List[Node]]] = [(0.0, source, [])]
    visited: set[Node] = set()

    while queue:
        distance, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]

        if node == target:
            return distance, path

        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(queue, (distance + weight, neighbor, path))

    return float("inf"), []


def buildRouteGraph(candidateRoutes: List[List[Dict[str, Any]]]) -> Graph:
    graph: Graph = {}

    for route in candidateRoutes:
        if len(route) < 2:
            continue
        for current, nextPoint in zip(route, route[1:]):
            nodeA: Node = (float(current["lat"]), float(current["lng"]))
            nodeB: Node = (float(nextPoint["lat"]), float(nextPoint["lng"]))
            segmentLength = haversineDistanceKm(nodeA[0], nodeA[1], nodeB[0], nodeB[1])
            riskWeight = segmentLength
            addUndirectedEdge(graph, nodeA, nodeB, riskWeight)

    return graph
