import unittest

from utils import haversineDistanceKm, normalizeScore


class UtilsTests(unittest.TestCase):
    def test_haversine_distance_positive(self) -> None:
        distance = haversineDistanceKm(12.9716, 77.5946, 12.9352, 77.6245)
        self.assertGreater(distance, 0.0)

    def test_normalize_score_bounds(self) -> None:
        self.assertEqual(normalizeScore(-1.0), 0.0)
        self.assertEqual(normalizeScore(2.0), 1.0)
        middle = normalizeScore(0.5)
        self.assertGreaterEqual(middle, 0.0)
        self.assertLessEqual(middle, 1.0)


if __name__ == "__main__":
    unittest.main()
