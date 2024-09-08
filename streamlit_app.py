import streamlit as st
import anthropic

with st.sidebar:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("📝 File Q&A with Anthropic Claude 3.5 Sonnet")

uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))

question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not api_key:
    st.info("Please add your Anthropic API key to continue.")

if uploaded_file and question and api_key:
    article = uploaded_file.read().decode()
    
    client = anthropic.Client(api_key=api_key)
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Here's an article:\n\n{article}\n\n{question}"}
        ]
    )
    
    st.write("### Answer")
    st.write(message.content[0].text)