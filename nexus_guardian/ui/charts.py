"""Plotly chart factory functions for NEXUS GUARDIAN."""
import plotly.graph_objects as go


def histogram_dark(data, title: str, color: str, nbins: int = 10) -> go.Figure:
    fig = go.Figure(go.Histogram(
        x=data, nbinsx=nbins, marker_color=color, opacity=0.9,
        marker_line_color='rgba(0,0,0,0.5)', marker_line_width=0.5,
        xbins=dict(start=0, end=100, size=10),
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(family="JetBrains Mono", size=10, color="#5a6478"), x=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d1d9", family="JetBrains Mono", size=10),
        margin=dict(l=32, r=8, t=32, b=32), height=180,
        xaxis=dict(range=[0, 100], gridcolor="#1e2530", zeroline=False, tickfont=dict(size=9)),
        yaxis=dict(gridcolor="#1e2530", zeroline=False, tickfont=dict(size=9)),
        bargap=0.08, showlegend=False,
    )
    return fig


def radar_chart(breakdown: dict) -> go.Figure:
    cats = list(breakdown.keys()) + [list(breakdown.keys())[0]]
    vals = list(breakdown.values()) + [list(breakdown.values())[0]]
    fig  = go.Figure(go.Scatterpolar(
        r=vals, theta=cats, fill='toself',
        fillcolor='rgba(255,107,53,0.15)',
        line=dict(color='#ff6b35', width=2),
        marker=dict(size=5, color='#ff6b35'),
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


def time_area(hist: list, key: str, color: str, title: str) -> go.Figure:
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    fig = go.Figure(go.Scatter(
        x=[h["tick"] for h in hist], y=[h[key] for h in hist],
        fill='tozeroy', fillcolor=f"rgba({r},{g},{b},0.12)",
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


def scatter_rad_vs_hr(hist: list) -> go.Figure:
    fig = go.Figure(go.Scatter(
        x=[h["radiation"] for h in hist],
        y=[h["hr"]        for h in hist],
        mode='markers',
        marker=dict(
            size=7, color=[h["exposure"] for h in hist],
            colorscale=[[0, '#00e676'], [0.5, '#ffd60a'], [1, '#ff3b3b']],
            showscale=True,
            colorbar=dict(title=dict(text="Exposure", font=dict(size=9, color='#5a6478')),
                          tickfont=dict(size=9, color='#5a6478'), thickness=10),
            line=dict(width=0.5, color='rgba(0,0,0,0.3)'), opacity=0.85,
        ),
    ))
    fig.update_layout(
        title=dict(text="Radiation (mSv/h) vs Heart Rate — coloured by exposure score",
                   font=dict(family="JetBrains Mono", size=10, color="#5a6478"), x=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#c9d1d9', family='JetBrains Mono', size=10),
        margin=dict(l=40, r=60, t=36, b=36), height=220,
        xaxis=dict(title=dict(text="Radiation mSv/h", font=dict(size=9, color='#5a6478')),
                   gridcolor='#1e2530', zeroline=False, tickfont=dict(size=9)),
        yaxis=dict(title=dict(text="Heart Rate BPM",   font=dict(size=9, color='#5a6478')),
                   gridcolor='#1e2530', zeroline=False, tickfont=dict(size=9)),
        showlegend=False,
    )
    return fig
