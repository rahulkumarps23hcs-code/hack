from typing import Any, Dict

from config import nightModeConfig
from logging_utils import logError
from utils import normalizeScore, parseTimestamp


def _computeNightModeScore(context: Dict[str, Any]) -> float:
    unsafeProbability = float(context.get("unsafeProbability", 0.0))
    incidentScore = float(context.get("incidentScore", 0.0))
    userPreference = float(context.get("userPreference", 0.5))

    timestampValue = context.get("timestamp")
    hourValue = context.get("hour")
    if hourValue is None and timestampValue is not None:
        timestamp = parseTimestamp(timestampValue)
        hourValue = timestamp.hour if timestamp else 0
    hourValue = int(hourValue or 0)

    if nightModeConfig.nightStartHour > nightModeConfig.nightEndHour:
        inNightWindow = (
            hourValue >= nightModeConfig.nightStartHour
            or hourValue < nightModeConfig.nightEndHour
        )
    else:
        inNightWindow = (
            nightModeConfig.nightStartHour
            <= hourValue
            < nightModeConfig.nightEndHour
        )

    score = 0.0
    score += nightModeConfig.unsafeZoneWeight * unsafeProbability
    score += nightModeConfig.incidentWeight * incidentScore
    score += nightModeConfig.preferenceWeight * userPreference
    if inNightWindow:
        score += nightModeConfig.lateNightBonus

    return normalizeScore(score, 0.0, 1.5)


def predictNightMode(context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        score = _computeNightModeScore(context)
        shouldEnable = score >= nightModeConfig.triggerThreshold

        return {
            "score": score,
            "shouldEnable": shouldEnable,
            "threshold": nightModeConfig.triggerThreshold,
        }
    except Exception as error:
        logError("predictNightMode failed", error)
        return {
            "score": 0.0,
            "shouldEnable": False,
            "threshold": nightModeConfig.triggerThreshold,
            "error": "night mode prediction error",
        }


def getMockNightModeInput() -> Dict[str, Any]:
    return {
        "timestamp": "2025-01-01T23:30:00",
        "unsafeProbability": 0.7,
        "incidentScore": 0.4,
        "userPreference": 0.8,
    }
