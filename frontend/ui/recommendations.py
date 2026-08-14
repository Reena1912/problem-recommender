import streamlit as st
from ui.styles import H
from ui.client import api

def dc(d):
    """Map difficulty keys to CSS styles."""
    return {"Easy": "lc-de", "Medium": "lc-dm", "Hard": "lc-dh"}.get(d, "lc-de")

def render_recommendations(username: str):
    """Render recommendations section with clean editorial layout."""
    H('''
    <div class="lc-container" style="margin-top:2.5rem;">
        <div style="background:#ffffff;border:1px solid #e4ebe6;border-radius:24px;padding:2.5rem;box-shadow:0 10px 30px rgba(0,0,0,0.03);margin-bottom:1rem;">
            <div class="lc-sec-hdr" style="margin-bottom:0!important;">
                <div class="lc-sec-num">02</div>
                <div>
                    <div class="lc-sec-title">A quick glance of your recommended problems <span class="lc-sec-dash">—</span></div>
                    <div class="lc-sec-sub">Ranked by how directly they target your top algorithmic skill gaps</div>
                </div>
            </div>
        </div>
    </div>
    ''')
    
    tabs = st.tabs(["✦ All Recommendations", "🟢 Easy Problems", "🟠 Medium Problems", "🔴 Hard Problems"])
    for tab, diff in zip(tabs, [None, "Easy", "Medium", "Hard"]):
        with tab:
            _rec_tab(username, diff)

def _rec_tab(username: str, difficulty: str | None):
    """Fetch recommendations from backend API and render problem cards."""
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
    H(f'<div class="lc-weak-bar"><span style="color:#132e28!important;font-weight:700;">📍 Primary Skill Gaps:</span> {tags_html}</div>')

    medals = ["01","02","03","04","05"]
    icons  = ["🥇","🥈","🥉","#4","#5"]

    for i, p in enumerate(pool[:5]):
        sel = st.session_state[sel_key] == i
        
        open_link = f'<a href="https://leetcode.com/problems/{p["titleSlug"]}/" target="_blank" class="lc-card-action-btn">Open Problem ↗</a>'
        
        if sel:
            select_link = '<span class="lc-card-selected-badge">✓ Selected</span>'
            active_cls = "active"
        else:
            select_link = f'<a href="/?select={i}&diff={difficulty or "all"}" target="_self" class="lc-card-action-btn select-btn">Select</a>'
            active_cls = ""

        ws    = p["weakness_score"]
        bar_w = int(ws * 100)
        t_chips = "".join(f'<span class="lc-tchip">{t}</span>' for t in p["tags"][:5])

        H(f'''
        <div class="lc-rcard {active_cls}">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div style="flex:1">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                        <div class="lc-rcard-idx">{icons[i]} &nbsp;Step #{medals[i]}</div>
                        <div style="display:flex; gap:8px;">
                            {select_link}
                            {open_link}
                        </div>
                    </div>
                    <div class="lc-rcard-title">{p["title"]}</div>
                    <div class="lc-rcard-meta">
                        <span class="lc-dbadge {dc(p["difficulty"])}">{p["difficulty"]}</span>
                        <span class="lc-rmeta">Weakness Coefficient &nbsp;<b>{ws:.2f}</b></span>
                        <span class="lc-rmeta">·&nbsp;{p["acceptance_rate"]:.1f}% acceptance</span>
                    </div>
                    <div style="margin-top:0.6rem;">{t_chips}</div>
                </div>
                <div style="text-align:right;min-width:90px;flex-shrink:0;margin-left:1.5rem;">
                    <div class="lc-wsscore">{bar_w}</div>
                    <div class="lc-wslbl">Impact Score</div>
                    <div class="lc-wsbar-wrap"><div class="lc-wsbar" style="width:{bar_w}%;"></div></div>
                </div>
            </div>
        </div>
        ''')

        if sel:
            all_tags = "".join(f'<span class="lc-tchip">{t}</span>' for t in p["tags"])
            H(f'''
            <div class="lc-dpanel">
                <div class="lc-dpanel-hdr">Problem Analytics Breakdown</div>
                <div class="lc-dstats">
                    <div><div class="lc-dstat-val">{p["acceptance_rate"]:.1f}%</div><div class="lc-dstat-lbl">Acceptance Rate</div></div>
                    <div><div class="lc-dstat-val">{bar_w} / 100</div><div class="lc-dstat-lbl">Weakness Match</div></div>
                    <div><div class="lc-dstat-val">{p["difficulty"].upper()}</div><div class="lc-dstat-lbl">Difficulty Level</div></div>
                </div>
                <div class="lc-dstat-lbl" style="margin-bottom:0.4rem;">Target Algorithm Topics</div>
                <div>{all_tags}</div>
            </div>
            ''')

def render_refresh(username: str):
    """Render refresh button to purge session cache and re-analyze profile."""
    _, mid, _ = st.columns([3.5, 3, 3.5])
    with mid:
        if st.button("🔄 Re-analyze Profile Data", use_container_width=True, type="primary"):
            with st.spinner("Re-fetching profile data…"):
                res = api(f"/update?username={username}", method="POST")
                if res and res.get("success"):
                    for k in list(st.session_state.keys()):
                        if k.startswith(("pool_","sel_")):
                            del st.session_state[k]
                    st.success(f"✓ Updated — top pick: **{res['top_recommendation']}**")
                    st.rerun()
