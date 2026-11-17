"""Offline demonstration, explicitly not Moscow data."""

import csv
from pathlib import Path

import networkx as nx
from road_percolation.simulation import (
    curve, local_order, mean_curve, random_order, threshold_candidates,
)


def main():
    graph = nx.grid_2d_graph(8, 8)
    for (x, y) in graph:
        graph.nodes[(x, y)].update(x=x, y=y)
    nx.set_edge_attributes(graph, 1.0, "length")
    qs = [i / 50 for i in range(51)]
    output = Path(__file__).resolve().parents[1] / "reports" / "tables"
    output.mkdir(parents=True, exist_ok=True)
    for scenario in ["random", "local"]:
        runs = []
        rows = []
        for seed in range(20):
            # Uniform center in the demo grid square, not an OSM polygon.
            from random import Random
            rng = Random(seed)
            center = (rng.uniform(0, 7), rng.uniform(0, 7))
            order = random_order(graph, seed) if scenario == "random" else local_order(graph, center, seed)
            run = curve(graph, order, qs)
            runs.append(run)
            rows.extend(dict(row, seed=seed, scenario=scenario, data_source="synthetic_grid") for row in run)
        summary = mean_curve(runs)
        for name, records in [(f"demo_{scenario}_runs.csv", rows), (f"demo_{scenario}_summary.csv", summary)]:
            with (output / name).open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(records[0]))
                writer.writeheader()
                writer.writerows(records)
        print(f"Synthetic grid / {scenario}: q_star candidates = {threshold_candidates(summary)}")


if __name__ == "__main__":
    main()
