from __future__ import annotations

from typing import Any, Dict, List

from preprocessing.clean_data import cleanNumeric, normalizeScore
from utils import parseTimestamp


def buildUnsafeZoneFeatures(record: Dict[str, Any]) -> List[float]:
    location = record.get("location") or {}

    hourValue = record.get("hour")
    if hourValue is None and record.get("timestamp") is not None:
        timestamp = parseTimestamp(record["timestamp"])
        hourValue = timestamp.hour if timestamp else 0

    normalizedHour = cleanNumeric(hourValue or 0, default=0.0, minValue=0.0) / 23.0
    recentIncidents = cleanNumeric(record.get("recentIncidents", 0.0), default=0.0, minValue=0.0)
    crowdScore = normalizeScore(record.get("crowdScore", 0.5), default=0.5)

    return [normalizedHour, recentIncidents, crowdScore, 1.0]


def buildSosRiskFeatures(context: Dict[str, Any]) -> List[float]:
    speedKmh = cleanNumeric(context.get("speedKmh", 0.0), default=0.0, minValue=0.0)
    suddenStop = 1.0 if context.get("suddenStop", False) else 0.0
    unsafeProbability = normalizeScore(context.get("unsafeProbability", 0.0), default=0.0)
    timeInAppSeconds = cleanNumeric(context.get("timeInAppSeconds", 0.0), default=0.0, minValue=0.0) / 600.0

    return [speedKmh / 80.0, suddenStop, unsafeProbability, timeInAppSeconds]


def buildNightModeFeatures(context: Dict[str, Any]) -> List[float]:
    unsafeProbability = normalizeScore(context.get("unsafeProbability", 0.0), default=0.0)
    incidentScore = normalizeScore(context.get("incidentScore", 0.0), default=0.0)
    userPreference = normalizeScore(context.get("userPreference", 0.5), default=0.5)

    hourValue = context.get("hour")
    if hourValue is None and context.get("timestamp") is not None:
        timestamp = parseTimestamp(context["timestamp"])
        hourValue = timestamp.hour if timestamp else 0

    normalizedHour = cleanNumeric(hourValue or 0, default=0.0, minValue=0.0) / 23.0

    return [unsafeProbability, incidentScore, userPreference, normalizedHour]
