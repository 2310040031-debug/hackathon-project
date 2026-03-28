"""
Incident Scrollytelling Component — Image Edition.
Renders a full-screen cinematic scroll experience using real news photographs
of industrial accidents caused by delayed alert systems.
Images are loaded from the local nexus_guardian/images/ folder,
converted to base64 so Streamlit's iframe can display them without
needing a static file server.
"""

import os
import base64


def _img_to_b64(filename: str) -> str:
    """
    Convert a local image file to a base64 data URI.
    Falls back to an empty string if the file is not found,
    so the panel still renders (just without a background image).
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base_dir, "images", filename)
    if not os.path.exists(img_path):
        return ""
    with open(img_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    ext = filename.rsplit(".", 1)[-1].lower()
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
    return f"data:{mime};base64,{data}"


def _build_html() -> str:
    """Build the full HTML string with base64-embedded images."""

    imgs = {
        "sigachi": _img_to_b64("sigachi.jpg"),
        "lg": _img_to_b64("lg.jpg"),
        "ntpc": _img_to_b64("ntpc.jpg"),
        "neyveli": _img_to_b64("neyveli.jpg"),
        "bhilai": _img_to_b64("bhilai.jpg"),
        "fumes": _img_to_b64("fumes.jpg"),
        "tank": _img_to_b64("tank.jpg"),
        "sewage": _img_to_b64("sewage.jpg"),
        "gas": _img_to_b64("gas.jpg"),
        "midc": _img_to_b64("midc.jpg"),
    }

    def bg(key: str) -> str:
        src = imgs.get(key, "")
        if src:
            return f'style="background-image:url(\'{src}\');"'
        return 'style="background:#0a0a0a;"'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
html,body{{
  background:#050709;
  color:white;
  overflow-x:hidden;
  font-family:'Playfair Display',serif;
  scroll-behavior:smooth;
}}
.panel{{
  height:100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  flex-direction:column;
  text-align:center;
  padding:24px;
  opacity:0.08;
  transform:scale(0.96);
  transition:opacity 1s ease, transform 1s ease;
  background-size:cover;
  background-position:center;
  background-repeat:no-repeat;
  position:relative;
}}
.panel::before{{
  content:"";
  position:absolute;
  inset:0;
  background:rgba(0,0,0,0.68);
  z-index:0;
}}
.panel h1,
.panel small,
.panel .tag,
.panel .badge{{
  position:relative;
  z-index:2;
}}
.panel.active{{
  opacity:1;
  transform:scale(1.03);
}}
h1{{
  font-size:clamp(1.6rem,4.5vw,3.8rem);
  letter-spacing:8px;
  text-transform:uppercase;
  font-weight:900;
  margin:0;
  line-height:1.2;
  color:#ff3b3b;
  text-shadow:0 0 30px rgba(255,59,59,0.55);
}}
.plain h1{{
  color:#e8edf5;
  text-shadow:none;
  letter-spacing:10px;
}}
.accent h1{{
  background:linear-gradient(135deg,#00d4ff 0%,#00ff9d 100%);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
  text-shadow:none;
}}
small{{
  font-family:'JetBrains Mono',monospace;
  font-size:clamp(0.7rem,1.8vw,0.95rem);
  letter-spacing:3px;
  color:#ffcccc;
  opacity:0.9;
  margin-top:14px;
  text-transform:uppercase;
  position:relative;
  z-index:2;
}}
.plain small{{color:#8a94a8;}}
.accent small{{color:#8a94a8;}}
.badge{{
  font-family:'JetBrains Mono',monospace;
  font-size:0.6rem;
  letter-spacing:0.22em;
  color:#5a6478;
  text-transform:uppercase;
  margin-bottom:10px;
}}
.tag{{
  display:inline-block;
  margin-top:14px;
  padding:0.2rem 0.9rem;
  border:1px solid rgba(255,59,59,0.45);
  border-radius:20px;
  font-family:'JetBrains Mono',monospace;
  font-size:0.58rem;
  color:#ff9999;
  letter-spacing:0.14em;
  background:rgba(255,59,59,0.06);
}}
.divider{{
  width:1px;
  height:50px;
  background:linear-gradient(to bottom,transparent,#ff3b3b,transparent);
  margin:18px auto 0;
  position:relative;
  z-index:2;
}}
.band{{
  width:230px;
  height:105px;
  background:#0d1117;
  border-radius:80px;
  margin-top:28px;
  border:1px solid rgba(0,212,255,0.3);
  box-shadow:0 0 60px rgba(0,212,255,0.15);
  transition:transform 1.2s ease,box-shadow 1.2s ease;
  position:relative;
  z-index:2;
}}
.product.active .band{{
  transform:scale(1.55);
  box-shadow:0 0 120px rgba(0,212,255,0.45);
}}
</style>
</head>
<body>

<!-- INTRO -->
<section class="panel plain">
  <div class="badge">Industrial Safety Intelligence · India</div>
  <h1>Most accidents don't begin with impact</h1>
</section>
<section class="panel plain">
  <h1>They begin with silence</h1>
  <div class="divider"></div>
</section>
<section class="panel plain">
  <h1>And no one notices</h1>
  <small>Until it's too late</small>
</section>

<!-- INCIDENTS -->
<section class="panel" {bg("sigachi")}>
  <div class="badge">Telangana · 2021</div>
  <h1>Sigachi Explosion</h1>
  <small>Pressure buildup → blast · 17 dead</small>
  <span class="tag">Unmonitored Reactor Pressure</span>
</section>

<section class="panel" {bg("lg")}>
  <div class="badge">Vizag · 2020</div>
  <h1>LG Polymers Leak</h1>
  <small>Temperature rise → toxic cloud · 12 dead</small>
  <span class="tag">No Real-Time Sensor Alert</span>
</section>

<section class="panel" {bg("ntpc")}>
  <div class="badge">Uttar Pradesh · 2017</div>
  <h1>NTPC Explosion</h1>
  <small>Boiler failure → blast · 26 killed</small>
  <span class="tag">Missed Early Warning Signal</span>
</section>

<section class="panel" {bg("neyveli")}>
  <div class="badge">Tamil Nadu · 2020</div>
  <h1>Neyveli Blast</h1>
  <small>High pressure boiler failure · 8 injured</small>
  <span class="tag">Unmonitored Pressure Spike</span>
</section>

<section class="panel" {bg("bhilai")}>
  <div class="badge">Chhattisgarh · 2019</div>
  <h1>Bhilai Pipeline</h1>
  <small>Gas rupture → fire</small>
  <span class="tag">No Gas Leak Detection Active</span>
</section>

<section class="panel" {bg("fumes")}>
  <div class="badge">Hyderabad · 2016</div>
  <h1>Toxic Fumes</h1>
  <small>Workers inhaled gas → unconscious · 2 dead</small>
  <span class="tag">VOC Threshold Exceeded Silently</span>
</section>

<section class="panel" {bg("tank")}>
  <div class="badge">Gujarat · 2018</div>
  <h1>Tank Suffocation</h1>
  <small>No ventilation → oxygen depletion · 4 dead</small>
  <span class="tag">No Confined Space O₂ Monitor</span>
</section>

<section class="panel" {bg("sewage")}>
  <div class="badge">Delhi · 2025</div>
  <h1>Sewage Collapse</h1>
  <small>Toxic gases → workers overcome</small>
  <span class="tag">No Wearable Detection Active</span>
</section>

<section class="panel" {bg("gas")}>
  <div class="badge">Anakapalli · 2025</div>
  <h1>Gas Exposure</h1>
  <small>Pharma gas leak → 2 dead, 1 critical</small>
  <span class="tag">Delayed Evacuation Protocol</span>
</section>

<section class="panel" {bg("midc")}>
  <div class="badge">Maharashtra · Recurring</div>
  <h1>Chemical Leaks</h1>
  <small>DMS gas leak → 13 hospitalised</small>
  <span class="tag">No Predictive AI Layer</span>
</section>

<!-- TRANSITION -->
<section class="panel plain">
  <h1>Different incidents</h1>
</section>
<section class="panel plain">
  <h1>Same root cause</h1>
  <div class="divider"></div>
</section>
<section class="panel plain">
  <h1>No early warning</h1>
  <small>Every single time</small>
</section>


<!-- FINAL -->
<section class="panel accent">
  <h1>We don't react</h1>
</section>
<section class="panel accent">
  <h1>We prevent</h1>
  <small>Powered by NEXUS GUARDIAN</small>
</section>

<script>
const panels=document.querySelectorAll(".panel");
function check(){{
  const sy=window.scrollY;
  panels.forEach(p=>{{
    const active=sy>p.offsetTop-p.offsetHeight/1.4;
    p.classList.toggle("active",active);
  }});
}}
window.addEventListener("scroll",check);
check();
</script>
</body>
</html>"""


def render(height: int = 650) -> None:
    """
    Embed the incident scrollytelling experience into Streamlit.
    Images are base64-encoded at render time so no static file server is needed.
    height: iframe height in pixels. Increase if content feels cut off.
    """
    import streamlit.components.v1 as components

    components.html(_build_html(), height=height, scrolling=True)
