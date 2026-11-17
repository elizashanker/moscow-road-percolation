import unittest
import networkx as nx

from road_percolation.simulation import curve, local_order, mean_curve, random_order, threshold_candidates


class SimulationTests(unittest.TestCase):
    def test_multigraph_parallel_edges_and_isolates(self):
        graph = nx.MultiGraph()
        graph.add_nodes_from([0, 1, 2, 3])
        graph.add_edge(0, 1, key="first", length=2.0)
        graph.add_edge(0, 1, key="second", length=3.0)
        graph.add_edge(1, 2, key="bridge", length=5.0)
        order = [(0, 1, "first"), (0, 1, "second"), (1, 2, "bridge")]
        result = curve(graph, order, [0, 1 / 3, 2 / 3, 1])
        self.assertEqual([r["s1"] for r in result], [0.75, 0.75, 0.5, 0.25])
        self.assertEqual(result[-1]["components"], 4)
        self.assertEqual(result[1]["removed_length_fraction"], 0.2)
        self.assertEqual(graph.number_of_edges(), 3)

    def test_bridge_splits_two_blocks(self):
        graph = nx.Graph([(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3)])
        edges = list(graph.edges())
        order = [(2, 3)] + [e for e in edges if e != (2, 3)]
        result = curve(graph, order, [0, 1 / 7])
        self.assertEqual((result[1]["s1"], result[1]["s2"]), (0.5, 0.5))

    def test_peak_of_mean_is_not_mean_of_peaks(self):
        first = [{"q_requested": q, "q": q, "s1": 1, "s2": s} for q, s in [(0, 0), (0.25, 0.6), (0.5, 0.4), (0.75, 0.0), (1, 0)]]
        second = [{"q_requested": q, "q": q, "s1": 1, "s2": s} for q, s in [(0, 0), (0.25, 0.0), (0.5, 0.5), (0.75, 0.2), (1, 0)]]
        self.assertEqual(threshold_candidates(mean_curve([first, second])), [0.5])
        self.assertNotEqual((0.25 + 0.5) / 2, 0.5)

    def test_plateau_is_reported(self):
        summary = [{"q": 0.2, "mean_s2": 0.3}, {"q": 0.4, "mean_s2": 0.3}]
        self.assertEqual(threshold_candidates(summary), [0.2, 0.4])

    def test_local_and_random_reproducibility(self):
        graph = nx.path_graph(4)
        for node in graph:
            graph.nodes[node].update(x=float(node), y=0.0)
        self.assertEqual(local_order(graph, (0, 0), 1), [(0, 1), (1, 2), (2, 3)])
        self.assertEqual(random_order(graph, 2), random_order(graph, 2))

    def test_invalid_inputs_fail_before_experiment(self):
        graph = nx.path_graph(3)
        for fractions in [[0.5, 0.2], [-0.1], [float("nan")]]:
            with self.assertRaises(ValueError):
                curve(graph, list(graph.edges()), fractions)
        with self.assertRaises(ValueError):
            random_order(nx.DiGraph([(1, 2)]), 0)
        with self.assertRaises(ValueError):
            curve(graph, [(0, 1)], [0])


if __name__ == "__main__":
    unittest.main()
