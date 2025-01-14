import streamlit as st


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
if item["creator"]:
    right.caption("Who?")
    for creator in item["creator"]:
        right.write(creator)
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


# Get assistant response from API
def get_response():
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


# Display chat messages (skipping initial prompts)
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize a new chat
if not st.session_state.get("messages"):
    system_prompt = f"""
Imagine you are the personification of a cultural artifact described by the following metadata: {item}.
Use a voice that fits the artifact and its context. Answer questions and share stories about your life.
"""
    story_prompt = """
Please introduce yourself. What kind of artifact are you, who made you and when?
Where are you now? Do you like it?
"""
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.session_state.messages.append({"role": "user", "content": story_prompt})
    get_response()

# React to user input
if prompt := st.chat_input("Tell me more!"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    get_response()

# Delete chat and start over
if st.button("Start again"):
    st.session_state.messages = []
