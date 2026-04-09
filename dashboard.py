import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LeetCode Recommender",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def call_api(endpoint: str, method: str = "GET") -> dict | None:
    try:
        if method == "POST":
            response = requests.post(f"{API_BASE}{endpoint}", timeout=120)
        else:
            response = requests.get(f"{API_BASE}{endpoint}", timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API error {response.status_code}: {response.text}")
            return None

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Make sure uvicorn is running on port 8000.")
        return None
    except requests.exceptions.Timeout:
        st.error("Request timed out.")
        return None


def difficulty_color(difficulty: str) -> str:
    colors = {
        "Easy": "green",
        "Medium": "orange", 
        "Hard": "red"
    }
    return colors.get(difficulty, "gray")


def render_recommendation_card(data: dict):
    rec = data["recommendation"]
    weak_tags = data["your_weakest_tags"]
    message = data["message"]

    st.markdown("## 🎯 Your Next Problem")
    st.caption(message)

    col1, col2 = st.columns([2, 1])

    with col1:
        difficulty = rec["difficulty"]
        color = difficulty_color(difficulty)

        st.markdown(f"### [{rec['title']}]({rec['leetcode_url']})")
        st.markdown(
            f"**Difficulty:** :{color}[{difficulty}] &nbsp;&nbsp; "
            f"**Acceptance Rate:** {rec['acceptance_rate']:.1f}% &nbsp;&nbsp; "
            f"**Weakness Score:** {rec['weakness_score']:.2f}"
        )

        st.markdown("**Tags:**")
        tags_html = " ".join([
            f"<span style='background-color:#1e1e2e; padding:3px 10px; "
            f"border-radius:12px; margin:3px; font-size:13px; "
            f"border:1px solid #444;'>{tag}</span>"
            for tag in rec["tags"]
        ])
        st.markdown(tags_html, unsafe_allow_html=True)

    with col2:
        st.markdown("**Your weakest areas right now:**")
        for i, tag in enumerate(weak_tags, 1):
            st.markdown(f"{i}. {tag}")

        st.markdown("")
        st.link_button(
            "Open Problem on LeetCode →",
            rec["leetcode_url"],
            use_container_width=True
        )
def render_weak_tags_chart():
    st.markdown("## 📊 Your Weak Areas")

    path = os.path.join("data", "processed", "tag_scores.json")
    if not os.path.exists(path):
        st.warning("tag_scores.json not found. Run Phase 1 scripts first.")
        return

    with open(path, "r") as f:
        tag_scores = json.load(f)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 10 weakest tags")
        weakest = tag_scores[:10]
        tags = [t["tag"] for t in weakest]
        scores = [t["weakness_score"] for t in weakest]

        fig = px.bar(
            x=scores,
            y=tags,
            orientation="h",
            labels={"x": "Weakness Score", "y": "Tag"},
            color=scores,
            color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"],
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=0, b=0),
            yaxis=dict(autorange="reversed"),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Top 10 strongest tags")
        strongest = list(reversed(tag_scores[-10:]))
        tags_s = [t["tag"] for t in strongest]
        scores_s = [t["strength_score"] for t in strongest]

        fig2 = px.bar(
            x=scores_s,
            y=tags_s,
            orientation="h",
            labels={"x": "Strength Score", "y": "Tag"},
            color=scores_s,
            color_continuous_scale=["#f39c12", "#2ecc71"],
        )
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=0, b=0),
            yaxis=dict(autorange="reversed"),
            height=350
        )
        st.plotly_chart(fig2, use_container_width=True)

def render_difficulty_chart():
    st.markdown("## 📈 Your Progress by Difficulty")

    path = os.path.join("data", "processed", "problems_clean.json")
    if not os.path.exists(path):
        st.warning("problems_clean.json not found. Run Phase 1 scripts first.")
        return

    with open(path, "r") as f:
        clean = json.load(f)

    solve_counts = clean["solve_counts"]
    total_available = clean["total_available"]

    difficulties = ["Easy", "Medium", "Hard"]
    solved = [solve_counts.get(d, 0) for d in difficulties]
    total = [total_available.get(d, 0) for d in difficulties]
    remaining = [max(0, t - s) for t, s in zip(total, solved)]
    percentages = [
        round((s / t * 100), 1) if t > 0 else 0
        for s, t in zip(solved, total)
    ]

    col1, col2, col3 = st.columns(3)
    colors = ["#2ecc71", "#f39c12", "#e74c3c"]

    for col, diff, s, t, pct, color in zip(
        [col1, col2, col3], difficulties, solved, total, percentages, colors
    ):
        with col:
            st.markdown(f"#### {diff}")
            fig = go.Figure(go.Pie(
                values=[s, max(0, t - s)],
                labels=["Solved", "Remaining"],
                hole=0.65,
                marker_colors=[color, "#2a2a3e"],
                textinfo="none",
                hovertemplate="%{label}: %{value}<extra></extra>"
            ))
            fig.update_layout(
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10),
                height=200,
                paper_bgcolor="rgba(0,0,0,0)",
                annotations=[{
                    "text": f"<b>{pct}%</b>",
                    "x": 0.5, "y": 0.5,
                    "font_size": 22,
                    "showarrow": False
                }]
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                f"<div style='text-align:center; font-size:14px; "
                f"color:gray;'>{s} / {t} solved</div>",
                unsafe_allow_html=True
            )
def render_controls():
    st.markdown("---")
    st.markdown("## ⚙️ Controls")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🎲 Any difficulty", use_container_width=True):
            st.session_state.difficulty_filter = None
            st.rerun()

    with col2:
        if st.button("🟢 Easy", use_container_width=True):
            st.session_state.difficulty_filter = "easy"
            st.rerun()

    with col3:
        if st.button("🟠 Medium", use_container_width=True):
            st.session_state.difficulty_filter = "medium"
            st.rerun()

    with col4:
        if st.button("🔴 Hard", use_container_width=True):
            st.session_state.difficulty_filter = "hard"
            st.rerun()

    st.markdown("")

    if st.button(
        "🔄 Refresh — re-scrape LeetCode and retrain model",
        use_container_width=True,
        type="primary"
    ):
        with st.spinner("Fetching your latest LeetCode data and retraining... (this takes ~60 seconds)"):
            result = call_api("/update", method="POST")
            if result and result.get("success"):
                st.success(f"Updated! New top recommendation: {result['top_recommendation']}")
                st.rerun()
                
def main():
    st.markdown(
        "<h1 style='text-align:center;'>🧠 LeetCode Recommender</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:gray;'>Deliberate practice — "
        "solve the right problem, not just any problem.</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    if "difficulty_filter" not in st.session_state:
        st.session_state.difficulty_filter = None

    difficulty = st.session_state.difficulty_filter
    if difficulty:
        endpoint = f"/recommend/{difficulty}"
    else:
        endpoint = "/recommend"

    with st.spinner("Loading recommendation..."):
        data = call_api(endpoint)

    if data:
        render_recommendation_card(data)

    st.markdown("---")
    render_weak_tags_chart()
    render_difficulty_chart()
    render_controls()


if __name__ == "__main__":
    main()