import re
from typing import Dict, List, Any

class CitizenAssistant:
    """
    Citizen Safe-Access conversational assistant (Web / WhatsApp / Telegram proxy).
    Answers queries like:
    - 'Can I reach the hospital from here?'
    - 'Which clinic is open?'
    - 'How do I safely reach AIIMS or PMCH?'
    Respects Safety Guidelines: Never presents a route as guaranteed safe.
    """

    SAFETY_DISCLAIMER = (
        "⚠️ SAFETY NOTICE: Predictions are based on hydrologic models and satellite sensor estimates. "
        "Flood depths fluctuate rapidly. Never attempt to drive or walk through active flowing floodwaters. "
        "Follow on-ground directives from local police, NDRF, and District Disaster Management Authority (DDMA)."
    )

    def process_query(
        self,
        query: str,
        isolation_data: Dict[str, Any],
        district_geodata: Dict[str, Any],
        weather_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        q_lower = query.lower()

        # Check for specific community mention
        target_comm = None
        for comm in isolation_data.get("communities", []):
            c_name = comm.get("name", "").lower()
            c_id = (comm.get("id") or comm.get("community_id") or "").lower()
            if (c_name and c_name in q_lower) or (c_id and c_id in q_lower):
                target_comm = comm
                break

        # Check for hospital mention
        target_hosp = None
        for h in district_geodata.get("hospitals", []):
            if h["name"].lower() in q_lower or h["id"].lower() in q_lower or ("pmch" in q_lower and "pmch" in h["id"]) or ("aiims" in q_lower and "aiims" in h["id"]) or ("smch" in q_lower and "smch" in h["id"]):
                target_hosp = h
                break

        # Generate intelligent response
        if target_comm:
            status = target_comm["status"]
            acc = target_comm.get("access_details", {})

            if status == "ISOLATED":
                answer = (
                    f"🚨 **URGENT WARNING FOR {target_comm['name'].upper()}**:\n\n"
                    f"Our live road sensor and isolation graph indicates that **all primary and feeder road connections to healthcare facilities from your area are currently impassable due to severe water ingress**.\n\n"
                    f"• **Recommended Action**: Do NOT attempt to wade through submerged roads. Move to the highest floor or upper concrete structure.\n"
                    f"• **Emergency Rescue**: The District Disaster Management Authority and NDRF rescue boats have been assigned to your sector.\n"
                    f"• **Emergency Helplines**: 1077 (District Disaster Control Room) | 112 (National Emergency Service)."
                )
                route_viable = False
                route_path = []
            elif status == "DETOUR_REQUIRED":
                hosp_name = acc.get("target_hospital", {}).get("name", "Nearest Medical Center")
                dist = acc.get("distance_km", "Unknown")
                time_est = acc.get("est_time_mins", 30)
                segments = [s["name"] for s in acc.get("path_segments", [])]
                
                answer = (
                    f"ℹ️ **ACCESS ROUTE UPDATE FOR {target_comm['name']}**:\n\n"
                    f"The direct route to your nominal hospital is flooded. However, **an elevated alternative route to {hosp_name} is currently open**.\n\n"
                    f"• **Viable Facility**: {hosp_name}\n"
                    f"• **Total Estimated Distance**: {dist} km (~{time_est} minutes)\n"
                    f"• **Route Corridor**: {' ➔ '.join(segments)}\n"
                    f"• **Caution**: Exercise high vigilance near low-lying intersections."
                )
                route_viable = True
                route_path = acc.get("path_segments", [])
            else:
                hosp_name = acc.get("target_hospital", {}).get("name", "Nearest Clinic")
                answer = (
                    f"✅ **NORMAL ROUTE CLEAR**: Access from {target_comm['name']} to {hosp_name} is currently open and passable.\n\n"
                    f"• Distance: {acc.get('distance_km')} km (~{acc.get('est_time_mins')} mins)\n"
                    f"• Roads are currently within safe passability thresholds."
                )
                route_viable = True
                route_path = acc.get("path_segments", [])

        elif "hospital" in q_lower or "clinic" in q_lower or "bed" in q_lower:
            hosp_list = district_geodata.get("hospitals", [])
            open_hospitals = [f"• **{h['name']}** ({h['type'].replace('_', ' ').title()}) - {h.get('beds', 0)} beds, ICU: {'Yes' if h.get('icu_available') else 'No'}" for h in hosp_list]
            answer = (
                f"🏥 **Monitored Health Facilities Status**:\n\n" +
                "\n".join(open_hospitals) +
                "\n\nTo check safe pathing from your location, specify your neighborhood (e.g., *'Can I reach PMCH from Rajendra Nagar?'*)."
            )
            route_viable = True
            route_path = []
        else:
            rain = weather_data.get("weather", {}).get("rain_next_24h_mm", 0.0)
            gauge = weather_data.get("gauge", {}).get("current_gauge_m", 0.0)
            stn = weather_data.get("gauge", {}).get("station", "Local Gauge")
            
            answer = (
                f"👋 **FloodLens Safe-Access Assistant**\n\n"
                f"Current District Conditions:\n"
                f"• River Gauge ({stn}): **{gauge}m**\n"
                f"• Forecast Rainfall (24h): **{rain} mm**\n\n"
                f"You can ask me questions like:\n"
                f"• *'Can I reach the hospital from Rajendra Nagar?'*\n"
                f"• *'What is the route from Danapur Diara?'*\n"
                f"• *'Which hospitals have ICU capacity?'*"
            )
            route_viable = True
            route_path = []

        return {
            "query": query,
            "response": answer,
            "disclaimer": self.SAFETY_DISCLAIMER,
            "route_viable": route_viable,
            "suggested_path": route_path
        }

citizen_assistant = CitizenAssistant()
