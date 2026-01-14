import os
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Configuration & Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Earnings Call Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a "nice" look
st.markdown("""
<style>
    /* Global basic styles */
    .main {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #0e1117;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Metrics styling */
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #333;
    }
    
    /* Card-like look for containers */
    .stContainer {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

script_dir = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_FOLDER = os.path.join(script_dir, "../data/analysis")

# Map sentiment text to numerical scores for charting
SENTIMENT_MAP = {"Positive": 1, "Neutral": 0, "Negative": -1}
COLOR_MAP = {"Positive": "green", "Neutral": "gray", "Negative": "red"}

# -----------------------------------------------------------------------------
# Data Loading
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    """Loads all JSON analysis files and returns a DataFrame and raw dicts."""
    if not os.path.exists(ANALYSIS_FOLDER):
        return pd.DataFrame(), {}
        
    files = [f for f in os.listdir(ANALYSIS_FOLDER) if f.endswith("_analysis.json")]
    all_data = []
    file_map = {}
    
    for f in sorted(files):
        with open(os.path.join(ANALYSIS_FOLDER, f), "r") as file:
            d = json.load(file)
            quarter = f.split()[0] # e.g. "Q1" or "Q1 2025..." depending on filename
            # Clean up quarter name if it's long
            if " " in f:
                quarter = f.split()[0]
            
            d["Quarter"] = quarter
            d["Filename"] = f
            d["Mgmt Score"] = SENTIMENT_MAP.get(d.get("Management Sentiment", "Neutral"), 0)
            d["Q&A Score"] = SENTIMENT_MAP.get(d.get("Q&A Sentiment", "Neutral"), 0)
            d["Tone Score"] = SENTIMENT_MAP.get(d.get("Quarter-over-Quarter Tone Change", "Neutral"), 0)
            
            all_data.append(d)
            file_map[quarter] = d

    df = pd.DataFrame(all_data)
    # Sort by Quarter logic (simple alphanumeric sort for now)
    df = df.sort_values("Quarter")
    return df, file_map

df, data_map = load_data()

# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
st.sidebar.title("📊 Financial Insights")
st.sidebar.markdown("---")

if not df.empty:
    quarters = df["Quarter"].tolist()
    selected_quarter = st.sidebar.selectbox("Select Quarter", quarters, index=len(quarters)-1)
    
    selected_data = data_map[selected_quarter]
else:
    st.sidebar.warning("No analysis files found.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.info("Select a quarter to view detailed insights and how they compare to trends.")

# -----------------------------------------------------------------------------
# Main Content
# -----------------------------------------------------------------------------

st.title(f"NVIDIA Earnings Call Insights ({selected_quarter} 2025)")

# Top Metrics Row
col1, col2, col3 = st.columns(3)

def get_delta_color(val):
    return "normal" if val == 0 else ("inverse" if val < 0 else "normal") 

with col1:
    sentiment = selected_data.get("Management Sentiment", "Neutral")
    st.metric(
        label="Management Sentiment",
        value=sentiment,
        delta=None, # Could compute delta if we had previous quarter logic easily tailored
        delta_color="off"
    )

with col2:
    sentiment = selected_data.get("Q&A Sentiment", "Neutral")
    st.metric(
        label="Analyst Q&A Sentiment",
        value=sentiment
    )

with col3:
    tone = selected_data.get("Quarter-over-Quarter Tone Change", "Neutral")
    st.metric(
        label="Tone Shift",
        value=tone
    )

st.divider()

# Two-column layout for Details and Charts
c_left, c_right = st.columns([1, 2])

with c_left:
    st.subheader("💡 Strategic Focuses")
    focuses = selected_data.get("Strategic Focuses", [])
    if focuses:
        for i, focus in enumerate(focuses, 1):
            st.info(f"**{i}.** {focus}")
    else:
        st.write("No strategic focuses extracted.")

with c_right:
    st.subheader("📈 Sentiment Trends")
    
    # Plotly Line Chart
    if not df.empty:
        fig = px.line(
            df, 
            x="Quarter", 
            y=["Mgmt Score", "Q&A Score"],
            markers=True,
            title="Sentiment Score Over Time (1=Pos, 0=Neu, -1=Neg)",
            labels={"value": "Sentiment Score", "variable": "Metric"},
            color_discrete_map={"Mgmt Score": "#00CC96", "Q&A Score": "#EF553B"}
        )
        fig.update_yaxes(range=[-1.5, 1.5], tickvals=[-1, 0, 1], ticktext=["Negative", "Neutral", "Positive"])
        fig.update_layout(
            hovermode="x unified",
            xaxis_title=None,
            legend_title=None,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

# Raw Data Expander
with st.expander("View Analysis Raw Data"):
    st.json(selected_data)
