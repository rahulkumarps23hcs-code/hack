from typing import Union

import numpy as np
import pandas as pd

from logger import getLogger


Number = Union[float, int]
EARTH_RADIUS_KM: float = 6371.0

logger = getLogger(__name__)


def isValidLatLng(lat: Number, lng: Number) -> bool:
    try:
        latFloat = float(lat)
        lngFloat = float(lng)
    except (TypeError, ValueError):
        return False
    return -90.0 <= latFloat <= 90.0 and -180.0 <= lngFloat <= 180.0


def filterInvalidCoordinates(
    df: pd.DataFrame,
    latCol: str = "lat",
    lngCol: str = "lng",
) -> pd.DataFrame:
    if latCol not in df.columns or lngCol not in df.columns:
        logger.warning(
            "Latitude/longitude columns '%s'/'%s' not found; returning original frame.",
            latCol,
            lngCol,
        )
        return df.copy()
    mask = df[latCol].between(-90, 90) & df[lngCol].between(-180, 180)
    cleaned = df.loc[mask].copy()
    logger.info("Filtered invalid coordinates: %d -> %d rows", len(df), len(cleaned))
    return cleaned


def addRoundedCoordinates(
    df: pd.DataFrame,
    latCol: str = "lat",
    lngCol: str = "lng",
    latRound: int = 4,
    lngRound: int = 4,
) -> pd.DataFrame:
    result = df.copy()
    if latCol not in result.columns or lngCol not in result.columns:
        raise KeyError(f"Columns '{latCol}'/'{lngCol}' not found in DataFrame.")
    result["latRound"] = result[latCol].astype(float).round(latRound)
    result["lngRound"] = result[lngCol].astype(float).round(lngRound)
    return result


def haversineDistance(
    lat1: Number,
    lng1: Number,
    lat2: Number,
    lng2: Number,
    unit: str = "km",
):
    lat1Rad = np.radians(np.asarray(lat1, dtype=float))
    lng1Rad = np.radians(np.asarray(lng1, dtype=float))
    lat2Rad = np.radians(np.asarray(lat2, dtype=float))
    lng2Rad = np.radians(np.asarray(lng2, dtype=float))
    dLat = lat2Rad - lat1Rad
    dLng = lng2Rad - lng1Rad
    a = np.sin(dLat / 2.0) ** 2 + np.cos(lat1Rad) * np.cos(lat2Rad) * np.sin(dLng / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    distanceKm = EARTH_RADIUS_KM * c
    if unit == "km":
        return distanceKm
    if unit in ("m", "meter", "meters"):
        return distanceKm * 1000.0
    raise ValueError(f"Unsupported unit: {unit}")


if __name__ == "__main__":
    dfExample = pd.DataFrame(
        {
            "lat": [12.9716, 95.0, -100.0],
            "lng": [77.5946, 180.0, 200.0],
        }
    )
    logger.info("Original coordinates:\n%s", dfExample)
    validDf = filterInvalidCoordinates(dfExample)
    logger.info("After filtering invalid coordinates:\n%s", validDf)
    distKm = haversineDistance(12.9716, 77.5946, 12.2958, 76.6394)
    logger.info("Example haversine distance: %.2f km", float(distKm))
