import streamlit as st

css_vars = """
:root {
    --bg-color: #f6f8f6;
    --text-color: #132e28;
    --text-muted: #566961;
    --text-desc: #41524b;
    --card-bg: #ffffff;
    --card-border: #e4ebe6;
    --card-shadow: 0 10px 30px rgba(0, 0, 0, 0.035);
    --card-hover-bg: #fafdfb;
    --card-selected-bg: #edf4f0;
    --card-selected-border: #132e28;
    --card-idx-color: #7a8a83;
    --nav-bg: #ffffff;
    --nav-border: #e4ebe6;
    --search-bg: #edf4f0;
    --search-border: #d4e3d9;
    --input-bg: #ffffff;
    --input-border: #beede0;
    --placeholder-color: #7d9489;
    --dpanel-bg: #edf4f0;
    --dpanel-border: #d4e3d9;
    --stats-lbl: #566961;
    --sec-num-color: #b8d1c3;
    --tchip-bg: #e4ebe6;
    --tchip-color: #132e28;
    --tchip-border: #cfdcd4;
    --tab-list-bg: #edf4f0;
    --tab-list-border: #d4e3d9;
    --tab-selected-bg: #132e28;
    --tab-selected-color: #ffffff;
    --tab-unselected-color: #566961;
    --primary-green: #132e28;
    --accent-sage: #dce8e0;
    --accent-sage-light: #edf4f0;
    --footer-bg: #132e28;
    --footer-text: #e2ede6;
    --pillar-border: #e4ebe6;
    --button-sec-bg: #edf4f0;
    --button-sec-text: #132e28;
    --button-sec-hover: #d7e4dc;
}
"""

plotly_text_color = "#132e28"
plotly_axis_color = "#566961"
plotly_grid_color = "#e4ebe6"
unsolved_pie_color = "#e4ebe6"

HERO_IMG_1 = "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&q=80"
HERO_IMG_2 = "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600&q=80"
HERO_IMG_3 = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=80"

def H(html: str):
    """Render HTML safely inside Streamlit without CommonMark code block leaks."""
    clean_html = " ".join(line.strip() for line in html.splitlines() if line.strip())
    st.markdown(clean_html, unsafe_allow_html=True)

def inject_styles():
    """Inject custom clean organic sage & forest green editorial stylesheet with high-contrast text rules."""
    H(f"""<style>
{css_vars}
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

/* ── GLOBAL RESET & LAYOUT CONTAINER ── */
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}

html,body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"]>.main,
section.main>.block-container {{
    font-family:'Plus Jakarta Sans',sans-serif!important;
}}

/* Disable Streamlit Markdown Pre/Code formatting leak */
[data-testid="stMarkdownContainer"] pre,
[data-testid="stMarkdownContainer"] code{{
    background:transparent!important;
    border:none!important;
    padding:0!important;
    margin:0!important;
    font-family:'Plus Jakarta Sans',sans-serif!important;
    color:inherit!important;
    white-space:normal!important;
    display:inline!important;
}}

[data-testid="stAppViewContainer"]{{background:var(--bg-color)!important;}}
[data-testid="stAppViewContainer"]>.main{{background:var(--bg-color)!important;}}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"]{{display:none!important;}}
.block-container{{padding:0!important;max-width:100%!important;}}

/* Central Alignment Container */
.lc-container{{
    max-width:1180px;
    margin:0 auto;
    padding:0 1.5rem;
}}

/* ── FLEXBOX LAYOUT FOR STREAMLIT COLUMNS ── */
div[data-testid="stHorizontalBlock"],
div.stHorizontalBlock {{
    display: flex !important;
    flex-direction: row !important;
    gap: 1rem !important;
    width: 100% !important;
    align-items: center !important;
}}

div[data-testid="stColumn"] > div {{
    width: 100% !important;
}}

/* ── NAV BAR ── */
.lc-nav-wrap{{
    background:#ffffff;
    border-bottom:1px solid #e4ebe6;
    position:sticky;
    top:0;
    z-index:100;
    box-shadow:0 4px 20px rgba(0,0,0,0.02);
}}
.lc-nav{{
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:1.1rem 0;
}}
.lc-nav-logo{{
    font-family:'Outfit',sans-serif!important;
    font-size:1.35rem;
    font-weight:800;
    letter-spacing:0.03em;
    color:#132e28!important;
    display:flex;
    align-items:center;
    gap:0.35rem;
}}
.lc-nav-logo span{{color:#22c55e!important;}}
.lc-nav-links{{
    display:flex;
    gap:2.2rem;
    font-size:0.9rem;
    font-weight:600;
    color:#566961!important;
}}
.lc-nav-links a{{
    color:#566961!important;
    text-decoration:none!important;
    transition:color 0.2s ease;
}}
.lc-nav-links a:hover{{
    color:#132e28!important;
}}
.lc-nav-cta{{
    background:#132e28!important;
    color:#ffffff!important;
    font-weight:700;
    font-size:0.82rem;
    letter-spacing:0.03em;
    padding:0.6rem 1.4rem;
    border-radius:50px!important;
    border:none;
    text-decoration:none!important;
    transition:all 0.2s ease;
    box-shadow:0 4px 12px rgba(19,46,40,0.15);
}}
.lc-nav-cta:hover{{
    background:#0b1d19!important;
    transform:translateY(-1px);
}}

/* ── HERO SECTION ── */
.lc-hero-section{{
    padding:3.5rem 0 2rem;
    background:var(--bg-color);
}}
.lc-hero-grid{{
    display:grid;
    grid-template-columns:1.1fr 0.9fr;
    gap:3.5rem;
    align-items:center;
}}
.lc-eyebrow{{
    font-size:0.75rem;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.18em;
    color:#132e28!important;
    margin-bottom:1.2rem;
    display:flex;
    align-items:center;
    gap:0.6rem;
}}
.lc-eyebrow-line{{
    display:inline-block;
    width:32px;
    height:2px;
    background:#132e28;
    flex-shrink:0;
}}
.lc-hero-title{{
    font-family:'Outfit',sans-serif!important;
    font-size:3.6rem;
    font-weight:800;
    line-height:1.08;
    color:#132e28!important;
    margin-bottom:1.2rem;
    letter-spacing:-0.02em;
}}
.lc-hero-desc{{
    font-size:1.02rem;
    color:#41524b!important;
    font-weight:400;
    line-height:1.65;
    max-width:520px;
    margin-bottom:2rem;
}}
.lc-hero-actions{{
    display:flex;
    gap:1rem;
    align-items:center;
}}
.lc-btn-pill-primary{{
    background:#132e28!important;
    color:#ffffff!important;
    font-weight:700;
    font-size:0.85rem;
    padding:0.75rem 1.8rem;
    border-radius:50px!important;
    text-decoration:none!important;
    display:inline-flex;
    align-items:center;
    gap:0.5rem;
    transition:all 0.2s ease;
    box-shadow:0 6px 20px rgba(19,46,40,0.18);
}}
.lc-btn-pill-primary:hover{{
    background:#0b1d19!important;
    transform:translateY(-2px);
}}
.lc-btn-pill-sec{{
    background:transparent;
    color:#132e28!important;
    font-weight:700;
    font-size:0.85rem;
    padding:0.72rem 1.6rem;
    border-radius:50px!important;
    border:1.5px solid #132e28!important;
    text-decoration:none!important;
    display:inline-flex;
    align-items:center;
    gap:0.5rem;
    transition:all 0.2s ease;
}}
.lc-btn-pill-sec:hover{{
    background:rgba(19,46,40,0.06);
}}

/* ── STADIUM ARCH IMAGES (HERO RIGHT) ── */
.lc-stadium-grid{{
    display:flex;
    gap:1.1rem;
    justify-content:center;
    align-items:center;
    position:relative;
}}
.lc-stadium-card{{
    width:130px;
    height:280px;
    border-radius:100px;
    overflow:hidden;
    box-shadow:0 12px 30px rgba(0,0,0,0.08);
    position:relative;
    transition:transform 0.3s ease;
}}
.lc-stadium-card:nth-child(2){{
    transform:translateY(-18px);
}}
.lc-stadium-card:hover{{
    transform:translateY(-5px) scale(1.03);
}}
.lc-stadium-card img{{
    width:100%;
    height:100%;
    object-fit:cover;
}}
.lc-sparkle{{
    position:absolute;
    color:#22c55e;
    font-size:1.4rem;
    pointer-events:none;
}}

/* ── SAGE METRICS BANNER ── */
.lc-metrics-banner{{
    background:#dce8e0;
    border-radius:100px;
    padding:1.1rem 2.5rem;
    margin-top:3rem;
    display:flex;
    justify-content:space-around;
    align-items:center;
    color:#132e28!important;
    font-weight:700;
    font-size:0.88rem;
    letter-spacing:0.02em;
    box-shadow:0 6px 25px rgba(220,232,224,0.5);
}}
.lc-metrics-banner span{{
    color:#132e28!important;
    display:inline-flex;
    align-items:center;
    gap:0.5rem;
}}

/* ── SEARCH STRIP ── */
.lc-search-wrap{{
    background:#ffffff;
    border:1px solid #e4ebe6;
    border-radius:24px;
    padding:2.2rem 2.6rem;
    margin:2.5rem 0 2rem;
    box-shadow:0 10px 30px rgba(0,0,0,0.03);
}}
.lc-search-title{{
    font-family:'Outfit',sans-serif!important;
    font-size:1.5rem;
    font-weight:800;
    color:#132e28!important;
    margin-bottom:0.3rem;
}}
.lc-search-sub{{
    font-size:0.88rem;
    color:#566961!important;
    margin-bottom:1.5rem;
}}

div[data-testid="stTextInputRootElement"]{{
    background-color:#edf4f0!important;
    border:1.5px solid #d4e3d9!important;
    border-radius:50px!important;
    transition:all 0.2s!important;
    height:48px!important;
}}
div[data-testid="stTextInputRootElement"]:focus-within{{
    border-color:#132e28!important;
    background-color:#ffffff!important;
    box-shadow:0 0 0 4px rgba(19,46,40,0.1)!important;
}}
div[data-testid="stTextInputRootElement"] input{{
    color:#132e28!important;
    font-family:'Plus Jakarta Sans',sans-serif!important;
    font-size:0.95rem!important;
    font-weight:600!important;
    background:transparent!important;
    padding:0.6rem 1.4rem!important;
    border:none!important;
    height:46px!important;
}}

/* Streamlit Primary & Form Submit Button Overrides (FORCE DEEP FOREST GREEN) */
.stButton>button,
button[kind="primary"],
button[kind="primaryFormSubmit"],
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-primaryFormSubmit"],
[data-testid="stFormSubmitButton"] button,
.stButton>button[kind="primary"]{{
    font-family:'Plus Jakarta Sans',sans-serif!important;
    font-weight:800!important;
    letter-spacing:0.02em!important;
    border-radius:50px!important;
    transition:all 0.2s!important;
    text-transform:none!important;
    font-size:0.88rem!important;
    height:48px!important;
    background:#132e28!important;
    color:#ffffff!important;
    border:none!important;
    box-shadow:0 4px 15px rgba(19,46,40,0.25)!important;
    opacity:1!important;
    visibility:visible!important;
}}
.stButton>button[kind="primary"] p,
.stButton>button[kind="primary"] span,
.stButton>button[kind="primary"] div,
[data-testid="stBaseButton-primary"] p,
[data-testid="stBaseButton-primary"] span,
[data-testid="stBaseButton-primary"] div,
[data-testid="stFormSubmitButton"] button p,
[data-testid="stFormSubmitButton"] button span,
[data-testid="stFormSubmitButton"] button div{{
    color:#ffffff!important;
    font-weight:800!important;
}}
.stButton>button[kind="primary"]:hover,
button[kind="primaryFormSubmit"]:hover,
[data-testid="stFormSubmitButton"] button:hover{{
    background:#0b1d19!important;
    transform:translateY(-1px);
    box-shadow:0 6px 20px rgba(19,46,40,0.35)!important;
}}
.stButton>button[kind="secondary"]{{
    background:#ffffff!important;
    color:#132e28!important;
    border:1.5px solid #d4e3d9!important;
    padding:0 1.4rem!important;
    height:48px!important;
    font-weight:700!important;
}}
.stButton>button[kind="secondary"] p,
.stButton>button[kind="secondary"] span,
.stButton>button[kind="secondary"] div{{
    color:#132e28!important;
    font-weight:700!important;
}}
.stButton>button[kind="secondary"]:hover{{
    background:#edf4f0!important;
    border-color:#132e28!important;
}}

/* ── FORM CONTAINER CARD STYLING ── */
div[data-testid="stForm"] {{
    background:#ffffff!important;
    border:1px solid #e4ebe6!important;
    border-radius:24px!important;
    padding:2rem 2.5rem!important;
    box-shadow:0 10px 30px rgba(0,0,0,0.03)!important;
    margin-bottom:1.5rem!important;
}}

/* ── STAT CARDS ── */
.lc-stat-card {{
    background:#ffffff;
    border:1px solid #e4ebe6;
    border-radius:18px;
    padding:1.4rem 1.6rem;
    position:relative;
    box-shadow:0 8px 25px rgba(0,0,0,0.03);
    transition:transform 0.2s ease, box-shadow 0.2s ease;
    width: 100% !important;
    height: 100% !important;
}}
.lc-stat-card:hover {{
    transform:translateY(-2px);
    box-shadow:0 12px 30px rgba(0,0,0,0.06);
}}
.lc-stat-hdr{{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:0.6rem;
}}
.lc-stat-title{{
    font-size:0.72rem;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.08em;
    color:#566961!important;
}}
.lc-stat-val{{
    font-family:'Outfit',sans-serif!important;
    font-size:2.8rem;
    font-weight:800;
    line-height:1;
    color:#132e28!important;
}}
.lc-stat-sub{{
    font-size:0.75rem;
    color:#7a8a83!important;
    margin-top:0.3rem;
}}
.lc-stat-badge{{
    font-size:0.68rem;
    font-weight:700;
    padding:4px 10px;
    border-radius:50px;
    letter-spacing:0.04em;
}}
.sb-tot{{background:#edf4f0;color:#132e28!important;border:1px solid #d4e3d9;}}
.sb-ez{{background:#eefcf2;color:#16a34a!important;border:1px solid #bbf7d0;}}
.sb-md{{background:#fffbeb;color:#d97706!important;border:1px solid #fde68a;}}
.sb-hd{{background:#fef2f2;color:#dc2626!important;border:1px solid #fecaca;}}

/* ── SECTION HEADER ── */
.lc-sec-hdr{{
    display:flex;
    align-items:baseline;
    gap:1rem;
    margin-bottom:2rem;
}}
.lc-sec-num{{
    font-family:'Outfit',sans-serif!important;
    font-size:3rem;
    font-weight:800;
    color:#b8d1c3!important;
    line-height:1;
    flex-shrink:0;
}}
.lc-sec-title{{
    font-family:'Outfit',sans-serif!important;
    font-size:2.1rem;
    font-weight:800;
    color:#132e28!important;
    letter-spacing:-0.01em;
    line-height:1.1;
}}
.lc-sec-dash{{
    color:#7a8a83!important;
    font-weight:400;
}}
.lc-sec-sub{{
    font-size:0.88rem;
    color:#566961!important;
    margin-top:0.3rem;
    font-weight:400;
}}

/* ── 3-STEP PROCESS SECTION ── */
.lc-process-grid{{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:1.5rem;
    margin:1.8rem 0 3.5rem;
}}
.lc-process-card{{
    background:#ffffff;
    border:1px solid #e4ebe6;
    border-radius:20px;
    padding:2rem;
    position:relative;
    box-shadow:0 8px 25px rgba(0,0,0,0.03);
}}
.lc-process-card.active-step{{
    background:#edf4f0;
    border-color:#beede0;
}}
.lc-step-tag{{
    font-family:'Outfit',sans-serif!important;
    font-size:2.2rem;
    font-weight:800;
    color:#132e28!important;
    margin-bottom:0.8rem;
}}
.lc-step-title{{
    font-size:1.15rem;
    font-weight:700;
    color:#132e28!important;
    margin-bottom:0.6rem;
}}
.lc-step-desc{{
    font-size:0.88rem;
    color:#566961!important;
    line-height:1.6;
}}

/* ── STREAMLIT SAGE TABS HIGH CONTRAST FIX ── */
[data-baseweb="tab-list"]{{
    background:#edf4f0!important;
    border-radius:50px!important;
    padding:4px!important;
    border:1px solid #d4e3d9!important;
    gap:4px!important;
    margin-bottom:1.5rem!important;
}}
[data-baseweb="tab"]{{
    border-radius:50px!important;
    color:#566961!important;
    font-family:'Plus Jakarta Sans',sans-serif!important;
    font-weight:700!important;
    font-size:0.85rem!important;
    text-transform:none!important;
    padding:0.6rem 1.4rem!important;
    background:transparent!important;
}}
[data-baseweb="tab"] * {{
    color:#566961!important;
}}
[aria-selected="true"][data-baseweb="tab"]{{
    background:#132e28!important;
    color:#ffffff!important;
}}
[aria-selected="true"][data-baseweb="tab"] *,
[aria-selected="true"][data-baseweb="tab"] span,
[aria-selected="true"][data-baseweb="tab"] div{{
    color:#ffffff!important;
}}

/* ── RECOMMENDATION CARDS ── */
.lc-rcard{{
    background:#ffffff;
    border:1px solid #e4ebe6;
    border-radius:16px;
    padding:1.4rem 1.8rem;
    margin-bottom:0.8rem;
    position:relative;
    box-shadow:0 4px 15px rgba(0,0,0,0.02);
    transition:all 0.2s ease;
}}
.lc-rcard:hover{{
    border-color:#beede0;
    box-shadow:0 8px 25px rgba(0,0,0,0.05);
}}
.lc-rcard.active{{
    border:2px solid #132e28;
    background:#fafdfb;
}}
.lc-rcard-idx{{
    font-family:'Outfit',sans-serif!important;
    font-size:0.88rem;
    font-weight:700;
    color:#566961!important;
}}
.lc-rcard-title{{
    font-size:1.05rem;
    font-weight:700;
    color:#132e28!important;
    margin-bottom:0.4rem;
}}
.lc-rcard-meta{{
    display:flex;
    gap:0.7rem;
    align-items:center;
    flex-wrap:wrap;
}}
.lc-dbadge{{
    font-size:0.68rem;
    font-weight:700;
    padding:3px 10px;
    border-radius:50px;
    letter-spacing:0.04em;
    text-transform:uppercase;
}}
.lc-de{{background:#eefcf2;color:#16a34a!important;border:1px solid #bbf7d0;}}
.lc-dm{{background:#fffbeb;color:#d97706!important;border:1px solid #fde68a;}}
.lc-dh{{background:#fef2f2;color:#dc2626!important;border:1px solid #fecaca;}}
.lc-rmeta{{
    font-size:0.75rem;
    color:#7a8a83!important;
}}
[data-testid="stMarkdownContainer"] span.lc-tchip{{
    display:inline-block;
    font-size:0.68rem;
    background:#edf4f0;
    color:#132e28!important;
    padding:3px 9px;
    border-radius:50px;
    border:1px solid #beede0;
    margin:2px 2px;
    font-weight:600!important;
}}
.lc-wsbar-wrap{{
    width:80px;
    height:5px;
    background:#e4ebe6;
    border-radius:10px;
    margin-top:0.4rem;
    margin-left:auto;
}}
.lc-wsbar{{
    height:5px;
    background:#132e28;
    border-radius:10px;
}}
.lc-wsscore{{
    font-family:'Outfit',sans-serif!important;
    font-size:2.2rem;
    font-weight:800;
    line-height:1;
    color:#132e28!important;
}}
.lc-wslbl{{
    font-size:0.62rem;
    color:#7a8a83!important;
    text-transform:uppercase;
    letter-spacing:0.1em;
    font-weight:700;
}}

/* ── DETAIL PANEL ── */
.lc-dpanel{{
    background:#edf4f0;
    border:1px solid #beede0;
    border-radius:14px;
    padding:1.4rem 1.8rem;
    margin-bottom:0.8rem;
}}
.lc-dpanel-hdr{{
    font-size:0.7rem;
    color:#566961!important;
    text-transform:uppercase;
    letter-spacing:0.12em;
    font-weight:700;
    margin-bottom:0.8rem;
}}
.lc-dstats{{
    display:flex;
    justify-content:space-between;
    margin:0.8rem 0 1rem;
    gap:1rem;
}}
.lc-dstat-val{{
    font-family:'Outfit',sans-serif!important;
    font-size:2.2rem;
    font-weight:800;
    color:#132e28!important;
    line-height:1;
    white-space:nowrap!important;
}}
.lc-dstat-lbl{{
    font-size:0.68rem;
    color:#566961!important;
    text-transform:uppercase;
    letter-spacing:0.08em;
    margin-top:0.3rem;
    white-space:nowrap!important;
    font-weight:600;
}}

/* ── WEAK TAG BAR & CHIPS ── */
.lc-weak-bar{{
    background:#edf4f0;
    border:1px solid #beede0;
    border-left:4px solid #132e28;
    border-radius:12px;
    padding:0.8rem 1.3rem;
    margin-bottom:1.3rem;
    font-size:0.85rem;
    color:#566961!important;
    display:flex;
    align-items:center;
    gap:0.8rem;
    flex-wrap:wrap;
}}
[data-testid="stMarkdownContainer"] span.lc-weak-tchip{{
    display:inline-block;
    font-size:0.72rem;
    background:#132e28!important;
    color:#ffffff!important;
    padding:4px 12px;
    border-radius:50px;
    margin:2px 2px;
    font-weight:700!important;
}}

/* ── LINK BUTTON ── */
.lc-card-action-btn{{
    color:#132e28!important;
    text-decoration:none!important;
    font-weight:700!important;
    border:1.5px solid #132e28!important;
    padding:4px 12px!important;
    border-radius:50px!important;
    font-size:0.72rem!important;
    transition:all 0.2s ease!important;
}}
.lc-card-action-btn:hover{{
    background-color:#132e28!important;
    color:#ffffff!important;
}}
.lc-card-action-btn.select-btn{{
    border-color:#beede0!important;
    color:#566961!important;
}}
.lc-card-action-btn.select-btn:hover{{
    background-color:#edf4f0!important;
    color:#132e28!important;
    border-color:#132e28!important;
}}
.lc-card-selected-badge{{
    background-color:#edf4f0!important;
    color:#132e28!important;
    border:1.5px solid #132e28!important;
    padding:4px 12px!important;
    border-radius:50px!important;
    font-size:0.72rem!important;
    font-weight:700!important;
}}

/* ── FOOTER & SUBMIT BUTTON OVERRIDES ── */
.lc-footer-wrap,
.lc-footer-wrap *,
.lc-footer-newsletter,
.lc-footer-newsletter * {{
    color:#e2ede6!important;
}}
.lc-footer-wrap{{
    background:#132e28!important;
    padding:4rem 0 2.5rem;
    margin-top:3.5rem;
}}
.lc-footer-newsletter{{
    background:#1c3e37!important;
    border:1px solid #28544b!important;
    border-radius:20px;
    padding:2.2rem 2.8rem;
    margin-bottom:3.5rem;
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:2rem;
}}
.lc-footer-nl-title,
.lc-footer-nl-title * {{
    font-family:'Outfit',sans-serif!important;
    font-size:1.6rem!important;
    font-weight:800!important;
    color:#ffffff!important;
    margin-bottom:0.3rem;
}}
.lc-footer-nl-sub,
.lc-footer-nl-sub * {{
    font-size:0.88rem!important;
    color:#b8d1c3!important;
}}

button.lc-nl-btn,
.lc-footer-newsletter button {{
    background:#22c55e!important;
    color:#ffffff!important;
    font-family:'Plus Jakarta Sans',sans-serif!important;
    font-weight:800!important;
    font-size:0.9rem!important;
    border-radius:50px!important;
    border:none!important;
    padding:0.75rem 1.8rem!important;
    cursor:pointer!important;
    white-space:nowrap!important;
    box-shadow:0 4px 15px rgba(34,197,94,0.4)!important;
    display:inline-block!important;
    opacity:1!important;
    visibility:visible!important;
}}

.lc-footer-bottom{{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding-top:2rem;
    border-top:1px solid #22423c;
}}
.lc-footer-logo{{
    font-family:'Outfit',sans-serif!important;
    font-size:1.3rem!important;
    font-weight:800!important;
    color:#ffffff!important;
}}
.lc-footer-logo span{{color:#22c55e!important;}}
.lc-footer-copy{{
    font-size:0.8rem!important;
    color:#a3c2b1!important;
}}

hr{{border-color:#e4ebe6!important;margin:0!important;}}
[data-testid="stSpinner"]>div{{border-top-color:#132e28!important;}}
</style>""")
