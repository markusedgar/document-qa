import streamlit as st
from openai import OpenAI

st.title("📝 Analyse your research data")

# Try to get the API key from secrets, otherwise use an input field
api_key = st.secrets["OPENAI_API_KEY"]
if not api_key:
    st.error("OpenAI API key not found in secrets. Please add it to continue.")

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
    ("Compile relevant quotes", """You are tasked with analyzing transcript data from 20 respondents to compile a list of relevant quotes that address a specific research question or relate to a given theme. Your objective is to extract and present key insights from the data in an organized, easy-to-read format.

        Instructions:
        Understand the Research Question or Research Theme: Start by thoroughly reading and comprehending the research question or theme.
        Analyze the Transcript Data: Go through the transcript data to identify quotes relevant to the research question or theme.
        
        Steps:
        Extract Quotes: Identify quotes from the transcripts that are directly related to the research question or theme.
        Respondent Identification: For each quote, note the respondent's name and provide a brief summary of who they are (if available).
        Quote Relevance: Briefly explain how each quote relates to the research question or theme.
        
        Formatting:
        Use the following format for your output:

        ```txt
        Respondent Name (brief description)

        "[Quote]"

        Relation to research question: [Concise explanation of how the quote connects to the research question]
        
        ----------------------------------------
        
        ```
        Additional Guidelines:
        Make sure to only include quotes that are directly related to the research question or theme.
        Keep explanations clear and to the point.
        If a respondent has multiple relevant quotes, group them under their name.
        If no relevant quotes are found for a respondent, omit them from your output.
        Ensure you complete the analysis for all 20 respondents.
        Begin your analysis now, ensuring your output adheres to the format above.""")]

# Selectbox for choosing a base prompt
selected_base_prompt = st.selectbox(
    "Choose a base prompt",
    options=[prompt[0] for prompt in base_prompts],
    index=0,
    key="base_prompt_select"
)

# Research question input field
research_question = st.text_area(
    "Enter your research theme or question",
    placeholder="Type your research question or theme here",
    height=100,
    disabled=not uploaded_file,
)

# Combine base prompt and research question (but don't display it)
selected_base_prompt_text = next(prompt[1] for prompt in base_prompts if prompt[0] == selected_base_prompt)
combined_prompt = f"{selected_base_prompt_text}\n\nResearch Question or general research theme: {research_question or 'Analyze the general themes and insights from the interviews'}"

# Submit button to trigger LLM request
submit_button = st.button("Submit", disabled=not (uploaded_file and research_question and api_key))

if submit_button:
    research_data = uploaded_file
    
    with st.spinner("Generating answer... Please wait."):
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful design research assistant."},
                    {"role": "user", "content": f"Here's the research data:\n\n{research_data}\n\n{combined_prompt}"}
                ],
                max_tokens=1024
            )
            
            st.write("### Answer")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please check your API key and try again.")