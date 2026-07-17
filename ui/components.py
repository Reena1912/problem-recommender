import streamlit as st
from ui.styles import H

def pct(s, t):
    return round(s / t * 100, 1) if t else 0

def render_nav():
    """Render the standard navigation header."""
    H(f'<div class="lc-nav"><div class="lc-nav-logo">LC<span>.</span>RECOMMENDER</div><div class="lc-nav-links"><span>Dashboard</span><span>Analytics</span><span>About</span></div></div>')

def render_hero(username: str | None):
    """Render the hero section with the background graphic."""
    user_line = f'<div style="font-family:Bebas Neue,sans-serif;font-size:2rem;color:#ff4d00;letter-spacing:0.08em;margin-bottom:0.5rem;">@{username}</div>' if username else ""
    H(f'<div class="lc-hero"><div class="lc-hero-glow"></div><div class="lc-hero-right"><div class="lc-hero-right-q">Great practice should feel targeted.</div><div class="lc-hero-right-s">From tag analysis to ranked recommendations, we surface the problems your skill gaps need most.</div></div><div class="lc-hero-content"><div class="lc-eyebrow"><span class="lc-eyebrow-line"></span>Data-Driven Practice</div><div class="lc-hero-title">STOP<br>GRINDING<br><span class="orange">BLINDLY.</span></div>{user_line}<div class="lc-hero-desc">Know exactly which problems to solve next. We analyse your LeetCode profile and surface the gaps that matter most for your growth.</div></div><div class="lc-pillars"><div class="lc-pillar"><div class="lc-pillar-num">#01</div><div class="lc-pillar-lbl">Profile Analysis</div></div><div class="lc-pillar"><div class="lc-pillar-num">#02</div><div class="lc-pillar-lbl">Weakness Scoring</div></div><div class="lc-pillar"><div class="lc-pillar-num">#03</div><div class="lc-pillar-lbl">Problem Ranking</div></div><div class="lc-pillar"><div class="lc-pillar-num">#04</div><div class="lc-pillar-lbl">Deliberate Practice</div></div></div></div>')

def render_search():
    """Render the username search input form and handle clear/submit triggers."""
    H('<div class="lc-search">')
    c1, c2, c3, c4 = st.columns([1.2, 6, 1.3, 0.9])
    with c1:
        H('<div class="lc-search-label">Your Username</div>')
    with c2:
        entered = st.text_input("u", value=st.session_state.get("username") or "",
                                placeholder="Enter LeetCode username…",
                                label_visibility="collapsed")
    with c3:
        go = st.button("Analyze →", use_container_width=True, type="primary")
    with c4:
        clear = st.button("Clear", use_container_width=True)
    H('</div>')

    if clear:
        auth_user = st.session_state.get("auth_user")
        theme = st.session_state.get("theme")
        st.session_state.clear()
        if auth_user:
            st.session_state["auth_user"] = auth_user
        if theme:
            st.session_state["theme"] = theme
        st.rerun()
    if go and entered.strip():
        if (st.session_state.get("username") or "") != entered.strip():
            auth_user = st.session_state.get("auth_user")
            theme = st.session_state.get("theme")
            st.session_state.clear()
            if auth_user:
                st.session_state["auth_user"] = auth_user
            if theme:
                st.session_state["theme"] = theme
        st.session_state.username = entered.strip()
        st.rerun()

def render_stats(stats: dict):
    """Render the user stats counters."""
    sc, ta = stats["solve_counts"], stats["total_available"]
    rows = [
        ("tot","Total Solved", sc.get("All",0),    ta.get("All",0),    "p-tot"),
        ("ez", "Easy",         sc.get("Easy",0),   ta.get("Easy",0),   "p-ez"),
        ("md", "Medium",       sc.get("Medium",0), ta.get("Medium",0), "p-md"),
        ("hd", "Hard",         sc.get("Hard",0),   ta.get("Hard",0),   "p-hd"),
    ]
    cells = "".join(f'<div class="lc-stat {cls}"><div class="lc-stat-tag">{label}</div><div class="lc-stat-num">{s:,}</div><div class="lc-stat-of">out of {t:,} problems</div><span class="lc-stat-pct {pcls}">{pct(s,t)}% complete</span></div>' for cls,label,s,t,pcls in rows)
    H(f'<div class="lc-stats">{cells}</div>')

def render_footer():
    """Render the bottom copy section."""
    H('<div class="lc-footer"><div class="lc-footer-logo">LC<span>.</span>RECOMMENDER</div><div class="lc-footer-copy">Data from LeetCode GraphQL API · Weakness-Score Ranking · Built with ⚡</div></div>')
