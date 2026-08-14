import streamlit as st
from ui.styles import H, HERO_IMG_1, HERO_IMG_2, HERO_IMG_3
from ui.client import api

def pct(s, t):
    return round(s / t * 100, 1) if t else 0

def render_nav():
    """Render top navigation header matching the reference design."""
    H('''
    <div class="lc-nav-wrap">
        <div class="lc-container">
            <div class="lc-nav">
                <div class="lc-nav-logo">ALGO<span style="color:#22c55e;">.</span>MATCH</div>
                <div class="lc-nav-links">
                    <a href="#">Dashboard</a>
                    <a href="#process">Methodology</a>
                    <a href="#analytics">Analytics</a>
                    <a href="https://leetcode-recommender-api.onrender.com/docs" target="_blank">API Docs</a>
                </div>
                <a href="#search" class="lc-nav-cta">Analyze Profile</a>
            </div>
        </div>
    </div>
    ''')

def render_hero(username: str | None):
    """Render hero section with stadium arch visual cards and metric pill strip."""
    user_badge = f'<div style="font-family:Outfit,sans-serif;font-size:1.1rem;font-weight:700;color:#132e28;background:#dce8e0;padding:0.4rem 1.2rem;border-radius:50px;display:inline-block;margin-bottom:1rem;">Active Profile: @{username}</div>' if username else ""
    
    H(f'''
    <div class="lc-hero-section">
        <div class="lc-container">
            <div class="lc-hero-grid">
                <div>
                    <div class="lc-eyebrow"><span class="lc-eyebrow-line"></span>Data-Driven Practice Platform</div>
                    <div class="lc-hero-title">
                        Stop grinding blindly.<br>
                        Target your exact skill gaps.
                    </div>
                    {user_badge}
                    <div class="lc-hero-desc">
                        An intelligent, production-ready system that analyzes any LeetCode profile, detects algorithmic blind spots, and recommends the most impactful problems to solve next — backed by data-driven weakness scoring.
                    </div>
                    <div class="lc-hero-actions">
                        <a href="#search" class="lc-btn-pill-primary">Get Started Now →</a>
                        <a href="https://leetcode-recommender-api.onrender.com/docs" target="_blank" class="lc-btn-pill-sec">Explore API Docs ↗</a>
                    </div>
                </div>
                
                <div class="lc-stadium-grid">
                    <span class="lc-sparkle" style="top:-10px;left:20px;">✦</span>
                    <span class="lc-sparkle" style="bottom:10px;right:30px;">✦</span>
                    
                    <div class="lc-stadium-card">
                        <img src="{HERO_IMG_1}" alt="Algorithm Analysis">
                    </div>
                    <div class="lc-stadium-card">
                        <img src="{HERO_IMG_2}" alt="Developer Workspace">
                    </div>
                    <div class="lc-stadium-card">
                        <img src="{HERO_IMG_3}" alt="Data Visualization">
                    </div>
                </div>
            </div>
            
            <div class="lc-metrics-banner">
                <span>⚡ 3,900+ Catalog Problems</span>
                <span>✦ Sub-Second Caching</span>
                <span>⚡ LeetCode GraphQL Sync</span>
                <span>✦ Data-Driven Weakness Scoring</span>
            </div>
        </div>
    </div>
    ''')

def render_process():
    """Render the 3-step practice methodology section."""
    H('''
    <div class="lc-container" id="process">
        <div class="lc-sec-hdr">
            <div class="lc-sec-num">01</div>
            <div>
                <div class="lc-sec-title">A simple, yet effective three step process <span class="lc-sec-dash">—</span></div>
                <div class="lc-sec-sub">How our recommendation engine pinpoints your exact algorithmic weakness</div>
            </div>
        </div>
        
        <div class="lc-process-grid">
            <div class="lc-process-card active-step">
                <div class="lc-step-tag">01.</div>
                <div class="lc-step-title">Profile Analysis</div>
                <div class="lc-step-desc">We fetch real-time solved counts and tag distributions from LeetCode GraphQL API with exponential backoff retries.</div>
            </div>
            <div class="lc-process-card">
                <div class="lc-step-tag">02.</div>
                <div class="lc-step-title">Weakness Scoring</div>
                <div class="lc-step-desc">Calculates a normalized weakness coefficient (0.0 to 1.0) for 40+ algorithmic topics relative to your top strengths.</div>
            </div>
            <div class="lc-process-card">
                <div class="lc-step-tag">03.</div>
                <div class="lc-step-title">Precision Ranking</div>
                <div class="lc-step-desc">Ranks 3,900+ unsolved catalog problems and surfaces the highest-value Easy, Medium, or Hard questions to practice.</div>
            </div>
        </div>
    </div>
    ''')

def render_search():
    """Render unified username search card with quick presets cleanly inside st.form container."""
    H('<div class="lc-container" id="search">')
    
    with st.form(key="search_form", border=True):
        st.markdown('''
        <div style="margin-bottom: 1rem;">
            <div class="lc-search-title">Analyze Any LeetCode Profile</div>
            <div class="lc-search-sub">Enter a username below to calculate weakness scores across 40+ algorithmic topics.</div>
        </div>
        ''', unsafe_allow_html=True)
        
        c1, c2 = st.columns([4.5, 1.2])
        with c1:
            entered = st.text_input("u", value=st.session_state.get("username") or "",
                                    placeholder="e.g. neetcode, tourist, or NovaAsher…",
                                    label_visibility="collapsed")
        with c2:
            go = st.form_submit_button("Analyze Profile →", type="primary", use_container_width=True)

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

    H('</div>')

def render_stats(stats: dict):
    """Render user stat counter cards in a SINGLE HORIZONTAL LINE (4 cards side-by-side in 1 row using Streamlit columns)."""
    sc, ta = stats["solve_counts"], stats["total_available"]
    rows = [
        ("Total Solved", sc.get("All",0),    ta.get("All",0),    "sb-tot"),
        ("Easy Solved",  sc.get("Easy",0),   ta.get("Easy",0),   "sb-ez"),
        ("Medium Solved",sc.get("Medium",0), ta.get("Medium",0), "sb-md"),
        ("Hard Solved",  sc.get("Hard",0),   ta.get("Hard",0),   "sb-hd"),
    ]
    
    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]
    
    for (label, s, t, bcls), col in zip(rows, cols):
        p = pct(s, t)
        with col:
            st.markdown(
                f'<div class="lc-stat-card" style="margin-bottom:0!important;">'
                f'<div class="lc-stat-hdr"><span class="lc-stat-title">{label}</span><span class="lc-stat-badge {bcls}">{p}%</span></div>'
                f'<div class="lc-stat-val">{s:,}</div>'
                f'<div class="lc-stat-sub">out of {t:,} available problems</div>'
                f'</div>',
                unsafe_allow_html=True
            )

def render_footer():
    """Render deep forest green footer with AlgoMatch branding."""
    H('''
    <div style="background:#132e28; padding:3rem 0 2.5rem; margin-top:4rem; border-top:1px solid #1e3a34;">
        <div class="lc-container">
            <div class="lc-footer-bottom" style="border-top:none!important; padding-top:0!important;">
                <div class="lc-footer-logo">ALGO<span style="color:#22c55e;">.</span>MATCH</div>
                <div class="lc-footer-copy">Data from LeetCode GraphQL API · Weakness-Score Ranking Engine · Built with ⚡</div>
            </div>
        </div>
    </div>
    ''')
