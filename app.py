import streamlit as st
import yfinance as yf

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Stock App", layout="wide")

# -------------------- BACKGROUND --------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1642543492481-44e81e3914a7");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Dark overlay */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.75);
    z-index: -1;
}

/* Text color */
h1, h2, h3, p, label {
    color: white !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -------------------- LIVE TICKER --------------------
stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ITC.NS"]

ticker_text = ""

for s in stocks:
    try:
        data = yf.Ticker(s).history(period="1d")
        price = data["Close"].iloc[-1]
        ticker_text += f"{s.replace('.NS','')} ₹{price:.0f}  |  "
    except:
        ticker_text += f"{s.replace('.NS','')} N/A  |  "

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
    animation: ticker 25s linear infinite;
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
st.markdown("<h1 style='text-align: center;'>📊 Stock Selection Model</h1>", unsafe_allow_html=True)
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

                # Layout
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("💰 Price", f"₹{price:.2f}")

                # Dummy logic (stable)
                eps = round(price % 20 + 5, 2)
                roe = round(price % 25 + 5, 2)
                de = round(price % 2, 2)
                pe = round(price % 30 + 10, 2)

                with col2:
                    st.metric("📈 EPS Growth", f"{eps}%")

                st.metric("🏦 ROE", f"{roe}%")
                st.metric("⚖️ Debt/Equity", f"{de}")
                st.metric("💸 P/E Ratio", f"{pe}")

                st.markdown("---")

                # Recommendation
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
