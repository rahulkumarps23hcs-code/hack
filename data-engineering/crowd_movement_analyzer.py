from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd

from logger import getLogger
from geospatial_utils import addRoundedCoordinates, filterInvalidCoordinates


logger = getLogger(__name__)


def resolveOutputPath(outputDir: str, filename: str) -> Path:
    baseDir = Path(__file__).resolve().parent
    outDir = (baseDir / outputDir) if not Path(outputDir).is_absolute() else Path(outputDir)
    outDir.mkdir(parents=True, exist_ok=True)
    return outDir / filename


def loadCrowdMovements(inputPath: str, **readKwargs: Any) -> pd.DataFrame:
    path = Path(inputPath)
    if path.suffix.lower() == ".parquet":
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
    cleaned = df.copy()
    if timestampCol in cleaned.columns:
        cleaned[timestampCol] = pd.to_datetime(cleaned[timestampCol], errors="coerce")
        cleaned = cleaned.dropna(subset=[timestampCol])
    else:
        raise KeyError(f"Timestamp column '{timestampCol}' not found in crowd data.")
    if entityIdCol in cleaned.columns:
        cleaned = cleaned.dropna(subset=[entityIdCol])
    else:
        logger.warning("Entity ID column '%s' not found in crowd data.", entityIdCol)
    if latCol in cleaned.columns and lngCol in cleaned.columns:
        cleaned = filterInvalidCoordinates(cleaned, latCol=latCol, lngCol=lngCol)
    else:
        logger.warning(
            "Latitude/longitude columns '%s'/'%s' not found; skipping spatial filtering.",
            latCol,
            lngCol,
        )
    sortCols = [c for c in [entityIdCol, timestampCol] if c in cleaned.columns]
    if sortCols:
        cleaned = cleaned.sort_values(sortCols).reset_index(drop=True)
    logger.info("Crowd movement data cleaned; final shape=%s", cleaned.shape)
    return cleaned


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


def saveCrowdFeatures(
    df: pd.DataFrame,
    outputDir: str = "clean-data",
    filename: str = "crowd-density-features.parquet",
) -> Path:
    outputPath = resolveOutputPath(outputDir, filename)
    if outputPath.suffix.lower() == ".parquet":
        df.to_parquet(outputPath, index=False)
    else:
        df.to_csv(outputPath, index=False)
    logger.info("Saved crowd density features to %s", outputPath)
    return outputPath


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "entityId": ["A", "A", "B", "B"],
            "timestamp": [
                "2024-01-01 10:00:00",
                "2024-01-01 10:03:00",
                "2024-01-01 10:01:00",
                "2024-01-01 10:10:00",
            ],
            "lat": [12.9716, 12.9717, 12.9720, 12.2958],
            "lng": [77.5946, 77.5947, 77.5948, 76.6394],
        }
    )
    logger.info("Raw crowd movement sample:\n%s", sample)
    cleanedSample = cleanCrowdMovements(sample)
    density = computeCrowdDensity(cleanedSample, timeFreq="5min")
    logger.info("Crowd density sample:\n%s", density)
    outputPath = saveCrowdFeatures(density)
    logger.info("Dummy crowd density features written to %s", outputPath)
