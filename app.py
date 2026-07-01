from io import BytesIO

import streamlit as st
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pypdf import PdfReader


st.set_page_config(page_title="Gemini Chatbot", page_icon=None)

MAX_PDF_MARKDOWN_CHARS = 20000


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


def clean_pdf_line(line: str) -> str:
    return " ".join(line.strip().split())


def looks_like_heading(line: str) -> bool:
    if len(line) > 80 or line.endswith((".", ",", ";", ":")):
        return False
    return line.isupper() or line.istitle()


def pdf_to_markdown(pdf_file) -> str:
    reader = PdfReader(BytesIO(pdf_file.getvalue()))
    markdown_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        lines = []

        for raw_line in page_text.splitlines():
            line = clean_pdf_line(raw_line)
            if not line:
                continue
            if looks_like_heading(line):
                lines.append(f"### {line}")
            else:
                lines.append(line)

        if lines:
            markdown_pages.append(f"## Page {page_number}\n\n" + "\n\n".join(lines))

    markdown = "\n\n".join(markdown_pages).strip()
    if not markdown:
        raise ValueError("No readable text was found in this PDF.")

    if len(markdown) > MAX_PDF_MARKDOWN_CHARS:
        markdown = (
            markdown[:MAX_PDF_MARKDOWN_CHARS]
            + "\n\n[PDF content was shortened to reduce token usage.]"
        )

    return markdown


def get_pdf_context_message() -> SystemMessage | None:
    pdf_markdown = st.session_state.get("pdf_markdown", "")
    if not pdf_markdown:
        return None

    return SystemMessage(
        content=(
            "Use the following PDF content as reference when it is relevant. "
            "The PDF has already been converted to markdown to reduce token usage. "
            "If the answer is not in the PDF, say that clearly.\n\n"
            f"{pdf_markdown}"
        )
    )


def get_response(api_key: str, prompt: str) -> str:
    chat_history = get_chat_history()
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key,
        temperature=0.7,
        max_retries=2,
    )

    chat_history.add_user_message(prompt)

    messages = chat_history.messages
    pdf_context_message = get_pdf_context_message()
    if pdf_context_message:
        messages = [pdf_context_message, *messages]

    response = model.invoke(messages)
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

    uploaded_pdf = st.file_uploader("PDF context", type=["pdf"])
    if uploaded_pdf:
        uploaded_pdf_id = f"{uploaded_pdf.name}:{uploaded_pdf.size}"
        if st.session_state.get("uploaded_pdf_id") != uploaded_pdf_id:
            try:
                st.session_state.pdf_markdown = pdf_to_markdown(uploaded_pdf)
                st.session_state.uploaded_pdf_id = uploaded_pdf_id
                st.success("PDF converted to markdown.")
            except Exception as error:
                st.session_state.pdf_markdown = ""
                st.session_state.uploaded_pdf_id = ""
                st.error("Could not read this PDF.")
                st.caption(str(error))

    if st.session_state.get("pdf_markdown"):
        with st.expander("PDF markdown preview"):
            st.markdown(st.session_state.pdf_markdown[:4000])
            if len(st.session_state.pdf_markdown) > 4000:
                st.caption("Preview shortened.")

    if st.button("Clear chat"):
        st.session_state.chat_history = InMemoryChatMessageHistory()
        st.rerun()

    if st.button("Remove PDF"):
        st.session_state.pdf_markdown = ""
        st.session_state.uploaded_pdf_id = ""
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
