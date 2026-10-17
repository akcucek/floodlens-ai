import time
from typing import List, Dict, Any
from backend.config import DISTRICTS

class AlertService:
    """
    Alert service calibrated to official IMD (India Meteorological Department),
    NDMA Sachet, and CWC (Central Water Commission) criteria.
    - Green (No Warning): Rain < 64.5 mm and gauge < warning level.
    - Yellow (Watch / Be Updated): Rain 64.5 - 115.5 mm (Heavy Rain) or gauge near warning.
    - Orange (Alert / Be Prepared): Rain 115.6 - 204.4 mm (Very Heavy Rain) or gauge >= warning level.
    - Red (Warning / Take Action): Rain > 204.4 mm (Extremely Heavy Rain) or gauge >= danger level.
    """

    def get_district_alerts(self, district_id: str, scenario: str = "live", weather_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        district = DISTRICTS.get(district_id, DISTRICTS["patna"])
        alerts = []
        now_str = time.strftime("%Y-%m-%d %H:%M:%S IST")

        rain_24h = 0.0
        rain_rate = 0.0
        if weather_data and "weather" in weather_data:
            rain_24h = float(weather_data["weather"].get("rain_next_24h_mm", 0.0))
            rain_rate = float(weather_data["weather"].get("precipitation_current_mm", 0.0))

        cur_gauge = 0.0
        warning_level = float(district.get("warning_level_m", 50.0))
        danger_level = float(district.get("danger_level_m", 52.0))
        if weather_data and "gauge" in weather_data:
            cur_gauge = float(weather_data["gauge"].get("current_gauge_m", 0.0))

        # Check Red Alert criteria
        is_cloudburst = (scenario == "extreme_cloudburst") or (rain_24h >= 204.5) or (rain_rate >= 50.0)
        is_above_danger = cur_gauge >= danger_level

        # Check Orange Alert criteria
        is_monsoon_surge = (scenario == "monsoon_surge") or (rain_24h >= 115.6) or (rain_rate >= 25.0)
        is_above_warning = cur_gauge >= warning_level

        # Check Yellow Alert criteria (IMD Heavy Rain: 64.5 - 115.5 mm)
        is_heavy_rain = (rain_24h >= 64.5) or (cur_gauge >= warning_level - 0.5)

        if is_cloudburst or is_above_danger:
            alerts.append({
                "id": f"NDMA-RED-{district_id}-01",
                "agency": "NDMA Sachet / IMD",
                "level": "RED",
                "headline": f"FLASH FLOOD & INUNDATION WARNING: {district['name'].upper()}",
                "description": f"Extremely heavy rainfall detected ({rain_24h:.1f} mm). Immediate threat of severe inundation in low-lying areas. River {district['river']} rising rapidly above danger mark ({district['danger_level_m']}m). Evacuate vulnerable settlements.",
                "area": district["name"],
                "effective": now_str,
                "expires": "Next 24 Hours",
                "recommended_action": "Execute immediate evacuation of riverine lowlands and Diara habitations. Mobilize NDRF/SDRF boats.",
                "confidence": 0.95
            })
            if is_above_danger:
                alerts.append({
                    "id": f"CWC-DANGER-{district_id}-02",
                    "agency": "Central Water Commission (CWC)",
                    "level": "RED",
                    "headline": f"RIVER GAUGE EXCEEDS DANGER LEVEL AT {district['cwc_gauge_station']}",
                    "description": f"Water level ({cur_gauge:.2f}m) has breached danger mark {district['danger_level_m']}m. Backflow into municipal drainage outfalls expected.",
                    "area": district["name"],
                    "effective": now_str,
                    "expires": "Next 12 Hours",
                    "recommended_action": "Close flood gates and deploy high-capacity dewatering pumps at major outfalls.",
                    "confidence": 0.98
                })

        elif is_monsoon_surge or is_above_warning:
            alerts.append({
                "id": f"IMD-ORANGE-{district_id}-01",
                "agency": "IMD (India Meteorological Department)",
                "level": "ORANGE",
                "headline": f"VERY HEAVY RAINFALL ALERT: {district['name'].upper()}",
                "description": f"Continuous rainfall expected ({rain_24h:.1f} mm / 24h). River gauge approaching or above warning level ({warning_level}m). Waterlogging likely on secondary arterials.",
                "area": district["name"],
                "effective": now_str,
                "expires": "Next 36 Hours",
                "recommended_action": "Avoid underpasses and low-lying arterial transit. Pre-position disaster response vehicles.",
                "confidence": 0.88
            })

        elif is_heavy_rain:
            alerts.append({
                "id": f"IMD-YELLOW-{district_id}-01",
                "agency": "IMD District Bulletin",
                "level": "YELLOW",
                "headline": f"HEAVY RAINFALL WATCH: {district['name']}",
                "description": f"Isolated heavy showers forecasted ({rain_24h:.1f} mm / 24h) over {district['river']}. Localized waterlogging possible in low depressions.",
                "area": district["name"],
                "effective": now_str,
                "expires": "Next 48 Hours",
                "recommended_action": "Monitor municipal drainage and clear catch basins.",
                "confidence": 0.82
            })

        # Under normal conditions (rain < 64.5 mm and river normal), return no active alerts!
        return alerts

alert_service = AlertService()
