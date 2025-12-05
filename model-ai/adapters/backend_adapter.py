from __future__ import annotations

from typing import Any, Dict, List

from inference.night_mode_predictor import predictNightMode
from inference.safe_route_optimizer import optimizeSafeRoute
from inference.sos_risk_model import predictSosRisk
from inference.unsafe_zone_detector import predictUnsafeZones


def format_safe_response(success: bool, message: str, data: Any) -> Dict[str, Any]:
    return {
        "success": bool(success),
        "message": str(message),
        "data": data,
    }


def runUnsafeZoneInference(locations: List[Dict[str, Any]]) -> Dict[str, Any]:
    try:
        data = predictUnsafeZones(locations)
        return format_safe_response(True, "unsafe zones computed", data)
    except Exception as error:
        return format_safe_response(False, "unsafe zone prediction failed", {"error": str(error)})


def runSafeRouteInference(routes: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
    try:
        data = optimizeSafeRoute(routes)
        return format_safe_response(True, "safe route computed", data)
    except Exception as error:
        return format_safe_response(False, "safe route optimization failed", {"error": str(error)})


def runNightModeInference(context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        data = predictNightMode(context)
        return format_safe_response(True, "night mode decision computed", data)
    except Exception as error:
        return format_safe_response(False, "night mode prediction failed", {"error": str(error)})


def runSosRiskInference(context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        data = predictSosRisk(context)
        return format_safe_response(True, "sos risk computed", data)
    except Exception as error:
        return format_safe_response(False, "sos risk prediction failed", {"error": str(error)})
