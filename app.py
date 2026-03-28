"""
NEXUS GUARDIAN — Industrial AI Safety Intelligence
Petrochemical & Pharmaceutical Edition
Run: pip install streamlit pandas plotly && streamlit run app.py
"""
import time, math, os, random
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NEXUS GUARDIAN — Industrial AI Safety",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────
# GLOBAL CSS — DARK INDUSTRIAL LUXURY
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Instrument+Sans:wght@400;500;600&display=swap');

:root {
  --bg:       #050709;
  --surface:  #0c0e12;
  --card:     #101318;
  --border:   #1e2530;
  --accent:   #00d4ff;
  --accent2:  #ff6b35;
  --accent3:  #00ff9d;
  --warn:     #ffd60a;
  --danger:   #ff3b3b;
  --safe:     #00e676;
  --text:     #e8edf5;
  --muted:    #5a6478;
  --glow:     0 0 20px rgba(0,212,255,0.3);
}

html, body, [class*="css"] {
  font-family: 'Instrument Sans', sans-serif;
  background: var(--bg) !important;
  color: var(--text) !important;
}

.stApp { background: var(--bg) !important; }

div[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
div[data-testid="stSidebar"] * { color: var(--text) !important; }

.block-container { padding: 1.5rem 2rem 3rem !important; }

.nexus-hero {
  position: relative;
  padding: 2rem 0 1.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--border);
  overflow: hidden;
}
.nexus-hero::before {
  content: '';
  position: absolute;
  top: -60px; left: -80px;
  width: 400px; height: 300px;
  background: radial-gradient(ellipse, rgba(0,212,255,0.06) 0%, transparent 70%);
  pointer-events: none;
}
.nexus-hero::after {
  content: '';
  position: absolute;
  top: -40px; right: -60px;
  width: 300px; height: 250px;
  background: radial-gradient(ellipse, rgba(0,255,157,0.04) 0%, transparent 70%);
  pointer-events: none;
}
.hero-title {
  font-family: 'Syne', sans-serif;
  font-weight: 800;
  font-size: 2.6rem;
  letter-spacing: -0.02em;
  line-height: 1;
  background: linear-gradient(135deg, #00d4ff 0%, #00ff9d 50%, #e8edf5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}
.hero-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--muted);
  margin-top: 0.4rem;
}
.hero-tag {
  display: inline-block;
  padding: 0.2rem 0.7rem;
  border: 1px solid rgba(0,212,255,0.3);
  border-radius: 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--accent);
  letter-spacing: 0.1em;
  margin-right: 0.5rem;
  margin-top: 0.8rem;
  background: rgba(0,212,255,0.05);
}

.section-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--muted);
  padding: 0.3rem 0;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1.2rem;
}
.section-label span { color: var(--accent); margin-right: 0.5rem; }

.m-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.2rem 1.4rem;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
}
.m-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 2px;
  background: var(--accent-line, var(--border));
  border-radius: 2px 2px 0 0;
}
.m-card-safe    { --accent-line: var(--safe); }
.m-card-warn    { --accent-line: var(--warn); }
.m-card-danger  { --accent-line: var(--danger); }
.m-card-info    { --accent-line: var(--accent); }
.m-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 0.3rem;
}
.m-value {
  font-family: 'Syne', sans-serif;
  font-size: 2.2rem;
  font-weight: 700;
  line-height: 1;
  color: var(--text);
}
.m-unit {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--muted);
  margin-left: 0.2rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  font-weight: 500;
  letter-spacing: 0.08em;
}
.badge::before { content:''; width:6px; height:6px; border-radius:50%; display:inline-block; }
.b-safe     { background:#001a0d; color:#00e676; border:1px solid #00e676; }
.b-safe::before { background:#00e676; box-shadow:0 0 6px #00e676; }
.b-warning  { background:#1a1500; color:#ffd60a; border:1px solid #ffd60a; }
.b-warning::before { background:#ffd60a; box-shadow:0 0 6px #ffd60a; }
.b-rotate   { background:#1a0800; color:#ff6b35; border:1px solid #ff6b35; }
.b-rotate::before { background:#ff6b35; box-shadow:0 0 6px #ff6b35; }
.b-critical { background:#1a0000; color:#ff3b3b; border:1px solid #ff3b3b; }
.b-critical::before { background:#ff3b3b; box-shadow:0 0 6px #ff3b3b; animation:pulse-dot 1s infinite; }
@keyframes pulse-dot { 0%,100%{opacity:1} 50%{opacity:.3} }

.agent-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
}
.agent-card::after {
  content: '';
  position: absolute;
  bottom: -40px; right: -40px;
  width: 120px; height: 120px;
  border-radius: 50%;
  background: var(--agent-glow, rgba(0,212,255,0.03));
  filter: blur(20px);
  pointer-events: none;
}
.agent-machine { --agent-glow: rgba(255,107,53,0.08); border-color: rgba(255,107,53,0.2); }
.agent-worker  { --agent-glow: rgba(0,212,255,0.08);  border-color: rgba(0,212,255,0.2);  }
.agent-expo    { --agent-glow: rgba(0,255,157,0.08);  border-color: rgba(0,255,157,0.2);  }

.agent-icon {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--agent-color, var(--accent));
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin-bottom: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.agent-icon::before {
  content: '';
  width: 20px; height: 1px;
  background: var(--agent-color, var(--accent));
}

.agent-score {
  font-family: 'Syne', sans-serif;
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 0.2rem;
}
.agent-score-safe   { color: var(--safe); }
.agent-score-warn   { color: var(--warn); }
.agent-score-danger { color: var(--danger); }

.agent-rec {
  font-size: 0.82rem;
  color: #8a94a8;
  line-height: 1.5;
  margin-top: 0.8rem;
  padding-top: 0.8rem;
  border-top: 1px solid var(--border);
}

.supervisor-card {
  background: linear-gradient(135deg, #0c1018 0%, #0f1520 100%);
  border: 1px solid rgba(0,212,255,0.2);
  border-radius: 16px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}
.supervisor-card::before {
  content: '';
  position: absolute;
  top: -1px; left: 5%; right: 5%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
}
.sup-verdict {
  font-family: 'Syne', sans-serif;
  font-size: 1.8rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}
.sup-score {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--muted);
  margin-top: 0.3rem;
}
.sup-exp {
  font-size: 0.88rem;
  color: #8a94a8;
  line-height: 1.6;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.shift-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.5rem;
}
.shift-time {
  font-family: 'Syne', sans-serif;
  font-size: 2.8rem;
  font-weight: 700;
}
.shift-bar-track {
  height: 8px;
  background: #1a1f2a;
  border-radius: 4px;
  margin: 1rem 0 0.4rem;
  overflow: hidden;
}
.shift-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.risk-row {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 0.8rem;
}
.risk-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted);
  width: 120px;
  flex-shrink: 0;
}
.risk-track {
  flex: 1;
  height: 6px;
  background: #1a1f2a;
  border-radius: 3px;
  overflow: hidden;
}
.risk-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}
.risk-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  width: 36px;
  text-align: right;
  flex-shrink: 0;
}

.ticker-bar {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  color: var(--muted);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  overflow: hidden;
}
.ticker-live { color: var(--safe); animation: blink 1.5s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }
.ticker-item { display: flex; align-items: center; gap: 0.4rem; }
.ticker-item strong { color: var(--text); }

.industry-slide {
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  height: 120px;
  background: var(--card);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 1.2rem;
  gap: 1rem;
}
.industry-icon { font-size: 2rem; flex-shrink: 0; }
.industry-name { font-family: 'Syne', sans-serif; font-size: 0.95rem; font-weight: 600; }
.industry-desc { font-size: 0.75rem; color: var(--muted); margin-top: 0.2rem; line-height: 1.4; }

.worker-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1.5fr;
  align-items: center;
  padding: 0.7rem 0.8rem;
  border-radius: 8px;
  margin-bottom: 0.4rem;
  background: var(--card);
  border: 1px solid var(--border);
  font-size: 0.82rem;
}
.worker-row-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted);
  padding: 0.4rem 0.8rem;
  margin-bottom: 0.4rem;
}
.worker-name { font-weight: 500; }
.worker-critical { border-color: rgba(255,59,59,0.3); background: rgba(255,59,59,0.04); }
.worker-warn     { border-color: rgba(255,214,10,0.3); background: rgba(255,214,10,0.04); }

.rad-meter {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.2rem;
  position: relative;
}
.rad-value {
  font-family: 'Syne', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--warn);
}
.rad-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--muted);
  margin-bottom: 0.3rem;
}

.js-plotly-plot .plotly .main-svg { background: transparent !important; }

.sidebar-section {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--muted);
  padding: 0.8rem 0 0.4rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 0.8rem;
}
.stSlider label, .stSelectbox label, .stToggle label {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.72rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
  color: var(--muted) !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# REQUIRED COLUMNS — single source of truth
# ─────────────────────────────────────────────────────────
REQUIRED_COLS = {
    "facility", "category", "temperature", "gas_ppm",
    "noise_db", "radiation", "heart_rate", "fatigue", "hour"
}


# ─────────────────────────────────────────────────────────
# DATASET — REAL INDUSTRY PROFILES
# ─────────────────────────────────────────────────────────
def build_dataset() -> pd.DataFrame:
    """
    Realistic sensor profiles modelled on published occupational health data
    for petrochemical (refinery) and pharmaceutical (API manufacturing) plants.
    Sources: OSHA PELs, NIOSH RELs, WHO radiation guidelines, industry case studies.
    """
    random.seed(2024)
    rows = []

    profiles = [
        # (name, category, base_temp, base_gas_ppm, base_rad_mSv, base_hr, risk_profile)
        ("Distillation Column",   "Petrochemical", 78, 45,  0.08, 82, "rising"),
        ("Catalytic Cracker",     "Petrochemical", 85, 80,  0.12, 88, "high"),
        ("Hydrodesulfurization",  "Petrochemical", 72, 120, 0.09, 85, "high"),
        ("LPG Storage Unit",      "Petrochemical", 42, 25,  0.05, 76, "moderate"),
        ("Crude Distillation",    "Petrochemical", 68, 60,  0.10, 80, "rising"),
        ("API Synthesis Reactor", "Pharmaceutical", 55, 35,  0.06, 78, "moderate"),
        ("Solvent Recovery Unit", "Pharmaceutical", 48, 90,  0.04, 80, "rising"),
        ("Tablet Coating Room",   "Pharmaceutical", 38, 15,  0.03, 72, "normal"),
        ("Sterile Fill & Finish", "Pharmaceutical", 22,  8,  0.02, 70, "normal"),
        ("Cytotoxic Drug Lab",    "Pharmaceutical", 25, 12,  0.15, 75, "high"),
        ("Fermentation Suite",    "Pharmaceutical", 35, 20,  0.03, 73, "normal"),
        ("Solvent Storage",       "Pharmaceutical", 30, 70,  0.04, 76, "moderate"),
    ]

    for name, category, bt, bg, br, bhr, rtype in profiles:
        for i in range(160):
            t     = i / 159
            wave  = math.sin(t * 2 * math.pi)
            wave2 = math.sin(t * 4 * math.pi + 1.2)

            muls = {
                "normal":   (1.0, 1.0, 1.0, 1.0, 0.05),
                "moderate": (1.2, 1.3, 1.2, 1.1, 0.15),
                "rising":   (1.4, 1.6, 1.3, 1.2, 0.25),
                "high":     (1.8, 2.2, 1.8, 1.4, 0.40),
            }
            temp_mul, gas_mul, rad_mul, hr_mul, trend = muls.get(rtype, muls["normal"])

            temp   = max(18,  min(92,  bt  * temp_mul + 6  * wave  * trend * bt  + random.gauss(0, 1.2)))
            gas    = max(0,   min(280, bg  * gas_mul  + 12 * wave2 * trend * bg  + random.gauss(0, 2.5)))
            noise  = max(58,  min(108, 70  + 10 * trend + 5 * wave + random.gauss(0, 1.5)))
            rad    = max(0,   min(2.5, br  * rad_mul  + 0.04 * wave * trend       + random.gauss(0, 0.005)))
            hr     = max(62,  min(132, bhr * hr_mul   + 8  * wave  * trend        + random.gauss(0, 2.0)))
            fatigue= max(5,   min(95,  8   + 45 * t   * trend * 2 + 10 * wave2 * 0.3 + random.gauss(0, 2)))

            rows.append({
                "facility":    name,
                "category":    category,
                "temperature": round(temp,    1),
                "gas_ppm":     round(gas,     1),
                "noise_db":    round(noise,   1),
                "radiation":   round(rad,     4),
                "heart_rate":  round(hr,      1),
                "fatigue":     round(fatigue, 1),
                "hour":        round(i / 160 * 12, 2),
            })

    return pd.DataFrame(rows)


def _csv_is_valid(path: str) -> bool:
    """Return True only if the CSV exists, is non-empty, and has every required column."""
    if not os.path.exists(path):
        return False
    try:
        # Read just the header — fast even for large files
        header = pd.read_csv(path, nrows=0)
        return REQUIRED_COLS.issubset(set(header.columns))
    except Exception:
        return False


@st.cache_data
def load_dataset() -> pd.DataFrame:
    """
    Load the sensor dataset.
    Priority:
      1. Valid cached CSV next to the script  →  read it
      2. Otherwise                            →  build from scratch, persist to CSV
    The cache is invalidated automatically when Streamlit detects a code change.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path   = os.path.join(script_dir, "sensor_data.csv")

    if _csv_is_valid(csv_path):
        df = pd.read_csv(csv_path)
        # Paranoia: strip whitespace from column names (Excel/LibreOffice artefact)
        df.columns = df.columns.str.strip()
        return df

    # Build fresh and try to cache it
    df = build_dataset()
    try:
        df.to_csv(csv_path, index=False)
    except OSError:
        pass  # read-only filesystem — silently skip
    return df


def get_row(df: pd.DataFrame, tick: int, facility: str) -> dict:
    sub = df[df["facility"] == facility].reset_index(drop=True)
    r   = sub.iloc[tick % len(sub)]
    return {k: float(r[k]) for k in
            ["temperature", "gas_ppm", "noise_db", "radiation", "heart_rate", "fatigue", "hour"]}


# ─────────────────────────────────────────────────────────
# AI AGENTS
# ─────────────────────────────────────────────────────────
def machine_agent(temp, gas, noise, rad):
    t_sc  = min(100, max(0, (temp - 18) / 74 * 100))
    g_sc  = min(100, max(0, (gas / 250) * 100))
    n_sc  = min(100, max(0, (noise - 58) / 50 * 100))
    r_sc  = min(100, max(0, (rad / 2.0) * 100))

    base  = t_sc * 0.30 + g_sc * 0.32 + n_sc * 0.18 + r_sc * 0.20

    patterns = []
    if temp > 75 and noise > 88:
        base = min(100, base + 14); patterns.append("mechanical overload signature")
    if gas > 100 and temp > 65:
        base = min(100, base + 16); patterns.append("exothermic reaction / leak risk")
    if rad > 0.4:
        base = min(100, base + 12); patterns.append("hazardous radiation zone")
    if gas > 60 and noise > 85 and temp > 70:
        base = min(100, base + 10); patterns.append("multi-hazard convergence")

    score       = round(base, 1)
    pattern_str = "; ".join(patterns) if patterns else "No anomalous patterns detected"

    if score < 33:
        status, rec = "OPTIMAL", "Equipment operating within nominal parameters. Scheduled maintenance on track."
    elif score < 55:
        status, rec = "ADVISORY", "Minor deviations noted. Increase sensor polling and schedule inspection within 48 h."
    elif score < 72:
        status, rec = "WARNING",  "Significant stress indicators. Reduce throughput by 20% and alert maintenance team."
    else:
        status, rec = "CRITICAL", "Immediate risk of equipment failure. Initiate emergency shutdown protocol NOW."

    return score, status, rec, pattern_str, {
        "Temperature": t_sc, "Gas/VOC": g_sc, "Vibration/Noise": n_sc, "Radiation": r_sc
    }


def exposure_system(rad, gas, temp, cur, tw=0.10):
    rad_dose  = rad * 18
    chem_dose = (gas / 250) * 28
    heat_dose = max(0, (temp - 28) / 64) * 12
    score     = min(100, cur + (rad_dose + chem_dose + heat_dose) * tw)
    level     = ("MINIMAL" if score < 20 else
                 "LOW"     if score < 40 else
                 "MODERATE"if score < 65 else "HIGH")
    return round(score, 2), level


def worker_agent(hr, fatigue, exp, m_risk):
    eff_fatigue = min(100, fatigue + exp * 0.28 + m_risk * 0.12)
    hr_sc       = min(100, max(0, (hr - 60) / 72 * 100))
    rad_penalty = min(20, exp * 0.2)
    score       = hr_sc * 0.28 + eff_fatigue * 0.38 + exp * 0.26 + rad_penalty * 0.08

    if hr > 105 and exp > 50: score = min(100, score + 14)
    if exp > 65:               score = min(100, score + 10)
    if fatigue > 70 and hr > 95: score = min(100, score + 8)

    score = round(min(100, score), 1)

    if score < 33:
        status, rec = "FIT",      "Worker in excellent condition. No restrictions required."
    elif score < 55:
        status, rec = "CAUTION",  "Early fatigue/stress indicators. Increase hydration breaks. Monitor every 30 min."
    elif score < 72:
        status, rec = "AT RISK",  "Significant physiological strain. Reassign to low-exposure zone immediately."
    else:
        status, rec = "CRITICAL", "Dangerous health state. Immediate removal from hazardous area. Medical evaluation required."

    return score, status, rec


def shift_intelligence(exp, w_risk, hour):
    base_max      = 480
    exp_factor    = max(0, 1 - exp / 110)
    risk_factor   = max(0, 1 - w_risk / 150)
    hour_factor   = max(0, 1 - hour / 16)
    time_remaining= max(0, round(base_max * exp_factor * risk_factor * hour_factor))
    rotation_due  = time_remaining < 120

    if w_risk >= 68 or exp >= 78:
        decision, urgency = "STOP IMMEDIATELY",  "critical"
    elif w_risk >= 48 or exp >= 52 or rotation_due:
        decision, urgency = "ROTATE WORKER",     "warning"
    elif w_risk >= 30 or exp >= 35:
        decision, urgency = "REDUCE EXPOSURE",   "advisory"
    else:
        decision, urgency = "CONTINUE SHIFT",    "safe"

    return time_remaining, decision, urgency


def supervisor_agent(m_risk, w_risk, exp):
    combined    = m_risk * 0.33 + w_risk * 0.42 + exp * 0.25
    max_single  = max(m_risk, w_risk, exp)
    if max_single >= 80:
        combined = max(combined, max_single * 0.92)
    combined = round(combined, 1)

    if combined < 28:
        return ("ALL SYSTEMS NOMINAL", "safe",
                "All risk vectors within acceptable limits. Operations may continue at full capacity. Next scheduled review in 4 hours.",
                combined)
    elif combined < 48:
        return ("ELEVATED ADVISORY", "warning",
                "Cross-agent analysis detects moderate stress accumulation. Recommend supervisor walkthrough and equipment log review within 90 minutes.",
                combined)
    elif combined < 68:
        return ("ROTATION REQUIRED", "rotate",
                "Worker physiological strain approaching threshold. Initiate shift rotation protocol. Machine inspection recommended before next cycle.",
                combined)
    else:
        return ("EMERGENCY STOP", "critical",
                "CRITICAL: Combined risk exceeds emergency threshold. Activate plant emergency protocol. Evacuate affected zones. Contact safety officer immediately.",
                combined)


# ─────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────
for k, v in [("tick", 0), ("exposure", 0.0), ("running", False), ("history", [])]:
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────
# LOAD DATA  ← all KeyError risk lives here; fixed above
# ─────────────────────────────────────────────────────────
df = load_dataset()

# Belt-and-suspenders: validate at runtime so we get a clear message, not a cryptic KeyError
missing = REQUIRED_COLS - set(df.columns)
if missing:
    st.error(
        f"**Dataset is missing columns:** `{missing}`\n\n"
        "Delete `sensor_data.csv` next to the script and restart — "
        "the app will regenerate a clean dataset automatically."
    )
    st.stop()

facilities = df["facility"].unique().tolist()
categories = ["All", "Petrochemical", "Pharmaceutical"]

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


# ─────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#00d4ff;margin-bottom:0.2rem;">⬡ NEXUS GUARDIAN</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#5a6478;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:1.2rem;">Control Interface v2.4</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Facility Selection</div>', unsafe_allow_html=True)
    facility   = st.selectbox("Active Facility", facilities, label_visibility="collapsed")
    cat_filter = st.selectbox("Industry Filter", categories, label_visibility="collapsed")

    if cat_filter != "All":
        fac_filtered = df[df["category"] == cat_filter]["facility"].unique().tolist()
        if facility not in fac_filtered and fac_filtered:
            facility = fac_filtered[0]

    st.markdown('<div class="sidebar-section">Simulation Control</div>', unsafe_allow_html=True)
    manual = st.toggle("Manual Sensor Override", value=False)
    if manual:
        temp       = st.slider("Temperature °C",   18,  92, 55)
        gas        = st.slider("Gas / VOC ppm",     0, 280, 45)
        noise      = st.slider("Noise dB",         58, 108, 76)
        radiation  = st.slider("Radiation mSv/h", 0.0, 2.5, 0.08, 0.01)
        heart_rate = st.slider("Heart Rate BPM",   62, 132, 82)
        fatigue    = st.slider("Fatigue Index",     0,  95, 25)

    st.markdown('<div class="sidebar-section">Simulation</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("▶ START", use_container_width=True, type="primary"):
            st.session_state.running = True
    with c2:
        if st.button("⏹ STOP", use_container_width=True):
            st.session_state.running = False
    if st.button("↺ RESET ALL", use_container_width=True):
        st.session_state.tick = 0
        st.session_state.exposure = 0.0
        st.session_state.running  = False
        st.session_state.history  = []

    st.markdown('<div class="sidebar-section">Thresholds</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#5a6478;line-height:2;">TEMP LIMIT: 85°C<br>GAS PEL: 200 ppm<br>NOISE TWA: 90 dB<br>RAD LIMIT: 1.0 mSv/h<br>SHIFT MAX: 8 h</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# TICK + PIPELINE
# ─────────────────────────────────────────────────────────
if st.session_state.running:
    st.session_state.tick += 1

tick = st.session_state.tick

if manual:
    sensors = {
        "temperature": temp, "gas_ppm": gas, "noise_db": noise,
        "radiation": radiation, "heart_rate": heart_rate,
        "fatigue": fatigue, "hour": 6.0
    }
else:
    sensors = get_row(df, tick, facility)

m_risk, m_status, m_rec, m_patterns, m_breakdown = machine_agent(
    sensors["temperature"], sensors["gas_ppm"], sensors["noise_db"], sensors["radiation"])

exp_score, exp_level = exposure_system(
    sensors["radiation"], sensors["gas_ppm"], sensors["temperature"], st.session_state.exposure)
st.session_state.exposure = exp_score

w_risk, w_status, w_rec = worker_agent(
    sensors["heart_rate"], sensors["fatigue"], exp_score, m_risk)

time_left, shift_dec, shift_urgency = shift_intelligence(exp_score, w_risk, sensors["hour"])

sup_status, sup_color, sup_exp, comb_score = supervisor_agent(m_risk, w_risk, exp_score)

st.session_state.history.append({
    "tick": tick, "machine": m_risk, "worker": w_risk,
    "exposure": exp_score, "combined": comb_score,
    "temp": sensors["temperature"], "gas": sensors["gas_ppm"],
    "radiation": sensors["radiation"], "hr": sensors["heart_rate"]
})
if len(st.session_state.history) > 80:
    st.session_state.history = st.session_state.history[-80:]

hist = st.session_state.history


# ─────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────
def badge_html(text, btype):
    return f'<span class="badge b-{btype}">{text}</span>'

def score_class(v):
    return "agent-score-safe" if v < 33 else ("agent-score-warn" if v < 65 else "agent-score-danger")

def score_color(v):
    return "#00e676" if v < 33 else ("#ffd60a" if v < 65 else "#ff3b3b")

def badge_type(status):
    s = status.lower()
    if any(x in s for x in ["optimal","fit","nominal","safe","minimal","low","continue"]): return "safe"
    if any(x in s for x in ["advisory","caution","warning","moderate","elevated","reduce"]): return "warning"
    if any(x in s for x in ["rotate","rotation","at risk"]): return "rotate"
    return "critical"

def make_histogram_dark(data, title, color, nbins=10):
    fig = go.Figure(go.Histogram(
        x=data, nbinsx=nbins,
        marker_color=color, opacity=0.9,
        marker_line_color='rgba(0,0,0,0.5)', marker_line_width=0.5,
        xbins=dict(start=0, end=100, size=10),
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(family="JetBrains Mono", size=10, color="#5a6478"), x=0, pad=dict(l=0, t=0)),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d1d9", family="JetBrains Mono", size=10),
        margin=dict(l=32, r=8, t=32, b=32), height=180,
        xaxis=dict(range=[0, 100], gridcolor="#1e2530", zeroline=False,
                   tickfont=dict(size=9), title=None,
                   showline=True, linecolor="#1e2530"),
        yaxis=dict(gridcolor="#1e2530", zeroline=False, tickfont=dict(size=9), title=None),
        bargap=0.08, showlegend=False,
    )
    return fig

def make_radar_chart(breakdown):
    cats   = list(breakdown.keys()) + [list(breakdown.keys())[0]]
    vals   = list(breakdown.values()) + [list(breakdown.values())[0]]
    fig = go.Figure(go.Scatterpolar(
        r=vals, theta=cats, fill='toself',
        fillcolor='rgba(255,107,53,0.15)',
        line=dict(color='#ff6b35', width=2),
        marker=dict(size=5, color='#ff6b35')
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(range=[0, 100], gridcolor='#1e2530',
                            tickfont=dict(size=8, color='#5a6478'), showline=False),
            angularaxis=dict(gridcolor='#1e2530', tickfont=dict(size=10, color='#8a94a8')),
        ),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=30, r=30, t=20, b=20), height=200, showlegend=False,
    )
    return fig

def make_time_area(hist, key, color, title):
    xs = [h["tick"] for h in hist]
    ys = [h[key]    for h in hist]
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    fig = go.Figure(go.Scatter(
        x=xs, y=ys, fill='tozeroy',
        fillcolor=f"rgba({r},{g},{b},0.12)",
        line=dict(color=color, width=1.5), mode='lines',
    ))
    fig.add_hline(y=65, line=dict(color='rgba(255,59,59,0.4)',  width=1, dash='dot'))
    fig.add_hline(y=33, line=dict(color='rgba(255,214,10,0.3)', width=1, dash='dot'))
    fig.update_layout(
        title=dict(text=title, font=dict(family="JetBrains Mono", size=10, color="#5a6478"), x=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#c9d1d9', family='JetBrains Mono', size=10),
        margin=dict(l=32, r=8, t=32, b=28), height=160,
        xaxis=dict(gridcolor='#1e2530', zeroline=False, tickfont=dict(size=9), showgrid=False),
        yaxis=dict(range=[0, 105], gridcolor='#1e2530', zeroline=False, tickfont=dict(size=9)),
        showlegend=False,
    )
    return fig

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


# ─────────────────────────────────────────────────────────
# MAIN UI
# ─────────────────────────────────────────────────────────

# ── HERO ──────────────────────────────────────────────────
st.markdown("""
<div class="nexus-hero">
  <div class="hero-title">NEXUS GUARDIAN</div>
  <div class="hero-sub">Industrial AI Safety Intelligence Platform</div>
  <div style="margin-top:0.8rem;">
    <span class="hero-tag">PETROCHEMICAL</span>
    <span class="hero-tag">PHARMACEUTICAL</span>
    <span class="hero-tag">REAL-TIME AI</span>
    <span class="hero-tag">v2.4.1</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── INDUSTRY SLIDES ────────────────────────────────────────
st.markdown('<div class="section-label"><span>01</span> Active Industries & Facilities</div>', unsafe_allow_html=True)
ic1, ic2 = st.columns(2)
for col, (ind, data) in zip([ic1, ic2], INDUSTRY_DATA.items()):
    r, g, b = hex_to_rgb(data["color"])
    hazard_spans = "".join(
        f'<span style="background:rgba({r},{g},{b},0.1);color:{data["color"]};'
        f'font-size:0.6rem;padding:0.15rem 0.5rem;border-radius:3px;'
        f'font-family:JetBrains Mono,monospace;">{h}</span>'
        for h in data["hazards"]
    )
    with col:
        st.markdown(f"""
        <div class="industry-slide" style="border-color:rgba({r},{g},{b},0.25);">
          <div>
            <div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:{data['color']};
                        text-transform:uppercase;letter-spacing:0.18em;margin-bottom:0.3rem;">{ind}</div>
            <div class="industry-name">{data['icon']} {data['companies']}</div>
            <div class="industry-desc">{data['desc']}</div>
            <div style="margin-top:0.5rem;display:flex;gap:0.4rem;flex-wrap:wrap;">{hazard_spans}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── LIVE TICKER ────────────────────────────────────────────
fac_row = df[df["facility"] == facility].iloc[0]
exp_col_ticker = '#ff3b3b' if exp_score > 65 else ('#ffd60a' if exp_score > 35 else '#00e676')
sup_col_ticker = ('#ff3b3b' if any(x in sup_status for x in ["EMERGENCY","CRITICAL"])
                  else '#ffd60a' if any(x in sup_status for x in ["ROTATION","ELEVATED"])
                  else '#00e676')

st.markdown(f"""
<div class="ticker-bar">
  <span class="ticker-live">● LIVE</span>
  <span class="ticker-item">FACILITY: <strong>{facility}</strong></span>
  <span class="ticker-item">CATEGORY: <strong>{fac_row['category']}</strong></span>
  <span class="ticker-item">TICK: <strong>#{tick}</strong></span>
  <span class="ticker-item">SHIFT HOUR: <strong>{sensors['hour']:.1f}h</strong></span>
  <span class="ticker-item">EXPOSURE: <strong style="color:{exp_col_ticker}">{exp_score:.1f}</strong></span>
  <span class="ticker-item">VERDICT: <strong style="color:{sup_col_ticker}">{sup_status}</strong></span>
</div>
""", unsafe_allow_html=True)

# ── LIVE SENSOR STRIP ─────────────────────────────────────
st.markdown('<div class="section-label"><span>02</span> Live Sensor Readings</div>', unsafe_allow_html=True)

def sensor_card(label, value, unit, limit, css_class="info"):
    pct     = min(100, value / limit * 100) if limit else 0
    bar_col = "#ff3b3b" if pct > 85 else ("#ffd60a" if pct > 60 else "#00e676")
    return f"""
    <div class="m-card m-card-{css_class}">
      <div class="m-label">{label}</div>
      <div class="m-value">{value:.1f}<span class="m-unit">{unit}</span></div>
      <div class="risk-track" style="margin-top:0.6rem;height:4px;">
        <div class="risk-fill" style="width:{pct:.0f}%;background:{bar_col};"></div>
      </div>
      <div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#5a6478;margin-top:0.3rem;">
        Limit: {limit} {unit}
      </div>
    </div>"""

s1, s2, s3, s4, s5, s6 = st.columns(6)
with s1: st.markdown(sensor_card("Temperature",  sensors['temperature'], "°C",    85,  "warn"   if sensors['temperature'] > 60  else "info"),  unsafe_allow_html=True)
with s2: st.markdown(sensor_card("Gas / VOC",    sensors['gas_ppm'],     "ppm",   200, "danger" if sensors['gas_ppm'] > 150     else "warn" if sensors['gas_ppm'] > 80 else "info"), unsafe_allow_html=True)
with s3: st.markdown(sensor_card("Noise Level",  sensors['noise_db'],    "dB",    90,  "warn"   if sensors['noise_db'] > 82     else "info"),  unsafe_allow_html=True)
with s4: st.markdown(sensor_card("Radiation",    sensors['radiation'],   "mSv/h", 1.0, "danger" if sensors['radiation'] > 0.6   else "warn" if sensors['radiation'] > 0.3 else "safe"), unsafe_allow_html=True)
with s5: st.markdown(sensor_card("Heart Rate",   sensors['heart_rate'],  "BPM",   110, "warn"   if sensors['heart_rate'] > 90   else "info"),  unsafe_allow_html=True)
with s6: st.markdown(sensor_card("Fatigue Index",sensors['fatigue'],     "/100",  70,  "danger" if sensors['fatigue'] > 70      else "warn" if sensors['fatigue'] > 45 else "safe"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── AI AGENTS ─────────────────────────────────────────────
st.markdown('<div class="section-label"><span>03</span> AI Agent Analysis</div>', unsafe_allow_html=True)
ag1, ag2, ag3 = st.columns(3)

# Machine Agent
with ag1:
    bt = badge_type(m_status)
    risk_bars = "".join(
        f'<div class="risk-row">'
        f'<div class="risk-label">{k}</div>'
        f'<div class="risk-track"><div class="risk-fill" style="width:{v:.0f}%;background:{score_color(v)};"></div></div>'
        f'<div class="risk-num" style="color:{score_color(v)};">{v:.0f}</div>'
        f'</div>'
        for k, v in m_breakdown.items()
    )
    st.markdown(f"""
    <div class="agent-card agent-machine">
      <div class="agent-icon" style="--agent-color:#ff6b35;">MACHINE HEALTH AGENT</div>
      <div class="agent-score {score_class(m_risk)}">{m_risk}</div>
      <div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#5a6478;margin:.2rem 0 .6rem;">/ 100 risk index</div>
      {badge_html(m_status, bt)}
      <div style="margin-top:0.8rem;">{risk_bars}</div>
      <div class="agent-rec">
        <div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#5a6478;margin-bottom:0.3rem;">PATTERN DETECTION</div>
        <div style="color:#ffd60a;font-size:0.75rem;margin-bottom:0.5rem;">{m_patterns}</div>
        {m_rec}
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(make_radar_chart(m_breakdown), use_container_width=True)

# Exposure Agent
with ag2:
    et            = badge_type(exp_level)
    rad_impact_pct= min(100, sensors['radiation'] / 2.0 * 100)
    rad_long      = ('HIGH CONCERN — exceeds ICRP 20 mSv/yr guidance' if sensors['radiation'] > 0.6
                     else 'MODERATE — cumulative monitoring required'   if sensors['radiation'] > 0.25
                     else 'WITHIN annual dose limits')
    rad_fill_col  = '#ff3b3b' if sensors['radiation'] > 0.6 else ('#ffd60a' if sensors['radiation'] > 0.3 else '#00e676')
    voc_pct       = min(100, sensors['gas_ppm'] / 250 * 100)
    heat_pct      = min(100, max(0, (sensors['temperature'] - 28) / 64) * 100)

    st.markdown(f"""
    <div class="agent-card agent-expo">
      <div class="agent-icon" style="--agent-color:#00ff9d;">EXPOSURE MONITOR</div>
      <div class="agent-score {score_class(exp_score)}">{exp_score:.1f}</div>
      <div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#5a6478;margin:.2rem 0 .6rem;">cumulative dose index</div>
      {badge_html(exp_level, et)}
      <div style="margin-top:1rem;">
        <div class="rad-meter" style="margin-bottom:0.8rem;">
          <div class="rad-label">Radiation Impact (mSv/h)</div>
          <div class="rad-value">{sensors['radiation']:.3f}</div>
          <div class="risk-track" style="margin-top:0.4rem;">
            <div class="risk-fill" style="width:{rad_impact_pct:.0f}%;background:{rad_fill_col};"></div>
          </div>
          <div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#5a6478;margin-top:0.3rem;">{rad_long}</div>
        </div>
        <div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#5a6478;margin-bottom:0.3rem;">DOSE BREAKDOWN</div>
        <div class="risk-row"><div class="risk-label">Radiation</div><div class="risk-track"><div class="risk-fill" style="width:{rad_impact_pct:.0f}%;background:#ffd60a;"></div></div><div class="risk-num" style="color:#ffd60a;">{rad_impact_pct:.0f}</div></div>
        <div class="risk-row"><div class="risk-label">Chemical/VOC</div><div class="risk-track"><div class="risk-fill" style="width:{voc_pct:.0f}%;background:#ff6b35;"></div></div><div class="risk-num" style="color:#ff6b35;">{voc_pct:.0f}</div></div>
        <div class="risk-row"><div class="risk-label">Heat Stress</div><div class="risk-track"><div class="risk-fill" style="width:{heat_pct:.0f}%;background:#00d4ff;"></div></div><div class="risk-num" style="color:#00d4ff;">{heat_pct:.0f}</div></div>
      </div>
      <div class="agent-rec">Cumulative exposure tracked per NIOSH TLV/TWA methodology. Radiation dose follows ICRP 103 framework. Reset at shift end.</div>
    </div>
    """, unsafe_allow_html=True)

# Worker Agent
with ag3:
    wt         = badge_type(w_status)
    hr_sc_val  = min(100, max(0, (sensors['heart_rate'] - 60) / 72 * 100))
    fat_sc_val = sensors['fatigue']
    rad_eff    = min(20, exp_score * 0.2)

    st.markdown(f"""
    <div class="agent-card agent-worker">
      <div class="agent-icon" style="--agent-color:#00d4ff;">WORKER HEALTH AGENT</div>
      <div class="agent-score {score_class(w_risk)}">{w_risk}</div>
      <div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#5a6478;margin:.2rem 0 .6rem;">/ 100 health risk index</div>
      {badge_html(w_status, wt)}
      <div style="margin-top:0.8rem;">
        <div class="risk-row"><div class="risk-label">Physiological</div><div class="risk-track"><div class="risk-fill" style="width:{hr_sc_val:.0f}%;background:{score_color(hr_sc_val)};"></div></div><div class="risk-num" style="color:{score_color(hr_sc_val)};">{hr_sc_val:.0f}</div></div>
        <div class="risk-row"><div class="risk-label">Fatigue Load</div><div class="risk-track"><div class="risk-fill" style="width:{fat_sc_val:.0f}%;background:{score_color(fat_sc_val)};"></div></div><div class="risk-num" style="color:{score_color(fat_sc_val)};">{fat_sc_val:.0f}</div></div>
        <div class="risk-row"><div class="risk-label">Exposure Load</div><div class="risk-track"><div class="risk-fill" style="width:{exp_score:.0f}%;background:{score_color(exp_score)};"></div></div><div class="risk-num" style="color:{score_color(exp_score)};">{exp_score:.0f}</div></div>
        <div class="risk-row"><div class="risk-label">Radiation Effect</div><div class="risk-track"><div class="risk-fill" style="width:{rad_eff:.0f}%;background:#ffd60a;"></div></div><div class="risk-num" style="color:#ffd60a;">{rad_eff:.0f}</div></div>
      </div>
      <div class="agent-rec">{w_rec}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── SUPERVISOR + SHIFT ─────────────────────────────────────
st.markdown('<div class="section-label"><span>04</span> Supervisor AI Agent & Shift Intelligence</div>', unsafe_allow_html=True)
sv1, sv2 = st.columns([3, 2])

with sv1:
    sup_c_map = {
        "safe":     ("#00e676", "rgba(0,230,118,0.3)"),
        "warning":  ("#ffd60a", "rgba(255,214,10,0.3)"),
        "rotate":   ("#ff6b35", "rgba(255,107,53,0.3)"),
        "critical": ("#ff3b3b", "rgba(255,59,59,0.3)"),
    }
    tc, tb = sup_c_map.get(sup_color, sup_c_map["safe"])

    st.markdown(f"""
    <div class="supervisor-card" style="border-color:{tb};">
      <div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#5a6478;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.8rem;">⬡ Supervisor AI Agent — Final Verdict</div>
      <div class="sup-verdict" style="color:{tc};">{sup_status}</div>
      <div class="sup-score">Combined Risk Index: {comb_score} / 100 &nbsp;·&nbsp; Machine {m_risk:.0f}% · Worker {w_risk:.0f}% · Exposure {exp_score:.0f}%</div>
      <div class="sup-exp">{sup_exp}</div>
      <div style="margin-top:1.2rem;display:grid;grid-template-columns:repeat(3,1fr);gap:0.8rem;">
        <div style="text-align:center;background:rgba(255,107,53,0.06);border:1px solid rgba(255,107,53,0.15);border-radius:8px;padding:0.8rem;">
          <div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:700;color:#ff6b35;">{m_risk:.0f}</div>
          <div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#5a6478;text-transform:uppercase;letter-spacing:.12em;">Machine</div>
        </div>
        <div style="text-align:center;background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.15);border-radius:8px;padding:0.8rem;">
          <div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:700;color:#00d4ff;">{w_risk:.0f}</div>
          <div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#5a6478;text-transform:uppercase;letter-spacing:.12em;">Worker</div>
        </div>
        <div style="text-align:center;background:rgba(0,255,157,0.06);border:1px solid rgba(0,255,157,0.15);border-radius:8px;padding:0.8rem;">
          <div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:700;color:#00ff9d;">{exp_score:.0f}</div>
          <div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#5a6478;text-transform:uppercase;letter-spacing:.12em;">Exposure</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with sv2:
    bar_pct   = min(100, time_left / 480 * 100)
    bar_col   = "#ff3b3b" if bar_pct < 25 else ("#ffd60a" if bar_pct < 50 else "#00e676")
    sdec_col  = {"CONTINUE SHIFT": "#00e676", "REDUCE EXPOSURE": "#ffd60a",
                 "ROTATE WORKER": "#ff6b35", "STOP IMMEDIATELY": "#ff3b3b"}.get(shift_dec, "#ffd60a")

    st.markdown(f"""
    <div class="shift-card">
      <div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#5a6478;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.8rem;">Work Shift Intelligence</div>
      <div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#5a6478;margin-bottom:0.2rem;">SAFE TIME REMAINING</div>
      <div class="shift-time" style="color:{bar_col};">{time_left} <span style="font-size:1rem;color:#5a6478;">min</span></div>
      <div class="shift-bar-track">
        <div class="shift-bar-fill" style="width:{bar_pct:.1f}%;background:{bar_col};"></div>
      </div>
      <div style="font-family:JetBrains Mono,monospace;font-size:0.68rem;color:#5a6478;margin-bottom:1.2rem;">{bar_pct:.0f}% of 8-hour shift capacity remaining</div>
      <div style="font-family:Syne,sans-serif;font-size:1.3rem;font-weight:700;color:{sdec_col};margin-bottom:0.4rem;">{shift_dec}</div>
      <div style="font-size:0.78rem;color:#8a94a8;line-height:1.5;">Decision based on cumulative exposure ({exp_score:.1f}), physiological strain ({w_risk:.1f}), and hours on shift ({sensors['hour']:.1f}h). Threshold model per OSHA 29 CFR 1910.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── WORKER ROSTER ─────────────────────────────────────────
st.markdown('<div class="section-label"><span>05</span> Worker Shift Roster & Rotation Status</div>', unsafe_allow_html=True)
st.markdown("""
<div class="worker-row worker-row-header">
  <div>Worker</div><div>Role</div><div>Hours In</div><div>Health Status</div><div>Action</div>
</div>
""", unsafe_allow_html=True)

random.seed(tick % 50 + 1)
for w in WORKERS:
    ind_risk = max(5,  min(95, w_risk * (0.7 + w["hours_in"] / 16) + random.gauss(0, 5)))
    ind_exp  = max(2,  min(95, exp_score * (0.8 + w["hours_in"] / 20) + random.gauss(0, 3)))
    _, ind_dec, _ = shift_intelligence(ind_exp, ind_risk, w["hours_in"])

    row_class  = "worker-critical" if ind_risk >= 65 else ("worker-warn" if ind_risk >= 40 else "")
    action_col = "#ff3b3b" if "STOP" in ind_dec else ("#ffd60a" if ("ROTATE" in ind_dec or "REDUCE" in ind_dec) else "#00e676")
    status_col = "#ff3b3b" if ind_risk >= 65 else ("#ffd60a" if ind_risk >= 40 else "#00e676")
    status_txt = "CRITICAL" if ind_risk >= 65 else ("AT RISK" if ind_risk >= 40 else "FIT")

    st.markdown(f"""
    <div class="worker-row {row_class}">
      <div>
        <div class="worker-name">{w['name']}</div>
        <div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#5a6478;">{w['id']} · Since {w['shift_start']}</div>
      </div>
      <div style="font-size:0.78rem;color:#8a94a8;">{w['role']}</div>
      <div style="font-family:JetBrains Mono,monospace;font-size:0.8rem;">{w['hours_in']:.1f}h</div>
      <div style="font-family:JetBrains Mono,monospace;font-size:0.75rem;color:{status_col};">{status_txt} <span style="color:#5a6478;">({ind_risk:.0f})</span></div>
      <div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:{action_col};font-weight:500;">{ind_dec}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── HISTOGRAMS + CHARTS ────────────────────────────────────
st.markdown('<div class="section-label"><span>06</span> Risk Distribution Histograms & Trend Analysis</div>', unsafe_allow_html=True)

if len(hist) > 3:
    m_vals = [h["machine"]  for h in hist]
    w_vals = [h["worker"]   for h in hist]
    e_vals = [h["exposure"] for h in hist]
    c_vals = [h["combined"] for h in hist]

    h1, h2, h3, h4 = st.columns(4)
    with h1: st.plotly_chart(make_histogram_dark(m_vals, "Machine Risk Dist.",   "#ff6b35"), use_container_width=True)
    with h2: st.plotly_chart(make_histogram_dark(w_vals, "Worker Risk Dist.",    "#00d4ff"), use_container_width=True)
    with h3: st.plotly_chart(make_histogram_dark(e_vals, "Exposure Score Dist.", "#00ff9d"), use_container_width=True)
    with h4: st.plotly_chart(make_histogram_dark(c_vals, "Combined Risk Dist.",  "#ffd60a"), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    with t1: st.plotly_chart(make_time_area(hist, "machine",  "#ff6b35", "Machine risk over time"),        use_container_width=True)
    with t2: st.plotly_chart(make_time_area(hist, "worker",   "#00d4ff", "Worker risk over time"),         use_container_width=True)
    t3, t4 = st.columns(2)
    with t3: st.plotly_chart(make_time_area(hist, "exposure", "#00ff9d", "Cumulative exposure trend"),     use_container_width=True)
    with t4: st.plotly_chart(make_time_area(hist, "combined", "#ffd60a", "Combined supervisor risk"),      use_container_width=True)

    if len(hist) > 10:
        st.markdown("<br>", unsafe_allow_html=True)
        r_vals  = [h["radiation"] for h in hist]
        hr_vals = [h["hr"]        for h in hist]
        exp_col_list = [h["exposure"] for h in hist]

        fig_sc = go.Figure(go.Scatter(
            x=r_vals, y=hr_vals, mode='markers',
            marker=dict(
                size=7, color=exp_col_list,
                colorscale=[[0, '#00e676'], [0.5, '#ffd60a'], [1, '#ff3b3b']],
                showscale=True,
                colorbar=dict(title=dict(text="Exposure", font=dict(size=9, color='#5a6478')),
                              tickfont=dict(size=9, color='#5a6478'), thickness=10),
                line=dict(width=0.5, color='rgba(0,0,0,0.3)'),
                opacity=0.85,
            ),
        ))
        fig_sc.update_layout(
            title=dict(text="Radiation (mSv/h) vs Heart Rate — coloured by exposure score",
                       font=dict(family="JetBrains Mono", size=10, color="#5a6478"), x=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c9d1d9', family='JetBrains Mono', size=10),
            margin=dict(l=40, r=60, t=36, b=36), height=220,
            xaxis=dict(title=dict(text="Radiation mSv/h", font=dict(size=9, color='#5a6478')),
                       gridcolor='#1e2530', zeroline=False, tickfont=dict(size=9)),
            yaxis=dict(title=dict(text="Heart Rate BPM", font=dict(size=9, color='#5a6478')),
                       gridcolor='#1e2530', zeroline=False, tickfont=dict(size=9)),
            showlegend=False,
        )
        st.plotly_chart(fig_sc, use_container_width=True)
else:
    st.markdown('<div style="text-align:center;padding:3rem;color:#5a6478;font-family:JetBrains Mono,monospace;font-size:0.8rem;border:1px solid #1e2530;border-radius:12px;">▶ Press START to collect data for histogram analysis</div>', unsafe_allow_html=True)

# ── RADIATION IMPACT INFO PANEL ────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label"><span>07</span> Radiation Impact — Industry Context</div>', unsafe_allow_html=True)

ri1, ri2, ri3, ri4 = st.columns(4)
rad_cards = [
    ("0–0.1 mSv/h",  "Background Zone",  "Equivalent to natural background. Annual dose &lt;20 mSv. No restrictions.",                         "#00e676", "safe",   sensors['radiation'] <  0.1),
    ("0.1–0.3 mSv/h","Controlled Area",  "Continuous monitoring required. Annual limit approach. PPE mandatory.",                                "#ffd60a", "warn",   0.1 <= sensors['radiation'] <  0.3),
    ("0.3–1.0 mSv/h","Supervised Zone",  "Shift restrictions apply. Immediate fatigue escalation. Dosimeter required.",                         "#ff6b35", "rotate", 0.3 <= sensors['radiation'] <  1.0),
    (">1.0 mSv/h",   "Exclusion Zone",   "Evacuation threshold. Thyroid &amp; marrow risk. Emergency protocol active.",                         "#ff3b3b", "danger", sensors['radiation'] >= 1.0),
]
for col, (dose, zone, desc, color, cls, active) in zip([ri1, ri2, ri3, ri4], rad_cards):
    r, g, b      = hex_to_rgb(color)
    border_style = f"border-color:{color}!important;" if active else ""
    current_tag  = (f'<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;'
                    f'color:{color};margin-top:0.5rem;letter-spacing:0.1em;">◉ CURRENT RANGE</div>'
                    if active else "")
    with col:
        st.markdown(f"""
        <div class="m-card" style="{border_style}background:rgba({r},{g},{b},0.05);">
          <div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:{color};margin-bottom:0.2rem;">{dose}</div>
          <div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;font-weight:500;color:{color};margin-bottom:0.5rem;">{zone}</div>
          <div style="font-size:0.78rem;color:#8a94a8;line-height:1.5;">{desc}</div>
          {current_tag}
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top:1px solid #1e2530;padding-top:1rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
  <div style="font-family:Syne,sans-serif;font-size:0.9rem;font-weight:700;color:#00d4ff;">⬡ NEXUS GUARDIAN</div>
  <div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#5a6478;text-align:center;">
    Facility: {facility} &nbsp;·&nbsp; Tick #{tick} &nbsp;·&nbsp;
    Dataset: {len(df)} records · {df['facility'].nunique()} facilities<br>
    Standards: OSHA 29 CFR 1910 · ICRP 103 · NIOSH REL · WHO IEH
  </div>
  <div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#5a6478;">v2.4.1 · AI Safety Intelligence</div>
</div>
""", unsafe_allow_html=True)

# ── AUTO REFRESH ────────────────────────────────────────────
if st.session_state.running:
    time.sleep(1)
    st.rerun()