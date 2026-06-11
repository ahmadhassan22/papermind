import streamlit as st
import requests

st.title("RAG Document Q&A")

# Upload
uploaded_file = st.file_uploader("Upload PDF")

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    requests.post("http://127.0.0.1:8000/upload", files=files)
    st.success("Uploaded!")

# Query
query = st.text_input("Ask a question")

if st.button("Ask"):
    response = requests.post(
        "http://127.0.0.1:8000/query",
        json={"question": query}
    )
    st.write(response.json()["answer"])