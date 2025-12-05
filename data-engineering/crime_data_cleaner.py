from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd

from logger import getLogger
from geospatial_utils import filterInvalidCoordinates


logger = getLogger(__name__)


def resolveOutputPath(outputDir: str, filename: str) -> Path:
    baseDir = Path(__file__).resolve().parent
    outDir = (baseDir / outputDir) if not Path(outputDir).is_absolute() else Path(outputDir)
    outDir.mkdir(parents=True, exist_ok=True)
    return outDir / filename


def loadCrimeData(inputPath: str, **readKwargs: Any) -> pd.DataFrame:
    path = Path(inputPath)
    if path.suffix.lower() == ".parquet":
        df = pd.read_parquet(path, **readKwargs)
    else:
        df = pd.read_csv(path, **readKwargs)
    logger.info("Loaded crime data from %s with shape %s", path, df.shape)
    return df


def cleanCrimeData(
    df: pd.DataFrame,
    idCol: Optional[str] = None,
    timestampCol: str = "timestamp",
    latCol: str = "lat",
    lngCol: str = "lng",
    typeCol: str = "type",
    severityCol: str = "severity",
    descriptionCol: str = "description",
    dropNaThreshold: float = 0.8,
) -> pd.DataFrame:
    cleaned = df.copy()
    if timestampCol in cleaned.columns:
        cleaned[timestampCol] = pd.to_datetime(cleaned[timestampCol], errors="coerce")
        cleaned = cleaned.dropna(subset=[timestampCol])
    else:
        logger.warning("Timestamp column '%s' not found in crime data.", timestampCol)
    if typeCol in cleaned.columns:
        typeSeries = cleaned[typeCol].astype(str).str.strip().str.lower()
        typeSeries = typeSeries.replace("nan", pd.NA)
        cleaned[typeCol] = typeSeries.fillna("unknown")
    if severityCol in cleaned.columns:
        severitySeries = cleaned[severityCol].astype(str).str.strip().str.lower()
        severitySeries = severitySeries.replace("nan", pd.NA)
        cleaned[severityCol] = severitySeries.fillna("medium")
    if descriptionCol in cleaned.columns:
        descSeries = cleaned[descriptionCol].fillna("").astype(str)
        descSeries = descSeries.str.replace(r"\s+", " ", regex=True).str.strip()
        descSeries = descSeries.replace("", pd.NA)
        cleaned[descriptionCol] = descSeries
        cleaned = cleaned.dropna(subset=[descriptionCol])
    if latCol in cleaned.columns and lngCol in cleaned.columns:
        cleaned = filterInvalidCoordinates(cleaned, latCol=latCol, lngCol=lngCol)
    else:
        logger.warning(
            "Latitude/longitude columns '%s'/'%s' not found; skipping spatial filtering.",
            latCol,
            lngCol,
        )
    if idCol and idCol in cleaned.columns:
        before = len(cleaned)
        cleaned = cleaned.drop_duplicates(subset=[idCol])
        logger.info("Dropped %d duplicate crime rows using idCol '%s'", before - len(cleaned), idCol)
    else:
        cleaned = cleaned.drop_duplicates()
    nonNullRatio = 1.0 - cleaned.isna().mean()
    colsToKeep = nonNullRatio[nonNullRatio >= dropNaThreshold].index.tolist()
    droppedCols = sorted(set(cleaned.columns) - set(colsToKeep))
    cleaned = cleaned[colsToKeep]
    if droppedCols:
        logger.info("Dropped columns with low non-null ratio: %s", droppedCols)
    logger.info("Crime data cleaned; final shape=%s", cleaned.shape)
    return cleaned


def saveCleanCrimeData(
    df: pd.DataFrame,
    outputDir: str = "clean-data",
    filename: str = "crime-data-clean.parquet",
) -> Path:
    outputPath = resolveOutputPath(outputDir, filename)
    if outputPath.suffix.lower() == ".parquet":
        df.to_parquet(outputPath, index=False)
    else:
        df.to_csv(outputPath, index=False)
    logger.info("Saved cleaned crime data to %s", outputPath)
    return outputPath


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "id": [1, 2, 2],
            "type": ["robbery", "ASSAULT", None],
            "severity": ["high", "medium", None],
            "timestamp": [
                "2024-01-01 10:00:00",
                "2024-01-01 10:10:00",
                "2024-01-01 10:10:00",
            ],
            "lat": [12.9716, 12.2958, 12.2958],
            "lng": [77.5946, 76.6394, 76.6394],
            "description": [
                "wallet stolen",
                "fight in street",
                None,
            ],
        }
    )
    logger.info("Raw crime sample:\n%s", sample)
    cleanedSample = cleanCrimeData(sample, idCol="id")
    logger.info("Cleaned crime sample:\n%s", cleanedSample)
    outputPath = saveCleanCrimeData(cleanedSample)
    logger.info("Dummy cleaned crime data written to %s", outputPath)
