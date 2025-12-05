from typing import Any, Dict, List, Tuple

from config import unsafeZoneConfig
from logging_utils import logError
from utils import generateDummyHeatmap, getUnsafeZoneModel, parseTimestamp


def _extractFeatures(locationItem: Dict[str, Any]) -> List[float]:
    features = locationItem.get("features")
    if isinstance(features, (list, tuple)) and features:
        return [float(value) for value in features]

    hourValue = locationItem.get("hour")
    if hourValue is None and locationItem.get("timestamp") is not None:
        timestamp = parseTimestamp(locationItem["timestamp"])
        hourValue = timestamp.hour if timestamp else 0

    normalizedHour = float(hourValue or 0) / 23.0
    recentIncidents = float(locationItem.get("recentIncidents", 0))
    crowdScore = float(locationItem.get("crowdScore", 0.5))

    return [normalizedHour, recentIncidents, crowdScore, 1.0]


def predictUnsafeZones(locations: List[Dict[str, Any]]) -> Dict[str, Any]:
    try:
        model = getUnsafeZoneModel()
        alertList: List[Dict[str, Any]] = []
        scoreList: List[Dict[str, Any]] = []
        heatmapPoints: List[Tuple[float, float, float]] = []

        for index, locationItem in enumerate(locations):
            locationObject = locationItem.get("location", {})
            latValue = float(locationObject.get("lat", 0.0))
            lngValue = float(locationObject.get("lng", 0.0))

            featureVector = _extractFeatures(locationItem)
            unsafeProbability = float(model.predictProba(featureVector))
            isUnsafe = unsafeProbability >= unsafeZoneConfig.probabilityThreshold

            alertId = locationItem.get("id") or f"unsafe-{index}"
            timestampValue = locationItem.get("timestamp")
            descriptionValue = locationItem.get("description") or "Unsafe zone detected by model"

            alert = {
                "id": alertId,
                "type": unsafeZoneConfig.defaultAlertType,
                "severity": unsafeZoneConfig.defaultSeverity if isUnsafe else "medium",
                "timestamp": timestampValue,
                "location": {"lat": latValue, "lng": lngValue},
                "description": descriptionValue,
            }
            alertList.append(alert)

            scoreList.append(
                {
                    "id": alertId,
                    "unsafeProbability": unsafeProbability,
                    "isUnsafe": isUnsafe,
                }
            )

            heatmapPoints.append((latValue, lngValue, unsafeProbability))

        heatmap = generateDummyHeatmap(
            heatmapPoints,
            gridSize=unsafeZoneConfig.heatmapGridSize,
            bounds=unsafeZoneConfig.heatmapBounds,
        )

        return {
            "alerts": alertList,
            "scores": scoreList,
            "heatmap": heatmap,
        }
    except Exception as error:
        logError("predictUnsafeZones failed", error)
        return {
            "alerts": [],
            "scores": [],
            "heatmap": {"grid": [], "bounds": (0.0, 1.0, 0.0, 1.0), "gridSize": 0},
            "error": "unsafe zone prediction error",
        }


def getMockUnsafeZoneInput() -> List[Dict[str, Any]]:
    return [
        {
            "id": "loc-1",
            "timestamp": "2025-01-01T23:15:00",
            "location": {"lat": 12.9716, "lng": 77.5946},
            "recentIncidents": 5,
            "crowdScore": 0.3,
        },
        {
            "id": "loc-2",
            "timestamp": "2025-01-01T20:15:00",
            "location": {"lat": 12.9352, "lng": 77.6245},
            "recentIncidents": 1,
            "crowdScore": 0.7,
        },
    ]
