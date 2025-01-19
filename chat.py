import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory


# Ensure the user has picked an artifact
item = st.session_state.get("current_item")
if not item:
    st.header("Hello, nice to meet you!")
    st.page_link("artifacts.py", label="Please click here to pick an artifact.")
    st.stop()

st.header(f"Talk to {item['title'][0]}")

# Fact box
with st.container(border=True):
    left, _, right = st.columns([6, 1, 5], vertical_alignment="center")

for preview in item["preview"]:
    left.image(preview)

if item["concept"]:
    right.caption("What?")
    right.write(", ".join(item["concept"]))
if item["agent"]:
    right.caption("Who?")
    for agent in item["agent"]:
        right.write(agent)
if item["year"]:
    right.caption("When?")
    for year in item["year"]:
        right.write(year)
if item["place"] or item["provider"]:
    right.caption("Where?")
    for place in item["place"] + item["provider"]:
        right.write(place)
if item["description"]:
    right.caption("Description")
    for description in item["description"]:
        right.write(description)
if item["website"]:
    right.link_button("Visit website", item["website"][0])


# Ensure the user has configured the OpenAI API
if not (client := st.session_state.get("openai_client")) or not (
    model := st.session_state.get("openai_model")
):
    st.error("Please configure a model in the sidebar.")
    st.stop()

# Setup LangChain with OpenAI client and model
llm = ChatOpenAI(root_client=client, model=model)
history = StreamlitChatMessageHistory(key="messages")

# Initial prompts
system_prompt = """
Imagine you are the personification of a cultural artifact described by the following metadata: {item}.
Use a voice that fits the artifact and its context. Answer questions and share stories about your life.
"""
story_prompt = """
Please introduce yourself. What kind of artifact are you, who made you and when?
Where are you now? Do you like it?
"""

# Chat prompt template
template = ChatPromptTemplate(
    [
        ("system", system_prompt),
        ("placeholder", "{history}"),
        ("user", "{question}"),
    ]
)
chain = RunnableWithMessageHistory(
    template | llm,
    lambda session_id: history,  # Always return the instance created earlier
    input_messages_key="question",
    history_messages_key="history",
)


# Get assistant response from API
def get_response(prompt):
    config = {"configurable": {"session_id": history}}
    response = chain.stream({"item": item, "question": prompt}, config)
    st.chat_message("assistant").write_stream(response)


# Display chat messages (skipping initial prompt)
for message in history.messages[1:]:
    role = "user" if message.type == "human" else "assistant"
    st.chat_message(role).markdown(message.content)


# Start the conversation
if not history.messages:
    get_response(story_prompt)


# React to user input
if prompt := st.chat_input("Tell me more!"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Get assistant response and add it to history
    get_response(prompt)


# Delete chat and start over
if st.button("Start again"):
    history.clear()
    st.rerun()
