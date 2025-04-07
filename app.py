# Full Python Implementation: Deibel Strategy Model Automation

from dataclasses import dataclass, field
from typing import List, Dict
import uuid
import random
import requests
import streamlit as st
import openai
import os

# --- Configuration ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# 1. Define Strategic Elements
@dataclass
class StrategicElement:
    id: str
    name: str
    type: str  # 'End', 'Means', 'Way', 'Context', 'Risk'
    metadata: Dict


# 2. GPT-based Extraction

def extract_elements_from_text(text: str) -> List[StrategicElement]:
    prompt = f"""
    Extract strategic elements from the following text.
    Classify each as one of the following: End, Means, Way, Context, Risk.
    Return in JSON format: [{{'name': ..., 'type': ..., 'metadata': {{}}}}]

    Text:
    {text}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    raw_elements = eval(response.choices[0].message['content'])
    elements = []
    for el in raw_elements:
        elements.append(StrategicElement(
            id=str(uuid.uuid4()),
            name=el['name'],
            type=el['type'],
            metadata=el.get('metadata', {})
        ))
    return elements


# 3. Strategy Path Definition
@dataclass
class StrategyPath:
    end: StrategicElement
    means: StrategicElement
    way: str
    risk_score: float
    utility_score: float


# 4. Generate Strategic Paths
def generate_strategic_paths(ends: List[StrategicElement], means_list: List[StrategicElement]) -> List[StrategyPath]:
    paths = []
    for end in ends:
        for means in means_list:
            way = f"Apply '{means.name}' to achieve '{end.name}'"
            risk_score = round(random.uniform(0.1, 0.5), 2)
            utility_score = round(random.uniform(0.6, 0.95), 2)
            path = StrategyPath(end, means, way, risk_score, utility_score)
            paths.append(path)
    return paths


# 5. Rank Strategies
def rank_strategies(paths: List[StrategyPath]) -> List[StrategyPath]:
    return sorted(paths, key=lambda p: p.utility_score - p.risk_score, reverse=True)


# 6. Fetch Real-time News (Placeholder using NewsAPI)
def fetch_news(query: str) -> str:
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return "\n".join([article["title"] + ". " + article["description"] for article in articles[:3]])
    return ""


# 7. Streamlit UI

def run_app():
    st.title("🧠 Deibel Strategic Intelligence Assistant")

    user_input = st.text_area("Enter strategy-related input or policy goal:",
                              "Achieve carbon neutrality by 2040. Increase renewable energy funding.")

    if st.button("Analyze Strategy"):
        with st.spinner("Extracting strategic elements using GPT..."):
            elements = extract_elements_from_text(user_input)

        ends = [e for e in elements if e.type == "End"]
        means = [e for e in elements if e.type == "Means"]

        if not ends or not means:
            st.warning("Insufficient elements extracted. Please refine input.")
            return

        paths = generate_strategic_paths(ends, means)
        ranked_paths = rank_strategies(paths)

        st.subheader("Top Strategic Recommendations")
        for i, path in enumerate(ranked_paths, start=1):
            st.markdown(f"**{i}. {path.way}**")
            st.markdown(f"- Utility Score: `{path.utility_score}`  ")
            st.markdown(f"- Risk Score: `{path.risk_score}`")

        st.subheader("📰 Related Real-Time News")
        news_summary = fetch_news("carbon neutrality")
        st.text_area("Relevant Headlines:", news_summary, height=200)


# 8. CLI Fallback

def main():
    print("Running CLI version...")
    text_input = "Achieve carbon neutrality by 2040. Increase renewable energy funding."
    elements = extract_elements_from_text(text_input)
    ends = [e for e in elements if e.type == "End"]
    means = [e for e in elements if e.type == "Means"]

    paths = generate_strategic_paths(ends, means)
    ranked_paths = rank_strategies(paths)

    print("\nTop Strategic Recommendations:\n")
    for i, path in enumerate(ranked_paths, start=1):
        print(f"{i}. {path.way}")
        print(f"   Utility Score: {path.utility_score}, Risk Score: {path.risk_score}\n")


if __name__ == "__main__":
    if os.getenv("USE_STREAMLIT"):
        run_app()
    else:
        main()
