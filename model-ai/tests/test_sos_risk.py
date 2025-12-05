import unittest

from inference.sos_risk_model import getMockSosRiskInput, predictSosRisk


class SosRiskModelTests(unittest.TestCase):
    def test_predict_sos_risk_with_mock_input(self) -> None:
        context = getMockSosRiskInput()
        result = predictSosRisk(context)

        self.assertIsInstance(result, dict)
        self.assertIn("riskScore", result)
        self.assertIn("riskLevel", result)
        self.assertIn("shouldPromptSos", result)


if __name__ == "__main__":
    unittest.main()
