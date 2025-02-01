import os
import streamlit as st
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Wood Chat", layout="wide")
st.write("---")
st.title("Chat With Woods")
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

system_message = {
    "role": "system",
    "content": (
        "You are a helpful assistant that only answers questions related to furniture. "
        "If a user asks about anything other than furniture, respond with: "
        "'Sorry I will only answer regarding furnitures. Ask me about that.'"
    )
}

if not st.session_state.messages:
    st.session_state.messages.append(system_message)

chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Response:** {message['content']}")
            st.write("---")

with st.container():
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message here...", key="chat_input")
        submitted = st.form_submit_button("Send")

if submitted:
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"Error: {str(e)}"

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
