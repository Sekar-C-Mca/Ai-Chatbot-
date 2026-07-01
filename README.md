# AI Chatbot

A simple Streamlit chatbot built with LangChain and Gemini.

The app lets the user enter their own Gemini API key in the sidebar, then chat with the model in a clean chat interface. It also supports PDF upload. The PDF is converted into markdown first and then used as context for the chat, so the app follows a basic RAG style workflow instead of sending a raw PDF directly to the model.

## Features

- Streamlit chat UI
- Gemini through LangChain
- Session-based chat memory
- LangChain message history
- PDF upload support
- PDF to markdown conversion
- Basic RAG-style context retrieval from uploaded PDF content
- Simple error handling for missing API key and Gemini API failures

## How The RAG Flow Works

1. Upload a PDF from the sidebar.
2. The app extracts readable text from the PDF.
3. The extracted text is converted into markdown.
4. The markdown is stored in Streamlit session state.
5. When the user asks a question, the PDF markdown is added as context for Gemini.
6. Gemini answers using both the chat history and the uploaded PDF context.

This is a lightweight retrieval flow for a small chatbot. It keeps things simple and helps reduce token usage by sending cleaned markdown text instead of the original PDF file.

## Tech Stack

- Streamlit
- LangChain
- Gemini API
- pypdf

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Gemini API Key

The app asks for the Gemini API key in the sidebar. You can create a free Gemini API key from Google AI Studio.

The key is not stored permanently by the app. It is only used during the current Streamlit session.

## Deploy On Streamlit

1. Push this project to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app.
4. Select this GitHub repository.
5. Set the main file path to:

```text
app.py
```

6. Deploy the app.

## Notes

This project is meant to be simple and easy to understand. For larger PDFs or production-level RAG, the next step would be to split the markdown into chunks, create embeddings, store them in a vector database, and retrieve only the most relevant chunks for each question.
