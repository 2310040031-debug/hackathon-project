"""
Cumulative Bio-Exposure Model.
Based on NIOSH/OSHA dose-response curves (TLV/TWA methodology).
Radiation dose follows ICRP 103 framework.
"""


def run(rad: float, gas: float, temp: float, current_score: float, time_weight: float = 0.10) -> dict:
    """
    Accumulates dose across shift ticks.
    Returns dict with keys: score (float 0-100), level (str)
    """
    rad_dose  = rad * 18
    chem_dose = (gas / 250) * 28
    heat_dose = max(0, (temp - 28) / 64) * 12
    delta     = (rad_dose + chem_dose + heat_dose) * time_weight
    score     = round(min(100, current_score + delta), 2)
    level     = ("MINIMAL"  if score < 20 else
                 "LOW"      if score < 40 else
                 "MODERATE" if score < 65 else "HIGH")
    return {"score": score, "level": level}
