"""
Work Shift Safety Model.
Based on TLV/TWA occupational exposure limits (OSHA 29 CFR 1910).
"""
from constants import SHIFT_MAX_MINUTES


def run(exp_score: float, worker_risk: float, hour: float) -> dict:
    """
    Returns dict with keys:
        time_remaining (int, minutes), decision (str), urgency (str)
    """
    exp_factor  = max(0, 1 - exp_score   / 110)
    risk_factor = max(0, 1 - worker_risk / 150)
    hour_factor = max(0, 1 - hour        /  16)
    time_remaining = max(0, round(SHIFT_MAX_MINUTES * exp_factor * risk_factor * hour_factor))
    rotation_due   = time_remaining < 120

    if worker_risk >= 68 or exp_score >= 78:
        decision, urgency = "STOP IMMEDIATELY", "critical"
    elif worker_risk >= 48 or exp_score >= 52 or rotation_due:
        decision, urgency = "ROTATE WORKER",    "warning"
    elif worker_risk >= 30 or exp_score >= 35:
        decision, urgency = "REDUCE EXPOSURE",  "advisory"
    else:
        decision, urgency = "CONTINUE SHIFT",   "safe"

    return {"time_remaining": time_remaining, "decision": decision, "urgency": urgency}
