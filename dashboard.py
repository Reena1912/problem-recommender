"""
LeetCode Recommender — Bold Editorial UI v5
Fixes: white text enforced everywhere, hero background image added.
"""

import streamlit as st
import requests
import plotly.graph_objects as go

import os
API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")


HERO_BG = "https://images.unsplash.com/photo-1555099962-4199c345e5dd?w=1600&q=80"

st.set_page_config(
    page_title="LeetCode Recommender",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700;900&display=swap');

/* ── GLOBAL RESET ── */
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}

/* Force white text everywhere Streamlit tries to go gray */
html,body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"]>.main,
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
section.main>.block-container,
div,p,span,li,a{{
    font-family:'Inter',sans-serif!important;
    background-color:transparent;
}}
/* Streamlit wraps all markdown in <p> tags - force white */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] div{{
    color:#ffffff!important;
}}

[data-testid="stAppViewContainer"]{{background:#0c0c0c!important;}}
[data-testid="stAppViewContainer"]>.main{{background:#0c0c0c!important;}}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"]{{display:none!important;}}
.block-container{{padding:0!important;max-width:100%!important;}}

/* ── NAV ── */
.lc-nav{{display:flex;align-items:center;justify-content:space-between;padding:1.3rem 4rem;border-bottom:1px solid #1f1f1f;background:#0c0c0c;position:sticky;top:0;z-index:100;}}
.lc-nav-logo{{font-family:'Bebas Neue',sans-serif!important;font-size:1.5rem;letter-spacing:0.08em;color:#ffffff!important;}}
.lc-nav-logo span{{color:#ff4d00!important;}}
.lc-nav-links{{display:flex;gap:2.5rem;font-size:0.82rem;font-weight:500;color:#888888!important;letter-spacing:0.04em;}}
.lc-nav-links span{{color:#888888!important;}}
.lc-nav-cta{{background:#ff4d00;color:#ffffff!important;font-weight:700;font-size:0.75rem;letter-spacing:0.08em;text-transform:uppercase;padding:0.55rem 1.3rem;border-radius:50px;border:none;}}

/* ── HERO ── */
.lc-hero{{
    position:relative;
    min-height:520px;
    padding:3.5rem 4rem 0;
    overflow:hidden;
    border-bottom:1px solid #1f1f1f;
    background-image:url('{HERO_BG}');
    background-size:cover;
    background-position:center 30%;
}}
/* Dark overlay so text pops over photo */
.lc-hero::before{{
    content:'';
    position:absolute;inset:0;
    background:linear-gradient(90deg,#0c0c0cee 0%,#0c0c0cbb 50%,#0c0c0c55 100%),
               linear-gradient(180deg,#0c0c0c22 0%,#0c0c0cdd 85%,#0c0c0c 100%);
    z-index:0;
}}
.lc-hero-glow{{position:absolute;top:-60px;right:-40px;width:500px;height:500px;background:radial-gradient(circle,#ff4d0030 0%,transparent 65%);pointer-events:none;z-index:1;}}
.lc-hero-content{{position:relative;z-index:2;}}
.lc-eyebrow{{font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:0.2em;color:#ff4d00!important;margin-bottom:1.2rem;display:flex;align-items:center;gap:0.7rem;}}
.lc-eyebrow-line{{display:inline-block;width:28px;height:2px;background:#ff4d00;flex-shrink:0;}}
.lc-hero-title{{font-family:'Bebas Neue',sans-serif!important;font-size:8rem;line-height:0.88;color:#ffffff!important;letter-spacing:0.01em;margin-bottom:1.5rem;}}
.lc-hero-title .orange{{color:#ff4d00!important;}}
.lc-hero-desc{{font-size:1rem;color:#cccccc!important;font-weight:300;line-height:1.7;max-width:420px;margin-bottom:2.5rem;}}
.lc-hero-right{{position:absolute;right:4rem;top:3.5rem;max-width:260px;text-align:right;z-index:2;}}
.lc-hero-right-q{{font-size:1.25rem;font-weight:700;color:#ffffff!important;line-height:1.35;margin-bottom:0.8rem;}}
.lc-hero-right-s{{font-size:0.8rem;color:#aaaaaa!important;line-height:1.65;}}
.lc-pillars{{display:flex;border-top:1px solid rgba(255,255,255,0.08);margin-top:2rem;position:relative;z-index:2;}}
.lc-pillar{{flex:1;padding:1.2rem 0;border-right:1px solid rgba(255,255,255,0.08);}}
.lc-pillar:last-child{{border-right:none;}}
.lc-pillar-num{{font-size:0.62rem;color:#ff4d00!important;font-weight:600;letter-spacing:0.1em;margin-bottom:0.3rem;}}
.lc-pillar-lbl{{font-size:0.75rem;color:#888888!important;}}

/* ── SEARCH STRIP ── */
.lc-search{{background:#111111;border-bottom:1px solid #1f1f1f;padding:1.4rem 4rem;}}
.lc-search-label{{font-size:0.68rem;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:#555555!important;white-space:nowrap;padding-top:0.75rem;}}
[data-testid="stTextInput"] input{{background:#1a1a1a!important;border:1px solid #2a2a2a!important;border-radius:7px!important;color:#ffffff!important;font-family:'Inter',sans-serif!important;font-size:0.95rem!important;padding:0.72rem 1.2rem!important;transition:border-color 0.2s,box-shadow 0.2s!important;}}
[data-testid="stTextInput"] input::placeholder{{color:#444444!important;}}
[data-testid="stTextInput"] input:focus{{border-color:#ff4d00!important;box-shadow:0 0 0 3px #ff4d0018!important;}}
[data-testid="stTextInput"] label{{display:none!important;}}

/* ── BUTTONS ── */
.stButton>button{{font-family:'Inter',sans-serif!important;font-weight:700!important;letter-spacing:0.06em!important;border-radius:7px!important;transition:all 0.2s!important;text-transform:uppercase!important;font-size:0.76rem!important;}}
.stButton>button[kind="primary"]{{background:#ff4d00!important;color:#ffffff!important;border:none!important;padding:0.72rem 1.4rem!important;}}
.stButton>button[kind="primary"]:hover{{background:#e04400!important;transform:translateY(-1px);box-shadow:0 8px 28px #ff4d0045!important;}}
.stButton>button[kind="secondary"]{{background:transparent!important;color:#666666!important;border:1px solid #2a2a2a!important;padding:0.72rem 1.1rem!important;}}
.stButton>button[kind="secondary"]:hover{{border-color:#ff4d00!important;color:#ff4d00!important;}}

/* ── STAT STRIP ── */
.lc-stats{{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid #1f1f1f;background:#0c0c0c;}}
.lc-stat{{padding:1.8rem 0 1.8rem 4rem;border-right:1px solid #1f1f1f;position:relative;}}
.lc-stat:last-child{{border-right:none;}}
.lc-stat::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;}}
.lc-stat.tot::before{{background:#ff4d00;}}
.lc-stat.ez::before{{background:#22c55e;}}
.lc-stat.md::before{{background:#f59e0b;}}
.lc-stat.hd::before{{background:#ef4444;}}
.lc-stat-tag{{font-size:0.62rem;font-weight:600;text-transform:uppercase;letter-spacing:0.14em;color:#444444!important;margin-bottom:0.5rem;}}
.lc-stat-num{{font-family:'Bebas Neue',sans-serif!important;font-size:3.8rem;line-height:1;color:#ffffff!important;}}
.lc-stat-of{{font-size:0.73rem;color:#444444!important;margin-top:0.2rem;}}
.lc-stat-pct{{display:inline-block;font-size:0.65rem;font-weight:700;padding:2px 9px;border-radius:3px;margin-top:0.5rem;letter-spacing:0.04em;text-transform:uppercase;}}
.p-tot{{background:#ff4d0015;color:#ff4d00!important;}}
.p-ez{{background:#22c55e15;color:#22c55e!important;}}
.p-md{{background:#f59e0b15;color:#f59e0b!important;}}
.p-hd{{background:#ef444415;color:#ef4444!important;}}

/* ── SECTIONS ── */
.lc-section{{padding:3rem 4rem;border-bottom:1px solid #1f1f1f;background:#0c0c0c;}}
.lc-sec-hdr{{display:flex;align-items:baseline;gap:1.5rem;margin-bottom:1.8rem;}}
.lc-sec-num{{font-family:'Bebas Neue',sans-serif!important;font-size:5rem;color:#161616;line-height:1;flex-shrink:0;}}
.lc-sec-title{{font-family:'Bebas Neue',sans-serif!important;font-size:2.2rem;color:#ffffff!important;letter-spacing:0.03em;line-height:1;}}
.lc-sec-title span{{color:#ff4d00!important;}}
.lc-sec-sub{{font-size:0.76rem;color:#555555!important;margin-top:0.3rem;}}

/* ── REC CARDS ── */
.lc-rcard{{background:#111111;border:1px solid #1f1f1f;border-radius:4px;padding:1.2rem 1.5rem;margin-bottom:0.55rem;position:relative;transition:border-color 0.2s,background 0.2s;}}
.lc-rcard:hover{{border-color:#2a2a2a;background:#141414;}}
.lc-rcard.active{{border-color:#ff4d00;background:#150c08;border-left-width:3px;}}
.lc-rcard-top{{display:flex;justify-content:space-between;align-items:flex-start;}}
.lc-rcard-idx{{font-family:'Bebas Neue',sans-serif!important;font-size:0.75rem;color:#2a2a2a!important;letter-spacing:0.1em;margin-bottom:0.3rem;}}
.lc-rcard-title{{font-size:0.98rem;font-weight:600;color:#ffffff!important;margin-bottom:0.45rem;}}
.lc-rcard-meta{{display:flex;gap:0.6rem;align-items:center;flex-wrap:wrap;}}
.lc-dbadge{{font-size:0.62rem;font-weight:700;padding:2px 8px;border-radius:3px;letter-spacing:0.06em;text-transform:uppercase;}}
.lc-de{{background:#22c55e12;color:#22c55e!important;border:1px solid #22c55e22;}}
.lc-dm{{background:#f59e0b12;color:#f59e0b!important;border:1px solid #f59e0b22;}}
.lc-dh{{background:#ef444412;color:#ef4444!important;border:1px solid #ef444422;}}
.lc-rmeta{{font-size:0.68rem;color:#444444!important;}}
.lc-tchip{{display:inline-block;font-size:0.62rem;background:#161616;color:#666666!important;padding:2px 7px;border-radius:3px;border:1px solid #222222;margin:2px 1px;}}
.lc-wsbar-wrap{{width:70px;height:3px;background:#1f1f1f;border-radius:2px;margin-top:0.35rem;margin-left:auto;}}
.lc-wsbar{{height:3px;background:#ff4d00;border-radius:2px;}}
.lc-wsscore{{font-family:'Bebas Neue',sans-serif!important;font-size:2rem;line-height:1;letter-spacing:0.02em;}}
.lc-wslbl{{font-size:0.58rem;color:#2a2a2a!important;text-transform:uppercase;letter-spacing:0.1em;}}

/* ── DETAIL PANEL ── */
.lc-dpanel{{background:#0e0e0e;border:1px solid #ff4d0022;border-radius:4px;padding:1.3rem 1.5rem;margin-bottom:0.55rem;}}
.lc-dpanel-hdr{{font-size:0.6rem;color:#333333!important;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:0.6rem;}}
.lc-dstats{{display:flex;gap:2.5rem;margin:0.7rem 0 1rem;}}
.lc-dstat-val{{font-family:'Bebas Neue',sans-serif!important;font-size:2rem;color:#ffffff!important;line-height:1;}}
.lc-dstat-lbl{{font-size:0.6rem;color:#444444!important;text-transform:uppercase;letter-spacing:0.1em;margin-top:0.2rem;}}
.lc-tags-lbl{{font-size:0.62rem;color:#333333!important;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;}}

/* ── WEAK TAG BAR ── */
.lc-weak-bar{{background:#110a06;border:1px solid #ff4d0018;border-left:3px solid #ff4d00;border-radius:4px;padding:0.7rem 1.1rem;margin-bottom:1.1rem;font-size:0.8rem;color:#888888!important;display:flex;align-items:center;gap:0.7rem;flex-wrap:wrap;}}

/* ── TABS ── */
[data-baseweb="tab-list"]{{background:#111111!important;border-radius:4px!important;padding:3px!important;border:1px solid #1f1f1f!important;gap:2px!important;margin-bottom:1.4rem;}}
[data-baseweb="tab"]{{border-radius:3px!important;color:#444444!important;font-family:'Inter',sans-serif!important;font-weight:600!important;font-size:0.72rem!important;text-transform:uppercase!important;letter-spacing:0.07em!important;padding:0.42rem 0.9rem!important;}}
[aria-selected="true"][data-baseweb="tab"]{{background:#1e1e1e!important;color:#ff4d00!important;}}

/* ── LINK BUTTON ── */
[data-testid="stLinkButton"] a{{background:#ff4d00!important;color:#ffffff!important;border-radius:6px!important;font-weight:700!important;border:none!important;font-size:0.72rem!important;letter-spacing:0.06em!important;text-transform:uppercase!important;}}

/* ── CHART LABEL ── */
.lc-chart-lbl{{font-size:0.62rem;color:#333333!important;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:0.8rem;padding-bottom:0.6rem;border-bottom:1px solid #1a1a1a;}}

/* ── FOOTER ── */
.lc-footer{{padding:1.8rem 4rem;display:flex;justify-content:space-between;align-items:center;border-top:1px solid #1f1f1f;background:#0c0c0c;}}
.lc-footer-logo{{font-family:'Bebas Neue',sans-serif!important;font-size:1.1rem;color:#222222!important;letter-spacing:0.08em;}}
.lc-footer-logo span{{color:#ff4d00!important;}}
.lc-footer-copy{{font-size:0.65rem;color:#222222!important;letter-spacing:0.06em;text-transform:uppercase;}}

hr{{border-color:#1f1f1f!important;margin:0!important;}}
[data-testid="stSpinner"]>div{{border-top-color:#ff4d00!important;}}
</style>""", unsafe_allow_html=True)


# ── API ────────────────────────────────────────────────────────────────────
def api(ep: str, method="GET") -> dict | None:
    try:
        url = f"{API_BASE}{ep}"
        r = requests.post(url, timeout=120) if method == "POST" else requests.get(url, timeout=35)
        if r.status_code == 200:
            return r.json()
        st.warning(f"⚠️ {r.json().get('detail', r.text)}")
        return None
    except requests.exceptions.ConnectionError:
        st.error("❌ API not reachable — run: uvicorn api.main:app --reload --reload-dir api")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱ Still loading — wait a moment and retry.")
        return None


def dc(d): return {"Easy": "lc-de", "Medium": "lc-dm", "Hard": "lc-dh"}.get(d, "lc-de")
def pct(s, t): return round(s / t * 100, 1) if t else 0
def H(html: str): st.markdown(html, unsafe_allow_html=True)


# ── NAV ───────────────────────────────────────────────────────────────────
def render_nav():
    H('<div class="lc-nav"><div class="lc-nav-logo">LeetCode<span>.</span>RECOMMENDER</div><div class="lc-nav-links"><span>Dashboard</span><span>Analytics</span><span>About</span></div><div class="lc-nav-cta">Get Started ●</div></div>')


# ── HERO ──────────────────────────────────────────────────────────────────
def render_hero(username: str | None):
    user_line = f'<div style="font-family:Bebas Neue,sans-serif;font-size:2rem;color:#ff4d00;letter-spacing:0.08em;margin-bottom:0.5rem;">@{username}</div>' if username else ""
    H(f'<div class="lc-hero"><div class="lc-hero-glow"></div><div class="lc-hero-right"><div class="lc-hero-right-q">Great practice should feel targeted.</div><div class="lc-hero-right-s">From tag analysis to ranked recommendations, we surface the problems your skill gaps need most.</div></div><div class="lc-hero-content"><div class="lc-eyebrow"><span class="lc-eyebrow-line"></span>Data-Driven Practice</div><div class="lc-hero-title">STOP<br>GRINDING<br><span class="orange">BLINDLY.</span></div>{user_line}<div class="lc-hero-desc">Know exactly which problems to solve next. We analyse your LeetCode profile and surface the gaps that matter most for your growth.</div></div><div class="lc-pillars"><div class="lc-pillar"><div class="lc-pillar-num">#01</div><div class="lc-pillar-lbl">Profile Analysis</div></div><div class="lc-pillar"><div class="lc-pillar-num">#02</div><div class="lc-pillar-lbl">Weakness Scoring</div></div><div class="lc-pillar"><div class="lc-pillar-num">#03</div><div class="lc-pillar-lbl">Problem Ranking</div></div><div class="lc-pillar"><div class="lc-pillar-num">#04</div><div class="lc-pillar-lbl">Deliberate Practice</div></div></div></div>')


# ── SEARCH ────────────────────────────────────────────────────────────────
def render_search():
    H('<div class="lc-search">')
    c1, c2, c3, c4 = st.columns([1.2, 6, 1.3, 0.9])
    with c1:
        H('<div class="lc-search-label">Your Username</div>')
    with c2:
        entered = st.text_input("u", value=st.session_state.get("username", ""),
                                placeholder="Enter LeetCode username…",
                                label_visibility="collapsed")
    with c3:
        go = st.button("Analyze →", use_container_width=True, type="primary")
    with c4:
        clear = st.button("Clear", use_container_width=True)
    H('</div>')

    if clear:
        st.session_state.clear(); st.rerun()
    if go and entered.strip():
        if st.session_state.get("username") != entered.strip():
            st.session_state.clear()
        st.session_state.username = entered.strip()
        st.rerun()


# ── STAT STRIP ────────────────────────────────────────────────────────────
def render_stats(stats: dict):
    sc, ta = stats["solve_counts"], stats["total_available"]
    rows = [
        ("tot","Total Solved", sc.get("All",0),    ta.get("All",0),    "p-tot"),
        ("ez", "Easy",         sc.get("Easy",0),   ta.get("Easy",0),   "p-ez"),
        ("md", "Medium",       sc.get("Medium",0), ta.get("Medium",0), "p-md"),
        ("hd", "Hard",         sc.get("Hard",0),   ta.get("Hard",0),   "p-hd"),
    ]
    cells = "".join(f'<div class="lc-stat {cls}"><div class="lc-stat-tag">{label}</div><div class="lc-stat-num">{s:,}</div><div class="lc-stat-of">out of {t:,} problems</div><span class="lc-stat-pct {pcls}">{pct(s,t)}% complete</span></div>' for cls,label,s,t,pcls in rows)
    H(f'<div class="lc-stats">{cells}</div>')


# ── RECOMMENDATIONS ───────────────────────────────────────────────────────
def render_recommendations(username: str):
    H('<div class="lc-section">')
    H('<div class="lc-sec-hdr"><div class="lc-sec-num">01</div><div><div class="lc-sec-title">Your Next <span>Problems</span></div><div class="lc-sec-sub">Ranked by how much they target your weakest algorithmic areas</div></div></div>')
    tabs = st.tabs(["✦ All", "🟢 Easy", "🟠 Medium", "🔴 Hard"])
    for tab, diff in zip(tabs, [None, "Easy", "Medium", "Hard"]):
        with tab:
            _rec_tab(username, diff)
    H('</div>')


def _rec_tab(username: str, difficulty: str | None):
    ep = (f"/recommend/{difficulty.lower()}?username={username}" if difficulty else f"/recommend?username={username}")
    pool_key = f"pool_{username}_{difficulty or 'all'}"
    sel_key  = f"sel_{username}_{difficulty or 'all'}"

    with st.spinner("Ranking problems…"):
        data = api(ep)
    if not data:
        return

    rec, weak_tags = data["recommendation"], data["your_weakest_tags"]

    if pool_key not in st.session_state: st.session_state[pool_key] = []
    if sel_key  not in st.session_state: st.session_state[sel_key]  = 0

    pool = st.session_state[pool_key]
    if rec["titleSlug"] not in {p["titleSlug"] for p in pool}:
        pool.insert(0, rec)

    tags_html = " ".join(f'<span class="lc-tchip" style="background:#1a0c06;color:#ff4d00!important;border-color:#ff4d0022;">{t}</span>' for t in weak_tags)
    H(f'<div class="lc-weak-bar"><span style="color:#888888!important;">📍 Targeting:</span> {tags_html}</div>')

    medals = ["01","02","03","04","05"]
    icons  = ["🥇","🥈","🥉","#4","#5"]

    for i, p in enumerate(pool[:5]):
        sel   = st.session_state[sel_key] == i
        ws    = p["weakness_score"]
        bar_w = int(ws * 100)
        t_chips = "".join(f'<span class="lc-tchip">{t}</span>' for t in p["tags"][:5])
        ws_color = "#ff4d00" if sel else "#252525"
        active_cls = "active" if sel else ""

        H(f'<div class="lc-rcard {active_cls}"><div class="lc-rcard-top"><div style="flex:1"><div class="lc-rcard-idx">{icons[i]} &nbsp;#{medals[i]}</div><div class="lc-rcard-title">{p["title"]}</div><div class="lc-rcard-meta"><span class="lc-dbadge {dc(p["difficulty"])}">{p["difficulty"]}</span><span class="lc-rmeta">Weakness&nbsp;{ws:.2f}</span><span class="lc-rmeta">·&nbsp;{p["acceptance_rate"]:.1f}% acceptance</span></div><div style="margin-top:0.5rem;">{t_chips}</div></div><div style="text-align:right;min-width:80px;flex-shrink:0;"><div class="lc-wsscore" style="color:{ws_color};">{bar_w}</div><div class="lc-wslbl">score</div><div class="lc-wsbar-wrap"><div class="lc-wsbar" style="width:{bar_w}%;"></div></div></div></div></div>')

        c1, c2 = st.columns([3, 1])
        with c1:
            lbl = "✓  Selected" if sel else "▶  Select This Problem"
            if st.button(lbl, key=f"b_{pool_key}_{i}", type="primary" if sel else "secondary", use_container_width=True):
                st.session_state[sel_key] = i
                st.rerun()
        with c2:
            st.link_button("Open ↗", f"https://leetcode.com/problems/{p['titleSlug']}/", use_container_width=True)

        if sel:
            all_tags = "".join(f'<span class="lc-tchip">{t}</span>' for t in p["tags"])
            H(f'<div class="lc-dpanel"><div class="lc-dpanel-hdr">Problem Breakdown</div><div class="lc-dstats"><div><div class="lc-dstat-val">{p["acceptance_rate"]:.1f}%</div><div class="lc-dstat-lbl">Acceptance</div></div><div><div class="lc-dstat-val">{bar_w}</div><div class="lc-dstat-lbl">Weakness Score</div></div><div><div class="lc-dstat-val">{p["difficulty"][:3].upper()}</div><div class="lc-dstat-lbl">Difficulty</div></div></div><div class="lc-tags-lbl">Topics</div><div style="margin-top:0.3rem;">{all_tags}</div></div>')


# ── ANALYTICS ─────────────────────────────────────────────────────────────
def render_analytics(stats: dict):
    H('<div class="lc-section">')
    H('<div class="lc-sec-hdr"><div class="lc-sec-num">02</div><div><div class="lc-sec-title">Skill <span>Analytics</span></div><div class="lc-sec-sub">Where you stand across all algorithmic domains</div></div></div>')

    ts = stats["tag_scores"]
    col1, col2 = st.columns(2, gap="large")

    with col1:
        H('<div class="lc-chart-lbl">📉 Weakest Areas</div>')
        weakest = ts[:12]
        fig = go.Figure(go.Bar(
            x=[t["weakness_score"] for t in weakest], y=[t["tag"] for t in weakest],
            orientation="h",
            marker=dict(color=[t["weakness_score"] for t in weakest],
                        colorscale=[[0,"#22c55e"],[0.45,"#f59e0b"],[1,"#ff4d00"]], line=dict(width=0)),
            text=[f"  {t['solved']}×" for t in weakest],
            textposition="outside", textfont=dict(size=9, color="#333333"),
            hovertemplate="<b>%{y}</b><br>Weakness: %{x:.2f}<extra></extra>",
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=50,t=0,b=0), height=370,
            yaxis=dict(autorange="reversed", tickfont=dict(color="#888888",size=10), gridcolor="#111111"),
            xaxis=dict(tickfont=dict(color="#333333",size=9), gridcolor="#161616", range=[0,1.2]),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
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
                radialaxis=dict(visible=True, range=[0,1], tickfont=dict(color="#222222",size=8), gridcolor="#1a1a1a", linecolor="#1a1a1a"),
                angularaxis=dict(tickfont=dict(color="#888888",size=9), gridcolor="#1a1a1a", linecolor="#1a1a1a"),
            ),
            margin=dict(l=50,r=50,t=20,b=20), height=370,
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    H('<div class="lc-chart-lbl" style="margin-top:1.5rem;">📊 Completion Progress</div>')
    sc, ta = stats["solve_counts"], stats["total_available"]
    dcols = st.columns(3)
    for col, (d, color) in zip(dcols, [("Easy","#22c55e"),("Medium","#f59e0b"),("Hard","#ef4444")]):
        s, t = sc.get(d, 0), ta.get(d, 1)
        p = pct(s, t)
        with col:
            fig = go.Figure(go.Pie(
                values=[s, max(0, t-s)], hole=0.74,
                marker_colors=[color,"#191919"], textinfo="none",
                hovertemplate="%{label}: %{value}<extra></extra>",
            ))
            fig.update_layout(showlegend=False, margin=dict(l=5,r=5,t=5,b=5), height=155,
                paper_bgcolor="rgba(0,0,0,0)",
                annotations=[{"text":f"<b>{p}%</b>","x":0.5,"y":0.5,"font":{"size":18,"color":color,"family":"Bebas Neue"},"showarrow":False}],
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            H(f'<div style="text-align:center;margin-top:-0.8rem;"><span style="font-size:0.7rem;font-weight:700;color:{color}!important;text-transform:uppercase;letter-spacing:0.08em;">{d}</span><br><span style="font-size:0.68rem;color:#333333!important;">{s:,} / {t:,}</span></div>')

    H('<div class="lc-chart-lbl" style="margin-top:1.8rem;">💪 Strongest Areas</div>')
    strongest = list(reversed(ts[-10:]))
    fig2 = go.Figure(go.Bar(
        x=[t["strength_score"] for t in strongest], y=[t["tag"] for t in strongest],
        orientation="h",
        marker=dict(color=[t["strength_score"] for t in strongest],
                    colorscale=[[0,"#1a1a1a"],[1,"#ff4d00"]], line=dict(width=0)),
        text=[f"  {t['solved']}×" for t in strongest],
        textposition="outside", textfont=dict(size=9, color="#333333"),
        hovertemplate="<b>%{y}</b><br>Strength: %{x:.2f}<extra></extra>",
    ))
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0,r=50,t=0,b=0), height=290,
        yaxis=dict(autorange="reversed", tickfont=dict(color="#888888",size=10)),
        xaxis=dict(tickfont=dict(color="#333333",size=9), gridcolor="#161616", range=[0,1.2]),
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    H('</div>')


# ── REFRESH ───────────────────────────────────────────────────────────────
def render_refresh(username: str):
    H('<div style="padding:1.5rem 4rem;border-bottom:1px solid #1f1f1f;background:#0c0c0c;">')
    _, mid, _ = st.columns([4, 2, 4])
    with mid:
        if st.button("🔄  Refresh LeetCode Data", use_container_width=True, type="primary"):
            with st.spinner("Re-fetching profile…"):
                res = api(f"/update?username={username}", method="POST")
                if res and res.get("success"):
                    for k in list(st.session_state.keys()):
                        if k.startswith(("pool_","sel_")):
                            del st.session_state[k]
                    st.success(f"✓ Updated — top pick: **{res['top_recommendation']}**")
                    st.rerun()
    H('</div>')


# ── FOOTER ────────────────────────────────────────────────────────────────
def render_footer():
    H('<div class="lc-footer"><div class="lc-footer-logo">LC<span>.</span>RECOMMENDER</div><div class="lc-footer-copy">Data from LeetCode GraphQL API</div></div>')


# ── MAIN ──────────────────────────────────────────────────────────────────
def main():
    username = st.session_state.get("username", "").strip()
    render_nav()
    render_hero(username or None)
    render_search()

    if not username:
        H('<div style="text-align:center;padding:5rem 2rem;border-bottom:1px solid #1f1f1f;background:#0c0c0c;"><div style="font-family:Bebas Neue,sans-serif;font-size:5rem;color:#161616;line-height:1;">ENTER USERNAME ABOVE</div><div style="font-size:0.82rem;color:#2a2a2a;margin-top:0.6rem;">First load takes ~15–25 s · Results cached 10 minutes</div></div>')
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
