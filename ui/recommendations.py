import streamlit as st
from ui.styles import H
from ui.client import api

def dc(d):
    """Map difficulty keys to CSS styles."""
    return {"Easy": "lc-de", "Medium": "lc-dm", "Hard": "lc-dh"}.get(d, "lc-de")

def render_recommendations(username: str):
    """Render difficulty tabs and call sub-renderers."""
    H('<div class="lc-section">')
    H('<div class="lc-sec-hdr"><div class="lc-sec-num">01</div><div><div class="lc-sec-title">Your Next <span>Problems</span></div><div class="lc-sec-sub">Ranked by how much they target your weakest algorithmic areas</div></div></div>')
    tabs = st.tabs(["✦ All", "🟢 Easy", "🟠 Medium", "🔴 Hard"])
    for tab, diff in zip(tabs, [None, "Easy", "Medium", "Hard"]):
        with tab:
            _rec_tab(username, diff)
    H('</div>')

def _rec_tab(username: str, difficulty: str | None):
    """Fetch recommendations from backend API and render problem list cards."""
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

    tags_html = " ".join(f'<span class="lc-weak-tchip">{t}</span>' for t in weak_tags)
    H(f'<div class="lc-weak-bar"><span style="color:var(--text-muted)!important;">📍 Targeting:</span> {tags_html}</div>')

    medals = ["01","02","03","04","05"]
    icons  = ["🥇","🥈","🥉","#4","#5"]

    for i, p in enumerate(pool[:5]):
        sel = st.session_state[sel_key] == i
        
        # Action links inside card top header
        open_link = f'<a href="https://leetcode.com/problems/{p["titleSlug"]}/" target="_blank" class="lc-card-action-btn">Open ↗</a>'
        
        if sel:
            select_link = '<span class="lc-card-selected-badge">Selected</span>'
            active_cls = "active"
        else:
            select_link = f'<a href="/?select={i}&diff={difficulty or "all"}" target="_self" class="lc-card-action-btn select-btn">Select</a>'
            active_cls = ""

        ws    = p["weakness_score"]
        bar_w = int(ws * 100)
        t_chips = "".join(f'<span class="lc-tchip">{t}</span>' for t in p["tags"][:5])
        ws_color = "#ff4d00" if sel else "#888888"

        H(f'''
        <div class="lc-rcard {active_cls}">
            <div class="lc-rcard-top">
                <div style="flex:1">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                        <div class="lc-rcard-idx">{icons[i]} &nbsp;#{medals[i]}</div>
                        <div style="display:flex; gap:8px;">
                            {select_link}
                            {open_link}
                        </div>
                    </div>
                    <div class="lc-rcard-title">{p["title"]}</div>
                    <div class="lc-rcard-meta">
                        <span class="lc-dbadge {dc(p["difficulty"])}">{p["difficulty"]}</span>
                        <span class="lc-rmeta">Weakness&nbsp;{ws:.2f}</span>
                        <span class="lc-rmeta">·&nbsp;{p["acceptance_rate"]:.1f}% acceptance</span>
                    </div>
                    <div style="margin-top:0.5rem;">{t_chips}</div>
                </div>
                <div style="text-align:right;min-width:80px;flex-shrink:0;margin-left:1.5rem;">
                    <div class="lc-wsscore" style="color:{ws_color};">{bar_w}</div>
                    <div class="lc-wslbl">score</div>
                    <div class="lc-wsbar-wrap"><div class="lc-wsbar" style="width:{bar_w}%;"></div></div>
                </div>
            </div>
        </div>
        ''')

        if sel:
            all_tags = "".join(f'<span class="lc-tchip">{t}</span>' for t in p["tags"])
            H(f'<div class="lc-dpanel"><div class="lc-dpanel-hdr">Problem Breakdown</div><div class="lc-dstats"><div><div class="lc-dstat-val">{p["acceptance_rate"]:.1f}%</div><div class="lc-dstat-lbl">Acceptance</div></div><div><div class="lc-dstat-val">{bar_w}</div><div class="lc-dstat-lbl">Weakness Score</div></div><div><div class="lc-dstat-val">{p["difficulty"].upper()}</div><div class="lc-dstat-lbl">Difficulty</div></div></div><div class="lc-tags-lbl">Topics</div><div style="margin-top:0.3rem;">{all_tags}</div></div>')

def render_refresh(username: str):
    """Render refresh button to purge session cache and fetch fresh stats from backend API."""
    H('<div style="padding:1.5rem 4rem;border-bottom:1px solid var(--card-border);background:var(--bg-color);">')
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
