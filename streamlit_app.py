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
    ("Custom Question", ""),
    ("Compile relevant quotes", """You are tasked with analyzing transcript data from 20 respondents and compiling a list of relevant quotes that relate to a specific research question. Your goal is to extract meaningful insights from the data and present them in a clear, organized manner.

        First, carefully read and understand the research question.

        Now, you will analyze the data.

        As you go through the transcript data, follow these steps:

        1. Identify quotes that are directly related to the research question.
        2. For each relevant quote, note the name of the respondent and a brief summary of who they are (if provided).
        3. Determine how the quote relates to the research question.

        Format your output using Markdown as follows:

        ```markdown
        ## [Name of Respondent] (brief summary of who they are)

        > "[Quote]"

        *Relation to research question:* [Brief explanation of how the quote relates to the research question]
        ```

        Important guidelines:
        - Ensure that each quote you select is directly relevant to the research question.
        - Be concise in your explanations of how the quote relates to the research question.
        - If multiple quotes from the same respondent are relevant, you may include them under the same respondent heading.
        - Aim for clarity and readability in your output.

        Remember to process all 20 respondents, even if some may not have relevant quotes. In such cases, you can simply omit that respondent from your output.

        Begin your analysis now, and present your findings in the format specified above."""),
    ("Main Points", "What are the main points discussed in the data?"),
    ("Key Stakeholders", "Who are the key stakeholders mentioned and what are their roles?")
]

# Selectbox for choosing a prompt
selected_prompt = st.selectbox(
    "Choose a prompt or select 'Custom Question' to enter your own",
    options=[prompt[0] for prompt in default_prompts],
    index=0,
    key="prompt_select"
)

# Custom prompt text area
custom_question = st.text_area(
    "Please add your research question",
    placeholder="Type your research question here",
    height=150,
    disabled=selected_prompt != "Custom Question" or not uploaded_file,
)

# Set the question based on selection
if selected_prompt == "Custom Question":
    question = custom_question
else:
    question = next(prompt[1] for prompt in default_prompts if prompt[0] == selected_prompt)

# Display the selected question
st.text_area("Selected Question", value=question, height=150, disabled=True)

# Button to trigger LLM request
trigger_llm = st.button("Generate Answer", disabled=not (uploaded_file and question and api_key))

if trigger_llm:
    research_data = uploaded_file
    
    try:
        client = anthropic.Client(api_key=api_key)
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": f"Here's research data:\n\n{research_data}\n\n{question}"}
            ]
        )
        
        st.write("### Answer")
        st.write(message.content[0].text)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your API key and try again.")

if uploaded_file and question and not api_key:
    st.info("Please enter your Anthropic API key in the sidebar to continue.")

if uploaded_file and question and api_key:
    research_data = uploaded_file
    
    try:
        client = anthropic.Client(api_key=api_key)
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": f"Here's research data:\n\n{research_data}\n\n{question}"}
            ]
        )
        
        st.write("### Answer")
        st.write(message.content[0].text)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your API key and try again.")