from pathlib import Path
from typing import Optional

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from .features import buildSosRiskFeatures, loadAlerts


def getTrainedDir() -> Path:
    return Path(__file__).resolve().parents[1] / "trained"


def trainSosRiskModel(alertsCsvDir: Optional[Path] = None) -> LogisticRegression:
    alerts = loadAlerts(alertsCsvDir)
    X, y = buildSosRiskFeatures(alerts)
    if len(np.unique(y)) < 2:
        raise ValueError("Not enough class variety to train SOS risk model.")
    XTrain, XTest, yTrain, yTest = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = LogisticRegression(max_iter=1000)
    model.fit(XTrain, yTrain)
    yPred = model.predict(XTest)
    report = classification_report(yTest, yPred, output_dict=False)
    print("SOS risk model classification report:\n", report)
    return model


def saveSosRiskModel(model: LogisticRegression, fileName: str = "sos_risk_model.pkl") -> Path:
    trainedDir = getTrainedDir()
    trainedDir.mkdir(parents=True, exist_ok=True)
    path = trainedDir / fileName
    joblib.dump(model, path)
    return path


def loadSosRiskModel(fileName: str = "sos_risk_model.pkl") -> LogisticRegression:
    path = getTrainedDir() / fileName
    if not path.exists():
        raise FileNotFoundError(f"SOS risk model file not found: {path}")
    model: LogisticRegression = joblib.load(path)
    return model


def predictSosRisk(
    model: LogisticRegression,
    hour: int,
    messageLength: int,
    isNight: int,
    severityCode: int = 1,
) -> float:
    features = np.array([[hour, messageLength, isNight, severityCode]], dtype=float)
    proba = model.predict_proba(features)[0, 1]
    return float(proba)
