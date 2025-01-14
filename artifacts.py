import streamlit as st
import requests
import utils

# Europeana API key and base URL
API_KEY = st.secrets.get("EUROPEANA_API_KEY")
BASE_URL = "https://api.europeana.eu/record/v2/search.json"


# Prepare the Streamlit session state
if "europeana" not in st.session_state:
    session = requests.session()
    session.headers.update({"X-Api-Key": API_KEY})
    st.session_state["europeana"] = session
if "cursor" not in st.session_state:
    st.session_state["cursor"] = "*"
if "total_results" not in st.session_state:
    st.session_state["total_results"] = 0
if "results" not in st.session_state:
    st.session_state["results"] = []
if "current_item" not in st.session_state:
    st.session_state["current_item"] = None


# Reset the search results in the streamlit session
def reset_results():
    st.session_state.cursor = "*"
    st.session_state.results = []
    st.session_state.total_results = 0


# Search form
search_query = st.text_input(
    "Search in the Europeana Database",
    on_change=reset_results,
    key="search_query",
)
# Restrict available museums
options = [
    "Fine Arts Museum Vienna",
    "Vienna Museum",
    "World Museum Vienna",
]
if "search_providers" not in st.session_state:
    st.session_state["search_providers"] = options
providers = st.pills(
    "Collections",
    options,
    selection_mode="multi",
    on_change=reset_results,
    key="search_providers",
)
providers_str = " OR ".join([f'"{provider}"' for provider in providers])


# Get results from the Europeana API
def query_api():
    # Search parameters
    params = [
        ("query", search_query),
        ("rows", 12),
        ("cursor", st.session_state["cursor"]),
        ("profile", "portal"),
        ("lang", "en"),
        ("qf", "TYPE:IMAGE"),
        ("qf", f"DATA_PROVIDER:{providers_str}"),
        ("reusability", "open OR restricted"),
    ]

    # Make the API call
    response = st.session_state.europeana.get(BASE_URL, params=params)
    data = response.json()
    st.session_state.total_results = data.get("totalResults", 0)
    st.session_state.results += data.get("items", [])
    st.session_state.cursor = data.get("nextCursor")
    if st.session_state.total_results <= data.get("itemsCount", 12):
        # Europeana should not return nextCursor if there are no more results
        # but on the first page it does. This is a workaround.
        st.session_state.cursor = None
    return data


# Display search results
@st.fragment
def list_items(num_columns=4):
    columns = st.columns(num_columns)

    for idx, item in enumerate(st.session_state["results"]):
        item = utils.clean_data(item)
        title = item["title"][0]
        provider = item["provider"][0]
        preview = item["preview"][0]

        with columns[idx % num_columns]:
            st.image(preview)
            st.write(f"#### {title}")
            st.write(provider)
            if st.button("Pick me", key=f"pick_{idx}"):
                st.session_state.current_item = item
                st.session_state.messages = []
                st.switch_page("chat.py")

    if st.session_state.cursor:
        st.button("Load more", on_click=query_api)


# Process the results
if search_query:
    if st.session_state.total_results == 0:
        query_api()
    total_results = st.session_state.total_results
    if total_results == 0:
        st.warning("No items found.")
    else:
        st.info(
            "1 item found." if total_results == 1 else f"{total_results} items found."
        )
        st.header("Choose an artifact")
        list_items()
