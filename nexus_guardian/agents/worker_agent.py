"""
Worker Health AI Agent.
Physiological + exposure cross-correlation model.
"""
from constants import RISK_WEIGHTS


def run(hr: float, fatigue: float, exp_score: float, machine_risk: float) -> dict:
    """
    Returns dict with keys: score (float 0-100), status (str), recommendation (str)
    """
    eff_fatigue = min(100, fatigue + exp_score * 0.28 + machine_risk * 0.12)
    hr_sc       = min(100, max(0, (hr - 60) / 72 * 100))
    rad_penalty = min(20, exp_score * 0.2)

    w     = RISK_WEIGHTS["worker"]
    score = (hr_sc * w["heart_rate"] + eff_fatigue * w["fatigue"] +
             exp_score * w["exposure"] + rad_penalty * w["radiation_penalty"])

    if hr > 105 and exp_score > 50: score = min(100, score + 14)
    if exp_score > 65:              score = min(100, score + 10)
    if fatigue > 70 and hr > 95:   score = min(100, score + 8)

    score = round(min(100, score), 1)

    if score < 33:
        status = "FIT";      rec = "Worker in excellent condition. No restrictions required."
    elif score < 55:
        status = "CAUTION";  rec = "Early fatigue/stress indicators. Increase hydration breaks. Monitor every 30 min."
    elif score < 72:
        status = "AT RISK";  rec = "Significant physiological strain. Reassign to low-exposure zone immediately."
    else:
        status = "CRITICAL"; rec = "Dangerous health state. Immediate removal from hazardous area. Medical evaluation required."

    return {"score": score, "status": status, "recommendation": rec}
