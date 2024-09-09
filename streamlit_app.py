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

# Base prompts
base_prompts = [
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
    ("Main Points", "Analyze the provided research data and identify the main points discussed. Your response should:"),
    ("Key Stakeholders", "Review the research data and identify the key stakeholders mentioned. For each stakeholder:")
]

# Selectbox for choosing a base prompt
selected_base_prompt = st.selectbox(
    "Choose a base prompt",
    options=[prompt[0] for prompt in base_prompts],
    index=0,
    key="base_prompt_select"
)

# Research question input field
research_question = st.text_area(
    "Enter your research question",
    placeholder="Type your research question here",
    height=100,
    disabled=not uploaded_file,
)

# Combine base prompt and research question
selected_base_prompt_text = next(prompt[1] for prompt in base_prompts if prompt[0] == selected_base_prompt)
combined_prompt = f"{selected_base_prompt_text}\n\nResearch Question: {research_question}"

# Display the combined prompt
st.text_area("Combined Prompt", value=combined_prompt, height=200, disabled=True)

# Submit button to trigger LLM request
submit_button = st.button("Submit", disabled=not (uploaded_file and research_question and api_key))

if submit_button:
    research_data = uploaded_file
    
    try:
        client = anthropic.Client(api_key=api_key)
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": f"Here's the research data:\n\n{research_data}\n\n{combined_prompt}"}
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