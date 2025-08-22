import os
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

ANALYSIS_FOLDER = "data/analysis"

# Set Streamlit app title
st.set_page_config(page_title="Earnings Call Dashboard", layout="wide")
st.title("NVIDIA Earnings Call Insights (2025)")

# File selector
files = [f for f in os.listdir(ANALYSIS_FOLDER) if f.endswith("_analysis.json")]
selected_file = st.selectbox("Select a Quarter Transcript", files)

if selected_file:
    with open(os.path.join(ANALYSIS_FOLDER, selected_file), "r") as f:
        data = json.load(f)

    st.subheader("Summary")
    st.write(f"**Management Sentiment:** {data['Management Sentiment']}")
    st.write(f"**Q&A Sentiment:** {data['Q&A Sentiment']}")
    st.write(f"**Tone Change vs Previous Quarter:** {data['Quarter-over-Quarter Tone Change']}")

    st.subheader("Strategic Focuses")
    for i, focus in enumerate(data["Strategic Focuses"], 1):
        st.markdown(f"{i}. {focus}")

# Optional: Multi-quarter comparison
st.subheader("Trend Comparison")
trend_data = []

for f in sorted(files):
    with open(os.path.join(ANALYSIS_FOLDER, f), "r") as file:
        d = json.load(file)
        quarter = f.split()[0]  # e.g., "Q1"
        trend_data.append({
            "Quarter": quarter,
            "Management": d["Management Sentiment"],
            "Q&A": d["Q&A Sentiment"],
            "Tone": d["Quarter-over-Quarter Tone Change"]
        })

df = pd.DataFrame(trend_data)

sentiment_map = {"Positive": 1, "Neutral": 0, "Negative": -1}
df["Mgmt Score"] = df["Management"].map(sentiment_map)
df["Q&A Score"] = df["Q&A"].map(sentiment_map)
df["Tone Score"] = df["Tone"].map(sentiment_map)

st.line_chart(df.set_index("Quarter")[["Mgmt Score", "Q&A Score", "Tone Score"]])
