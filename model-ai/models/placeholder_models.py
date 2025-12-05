import math
from typing import Sequence


class LogisticSafetyModel:
    """Lightweight placeholder for a logistic regression-style safety model.

    Accepts a feature vector and returns an unsafe probability in [0, 1].
    """

    def __init__(self, weights: Sequence[float] | None = None, bias: float = 0.0) -> None:
        self.weights = list(weights) if weights is not None else [
            0.4,
            0.3,
            0.2,
            0.1,
        ]
        self.bias = bias

    def predictProba(self, features: Sequence[float]) -> float:
        size = min(len(features), len(self.weights))
        zValue = self.bias
        for index in range(size):
            zValue += features[index] * self.weights[index]
        return 1.0 / (1.0 + math.exp(-zValue))


class RandomForestSafetyModel:
    """Lightweight placeholder for a random forest-style safety model.

    Simulates an ensemble of small logistic "trees" and averages their
    probabilities. Deterministic and cheap, suitable for mocks.
    """

    def __init__(self) -> None:
        self.trees: list[tuple[list[float], float]] = [
            ([0.3, 0.1, -0.1], 0.05),
            ([0.1, 0.25, 0.05], -0.05),
            ([0.05, 0.05, 0.2], 0.0),
        ]

    @staticmethod
    def _treeProba(features: Sequence[float], weights: Sequence[float], bias: float) -> float:
        size = min(len(features), len(weights))
        zValue = bias
        for index in range(size):
            zValue += features[index] * weights[index]
        return 1.0 / (1.0 + math.exp(-zValue))

    def predictProba(self, features: Sequence[float]) -> float:
        if not self.trees:
            return 0.5
        probabilities = [self._treeProba(features, weights, bias) for (weights, bias) in self.trees]
        return sum(probabilities) / len(probabilities)
