import datetime as dt
from typing import Any, Dict, Optional

import numpy as np

from .sos_risk_model import (
    loadSosRiskModel,
    predictSosRisk,
)
from .unsafe_zone_model import (
    loadUnsafeZoneModel,
    predictUnsafeScore,
)


_unsafeModel = None
_sosModel = None


def _ensureModelsLoaded() -> None:
    global _unsafeModel, _sosModel
    if _unsafeModel is None:
        _unsafeModel = loadUnsafeZoneModel()
    if _sosModel is None:
        _sosModel = loadSosRiskModel()


def _parseTimestamp(timestamp: str) -> dt.datetime:
    try:
        value = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except Exception as exc:
        raise ValueError(f"Invalid ISO timestamp: {timestamp}") from exc
    return value


def getUnsafeZoneScore(lat: float, lng: float, timestamp: str, severity: str = "medium") -> Dict[str, Any]:
    _ensureModelsLoaded()
    dtValue = _parseTimestamp(timestamp)
    hour = dtValue.hour
    dayOfWeek = dtValue.weekday()
    sev = str(severity).lower()
    if sev == "high":
        severityCode = 2
    elif sev == "low":
        severityCode = 0
    else:
        severityCode = 1
    score = predictUnsafeScore(_unsafeModel, lat, lng, hour, dayOfWeek, severityCode)
    return {
        "unsafeScore": float(score),
        "lat": float(lat),
        "lng": float(lng),
        "timestamp": timestamp,
        "severity": severity,
    }


def getSosRiskScore(
    description: str,
    lat: float,
    lng: float,
    timestamp: str,
    severity: str = "high",
) -> Dict[str, Any]:
    _ensureModelsLoaded()
    dtValue = _parseTimestamp(timestamp)
    hour = dtValue.hour
    messageLength = len(description or "")
    isNight = int(hour >= 20 or hour <= 5)
    sev = str(severity).lower()
    if sev == "high":
        severityCode = 2
    elif sev == "low":
        severityCode = 0
    else:
        severityCode = 1
    risk = predictSosRisk(_sosModel, hour, messageLength, isNight, severityCode)
    return {
        "riskScore": float(risk),
        "lat": float(lat),
        "lng": float(lng),
        "timestamp": timestamp,
        "severity": severity,
        "messageLength": messageLength,
    }
