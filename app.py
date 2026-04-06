import streamlit as st
import time

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StockSense · Fundamental Analyzer",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Inject Custom CSS + Animated Background ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* ── Root Variables ── */
:root {
    --bg:        #070d17;
    --surface:   #0d1a2a;
    --border:    #1a3050;
    --accent:    #00d4ff;
    --green:     #00ff88;
    --yellow:    #ffd60a;
    --red:       #ff4560;
    --text:      #c8dff0;
    --muted:     #5a7a9a;
    --glow:      0 0 20px rgba(0, 212, 255, 0.25);
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

.stApp {
    background-color: var(--bg) !important;
}

/* ── Animated SVG background canvas ── */
.bg-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}

/* ── Main content above background ── */
.block-container {
    position: relative;
    z-index: 1;
    padding-top: 2rem !important;
    max-width: 760px !important;
}

/* ── Header ── */
.header-wrap {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.header-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid var(--accent);
    padding: 4px 14px;
    border-radius: 2px;
    margin-bottom: 1rem;
    box-shadow: var(--glow);
}
.header-title {
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.1;
    color: #fff;
    letter-spacing: -0.02em;
    margin: 0;
}
.header-title span {
    color: var(--accent);
}
.header-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 0.6rem;
    letter-spacing: 0.08em;
}

/* ── Section label ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 2rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Input cards ── */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    border-color: var(--accent);
    box-shadow: var(--glow);
}

/* ── Streamlit number inputs ── */
.stNumberInput > div > div > input {
    background: #0a1828 !important;
    border: 1px solid var(--border) !important;
    color: var(--accent) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 1.1rem !important;
    border-radius: 6px !important;
    padding: 0.5rem 0.8rem !important;
}
.stNumberInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: var(--glow) !important;
}
.stNumberInput label {
    color: var(--text) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
}

/* ── Analyze Button ── */
.stButton > button {
    width: 100% !important;
    background: transparent !important;
    border: 1.5px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    padding: 0.9rem 2rem !important;
    border-radius: 6px !important;
    margin-top: 1rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: rgba(0, 212, 255, 0.08) !important;
    box-shadow: var(--glow) !important;
    transform: translateY(-1px) !important;
}

/* ── Result Box ── */
.result-box {
    border-radius: 10px;
    padding: 1.8rem 2rem;
    margin: 1.5rem 0 1rem;
    text-align: center;
    animation: fadeSlide 0.4s ease;
}
@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-box.green  { border: 1.5px solid var(--green);  background: rgba(0,255,136,0.06);  }
.result-box.yellow { border: 1.5px solid var(--yellow); background: rgba(255,214,10,0.06); }
.result-box.red    { border: 1.5px solid var(--red);    background: rgba(255,69,96,0.06);  }
.result-box.grey   { border: 1.5px solid var(--muted);  background: rgba(90,122,154,0.06); }

.result-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.result-verdict {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.01em;
    line-height: 1.2;
}
.result-box.green  .result-verdict { color: var(--green);  }
.result-box.yellow .result-verdict { color: var(--yellow); }
.result-box.red    .result-verdict { color: var(--red);    }
.result-box.grey   .result-verdict { color: var(--muted);  }

/* ── Metrics row ── */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.7rem;
    margin: 1.2rem 0;
}
.m-tile {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 0.6rem;
    text-align: center;
}
.m-tile-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
}
.m-tile-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--accent);
}

/* ── Score bar ── */
.score-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    margin: 0.8rem 0;
}
.score-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.8rem;
}
.bar-row {
    margin-bottom: 0.7rem;
}
.bar-label {
    display: flex;
    justify-content: space-between;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--text);
    margin-bottom: 0.3rem;
}
.bar-track {
    height: 4px;
    background: var(--border);
    border-radius: 2px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.6s ease;
}

/* ── Footer ── */
.footer {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--muted);
    text-align: center;
    padding: 2rem 0 1rem;
    letter-spacing: 0.08em;
}

/* ── Streamlit chrome cleanup ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
div[data-testid="stDecoration"] { display: none; }

/* ── Divider override ── */
hr { border-color: var(--border) !important; }
</style>

<!-- Animated SVG background: candlestick chart + grid lines + floating tickers -->
<div class="bg-canvas">
<svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
      <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#1a3050" stroke-width="0.5" opacity="0.5"/>
    </pattern>

    <linearGradient id="chartLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00d4ff" stop-opacity="0"/>
      <stop offset="40%" stop-color="#00d4ff" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#00ff88" stop-opacity="0.3"/>
    </linearGradient>
    <linearGradient id="chartFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#00d4ff" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#00d4ff" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="line2" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00ff88" stop-opacity="0"/>
      <stop offset="50%" stop-color="#00ff88" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#ffd60a" stop-opacity="0.2"/>
    </linearGradient>
  </defs>

  <!-- Grid -->
  <rect width="100%" height="100%" fill="url(#grid)"/>

  <!-- Chart area fill -->
  <path d="M0,420 C80,390 160,340 260,310 C340,285 420,320 500,280 C580,240 660,190 740,160 C820,130 900,150 980,120 C1060,90 1140,110 1220,85 L1220,520 L0,520Z"
        fill="url(#chartFill)"/>

  <!-- Primary chart line -->
  <path d="M0,420 C80,390 160,340 260,310 C340,285 420,320 500,280 C580,240 660,190 740,160 C820,130 900,150 980,120 C1060,90 1140,110 1220,85"
        fill="none" stroke="url(#chartLine)" stroke-width="2" opacity="0.7">
    <animate attributeName="stroke-dasharray" from="0 2000" to="2000 0" dur="4s" fill="freeze" begin="0s"/>
  </path>

  <!-- Secondary chart line -->
  <path d="M0,480 C100,460 200,430 300,400 C400,370 480,390 560,360 C640,330 720,290 820,270 C900,255 980,275 1060,240 C1140,205 1200,220 1280,195"
        fill="none" stroke="url(#line2)" stroke-width="1.5" opacity="0.5">
    <animate attributeName="stroke-dasharray" from="0 2000" to="2000 0" dur="5s" fill="freeze" begin="0.5s"/>
  </path>

  <!-- Candlesticks (decorative, scattered) -->
  <!-- Green candles -->
  <g opacity="0.25" fill="#00ff88" stroke="#00ff88">
    <rect x="60"  y="370" width="8" height="30" rx="1"/>
    <line x1="64"  y1="365" x2="64"  y2="405" stroke-width="1"/>
    <rect x="140" y="330" width="8" height="25" rx="1"/>
    <line x1="144" y1="325" x2="144" y2="360" stroke-width="1"/>
    <rect x="320" y="295" width="8" height="22" rx="1"/>
    <line x1="324" y1="288" x2="324" y2="320" stroke-width="1"/>
    <rect x="500" y="268" width="8" height="28" rx="1"/>
    <line x1="504" y1="260" x2="504" y2="300" stroke-width="1"/>
    <rect x="700" y="148" width="8" height="25" rx="1"/>
    <line x1="704" y1="140" x2="704" y2="178" stroke-width="1"/>
    <rect x="900" y="118" width="8" height="20" rx="1"/>
    <line x1="904" y1="110" x2="904" y2="142" stroke-width="1"/>
    <rect x="1100" y="88" width="8" height="18" rx="1"/>
    <line x1="1104" y1="80" x2="1104" y2="110" stroke-width="1"/>
  </g>
  <!-- Red candles -->
  <g opacity="0.2" fill="#ff4560" stroke="#ff4560">
    <rect x="100" y="345" width="8" height="25" rx="1"/>
    <line x1="104" y1="338" x2="104" y2="374" stroke-width="1"/>
    <rect x="220" y="308" width="8" height="20" rx="1"/>
    <line x1="224" y1="302" x2="224" y2="332" stroke-width="1"/>
    <rect x="420" y="298" width="8" height="28" rx="1"/>
    <line x1="424" y1="292" x2="424" y2="330" stroke-width="1"/>
    <rect x="620" y="200" width="8" height="22" rx="1"/>
    <line x1="624" y1="194" x2="624" y2="226" stroke-width="1"/>
    <rect x="820" y="138" width="8" height="18" rx="1"/>
    <line x1="824" y1="132" x2="824" y2="160" stroke-width="1"/>
  </g>

  <!-- Floating ticker labels -->
  <g font-family="monospace" font-size="10" fill="#00d4ff" opacity="0.12" letter-spacing="1">
    <text x="30"   y="80">NIFTY +1.24%</text>
    <text x="250"  y="180">SENSEX +0.87%</text>
    <text x="500"  y="60">RELIANCE ▲</text>
    <text x="780"  y="210">TCS +2.1%</text>
    <text x="1020" y="130">INFY ▼ -0.4%</text>
    <text x="100"  y="500">P/E: 18.4</text>
    <text x="400"  y="480">ROE: 22.3%</text>
    <text x="700"  y="510">EPS: +16.7%</text>
    <text x="950"  y="490">D/E: 0.42</text>
  </g>

  <!-- Horizontal reference lines -->
  <line x1="0" y1="200" x2="100%" y2="200" stroke="#1a3050" stroke-width="0.8" stroke-dasharray="6,8" opacity="0.5"/>
  <line x1="0" y1="350" x2="100%" y2="350" stroke="#1a3050" stroke-width="0.8" stroke-dasharray="6,8" opacity="0.4"/>
  <line x1="0" y1="450" x2="100%" y2="450" stroke="#1a3050" stroke-width="0.8" stroke-dasharray="6,8" opacity="0.3"/>
</svg>
</div>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-wrap">
    <div class="header-badge">Fundamental Analysis Engine v1.0</div>
    <h1 class="header-title">Stock<span>Sense</span></h1>
    <p class="header-sub">Enter financial metrics · Get an instant signal</p>
</div>
""", unsafe_allow_html=True)

# ── Input Section ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Financial Inputs</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    eps = st.number_input("📈  EPS Growth (%)", min_value=0.0, max_value=200.0, step=0.1,
                          help="Earnings Per Share growth YoY")
    roe = st.number_input("💰  Return on Equity (%)", min_value=0.0, max_value=100.0, step=0.1,
                          help="Net income / Shareholders' equity")
with col2:
    de  = st.number_input("⚖️  Debt / Equity Ratio", min_value=0.0, max_value=20.0, step=0.01,
                          help="Total debt / Total equity")
    pe  = st.number_input("💸  P/E Ratio", min_value=0.0, max_value=500.0, step=0.1,
                          help="Price / Earnings per share")

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
analyze = st.button("▶  RUN ANALYSIS", use_container_width=True)

# ── Analysis Logic ─────────────────────────────────────────────────────────────
if analyze:
    with st.spinner(""):
        time.sleep(0.6)   # brief dramatic pause

    # Determine verdict
    if eps >= 15 and roe >= 18 and de <= 1:
        if pe <= 20:
            verdict = "STRONG BUY"
            emoji   = "🟢"
            css_cls = "green"
            logic   = "Excellent fundamentals at a fair valuation."
        else:
            verdict = "BUY · EXPENSIVE"
            emoji   = "🟡"
            css_cls = "yellow"
            logic   = "Great fundamentals, but valuation is stretched."
    elif eps >= 10 and roe >= 15 and de <= 1.5:
        verdict = "BUY"
        emoji   = "🟡"
        css_cls = "yellow"
        logic   = "Solid metrics. Watch for P/E before entering."
    elif de > 2:
        verdict = "AVOID"
        emoji   = "🔴"
        css_cls = "red"
        logic   = "High leverage is a significant risk factor."
    else:
        verdict = "HOLD"
        emoji   = "⚪"
        css_cls = "grey"
        logic   = "Mixed signals. Await clearer catalysts."

    # Result card
    st.markdown(f"""
    <div class="result-box {css_cls}">
        <div class="result-label">Signal</div>
        <div class="result-verdict">{emoji} {verdict}</div>
        <div style="font-size:0.78rem; color:#8aa8c4; margin-top:0.5rem; font-family:'Space Mono',monospace;">{logic}</div>
    </div>
    """, unsafe_allow_html=True)

    # Metric tiles
    st.markdown(f"""
    <div class="metrics-row">
        <div class="m-tile">
            <div class="m-tile-label">EPS Growth</div>
            <div class="m-tile-value">{eps:.1f}%</div>
        </div>
        <div class="m-tile">
            <div class="m-tile-label">ROE</div>
            <div class="m-tile-value">{roe:.1f}%</div>
        </div>
        <div class="m-tile">
            <div class="m-tile-label">Debt/Equity</div>
            <div class="m-tile-value">{de:.2f}</div>
        </div>
        <div class="m-tile">
            <div class="m-tile-label">P/E Ratio</div>
            <div class="m-tile-value">{pe:.1f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Score bars (normalised, capped for display)
    def pct(val, low, high):
        return min(100, max(0, int((val - low) / (high - low) * 100)))

    eps_pct = pct(eps, 0, 30)
    roe_pct = pct(roe, 0, 30)
    de_pct  = pct(3 - de, 0, 3)   # inverted: lower D/E is better
    pe_pct  = pct(50 - pe, 0, 50) # inverted: lower P/E is better

    def bar_color(p):
        if p >= 65: return "var(--green)"
        if p >= 35: return "var(--yellow)"
        return "var(--red)"

    st.markdown(f"""
    <div class="score-wrap">
        <div class="score-title">Metric Scorecard</div>

        <div class="bar-row">
            <div class="bar-label"><span>EPS Growth</span><span>{eps:.1f}%</span></div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{eps_pct}%; background:{bar_color(eps_pct)};"></div>
            </div>
        </div>

        <div class="bar-row">
            <div class="bar-label"><span>Return on Equity</span><span>{roe:.1f}%</span></div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{roe_pct}%; background:{bar_color(roe_pct)};"></div>
            </div>
        </div>

        <div class="bar-row">
            <div class="bar-label"><span>Debt/Equity (lower = better)</span><span>{de:.2f}</span></div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{de_pct}%; background:{bar_color(de_pct)};"></div>
            </div>
        </div>

        <div class="bar-row">
            <div class="bar-label"><span>P/E Ratio (lower = cheaper)</span><span>{pe:.1f}</span></div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{pe_pct}%; background:{bar_color(pe_pct)};"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    StockSense · Built with Streamlit · For educational use only<br>
    Not financial advice · Always do your own research
</div>
""", unsafe_allow_html=True)
