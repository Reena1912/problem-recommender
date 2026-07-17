"""
LeetCode Recommender — Bold Editorial UI v5
Clean entrypoint orchestrating modular UI subcomponents.
"""

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from ui.styles import inject_styles, H
from ui.client import api
from ui.components import (
    render_nav,
    render_hero,
    render_search,
    render_stats,
    render_footer,
)
from ui.recommendations import render_recommendations, render_refresh
from ui.analytics import render_analytics

# Set up Streamlit Page configuration
st.set_page_config(
    page_title="LeetCode Recommender",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject custom layout styles
inject_styles()

def main():
    # Handle HTML problem selection redirect
    if "select" in st.query_params:
        username = (st.session_state.get("username") or "").strip()
        diff = st.query_params.get("diff", "all")
        sel_key = f"sel_{username}_{diff}"
        st.session_state[sel_key] = int(st.query_params["select"])
        st.query_params.clear()
        st.rerun()

    username = (st.session_state.get("username") or "").strip()
    render_nav()
    render_hero(username or None)
    render_search()

    if not username:
        H('<div style="text-align:center;padding:5rem 2rem;border-bottom:1px solid var(--card-border);background:var(--bg-color);"><div style="font-family:Bebas Neue,sans-serif;font-size:5rem;color:var(--sec-num-color);line-height:1;">ENTER USERNAME ABOVE</div><div style="font-size:0.82rem;color:var(--text-muted);margin-top:0.6rem;">First load takes ~15–25 s · Results cached 10 minutes</div></div>')
        render_footer()
        return

    with st.spinner(f"Fetching @{username}'s LeetCode profile…"):
        stats = api(f"/stats?username={username}")
    if not stats:
        render_footer()
        return

    render_stats(stats)
    render_recommendations(username)
    render_analytics(stats)
    render_refresh(username)
    render_footer()

if __name__ == "__main__":
    main()