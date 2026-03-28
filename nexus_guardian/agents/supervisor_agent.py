"""
Supervisor AI Agent.
Aggregates all risk vectors with priority weighting.
Single critical reading can override combined score.
"""
from constants import RISK_WEIGHTS


def run(machine_risk: float, worker_risk: float, exp_score: float) -> dict:
    """
    Returns dict with keys:
        status (str), color_key (str), explanation (str), combined_score (float)
    """
    w        = RISK_WEIGHTS["supervisor"]
    combined = machine_risk * w["machine"] + worker_risk * w["worker"] + exp_score * w["exposure"]
    max_single = max(machine_risk, worker_risk, exp_score)
    if max_single >= 80:
        combined = max(combined, max_single * 0.92)
    combined = round(combined, 1)

    if combined < 28:
        status, color, exp_text = (
            "ALL SYSTEMS NOMINAL", "safe",
            "All risk vectors within acceptable limits. Operations may continue at full capacity. Next review in 4 hours.")
    elif combined < 48:
        status, color, exp_text = (
            "ELEVATED ADVISORY", "warning",
            "Cross-agent analysis detects moderate stress accumulation. Recommend supervisor walkthrough within 90 minutes.")
    elif combined < 68:
        status, color, exp_text = (
            "ROTATION REQUIRED", "rotate",
            "Worker physiological strain approaching threshold. Initiate shift rotation. Machine inspection recommended before next cycle.")
    else:
        status, color, exp_text = (
            "EMERGENCY STOP", "critical",
            "CRITICAL: Combined risk exceeds emergency threshold. Activate plant emergency protocol. Evacuate affected zones. Contact safety officer immediately.")

    return {"status": status, "color_key": color, "explanation": exp_text, "combined_score": combined}
