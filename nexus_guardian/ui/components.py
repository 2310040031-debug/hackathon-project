"""Reusable HTML snippet builders for NEXUS GUARDIAN UI."""


def hex_to_rgb(h: str) -> tuple:
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def score_class(v: float) -> str:
    return "agent-score-safe" if v < 33 else ("agent-score-warn" if v < 65 else "agent-score-danger")


def score_color(v: float) -> str:
    return "#00e676" if v < 33 else ("#ffd60a" if v < 65 else "#ff3b3b")


def badge_type(status: str) -> str:
    s = status.lower()
    if any(x in s for x in ["optimal", "fit", "nominal", "safe", "minimal", "low", "continue"]):
        return "safe"
    if any(x in s for x in ["advisory", "caution", "warning", "moderate", "elevated", "reduce"]):
        return "warning"
    if any(x in s for x in ["rotate", "rotation", "at risk"]):
        return "rotate"
    return "critical"


def badge_html(text: str, btype: str) -> str:
    return f'<span class="badge b-{btype}">{text}</span>'


def sensor_card(label: str, value: float, unit: str, limit: float, css_class: str = "info") -> str:
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


def risk_bar_row(label: str, value: float) -> str:
    color = score_color(value)
    return (f'<div class="risk-row">'
            f'<div class="risk-label">{label}</div>'
            f'<div class="risk-track"><div class="risk-fill" style="width:{value:.0f}%;background:{color};"></div></div>'
            f'<div class="risk-num" style="color:{color};">{value:.0f}</div>'
            f'</div>')
