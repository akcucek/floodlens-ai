import os
from typing import Dict, Any

DISTRICTS: Dict[str, Dict[str, Any]] = {
    # ==================== ASSAM & NORTH-EAST (Brahmaputra & Barak) ====================
    "silchar": {
        "id": "silchar",
        "name": "Cachar (Silchar), Assam",
        "region_zone": "North-East (Barak Basin)",
        "river": "Barak River Basin",
        "state": "Assam",
        "center": [24.8333, 92.7789],
        "zoom": 12,
        "bbox": [24.78, 92.72, 24.89, 92.86],
        "cwc_gauge_station": "Annapurna Ghat, Silchar",
        "danger_level_m": 19.83,
        "warning_level_m": 18.83,
        "current_gauge_m_baseline": 17.40,
        "dem_base_elevation_m": 22.0,
        "annual_flood_frequency": "Annual Severe"
    },
    "guwahati": {
        "id": "guwahati",
        "name": "Kamrup Metro (Guwahati), Assam",
        "region_zone": "North-East (Brahmaputra Basin)",
        "river": "Brahmaputra River Basin",
        "state": "Assam",
        "center": [26.1445, 91.7362],
        "zoom": 12,
        "bbox": [26.08, 91.65, 26.22, 91.85],
        "cwc_gauge_station": "Guwahati DC Court Ghat",
        "danger_level_m": 49.68,
        "warning_level_m": 48.68,
        "current_gauge_m_baseline": 47.10,
        "dem_base_elevation_m": 55.0,
        "annual_flood_frequency": "Annual Regular"
    },
    "dhemaji": {
        "id": "dhemaji",
        "name": "Dhemaji & Lakhimpur, Assam",
        "region_zone": "North-East (Subansiri & Jiadhal)",
        "river": "Jiadhal & Subansiri Basins",
        "state": "Assam",
        "center": [27.4833, 94.5833],
        "zoom": 11,
        "bbox": [27.35, 94.40, 27.65, 94.75],
        "cwc_gauge_station": "Kumotia / Jiadhal Gauge Point",
        "danger_level_m": 105.40,
        "warning_level_m": 104.20,
        "current_gauge_m_baseline": 101.80,
        "dem_base_elevation_m": 104.0,
        "annual_flood_frequency": "Extreme Flash Floods"
    },
    "dibrugarh": {
        "id": "dibrugarh",
        "name": "Dibrugarh & Majuli, Assam",
        "region_zone": "North-East (Upper Brahmaputra)",
        "river": "Upper Brahmaputra & Dihing",
        "state": "Assam",
        "center": [27.4728, 94.9120],
        "zoom": 12,
        "bbox": [27.38, 94.80, 27.56, 95.05],
        "cwc_gauge_station": "Dibrugarh Town Protection Dyke",
        "danger_level_m": 105.70,
        "warning_level_m": 104.70,
        "current_gauge_m_baseline": 103.20,
        "dem_base_elevation_m": 108.0,
        "annual_flood_frequency": "High Riverine Inundation"
    },

    # ==================== BIHAR (Ganga, Kosi, Bagmati & Gandak) ====================
    "patna": {
        "id": "patna",
        "name": "Patna District, Bihar",
        "region_zone": "Ganga Plains (Bihar)",
        "river": "Ganga, Son & Punpun Basins",
        "state": "Bihar",
        "center": [25.5941, 85.1376],
        "zoom": 12,
        "bbox": [25.53, 85.02, 25.68, 85.25],
        "cwc_gauge_station": "Gandhi Ghat, Patna",
        "danger_level_m": 48.60,
        "warning_level_m": 47.60,
        "current_gauge_m_baseline": 46.20,
        "dem_base_elevation_m": 53.0,
        "annual_flood_frequency": "High Urban Inundation"
    },
    "darbhanga": {
        "id": "darbhanga",
        "name": "Darbhanga & Madhubani, Bihar",
        "region_zone": "Mithila Basin (Bagmati & Kamla)",
        "river": "Bagmati, Kamla Balan & Adhwara",
        "state": "Bihar",
        "center": [26.1542, 85.8918],
        "zoom": 12,
        "bbox": [26.05, 85.78, 26.25, 86.02],
        "cwc_gauge_station": "Hayaghat / Kamla Balan Rail Bridge",
        "danger_level_m": 45.72,
        "warning_level_m": 44.72,
        "current_gauge_m_baseline": 43.10,
        "dem_base_elevation_m": 49.0,
        "annual_flood_frequency": "Severe Recurrent"
    },
    "bhagalpur": {
        "id": "bhagalpur",
        "name": "Bhagalpur & Katihar, Bihar",
        "region_zone": "Ganga & Kosi Confluence",
        "river": "Ganga & Kosi Rivers",
        "state": "Bihar",
        "center": [25.2425, 86.9842],
        "zoom": 12,
        "bbox": [25.15, 86.88, 25.35, 87.10],
        "cwc_gauge_station": "Colgong / Kahalgaon Ganga Gauge",
        "danger_level_m": 31.09,
        "warning_level_m": 30.09,
        "current_gauge_m_baseline": 28.90,
        "dem_base_elevation_m": 41.0,
        "annual_flood_frequency": "Severe Inundation & Erosion"
    },
    "muzaffarpur": {
        "id": "muzaffarpur",
        "name": "Muzaffarpur & Sitamarhi, Bihar",
        "region_zone": "Gandak Basin (North Bihar)",
        "river": "Burhi Gandak & Bagmati",
        "state": "Bihar",
        "center": [26.1209, 85.3647],
        "zoom": 12,
        "bbox": [26.02, 85.25, 26.22, 85.48],
        "cwc_gauge_station": "Sikandarpur Burhi Gandak Station",
        "danger_level_m": 52.53,
        "warning_level_m": 51.53,
        "current_gauge_m_baseline": 49.80,
        "dem_base_elevation_m": 56.0,
        "annual_flood_frequency": "Annual High"
    },

    # ==================== ODISHA (Mahanadi, Brahmani & Baitarani) ====================
    "cuttack": {
        "id": "cuttack",
        "name": "Cuttack & Kendrapara, Odisha",
        "region_zone": "Eastern Delta (Mahanadi)",
        "river": "Mahanadi & Kathajodi Delta",
        "state": "Odisha",
        "center": [20.4625, 85.8828],
        "zoom": 12,
        "bbox": [20.38, 85.78, 20.55, 85.98],
        "cwc_gauge_station": "Naraj Barrage, Cuttack",
        "danger_level_m": 26.41,
        "warning_level_m": 25.41,
        "current_gauge_m_baseline": 23.80,
        "dem_base_elevation_m": 30.0,
        "annual_flood_frequency": "Severe Cyclone & River Surge"
    },
    "puri": {
        "id": "puri",
        "name": "Puri & Kanas Basin, Odisha",
        "region_zone": "Coastal Lagoon & Rivers (Odisha)",
        "river": "Bhargavi, Daya & Kushabhadra",
        "state": "Odisha",
        "center": [19.8135, 85.8312],
        "zoom": 12,
        "bbox": [19.75, 85.75, 19.92, 85.95],
        "cwc_gauge_station": "Achhutpur / Bhargavi Gauge",
        "danger_level_m": 11.20,
        "warning_level_m": 10.20,
        "current_gauge_m_baseline": 8.50,
        "dem_base_elevation_m": 7.0,
        "annual_flood_frequency": "Coastal Inundation & Breaches"
    },

    # ==================== KERALA (Western Ghats & Coastal Deluge) ====================
    "wayanad": {
        "id": "wayanad",
        "name": "Wayanad (Meppadi / Kalpetta), Kerala",
        "region_zone": "Western Ghats Flash Flood Zone",
        "river": "Kabini & Chaliyar Basins",
        "state": "Kerala",
        "center": [11.6054, 76.0830],
        "zoom": 12,
        "bbox": [11.50, 76.00, 11.70, 76.18],
        "cwc_gauge_station": "Muthanga / Kalpetta Stream Gauge",
        "danger_level_m": 65.00,
        "warning_level_m": 62.50,
        "current_gauge_m_baseline": 58.00,
        "dem_base_elevation_m": 780.0,
        "annual_flood_frequency": "Flash Floods & Debris Flow"
    },
    "ernakulam": {
        "id": "ernakulam",
        "name": "Ernakulam & Aluva, Kerala",
        "region_zone": "Central Kerala (Periyar Basin)",
        "river": "Periyar & Muvattupuzha Rivers",
        "state": "Kerala",
        "center": [10.1076, 76.3516],
        "zoom": 12,
        "bbox": [10.02, 76.25, 10.18, 76.45],
        "cwc_gauge_station": "Aluva Manappuram Periyar Gauge",
        "danger_level_m": 3.50,
        "warning_level_m": 2.50,
        "current_gauge_m_baseline": 1.40,
        "dem_base_elevation_m": 8.0,
        "annual_flood_frequency": "Dam Overflow & Estuarine Deluge"
    },
    "alappuzha": {
        "id": "alappuzha",
        "name": "Alappuzha & Kuttanad, Kerala",
        "region_zone": "Below-Sea-Level Backwaters (Kuttanad)",
        "river": "Pamba, Manimala & Achenkovil",
        "state": "Kerala",
        "center": [9.4981, 76.3388],
        "zoom": 12,
        "bbox": [9.40, 76.25, 9.60, 76.45],
        "cwc_gauge_station": "Pallathuruthy Vembanad Gauge",
        "danger_level_m": 1.60,
        "warning_level_m": 1.20,
        "current_gauge_m_baseline": 0.85,
        "dem_base_elevation_m": 1.0,
        "annual_flood_frequency": "Prolonged Submersion"
    },

    # ==================== MAHARASHTRA (Panchganga, Krishna, Konkan) ====================
    "kolhapur": {
        "id": "kolhapur",
        "name": "Kolhapur & Sangli, Maharashtra",
        "region_zone": "Upper Krishna & Panchganga Basin",
        "river": "Panchganga & Krishna Basins",
        "state": "Maharashtra",
        "center": [16.7050, 74.2433],
        "zoom": 12,
        "bbox": [16.62, 74.15, 16.78, 74.35],
        "cwc_gauge_station": "Rajaram Barrage, Kolhapur",
        "danger_level_m": 43.00,
        "warning_level_m": 39.00,
        "current_gauge_m_baseline": 32.00,
        "dem_base_elevation_m": 560.0,
        "annual_flood_frequency": "Severe Inundation / Dam Backwater"
    },
    "mumbai": {
        "id": "mumbai",
        "name": "Mumbai Metropolitan Region, Maharashtra",
        "region_zone": "Western Coast Urban Flood Basin",
        "river": "Mithi, Dahisar & Ulhas Rivers",
        "state": "Maharashtra",
        "center": [19.0760, 72.8777],
        "zoom": 12,
        "bbox": [18.98, 72.80, 19.18, 72.98],
        "cwc_gauge_station": "Kurla / BKC Mithi River Sensor",
        "danger_level_m": 4.20,
        "warning_level_m": 3.30,
        "current_gauge_m_baseline": 1.80,
        "dem_base_elevation_m": 8.0,
        "annual_flood_frequency": "Extreme Urban Flash Deluge"
    },

    # ==================== UTTAR PRADESH (Ganga, Rapti, Yamuna) ====================
    "gorakhpur": {
        "id": "gorakhpur",
        "name": "Gorakhpur & Deoria, Uttar Pradesh",
        "region_zone": "Terai & Rapti Basin",
        "river": "Rapti, Rohini & Ghaghra",
        "state": "Uttar Pradesh",
        "center": [26.7606, 83.3732],
        "zoom": 12,
        "bbox": [26.68, 83.28, 26.85, 83.48],
        "cwc_gauge_station": "Birdghat Rapti River Station",
        "danger_level_m": 74.98,
        "warning_level_m": 73.98,
        "current_gauge_m_baseline": 71.50,
        "dem_base_elevation_m": 84.0,
        "annual_flood_frequency": "Annual Terai Inundation"
    },
    "varanasi": {
        "id": "varanasi",
        "name": "Varanasi District, Uttar Pradesh",
        "region_zone": "Middle Ganga Basin",
        "river": "Ganga & Varuna Rivers",
        "state": "Uttar Pradesh",
        "center": [25.3176, 82.9739],
        "zoom": 12,
        "bbox": [25.24, 82.88, 25.40, 83.08],
        "cwc_gauge_station": "Mirzapur / Rajghat Varanasi Gauge",
        "danger_level_m": 71.26,
        "warning_level_m": 70.26,
        "current_gauge_m_baseline": 66.80,
        "dem_base_elevation_m": 76.0,
        "annual_flood_frequency": "Riverine Flood Plain"
    },

    # ==================== WEST BENGAL (Ganga, Shilabati, Teesta) ====================
    "murshidabad": {
        "id": "murshidabad",
        "name": "Murshidabad & Malda, West Bengal",
        "region_zone": "Lower Ganga / Bhagirathi Basin",
        "river": "Bhagirathi, Jalangi & Ganga",
        "state": "West Bengal",
        "center": [24.1750, 88.2800],
        "zoom": 12,
        "bbox": [24.05, 88.18, 24.28, 88.38],
        "cwc_gauge_station": "Berhampore Bhagirathi Gauge",
        "danger_level_m": 18.00,
        "warning_level_m": 16.50,
        "current_gauge_m_baseline": 14.20,
        "dem_base_elevation_m": 19.0,
        "annual_flood_frequency": "Bank Erosion & Inundation"
    },
    "medinipur": {
        "id": "medinipur",
        "name": "Ghatal & Paschim Medinipur, West Bengal",
        "region_zone": "Rupnarayan & Shilabati (Ghatal Basin)",
        "river": "Shilabati & Rupnarayan Basins",
        "state": "West Bengal",
        "center": [22.6667, 87.7167],
        "zoom": 12,
        "bbox": [22.56, 87.60, 22.78, 87.85],
        "cwc_gauge_station": "Ghatal Circuit Embankment Gauge",
        "danger_level_m": 13.50,
        "warning_level_m": 12.00,
        "current_gauge_m_baseline": 9.80,
        "dem_base_elevation_m": 12.0,
        "annual_flood_frequency": "Chronic Annual Flooding"
    },

    # ==================== GUJARAT (Tapi & Narmada) ====================
    "surat": {
        "id": "surat",
        "name": "Surat District, Gujarat",
        "region_zone": "Western Peninsular (Tapi Basin)",
        "river": "Tapi River & Ukai Dam Basin",
        "state": "Gujarat",
        "center": [21.1702, 72.8311],
        "zoom": 12,
        "bbox": [21.08, 72.75, 21.28, 72.95],
        "cwc_gauge_station": "Hope Bridge Tapi River Gauge",
        "danger_level_m": 9.50,
        "warning_level_m": 8.00,
        "current_gauge_m_baseline": 5.20,
        "dem_base_elevation_m": 13.0,
        "annual_flood_frequency": "High Inundation on Dam Release"
    },

    # ==================== ANDHRA PRADESH (Godavari & Krishna Delta) ====================
    "godavari": {
        "id": "godavari",
        "name": "East Godavari (Rajahmundry), Andhra Pradesh",
        "region_zone": "Godavari Delta & Konaseema",
        "river": "Godavari River Basin",
        "state": "Andhra Pradesh",
        "center": [17.0005, 81.8040],
        "zoom": 12,
        "bbox": [16.90, 81.70, 17.12, 81.92],
        "cwc_gauge_station": "Dowleswaram Barrage, Rajahmundry",
        "danger_level_m": 14.75,
        "warning_level_m": 13.75,
        "current_gauge_m_baseline": 11.20,
        "dem_base_elevation_m": 14.0,
        "annual_flood_frequency": "Delta Surge & Island Habitations"
    },

    # ==================== TAMIL NADU (Coromandel Urban Floods) ====================
    "chennai": {
        "id": "chennai",
        "name": "Chennai Metropolitan Area, Tamil Nadu",
        "region_zone": "Coromandel Coastal River Basin",
        "river": "Adyar, Cooum & Kosasthalaiyar",
        "state": "Tamil Nadu",
        "center": [13.0827, 80.2707],
        "zoom": 12,
        "bbox": [12.96, 80.15, 13.18, 80.32],
        "cwc_gauge_station": "Chembarambakkam / Maraimalai Adyar Outfall",
        "danger_level_m": 18.50,
        "warning_level_m": 16.80,
        "current_gauge_m_baseline": 11.00,
        "dem_base_elevation_m": 6.0,
        "annual_flood_frequency": "Cyclone & Cloudburst Urban Surge"
    },

    # ==================== HIMALAYAN FLASH FLOOD & CLOUDBURST ZONES ====================
    "kullu_mandi": {
        "id": "kullu_mandi",
        "name": "Kullu & Mandi, Himachal Pradesh",
        "region_zone": "Himalayan Flash Flood (Beas River)",
        "river": "Beas & Parbati Basins",
        "state": "Himachal Pradesh",
        "center": [31.9579, 77.1095],
        "zoom": 11,
        "bbox": [31.80, 76.95, 32.10, 77.25],
        "cwc_gauge_station": "Pandoh Dam / Mandi Beas Gauge",
        "danger_level_m": 850.00,
        "warning_level_m": 845.00,
        "current_gauge_m_baseline": 830.00,
        "dem_base_elevation_m": 1220.0,
        "annual_flood_frequency": "Torrential Mountain Flash Deluge"
    },
    "srinagar": {
        "id": "srinagar",
        "name": "Srinagar Valley, Jammu & Kashmir",
        "region_zone": "Kashmir Valley (Jhelum Basin)",
        "river": "Jhelum River & Dal Catchment",
        "state": "Jammu & Kashmir",
        "center": [34.0837, 74.7973],
        "zoom": 12,
        "bbox": [33.98, 74.70, 34.18, 74.92],
        "cwc_gauge_station": "Ram Munshi Bagh Gauge, Srinagar",
        "danger_level_m": 6.40,
        "warning_level_m": 5.48,
        "current_gauge_m_baseline": 3.80,
        "dem_base_elevation_m": 1585.0,
        "annual_flood_frequency": "Glacial & Basin Inundation"
    }
}

# Automatically load .env file if present
ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
if os.path.exists(ENV_PATH):
    try:
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and v:
                        os.environ[k] = v
    except Exception:
        pass

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_FLOOD_URL = "https://flood-api.open-meteo.com/v1/flood"

