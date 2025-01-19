import streamlit as st
from openai import OpenAI

# Pages
search_page = st.Page("artifacts.py", title="Search")
chat_page = st.Page("chat.py", title="Chat")

pg = st.navigation([search_page, chat_page], position="hidden")
layout = "wide" if pg._url_path == "artifacts" else "centered"
st.set_page_config(layout=layout, initial_sidebar_state="expanded")

st.title("Meet voices from the past")
st.markdown(
    "Explore cultural artifacts by having them tell their own stories using "
    "AI. Simply search for an object to discover its journey through history "
    "and even engage in a conversation where facts blend with imagination."
)

# Sidebar
st.sidebar.title("Settings")
ai_api_url = st.sidebar.text_input(
    "OpenAI API compatible base URL",
    st.secrets.get("OPENAI_BASE_URL"),
)
ai_api_key = st.sidebar.text_input(
    "API Key",
    st.secrets.get("OPENAI_API_KEY"),
    type="password",
)

# Initialize OpenAI client
if ai_api_url and ai_api_key:
    client = OpenAI(base_url=ai_api_url, api_key=ai_api_key)
    st.session_state["openai_client"] = client
    models = [model.id for model in client.models.list().data]
    st.sidebar.selectbox("Select a model", models, key="openai_model")

# Disclaimer
st.sidebar.markdown(
    "This application uses AI to blend factual information with creative "
    "storytelling. Responses may not be accurate."
)

# Keep search form values when switching pages
if "search_query" in st.session_state:
    st.session_state.search_query = st.session_state.search_query
if "search_providers" in st.session_state:
    st.session_state.search_providers = st.session_state.search_providers

# Load page
pg.run()
