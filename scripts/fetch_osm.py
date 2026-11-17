"""Download and preserve OSM inputs; no percolation conclusions are generated."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tomllib


def main():
    import networkx as nx
    import osmnx as ox
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("configs/experiment.toml"))
    args = parser.parse_args()
    config = tomllib.loads(args.config.read_text(encoding="utf-8"))
    root = Path(__file__).resolve().parents[1]
    raw, processed = root / "data/raw", root / "data/processed"
    raw.mkdir(parents=True, exist_ok=True)
    processed.mkdir(parents=True, exist_ok=True)
    for district in config["districts"]:
        slug = district["slug"]
        target = processed / f"{slug}.graphml"
        if target.exists() or (raw / f"{slug}.geojson").exists():
            raise FileExistsError(f"Existing snapshot for {slug}; preserve or rename it before re-downloading")
        boundary = ox.geocode_to_gdf(district["osm_query"])
        polygon = boundary.geometry.iloc[0]
        if polygon.geom_type not in {"Polygon", "MultiPolygon"}:
            raise ValueError(f"Not an administrative polygon: {district['name']}")
        boundary.to_file(raw / f"{slug}.geojson", driver="GeoJSON")
        graph = ox.graph_from_polygon(polygon, network_type="drive", simplify=True, retain_all=True, truncate_by_edge=False)
        ox.save_graphml(graph, filepath=raw / f"{slug}_directed.graphml")
        graph = ox.convert.to_undirected(ox.project_graph(graph))
        loops = list(nx.selfloop_edges(graph, keys=True))
        graph.remove_edges_from(loops)
        ox.save_graphml(graph, filepath=target)
        sizes = sorted((len(c) for c in nx.connected_components(graph)), reverse=True)
        metadata = {
            "district": district,
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
            "osmnx_version": ox.__version__,
            "networkx_version": nx.__version__,
            "nodes": len(graph), "edges": graph.number_of_edges(),
            "component_sizes": sizes, "removed_self_loops": len(loops),
            "crs": str(graph.graph["crs"]),
            "graph_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "boundary_review_required": True,
            "attribution": "© OpenStreetMap contributors",
        }
        (processed / f"{slug}_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved {district['name']}: {len(graph)} nodes, {graph.number_of_edges()} edges. Verify boundary before experiments.")


if __name__ == "__main__":
    main()
