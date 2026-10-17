import time
from typing import List, Dict, Any

SEED_REPORTS: List[Dict[str, Any]] = [
    {
        "id": "rep_101",
        "district": "patna",
        "author": "Ramesh K. (Ward Resident)",
        "location_name": "Rajendra Nagar Road No. 4 Underpass",
        "lat": 25.5995,
        "lon": 85.1580,
        "reported_text": "कमर तक पानी भर गया है। नालों का पानी उल्टा बह रहा है, गाड़ियां डूब चुकी हैं। कोई भी ऑटो या एम्बुलेंस नहीं आ सकती।",
        "language": "Hindi",
        "english_summary": "Waist-deep water logged at Rajendra Nagar underpass. Drains backing up, vehicles submerged. Ambulances cannot enter.",
        "water_depth_cm": 95,
        "status": "verified",
        "urgency": "critical",
        "requires_boat": True,
        "confidence": 0.94,
        "photo_url": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=400&q=80",
        "timestamp": "12 mins ago",
        "source": "WhatsApp Bot Intake (#91-BiharRelief)"
    },
    {
        "id": "rep_102",
        "district": "patna",
        "author": "Anita Devi (Danapur Diara)",
        "location_name": "Danapur Diara Ghat Sector",
        "lat": 25.6550,
        "lon": 85.0680,
        "reported_text": "गंगा का जलस्तर बहुत तेजी से बढ़ा है, संपर्क मार्ग पूरी तरह कट गया है। प्राथमिक स्वास्थ्य केंद्र तक नाव के बिना जाना नामुमकिन है।",
        "language": "Hindi",
        "english_summary": "Ganga water level surging rapidly, connecting causeway completely cut off. Impossible to reach primary health centre without boats.",
        "water_depth_cm": 110,
        "status": "verified",
        "urgency": "critical",
        "requires_boat": True,
        "confidence": 0.96,
        "photo_url": "https://images.unsplash.com/photo-1514496959998-c01c40915c5f?auto=format&fit=crop&w=400&q=80",
        "timestamp": "28 mins ago",
        "source": "Web Citizen Form"
    },
    {
        "id": "rep_103",
        "district": "patna",
        "author": "Dr. S. K. Jha (PMCH Emergency)",
        "location_name": "JP Ganga Pathway - Ashok Rajpath Entry",
        "lat": 25.6210,
        "lon": 85.1520,
        "reported_text": "Ashok Rajpath has minor waterlogging (15cm), but Marine Drive (JP Ganga Pathway) elevated corridor is clear for trauma ambulances.",
        "language": "English",
        "english_summary": "Ashok Rajpath has minor waterlogging (15cm), elevated JP Ganga Pathway is open for trauma ambulances.",
        "water_depth_cm": 15,
        "status": "verified",
        "urgency": "medium",
        "requires_boat": False,
        "confidence": 0.91,
        "photo_url": None,
        "timestamp": "45 mins ago",
        "source": "Verified Responder App"
    },
    {
        "id": "rep_104",
        "district": "silchar",
        "author": "Debashish Roy (Rangirkhari)",
        "location_name": "Rangirkhari Main Point",
        "lat": 24.8150,
        "lon": 92.8010,
        "reported_text": "বৰাক নদীৰ পানী ৰাস্তালৈ উঠি আহিছে। ৰঙিৰখাৰী পইন্টত আঁঠুৰ ওপৰত পানী।",
        "language": "Assamese",
        "english_summary": "Barak river water has breached the road. Knee-deep water at Rangirkhari point.",
        "water_depth_cm": 55,
        "status": "verified",
        "urgency": "high",
        "requires_boat": False,
        "confidence": 0.89,
        "photo_url": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=400&q=80",
        "timestamp": "18 mins ago",
        "source": "Telegram Bot Intake"
    }
]

class CommunityReportService:
    def __init__(self):
        self.reports: List[Dict[str, Any]] = list(SEED_REPORTS)

    def get_reports_for_district(self, district_id: str) -> List[Dict[str, Any]]:
        return [r for r in self.reports if r.get("district") == district_id]

    def add_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        self.reports.insert(0, report_data)
        return report_data

community_report_service = CommunityReportService()
