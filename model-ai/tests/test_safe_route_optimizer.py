import unittest

from inference.safe_route_optimizer import getMockRoutesInput, optimizeSafeRoute
from utils import buildRouteGraph, dijkstraShortestPath


class SafeRouteOptimizerTests(unittest.TestCase):
    def test_optimize_safe_route_with_mock_input(self) -> None:
        routes = getMockRoutesInput()
        result = optimizeSafeRoute(routes)

        self.assertIsInstance(result, dict)
        self.assertIn("bestRouteIndex", result)
        self.assertIn("bestRoute", result)
        self.assertTrue(result["graphUsed"])

    def test_graph_and_dijkstra_consistency(self) -> None:
        routes = getMockRoutesInput()
        graph = buildRouteGraph(routes)

        firstRoute = routes[0]
        startNode = (firstRoute[0]["lat"], firstRoute[0]["lng"])
        endNode = (firstRoute[-1]["lat"], firstRoute[-1]["lng"])

        distance, path = dijkstraShortestPath(graph, startNode, endNode)

        self.assertGreaterEqual(distance, 0.0)
        self.assertGreaterEqual(len(path), 1)


if __name__ == "__main__":
    unittest.main()
