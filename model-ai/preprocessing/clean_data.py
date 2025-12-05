from __future__ import annotations

from typing import Any, Dict, List, Optional


def cleanNumeric(value: Any, default: float = 0.0, minValue: Optional[float] = None, maxValue: Optional[float] = None) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = float(default)

    if minValue is not None and number < minValue:
        number = minValue
    if maxValue is not None and number > maxValue:
        number = maxValue

    return number


def normalizeScore(value: Any, default: float = 0.0) -> float:
    number = cleanNumeric(value, default=default)
    if number < 0.0:
        return 0.0
    if number > 1.0:
        return 1.0
    return number


def hasValidLocation(record: Dict[str, Any]) -> bool:
    location = record.get("location") or {}
    try:
        latValue = float(location.get("lat"))
        lngValue = float(location.get("lng"))
    except (TypeError, ValueError):
        return False
    return not (latValue == 0.0 and lngValue == 0.0)


def cleanUnsafeZoneRecords(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []

    for record in records:
        if not hasValidLocation(record):
            continue

        recordCopy = dict(record)
        location = dict(recordCopy.get("location") or {})

        try:
            location["lat"] = float(location.get("lat"))
            location["lng"] = float(location.get("lng"))
        except (TypeError, ValueError):
            continue

        recordCopy["location"] = location
        recordCopy["crowdScore"] = normalizeScore(recordCopy.get("crowdScore", 0.5), default=0.5)
        recordCopy["incidentScore"] = normalizeScore(recordCopy.get("incidentScore", recordCopy.get("recentIncidents", 0.0)))

        cleaned.append(recordCopy)

    return cleaned


def cleanSosRiskContexts(contexts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []

    for context in contexts:
        contextCopy = dict(context)
        contextCopy["speedKmh"] = cleanNumeric(contextCopy.get("speedKmh", 0.0), default=0.0, minValue=0.0)
        contextCopy["unsafeProbability"] = normalizeScore(contextCopy.get("unsafeProbability", 0.0), default=0.0)
        contextCopy["timeInAppSeconds"] = cleanNumeric(contextCopy.get("timeInAppSeconds", 0.0), default=0.0, minValue=0.0)
        cleaned.append(contextCopy)

    return cleaned


def cleanNightModeContexts(contexts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []

    for context in contexts:
        contextCopy = dict(context)
        contextCopy["unsafeProbability"] = normalizeScore(contextCopy.get("unsafeProbability", 0.0), default=0.0)
        contextCopy["incidentScore"] = normalizeScore(contextCopy.get("incidentScore", 0.0), default=0.0)
        contextCopy["userPreference"] = normalizeScore(contextCopy.get("userPreference", 0.5), default=0.5)
        cleaned.append(contextCopy)

    return cleaned
