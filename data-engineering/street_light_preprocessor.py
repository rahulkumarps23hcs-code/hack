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


def loadStreetLightData(inputPath: str, **readKwargs: Any) -> pd.DataFrame:
    path = Path(inputPath)
    if path.suffix.lower() == ".parquet":
        df = pd.read_parquet(path, **readKwargs)
    else:
        df = pd.read_csv(path, **readKwargs)
    logger.info("Loaded street light data from %s with shape %s", path, df.shape)
    return df


def preprocessStreetLights(
    df: pd.DataFrame,
    idCol: Optional[str] = None,
    latCol: str = "lat",
    lngCol: str = "lng",
    statusCol: str = "status",
    installTimestampCol: str = "installedAt",
    brightnessCol: str = "brightness",
) -> pd.DataFrame:
    cleaned = df.copy()
    if installTimestampCol in cleaned.columns:
        cleaned[installTimestampCol] = pd.to_datetime(cleaned[installTimestampCol], errors="coerce")
    if statusCol in cleaned.columns:
        statusSeries = cleaned[statusCol].astype(str).str.strip().str.lower()
        statusSeries = statusSeries.replace("nan", pd.NA)
        mapping = {
            "on": "working",
            "working": "working",
            "ok": "working",
            "operational": "working",
            "off": "off",
            "broken": "faulty",
            "faulty": "faulty",
            "not working": "faulty",
        }
        statusSeries = statusSeries.replace(mapping)
        cleaned[statusCol] = statusSeries.fillna("unknown")
    if brightnessCol in cleaned.columns:
        cleaned[brightnessCol] = pd.to_numeric(cleaned[brightnessCol], errors="coerce")
        medianBrightness = cleaned[brightnessCol].median()
        if not np.isnan(medianBrightness):
            cleaned[brightnessCol] = cleaned[brightnessCol].fillna(medianBrightness)
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
        logger.info("Dropped %d duplicate street light rows using idCol '%s'", before - len(cleaned), idCol)
    else:
        cleaned = cleaned.drop_duplicates()
    logger.info("Street light data cleaned; final shape=%s", cleaned.shape)
    return cleaned


def saveCleanStreetLights(
    df: pd.DataFrame,
    outputDir: str = "clean-data",
    filename: str = "street-lights-clean.parquet",
) -> Path:
    outputPath = resolveOutputPath(outputDir, filename)
    if outputPath.suffix.lower() == ".parquet":
        df.to_parquet(outputPath, index=False)
    else:
        df.to_csv(outputPath, index=False)
    logger.info("Saved cleaned street light data to %s", outputPath)
    return outputPath


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "id": ["L1", "L2", "L2"],
            "lat": [12.9716, 12.2958, 12.2958],
            "lng": [77.5946, 76.6394, 76.6394],
            "status": ["On", "BROKEN", None],
            "installedAt": ["2020-01-01", "2019-06-15", "2019-06-15"],
            "brightness": [100.0, None, 120.0],
        }
    )
    logger.info("Raw street light sample:\n%s", sample)
    cleanedSample = preprocessStreetLights(sample, idCol="id")
    logger.info("Cleaned street light sample:\n%s", cleanedSample)
    outputPath = saveCleanStreetLights(cleanedSample)
    logger.info("Dummy cleaned street light data written to %s", outputPath)
