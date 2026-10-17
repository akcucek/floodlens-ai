import os
import time
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from backend.config import DISTRICTS
from backend.data_sources.weather_service import weather_service
from backend.data_sources.alert_service import alert_service
from backend.data_sources.osm_service import osm_service
from backend.data_sources.community_reports import community_report_service
from backend.intelligence.road_failure import road_failure_model
from backend.intelligence.isolation_graph import isolation_analyzer
from backend.intelligence.gemini_verifier import gemini_verifier
from backend.agents.response_agent import response_agent
from backend.agents.citizen_bot import citizen_assistant

app = FastAPI(
    title="FloodLens AI API",
    description="Live flood impact and safe-access intelligence for India",
    version="1.0.0"
)

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Request Models ---
class ReportSubmitRequest(BaseModel):
    district: str
    author: str
    reported_text: str
    photo_url: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

class ChatQueryRequest(BaseModel):
    district: str
    query: str
    scenario: Optional[str] = "live"

class ApprovePlanRequest(BaseModel):
    plan_id: str
    official_name: Optional[str] = "District Magistrate / Addl. DM Relief"

# --- API Endpoints ---

@app.get("/api/districts")
def get_districts():
    """Returns available monitored flood-prone districts."""
    return {"districts": list(DISTRICTS.values())}

@app.get("/api/flood-intelligence")
def get_flood_intelligence(
    district: str = Query("patna", description="District ID (e.g., patna, silchar, wayanad)"),
    scenario: str = Query("live", description="Scenario: live, monsoon_surge, extreme_cloudburst")
):
    """
    Core Intelligence Pipeline:
    1. Ingests Open-Meteo weather & GloFAS river discharge
    2. Ingests CWC river gauge & NDMA Sachet alerts
    3. Runs Road-Failure Prediction Model
    4. Runs NetworkX Community Isolation & Safe-Access Routing
    5. Merges crowdsourced community reports
    """
    if district not in DISTRICTS:
        district = "patna"

    district_cfg = DISTRICTS[district]
    
    # 1. Weather and River Discharge
    weather_data = weather_service.get_weather_and_river(district, scenario)

    # 2. Alerts
    alerts = alert_service.get_district_alerts(district, scenario, weather_data)

    # 3. OSM & Geospatial Features
    geodata = osm_service.get_district_geodata(district)
    base_elev = district_cfg["dem_base_elevation_m"]

    # 4. Predict Road Failures
    road_predictions = []
    for seg in geodata.get("road_segments", []):
        pred = road_failure_model.predict_segment_failure(seg, weather_data, base_elev)
        road_predictions.append(pred)

    # 5. Isolation Graph Analysis
    isolation_data = isolation_analyzer.analyze_district(geodata, road_predictions)

    # 6. Community Reports
    reports = community_report_service.get_reports_for_district(district)

    return {
        "district": district_cfg,
        "scenario": scenario,
        "timestamp": weather_data.get("timestamp"),
        "weather": weather_data.get("weather"),
        "river_discharge": weather_data.get("river_discharge"),
        "gauge": weather_data.get("gauge"),
        "alerts": alerts,
        "hospitals": geodata.get("hospitals", []),
        "shelters": geodata.get("shelters", []),
        "nodes": geodata.get("nodes", {}),
        "road_segments": geodata.get("road_segments", []),
        "road_predictions": road_predictions,
        "isolation_analysis": isolation_data,
        "community_reports": reports
    }

@app.post("/api/reports/submit")
def submit_community_report(req: ReportSubmitRequest):
    """
    Intake citizen report:
    Extracts text (Hindi/Assamese/English), verifies water depth & plausibility with Gemini.
    """
    district_info = DISTRICTS.get(req.district, DISTRICTS["patna"])
    coords = {"lat": req.lat, "lon": req.lon} if req.lat and req.lon else None

    # Call Gemini verifier
    verification = gemini_verifier.extract_and_verify(
        raw_text=req.reported_text,
        image_url=req.photo_url,
        reported_coords=coords,
        district_name=district_info["name"]
    )

    # Fallback coordinates if not provided
    center_lat, center_lon = district_info["center"]
    final_lat = req.lat if req.lat else center_lat + 0.005
    final_lon = req.lon if req.lon else center_lon + 0.005

    new_report = {
        "id": f"rep_{int(time.time())}",
        "district": req.district,
        "author": req.author or "Citizen Responder",
        "location_name": verification.get("extracted_location", "Monitored Sector"),
        "lat": final_lat,
        "lon": final_lon,
        "reported_text": req.reported_text,
        "language": verification.get("language_detected", "English"),
        "english_summary": verification.get("english_translation", req.reported_text),
        "water_depth_cm": verification.get("water_depth_cm_est", 30),
        "status": verification.get("verification_status", "investigating"),
        "urgency": verification.get("urgency", "medium"),
        "requires_boat": verification.get("requires_boat_rescue", False),
        "confidence": verification.get("plausibility_score", 0.8),
        "photo_url": req.photo_url,
        "timestamp": "Just now",
        "source": "Web Citizen Intake Portal",
        "verification_details": verification
    }

    stored = community_report_service.add_report(new_report)
    return {"status": "success", "report": stored}

@app.post("/api/agent/generate-dispatch")
def generate_dispatch(
    district: str = Query("patna"),
    scenario: str = Query("live")
):
    """Generates draft response dispatch priorities using Response Agent."""
    district_cfg = DISTRICTS.get(district, DISTRICTS["patna"])
    weather_data = weather_service.get_weather_and_river(district, scenario)
    geodata = osm_service.get_district_geodata(district)
    
    road_predictions = [
        road_failure_model.predict_segment_failure(seg, weather_data, district_cfg["dem_base_elevation_m"])
        for seg in geodata.get("road_segments", [])
    ]
    isolation_data = isolation_analyzer.analyze_district(geodata, road_predictions)

    plan = response_agent.generate_dispatch_plan(district_cfg["name"], isolation_data, weather_data)
    return {"status": "success", "dispatch_plan": plan}

@app.post("/api/agent/approve-dispatch")
def approve_dispatch(req: ApprovePlanRequest):
    """Human-in-the-loop: District official signs and approves dispatch order."""
    res = response_agent.approve_plan(req.plan_id, req.official_name)
    if res.get("status") == "error":
        raise HTTPException(status_code=404, detail=res.get("message"))
    return res

@app.post("/api/assistant/chat")
def citizen_chat(req: ChatQueryRequest):
    """Citizen Safe-Access conversational assistant."""
    district = req.district if req.district in DISTRICTS else "patna"
    district_cfg = DISTRICTS[district]
    weather_data = weather_service.get_weather_and_river(district, req.scenario or "live")
    geodata = osm_service.get_district_geodata(district)

    road_predictions = [
        road_failure_model.predict_segment_failure(seg, weather_data, district_cfg["dem_base_elevation_m"])
        for seg in geodata.get("road_segments", [])
    ]
    isolation_data = isolation_analyzer.analyze_district(geodata, road_predictions)

    response = citizen_assistant.process_query(req.query, isolation_data, geodata, weather_data)
    return response

class SetApiKeyRequest(BaseModel):
    api_key: str

@app.get("/api/settings/api-key")
def get_api_key_status():
    key = os.environ.get("GEMINI_API_KEY", "")
    masked = f"{key[:6]}...{key[-4:]}" if len(key) > 10 else ("***" if key else "")
    return {
        "is_configured": bool(key),
        "masked_key": masked,
        "engine": "Gemini 2.5 Flash Multimodal" if key else "Built-in Multilingual Heuristic NLP (Fallback)"
    }

@app.post("/api/settings/api-key")
def set_api_key(req: SetApiKeyRequest):
    new_key = req.api_key.strip()
    os.environ["GEMINI_API_KEY"] = new_key
    gemini_verifier.api_key = new_key
    if new_key:
        try:
            from google import genai
            gemini_verifier.client = genai.Client(api_key=new_key)
        except Exception:
            pass
    else:
        gemini_verifier.client = None

    # Persist to .env
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    try:
        lines = []
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        
        found = False
        new_lines = []
        for line in lines:
            if line.strip().startswith("GEMINI_API_KEY="):
                new_lines.append(f"GEMINI_API_KEY={new_key}\n")
                found = True
            else:
                new_lines.append(line)
        if not found:
            new_lines.append(f"\nGEMINI_API_KEY={new_key}\n")

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    except Exception:
        pass

    return {
        "status": "success",
        "is_configured": bool(new_key),
        "message": "API key successfully updated and saved to .env"
    }


# Mount frontend directory for static serving
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_frontend_root():
        index_file = os.path.join(FRONTEND_DIR, "index.html")
        return FileResponse(index_file)
