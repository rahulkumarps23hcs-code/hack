from __future__ import annotations

import random
from typing import Any, Dict, List

from inference.safe_route_optimizer import optimizeSafeRoute


def generateSyntheticRoutes(routeCount: int = 5, pointsPerRoute: int = 4) -> List[List[Dict[str, Any]]]:
    routes: List[List[Dict[str, Any]]] = []
    baseLat = 12.9
    baseLng = 77.5

    for routeIndex in range(routeCount):
        route: List[Dict[str, Any]] = []
        lat = baseLat
        lng = baseLng
        for _ in range(pointsPerRoute):
            lat += random.uniform(0.0, 0.01)
            lng += random.uniform(0.0, 0.01)
            route.append({"lat": lat, "lng": lng})
        routes.append(route)

    return routes


def main() -> None:
    routes = generateSyntheticRoutes()
    result = optimizeSafeRoute(routes)

    bestIndex = result.get("bestRouteIndex")
    routeSummaries = result.get("routes", [])

    print("Route safety evaluation:")
    print("------------------------")
    print(f"candidate routes: {len(routes)}")
    print(f"best route index (model): {bestIndex}")

    print("\nPer-route scores:")
    print("index  lengthKm  safetyScore")
    for item in routeSummaries:
        print(f"{item['index']:5d}  {item['lengthKm']:8.3f}  {item['safetyScore']:11.3f}")


if __name__ == "__main__":  # pragma: no cover
    main()
