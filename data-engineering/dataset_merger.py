from pathlib import Path
from typing import Dict, Mapping, Optional

import pandas as pd

from logger import getLogger
from geospatial_utils import addRoundedCoordinates


logger = getLogger(__name__)


def resolveOutputPath(outputDir: str, filename: str) -> Path:
    baseDir = Path(__file__).resolve().parent
    outDir = (baseDir / outputDir) if not Path(outputDir).is_absolute() else Path(outputDir)
    outDir.mkdir(parents=True, exist_ok=True)
    return outDir / filename


def mergeOnTimeAndLocation(
    crimeDf: Optional[pd.DataFrame] = None,
    streetDf: Optional[pd.DataFrame] = None,
    crowdDf: Optional[pd.DataFrame] = None,
    sosDf: Optional[pd.DataFrame] = None,
    timeColumns: Optional[Mapping[str, str]] = None,
    latColumns: Optional[Mapping[str, str]] = None,
    lngColumns: Optional[Mapping[str, str]] = None,
    timeFreq: str = "5min",
    latRound: int = 4,
    lngRound: int = 4,
) -> pd.DataFrame:
    frames: Dict[str, pd.DataFrame] = {}
    if crimeDf is not None:
        frames["crime"] = crimeDf
    if streetDf is not None:
        frames["street"] = streetDf
    if crowdDf is not None:
        frames["crowd"] = crowdDf
    if sosDf is not None:
        frames["sos"] = sosDf
    if not frames:
        raise ValueError("At least one dataset must be provided for merging.")
    timeColumns = timeColumns or {}
    latColumns = latColumns or {}
    lngColumns = lngColumns or {}
    processed: Dict[str, pd.DataFrame] = {}
    for name, df in frames.items():
        temp = df.copy()
        timeCol = timeColumns.get(name, "timestamp")
        latCol = latColumns.get(name, "lat")
        lngCol = lngColumns.get(name, "lng")
        if timeCol not in temp.columns:
            raise KeyError(f"Time column '{timeCol}' not found in {name} dataset.")
        if latCol not in temp.columns or lngCol not in temp.columns:
            raise KeyError(
                f"Latitude/longitude columns '{latCol}'/'{lngCol}' not found in {name} dataset."
            )
        temp[timeCol] = pd.to_datetime(temp[timeCol], errors="coerce")
        temp = temp.dropna(subset=[timeCol])
        temp["timeBucket"] = temp[timeCol].dt.floor(timeFreq)
        temp = addRoundedCoordinates(
            temp,
            latCol=latCol,
            lngCol=lngCol,
            latRound=latRound,
            lngRound=lngRound,
        )
        temp = temp.rename(columns={"latRound": "latBucket", "lngRound": "lngBucket"})
        keyCols = {"timeBucket", "latBucket", "lngBucket", timeCol, latCol, lngCol}
        baseCols = [c for c in temp.columns if c in keyCols]
        valueCols = [c for c in temp.columns if c not in keyCols]
        renameMap: Dict[str, str] = {c: f"{name}__{c}" for c in valueCols}
        temp = temp[baseCols + valueCols].rename(columns=renameMap)
        processed[name] = temp
    merged: Optional[pd.DataFrame] = None
    for name, df in processed.items():
        if merged is None:
            merged = df
        else:
            merged = pd.merge(
                merged,
                df,
                on=["timeBucket", "latBucket", "lngBucket"],
                how="outer",
            )
    merged = merged.sort_values(["timeBucket", "latBucket", "lngBucket"]).reset_index(drop=True)
    logger.info("Merged datasets %s into shape %s", list(processed.keys()), merged.shape)
    return merged


def saveMergedDataset(
    df: pd.DataFrame,
    outputDir: str = "clean-data",
    filename: str = "merged-dataset.parquet",
) -> Path:
    outputPath = resolveOutputPath(outputDir, filename)
    if outputPath.suffix.lower() == ".parquet":
        df.to_parquet(outputPath, index=False)
    else:
        df.to_csv(outputPath, index=False)
    logger.info("Saved merged dataset to %s", outputPath)
    return outputPath


if __name__ == "__main__":
    crime = pd.DataFrame(
        {
            "id": [1, 2],
            "type": ["robbery", "assault"],
            "severity": ["high", "medium"],
            "timestamp": ["2024-01-01 10:00:00", "2024-01-01 10:06:00"],
            "lat": [12.9716, 12.2958],
            "lng": [77.5946, 76.6394],
            "description": ["wallet stolen", "street fight"],
        }
    )
    sos = pd.DataFrame(
        {
            "id": [101],
            "timestamp": ["2024-01-01 10:05:00"],
            "lat": [12.97155],
            "lng": [77.59465],
            "description": ["help at main road"],
        }
    )
    mergedDemo = mergeOnTimeAndLocation(crimeDf=crime, sosDf=sos, timeFreq="5min")
    logger.info("Merged demo dataset:\n%s", mergedDemo)
    outputPath = saveMergedDataset(mergedDemo)
    logger.info("Dummy merged dataset written to %s", outputPath)
