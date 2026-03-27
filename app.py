import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Industrial AI Dashboard", layout="wide")

st.title("🏭 Industrial Monitoring System")

# Simulated Data
temp = random.randint(20, 100)
pressure = random.randint(1, 10)

col1, col2 = st.columns(2)

with col1:
    st.metric("Temperature (°C)", temp)

with col2:
    st.metric("Pressure", pressure)

# AI Decision Logic
if temp > 75 and pressure > 7:
    st.error("⚠️ HIGH RISK: Possible Machine Failure")
    st.write("👉 Action: Reduce load immediately")
elif temp > 60:
    st.warning("⚠️ Warning: Monitor system closely")
else:
    st.success("✅ System Stable")

# Graph
data = pd.DataFrame({
    "Time": range(10),
    "Temp": [random.randint(20, 100) for _ in range(10)]
})

st.line_chart(data.set_index("Time"))