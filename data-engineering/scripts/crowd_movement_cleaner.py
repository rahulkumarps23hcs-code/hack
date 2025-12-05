import sys
from pathlib import Path
from typing import Any, Optional

import pandas as pd

currentDir = Path(__file__).resolve().parent
utilsDir = currentDir.parent / "utils"
if str(utilsDir) not in sys.path:
    sys.path.insert(0, str(utilsDir))

from logger import getLogger
from geospatial_utils import addRoundedCoordinates, filterInvalidCoordinates


logger = getLogger(__name__)


def loadCrowdMovements(filePath: str, **readKwargs: Any) -> pd.DataFrame:
    path = Path(filePath)
    suffix = path.suffix.lower()
    if suffix == ".json":
        df = pd.read_json(path, **readKwargs)
    elif suffix == ".parquet":
        df = pd.read_parquet(path, **readKwargs)
    else:
        df = pd.read_csv(path, **readKwargs)
    logger.info("Loaded crowd movement data from %s with shape %s", path, df.shape)
    return df


def cleanCrowdMovements(
    df: pd.DataFrame,
    entityIdCol: str = "entityId",
    timestampCol: str = "timestamp",
    latCol: str = "lat",
    lngCol: str = "lng",
) -> pd.DataFrame:
    data = df.copy()
    if timestampCol in data.columns:
        data[timestampCol] = pd.to_datetime(data[timestampCol], errors="coerce")
        data = data.dropna(subset=[timestampCol])
    else:
        raise KeyError(f"Timestamp column '{timestampCol}' not found in crowd data.")
    if entityIdCol in data.columns:
        data = data.dropna(subset=[entityIdCol])
    else:
        logger.warning("Entity ID column '%s' not found in crowd data.", entityIdCol)
    if latCol in data.columns and lngCol in data.columns:
        data = filterInvalidCoordinates(data, latCol=latCol, lngCol=lngCol)
    else:
        logger.warning(
            "Latitude/longitude columns '%s'/'%s' not found; skipping spatial filtering.",
            latCol,
            lngCol,
        )
    sortCols = [c for c in [entityIdCol, timestampCol] if c in data.columns]
    if sortCols:
        data = data.sort_values(sortCols).reset_index(drop=True)
    logger.info("Crowd movement data cleaned; final shape=%s", data.shape)
    return data


def computeCrowdDensity(
    df: pd.DataFrame,
    entityIdCol: str = "entityId",
    timestampCol: str = "timestamp",
    areaIdCol: Optional[str] = None,
    latCol: str = "lat",
    lngCol: str = "lng",
    timeFreq: str = "5min",
    latRound: int = 4,
    lngRound: int = 4,
) -> pd.DataFrame:
    if timestampCol not in df.columns:
        raise KeyError(f"Timestamp column '{timestampCol}' not found in crowd data.")
    data = df.copy()
    data[timestampCol] = pd.to_datetime(data[timestampCol], errors="coerce")
    data = data.dropna(subset=[timestampCol])
    data["timeBucket"] = data[timestampCol].dt.floor(timeFreq)
    if areaIdCol and areaIdCol in data.columns:
        groupCols = ["timeBucket", areaIdCol]
    else:
        data = addRoundedCoordinates(
            data,
            latCol=latCol,
            lngCol=lngCol,
            latRound=latRound,
            lngRound=lngRound,
        )
        groupCols = ["timeBucket", "latRound", "lngRound"]
    grouped = data.groupby(groupCols)
    density = grouped.size().rename("crowdSize").to_frame()
    if entityIdCol in data.columns:
        density["uniqueEntities"] = grouped[entityIdCol].nunique()
    result = density.reset_index()
    logger.info("Computed crowd density features; output shape=%s", result.shape)
    return result


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "entityId": ["A", "A", "B", "B"],
            "timestamp": [
                "2025-01-01 10:00:00",
                "2025-01-01 10:03:00",
                "2025-01-01 10:01:00",
                "2025-01-01 10:10:00",
            ],
            "lat": [26.9124, 26.9125, 26.9126, 26.9150],
            "lng": [75.7873, 75.7874, 75.7875, 75.7890],
        }
    )
    logger.info("Raw crowd movement sample:\n%s", sample)
    cleanedSample = cleanCrowdMovements(sample)
    densitySample = computeCrowdDensity(cleanedSample, timeFreq="5min")
    logger.info("Crowd density sample:\n%s", densitySample)
