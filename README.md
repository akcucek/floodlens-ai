# FloodLens AI

FloodLens AI is a flood-monitoring and disaster-response intelligence platform designed to support local authorities, emergency teams, and public responders during monsoon and flood emergencies. The system integrates live environmental data, district-level flood risk information, geospatial infrastructure analysis, and AI-assisted decision support to improve situational awareness and response planning.

https://floodlens-854681872487.us-central1.run.app/

## Overview

The platform analyzes weather conditions, river discharge, gauge levels, and flood alerts to assess the current risk state of selected districts. It also evaluates road network vulnerability, identifying roads likely to fail or become unusable during heavy rainfall or rising water levels. By combining this with network-based isolation analysis, the system can highlight communities that may become disconnected from hospitals, shelters, or safe routes during flooding events.

A key feature of FloodLens AI is its ability to ingest community-submitted flood reports from citizens, including local text descriptions and image-based evidence. These reports are processed and verified with AI support to estimate severity, water depth, urgency, and possible rescue needs. This creates a faster feedback loop between affected communities and response authorities.

The project includes a FastAPI backend, a front-end dashboard, and modular data and intelligence services. It is built to be extensible, allowing future integration with satellite imagery, real-time government alert feeds, historical flood patterns, and advanced routing or optimization models.

Overall, FloodLens AI acts as a decision-support system for flood preparedness and emergency management, helping users understand risk, identify vulnerable areas, prioritize response actions, and communicate safe-access guidance effectively in critical situations.

![Uploading image.png…]()


## Key capabilities

- Flood intelligence analysis by district
- Weather and river/discharge monitoring
- Alert integration for flood scenarios
- Road-failure prediction using geospatial and hydrological signals
- Network-based isolation analysis to surface cut-off communities
- Safe-access routing and response prioritization
- Community report intake with multilingual text processing
- Citizen-facing assistant for local safe-access guidance
- FastAPI backend with a lightweight frontend dashboard

## Architecture

- `backend/` — FastAPI API, data sources, intelligence models, and agent logic
- `frontend/` — static dashboard assets and UI
- `run.py` — server entrypoint for starting the application
- `.env.example` — sample environment configuration
- `requirements.txt` — Python dependencies

## Tech stack

- Python
- FastAPI
- Uvicorn
- NetworkX
- Pydantic
- Open-Meteo / GloFAS-style stream integrations

## Getting started

### 1. Clone the project

```bash
git clone <repository-url>
cd floodlens-ai
```

### 2. Create environment variables

Copy the sample environment file and update values if needed:

```bash
cp .env.example .env
```

Useful variables:

- `PORT` — app port, default `8000`

### 3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Start the server

```bash
python run.py
```

The application will run on:

- API server: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`
- Dashboard: `http://127.0.0.1:8000/`

## Example API endpoints

- `GET /api/districts`
- `GET /api/flood-intelligence`
- `POST /api/reports/submit`
- `POST /api/agent/generate-dispatch`
- `POST /api/assistant/chat`

## District coverage

The app includes flood-prone district configurations across several regions, including:

- Assam / North-East
- Bihar
- Odisha
- Kerala

## Notes

- The project is intended for simulation, monitoring, and planning workflows rather than direct regulatory or operational deployment without review.

## License

This project does not currently declare a license. If you plan to distribute or reuse it, add an appropriate open-source license before public release.
