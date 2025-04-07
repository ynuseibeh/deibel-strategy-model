# 🧠 Deibel Strategy Model Automation

A decision intelligence assistant that automates the Deibel model for strategic planning using GPT-4, real-time data, and an interactive Streamlit UI.

## 🚀 Features
- Extracts strategic ends, means, and risks using GPT-4
- Suggests optimal strategy paths with risk and utility scoring
- Integrates real-time news via NewsAPI
- Web UI via Streamlit or CLI fallback

## 🔧 Setup

1. Clone this repo
2. Create a `.env` file using `.env.example`
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the app:
    ```bash
    streamlit run app.py
    ```

## 🔒 Environment Variables
- `OPENAI_API_KEY` – Your OpenAI GPT API key
- `NEWS_API_KEY` – NewsAPI key for real-time headlines
- `USE_STREAMLIT` – Set to `1` to run the web app

## 📦 Structure
- `app.py`: Main app logic
- `.env.example`: Environment template

## 📄 License
MIT License
