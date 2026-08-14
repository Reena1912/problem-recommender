import streamlit as st
import plotly.graph_objects as go
from ui.styles import (
    H,
    plotly_text_color,
    plotly_axis_color,
    plotly_grid_color,
)

def render_analytics(stats: dict):
    """Render 2 simple, intuitive, easy-to-understand interactive graphs."""
    H('''
    <div class="lc-container" id="analytics" style="margin-top:2rem;">
        <div class="lc-sec-hdr">
            <div class="lc-sec-num">03</div>
            <div>
                <div class="lc-sec-title">Skill Analytics & Practice Targets <span class="lc-sec-dash">—</span></div>
                <div class="lc-sec-sub">Simple breakdown of your weakest topics and difficulty progress</div>
            </div>
        </div>
    ''')

    ts = stats.get("tag_scores", [])
    sc = stats.get("solve_counts", {})
    
    if not ts:
        H('</div>')
        return

    sorted_ts = sorted(ts, key=lambda x: x["weakness_score"], reverse=True)

    col1, col2 = st.columns(2, gap="large")

    # GRAPH 1: Simple & Clear Top 8 Practice Targets (Horizontal Bar)
    with col1:
        H('<div style="font-size:0.85rem;font-weight:700;color:#132e28;margin-bottom:1rem;text-transform:uppercase;letter-spacing:0.08em;">📉 Top Topics Needing Practice</div>')
        
        top8_weak = sorted_ts[:8]
        tags = [t["tag"] for t in top8_weak]
        scores = [round(t["weakness_score"] * 100, 1) for t in top8_weak]

        fig1 = go.Figure(go.Bar(
            x=scores, y=tags,
            orientation="h",
            marker=dict(
                color=scores,
                colorscale=[[0, "#22c55e"], [0.5, "#eab308"], [1.0, "#132e28"]],
                line=dict(width=0)
            ),
            text=[f"  {s}% practice priority" for s in scores],
            textposition="outside",
            textfont=dict(size=11, color=plotly_text_color, family="Plus Jakarta Sans"),
            hovertemplate="<b>%{y}</b><br>Practice Priority: %{x}%<extra></extra>",
        ))

        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=120, t=10, b=10),
            height=360,
            yaxis=dict(
                autorange="reversed",
                tickfont=dict(color=plotly_axis_color, size=11, family="Plus Jakarta Sans"),
                gridcolor="rgba(0,0,0,0)"
            ),
            xaxis=dict(
                title=dict(text="Practice Priority (%)", font=dict(size=10, color=plotly_axis_color)),
                tickfont=dict(color=plotly_axis_color, size=10),
                gridcolor=plotly_grid_color,
                range=[0, 135]
            )
        )
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    # GRAPH 2: Simple & Clear Solved Breakdown by Difficulty (Donut Chart)
    with col2:
        H('<div style="font-size:0.85rem;font-weight:700;color:#132e28;margin-bottom:1rem;text-transform:uppercase;letter-spacing:0.08em;">🍰 Solved Problems by Difficulty</div>')
        
        easy_s = sc.get("Easy", 0)
        med_s = sc.get("Medium", 0)
        hard_s = sc.get("Hard", 0)
        total_s = sc.get("All", easy_s + med_s + hard_s)

        labels = ["Easy Solved", "Medium Solved", "Hard Solved"]
        values = [easy_s, med_s, hard_s]
        colors = ["#16a34a", "#d97706", "#dc2626"]

        fig2 = go.Figure(go.Pie(
            labels=labels,
            values=values,
            hole=0.62,
            marker=dict(colors=colors, line=dict(color="#ffffff", width=2)),
            textinfo="label+percent",
            textfont=dict(size=11, family="Plus Jakarta Sans"),
            hovertemplate="<b>%{label}</b><br>%{value} problems (%{percent})<extra></extra>",
        ))

        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.18,
                xanchor="center",
                x=0.5,
                font=dict(size=10, color=plotly_text_color)
            ),
            annotations=[{
                "text": f"<b>{total_s}</b><br><span style='font-size:11px;color:#566961;'>Total Solved</span>",
                "x": 0.5, "y": 0.5,
                "font": {"size": 22, "color": "#132e28", "family": "Outfit"},
                "showarrow": False
            }],
            margin=dict(l=20, r=20, t=10, b=30),
            height=360
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    H('</div>')
