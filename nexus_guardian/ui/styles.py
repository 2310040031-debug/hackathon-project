"""
All global CSS for NEXUS GUARDIAN.
Call inject() once at the top of app.py.
"""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Instrument+Sans:wght@400;500;600&display=swap');

:root {
  --bg:      #050709; --surface: #0c0e12; --card:   #101318;
  --border:  #1e2530; --accent:  #00d4ff; --accent2: #ff6b35;
  --accent3: #00ff9d; --warn:    #ffd60a; --danger:  #ff3b3b;
  --safe:    #00e676; --text:    #e8edf5; --muted:   #5a6478;
}
html, body, [class*="css"] { font-family:'Instrument Sans',sans-serif; background:var(--bg)!important; color:var(--text)!important; }
.stApp { background:var(--bg)!important; }
div[data-testid="stSidebar"] { background:var(--surface)!important; border-right:1px solid var(--border)!important; }
div[data-testid="stSidebar"] * { color:var(--text)!important; }
.block-container { padding:1.5rem 2rem 3rem!important; }

/* HERO */
.nexus-hero { position:relative; padding:2rem 0 1.5rem; margin-bottom:2rem; border-bottom:1px solid var(--border); }
.hero-title { font-family:'Syne',sans-serif; font-weight:800; font-size:2.6rem; letter-spacing:-0.02em; line-height:1; background:linear-gradient(135deg,#00d4ff 0%,#00ff9d 50%,#e8edf5 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin:0; }
.hero-sub { font-family:'JetBrains Mono',monospace; font-size:0.72rem; letter-spacing:0.22em; text-transform:uppercase; color:var(--muted); margin-top:0.4rem; }
.hero-tag { display:inline-block; padding:0.2rem 0.7rem; border:1px solid rgba(0,212,255,0.3); border-radius:20px; font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:var(--accent); letter-spacing:0.1em; margin-right:0.5rem; margin-top:0.8rem; background:rgba(0,212,255,0.05); }

/* SECTION LABEL */
.section-label { font-family:'JetBrains Mono',monospace; font-size:0.65rem; letter-spacing:0.25em; text-transform:uppercase; color:var(--muted); padding:0.3rem 0; border-bottom:1px solid var(--border); margin-bottom:1.2rem; }
.section-label span { color:var(--accent); margin-right:0.5rem; }

/* METRIC CARD */
.m-card { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:1.2rem 1.4rem; position:relative; overflow:hidden; }
.m-card::before { content:''; position:absolute; top:0; left:0; width:100%; height:2px; background:var(--accent-line,var(--border)); border-radius:2px 2px 0 0; }
.m-card-safe { --accent-line:var(--safe); } .m-card-warn { --accent-line:var(--warn); }
.m-card-danger { --accent-line:var(--danger); } .m-card-info { --accent-line:var(--accent); }
.m-label { font-family:'JetBrains Mono',monospace; font-size:0.65rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--muted); margin-bottom:0.3rem; }
.m-value { font-family:'Syne',sans-serif; font-size:2.2rem; font-weight:700; line-height:1; color:var(--text); }
.m-unit  { font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:var(--muted); margin-left:0.2rem; }

/* BADGES */
.badge { display:inline-flex; align-items:center; gap:0.3rem; padding:0.25rem 0.75rem; border-radius:4px; font-family:'JetBrains Mono',monospace; font-size:0.7rem; font-weight:500; letter-spacing:0.08em; }
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

/* AGENT CARDS */
.agent-card { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:1.5rem; position:relative; overflow:hidden; }
.agent-machine { border-color:rgba(255,107,53,0.2); }
.agent-worker  { border-color:rgba(0,212,255,0.2);  }
.agent-expo    { border-color:rgba(0,255,157,0.2);  }
.agent-icon { font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:var(--agent-color,var(--accent)); letter-spacing:0.15em; text-transform:uppercase; margin-bottom:0.8rem; display:flex; align-items:center; gap:0.5rem; }
.agent-icon::before { content:''; width:20px; height:1px; background:var(--agent-color,var(--accent)); }
.agent-score { font-family:'Syne',sans-serif; font-size:3.5rem; font-weight:800; line-height:1; margin-bottom:0.2rem; }
.agent-score-safe { color:var(--safe); } .agent-score-warn { color:var(--warn); } .agent-score-danger { color:var(--danger); }
.agent-rec { font-size:0.82rem; color:#8a94a8; line-height:1.5; margin-top:0.8rem; padding-top:0.8rem; border-top:1px solid var(--border); }

/* SUPERVISOR */
.supervisor-card { background:linear-gradient(135deg,#0c1018 0%,#0f1520 100%); border:1px solid rgba(0,212,255,0.2); border-radius:16px; padding:2rem; position:relative; }
.supervisor-card::before { content:''; position:absolute; top:-1px; left:5%; right:5%; height:1px; background:linear-gradient(90deg,transparent,var(--accent),transparent); }
.sup-verdict { font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800; letter-spacing:-0.02em; }
.sup-score { font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:var(--muted); margin-top:0.3rem; }
.sup-exp { font-size:0.88rem; color:#8a94a8; line-height:1.6; margin-top:1rem; padding-top:1rem; border-top:1px solid var(--border); }

/* SHIFT */
.shift-card { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:1.5rem; }
.shift-time { font-family:'Syne',sans-serif; font-size:2.8rem; font-weight:700; }
.shift-bar-track { height:8px; background:#1a1f2a; border-radius:4px; margin:1rem 0 0.4rem; overflow:hidden; }
.shift-bar-fill  { height:100%; border-radius:4px; }

/* RISK BARS */
.risk-row { display:flex; align-items:center; gap:0.8rem; margin-bottom:0.8rem; }
.risk-label { font-family:'JetBrains Mono',monospace; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.1em; color:var(--muted); width:120px; flex-shrink:0; }
.risk-track { flex:1; height:6px; background:#1a1f2a; border-radius:3px; overflow:hidden; }
.risk-fill  { height:100%; border-radius:3px; }
.risk-num   { font-family:'JetBrains Mono',monospace; font-size:0.75rem; width:36px; text-align:right; flex-shrink:0; }

/* TICKER */
.ticker-bar { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:0.5rem 1rem; font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:var(--muted); display:flex; align-items:center; gap:1.5rem; margin-bottom:1.5rem; overflow:hidden; }
.ticker-live { color:var(--safe); animation:blink 1.5s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }
.ticker-item { display:flex; align-items:center; gap:0.4rem; }
.ticker-item strong { color:var(--text); }

/* WORKER TABLE */
.worker-row { display:grid; grid-template-columns:2fr 1fr 1fr 1fr 1.5fr; align-items:center; padding:0.7rem 0.8rem; border-radius:8px; margin-bottom:0.4rem; background:var(--card); border:1px solid var(--border); font-size:0.82rem; }
.worker-row-header { font-family:'JetBrains Mono',monospace; font-size:0.62rem; text-transform:uppercase; letter-spacing:0.12em; color:var(--muted); padding:0.4rem 0.8rem; margin-bottom:0.4rem; }
.worker-critical { border-color:rgba(255,59,59,0.3);  background:rgba(255,59,59,0.04); }
.worker-warn     { border-color:rgba(255,214,10,0.3); background:rgba(255,214,10,0.04); }

/* RADIATION METER */
.rad-meter { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:1.2rem; }
.rad-value  { font-family:'Syne',sans-serif; font-size:2rem; font-weight:700; color:var(--warn); }
.rad-label  { font-family:'JetBrains Mono',monospace; font-size:0.62rem; text-transform:uppercase; letter-spacing:0.15em; color:var(--muted); margin-bottom:0.3rem; }

/* SIDEBAR */
.sidebar-section { font-family:'JetBrains Mono',monospace; font-size:0.62rem; text-transform:uppercase; letter-spacing:0.18em; color:var(--muted); padding:0.8rem 0 0.4rem; border-bottom:1px solid var(--border); margin-bottom:0.8rem; }
.stSlider label, .stSelectbox label, .stToggle label { font-family:'JetBrains Mono',monospace!important; font-size:0.72rem!important; text-transform:uppercase!important; letter-spacing:0.1em!important; color:var(--muted)!important; }

/* INDUSTRY */
.industry-slide { border-radius:12px; height:120px; background:var(--card); border:1px solid var(--border); display:flex; align-items:center; padding:1.2rem; gap:1rem; }
.industry-name { font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:600; }
.industry-desc { font-size:0.75rem; color:var(--muted); margin-top:0.2rem; line-height:1.4; }

::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:2px; }
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)
