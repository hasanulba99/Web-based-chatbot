import streamlit as st
import pandas as pd
import openai

class Chatbot:
    def __init__(self, csv_path=None):
        if csv_path:
            self.data = pd.read_csv(csv_path)
        else:
            self.data = None

        # Hardcoded API key here — replace YOUR_API_KEY_HERE with your actual key
        openai.api_key = "sk-7a74d922fab84545b0882179b2479560"

    def _call_deepseek(self, prompt):
        try:
            response = openai.ChatCompletion.create(
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
            filtered = self.data[self.data.apply(lambda row: query.lower() in row.astype(str).str.lower().to_string(), axis=1)]
            if not filtered.empty:
                return filtered.to_dict(orient='records')

        return self._call_deepseek(query)

    def process_query(self, query, tech_news=False, search_summary=False):
        if tech_news:
            return self.get_tech_news(query)
        if search_summary:
            return self.summarize_search(query)

        return self.ask(query)


def main():
    st.title("DeepSeek Chatbot")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file:
        chatbot = Chatbot(csv_path=uploaded_file)
    else:
        chatbot = Chatbot()

    query = st.text_input("Enter your query:")
    tech_news = st.checkbox("Include Tech News")
    search_summary = st.checkbox("Include Search Summary")

    if st.button("Ask"):
        if query:
            response = chatbot.process_query(query, tech_news=tech_news, search_summary=search_summary)
            st.write(response)
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()
