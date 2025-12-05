from __future__ import annotations

import random
from typing import Any, Dict, List

from inference.sos_risk_model import predictSosRisk


def generateSyntheticSosContexts(count: int = 100) -> List[Dict[str, Any]]:
    contexts: List[Dict[str, Any]] = []
    for index in range(count):
        speedKmh = random.uniform(0.0, 40.0)
        suddenStop = random.random() < 0.2
        unsafeProbability = random.uniform(0.0, 1.0)
        timeInAppSeconds = random.uniform(0.0, 900.0)
        isHighRisk = unsafeProbability > 0.6 or suddenStop or speedKmh < 2.0
        contexts.append(
            {
                "id": f"sos-{index}",
                "speedKmh": speedKmh,
                "suddenStop": suddenStop,
                "unsafeProbability": unsafeProbability,
                "timeInAppSeconds": timeInAppSeconds,
                "trueHighRisk": isHighRisk,
            }
        )
    return contexts


def computeClassificationMetrics(trueLabels: List[bool], predictedLabels: List[bool]) -> Dict[str, float]:
    truePositive = falsePositive = trueNegative = falseNegative = 0
    for truth, prediction in zip(trueLabels, predictedLabels):
        if truth and prediction:
            truePositive += 1
        elif not truth and prediction:
            falsePositive += 1
        elif not truth and not prediction:
            trueNegative += 1
        else:
            falseNegative += 1

    total = max(1, truePositive + trueNegative + falsePositive + falseNegative)
    accuracy = (truePositive + trueNegative) / total
    precision = truePositive / max(1, truePositive + falsePositive)
    recall = truePositive / max(1, truePositive + falseNegative)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "tp": float(truePositive),
        "tn": float(trueNegative),
        "fp": float(falsePositive),
        "fn": float(falseNegative),
    }


def main() -> None:
    contexts = generateSyntheticSosContexts()
    predictions = [predictSosRisk(context) for context in contexts]

    predictedLabels = [bool(item.get("shouldPromptSos")) for item in predictions]
    trueLabels = [bool(item.get("trueHighRisk")) for item in contexts]

    metrics = computeClassificationMetrics(trueLabels, predictedLabels)

    print("SOS risk evaluation:")
    print("---------------------")
    for key, value in metrics.items():
        print(f"{key:10s}: {value:.3f}" if isinstance(value, float) else f"{key:10s}: {value}")


if __name__ == "__main__":  # pragma: no cover
    main()
