from pathlib import Path
from typing import Any, Optional

import pandas as pd

from logger import getLogger
from geospatial_utils import filterInvalidCoordinates


logger = getLogger(__name__)


def resolveOutputPath(outputDir: str, filename: str) -> Path:
    baseDir = Path(__file__).resolve().parent
    outDir = (baseDir / outputDir) if not Path(outputDir).is_absolute() else Path(outputDir)
    outDir.mkdir(parents=True, exist_ok=True)
    return outDir / filename


def loadSosReports(inputPath: str, **readKwargs: Any) -> pd.DataFrame:
    path = Path(inputPath)
    if path.suffix.lower() == ".parquet":
        df = pd.read_parquet(path, **readKwargs)
    else:
        df = pd.read_csv(path, **readKwargs)
    logger.info("Loaded SOS reports from %s with shape %s", path, df.shape)
    return df


def cleanTextColumn(series: pd.Series) -> pd.Series:
    cleaned = series.fillna("").astype(str)
    cleaned = cleaned.str.replace(r"\s+", " ", regex=True).str.strip().str.lower()
    cleaned = cleaned.replace("", pd.NA)
    return cleaned


def cleanSosReports(
    df: pd.DataFrame,
    idCol: Optional[str] = "id",
    messageCol: str = "message",
    descriptionCol: str = "description",
    timestampCol: str = "timestamp",
    latCol: str = "lat",
    lngCol: str = "lng",
) -> pd.DataFrame:
    cleaned = df.copy()
    if messageCol in cleaned.columns and descriptionCol not in cleaned.columns:
        cleaned[descriptionCol] = cleaned[messageCol]
    if timestampCol in cleaned.columns:
        cleaned[timestampCol] = pd.to_datetime(cleaned[timestampCol], errors="coerce")
        cleaned = cleaned.dropna(subset=[timestampCol])
    else:
        logger.warning("Timestamp column '%s' not found in SOS reports.", timestampCol)
    if descriptionCol in cleaned.columns:
        cleaned[descriptionCol] = cleanTextColumn(cleaned[descriptionCol])
        cleaned = cleaned.dropna(subset=[descriptionCol])
    else:
        logger.warning("Description column '%s' not found in SOS reports.", descriptionCol)
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
        logger.info("Dropped %d duplicate SOS reports using idCol '%s'", before - len(cleaned), idCol)
    else:
        cleaned = cleaned.drop_duplicates()
    logger.info("SOS reports cleaned; final shape=%s", cleaned.shape)
    return cleaned


def saveCleanSosReports(
    df: pd.DataFrame,
    outputDir: str = "clean-data",
    filename: str = "sos-reports-clean.parquet",
) -> Path:
    outputPath = resolveOutputPath(outputDir, filename)
    if outputPath.suffix.lower() == ".parquet":
        df.to_parquet(outputPath, index=False)
    else:
        df.to_csv(outputPath, index=False)
    logger.info("Saved cleaned SOS reports to %s", outputPath)
    return outputPath


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "id": [101, 102, 102],
            "timestamp": [
                "2024-01-01 10:05:00",
                "2024-01-01 10:07:00",
                "2024-01-01 10:07:00",
            ],
            "lat": [12.9716, 12.2958, 12.2958],
            "lng": [77.5946, 76.6394, 76.6394],
            "message": [
                "HELP at main road!",
                " Need police at park gate  ",
                None,
            ],
        }
    )
    logger.info("Raw SOS sample:\n%s", sample)
    cleanedSample = cleanSosReports(sample)
    logger.info("Cleaned SOS sample:\n%s", cleanedSample)
    outputPath = saveCleanSosReports(cleanedSample)
    logger.info("Dummy cleaned SOS reports written to %s", outputPath)
