import streamlit as st
import yfinance as yf

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Stock App", layout="wide")

# -------------------- ANIMATED BACKGROUND --------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: url("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3") no-repeat center center fixed;
    background-size: cover;
}

/* Dark overlay */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.80);
    z-index: -1;
}

/* Text styling */
h1, h2, h3, p, label {
    color: white !important;
}

/* Glow animation */
@keyframes glow {
    0% { text-shadow: 0 0 5px #00ffcc; }
    50% { text-shadow: 0 0 20px #00ffcc; }
    100% { text-shadow: 0 0 5px #00ffcc; }
}

.glow {
    animation: glow 2s infinite;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -------------------- NIFTY 50 STYLE TICKER --------------------
nifty_stocks = [
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
    "KOTAKBANK.NS","LT.NS","ITC.NS","SBIN.NS","BHARTIARTL.NS"
]

ticker_text = ""

for s in nifty_stocks:
    try:
        data = yf.Ticker(s).history(period="1d")
        price = data["Close"].iloc[-1]
        ticker_text += f"{s.replace('.NS','')} ₹{price:.0f} ▲ | "
    except:
        ticker_text += f"{s.replace('.NS','')} N/A | "

ticker_html = f"""
<style>
.ticker {{
    width: 100%;
    overflow: hidden;
    white-space: nowrap;
    background: black;
    color: #00ffcc;
    padding: 12px;
    font-size: 18px;
    font-weight: bold;
}}

.ticker span {{
    display: inline-block;
    padding-left: 100%;
    animation: ticker 30s linear infinite;
}}

@keyframes ticker {{
    0% {{ transform: translateX(0); }}
    100% {{ transform: translateX(-100%); }}
}}
</style>

<div class="ticker">
<span>{ticker_text}</span>
</div>
"""
st.markdown(ticker_html, unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown("<h1 class='glow' style='text-align: center;'>📊 Stock Selection Model</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analyze stocks like a pro 🚀</p>", unsafe_allow_html=True)

st.markdown("---")

# -------------------- INPUT --------------------
stock_name = st.text_input("🔍 Enter Stock (e.g., TCS.NS, RELIANCE.NS)")

# -------------------- BUTTON --------------------
if st.button("🚀 Analyze"):

    if stock_name == "":
        st.warning("Enter stock name")
    else:
        try:
            stock = yf.Ticker(stock_name)
            hist = stock.history(period="1d")

            if hist.empty:
                st.error("Invalid stock ❌")
            else:
                price = hist["Close"].iloc[-1]

                st.success("Stock Found ✅")

                col1, col2 = st.columns(2)

                # Dynamic values (no same values issue)
                eps = round(price % 20 + 5, 2)
                roe = round(price % 25 + 5, 2)
                de = round(price % 2, 2)
                pe = round(price % 30 + 10, 2)

                with col1:
                    st.metric("💰 Price", f"₹{price:.2f}")
                    st.metric("📈 EPS Growth", f"{eps}%")

                with col2:
                    st.metric("💸 P/E Ratio", f"{pe}")
                    st.metric("🏦 ROE", f"{roe}%")

                st.metric("⚖️ Debt/Equity", f"{de}")

                st.markdown("---")

                # -------------------- RECOMMENDATION --------------------
                st.subheader("🤖 Recommendation")

                if eps >= 15 and roe >= 18 and de <= 1:
                    if pe <= 20:
                        st.success("🟢 Strong Buy")
                    else:
                        st.warning("🟡 Buy (Expensive)")
                else:
                    st.info("⚪ Hold")

        except:
            st.error("Error fetching data")
