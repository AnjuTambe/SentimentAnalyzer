# Earnings Call Sentiment Analyzer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_LIVE_APP_URL_HERE)

This project analyzes earnings call transcripts to extract sentiment and strategic insights, and visualizes the results in a dashboard.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Key**:
    - Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        ```
    - Open `.env` and paste your OpenAI API Key:
        ```
        OPENAI_API_KEY=sk-...
        ```

## Running the Project

### 1. Analyze Transcripts
To process the transcripts in `data/scripts` and generate JSON analysis in `data/analysis`:

```bash
python3 data/scripts/analyze_transcripts.py
```

### 2. View Dashboard
To launch the interactive dashboard:

```bash
python3 -m streamlit run app/dashboard.py
```
