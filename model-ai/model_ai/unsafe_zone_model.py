from pathlib import Path
from typing import Optional

import joblib
import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from .features import buildUnsafeZoneFeatures, loadAlerts


def getTrainedDir() -> Path:
    return Path(__file__).resolve().parents[1] / "trained"


def trainUnsafeZoneModel(alertsCsvDir: Optional[Path] = None) -> DecisionTreeClassifier:
    alerts = loadAlerts(alertsCsvDir)
    X, y = buildUnsafeZoneFeatures(alerts)
    if len(np.unique(y)) < 2:
        raise ValueError("Not enough class variety to train unsafe zone model.")
    XTrain, XTest, yTrain, yTest = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(XTrain, yTrain)
    yPred = model.predict(XTest)
    report = classification_report(yTest, yPred, output_dict=False)
    print("Unsafe zone model classification report:\n", report)
    return model


def saveUnsafeZoneModel(model: DecisionTreeClassifier, fileName: str = "unsafe_zone_model.pkl") -> Path:
    trainedDir = getTrainedDir()
    trainedDir.mkdir(parents=True, exist_ok=True)
    path = trainedDir / fileName
    joblib.dump(model, path)
    return path


def loadUnsafeZoneModel(fileName: str = "unsafe_zone_model.pkl") -> DecisionTreeClassifier:
    path = getTrainedDir() / fileName
    if not path.exists():
        raise FileNotFoundError(f"Unsafe zone model file not found: {path}")
    model: DecisionTreeClassifier = joblib.load(path)
    return model


def predictUnsafeScore(
    model: DecisionTreeClassifier,
    lat: float,
    lng: float,
    hour: int,
    dayOfWeek: int,
    severityCode: int = 1,
) -> float:
    features = np.array([[lat, lng, hour, dayOfWeek, severityCode]], dtype=float)
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(features)[0, 1]
        return float(proba)
    prediction = model.predict(features)[0]
    return float(prediction)
