import os
import json
import time
import requests
from typing import Dict, Any
from backend.config import DISTRICTS, OPEN_METEO_FORECAST_URL, OPEN_METEO_FLOOD_URL

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

class WeatherService:
    def __init__(self, cache_ttl_seconds: int = 300):
        self.cache_ttl = cache_ttl_seconds

    def get_weather_and_river(self, district_id: str, scenario: str = "live") -> Dict[str, Any]:
        """
        Fetches live real weather from Open-Meteo and river discharge from GloFAS.
        Supports scenarios: 'live', 'monsoon_surge', 'extreme_cloudburst'.
        """
        if district_id not in DISTRICTS:
            district_id = "patna"

        district = DISTRICTS[district_id]
        lat, lon = district["center"]
        cache_file = os.path.join(CACHE_DIR, f"live_{district_id}.json")

        data = None
        # Check cache if live
        if scenario == "live" and os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                    if time.time() - cached.get("_cached_at", 0) < self.cache_ttl:
                        data = cached
            except Exception:
                pass

        if not data:
            data = self._fetch_live(district, lat, lon)
            if data:
                data["_cached_at"] = time.time()
                try:
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                except Exception:
                    pass

        # Apply scenario adjustments if user selected a stress-test scenario
        return self._apply_scenario(data, district, scenario)

    def _fetch_live(self, district: Dict[str, Any], lat: float, lon: float) -> Dict[str, Any]:
        result = {
            "district": district["id"],
            "district_name": district["name"],
            "river_basin": district["river"],
            "source": "Open-Meteo Weather + GloFAS Flood API",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "status": "online",
            "weather": {},
            "river_discharge": {},
            "gauge": {}
        }

        # 1. Fetch Open-Meteo Weather
        try:
            w_res = requests.get(
                OPEN_METEO_FORECAST_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m",
                    "hourly": "precipitation,rain,weather_code",
                    "forecast_days": 3
                },
                timeout=8
            )
            if w_res.status_code == 200:
                w_json = w_res.json()
                curr = w_json.get("current", {})
                hourly = w_json.get("hourly", {})
                
                # Sum next 24h forecast rainfall
                rain_next_24h = sum(hourly.get("precipitation", [])[:24]) if hourly.get("precipitation") else 0.0

                result["weather"] = {
                    "temperature_c": curr.get("temperature_2m", 28.0),
                    "humidity_percent": curr.get("relative_humidity_2m", 65),
                    "precipitation_current_mm": curr.get("precipitation", 0.0),
                    "rain_next_24h_mm": round(rain_next_24h, 2),
                    "wind_speed_kmh": curr.get("wind_speed_10m", 10.0),
                    "weather_code": curr.get("weather_code", 0),
                    "hourly_rain": hourly.get("precipitation", [])[:24]
                }
        except Exception:
            pass

        if not result.get("weather"):
            result["weather"] = {
                "temperature_c": 24.5,
                "humidity_percent": 50,
                "precipitation_current_mm": 0.0,
                "rain_next_24h_mm": 0.0,
                "wind_speed_kmh": 7.5,
                "weather_code": 0,
                "hourly_rain": [0.0] * 24,
                "fallback": True
            }

        # 2. Fetch GloFAS Flood API River Discharge
        try:
            f_res = requests.get(
                OPEN_METEO_FLOOD_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "daily": "river_discharge,river_discharge_mean",
                    "forecast_days": 5
                },
                timeout=8
            )
            if f_res.status_code == 200:
                f_json = f_res.json()
                daily = f_json.get("daily", {})
                discharges = daily.get("river_discharge", [])
                discharge_mean = daily.get("river_discharge_mean", [])
                current_discharge = discharges[0] if discharges and discharges[0] is not None else 1250.0
                mean_baseline = discharge_mean[0] if discharge_mean and discharge_mean[0] is not None else 950.0

                result["river_discharge"] = {
                    "current_discharge_m3s": round(current_discharge, 1),
                    "baseline_mean_m3s": round(mean_baseline, 1),
                    "discharge_ratio": round(current_discharge / max(mean_baseline, 1.0), 2),
                    "forecast_5d": discharges[:5]
                }
        except Exception:
            result["river_discharge"] = {
                "current_discharge_m3s": 1450.0,
                "baseline_mean_m3s": 1050.0,
                "discharge_ratio": 1.38,
                "forecast_5d": [1450.0, 1520.0, 1610.0, 1490.0, 1380.0],
                "fallback": True
            }

        # 3. Compute River Gauge vs CWC Danger Level
        danger = district["danger_level_m"]
        warning = district["warning_level_m"]
        base_gauge = district["current_gauge_m_baseline"]

        # Derive simulated current gauge based on river discharge ratio
        ratio = result["river_discharge"].get("discharge_ratio", 1.0)
        est_gauge = round(base_gauge + (ratio - 1.0) * 1.5, 2)

        result["gauge"] = {
            "station": district["cwc_gauge_station"],
            "current_gauge_m": est_gauge,
            "warning_level_m": warning,
            "danger_level_m": danger,
            "above_warning": est_gauge >= warning,
            "above_danger": est_gauge >= danger,
            "freeboard_m": round(danger - est_gauge, 2)
        }

        return result

    def _apply_scenario(self, base_data: Dict[str, Any], district: Dict[str, Any], scenario: str) -> Dict[str, Any]:
        data = json.loads(json.dumps(base_data))
        data["scenario"] = scenario

        if scenario == "monsoon_surge":
            data["weather"]["precipitation_current_mm"] = max(data["weather"].get("precipitation_current_mm", 0), 18.5)
            data["weather"]["rain_next_24h_mm"] = max(data["weather"].get("rain_next_24h_mm", 0), 115.0)
            data["weather"]["weather_code"] = 65  # Heavy rain
            data["river_discharge"]["current_discharge_m3s"] *= 2.1
            data["river_discharge"]["discharge_ratio"] = round(data["river_discharge"]["discharge_ratio"] * 2.1, 2)
            data["gauge"]["current_gauge_m"] = round(district["warning_level_m"] + 0.35, 2)
            data["gauge"]["above_warning"] = True
            data["gauge"]["above_danger"] = False
            data["gauge"]["freeboard_m"] = round(district["danger_level_m"] - data["gauge"]["current_gauge_m"], 2)

        elif scenario == "extreme_cloudburst":
            data["weather"]["precipitation_current_mm"] = 48.0
            data["weather"]["rain_next_24h_mm"] = 245.0
            data["weather"]["weather_code"] = 95  # Thunderstorm with severe rain
            data["river_discharge"]["current_discharge_m3s"] *= 3.8
            data["river_discharge"]["discharge_ratio"] = round(data["river_discharge"]["discharge_ratio"] * 3.8, 2)
            data["gauge"]["current_gauge_m"] = round(district["danger_level_m"] + 0.92, 2)
            data["gauge"]["above_warning"] = True
            data["gauge"]["above_danger"] = True
            data["gauge"]["freeboard_m"] = round(district["danger_level_m"] - data["gauge"]["current_gauge_m"], 2)

        return data

weather_service = WeatherService()
