import unittest

from inference.night_mode_predictor import getMockNightModeInput, predictNightMode


class NightModePredictorTests(unittest.TestCase):
    def test_predict_night_mode_with_mock_input(self) -> None:
        context = getMockNightModeInput()
        result = predictNightMode(context)

        self.assertIsInstance(result, dict)
        self.assertIn("score", result)
        self.assertIn("shouldEnable", result)
        self.assertIn("threshold", result)


if __name__ == "__main__":
    unittest.main()
