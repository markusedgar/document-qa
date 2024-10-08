import streamlit as st
from openai import OpenAI
import os

def main_app():
    st.title("📝 Analyse your research data")

    # Try to get the API key from secrets, otherwise use an input field
    api_key = st.secrets["OPENAI_API_KEY"]
    if not api_key:
        st.error("OpenAI API key not found in secrets. Please add it to continue.")

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
            * Respondent Name (brief description): "[Quote]" 
            ** Relation to research question: [Concise explanation of how the quote connects to the research question] |
            
            Additional Guidelines:
            Make sure to mark up to 5 top quotes that are directly and strictly related to the research question or theme. You can iuclude more quotes if they are still directly related.
            Keep explanations clear and to the point.
            If a respondent has multiple relevant quotes, group them under their name.
            If no relevant quotes are found for a respondent, omit them from your output.
            Ensure you complete the analysis for all 20 respondents.
            Begin your analysis now, ensuring your output adheres to the format above."""),
            ("Identify stakeholders", """You are tasked with analyzing transcript data from 20 respondents to identify key stakeholders. Your objective is to extract and present key insights from the data in an organized, easy-to-read format.

            Instructions:
            Understand the Research Question or Research Theme: Start by thoroughly reading and comprehending the research question or theme.
            Analyze the Transcript Data: Go through the transcript data to identify stakeholders who were mentioned and are related research question or theme. Then analyse the transcript data to further identify relationships or value exchanges between stakeholders. 
            
            Steps:
            Extract stakeholders: Identify mentions of people and organisations beyond the travelers we talked to. Extract that information from the parts of the transcripts that are related to the research question or theme.
            Respondent Identification: For each mention of a stakeholder, add a note with a brief summary of who they are (if available). Add ONE defining quote from the transcripts as an illustration (including who said it) 
            Stakeholder Relevance: Briefly explain how each identified stakeholder relates to the research question or theme. 
            
            Use a table format for your output using the following columns:
            * Stakeholder Name (brief description)
            ** Brief description of the stakeholder
            ** Example quote from the transcripts: "[Example Quote]"
            ** Stakeholder Relevance & Value Exchanges: [Explanation of how the stakeholder is relevant to the research question and what value exchange exists]
            ** Respondent who mentioned the stakeholder: [list of names of the respondents who mentioned the stakeholder]
             """),
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

def ideation_helper():
    st.header("Ideation Helper")
    st.write("This section will help you generate ideas. The ideation prompt used here is based on the following research: https://arxiv.org/abs/2402.01727")
    st.write("""
              
     The ideation process follows these steps:
     1. Generate a list of ideas (short titles only) for possible products or services based on the requirements you provide.
     2. Review and refine the ideas to ensure they are unique and bold.
     3. Develop each idea with a name, followed by a colon, and a 40-80 word description.
     
     The output will reflect this structure, presenting a series of innovative and distinct ideas.
     """)

     # Try to get the API key from secrets, otherwise use an input field
    api_key = st.secrets["OPENAI_API_KEY"]
    if not api_key:
        st.error("OpenAI API key not found in secrets. Please add it to continue.")
    
    # Textarea for idea requirements
    idea_requirements = st.text_area(
        "What kind of ideas are you looking for?",
        placeholder="Describe the type of ideas you want (e.g. by posting your HMW question) and any specific requirements",
        height=150
    )
    # Slider for selecting the number of ideas to generate
    num_ideas = st.slider("Number of ideas to generate", min_value=10, max_value=25, value=15, step=1)

    # Submit button for idea generation
    generate_ideas_button = st.button("Generate Ideas", disabled=not idea_requirements)

    if generate_ideas_button:
        with st.spinner("Generating ideas... Please wait."):
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a creative ideation assistant."},
                        {"role": "user", "content": f"""Generate new product or service ideas with the following requirements:
                        {idea_requirements}

                        The ideas are just ideas. The product or service need not yet exist, nor may it
                        necessarily be clearly feasible.
                        Follow these steps. Do each step, even if you think you do not need to.
                        First generate a list of {num_ideas} ideas (short title only).
                        Second, go through the list and determine whether the ideas are different and
                        bold, modify the ideas as needed to make them bolder and more different. No two
                        ideas should be the same. This is important!
                        Next, give the ideas a name and combine it with a product or service description.
                        The name and idea are separated by a colon and followed by a description. The
                        idea should be expressed as a paragraph of 40-80 words. Do this step by step!"""}
                    ],
                    max_tokens=3000
                )
                
                st.write("### Generated Ideas")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your API key and try again.")

def prototyping_helper():
    st.header("Prototyping Helper")
    st.write("This section will help you generate advertisement slogans for your concept.")

    # Try to get the API key from secrets, otherwise use an input field
    api_key = st.secrets["OPENAI_API_KEY"]
    if not api_key:
        st.error("OpenAI API key not found in secrets. Please add it to continue.")
    
    # Define prompt templates
    prompt_templates = {
        "Standard Slogans": """Generate 10 catchy and memorable advertisement slogans for the following concept:
        {concept}

        The slogans should be: 
        1. Short and punchy
        2. Relevant to the concept
        3. Unique and creative
        4. Easy to remember

        Please provide a numbered list of 10 slogans.""",
        "Humorous Slogans": """Generate 10 funny and witty advertisement slogans for the following concept:
        {concept}

        The slogans should be:
        1. Humorous and entertaining
        2. Relevant to the concept
        3. Memorable and shareable
        4. Appropriate for the target audience

        Please provide a numbered list of 10 slogans.""",
        "Emotional Slogans": """Generate 10 emotionally appealing advertisement slogans for the following concept:
        {concept}

        The slogans should:
        1. Evoke strong positive emotions
        2. Connect with the audience on a personal level
        3. Highlight the benefits or value proposition
        4. Be memorable and impactful

        Please provide a numbered list of 10 slogans."""
    }

    # Dropdown for selecting prompt template
    selected_template = st.selectbox(
        "Choose a slogan style",
        options=list(prompt_templates.keys()),
        index=0
    )

    # Textarea for concept input
    concept = st.text_area(
        "Enter your concept",
        placeholder="Describe the product or service concept for which you want to generate slogans",
        height=100
    )

    # Submit button for slogan generation
    generate_slogans_button = st.button("Generate Slogans", disabled=not concept)

    if generate_slogans_button:
        with st.spinner("Generating slogans... Please wait."):
            try:
                client = OpenAI(api_key=api_key)
                
                # Merge selected template with concept
                full_prompt = prompt_templates[selected_template].format(concept=concept)
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a creative advertising assistant."},
                        {"role": "user", "content": full_prompt}
                    ],
                    max_tokens=1000
                )
                
                st.write("### Generated Slogans")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your API key and try again.")

def implementation_helper():
    st.header("Implementation Helper")
    st.write("This section will help you generate next steps to implement your concept.")

    # Try to get the API key from secrets, otherwise use an input field
    api_key = st.secrets["OPENAI_API_KEY"]
    if not api_key:
        st.error("OpenAI API key not found in secrets. Please add it to continue.")
    
    # Textarea for concept input
    concept = st.text_area(
        "Enter your concept",
        placeholder="Describe the product or service concept you want to implement",
        height=100
    )

    # Dropdown for selecting implementation phase
    implementation_phase = st.selectbox(
        "Choose the implementation phase",
        options=["Planning", "Development", "Testing", "Launch", "Post-launch"],
        index=0
    )

    # Submit button for generating implementation steps
    generate_steps_button = st.button("Generate Implementation Steps", disabled=not concept)

    if generate_steps_button:
        with st.spinner("Generating implementation steps... Please wait."):
            try:
                client = OpenAI(api_key=api_key)
                
                prompt = f"""Generate a detailed list of next steps to implement the following concept:
                {concept}

                Focus on the {implementation_phase} phase of implementation.

                Please provide:
                1. A numbered list of 5-7 concrete, actionable steps
                2. A brief explanation for each step
                3. Potential challenges or considerations for each step

                Format each step as follows:
                Step X: [Step Name]
                - Explanation: [Brief explanation of the step]
                - Considerations: [Potential challenges or important points to consider]

                """
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful product implementation assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1500
                )
                
                st.write("### Implementation Steps")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your API key and try again.")

def change_management_helper():
    st.header("Change Management Helper")
    st.write("This section will help you identify potential resistance within the organization when implementing a given concept.")

    # Try to get the API key from secrets, otherwise use an input field
    api_key = st.secrets["OPENAI_API_KEY"]
    if not api_key:
        st.error("OpenAI API key not found in secrets. Please add it to continue.")
    
    # Textarea for concept input
    concept = st.text_area(
        "Enter your concept",
        placeholder="Describe the concept you want to implement",
        height=100
    )

    # Submit button for generating resistance identification
    generate_resistance_button = st.button("Identify Potential Resistance", disabled=not concept)

    if generate_resistance_button:
        with st.spinner("Analyzing potential resistance... Please wait."):
            try:
                client = OpenAI(api_key=api_key)
                prompt = f"""Identify potential areas of resistance within the organization when implementing the following concept:
                {concept}

                Please provide:
                1. A numbered list of 5-7 potential sources of resistance
                2. A brief explanation for each source
                3. Suggestions on how to mitigate each resistance

                Format each point as follows:
                Source X: [Source Name]
                - Explanation: [Brief explanation of the resistance]
                - Mitigation: [Suggestions for addressing the resistance]
                """
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a change management assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1500
                )
                
                st.write("### Potential Resistance and Mitigation Strategies")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your API key and try again.")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Main App", "Ideation Helper", "Prototyping Helper", "Implementation Helper", "Change Management Helper"])

with tab1:
    main_app()

with tab2:
    ideation_helper()

with tab3:
    prototyping_helper()

with tab4:
    implementation_helper()

with tab5:
    change_management_helper()

