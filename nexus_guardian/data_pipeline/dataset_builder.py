"""
Synthetic sensor data generator.
Profiles are modelled on published occupational health data for
petrochemical (refinery) and pharmaceutical (API manufacturing) plants.
Sources: OSHA PELs, NIOSH RELs, WHO radiation guidelines.
"""
import math
import random
import pandas as pd

PROFILES = [
    # (name, category, base_temp, base_gas_ppm, base_rad_mSv, base_hr, risk_profile)
    ("Distillation Column",   "Petrochemical",  78,  45, 0.08, 82, "rising"),
    ("Catalytic Cracker",     "Petrochemical",  85,  80, 0.12, 88, "high"),
    ("Hydrodesulfurization",  "Petrochemical",  72, 120, 0.09, 85, "high"),
    ("LPG Storage Unit",      "Petrochemical",  42,  25, 0.05, 76, "moderate"),
    ("Crude Distillation",    "Petrochemical",  68,  60, 0.10, 80, "rising"),
    ("API Synthesis Reactor", "Pharmaceutical", 55,  35, 0.06, 78, "moderate"),
    ("Solvent Recovery Unit", "Pharmaceutical", 48,  90, 0.04, 80, "rising"),
    ("Tablet Coating Room",   "Pharmaceutical", 38,  15, 0.03, 72, "normal"),
    ("Sterile Fill & Finish", "Pharmaceutical", 22,   8, 0.02, 70, "normal"),
    ("Cytotoxic Drug Lab",    "Pharmaceutical", 25,  12, 0.15, 75, "high"),
    ("Fermentation Suite",    "Pharmaceutical", 35,  20, 0.03, 73, "normal"),
    ("Solvent Storage",       "Pharmaceutical", 30,  70, 0.04, 76, "moderate"),
]

RISK_MULS = {
    "normal":   (1.0, 1.0, 1.0, 1.0, 0.05),
    "moderate": (1.2, 1.3, 1.2, 1.1, 0.15),
    "rising":   (1.4, 1.6, 1.3, 1.2, 0.25),
    "high":     (1.8, 2.2, 1.8, 1.4, 0.40),
}


def build_dataset(seed: int = 2024, ticks: int = 160) -> pd.DataFrame:
    """Generate synthetic sensor readings for all facility profiles."""
    random.seed(seed)
    rows = []

    for name, category, bt, bg, br, bhr, rtype in PROFILES:
        temp_mul, gas_mul, rad_mul, hr_mul, trend = RISK_MULS[rtype]

        for i in range(ticks):
            t     = i / (ticks - 1)
            wave  = math.sin(t * 2 * math.pi)
            wave2 = math.sin(t * 4 * math.pi + 1.2)

            rows.append({
                "facility":    name,
                "category":    category,
                "temperature": round(max(18,  min(92,  bt  * temp_mul + 6  * wave  * trend * bt  + random.gauss(0, 1.2))), 1),
                "gas_ppm":     round(max(0,   min(280, bg  * gas_mul  + 12 * wave2 * trend * bg  + random.gauss(0, 2.5))), 1),
                "noise_db":    round(max(58,  min(108, 70  + 10 * trend + 5 * wave + random.gauss(0, 1.5))),               1),
                "radiation":   round(max(0,   min(2.5, br  * rad_mul  + 0.04 * wave * trend       + random.gauss(0, 0.005))), 4),
                "heart_rate":  round(max(62,  min(132, bhr * hr_mul   + 8  * wave  * trend        + random.gauss(0, 2.0))), 1),
                "fatigue":     round(max(5,   min(95,  8   + 45 * t * trend * 2 + 10 * wave2 * 0.3 + random.gauss(0, 2))), 1),
                "hour":        round(i / ticks * 12, 2),
            })

    return pd.DataFrame(rows)
