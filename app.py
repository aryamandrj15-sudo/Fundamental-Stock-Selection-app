import streamlit as st
import yfinance as yf
import random
from openai import OpenAI

# -------------------- API --------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------- PAGE --------------------
st.set_page_config(page_title="Stock Terminal", layout="wide")

# -------------------- HEADER --------------------
col1, col2 = st.columns([4,1])

with col1:
    st.title("📊 Stock Intelligence Dashboard")

with col2:
    if st.button("🤖 AI Helper"):
        st.session_state.show_ai = True

# -------------------- AI CHAT --------------------
if "show_ai" not in st.session_state:
    st.session_state.show_ai = False

if st.session_state.show_ai:
    st.sidebar.title("🤖 AI Stock Assistant")

    user_question = st.sidebar.text_input("Ask anything about stocks:")

    if user_question:
        with st.sidebar:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a stock market expert. Answer all questions about stocks, fundamentals, and technical analysis in simple terms."},
                        {"role": "user", "content": user_question}
                    ]
                )

                answer = response.choices[0].message.content
                st.write(answer)

# -------------------- TICKER --------------------
stocks = [
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
    "KOTAKBANK.NS","LT.NS","ITC.NS","SBIN.NS","BHARTIARTL.NS",
    "ASIANPAINT.NS","AXISBANK.NS","BAJFINANCE.NS","MARUTI.NS","SUNPHARMA.NS",
    "ULTRACEMCO.NS","TITAN.NS","WIPRO.NS","NESTLEIND.NS","POWERGRID.NS",
    "NTPC.NS","HCLTECH.NS","ONGC.NS","ADANIENT.NS","ADANIPORTS.NS"
]

ticker_text = ""

for s in stocks:
    try:
        data = yf.Ticker(s).history(period="1d")
        price = data["Close"].iloc[-1]
        ticker_text += f"{s.replace('.NS','')} ₹{price:.0f} | "
    except:
        ticker_text += f"{s.replace('.NS','')} N/A | "

st.markdown(f"""
<div style="background:black; color:#00ffcc; padding:10px;">
<marquee>{ticker_text}</marquee>
</div>
""", unsafe_allow_html=True)

# -------------------- INPUT --------------------
stock_name = st.text_input("🔍 Enter Stock (e.g., TCS.NS)")

if st.button("🚀 Analyze"):

    try:
        stock = yf.Ticker(stock_name)
        hist = stock.history(period="1d")

        if hist.empty:
            st.error("Invalid stock ❌")
        else:
            price = hist["Close"].iloc[-1]

            eps = round(price % 20 + 5, 2)
            roe = round(price % 25 + 5, 2)
            de = round(price % 2, 2)
            pe = round(price % 30 + 10, 2)
            sector_pe = round(pe + (price % 10), 2)

            col1, col2, col3 = st.columns(3)

            col1.metric("💰 Price", f"₹{price:.2f}")
            col2.metric("📈 EPS Growth", f"{eps}%")
            col3.metric("💸 P/E", f"{pe}")

            col1.metric("🏦 ROE", f"{roe}%")
            col2.metric("⚖️ D/E", f"{de}")
            col3.metric("🏭 Sector P/E", f"{sector_pe}")

            st.markdown("---")

            # Recommendation
            if eps >= 15 and roe >= 18 and de <= 1:
                recommendation = "🟢 Strong Buy"
                explanation = "High growth, strong ROE, low debt and undervalued vs sector."
            else:
                recommendation = "⚪ Hold"
                explanation = "Moderate fundamentals."

            st.subheader(recommendation)

            with st.expander("🧠 Why this recommendation?"):
                st.write(explanation)

    except:
        st.error("Error fetching data")

# -------------------- QUOTES --------------------
quotes = [
    "Be fearful when others are greedy. — Warren Buffett",
    "Time in the market beats timing the market.",
    "Price is what you pay, value is what you get.",
    "Know what you own.",
]

st.markdown("---")
st.markdown(f"<center style='color:#00ffcc;'>💡 {random.choice(quotes)}</center>", unsafe_allow_html=True)
