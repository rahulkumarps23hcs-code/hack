import unittest

from inference.unsafe_zone_detector import getMockUnsafeZoneInput, predictUnsafeZones


class UnsafeZonePredictorTests(unittest.TestCase):
    def test_predict_unsafe_zones_with_mock_input(self) -> None:
        locations = getMockUnsafeZoneInput()
        result = predictUnsafeZones(locations)

        self.assertIsInstance(result, dict)
        self.assertIn("alerts", result)
        self.assertIn("scores", result)
        self.assertIn("heatmap", result)

        alerts = result["alerts"]
        scores = result["scores"]

        self.assertEqual(len(alerts), len(locations))
        self.assertEqual(len(scores), len(locations))


if __name__ == "__main__":
    unittest.main()
