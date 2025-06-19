import streamlit as st
import pandas as pd
import openai

# ✅ Your DeepSeek API key directly in code (NOT RECOMMENDED for production)
DEEPSEEK_API_KEY = "sk-7a74d922fab84545b0882179b2479560"

class Chatbot:
    def __init__(self, csv_path=None):
        self.data = pd.read_csv(csv_path) if csv_path else None
        self.client = openai.OpenAI(api_key=DEEPSEEK_API_KEY)

    def _call_deepseek(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="deepseek-coder",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️ Error calling DeepSeek API: {e}"

    def get_tech_news(self, query):
        prompt = f"Provide latest tech news summary about: {query}"
        return self._call_deepseek(prompt)

    def summarize_search(self, query):
        prompt = f"Summarize web search results for: {query}"
        return self._call_deepseek(prompt)

    def ask(self, query):
        if self.data is not None:
            filtered = self.data[
                self.data.apply(lambda row: query.lower() in row.astype(str).str.lower().to_string(), axis=1)
            ]
            if not filtered.empty:
                return filtered.to_dict(orient='records')

        return self._call_deepseek(query)

    def process_query(self, query, tech_news=False, search_summary=False):
        if tech_news:
            return self.get_tech_news(query)
        if search_summary:
            return self.summarize_search(query)
        return self.ask(query)
