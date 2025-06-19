import streamlit as st
from chatbot import OllamaChatbot  # Adjust if using a different file/class
import pandas as pd

st.set_page_config(page_title="ShadowBot", layout="wide")
st.title("🤖 ShadowBot - Tech News & CSV Assistant")

# Initialize the chatbot
if "chatbot" not in st.session_state:
    st.session_state.chatbot = OllamaChatbot()

# User input
user_input = st.text_input("You:", "")

# Display response
if user_input:
    with st.spinner("ShadowBot is thinking..."):
        response = "".join(st.session_state.chatbot.get_response(user_input))
        st.markdown(response)

# CSV file uploader for future use
st.markdown("### 📂 Upload CSV for Analysis")
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])
if csv_file is not None:
    try:
        df = pd.read_csv(csv_file)
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Error loading CSV: {e}")