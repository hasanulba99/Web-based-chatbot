import streamlit as st
import pandas as pd
from deepseek import DeepSeek

class Chatbot:
    def __init__(self, csv_path=None):
        if csv_path:
            self.data = pd.read_csv(csv_path)
        else:
            self.data = None
        self.deepseek = DeepSeek()

    def process_query(self, query, tech_news=False, search_summary=False):
        if tech_news:
            # Placeholder: Implement logic to fetch tech news related to query
            news = self.deepseek.get_tech_news(query)
            return news
        if search_summary:
            # Placeholder: Implement logic to summarize search results
            summary = self.deepseek.summarize_search(query)
            return summary
        if self.data is not None:
            # Search in CSV data
            filtered = self.data[self.data.apply(lambda row: query.lower() in row.astype(str).str.lower().to_string(), axis=1)]
            if not filtered.empty:
                return filtered.to_dict(orient='records')
        # Default: Use DeepSeek to answer query
        answer = self.deepseek.ask(query)
        return answer

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
