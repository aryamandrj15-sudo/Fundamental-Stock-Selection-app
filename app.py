import streamlit as st

# Page config
st.set_page_config(page_title="Stock Selection Tool", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>📊 Fundamental Stock Selection Model</h1>", unsafe_allow_html=True)
st.markdown("---")

# Input Section
st.subheader("📥 Enter Financial Metrics")

col1, col2 = st.columns(2)

with col1:
    eps = st.number_input("📈 EPS Growth (%)", min_value=0.0, step=0.1)
    roe = st.number_input("💰 ROE (%)", min_value=0.0, step=0.1)

with col2:
    de = st.number_input("⚖️ Debt/Equity", min_value=0.0, step=0.1)
    pe = st.number_input("💸 P/E Ratio", min_value=0.0, step=0.1)

st.markdown("---")

# Button
if st.button("🚀 Analyze Stock"):

    if eps >= 15 and roe >= 18 and de <= 1:
        if pe <= 20:
            result = "🟢 Strong Buy"
            st.success(result)
        else:
            result = "🟡 Buy (Expensive)"
            st.warning(result)

    elif eps >= 10 and roe >= 15 and de <= 1.5:
        result = "🟡 Buy"
        st.warning(result)

    elif de > 2:
        result = "🔴 Avoid (High Debt)"
        st.error(result)

    else:
        result = "⚪ Hold"
        st.info(result)

    st.markdown("---")

    # Extra Insight
    st.subheader("📊 Quick Insight")
    st.write(f"""
    - EPS Growth: {eps}%
    - ROE: {roe}%
    - Debt/Equity: {de}
    - P/E Ratio: {pe}
    """)
