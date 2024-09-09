import streamlit as st
import anthropic

st.title("📝 File Q&A with Anthropic Claude 3.5 Sonnet")

# Try to get the API key from secrets, otherwise use an input field
api_key = st.secrets["ANTHROPIC_API_KEY"]
if not api_key:
    st.error("Anthropic API key not found in secrets. Please add it to continue.")

# Sidebar content removed

import os

# Directory containing the text files
data_dir = "data"

# Read and merge all text files in the data directory
uploaded_file = ""
for filename in os.listdir(data_dir):
    if filename.endswith((".txt", ".md")):
        file_path = os.path.join(data_dir, filename)
        with open(file_path, 'r') as file:
            uploaded_file += file.read() + "\n\n"

# Remove trailing newlines
uploaded_file = uploaded_file.rstrip()

# Default prompts
default_prompts = [
    "Can you give me a short summary?",
    "What are the main points discussed in the article?",
    "Who are the key people mentioned and what are their roles?"
]

# Buttons for default prompts
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(default_prompts[0]):
        question = default_prompts[0]
with col2:
    if st.button(default_prompts[1]):
        question = default_prompts[1]
with col3:
    if st.button(default_prompts[2]):
        question = default_prompts[2]

# Custom prompt text area
custom_question = st.text_area(
    "Or ask a custom question about the article",
    placeholder="Type your custom question here",
    height=150,
    disabled=not uploaded_file,
)

# Use custom question if provided, otherwise use the selected default prompt
question = custom_question if custom_question else (question if 'question' in locals() else "")

if uploaded_file and question and not api_key:
    st.info("Please enter your Anthropic API key in the sidebar to continue.")

if uploaded_file and question and api_key:
    article = uploaded_file
    
    try:
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
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your API key and try again.")