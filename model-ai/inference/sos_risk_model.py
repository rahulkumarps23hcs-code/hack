from typing import Any, Dict, List

from config import sosRiskConfig
from logging_utils import logError
from utils import getSosRiskModel, normalizeScore


def _extractRiskFeatures(context: Dict[str, Any]) -> List[float]:
    speedKmh = float(context.get("speedKmh", 0.0))
    suddenStop = 1.0 if context.get("suddenStop", False) else 0.0
    unsafeProbability = float(context.get("unsafeProbability", 0.0))
    timeInAppSeconds = float(context.get("timeInAppSeconds", 0.0)) / 600.0

    return [speedKmh / 80.0, suddenStop, unsafeProbability, timeInAppSeconds]


def _riskLevel(score: float) -> str:
    if score >= sosRiskConfig.highRiskThreshold:
        return "high"
    if score >= sosRiskConfig.mediumRiskThreshold:
        return "medium"
    return "low"


def predictSosRisk(context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        model = getSosRiskModel()
        features = _extractRiskFeatures(context)
        rawProbability = float(model.predictProba(features))
        score = normalizeScore(rawProbability, 0.0, 1.0)

        level = _riskLevel(score)
        shouldPromptSos = score >= sosRiskConfig.triggerPromptThreshold

        return {
            "riskScore": score,
            "riskLevel": level,
            "shouldPromptSos": shouldPromptSos,
            "thresholds": {
                "high": sosRiskConfig.highRiskThreshold,
                "medium": sosRiskConfig.mediumRiskThreshold,
                "prompt": sosRiskConfig.triggerPromptThreshold,
            },
        }
    except Exception as error:
        logError("predictSosRisk failed", error)
        return {
            "riskScore": 0.0,
            "riskLevel": "low",
            "shouldPromptSos": False,
            "thresholds": {
                "high": sosRiskConfig.highRiskThreshold,
                "medium": sosRiskConfig.mediumRiskThreshold,
                "prompt": sosRiskConfig.triggerPromptThreshold,
            },
            "error": "sos risk prediction error",
        }


def getMockSosRiskInput() -> Dict[str, Any]:
    return {
        "speedKmh": 3.0,
        "suddenStop": True,
        "unsafeProbability": 0.8,
        "timeInAppSeconds": 300,
    }
