import streamlit as st
import pandas as pd
from chatbot import Chatbot

st.set_page_config(page_title="ShadowBot AI", layout="wide")
st.title("🤖 ShadowBot AI Chat")

st.markdown("Upload a CSV file and ask any tech-related or data-related question.")

# Upload CSV
uploaded_file = st.file_uploader("📄 Upload CSV", type=["csv"])

# Instantiate chatbot
if uploaded_file:
    chatbot = Chatbot(csv_path=uploaded_file)
else:
    chatbot = Chatbot()

# Text input
query = st.text_input("💬 Ask me anything:")

# Optional checkboxes
col1, col2 = st.columns(2)
with col1:
    tech_news = st.checkbox("📰 Ask for Tech News")
with col2:
    search_summary = st.checkbox("🔍 Ask for Web Summary")

# Ask button
if st.button("Ask ShadowBot"):
    if query:
        with st.spinner("Thinking..."):
            response = chatbot.process_query(query, tech_news=tech_news, search_summary=search_summary)

            # Display response
            if isinstance(response, str):
                st.markdown("### 🧠 Response:")
                st.write(response)
            elif isinstance(response, list):
                st.markdown("### 📊 Matching Rows:")
                st.dataframe(pd.DataFrame(response))
            else:
                st.warning("🤷 Unexpected response format.")
    else:
        st.warning("Please enter a query.")
