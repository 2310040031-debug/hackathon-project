"""
Single source of truth for column names, industry metadata, worker roster,
and safety thresholds. Import from here — never hardcode elsewhere.
"""

REQUIRED_COLS = {
    "facility", "category", "temperature", "gas_ppm",
    "noise_db", "radiation", "heart_rate", "fatigue", "hour"
}

SENSOR_COLS = ["temperature", "gas_ppm", "noise_db", "radiation", "heart_rate", "fatigue", "hour"]

INDUSTRY_DATA = {
    "Petrochemical": {
        "icon": "⚗️",
        "companies": "Reliance, HPCL, BPCL, Indian Oil, ONGC",
        "desc": "Refineries, crackers, storage units — high temp/pressure/VOC environments",
        "color": "#ff6b35",
        "hazards": ["Benzene (carcinogen)", "H₂S", "Process heat", "Pressure vessels"]
    },
    "Pharmaceutical": {
        "icon": "💊",
        "companies": "Cipla, Sigachi, Sun Pharma, Dr. Reddy's, Aurobindo",
        "desc": "API synthesis, solvent handling, sterile manufacturing, cytotoxic drugs",
        "color": "#00d4ff",
        "hazards": ["Cytotoxic agents", "Organic solvents", "API dust", "Ionising radiation (sterilisation)"]
    }
}

WORKERS = [
    {"id": "W-001", "name": "Rajesh Kumar",  "role": "Reactor Operator",   "shift_start": "06:00", "hours_in": 6.2},
    {"id": "W-002", "name": "Priya Nair",    "role": "QC Analyst",         "shift_start": "06:00", "hours_in": 6.2},
    {"id": "W-003", "name": "Amir Shaikh",   "role": "Maintenance Tech",   "shift_start": "06:00", "hours_in": 6.2},
    {"id": "W-004", "name": "Sunita Reddy",  "role": "Process Engineer",   "shift_start": "14:00", "hours_in": 2.1},
    {"id": "W-005", "name": "Vikram Singh",  "role": "Safety Officer",     "shift_start": "06:00", "hours_in": 6.2},
    {"id": "W-006", "name": "Meera Pillai",  "role": "API Synthesis Lead", "shift_start": "06:00", "hours_in": 6.2},
]

THRESHOLDS = {
    "temperature": {"limit": 85,  "unit": "°C",    "warn": 60,  "danger": 80},
    "gas_ppm":     {"limit": 200, "unit": "ppm",   "warn": 80,  "danger": 150},
    "noise_db":    {"limit": 90,  "unit": "dB",    "warn": 82,  "danger": 88},
    "radiation":   {"limit": 1.0, "unit": "mSv/h", "warn": 0.3, "danger": 0.6},
    "heart_rate":  {"limit": 110, "unit": "BPM",   "warn": 90,  "danger": 105},
    "fatigue":     {"limit": 70,  "unit": "/100",  "warn": 45,  "danger": 70},
}

SHIFT_MAX_MINUTES = 480  # 8-hour shift

RISK_WEIGHTS = {
    "supervisor": {"machine": 0.33, "worker": 0.42, "exposure": 0.25},
    "machine":    {"temperature": 0.30, "gas": 0.32, "noise": 0.18, "radiation": 0.20},
    "worker":     {"heart_rate": 0.28, "fatigue": 0.38, "exposure": 0.26, "radiation_penalty": 0.08},
}
