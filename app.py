import streamlit as st
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


st.set_page_config(page_title="Gemini Chatbot", page_icon=None)


def message_text(content) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            else:
                text_parts.append(str(block))
        return "\n".join(text_parts)

    return str(content)


def get_chat_history() -> InMemoryChatMessageHistory:
    """Keep LangChain chat history in Streamlit session state."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = InMemoryChatMessageHistory()
    return st.session_state.chat_history


def get_response(api_key: str, prompt: str) -> str:
    chat_history = get_chat_history()
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key,
        temperature=0.7,
        max_retries=2,
    )

    chat_history.add_user_message(prompt)
    response = model.invoke(chat_history.messages)
    answer = message_text(response.content)
    chat_history.add_ai_message(answer)

    return answer


st.title("Gemini Chatbot")

with st.sidebar:
    st.header("Settings")
    gemini_api_key = st.text_input(
        "Gemini API key",
        type="password",
        help="Create a free key in Google AI Studio.",
    )

    if st.button("Clear chat"):
        st.session_state.chat_history = InMemoryChatMessageHistory()
        st.rerun()

if not gemini_api_key:
    st.info("Enter your Gemini API key in the sidebar to start chatting.")
    st.stop()

chat_history = get_chat_history()

for message in chat_history.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

user_prompt = st.chat_input("Ask something")

if user_prompt:
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        previous_message_count = len(chat_history.messages)
        try:
            with st.spinner("Thinking..."):
                answer = get_response(gemini_api_key, user_prompt)
            st.markdown(answer)
        except Exception as error:
            del chat_history.messages[previous_message_count:]
            st.error(
                "Gemini could not return a response. "
                "Please check your API key, quota, and network connection."
            )
            st.caption(str(error))
