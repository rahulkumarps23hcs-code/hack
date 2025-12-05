from typing import Any, Dict, List

from config import safeRouteConfig
from logging_utils import logError
from utils import buildRouteGraph, dijkstraShortestPath, haversineDistanceKm


def _routeLengthKm(route: List[Dict[str, Any]]) -> float:
    if len(route) < 2:
        return 0.0
    totalLength = 0.0
    for current, nextPoint in zip(route, route[1:]):
        totalLength += haversineDistanceKm(
            float(current["lat"]),
            float(current["lng"]),
            float(nextPoint["lat"]),
            float(nextPoint["lng"]),
        )
    return totalLength


def _lengthToSafetyScore(lengthKm: float) -> float:
    if lengthKm <= 0.0:
        return 1.0
    maxLength = safeRouteConfig.maxRouteLengthKm
    normalized = max(0.0, min(1.0, maxLength / (lengthKm + maxLength)))
    return normalized


def optimizeSafeRoute(candidateRoutes: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
    try:
        if not candidateRoutes:
            return {
                "bestRouteIndex": None,
                "bestRoute": [],
                "routes": [],
                "graphUsed": False,
            }

        graph = buildRouteGraph(candidateRoutes)

        routeSummaries = []
        for index, route in enumerate(candidateRoutes):
            lengthKm = _routeLengthKm(route)
            safetyScore = _lengthToSafetyScore(lengthKm)

            if len(route) >= 2:
                startNode = (float(route[0]["lat"]), float(route[0]["lng"]))
                endNode = (float(route[-1]["lat"]), float(route[-1]["lng"]))
                graphDistance, graphPath = dijkstraShortestPath(graph, startNode, endNode)
            else:
                graphDistance, graphPath = float("inf"), []

            routeSummaries.append(
                {
                    "index": index,
                    "lengthKm": lengthKm,
                    "safetyScore": safetyScore,
                    "graphDistance": graphDistance,
                    "graphPath": graphPath,
                }
            )

        routeSummaries.sort(key=lambda item: (-item["safetyScore"], item["lengthKm"]))
        bestSummary = routeSummaries[0]

        bestIndex = bestSummary["index"]
        bestRoute = candidateRoutes[bestIndex]

        for summary in routeSummaries:
            summary["isRecommended"] = summary["index"] == bestIndex

        return {
            "bestRouteIndex": bestIndex,
            "bestRoute": bestRoute,
            "routes": routeSummaries,
            "graphUsed": True,
        }
    except Exception as error:
        logError("optimizeSafeRoute failed", error)
        return {
            "bestRouteIndex": None,
            "bestRoute": [],
            "routes": [],
            "graphUsed": False,
            "error": "safe route optimization error",
        }


def getMockRoutesInput() -> List[List[Dict[str, Any]]]:
    return [
        [
            {"lat": 12.9716, "lng": 77.5946},
            {"lat": 12.9721, "lng": 77.6100},
            {"lat": 12.9750, "lng": 77.6200},
        ],
        [
            {"lat": 12.9716, "lng": 77.5946},
            {"lat": 12.9600, "lng": 77.6050},
            {"lat": 12.9500, "lng": 77.6150},
        ],
    ]
