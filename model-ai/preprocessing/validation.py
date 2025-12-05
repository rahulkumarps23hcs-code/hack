from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from preprocessing.clean_data import cleanNumeric


@dataclass
class LocationSchema:
    lat: float
    lng: float

    @classmethod
    def fromDict(cls, data: Dict[str, Any]) -> Tuple["LocationSchema" | None, List[str]]:
        errors: List[str] = []
        if not isinstance(data, dict):
            errors.append("location must be a dict")
            return None, errors

        try:
            latValue = float(data.get("lat"))
            lngValue = float(data.get("lng"))
        except (TypeError, ValueError):
            errors.append("lat and lng must be numeric")
            return None, errors

        return cls(lat=latValue, lng=lngValue), errors


@dataclass
class RouteSchema:
    points: List[LocationSchema]

    @classmethod
    def fromList(cls, data: List[Dict[str, Any]]) -> Tuple["RouteSchema" | None, List[str]]:
        errors: List[str] = []
        if not isinstance(data, list):
            errors.append("route must be a list of locations")
            return None, errors

        locations: List[LocationSchema] = []
        for index, item in enumerate(data):
            location, locationErrors = LocationSchema.fromDict(item if isinstance(item, dict) else {})
            if locationErrors:
                errors.append(f"invalid location at index {index}: {', '.join(locationErrors)}")
                continue
            if location is not None:
                locations.append(location)

        if not locations:
            errors.append("route must contain at least one valid location")
            return None, errors

        return cls(points=locations), errors


@dataclass
class ContextSchema:
    raw: Dict[str, Any]

    @classmethod
    def fromDict(cls, data: Dict[str, Any], requiredKeys: List[str] | None = None) -> Tuple["ContextSchema" | None, List[str]]:
        errors: List[str] = []
        if not isinstance(data, dict):
            errors.append("context must be a dict")
            return None, errors

        if requiredKeys:
            for key in requiredKeys:
                if key not in data:
                    errors.append(f"missing key: {key}")

        return cls(raw=dict(data)), errors


def validateLocation(location: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
    schema, errors = LocationSchema.fromDict(location)
    if schema is None:
        return False, {}, errors
    cleaned = {"lat": schema.lat, "lng": schema.lng}
    return True, cleaned, errors


def validateRoute(route: List[Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]], List[str]]:
    schema, errors = RouteSchema.fromList(route)
    if schema is None:
        return False, [], errors
    cleaned = [{"lat": item.lat, "lng": item.lng} for item in schema.points]
    return True, cleaned, errors


def validateContext(context: Dict[str, Any], requiredKeys: List[str] | None = None) -> Tuple[bool, Dict[str, Any], List[str]]:
    schema, errors = ContextSchema.fromDict(context, requiredKeys=requiredKeys)
    if schema is None:
        return False, {}, errors

    cleaned = dict(schema.raw)
    numericKeys = ["unsafeProbability", "incidentScore", "userPreference", "speedKmh", "timeInAppSeconds"]
    for key in numericKeys:
        if key in cleaned:
            cleaned[key] = cleanNumeric(cleaned[key])

    return True, cleaned, errors
