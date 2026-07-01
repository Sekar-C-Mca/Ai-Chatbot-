# AI Chatbot

A simple Streamlit chatbot built with Streamlit, LangChain, and Gemini.

Live Application: https://chatbotgeminipdf.streamlit.app/

The app lets the user enter their own Gemini API key in the sidebar, then chat with the model in a clean chat interface. It also supports PDF upload for a small RAG workflow. When a PDF is uploaded, the app extracts the readable text, converts it into markdown, and sends that markdown as context to the model. This avoids sending the raw PDF file and helps save tokens.

## Features

- Streamlit chat UI
- Gemini through LangChain
- Session-based chat memory
- LangChain message history
- PDF upload support
- PDF to markdown conversion
- Basic RAG and retrieval-style context from uploaded PDF content
- Simple error handling for missing API key and Gemini API failures

## How The RAG Flow Works

1. Upload a PDF from the sidebar.
2. The app extracts readable text from the PDF.
3. The extracted text is converted into markdown.
4. The markdown is stored in Streamlit session state.
5. When the user asks a question, the PDF markdown is sent to Gemini as context.
6. Gemini answers using both the chat history and the uploaded PDF context.

This is a lightweight retrieval flow for a small chatbot. The main idea is simple: clean the PDF into markdown first, then send only that markdown context to the model. That makes the prompt easier for the model to read and helps reduce token usage compared with passing the full PDF directly.

## Screenshots

Add screenshots here after running the app.

<img width="1917" height="954" alt="Screenshot From 2026-07-01 15-54-32" src="https://github.com/user-attachments/assets/f9c6e56c-7f21-4fd6-9667-fd49d58a8600" />
<img width="1917" height="954" alt="Screenshot From 2026-07-01 15-54-43" src="https://github.com/user-attachments/assets/cca44b71-d07d-4b0b-a7dd-d34b694fb0b2" />
<img width="1917" height="954" alt="Screenshot From 2026-07-01 15-55-10" src="https://github.com/user-attachments/assets/181ef552-224f-43cf-b146-989cf7c6b4aa" />


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
