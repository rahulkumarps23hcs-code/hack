from __future__ import annotations

from typing import Any, Dict, List


def toAlertModelList(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    alerts = result.get("alerts", []) if isinstance(result, dict) else []
    normalized: List[Dict[str, Any]] = []
    for item in alerts:
        if not isinstance(item, dict):
            continue
        location = item.get("location") or {}
        normalized.append(
            {
                "id": item.get("id"),
                "type": item.get("type"),
                "severity": item.get("severity"),
                "timestamp": item.get("timestamp"),
                "location": {
                    "lat": location.get("lat"),
                    "lng": location.get("lng"),
                },
                "description": item.get("description"),
            }
        )
    return normalized


def toSafeSpotList(spots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in spots:
        if not isinstance(item, dict):
            continue
        location = item.get("location") or {}
        normalized.append(
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "type": item.get("type"),
                "address": item.get("address"),
                "location": {
                    "lat": location.get("lat"),
                    "lng": location.get("lng"),
                },
            }
        )
    return normalized


def toSosRiskResponse(result: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(result, dict):
        return {
            "riskScore": 0.0,
            "riskLevel": "low",
            "shouldPromptSos": False,
            "thresholds": {},
        }
    return {
        "riskScore": float(result.get("riskScore", 0.0)),
        "riskLevel": result.get("riskLevel", "low"),
        "shouldPromptSos": bool(result.get("shouldPromptSos", False)),
        "thresholds": dict(result.get("thresholds", {})),
    }


def toRouteResponse(result: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(result, dict):
        return {"bestRouteIndex": None, "bestRoute": [], "routes": []}
    return {
        "bestRouteIndex": result.get("bestRouteIndex"),
        "bestRoute": list(result.get("bestRoute", [])),
        "routes": list(result.get("routes", [])),
    }
