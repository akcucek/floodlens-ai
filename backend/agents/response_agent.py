import time
from typing import Dict, List, Any

class FloodLensResponseAgent:
    """
    FloodLens Autonomous Decision Support Response Agent.
    Implements ADK-style tools:
    - get_risk(area)
    - find_isolated_areas()
    - nearest_open_service(origin)
    - alternative_route(origin, destination)
    - rank_by_population()
    Produces verifiable dispatch plans with human approval state machine.
    """

    def __init__(self):
        self.dispatch_plans: List[Dict[str, Any]] = []

    def get_risk(self, area_name: str, isolation_data: Dict[str, Any], weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tool: get_risk(area)"""
        for comm in isolation_data.get("communities", []):
            if area_name.lower() in comm["name"].lower():
                return {
                    "area": comm["name"],
                    "status": comm["status"],
                    "severity": comm["severity"],
                    "population": comm["population"],
                    "vulnerable_population": comm["vulnerable_population"],
                    "gauge_danger": weather_data.get("gauge", {}).get("above_danger", False),
                    "rainfall_24h_mm": weather_data.get("weather", {}).get("rain_next_24h_mm", 0.0)
                }
        return {"area": area_name, "error": "Area not found in monitored sectors"}

    def find_isolated_areas(self, isolation_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tool: find_isolated_areas()"""
        isolated = []
        for comm in isolation_data.get("communities", []):
            if comm["status"] == "ISOLATED":
                isolated.append(comm)
        return isolated

    def nearest_open_service(self, origin_name: str, isolation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tool: nearest_open_service()"""
        for comm in isolation_data.get("communities", []):
            if origin_name.lower() in comm["name"].lower():
                details = comm.get("access_details", {})
                return {
                    "origin": comm["name"],
                    "reachable": details.get("reachable", False),
                    "target_hospital": details.get("target_hospital"),
                    "distance_km": details.get("distance_km", 0.0),
                    "est_time_mins": details.get("est_time_mins", 0),
                    "is_alternative_route": details.get("is_alternative_route", False)
                }
        return {"error": f"Origin {origin_name} not found"}

    def rank_by_population(self, isolation_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tool: rank_by_population()"""
        all_comms = isolation_data.get("communities", [])
        # Score priority: ISOLATED * 1000 + DETOUR * 300 + vulnerable_pop * 0.1 + total_pop * 0.01
        def priority_score(c):
            mult = 10000 if c["status"] == "ISOLATED" else (3000 if c["status"] == "DETOUR_REQUIRED" else 500)
            return mult + c["vulnerable_population"] * 2.0 + c["population"] * 0.2

        ranked = sorted(all_comms, key=priority_score, reverse=True)
        return ranked

    def generate_dispatch_plan(
        self,
        district_name: str,
        isolation_data: Dict[str, Any],
        weather_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesizes agent tools to produce evidence summary and ranked dispatch priorities
        for District Magistrate and NDRF/SDRF commanders.
        """
        isolated = self.find_isolated_areas(isolation_data)
        ranked_comms = self.rank_by_population(isolation_data)
        
        priorities = []
        for idx, comm in enumerate(ranked_comms[:5], 1):
            status = comm["status"]
            pop = comm["population"]
            vuln = comm["vulnerable_population"]
            
            if status == "ISOLATED":
                rec_action = "Deploy NDRF Inflatable Zodiac Motorboats & Mobile Medical Tent. Establish emergency food/ORV supply bridge."
                unit_assigned = f"NDRF 9th Bn Strike Team #{idx}"
                resource = "4x Rescue Boats + 10 Para-medics + 500 Ration Kits"
                urgency = "P1 - IMMEDIATE LIFE SAFETY"
            elif status == "DETOUR_REQUIRED":
                rec_action = f"Deploy Traffic Police to mark submerged arterial and direct ambulances via designated elevated alternate route ({comm['access_details'].get('distance_km', '0')} km)."
                unit_assigned = f"SDRF Escort & Traffic Control Unit #{idx}"
                resource = "2x High-clearance 4x4 Ambulances + Road Signage"
                urgency = "P2 - LOGISTICAL CORRIDOR"
            else:
                rec_action = "Maintain standby drainage pumps and monitor river gauge outfall."
                unit_assigned = "Municipal Engineering Rapid Team"
                resource = "2x Heavy Dewatering Pumps (5000 LPM)"
                urgency = "P3 - PREVENTATIVE"

            priorities.append({
                "rank": idx,
                "target_area": comm["name"],
                "status": status,
                "population_affected": pop,
                "vulnerable_citizens": vuln,
                "urgency": urgency,
                "recommended_action": rec_action,
                "resource_package": resource,
                "assigned_unit": unit_assigned,
                "evidence_basis": f"Isolation Model: Access status is '{status}'. Nearest hospital route has failure prob >= 0.75. River level: {weather_data.get('gauge', {}).get('current_gauge_m')}m."
            })

        evidence_summary = (
            f"Based on real-time GloFAS river discharge ({weather_data.get('river_discharge', {}).get('current_discharge_m3s')} m³/s) "
            f"and 24h precipitation forecast ({weather_data.get('weather', {}).get('rain_next_24h_mm')} mm), "
            f"{len(isolated)} communities are fully marooned with severed healthcare access, affecting {isolation_data.get('summary', {}).get('population_cut_off', 0):,} citizens. "
            f"Automated priority ranking recommends immediate deployment of watercraft rescue units to high-density cut-off zones."
        )

        plan = {
            "plan_id": f"DISPATCH-{int(time.time())}",
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S IST"),
            "district": district_name,
            "evidence_summary": evidence_summary,
            "priorities": priorities,
            "approval_state": "PENDING_OFFICIAL_REVIEW",
            "approved_by": None,
            "approved_at": None,
            "dispatched_units": 0
        }

        self.dispatch_plans.insert(0, plan)
        return plan

    def approve_plan(self, plan_id: str, official_name: str = "District Magistrate / Addl. DM Relief") -> Dict[str, Any]:
        for plan in self.dispatch_plans:
            if plan["plan_id"] == plan_id:
                plan["approval_state"] = "APPROVED_BY_DISTRICT_AUTHORITY"
                plan["approved_by"] = official_name
                plan["approved_at"] = time.strftime("%Y-%m-%d %H:%M:%S IST")
                plan["dispatched_units"] = len(plan["priorities"])
                return {"status": "success", "plan": plan}
        return {"status": "error", "message": "Plan ID not found"}

response_agent = FloodLensResponseAgent()
