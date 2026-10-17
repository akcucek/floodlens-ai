import networkx as nx
from typing import Dict, List, Any

class IsolationAnalyzer:
    """
    Graph-based road accessibility & community isolation analyzer using NetworkX.
    Determines which habitations lose connection to critical health centers,
    evaluates alternative routes, and flags marooned zones.
    """

    def analyze_district(
        self,
        district_geodata: Dict[str, Any],
        road_predictions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        # Map predictions by segment_id
        pred_map = {p["segment_id"]: p for p in road_predictions}

        # 1. Build NetworkX Graphs:
        # Full graph (pre-flood conditions)
        G_full = nx.Graph()
        # Active graph (excluding impassable roads, weighting cautionary roads)
        G_active = nx.Graph()

        # Add nodes with geographical coordinates
        for node_id, data in district_geodata.get("nodes", {}).items():
            G_full.add_node(node_id, **data)
            G_active.add_node(node_id, **data)

        for seg in district_geodata.get("road_segments", []):
            u = seg["u"]
            v = seg["v"]
            dist_km = seg.get("distance_km", 1.0)
            pred = pred_map.get(seg["id"], {})
            prob_fail = pred.get("probability_impassable", 0.0)
            status = pred.get("status", "passable")

            # Always add to full graph
            G_full.add_edge(u, v, id=seg["id"], name=seg["name"], distance=dist_km, weight=dist_km)

            # In active graph:
            if status != "impassable":
                # Add traversal penalty if cautionary (waterlogged but slowly passable)
                penalty = 1.0 if status == "passable" else 3.5
                G_active.add_edge(
                    u, v,
                    id=seg["id"],
                    name=seg["name"],
                    distance=dist_km,
                    weight=dist_km * penalty,
                    status=status
                )

        # 2. Identify available hospitals
        hospitals = district_geodata.get("hospitals", [])
        hospital_node_ids = {h["node_id"]: h for h in hospitals}

        # 3. Analyze each community
        communities = district_geodata.get("communities", [])
        community_results = []
        isolated_communities = []
        compromised_communities = []
        safe_communities = []

        total_cut_off_population = 0
        total_vulnerable_cut_off = 0

        for comm in communities:
            comm_node = comm["node_id"]
            nominal_target_hosp_id = comm.get("nearest_hospital_id")
            
            # Find best route on G_active to ANY open hospital
            best_route = None
            best_target_hosp = None
            min_weight = float("inf")

            for h_node, h_info in hospital_node_ids.items():
                if nx.has_path(G_active, comm_node, h_node):
                    try:
                        path = nx.shortest_path(G_active, comm_node, h_node, weight="weight")
                        path_weight = nx.shortest_path_length(G_active, comm_node, h_node, weight="weight")
                        if path_weight < min_weight:
                            min_weight = path_weight
                            best_route = path
                            best_target_hosp = h_info
                    except Exception:
                        pass

            # Check pre-flood nominal route on G_full
            nominal_route_nodes = []
            nominal_hosp_node = None
            for h in hospitals:
                if h["id"] == nominal_target_hosp_id:
                    nominal_hosp_node = h["node_id"]
                    break

            if nominal_hosp_node and nx.has_path(G_full, comm_node, nominal_hosp_node):
                nominal_route_nodes = nx.shortest_path(G_full, comm_node, nominal_hosp_node, weight="weight")

            # Determine isolation status
            if not best_route:
                # Completely cut off from all health centers!
                status = "ISOLATED"
                severity = "CRITICAL"
                total_cut_off_population += comm["population"]
                total_vulnerable_cut_off += comm["vulnerable_count"]
                isolated_communities.append(comm["name"])
                
                details = {
                    "reachable": False,
                    "target_hospital": None,
                    "path_nodes": [],
                    "path_segments": [],
                    "distance_km": 0.0,
                    "est_time_mins": 0,
                    "reason": "All connecting access corridors are submerged or impassable."
                }
            else:
                # Reachable, but is it the original nearest hospital or a detour?
                path_segs = self._nodes_to_segments(G_active, best_route)
                total_dist = sum(s.get("distance", 1.0) for s in path_segs)
                
                # Check if nominal path was cut
                nominal_severed = False
                if nominal_hosp_node:
                    nominal_severed = not nx.has_path(G_active, comm_node, nominal_hosp_node)

                has_cautionary = any(s.get("status") == "cautionary" for s in path_segs)

                if nominal_severed:
                    status = "DETOUR_REQUIRED"
                    severity = "WARNING"
                    compromised_communities.append(comm["name"])
                    est_time = int(total_dist * 3.5) # slower due to detours
                elif has_cautionary:
                    status = "RESTRICTED"
                    severity = "CAUTION"
                    compromised_communities.append(comm["name"])
                    est_time = int(total_dist * 2.8)
                else:
                    status = "CONNECTED"
                    severity = "NORMAL"
                    safe_communities.append(comm["name"])
                    est_time = int(total_dist * 1.5)

                details = {
                    "reachable": True,
                    "target_hospital": best_target_hosp,
                    "is_alternative_route": nominal_severed,
                    "path_nodes": best_route,
                    "path_segments": path_segs,
                    "distance_km": round(total_dist, 2),
                    "est_time_mins": est_time,
                    "reason": "Alternative elevated route active." if nominal_severed else "Corridor clear and accessible."
                }

            community_results.append({
                "community_id": comm["id"],
                "name": comm["name"],
                "lat": comm["lat"],
                "lon": comm["lon"],
                "elevation_m": comm.get("elevation_m", 50.0),
                "population": comm["population"],
                "vulnerable_population": comm["vulnerable_count"],
                "status": status,
                "severity": severity,
                "access_details": details
            })

        return {
            "communities": community_results,
            "summary": {
                "total_communities": len(communities),
                "isolated_count": len(isolated_communities),
                "isolated_names": isolated_communities,
                "compromised_count": len(compromised_communities),
                "compromised_names": compromised_communities,
                "safe_count": len(safe_communities),
                "population_cut_off": total_cut_off_population,
                "vulnerable_cut_off": total_vulnerable_cut_off
            }
        }

    def _nodes_to_segments(self, G: nx.Graph, node_list: List[str]) -> List[Dict[str, Any]]:
        segments = []
        for i in range(len(node_list) - 1):
            u = node_list[i]
            v = node_list[i + 1]
            edge_data = G.get_edge_data(u, v, default={})
            segments.append({
                "u": u,
                "v": v,
                "name": edge_data.get("name", f"{u}->{v}"),
                "distance": edge_data.get("distance", 1.0),
                "status": edge_data.get("status", "passable")
            })
        return segments

isolation_analyzer = IsolationAnalyzer()
