import streamlit as st
import plotly.graph_objects as go
from ui.styles import (
    H,
    plotly_text_color,
    plotly_axis_color,
    plotly_grid_color,
    unsolved_pie_color,
)

def pct(s, t):
    return round(s / t * 100, 1) if t else 0

def render_analytics(stats: dict):
    """Render the user performance charts grid."""
    H('<div class="lc-section">')
    H('<div class="lc-sec-hdr"><div class="lc-sec-num">02</div><div><div class="lc-sec-title">Skill <span>Analytics</span></div><div class="lc-sec-sub">Where you stand across all algorithmic domains</div></div></div>')

    ts = stats["tag_scores"]
    
    # ROW 1: Weakest Areas & Strongest Areas side-by-side
    col1, col2 = st.columns(2, gap="large")

    with col1:
        H('<div class="lc-chart-lbl">📉 Weakest Areas (Top 10)</div>')
        weakest = ts[:10]
        fig = go.Figure(go.Bar(
            x=[t["weakness_score"] for t in weakest], y=[t["tag"] for t in weakest],
            orientation="h",
            marker=dict(color=[t["weakness_score"] for t in weakest],
                        colorscale=[[0,"#22c55e"],[0.45,"#f59e0b"],[1,"#ff4d00"]], line=dict(width=0)),
            text=[f"  {t['solved']} solved" for t in weakest],
            textposition="outside", textfont=dict(size=9, color=plotly_text_color),
            hovertemplate="<b>%{y}</b><br>Weakness: %{x:.2f}<extra></extra>",
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=70,t=10,b=10), height=320,
            yaxis=dict(autorange="reversed", tickfont=dict(color=plotly_axis_color,size=10), gridcolor="rgba(0,0,0,0)"),
            xaxis=dict(tickfont=dict(color=plotly_axis_color,size=9), gridcolor=plotly_grid_color, range=[0,1.3]),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        H('<div class="lc-chart-lbl">💪 Strongest Areas (Top 10)</div>')
        strongest = list(reversed(ts[-10:]))
        fig2 = go.Figure(go.Bar(
            x=[t["strength_score"] for t in strongest], y=[t["tag"] for t in strongest],
            orientation="h",
            marker=dict(color=[t["strength_score"] for t in strongest],
                        colorscale=[[0,unsolved_pie_color],[1,"#ff4d00"]], line=dict(width=0)),
            text=[f"  {t['solved']} solved" for t in strongest],
            textposition="outside", textfont=dict(size=9, color=plotly_text_color),
            hovertemplate="<b>%{y}</b><br>Strength: %{x:.2f}<extra></extra>",
        ))
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=70,t=10,b=10), height=320,
            yaxis=dict(autorange="reversed", tickfont=dict(color=plotly_axis_color,size=10), gridcolor="rgba(0,0,0,0)"),
            xaxis=dict(tickfont=dict(color=plotly_axis_color,size=9), gridcolor=plotly_grid_color, range=[0,1.3]),
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    H('<div style="margin-top: 2rem;"></div>')

    # ROW 2: Skill Radar & Completion Progress side-by-side
    col3, col4 = st.columns(2, gap="large")

    with col3:
        H('<div class="lc-chart-lbl">🕸 Skill Radar — Top 8 Topics</div>')
        top8 = sorted(ts, key=lambda x: x["solved"], reverse=True)[:8]
        labs = [t["tag"] for t in top8] + [top8[0]["tag"]]
        vals = [t["strength_score"] for t in top8] + [top8[0]["strength_score"]]
        fig3 = go.Figure(go.Scatterpolar(
            r=vals, theta=labs, fill="toself",
            fillcolor="rgba(255,77,0,0.08)",
            line=dict(color="#ff4d00", width=2),
            marker=dict(color="#ff4d00", size=5),
            hovertemplate="<b>%{theta}</b><br>%{r:.2f}<extra></extra>",
        ))
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",
            polar=dict(bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0,1], tickfont=dict(color=plotly_axis_color,size=8), gridcolor=plotly_grid_color, linecolor=plotly_grid_color),
                angularaxis=dict(tickfont=dict(color=plotly_axis_color,size=9), gridcolor=plotly_grid_color, linecolor=plotly_grid_color),
            ),
            margin=dict(l=50,r=50,t=20,b=20), height=320,
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    with col4:
        H('<div class="lc-chart-lbl">📊 Completion Progress</div>')
        sc, ta = stats["solve_counts"], stats["total_available"]
        dcols = st.columns(3)
        for col, (d, color) in zip(dcols, [("Easy","#22c55e"),("Medium","#f59e0b"),("Hard","#ef4444")]):
            s, t = sc.get(d, 0), ta.get(d, 1)
            p = pct(s, t)
            with col:
                fig = go.Figure(go.Pie(
                    values=[s, max(0, t-s)], hole=0.74,
                    marker_colors=[color,unsolved_pie_color], textinfo="none",
                    hovertemplate="%{label}: %{value}<extra></extra>",
                ))
                fig.update_layout(showlegend=False, margin=dict(l=5,r=5,t=5,b=5), height=140,
                    paper_bgcolor="rgba(0,0,0,0)",
                    annotations=[{"text":f"<b>{p}%</b>","x":0.5,"y":0.5,"font":{"size":18,"color":color,"family":"Bebas Neue"},"showarrow":False}],
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                H(f'<div style="text-align:center;margin-top:-0.5rem;"><span style="font-size:0.75rem;font-weight:700;color:{color}!important;text-transform:uppercase;letter-spacing:0.08em;">{d}</span><br><span style="font-size:0.75rem;color:var(--text-muted)!important;font-weight:500;">{s:,} / {t:,}</span></div>')

    H('</div>')
