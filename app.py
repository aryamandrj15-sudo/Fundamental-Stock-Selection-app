import streamlit as st

st.title("📊 Fundamental Stock Selection Model")

eps = st.number_input("EPS Growth (%)")
de = st.number_input("Debt/Equity")
roe = st.number_input("ROE (%)")
pe = st.number_input("P/E Ratio")

if st.button("Analyze"):

    if eps >= 15 and roe >= 18 and de <= 1:
        if pe <= 20:
            result = "🟢 Strong Buy"
        else:
            result = "🟡 Buy (Expensive)"
    
    elif eps >= 10 and roe >= 15 and de <= 1.5:
        result = "🟡 Buy"

    elif de > 2:
        result = "🔴 Avoid (High Debt)"

    else:
        result = "⚪ Hold"

    st.write("Recommendation:", result)
