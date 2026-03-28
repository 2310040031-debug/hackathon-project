"""
Machine Health AI Agent.
Weighted multi-parameter risk scoring with compound pattern detection.
Standards: OSHA 29 CFR 1910, NIOSH RELs.
"""
from constants import RISK_WEIGHTS


def run(temp: float, gas: float, noise: float, rad: float) -> dict:
    """
    Returns a dict with keys:
        score (float 0-100), status (str), recommendation (str),
        patterns (str), breakdown (dict[str, float])
    """
    t_sc = min(100, max(0, (temp  - 18) / 74  * 100))
    g_sc = min(100, max(0,  gas        / 250  * 100))
    n_sc = min(100, max(0, (noise - 58) / 50  * 100))
    r_sc = min(100, max(0,  rad        / 2.0  * 100))

    w = RISK_WEIGHTS["machine"]
    base = t_sc * w["temperature"] + g_sc * w["gas"] + n_sc * w["noise"] + r_sc * w["radiation"]

    patterns = []
    if temp > 75 and noise > 88:
        base = min(100, base + 14); patterns.append("mechanical overload signature")
    if gas > 100 and temp > 65:
        base = min(100, base + 16); patterns.append("exothermic reaction / leak risk")
    if rad > 0.4:
        base = min(100, base + 12); patterns.append("hazardous radiation zone")
    if gas > 60 and noise > 85 and temp > 70:
        base = min(100, base + 10); patterns.append("multi-hazard convergence")

    score = round(min(100, base), 1)

    if score < 33:
        status = "OPTIMAL";  rec = "Equipment operating within nominal parameters. Scheduled maintenance on track."
    elif score < 55:
        status = "ADVISORY"; rec = "Minor deviations noted. Increase sensor polling and schedule inspection within 48 h."
    elif score < 72:
        status = "WARNING";  rec = "Significant stress indicators. Reduce throughput by 20% and alert maintenance team."
    else:
        status = "CRITICAL"; rec = "Immediate risk of equipment failure. Initiate emergency shutdown protocol NOW."

    return {
        "score":          score,
        "status":         status,
        "recommendation": rec,
        "patterns":       "; ".join(patterns) if patterns else "No anomalous patterns detected",
        "breakdown":      {"Temperature": t_sc, "Gas/VOC": g_sc, "Vibration/Noise": n_sc, "Radiation": r_sc},
    }
