HTML_UI_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AlgoMatch — Algorithmic Skill Optimizer</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-color: #f4f7f5;
            --forest-green: #132e28;
            --emerald-green: #22c55e;
            --sage-accent: #e4ebe6;
            --card-bg: #ffffff;
            --border-color: #e4ebe6;
            --text-dark: #132e28;
            --text-muted: #566961;
            --easy-color: #16a34a;
            --medium-color: #d97706;
            --hard-color: #dc2626;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-dark);
            line-height: 1.5;
            padding-bottom: 4rem;
        }
        a { color: inherit; text-decoration: none; }
        
        .lc-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }
        
        /* Navigation */
        .lc-nav-wrap {
            background: rgba(244, 247, 245, 0.95);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid var(--border-color);
            padding: 1.2rem 0;
        }
        .lc-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .lc-nav-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: var(--forest-green);
        }
        .lc-nav-logo span { color: var(--emerald-green); }
        .lc-nav-links {
            display: flex;
            gap: 2.2rem;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-muted);
        }
        .lc-nav-links a:hover { color: var(--forest-green); }
        .lc-nav-cta {
            background: var(--forest-green);
            color: #ffffff;
            font-weight: 700;
            padding: 0.6rem 1.4rem;
            border-radius: 50px;
            font-size: 0.88rem;
            transition: all 0.2s;
        }
        .lc-nav-cta:hover { background: #0b1d19; transform: translateY(-1px); }

        /* Hero */
        .lc-hero-wrap {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2.5rem;
            align-items: center;
            padding: 4rem 0 3.5rem;
        }
        .lc-eyebrow {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-size: 0.75rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--text-muted);
            margin-bottom: 1rem;
        }
        .lc-eyebrow-line {
            width: 20px;
            height: 2px;
            background: var(--forest-green);
        }
        .lc-hero-title {
            font-family: 'Outfit', sans-serif;
            font-size: 3.4rem;
            font-weight: 800;
            line-height: 1.08;
            color: var(--forest-green);
            margin-bottom: 1.2rem;
            letter-spacing: -0.03em;
        }
        .lc-active-profile-pill {
            display: inline-flex;
            align-items: center;
            background: #dcfce7;
            color: #15803d;
            font-weight: 700;
            font-size: 0.88rem;
            padding: 0.35rem 0.9rem;
            border-radius: 50px;
            margin-bottom: 1.2rem;
        }
        .lc-hero-desc {
            font-size: 1.02rem;
            color: var(--text-muted);
            margin-bottom: 2rem;
            line-height: 1.6;
        }
        .lc-hero-btns {
            display: flex;
            gap: 1rem;
        }
        .lc-btn-primary {
            background: var(--forest-green);
            color: #ffffff;
            font-weight: 800;
            padding: 0.75rem 1.6rem;
            border-radius: 50px;
            font-size: 0.9rem;
            transition: all 0.2s;
        }
        .lc-btn-primary:hover { background: #0b1d19; }
        .lc-btn-secondary {
            background: transparent;
            color: var(--forest-green);
            border: 1.5px solid var(--forest-green);
            font-weight: 800;
            padding: 0.75rem 1.6rem;
            border-radius: 50px;
            font-size: 0.9rem;
            transition: all 0.2s;
        }
        .lc-btn-secondary:hover { background: rgba(19,46,40,0.05); }

        /* Hero Right Images */
        .lc-hero-imgs {
            display: flex;
            gap: 1rem;
            justify-content: flex-end;
        }
        .lc-img-pill {
            width: 140px;
            height: 300px;
            border-radius: 80px;
            object-fit: cover;
            box-shadow: 0 15px 35px rgba(0,0,0,0.08);
            border: 3px solid #ffffff;
        }

        /* Pill Feature Strip */
        .lc-feature-strip {
            display: flex;
            justify-content: space-between;
            background: #e4ebe6;
            border-radius: 50px;
            padding: 0.8rem 1.8rem;
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--forest-green);
            margin-bottom: 3.5rem;
        }

        /* Section Header */
        .lc-sec-hdr {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1.8rem;
        }
        .lc-sec-num {
            font-family: 'Outfit', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            color: #c4d7cc;
            line-height: 1;
        }
        .lc-sec-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--forest-green);
        }
        .lc-sec-sub {
            font-size: 0.85rem;
            color: var(--text-muted);
        }

        /* Three Process Cards */
        .lc-process-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin-bottom: 3.5rem;
        }
        .lc-process-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.02);
        }
        .lc-proc-num {
            font-family: 'Outfit', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--forest-green);
            margin-bottom: 0.8rem;
        }
        .lc-proc-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--forest-green);
            margin-bottom: 0.6rem;
        }
        .lc-proc-desc {
            font-size: 0.85rem;
            color: var(--text-muted);
            line-height: 1.5;
        }

        /* Search Card */
        .lc-search-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 2.2rem 2.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.03);
            margin-bottom: 2.5rem;
        }
        .lc-search-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--forest-green);
            margin-bottom: 0.3rem;
        }
        .lc-search-sub {
            font-size: 0.88rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
        }
        .lc-search-form {
            display: flex;
            gap: 1rem;
        }
        .lc-search-input {
            flex: 1;
            background: #f8faf9;
            border: 1.5px solid var(--border-color);
            border-radius: 50px;
            padding: 0.8rem 1.5rem;
            font-size: 0.95rem;
            color: var(--text-dark);
            outline: none;
            transition: all 0.2s;
        }
        .lc-search-input:focus {
            border-color: var(--forest-green);
            background: #ffffff;
        }
        .lc-search-btn {
            background: var(--forest-green);
            color: #ffffff;
            font-weight: 800;
            border: none;
            border-radius: 50px;
            padding: 0.8rem 2.2rem;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .lc-search-btn:hover {
            background: #0b1d19;
            transform: translateY(-1px);
        }

        /* Stats Grid */
        .lc-stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.2rem;
            margin-bottom: 3.5rem;
        }
        .lc-stat-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 18px;
            padding: 1.4rem 1.6rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.03);
        }
        .lc-stat-hdr {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.6rem;
        }
        .lc-stat-title {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
        }
        .lc-stat-badge {
            font-size: 0.72rem;
            font-weight: 800;
            padding: 0.15rem 0.6rem;
            border-radius: 50px;
        }
        .lc-stat-val {
            font-family: 'Outfit', sans-serif;
            font-size: 2.8rem;
            font-weight: 800;
            line-height: 1;
            color: var(--forest-green);
            margin-bottom: 0.4rem;
        }
        .lc-stat-sub {
            font-size: 0.76rem;
            color: var(--text-muted);
        }

        /* Skill Gaps Strip */
        .lc-gaps-strip {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1rem 1.5rem;
            margin-bottom: 1.5rem;
        }
        .lc-gaps-label {
            font-size: 0.82rem;
            font-weight: 800;
            color: var(--forest-green);
        }
        .lc-gap-pill {
            background: var(--forest-green);
            color: #ffffff;
            font-weight: 700;
            font-size: 0.78rem;
            padding: 0.3rem 0.9rem;
            border-radius: 50px;
        }

        /* Recommendation Step Card */
        .lc-rec-card {
            background: var(--card-bg);
            border: 1.5px solid var(--forest-green);
            border-radius: 20px;
            padding: 1.8rem 2.2rem;
            margin-bottom: 1.8rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.03);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .lc-step-hdr {
            font-size: 0.82rem;
            font-weight: 800;
            color: var(--forest-green);
            margin-bottom: 0.4rem;
        }
        .lc-rec-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 800;
            color: var(--forest-green);
            margin-bottom: 0.6rem;
        }
        .lc-rec-meta {
            display: flex;
            gap: 0.8rem;
            align-items: center;
            margin-bottom: 1rem;
        }
        .lc-rec-diff {
            font-size: 0.72rem;
            font-weight: 800;
            padding: 0.2rem 0.7rem;
            border-radius: 50px;
            text-transform: uppercase;
        }
        .diff-easy { background: #dcfce7; color: #16a34a; }
        .diff-medium { background: #fef3c7; color: #d97706; }
        .diff-hard { background: #fee2e2; color: #dc2626; }

        .lc-rec-tags {
            display: flex;
            gap: 0.5rem;
        }
        .lc-tag-pill {
            background: #f0f5f2;
            color: var(--text-muted);
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.15rem 0.6rem;
            border-radius: 6px;
        }
        .lc-rec-right {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        .lc-selected-btn {
            background: #ffffff;
            border: 1px solid var(--border-color);
            color: var(--forest-green);
            font-weight: 700;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            font-size: 0.82rem;
        }
        .lc-solve-btn {
            background: var(--forest-green);
            color: #ffffff;
            font-weight: 800;
            padding: 0.6rem 1.4rem;
            border-radius: 50px;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        .lc-solve-btn:hover { background: #0b1d19; }
        .lc-impact-box {
            text-align: right;
        }
        .lc-impact-val {
            font-family: 'Outfit', sans-serif;
            font-size: 2.8rem;
            font-weight: 800;
            color: var(--forest-green);
            line-height: 1;
        }
        .lc-impact-lbl {
            font-size: 0.7rem;
            font-weight: 800;
            color: var(--text-muted);
            letter-spacing: 0.08em;
        }

        /* Problem Breakdown Banner */
        .lc-breakdown-banner {
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 1.8rem 2.5rem;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            margin-bottom: 3.5rem;
        }
        .lc-bd-item {
            text-align: center;
        }
        .lc-bd-lbl {
            font-size: 0.72rem;
            font-weight: 800;
            color: var(--text-muted);
            letter-spacing: 0.08em;
            margin-bottom: 0.4rem;
        }
        .lc-bd-val {
            font-family: 'Outfit', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--forest-green);
        }

        /* Analytics Grid */
        .lc-analytics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.8rem;
            margin-bottom: 3.5rem;
        }
        .lc-chart-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 1.8rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.03);
            min-height: 320px;
        }
        .lc-chart-title {
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--forest-green);
            margin-bottom: 1.2rem;
        }

        /* Recommendation Tabs */
        .lc-rec-tabs {
            display: flex;
            gap: 0.8rem;
            margin-bottom: 1.8rem;
        }
        .lc-tab-btn {
            background: #ffffff;
            border: 1px solid var(--border-color);
            padding: 0.55rem 1.3rem;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 700;
            cursor: pointer;
            color: var(--text-muted);
            transition: all 0.2s;
        }
        .lc-tab-btn.active {
            background: var(--forest-green);
            color: #ffffff;
            border-color: var(--forest-green);
        }

        /* Footer */
        .lc-footer {
            background: var(--forest-green);
            color: #ffffff;
            padding: 2.5rem 0;
            margin-top: 4rem;
        }
        .lc-footer-inner {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .lc-footer-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 800;
        }
        .lc-footer-logo span { color: var(--emerald-green); }
        .lc-footer-copy {
            font-size: 0.8rem;
            color: #a3c4b5;
        }

        @media (max-width: 900px) {
            .lc-hero-wrap { grid-template-columns: 1fr; }
            .lc-stats-grid { grid-template-columns: repeat(2, 1fr); }
            .lc-process-grid { grid-template-columns: 1fr; }
            .lc-analytics-grid { grid-template-columns: 1fr; }
            .lc-hero-title { font-size: 2.4rem; }
        }
    </style>
</head>
<body>

    <!-- NAV -->
    <div class="lc-nav-wrap">
        <div class="lc-container">
            <div class="lc-nav">
                <div class="lc-nav-logo">ALGO<span>.</span>MATCH</div>
                <div class="lc-nav-links">
                    <a href="#search">Dashboard</a>
                    <a href="#process">Methodology</a>
                    <a href="#analytics">Analytics</a>
                    <a href="/docs" target="_blank">API Docs</a>
                </div>
                <a href="#search" class="lc-nav-cta">Analyze Profile</a>
            </div>
        </div>
    </div>

    <div class="lc-container">

        <!-- HERO -->
        <div class="lc-hero-wrap">
            <div>
                <div class="lc-eyebrow"><span class="lc-eyebrow-line"></span>Data-Driven Practice Platform</div>
                <h1 class="lc-hero-title">Stop grinding blindly.<br>Target your exact skill gaps.</h1>
                <div class="lc-active-profile-pill">Active Profile: @<span id="hero-username">neetcode</span></div>
                <p class="lc-hero-desc">An intelligent, production-ready system that analyzes any LeetCode profile, detects algorithmic blind spots, and recommends the most impactful problems to solve next — backed by data-driven weakness scoring.</p>
                <div class="lc-hero-btns">
                    <a href="#search" class="lc-btn-primary">Get Started Now →</a>
                    <a href="/docs" target="_blank" class="lc-btn-secondary">Explore API Docs ↗</a>
                </div>
            </div>
            <div class="lc-hero-imgs">
                <img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&q=80" class="lc-img-pill" alt="Code">
                <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400&q=80" class="lc-img-pill" alt="Team">
                <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&q=80" class="lc-img-pill" alt="Analytics">
            </div>
        </div>

        <!-- PILL FEATURE STRIP -->
        <div class="lc-feature-strip">
            <div>✦ 3,900+ Catalog Problems</div>
            <div>✦ Sub-Second Caching</div>
            <div>⚡ LeetCode GraphQL Sync</div>
            <div>✦ Data-Driven Weakness Scoring</div>
        </div>

        <!-- PROCESS SECTION -->
        <div class="lc-sec-hdr" id="process">
            <div class="lc-sec-num">01</div>
            <div>
                <div class="lc-sec-title">A simple, yet effective three step process —</div>
                <div class="lc-sec-sub">How our recommendation engine pinpoints your exact algorithmic weakness</div>
            </div>
        </div>

        <div class="lc-process-grid">
            <div class="lc-process-card">
                <div class="lc-proc-num">01.</div>
                <div class="lc-proc-title">Profile Analysis</div>
                <div class="lc-proc-desc">We fetch real-time solved counts and tag distributions from LeetCode GraphQL API with exponential backoff retries.</div>
            </div>
            <div class="lc-process-card">
                <div class="lc-proc-num">02.</div>
                <div class="lc-proc-title">Weakness Scoring</div>
                <div class="lc-proc-desc">Calculates a normalized weakness coefficient (0.0 to 1.0) for 40+ algorithmic topics relative to your top strengths.</div>
            </div>
            <div class="lc-process-card">
                <div class="lc-proc-num">03.</div>
                <div class="lc-proc-title">Precision Ranking</div>
                <div class="lc-proc-desc">Ranks 3,900+ unsolved catalog problems and surfaces the highest-value Easy, Medium, or Hard questions to practice.</div>
            </div>
        </div>

        <!-- SEARCH CARD -->
        <div class="lc-search-card" id="search">
            <div class="lc-search-title">Analyze Any LeetCode Profile</div>
            <div class="lc-search-sub">Enter a username below to calculate weakness scores across 40+ algorithmic topics.</div>
            <form class="lc-search-form" id="search-form">
                <input type="text" id="username-input" class="lc-search-input" placeholder="e.g. neetcode, tourist, or NovaAsher…" value="neetcode">
                <button type="submit" class="lc-search-btn">Analyze Profile →</button>
            </form>
        </div>

        <!-- STATS GRID -->
        <div class="lc-stats-grid">
            <div class="lc-stat-card">
                <div class="lc-stat-hdr">
                    <div class="lc-stat-title">Total Solved</div>
                    <div class="lc-stat-badge" style="background:#e8f4ec;color:#16a34a;" id="st-tot-pct">5.1%</div>
                </div>
                <div class="lc-stat-val" id="st-tot-val">205</div>
                <div class="lc-stat-sub" id="st-tot-sub">out of 4,019 available problems</div>
            </div>
            <div class="lc-stat-card">
                <div class="lc-stat-hdr">
                    <div class="lc-stat-title">Easy Solved</div>
                    <div class="lc-stat-badge" style="background:#dcfce7;color:#16a34a;" id="st-ez-pct">10.8%</div>
                </div>
                <div class="lc-stat-val" id="st-ez-val">103</div>
                <div class="lc-stat-sub" id="st-ez-sub">out of 958 available problems</div>
            </div>
            <div class="lc-stat-card">
                <div class="lc-stat-hdr">
                    <div class="lc-stat-title">Medium Solved</div>
                    <div class="lc-stat-badge" style="background:#fef3c7;color:#d97706;" id="st-md-pct">4.7%</div>
                </div>
                <div class="lc-stat-val" id="st-md-val">98</div>
                <div class="lc-stat-sub" id="st-md-sub">out of 2,099 available problems</div>
            </div>
            <div class="lc-stat-card">
                <div class="lc-stat-hdr">
                    <div class="lc-stat-title">Hard Solved</div>
                    <div class="lc-stat-badge" style="background:#fee2e2;color:#dc2626;" id="st-hd-pct">0.4%</div>
                </div>
                <div class="lc-stat-val" id="st-hd-val">4</div>
                <div class="lc-stat-sub" id="st-hd-sub">out of 962 available problems</div>
            </div>
        </div>

        <!-- RECOMMENDATIONS SECTION -->
        <div class="lc-sec-hdr">
            <div class="lc-sec-num">02</div>
            <div>
                <div class="lc-sec-title">A quick glance of your recommended problems —</div>
                <div class="lc-sec-sub">Ranked by how directly they target your top algorithmic skill gaps</div>
            </div>
        </div>

        <div class="lc-rec-tabs">
            <button class="lc-tab-btn active" data-diff="all">✦ All Recommendations</button>
            <button class="lc-tab-btn" data-diff="easy">🟢 Easy Problems</button>
            <button class="lc-tab-btn" data-diff="medium">🟠 Medium Problems</button>
            <button class="lc-tab-btn" data-diff="hard">🔴 Hard Problems</button>
        </div>

        <!-- SKILL GAPS STRIP -->
        <div class="lc-gaps-strip">
            <div class="lc-gaps-label">📍 Primary Skill Gaps:</div>
            <div class="lc-gap-pill">iterator</div>
            <div class="lc-gap-pill">data stream</div>
            <div class="lc-gap-pill">game theory</div>
        </div>

        <!-- STEP #01 RECOMMENDATION CARD -->
        <div id="recommendation-card-wrap">
            <div class="lc-rec-card">
                <div>
                    <div class="lc-step-hdr">🥇 Step #01</div>
                    <div class="lc-rec-title" id="rec-title">K-th Smallest in Lexicographical Order</div>
                    <div class="lc-rec-meta">
                        <span class="lc-rec-diff diff-hard" id="rec-diff">HARD</span>
                        <span style="font-size:0.8rem;color:var(--text-muted);" id="rec-coeff">Weakness Coefficient 0.99</span>
                        <span style="font-size:0.8rem;color:var(--text-muted);" id="rec-acc">· 46.4% acceptance</span>
                    </div>
                    <div class="lc-rec-tags" id="rec-tags">
                        <span class="lc-tag-pill">Trie</span>
                    </div>
                </div>
                <div class="lc-rec-right">
                    <button class="lc-selected-btn">✓ Selected</button>
                    <a href="https://leetcode.com/problems/k-th-smallest-in-lexicographical-order/" target="_blank" id="rec-url" class="lc-solve-btn">Open Problem ></a>
                    <div class="lc-impact-box">
                        <div class="lc-impact-val" id="rec-impact">98</div>
                        <div class="lc-impact-lbl">IMPACT SCORE</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- PROBLEM ANALYTICS BREAKDOWN -->
        <div class="lc-breakdown-banner">
            <div class="lc-bd-item">
                <div class="lc-bd-lbl">PROBLEM ANALYTICS BREAKDOWN</div>
                <div class="lc-bd-val" id="bd-acc">46.4%</div>
                <div style="font-size:0.72rem;color:var(--text-muted);">ACCEPTANCE RATE</div>
            </div>
            <div class="lc-bd-item">
                <div class="lc-bd-lbl">&nbsp;</div>
                <div class="lc-bd-val" id="bd-match">98 / 100</div>
                <div style="font-size:0.72rem;color:var(--text-muted);">WEAKNESS MATCH</div>
            </div>
            <div class="lc-bd-item">
                <div class="lc-bd-lbl">&nbsp;</div>
                <div class="lc-bd-val" id="bd-diff">HARD</div>
                <div style="font-size:0.72rem;color:var(--text-muted);">DIFFICULTY LEVEL</div>
            </div>
        </div>

        <!-- ANALYTICS SECTION -->
        <div class="lc-sec-hdr" id="analytics">
            <div class="lc-sec-num">03</div>
            <div>
                <div class="lc-sec-title">Skill Analytics & Practice Targets —</div>
                <div class="lc-sec-sub">Simple breakdown of your weakest topics and difficulty progress</div>
            </div>
        </div>

        <div class="lc-analytics-grid">
            <div class="lc-chart-card">
                <div class="lc-chart-title">📉 TOP TOPICS NEEDING PRACTICE</div>
                <canvas id="barChart" height="220"></canvas>
            </div>
            <div class="lc-chart-card">
                <div class="lc-chart-title">🍰 SOLVED PROBLEMS BY DIFFICULTY</div>
                <canvas id="donutChart" height="220"></canvas>
            </div>
        </div>

    </div>

    <!-- FOOTER -->
    <div class="lc-footer">
        <div class="lc-container">
            <div class="lc-footer-inner">
                <div class="lc-footer-logo">ALGO<span>.</span>MATCH</div>
                <div class="lc-footer-copy">Data from LeetCode GraphQL API · Weakness-Score Ranking Engine · Built with ⚡</div>
            </div>
        </div>
    </div>

    <script>
        let barChartInstance = null;
        let donutChartInstance = null;
        let activeDiff = 'all';

        async function fetchUserData(username) {
            document.getElementById('hero-username').textContent = username;

            try {
                // Fetch stats
                const statsRes = await fetch(`/stats?username=${encodeURIComponent(username)}`);
                if (!statsRes.ok) throw new Error("Failed to load user stats");
                const stats = await statsRes.json();

                updateStats(stats);
                updateCharts(stats);

                // Fetch recommendations
                loadRecommendations(username, activeDiff);
            } catch (err) {
                console.error(err);
            }
        }

        function updateStats(stats) {
            const sc = stats.solve_counts || {};
            const ta = stats.total_available || {};

            const calcPct = (s, t) => t ? ((s / t) * 100).toFixed(1) : '0.0';

            document.getElementById('st-tot-val').textContent = (sc.All || 205).toLocaleString();
            document.getElementById('st-tot-pct').textContent = `${calcPct(sc.All || 205, ta.All || 4019)}%`;
            document.getElementById('st-tot-sub').textContent = `out of ${(ta.All || 4019).toLocaleString()} available problems`;

            document.getElementById('st-ez-val').textContent = (sc.Easy || 103).toLocaleString();
            document.getElementById('st-ez-pct').textContent = `${calcPct(sc.Easy || 103, ta.Easy || 958)}%`;
            document.getElementById('st-ez-sub').textContent = `out of ${(ta.Easy || 958).toLocaleString()} available problems`;

            document.getElementById('st-md-val').textContent = (sc.Medium || 98).toLocaleString();
            document.getElementById('st-md-pct').textContent = `${calcPct(sc.Medium || 98, ta.Medium || 2099)}%`;
            document.getElementById('st-md-sub').textContent = `out of ${(ta.Medium || 2099).toLocaleString()} available problems`;

            document.getElementById('st-hd-val').textContent = (sc.Hard || 4).toLocaleString();
            document.getElementById('st-hd-pct').textContent = `${calcPct(sc.Hard || 4, ta.Hard || 962)}%`;
            document.getElementById('st-hd-sub').textContent = `out of ${(ta.Hard || 962).toLocaleString()} available problems`;
        }

        function updateCharts(stats) {
            const ts = stats.tag_scores || [];
            const sortedTs = [...ts].sort((a, b) => b.weakness_score - a.weakness_score).slice(0, 8);

            const labels1 = sortedTs.length ? sortedTs.map(t => t.tag) : ['Iterator', 'Data Stream', 'Game Theory', 'Bitmask', 'Quickselect', 'Trie', 'Union-Find', 'Queue'];
            const data1 = sortedTs.length ? sortedTs.map(t => (t.weakness_score * 100).toFixed(1)) : [98.8, 98.8, 98.8, 98.8, 98.8, 98.8, 98.8, 97.5];

            if (barChartInstance) barChartInstance.destroy();
            const ctx1 = document.getElementById('barChart').getContext('2d');
            barChartInstance = new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: labels1,
                    datasets: [{
                        label: 'Practice Priority (%)',
                        data: data1,
                        backgroundColor: '#132e28',
                        borderRadius: 6
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { max: 120, grid: { color: '#e4ebe6' } },
                        y: { grid: { display: false } }
                    }
                }
            });

            const sc = stats.solve_counts || {};
            const easy = sc.Easy || 103;
            const med = sc.Medium || 98;
            const hard = sc.Hard || 4;

            if (donutChartInstance) donutChartInstance.destroy();
            const ctx2 = document.getElementById('donutChart').getContext('2d');
            donutChartInstance = new Chart(ctx2, {
                type: 'doughnut',
                data: {
                    labels: ['Easy Solved', 'Medium Solved', 'Hard Solved'],
                    datasets: [{
                        data: [easy, med, hard],
                        backgroundColor: ['#16a34a', '#d97706', '#dc2626'],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: 'bottom' } },
                    cutout: '65%'
                }
            });
        }

        async function loadRecommendations(username, difficulty) {
            try {
                let url = `/recommend?username=${encodeURIComponent(username)}`;
                if (difficulty !== 'all') {
                    url = `/recommend/${difficulty}?username=${encodeURIComponent(username)}`;
                }
                const res = await fetch(url);
                if (!res.ok) throw new Error("Failed to fetch recommendation");
                const data = await res.json();
                
                const rec = data.recommendation;
                if (!rec) return;

                document.getElementById('rec-title').textContent = rec.title;
                document.getElementById('rec-diff').textContent = rec.difficulty.toUpperCase();
                document.getElementById('rec-diff').className = `lc-rec-diff diff-${rec.difficulty.toLowerCase()}`;
                document.getElementById('rec-coeff').textContent = `Weakness Coefficient ${(rec.weakness_score || 0.99).toFixed(2)}`;
                document.getElementById('rec-acc').textContent = `· ${rec.acceptance_rate}% acceptance`;
                document.getElementById('rec-tags').innerHTML = (rec.tags || ['Trie']).map(t => `<span class="lc-tag-pill">${t}</span>`).join('');
                document.getElementById('rec-url').href = rec.leetcode_url;
                
                const matchPct = Math.round((rec.weakness_score || 0.98) * 100);
                document.getElementById('rec-impact').textContent = matchPct;

                document.getElementById('bd-acc').textContent = `${rec.acceptance_rate}%`;
                document.getElementById('bd-match').textContent = `${matchPct} / 100`;
                document.getElementById('bd-diff').textContent = rec.difficulty.toUpperCase();
            } catch (err) {
                console.error(err);
            }
        }

        document.getElementById('search-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('username-input').value.trim();
            if (username) fetchUserData(username);
        });

        document.querySelectorAll('.lc-tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.lc-tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                activeDiff = btn.dataset.diff;
                const username = document.getElementById('username-input').value.trim();
                if (username) loadRecommendations(username, activeDiff);
            });
        });

        // Initial Load
        fetchUserData('neetcode');
    </script>
</body>
</html>
"""
