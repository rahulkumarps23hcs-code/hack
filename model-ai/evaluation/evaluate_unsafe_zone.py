from __future__ import annotations

import random
from typing import Any, Dict, List, Tuple

from inference.unsafe_zone_detector import predictUnsafeZones


def generateSyntheticUnsafeData(count: int = 100) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for index in range(count):
        recentIncidents = random.randint(0, 10)
        crowdScore = random.uniform(0.1, 1.0)
        isUnsafe = recentIncidents >= 4 or crowdScore <= 0.4
        records.append(
            {
                "id": f"synthetic-{index}",
                "timestamp": "2025-01-01T21:00:00",
                "location": {"lat": 12.9 + random.random() * 0.1, "lng": 77.5 + random.random() * 0.1},
                "recentIncidents": recentIncidents,
                "crowdScore": crowdScore,
                "trueUnsafe": isUnsafe,
            }
        )
    return records


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


def printScoreDistribution(scores: List[float]) -> None:
    if not scores:
        print("No scores to summarize")
        return
    minimum = min(scores)
    maximum = max(scores)
    average = sum(scores) / len(scores)
    print(f"score min={minimum:.3f} max={maximum:.3f} mean={average:.3f}")


def main() -> None:
    records = generateSyntheticUnsafeData()
    result = predictUnsafeZones(records)

    scores = result.get("scores", [])
    predictedLabels = [bool(item.get("isUnsafe")) for item in scores]
    trueLabels = [bool(item.get("trueUnsafe")) for item in records]

    metrics = computeClassificationMetrics(trueLabels, predictedLabels)

    print("Unsafe zone evaluation:")
    print("------------------------")
    for key, value in metrics.items():
        print(f"{key:10s}: {value:.3f}" if isinstance(value, float) else f"{key:10s}: {value}")

    probabilityValues = [float(item.get("unsafeProbability", 0.0)) for item in scores]
    print("\nScore distribution:")
    print("-------------------")
    printScoreDistribution(probabilityValues)


if __name__ == "__main__":  # pragma: no cover
    main()
