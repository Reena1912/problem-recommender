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
            --sage-accent: #dce8e0;
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
            padding-bottom: 3rem;
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
            padding: 1rem 0;
        }
        .lc-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .lc-nav-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: var(--forest-green);
        }
        .lc-nav-logo span { color: var(--emerald-green); }
        .lc-nav-links {
            display: flex;
            gap: 2rem;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-muted);
        }
        .lc-nav-links a:hover { color: var(--forest-green); }
        .lc-nav-cta {
            background: var(--forest-green);
            color: #ffffff;
            font-weight: 700;
            padding: 0.5rem 1.2rem;
            border-radius: 50px;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        .lc-nav-cta:hover { background: #0b1d19; transform: translateY(-1px); }

        /* Hero */
        .lc-hero-section {
            padding: 4rem 0 2.5rem;
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
            font-size: 3rem;
            font-weight: 800;
            line-height: 1.1;
            color: var(--forest-green);
            margin-bottom: 1.2rem;
            letter-spacing: -0.03em;
        }
        .lc-hero-desc {
            font-size: 1.05rem;
            color: var(--text-muted);
            max-width: 650px;
            margin-bottom: 2rem;
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
            padding: 0.8rem 2rem;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .lc-search-btn:hover {
            background: #0b1d19;
            transform: translateY(-1px);
        }

        /* Initial Placeholder */
        .lc-initial-card {
            background: var(--card-bg);
            border: 1px dashed #c4d7cc;
            border-radius: 24px;
            padding: 4rem 2rem;
            text-align: center;
            margin-top: 1.5rem;
        }
        .lc-initial-icon {
            font-size: 2.8rem;
            margin-bottom: 0.8rem;
        }
        .lc-initial-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 800;
            color: var(--forest-green);
            margin-bottom: 0.4rem;
        }
        .lc-initial-sub {
            font-size: 0.9rem;
            color: var(--text-muted);
            max-width: 480px;
            margin: 0 auto;
        }

        /* Hidden Results Container */
        #results-container {
            display: none;
        }

        /* Stats Grid */
        .lc-stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.2rem;
            margin-bottom: 2.5rem;
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

        /* Section Header */
        .lc-sec-hdr {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1.8rem;
            margin-top: 3rem;
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

        /* Analytics Grid */
        .lc-analytics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.8rem;
            margin-bottom: 3rem;
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

        /* Recommendations */
        .lc-rec-tabs {
            display: flex;
            gap: 0.8rem;
            margin-bottom: 1.8rem;
        }
        .lc-tab-btn {
            background: #ffffff;
            border: 1px solid var(--border-color);
            padding: 0.5rem 1.2rem;
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
        .lc-rec-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 1.8rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.03);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .lc-rec-diff {
            font-size: 0.72rem;
            font-weight: 800;
            padding: 0.2rem 0.7rem;
            border-radius: 50px;
            text-transform: uppercase;
            display: inline-block;
            margin-bottom: 0.6rem;
        }
        .diff-easy { background: #dcfce7; color: #16a34a; }
        .diff-medium { background: #fef3c7; color: #d97706; }
        .diff-hard { background: #fee2e2; color: #dc2626; }

        .lc-rec-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.3rem;
            font-weight: 800;
            color: var(--forest-green);
            margin-bottom: 0.4rem;
        }
        .lc-rec-tags {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        .lc-tag-pill {
            background: #f0f5f2;
            color: var(--text-muted);
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.15rem 0.6rem;
            border-radius: 6px;
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
        .lc-solve-btn:hover {
            background: #0b1d19;
            transform: translateY(-1px);
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
            .lc-stats-grid { grid-template-columns: repeat(2, 1fr); }
            .lc-analytics-grid { grid-template-columns: 1fr; }
            .lc-hero-title { font-size: 2.2rem; }
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
                    <a href="#analytics">Analytics</a>
                    <a href="/docs" target="_blank">API Docs</a>
                </div>
                <a href="#search" class="lc-nav-cta">Analyze Profile</a>
            </div>
        </div>
    </div>

    <!-- HERO -->
    <div class="lc-hero-section">
        <div class="lc-container">
            <div class="lc-eyebrow"><span class="lc-eyebrow-line"></span>Data-Driven Practice Platform</div>
            <h1 class="lc-hero-title">Stop grinding blindly.<br>Target your exact skill gaps.</h1>
            <p class="lc-hero-desc">An intelligent system that analyzes LeetCode profiles, detects algorithmic blind spots, and recommends the most impactful problems to solve next — backed by data-driven weakness scoring.</p>
        </div>
    </div>

    <!-- MAIN DASHBOARD CONTENT -->
    <div class="lc-container">
        
        <!-- SEARCH CARD -->
        <div class="lc-search-card" id="search">
            <div class="lc-search-title">Analyze Any LeetCode Profile</div>
            <div class="lc-search-sub">Enter a username below to calculate weakness scores across 40+ algorithmic topics.</div>
            <form class="lc-search-form" id="search-form">
                <input type="text" id="username-input" class="lc-search-input" placeholder="e.g. neetcode, tourist, or NovaAsher…" value="">
                <button type="submit" class="lc-search-btn">Analyze Profile →</button>
            </form>
        </div>

        <!-- INITIAL PLACEHOLDER -->
        <div class="lc-initial-card" id="initial-prompt">
            <div class="lc-initial-icon">🎯</div>
            <div class="lc-initial-title">Ready to Analyze Your Profile</div>
            <div class="lc-initial-sub">Type any LeetCode username into the box above and click <b style="color:var(--forest-green);">Analyze Profile →</b> to view skill analytics and target recommendations.</div>
        </div>

        <!-- HIDDEN RESULTS UNTIL USER SEARCHES -->
        <div id="results-container">
            <!-- STATS COUNTERS -->
            <div class="lc-stats-grid">
                <div class="lc-stat-card">
                    <div class="lc-stat-hdr">
                        <div class="lc-stat-title">Total Solved</div>
                        <div class="lc-stat-badge" style="background:#e8f4ec;color:#16a34a;" id="st-tot-pct">0%</div>
                    </div>
                    <div class="lc-stat-val" id="st-tot-val">0</div>
                    <div class="lc-stat-sub" id="st-tot-sub">out of 3,900+ problems</div>
                </div>
                <div class="lc-stat-card">
                    <div class="lc-stat-hdr">
                        <div class="lc-stat-title">Easy Solved</div>
                        <div class="lc-stat-badge" style="background:#dcfce7;color:#16a34a;" id="st-ez-pct">0%</div>
                    </div>
                    <div class="lc-stat-val" id="st-ez-val">0</div>
                    <div class="lc-stat-sub" id="st-ez-sub">out of 950+ easy</div>
                </div>
                <div class="lc-stat-card">
                    <div class="lc-stat-hdr">
                        <div class="lc-stat-title">Medium Solved</div>
                        <div class="lc-stat-badge" style="background:#fef3c7;color:#d97706;" id="st-md-pct">0%</div>
                    </div>
                    <div class="lc-stat-val" id="st-md-val">0</div>
                    <div class="lc-stat-sub" id="st-md-sub">out of 2,000+ medium</div>
                </div>
                <div class="lc-stat-card">
                    <div class="lc-stat-hdr">
                        <div class="lc-stat-title">Hard Solved</div>
                        <div class="lc-stat-badge" style="background:#fee2e2;color:#dc2626;" id="st-hd-pct">0%</div>
                    </div>
                    <div class="lc-stat-val" id="st-hd-val">0</div>
                    <div class="lc-stat-sub" id="st-hd-sub">out of 950+ hard</div>
                </div>
            </div>

            <!-- ANALYTICS SECTION -->
            <div class="lc-sec-hdr" id="analytics">
                <div class="lc-sec-num">01</div>
                <div>
                    <div class="lc-sec-title">Skill Analytics & Practice Targets</div>
                    <div class="lc-sec-sub">Simple breakdown of your weakest topics and difficulty progress</div>
                </div>
            </div>

            <div class="lc-analytics-grid">
                <div class="lc-chart-card">
                    <div class="lc-chart-title">📉 Top Topics Needing Practice</div>
                    <canvas id="barChart" height="220"></canvas>
                </div>
                <div class="lc-chart-card">
                    <div class="lc-chart-title">🍰 Solved Problems by Difficulty</div>
                    <canvas id="donutChart" height="220"></canvas>
                </div>
            </div>

            <!-- RECOMMENDATIONS SECTION -->
            <div class="lc-sec-hdr">
                <div class="lc-sec-num">02</div>
                <div>
                    <div class="lc-sec-title">Recommended Challenges</div>
                    <div class="lc-sec-sub">Ranked by how directly they target your top algorithmic skill gaps</div>
                </div>
            </div>

            <div class="lc-rec-tabs">
                <button class="lc-tab-btn active" data-diff="all">✦ All Recommendations</button>
                <button class="lc-tab-btn" data-diff="easy">🟢 Easy Problems</button>
                <button class="lc-tab-btn" data-diff="medium">🟠 Medium Problems</button>
                <button class="lc-tab-btn" data-diff="hard">🔴 Hard Problems</button>
            </div>

            <div id="recommendations-container">
                <div style="text-align:center;padding:2rem;color:var(--text-muted);">Loading recommendations…</div>
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
            document.getElementById('initial-prompt').style.display = 'none';
            document.getElementById('results-container').style.display = 'block';

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
                document.getElementById('recommendations-container').innerHTML = 
                    `<div style="color:#dc2626;padding:2rem;background:#fee2e2;border-radius:12px;text-align:center;">⚠️ Unable to fetch data for @${username}. Please check username.</div>`;
            }
        }

        function updateStats(stats) {
            const sc = stats.solve_counts || {};
            const ta = stats.total_available || {};

            const calcPct = (s, t) => t ? ((s / t) * 100).toFixed(1) : '0.0';

            document.getElementById('st-tot-val').textContent = (sc.All || 0).toLocaleString();
            document.getElementById('st-tot-pct').textContent = `${calcPct(sc.All || 0, ta.All || 1)}%`;
            document.getElementById('st-tot-sub').textContent = `out of ${(ta.All || 3900).toLocaleString()} available`;

            document.getElementById('st-ez-val').textContent = (sc.Easy || 0).toLocaleString();
            document.getElementById('st-ez-pct').textContent = `${calcPct(sc.Easy || 0, ta.Easy || 1)}%`;

            document.getElementById('st-md-val').textContent = (sc.Medium || 0).toLocaleString();
            document.getElementById('st-md-pct').textContent = `${calcPct(sc.Medium || 0, ta.Medium || 1)}%`;

            document.getElementById('st-hd-val').textContent = (sc.Hard || 0).toLocaleString();
            document.getElementById('st-hd-pct').textContent = `${calcPct(sc.Hard || 0, ta.Hard || 1)}%`;
        }

        function updateCharts(stats) {
            const ts = stats.tag_scores || [];
            const sortedTs = [...ts].sort((a, b) => b.weakness_score - a.weakness_score).slice(0, 8);

            const labels1 = sortedTs.map(t => t.tag);
            const data1 = sortedTs.map(t => (t.weakness_score * 100).toFixed(1));

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
                        x: { max: 100, grid: { color: '#e4ebe6' } },
                        y: { grid: { display: false } }
                    }
                }
            });

            const sc = stats.solve_counts || {};
            const easy = sc.Easy || 0;
            const med = sc.Medium || 0;
            const hard = sc.Hard || 0;

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
            const container = document.getElementById('recommendations-container');
            container.innerHTML = '<div style="text-align:center;padding:2rem;color:var(--text-muted);">Fetching recommended challenges…</div>';

            try {
                let url = `/recommend?username=${encodeURIComponent(username)}`;
                if (difficulty !== 'all') {
                    url = `/recommend/${difficulty}?username=${encodeURIComponent(username)}`;
                }
                const res = await fetch(url);
                if (!res.ok) throw new Error("Failed to fetch recommendation");
                const data = await res.json();
                
                const rec = data.recommendation;
                if (!rec) {
                    container.innerHTML = '<div style="padding:2rem;text-align:center;">No problems found.</div>';
                    return;
                }

                const diffClass = `diff-${rec.difficulty.toLowerCase()}`;
                const tagsHtml = (rec.tags || []).map(t => `<span class="lc-tag-pill">${t}</span>`).join('');
                const matchPct = (rec.weakness_score * 100).toFixed(0);

                container.innerHTML = `
                    <div class="lc-rec-card">
                        <div>
                            <span class="lc-rec-diff ${diffClass}">${rec.difficulty}</span>
                            <div class="lc-rec-title">${rec.title}</div>
                            <div style="font-size:0.85rem;color:var(--text-muted);margin-bottom:0.8rem;">
                                Acceptance Rate: <b>${rec.acceptance_rate}%</b> · Match Priority: <b style="color:var(--forest-green);">${matchPct}%</b>
                            </div>
                            <div class="lc-rec-tags">${tagsHtml}</div>
                        </div>
                        <div>
                            <a href="${rec.leetcode_url}" target="_blank" class="lc-solve-btn">Solve Challenge ↗</a>
                        </div>
                    </div>
                `;
            } catch (err) {
                console.error(err);
                container.innerHTML = '<div style="color:#dc2626;padding:1.5rem;text-align:center;">Failed to load recommendations.</div>';
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
    </script>
</body>
</html>
"""
