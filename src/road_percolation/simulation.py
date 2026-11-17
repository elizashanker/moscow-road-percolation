"""Metrics preserve the initial node set and account for multigraph keys."""

from math import floor, isclose, isfinite
from random import Random

import networkx as nx


def edge_ids(graph):
    if graph.is_directed():
        raise ValueError("First-version experiments require an undirected graph")
    if graph.is_multigraph():
        return list(graph.edges(keys=True))
    return list(graph.edges())


def random_order(graph, seed):
    edges = edge_ids(graph)
    Random(seed).shuffle(edges)
    return edges


def local_order(graph, center, seed):
    """Order by metric midpoint distance, breaking ties using the given seed.

    Coordinates must already use a metric CRS. This function orders edges;
    the experiment runner must sample centers uniformly inside the polygon.
    """
    edges = random_order(graph, seed)
    cx, cy = center

    def distance(edge):
        u, v = edge[:2]
        attrs = graph.get_edge_data(*edge)
        geometry = attrs.get("geometry")
        if geometry is not None:
            point = geometry.interpolate(0.5, normalized=True)
            x, y = point.x, point.y
        else:
            x = (graph.nodes[u]["x"] + graph.nodes[v]["x"]) / 2
            y = (graph.nodes[u]["y"] + graph.nodes[v]["y"]) / 2
        return (x - cx) ** 2 + (y - cy) ** 2

    return sorted(edges, key=distance)


def curve(graph, order, fractions):
    """Evaluate a nested closure sequence without changing the input graph."""
    edges = edge_ids(graph)
    n0, m0 = len(graph), len(edges)
    if not n0 or not m0:
        raise ValueError("An experiment needs at least one node and one edge")
    if len(order) != m0 or set(order) != set(edges):
        raise ValueError("Order must contain each edge exactly once, with keys")
    qs = list(fractions)
    if not qs or any(not isfinite(q) or not 0 <= q <= 1 for q in qs):
        raise ValueError("Fractions must be finite and between 0 and 1")
    if qs != sorted(qs):
        raise ValueError("Fractions must be nondecreasing")
    lengths = {}
    for edge in edges:
        value = graph.get_edge_data(*edge).get("length")
        if value is not None and isfinite(value) and value >= 0:
            lengths[edge] = value
    total_length = sum(lengths.values()) if len(lengths) == m0 else None
    current = graph.copy()
    removed, removed_length = 0, 0.0
    rows = []
    for requested in qs:
        count = min(m0, floor(requested * m0 + 1e-10))
        while removed < count:
            edge = order[removed]
            current.remove_edge(*edge)
            removed_length += lengths.get(edge, 0.0)
            removed += 1
        sizes = sorted((len(c) for c in nx.connected_components(current)), reverse=True)
        rows.append({
            "q_requested": requested,
            "q": count / m0,
            "removed_edges": count,
            "s1": sizes[0] / n0,
            "s2": (sizes[1] if len(sizes) > 1 else 0) / n0,
            "components": len(sizes),
            "removed_length_fraction": (
                removed_length / total_length if total_length else None
            ),
        })
    return rows


def mean_curve(curves):
    """Average comparable whole trajectories; require the same achieved q."""
    curves = list(curves)
    if not curves or any(not c for c in curves):
        raise ValueError("At least one nonempty trajectory is required")
    grid = [(r["q_requested"], r["q"]) for r in curves[0]]
    if any([(r["q_requested"], r["q"]) for r in c] != grid for c in curves):
        raise ValueError("Trajectories must have identical grids and edge counts")
    result = []
    for i, (requested, q) in enumerate(grid):
        result.append({
            "q_requested": requested,
            "q": q,
            "mean_s1": sum(c[i]["s1"] for c in curves) / len(curves),
            "mean_s2": sum(c[i]["s2"] for c in curves) / len(curves),
            "repetitions": len(curves),
        })
    return result


def threshold_candidates(summary):
    """Return all maxima of mean S2, including ties; never average per-run peaks."""
    if not summary:
        raise ValueError("A summary curve is required")
    peak = max(r["mean_s2"] for r in summary)
    return sorted({r["q"] for r in summary if isclose(r["mean_s2"], peak, abs_tol=1e-12)})
