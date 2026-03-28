"""
NEXUS GUARDIAN — Industrial AI Safety Intelligence Platform
Entry point. Run with: streamlit run app.py
"""
import os
import time
import random
import streamlit as st

# ── Page config must be first Streamlit call ──────────────
st.set_page_config(
    page_title="NEXUS GUARDIAN — Industrial AI Safety",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Internal modules ──────────────────────────────────────
from ui.styles     import inject
from ui.incident_scroll import render as render_incidents
from ui.components import (badge_html, badge_type, sensor_card, score_class,
                           score_color, risk_bar_row, hex_to_rgb)
from ui            import charts
from data_pipeline.loader import load_dataset, validate_or_stop, get_sensor_row
from agents        import machine_agent, exposure_system, worker_agent, shift_intelligence, supervisor_agent
from agents.validation_metrics import compute_dataset_validation, live_alignment
from constants     import INDUSTRY_DATA, WORKERS, THRESHOLDS

inject()


@st.cache_data(show_spinner="Computing AI model validation metrics…")
def _cached_validation_metrics(csv_path: str, mtime: float) -> dict:
    return compute_dataset_validation(csv_path, mtime)


# ── Paths ─────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "sensor_data.csv")

# ── Load + validate data ──────────────────────────────────
df = load_dataset(CSV_PATH)
validate_or_stop(df)

val_metrics = _cached_validation_metrics(
    CSV_PATH,
    os.path.getmtime(CSV_PATH) if os.path.isfile(CSV_PATH) else 0.0,
)

categories = ["All", "Petrochemical", "Pharmaceutical"]

# ── Session state ─────────────────────────────────────────
for k, v in [("tick", 0), ("exposure", 0.0), ("running", False), ("history", [])]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#00d4ff;margin-bottom:0.2rem;">⬡ NEXUS GUARDIAN</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#5a6478;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:1.2rem;">Control Interface v2.4</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Facility Selection</div>', unsafe_allow_html=True)

    # Industry filter comes FIRST so it controls the facility list
    cat_filter = st.selectbox(
        "Industry Filter",
        categories,
        label_visibility="collapsed",
        key="cat_filter"
    )

    # Build the filtered facility list based on selected industry
    if cat_filter == "All":
        filtered_facilities = df["facility"].unique().tolist()
    elif cat_filter == "Petrochemical":
        filtered_facilities = [
            "Distillation Column",
            "Catalytic Cracker",
            "Hydrodesulfurization",
            "LPG Storage Unit",
            "Crude Distillation",
        ]
    elif cat_filter == "Pharmaceutical":
        filtered_facilities = [
            "API Synthesis Reactor",
            "Solvent Recovery Unit",
            "Tablet Coating Room",
            "Sterile Fill & Finish",
        ]
    else:
        filtered_facilities = df["facility"].unique().tolist()

    # Only show facilities that actually exist in the loaded dataset
    available = df["facility"].unique().tolist()
    filtered_facilities = [f for f in filtered_facilities if f in available]

    # Facility dropdown now only shows filtered options
    facility = st.selectbox(
        "Active Facility",
        filtered_facilities,
        label_visibility="collapsed",
        key="facility_select"
    )

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
        st.session_state.tick = 0; st.session_state.exposure = 0.0
        st.session_state.running = False; st.session_state.history = []

    st.markdown('<div class="sidebar-section">Thresholds (Reference)</div>', unsafe_allow_html=True)
    for k, v in THRESHOLDS.items():
        st.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#5a6478;">{k.upper()}: {v["limit"]} {v["unit"]}</div>', unsafe_allow_html=True)

# ── Tick pipeline ─────────────────────────────────────────
if st.session_state.running:
    st.session_state.tick += 1
tick = st.session_state.tick

sensors = ({"temperature": temp, "gas_ppm": gas, "noise_db": noise,
            "radiation": radiation, "heart_rate": heart_rate, "fatigue": fatigue, "hour": 6.0}
           if manual else get_sensor_row(df, tick, facility))

m_result  = machine_agent.run(sensors["temperature"], sensors["gas_ppm"], sensors["noise_db"], sensors["radiation"])
exp_result= exposure_system.run(sensors["radiation"], sensors["gas_ppm"], sensors["temperature"], st.session_state.exposure)
st.session_state.exposure = exp_result["score"]
w_result  = worker_agent.run(sensors["heart_rate"], sensors["fatigue"], exp_result["score"], m_result["score"])
sh_result = shift_intelligence.run(exp_result["score"], w_result["score"], sensors["hour"])
sup_result= supervisor_agent.run(m_result["score"], w_result["score"], exp_result["score"])
live_val = live_alignment(m_result, w_result, sup_result, sensors, exp_result["score"])

st.session_state.history.append({
    "tick": tick, "machine": m_result["score"], "worker": w_result["score"],
    "exposure": exp_result["score"], "combined": sup_result["combined_score"],
    "temp": sensors["temperature"], "gas": sensors["gas_ppm"],
    "radiation": sensors["radiation"], "hr": sensors["heart_rate"],
})
if len(st.session_state.history) > 80:
    st.session_state.history = st.session_state.history[-80:]
hist = st.session_state.history

# ─────────────────────────────────────────────────────────
# RENDER UI
# ─────────────────────────────────────────────────────────

# 00 Hero
st.markdown("""
<div class="nexus-hero">
  <div class="hero-title">NEXUS GUARDIAN</div>
  <div class="hero-sub">Industrial AI Safety Intelligence Platform</div>
  <div style="margin-top:0.8rem;">
    <span class="hero-tag">PETROCHEMICAL</span><span class="hero-tag">PHARMACEUTICAL</span>
    <span class="hero-tag">REAL-TIME AI</span><span class="hero-tag">v2.4.1</span>
  </div>
</div>""", unsafe_allow_html=True)

# 00b Incident Scrollytelling
st.markdown('<div class="section-label"><span>00</span> Why This Exists — Real Incidents</div>', unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#5a6478;letter-spacing:0.15em;margin-bottom:0.8rem;">
  SCROLL INSIDE THE PANEL BELOW TO NAVIGATE THROUGH DOCUMENTED INDUSTRIAL ACCIDENTS
</div>
""", unsafe_allow_html=True)
render_incidents(height=650)
st.markdown("<br>", unsafe_allow_html=True)

# 01 Industry Slides
st.markdown('<div class="section-label"><span>01</span> Active Industries & Facilities</div>', unsafe_allow_html=True)
for col, (ind, data) in zip(st.columns(2), INDUSTRY_DATA.items()):
    r, g, b = hex_to_rgb(data["color"])
    hazards = "".join(f'<span style="background:rgba({r},{g},{b},0.1);color:{data["color"]};font-size:0.6rem;padding:0.15rem 0.5rem;border-radius:3px;font-family:JetBrains Mono,monospace;">{h}</span>' for h in data["hazards"])
    with col:
        st.markdown(f'<div class="industry-slide" style="border-color:rgba({r},{g},{b},0.25);"><div><div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:{data["color"]};text-transform:uppercase;letter-spacing:0.18em;margin-bottom:0.3rem;">{ind}</div><div class="industry-name">{data["icon"]} {data["companies"]}</div><div class="industry-desc">{data["desc"]}</div><div style="margin-top:0.5rem;display:flex;gap:0.4rem;flex-wrap:wrap;">{hazards}</div></div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 02 Ticker
fac_row   = df[df["facility"] == facility].iloc[0]
exp_c     = '#ff3b3b' if exp_result["score"] > 65 else ('#ffd60a' if exp_result["score"] > 35 else '#00e676')
sup_c     = '#ff3b3b' if any(x in sup_result["status"] for x in ["EMERGENCY","CRITICAL"]) else ('#ffd60a' if any(x in sup_result["status"] for x in ["ROTATION","ELEVATED"]) else '#00e676')
st.markdown(f'<div class="ticker-bar"><span class="ticker-live">● LIVE</span><span class="ticker-item">FACILITY: <strong>{facility}</strong></span><span class="ticker-item">CATEGORY: <strong>{fac_row["category"]}</strong></span><span class="ticker-item">TICK: <strong>#{tick}</strong></span><span class="ticker-item">SHIFT HOUR: <strong>{sensors["hour"]:.1f}h</strong></span><span class="ticker-item">EXPOSURE: <strong style="color:{exp_c}">{exp_result["score"]:.1f}</strong></span><span class="ticker-item">VERDICT: <strong style="color:{sup_c}">{sup_result["status"]}</strong></span></div>', unsafe_allow_html=True)

# 03 Live Sensor Strip
st.markdown('<div class="section-label"><span>02</span> Live Sensor Readings</div>', unsafe_allow_html=True)
th = THRESHOLDS
s1,s2,s3,s4,s5,s6 = st.columns(6)
with s1: st.markdown(sensor_card("Temperature",  sensors["temperature"], "°C",    th["temperature"]["limit"], "warn"   if sensors["temperature"] > th["temperature"]["warn"] else "info"), unsafe_allow_html=True)
with s2: st.markdown(sensor_card("Gas / VOC",    sensors["gas_ppm"],     "ppm",   th["gas_ppm"]["limit"],     "danger" if sensors["gas_ppm"] > th["gas_ppm"]["danger"] else "warn" if sensors["gas_ppm"] > th["gas_ppm"]["warn"] else "info"), unsafe_allow_html=True)
with s3: st.markdown(sensor_card("Noise Level",  sensors["noise_db"],    "dB",    th["noise_db"]["limit"],    "warn"   if sensors["noise_db"] > th["noise_db"]["warn"] else "info"), unsafe_allow_html=True)
with s4: st.markdown(sensor_card("Radiation",    sensors["radiation"],   "mSv/h", th["radiation"]["limit"],   "danger" if sensors["radiation"] > th["radiation"]["danger"] else "warn" if sensors["radiation"] > th["radiation"]["warn"] else "safe"), unsafe_allow_html=True)
with s5: st.markdown(sensor_card("Heart Rate",   sensors["heart_rate"],  "BPM",   th["heart_rate"]["limit"],  "warn"   if sensors["heart_rate"] > th["heart_rate"]["warn"] else "info"), unsafe_allow_html=True)
with s6: st.markdown(sensor_card("Fatigue Index",sensors["fatigue"],     "/100",  th["fatigue"]["limit"],     "danger" if sensors["fatigue"] > th["fatigue"]["danger"] else "warn" if sensors["fatigue"] > th["fatigue"]["warn"] else "safe"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 04 AI Agent Cards
st.markdown('<div class="section-label"><span>03</span> AI Agent Analysis</div>', unsafe_allow_html=True)
ag1, ag2, ag3 = st.columns(3)

with ag1:
    bt        = badge_type(m_result["status"])
    risk_bars = "".join(risk_bar_row(k, v) for k, v in m_result["breakdown"].items())
    st.markdown(f'<div class="agent-card agent-machine"><div class="agent-icon" style="--agent-color:#ff6b35;">MACHINE HEALTH AGENT</div><div class="agent-score {score_class(m_result["score"])}">{m_result["score"]}</div><div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#5a6478;margin:.2rem 0 .6rem;">/ 100 risk index</div>{badge_html(m_result["status"], bt)}<div style="margin-top:0.8rem;">{risk_bars}</div><div class="agent-rec"><div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#5a6478;margin-bottom:0.3rem;">PATTERN DETECTION</div><div style="color:#ffd60a;font-size:0.75rem;margin-bottom:0.5rem;">{m_result["patterns"]}</div>{m_result["recommendation"]}</div></div>', unsafe_allow_html=True)
    st.plotly_chart(charts.radar_chart(m_result["breakdown"]), use_container_width=True)

with ag2:
    et  = badge_type(exp_result["level"])
    rip = min(100, sensors["radiation"] / 2.0 * 100)
    rfc = '#ff3b3b' if sensors["radiation"] > 0.6 else ('#ffd60a' if sensors["radiation"] > 0.3 else '#00e676')
    rlt = ('HIGH CONCERN — exceeds ICRP 20 mSv/yr guidance' if sensors["radiation"] > 0.6 else 'MODERATE — cumulative monitoring required' if sensors["radiation"] > 0.25 else 'WITHIN annual dose limits')
    vpc = min(100, sensors["gas_ppm"] / 250 * 100)
    hpc = min(100, max(0, (sensors["temperature"] - 28) / 64) * 100)
    st.markdown(f'<div class="agent-card agent-expo"><div class="agent-icon" style="--agent-color:#00ff9d;">EXPOSURE MONITOR</div><div class="agent-score {score_class(exp_result["score"])}">{exp_result["score"]:.1f}</div><div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#5a6478;margin:.2rem 0 .6rem;">cumulative dose index</div>{badge_html(exp_result["level"], et)}<div style="margin-top:1rem;"><div class="rad-meter" style="margin-bottom:0.8rem;"><div class="rad-label">Radiation Impact (mSv/h)</div><div class="rad-value">{sensors["radiation"]:.3f}</div><div class="risk-track" style="margin-top:0.4rem;"><div class="risk-fill" style="width:{rip:.0f}%;background:{rfc};"></div></div><div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#5a6478;margin-top:0.3rem;">{rlt}</div></div>{risk_bar_row("Radiation", rip)}{risk_bar_row("Chemical/VOC", vpc)}{risk_bar_row("Heat Stress", hpc)}</div><div class="agent-rec">Cumulative exposure tracked per NIOSH TLV/TWA. Radiation follows ICRP 103 framework. Reset at shift end.</div></div>', unsafe_allow_html=True)

with ag3:
    wt      = badge_type(w_result["status"])
    hr_sc   = min(100, max(0, (sensors["heart_rate"] - 60) / 72 * 100))
    rad_eff = min(20, exp_result["score"] * 0.2)
    st.markdown(f'<div class="agent-card agent-worker"><div class="agent-icon" style="--agent-color:#00d4ff;">WORKER HEALTH AGENT</div><div class="agent-score {score_class(w_result["score"])}">{w_result["score"]}</div><div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#5a6478;margin:.2rem 0 .6rem;">/ 100 health risk index</div>{badge_html(w_result["status"], wt)}<div style="margin-top:0.8rem;">{risk_bar_row("Physiological", hr_sc)}{risk_bar_row("Fatigue Load", sensors["fatigue"])}{risk_bar_row("Exposure Load", exp_result["score"])}{risk_bar_row("Radiation Effect", rad_eff)}</div><div class="agent-rec">{w_result["recommendation"]}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-label"><span>03b</span> AI Model Validation — Threshold Oracle</div>', unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#5a6478;letter-spacing:0.06em;margin-bottom:1rem;line-height:1.55;">
  <strong style="color:#a8b0c4;">Offline accuracy</strong> compares each agent’s risk <em>tier</em> to an independent label derived from
  <span style="color:#00d4ff;">constants.THRESHOLDS</span> (warn / danger / limit bands). The full CSV is replayed per facility with cumulative exposure, same as live simulation.
  <strong style="color:#a8b0c4;">Mean abs. error (MAE)</strong> is |agent score − tier proxy| averaged over all rows (lower is tighter to the oracle band).
</div>
""", unsafe_allow_html=True)

vm = val_metrics
mv1, mv2, mv3, mv4 = st.columns(4)
with mv1:
    st.metric("Machine Health", f"{vm['machine_accuracy']:.1f}%")
    st.caption(f"MAE vs tier proxy: {vm['machine_mae_vs_tier']:.1f}")
with mv2:
    st.metric("Worker Health", f"{vm['worker_accuracy']:.1f}%")
    st.caption(f"MAE vs tier proxy: {vm['worker_mae_vs_tier']:.1f}")
with mv3:
    st.metric("Supervisor", f"{vm['supervisor_accuracy']:.1f}%")
    st.caption("Verdict tier match rate")
with mv4:
    st.metric("Overall (mean)", f"{vm['overall_accuracy']:.1f}%")
    st.caption(f"Dataset steps: {vm['n_samples']:,}")

lv = live_val
_ok = "#00e676"
_bad = "#ff6b35"
_dot_m = _ok if lv["machine_match"] else _bad
_dot_w = _ok if lv["worker_match"] else _bad
_dot_s = _ok if lv["supervisor_match"] else _bad
st.markdown(f"""
<div style="border:1px solid #1e2530;border-radius:12px;padding:1rem 1.2rem;margin-top:0.5rem;background:rgba(13,17,23,0.35);">
  <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:#5a6478;letter-spacing:0.18em;text-transform:uppercase;margin-bottom:0.75rem;">This tick vs oracle</div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.9rem;font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#c5cdd8;">
    <div><span style="color:{_dot_m};">●</span> Machine <span style="color:#5a6478;">{'aligns' if lv['machine_match'] else 'differs'}</span><br/><span style="font-size:0.62rem;color:#5a6478;">oracle: {lv['oracle_machine']}</span></div>
    <div><span style="color:{_dot_w};">●</span> Worker <span style="color:#5a6478;">{'aligns' if lv['worker_match'] else 'differs'}</span><br/><span style="font-size:0.62rem;color:#5a6478;">oracle: {lv['oracle_worker']}</span></div>
    <div><span style="color:{_dot_s};">●</span> Supervisor <span style="color:#5a6478;">{'aligns' if lv['supervisor_match'] else 'differs'}</span><br/><span style="font-size:0.62rem;color:#5a6478;">oracle: {lv['oracle_supervisor']}</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 05 Supervisor + Shift
st.markdown('<div class="section-label"><span>04</span> Supervisor AI Agent & Shift Intelligence</div>', unsafe_allow_html=True)
sv1, sv2 = st.columns([3, 2])

SUP_COLOR_MAP = {
    "safe":     ("#00e676", "rgba(0,230,118,0.3)"),
    "warning":  ("#ffd60a", "rgba(255,214,10,0.3)"),
    "rotate":   ("#ff6b35", "rgba(255,107,53,0.3)"),
    "critical": ("#ff3b3b", "rgba(255,59,59,0.3)"),
}
tc, tb = SUP_COLOR_MAP.get(sup_result["color_key"], SUP_COLOR_MAP["safe"])
with sv1:
    st.markdown(f'<div class="supervisor-card" style="border-color:{tb};"><div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#5a6478;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.8rem;">⬡ Supervisor AI Agent — Final Verdict</div><div class="sup-verdict" style="color:{tc};">{sup_result["status"]}</div><div class="sup-score">Combined Risk Index: {sup_result["combined_score"]} / 100 &nbsp;·&nbsp; Machine {m_result["score"]:.0f}% · Worker {w_result["score"]:.0f}% · Exposure {exp_result["score"]:.0f}%</div><div class="sup-exp">{sup_result["explanation"]}</div><div style="margin-top:1.2rem;display:grid;grid-template-columns:repeat(3,1fr);gap:0.8rem;"><div style="text-align:center;background:rgba(255,107,53,0.06);border:1px solid rgba(255,107,53,0.15);border-radius:8px;padding:0.8rem;"><div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:700;color:#ff6b35;">{m_result["score"]:.0f}</div><div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#5a6478;text-transform:uppercase;">Machine</div></div><div style="text-align:center;background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.15);border-radius:8px;padding:0.8rem;"><div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:700;color:#00d4ff;">{w_result["score"]:.0f}</div><div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#5a6478;text-transform:uppercase;">Worker</div></div><div style="text-align:center;background:rgba(0,255,157,0.06);border:1px solid rgba(0,255,157,0.15);border-radius:8px;padding:0.8rem;"><div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:700;color:#00ff9d;">{exp_result["score"]:.0f}</div><div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#5a6478;text-transform:uppercase;">Exposure</div></div></div></div>', unsafe_allow_html=True)

bpct  = min(100, sh_result["time_remaining"] / 480 * 100)
bcol  = "#ff3b3b" if bpct < 25 else ("#ffd60a" if bpct < 50 else "#00e676")
sdcol = {"CONTINUE SHIFT": "#00e676", "REDUCE EXPOSURE": "#ffd60a", "ROTATE WORKER": "#ff6b35", "STOP IMMEDIATELY": "#ff3b3b"}.get(sh_result["decision"], "#ffd60a")
with sv2:
    st.markdown(f'<div class="shift-card"><div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#5a6478;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.8rem;">Work Shift Intelligence</div><div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#5a6478;margin-bottom:0.2rem;">SAFE TIME REMAINING</div><div class="shift-time" style="color:{bcol};">{sh_result["time_remaining"]} <span style="font-size:1rem;color:#5a6478;">min</span></div><div class="shift-bar-track"><div class="shift-bar-fill" style="width:{bpct:.1f}%;background:{bcol};"></div></div><div style="font-family:JetBrains Mono,monospace;font-size:0.68rem;color:#5a6478;margin-bottom:1.2rem;">{bpct:.0f}% of 8-hour shift capacity remaining</div><div style="font-family:Syne,sans-serif;font-size:1.3rem;font-weight:700;color:{sdcol};margin-bottom:0.4rem;">{sh_result["decision"]}</div><div style="font-size:0.78rem;color:#8a94a8;line-height:1.5;">Decision based on cumulative exposure ({exp_result["score"]:.1f}), strain ({w_result["score"]:.1f}), shift hour ({sensors["hour"]:.1f}h). Per OSHA 29 CFR 1910.</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 06 Worker Roster
st.markdown('<div class="section-label"><span>05</span> Worker Shift Roster & Rotation Status</div>', unsafe_allow_html=True)
st.markdown('<div class="worker-row worker-row-header"><div>Worker</div><div>Role</div><div>Hours In</div><div>Health Status</div><div>Action</div></div>', unsafe_allow_html=True)
random.seed(tick % 50 + 1)
for w in WORKERS:
    ir  = max(5, min(95, w_result["score"] * (0.7 + w["hours_in"] / 16) + random.gauss(0, 5)))
    ie  = max(2, min(95, exp_result["score"] * (0.8 + w["hours_in"] / 20) + random.gauss(0, 3)))
    isr = shift_intelligence.run(ie, ir, w["hours_in"])
    rc  = "worker-critical" if ir >= 65 else ("worker-warn" if ir >= 40 else "")
    ac  = "#ff3b3b" if "STOP" in isr["decision"] else ("#ffd60a" if ("ROTATE" in isr["decision"] or "REDUCE" in isr["decision"]) else "#00e676")
    sc  = "#ff3b3b" if ir >= 65 else ("#ffd60a" if ir >= 40 else "#00e676")
    st_= "CRITICAL" if ir >= 65 else ("AT RISK" if ir >= 40 else "FIT")
    st.markdown(f'<div class="worker-row {rc}"><div><div style="font-weight:500;">{w["name"]}</div><div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#5a6478;">{w["id"]} · Since {w["shift_start"]}</div></div><div style="font-size:0.78rem;color:#8a94a8;">{w["role"]}</div><div style="font-family:JetBrains Mono,monospace;font-size:0.8rem;">{w["hours_in"]:.1f}h</div><div style="font-family:JetBrains Mono,monospace;font-size:0.75rem;color:{sc};">{st_} <span style="color:#5a6478;">({ir:.0f})</span></div><div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:{ac};font-weight:500;">{isr["decision"]}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 07 Charts
st.markdown('<div class="section-label"><span>06</span> Risk Distribution Histograms & Trend Analysis</div>', unsafe_allow_html=True)
if len(hist) > 3:
    h1, h2, h3, h4 = st.columns(4)
    with h1: st.plotly_chart(charts.histogram_dark([h["machine"]  for h in hist], "Machine Risk Dist.",   "#ff6b35"), use_container_width=True)
    with h2: st.plotly_chart(charts.histogram_dark([h["worker"]   for h in hist], "Worker Risk Dist.",    "#00d4ff"), use_container_width=True)
    with h3: st.plotly_chart(charts.histogram_dark([h["exposure"] for h in hist], "Exposure Score Dist.", "#00ff9d"), use_container_width=True)
    with h4: st.plotly_chart(charts.histogram_dark([h["combined"] for h in hist], "Combined Risk Dist.",  "#ffd60a"), use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    with t1: st.plotly_chart(charts.time_area(hist, "machine",  "#ff6b35", "Machine risk over time"),    use_container_width=True)
    with t2: st.plotly_chart(charts.time_area(hist, "worker",   "#00d4ff", "Worker risk over time"),     use_container_width=True)
    t3, t4 = st.columns(2)
    with t3: st.plotly_chart(charts.time_area(hist, "exposure", "#00ff9d", "Cumulative exposure trend"),  use_container_width=True)
    with t4: st.plotly_chart(charts.time_area(hist, "combined", "#ffd60a", "Combined supervisor risk"),  use_container_width=True)
    if len(hist) > 10:
        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(charts.scatter_rad_vs_hr(hist), use_container_width=True)
else:
    st.markdown('<div style="text-align:center;padding:3rem;color:#5a6478;font-family:JetBrains Mono,monospace;font-size:0.8rem;border:1px solid #1e2530;border-radius:12px;">▶ Press START to collect data for histogram analysis</div>', unsafe_allow_html=True)

# 08 Radiation Panel
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label"><span>07</span> Radiation Impact — Industry Context</div>', unsafe_allow_html=True)
RAD_CARDS = [
    ("0–0.1 mSv/h",  "Background Zone",  "Equivalent to natural background. Annual dose &lt;20 mSv. No restrictions.",              "#00e676", sensors["radiation"] <  0.1),
    ("0.1–0.3 mSv/h","Controlled Area",  "Continuous monitoring required. Annual limit approach. PPE mandatory.",                    "#ffd60a", 0.1 <= sensors["radiation"] <  0.3),
    ("0.3–1.0 mSv/h","Supervised Zone",  "Shift restrictions apply. Immediate fatigue escalation. Dosimeter required.",             "#ff6b35", 0.3 <= sensors["radiation"] <  1.0),
    (">1.0 mSv/h",   "Exclusion Zone",   "Evacuation threshold. Thyroid &amp; marrow risk. Emergency protocol active.",             "#ff3b3b", sensors["radiation"] >= 1.0),
]
for col, (dose, zone, desc, color, active) in zip(st.columns(4), RAD_CARDS):
    r, g, b = hex_to_rgb(color)
    bdr = f"border-color:{color}!important;" if active else ""
    tag = f'<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:{color};margin-top:0.5rem;">◉ CURRENT RANGE</div>' if active else ""
    with col:
        st.markdown(f'<div class="m-card" style="{bdr}background:rgba({r},{g},{b},0.05);"><div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:{color};margin-bottom:0.2rem;">{dose}</div><div style="font-family:JetBrains Mono,monospace;font-size:0.7rem;font-weight:500;color:{color};margin-bottom:0.5rem;">{zone}</div><div style="font-size:0.78rem;color:#8a94a8;line-height:1.5;">{desc}</div>{tag}</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f'<div style="border-top:1px solid #1e2530;padding-top:1rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;"><div style="font-family:Syne,sans-serif;font-size:0.9rem;font-weight:700;color:#00d4ff;">⬡ NEXUS GUARDIAN</div><div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#5a6478;text-align:center;">Facility: {facility} · Tick #{tick} · Dataset: {len(df)} records · {df["facility"].nunique()} facilities<br>Standards: OSHA 29 CFR 1910 · ICRP 103 · NIOSH REL · WHO IEH</div><div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#5a6478;">v2.4.1 · AI Safety Intelligence</div></div>', unsafe_allow_html=True)

# Auto-refresh
if st.session_state.running:
    time.sleep(1)
    st.rerun()
