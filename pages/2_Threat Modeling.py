'''
#main.py
import os
import base64
import streamlit as st
import streamlit.components.v1 as components
#from dotenv import load_dotenv


from threat_model import create_threat_model_prompt, get_threat_model_openai, get_threat_model_google, json_to_markdown
from attack_tree import create_attack_tree_prompt, get_attack_tree_openai
from mitigations import create_mitigations_prompt, get_mitigations_openai, get_mitigations_google

# ------------------------------------ Helper Functions ------------------------------------ #

# Function to get user input for the application description and key details
def get_input():
    input_text = st.text_area(
        label="Describe the application to be modelled",
        placeholder="Enter your application details...",
        height=150,
        key="app_input",
        help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
    )
    return input_text

# Function to render Mermaid diagram
def mermaid(code: str, height: int = 500) -> None:
    components.html(
        f"""
        <pre class="mermaid" style="height: {height}px;">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=height,
    )


# ------------------ Streamlit UI Configuration ------------------ #

st.set_page_config(
    page_title="ThreatGPT",
    page_icon=":material/security:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Create three columns
col1, col2, col3 = st.columns([1,1,1])

# Use the middle column to display the logo, which will be centered

#with col1:
#    st.image("deloitte-logo1.png", width=150)



# ------------------ Sidebar ------------------ #

#st.sidebar.header("ThreatGPT")

with st.sidebar:
    
    # Add model selection input field to the sidebar
    model_provider = st.selectbox(
        "Select your preferred model provider:",
        ["Google Gemini", "OpenAI"],
        key="model_provider",
        help="Select the LLM model provider you would like to use.", 
    )

    # if model_provider == "OpenAI API":
        
    #     # Load OpenAI API key
    #     load_dotenv(override=True)
    #     openai_api_key = os.getenv("OPENAI_API_KEY")
    #     # Add model selection input field to the sidebar
    #     selected_model = st.selectbox(
    #         "Select the model you would like to use:",
    #         ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
    #         key="selected_model",
    #         #help="The model points to the latest available version.",
    #     )

    methodology = st.selectbox(
        label="Select the methodology to model the application",
        options=["DREAD", "STRIDE", "MITRE ATT&CK"],
        key="methodology",
    )

#model_provider = "OpenAI API"
#selected_model = "gpt-4o"

# model_provider = "Gemini API"
# selected_model = "gemini-1.5-pro"

#Load OpenAI and Google Gemini API key
#load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")   #st.secrets("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

# ------------------ Main App UI ------------------ #

col1, col2, col3 = st.columns([1,1,1])

with col2:
    st.title("ThreatGPT")


# If model provider is OpenAI API and the model is gpt-4-turbo or gpt-4o
# if model_provider == "OpenAI API":
#     if selected_model == "gpt-4o" or selected_model == "gpt-4-turbo" : 
#         uploaded_file = st.file_uploader("Upload architecture diagram", type=["xml", "jpg", "jpeg", "png"])

#         if uploaded_file is not None:
#             if not openai_api_key:
#                 st.error("Please enter your OpenAI API key to analyse the image.")
#             else:
#                 if 'uploaded_file' not in st.session_state or st.session_state.uploaded_file != uploaded_file:
#                     st.session_state.uploaded_file = uploaded_file
#                     with st.spinner("Analysing the uploaded image..."):
#                         def encode_image(uploaded_file):
#                             return base64.b64encode(uploaded_file.read()).decode('utf-8')

#                         base64_image = encode_image(uploaded_file)

#                         image_analysis_prompt = create_image_analysis_prompt()

#                         try:
#                             image_analysis_output = get_image_analysis(openai_api_key, selected_model, image_analysis_prompt, base64_image)
#                             if image_analysis_output and 'choices' in image_analysis_output and image_analysis_output['choices']:
#                                 image_analysis_content = image_analysis_output['choices'][0]['message']['content']
#                                 st.session_state.image_analysis_content = image_analysis_content
#                             else:
#                                 st.error("Failed to analyze the image. Please check the API key and try again.")
#                         except KeyError as e:
#                             st.error("Failed to analyze the image. Please check the API key and try again.")
#                             print(f"Error: {e}")
#                         except Exception as e:
#                             st.error("An unexpected error occurred while analyzing the image.")
#                             print(f"Error: {e}")

#                 app_input = st.text_area(
#                     label="Describe the application to be modelled",
#                     value=st.session_state.get('image_analysis_content', ''),
#                     height=150,
#                     key="app_input",
#                     help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
#                 )
#         else:
#             if 'image_analysis_content' in st.session_state:
#                 del st.session_state.image_analysis_content
#             app_input = get_input()
# else:
  

app_input = get_input()

# Create two columns layout for input fields
col1, col2 = st.columns(2)

# Create input fields for app_type, sensitive_data and pam
with col1:
    
    app_type = st.selectbox(
        label="Select the application type",
        options=[
            "Other",
            "Web application",
            "Mobile application",
            "Desktop application",
            "Cloud application",
            "IoT application",
        ],
        key="app_type",
    )

    sensitive_data = st.selectbox(
        label="What is the highest sensitivity level of the data processed by the application?",
        options=[
            "None",
            "Top Secret",
            "Secret",
            "Confidential",
            "Restricted",
            "Unclassified",
        ],
        key="sensitive_data",
    )

    pam = st.selectbox(
        label="Are privileged accounts stored in a PAM solution?",
        options=["No","Yes"],
        key="pam",
    )
    
    

# Create input fields for internet_facing and authentication
with col2:
    internet_facing = st.selectbox(
        label="Is the application internet-facing?",
        options=["No", "Yes"],
        key="internet_facing",
    )

    authentication = st.multiselect(
        "What authentication methods are supported by the application?",
        ["None", "SSO", "MFA", "OAUTH2", "Basic"],
        key="authentication",
    )

# ------------------ Threat Model Generation ------------------ #

# Create a collapsible section for Threat Modeling
with st.expander("Threat Model", expanded=True):    
    # Create a submit button for Threat Modelling
    threat_model_submit_button = st.button(label="Generate Threat Model")

    # If the Generate Threat Model button is clicked and the user has provided an application description
    if threat_model_submit_button and app_input:
        # Generate the prompt using the create_prompt function
        threat_model_prompt = create_threat_model_prompt(methodology, app_type, authentication, internet_facing, sensitive_data, pam, app_input)

        # Show a spinner while generating the threat model
        with st.spinner("Analysing potential threats..."):
            max_retries = 3
            retry_count = 0
            while retry_count < max_retries:
                try:    
                    # Call one of the get_threat_model functions with the generated prompt
                    if model_provider == "OpenAI":
                        selected_model = "gpt-4o"
                        model_output = get_threat_model_openai(openai_api_key, selected_model, threat_model_prompt)

                    if model_provider == "Google Gemini":
                        selected_model = "gemini-1.5-pro"
                        model_output = get_threat_model_google(google_api_key, selected_model, threat_model_prompt)

                    # Access the threat model and improvement suggestions from the parsed content
                    threat_model = model_output.get("threat_model", [])
                    suggestions_summary = model_output.get("suggestions_summary", [])

                    # Save the threat model to the session state for later use in mitigations
                    st.session_state['threat_model'] = threat_model
                    break  # Exit the loop if successful
                except Exception as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        st.error(f"Error generating threat model after {max_retries} attempts: {e}")
                        threat_model = []
                        suggestions_summary = []
                    else:
                        st.warning(f"Error generating threat model. Retrying attempt {retry_count+1}/{max_retries}...")

        # Convert the threat model JSON to Markdown
        markdown_output = json_to_markdown(threat_model, suggestions_summary)

        # Display the threat model in Markdown
        st.markdown(markdown_output)


        # Add a button to allow the user to download the output as a Markdown file
        st.download_button(
            label="Download Threat Model (Markdown)",
            data=markdown_output,  # Use the Markdown output
            file_name="threatGPT_threatModel.md", 
            mime="text/markdown",
        )


    # If the submit button is clicked and the user has not provided an application description
    if threat_model_submit_button and not app_input:
        st.error("Please enter your application details before submitting.")



# ------------------ Attack Tree Generation ------------------ #

# # Create a collapsible section for Attack Tree
# with st.expander("Attack Tree", expanded=True):

#     # Create a submit button for Attack Tree
#     attack_tree_submit_button = st.button(label="Generate Attack Tree")

#     # If the Generate Attack Tree button is clicked and the user has provided an application description
#     if attack_tree_submit_button and app_input:
#         # Generate the prompt using the create_attack_tree_prompt function
#         attack_tree_prompt = create_attack_tree_prompt(methodology, app_type, authentication, internet_facing, sensitive_data, pam, app_input)

#         # Show a spinner while generating the attack tree
#         with st.spinner("Generating attack tree..."):
#             try:
#                 # Call to either of the get_attack_tree functions with the generated prompt
#                 if model_provider == "OpenAI":
#                     mermaid_code = get_attack_tree_openai(openai_api_key, selected_model, attack_tree_prompt)
#                 # elif model_provider == "Google Gemini":
#                 #     mermaid_code = get_attack_tree(google_api_key, selected_model, attack_tree_prompt)

#                 # Display the generated attack tree code
#                 st.write("Attack Tree Code:")
#                 st.code(mermaid_code)

#                 # Visualise the attack tree using the Mermaid custom component
#                 st.write("Attack Tree Diagram Preview:")
#                 mermaid(mermaid_code)
                
#                 col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
                
#                 with col1:              
#                     # Add a button to allow the user to download the Mermaid code
#                     st.download_button(
#                         label="Download Diagram Code",
#                         data=mermaid_code,
#                         file_name="attack_tree.md",
#                         mime="text/plain",
#                         help="Download the Mermaid code for the attack tree diagram."
#                     )

#                 with col2:
#                     # Add a button to allow the user to open the Mermaid Live editor
#                     mermaid_live_button = st.link_button("Open Mermaid Live", "https://mermaid.live")
                
#                 with col3:
#                     # Blank placeholder
#                     st.write("")
                
#                 with col4:
#                     # Blank placeholder
#                     st.write("")
                
#                 with col5:
#                     # Blank placeholder
#                     st.write("")

#             except Exception as e:
#                 st.error(f"Error generating attack tree: {e}")

#     if attack_tree_submit_button and not app_input:
#         st.error("Please enter your application details before submitting.")

# ------------------ Mitigations Generation ------------------ #


# st.write("Mitigations")
# # Create a submit button for Mitigations
# mitigations_submit_button = st.button(label="Suggest Mitigations")

# # If the Suggest Mitigations button is clicked and the user has identified threats
# if mitigations_submit_button:
#     # Check if threat_model data exists
#     if 'threat_model' in st.session_state and st.session_state['threat_model']:
#         # Convert the threat_model data into a Markdown list
#         threats_markdown = json_to_markdown(st.session_state['threat_model'], [])
#         # Generate the prompt using the create_mitigations_prompt function
#         mitigations_prompt = create_mitigations_prompt(methodology, threats_markdown)

#         # Show a spinner while suggesting mitigations
#         with st.spinner("Suggesting mitigations..."):
#             max_retries = 3
#             retry_count = 0
#             while retry_count < max_retries:
#                 try:
#                     # Call to either of the get_mitigations functions with the generated prompt
#                     if model_provider == "OpenAI API":
#                         mitigations_markdown = get_mitigations(openai_api_key, selected_model, mitigations_prompt)

#                     # Display the suggested mitigations in Markdown
#                     with st.container():
#                         st.markdown(mitigations_markdown)
#                     break  # Exit the loop if successful
#                 except Exception as e:
#                     retry_count += 1
#                     if retry_count == max_retries:
#                         st.error(f"Error suggesting mitigations after {max_retries} attempts: {e}")
#                         mitigations_markdown = ""
#                     else:
#                         st.warning(f"Error suggesting mitigations. Retrying attempt {retry_count+1}/{max_retries}...")
        
#         #st.markdown("")

#         # # Add a button to allow the user to download the mitigations as a Markdown file
#         # st.download_button(
#         #     label="Download Mitigations",
#         #     data=mitigations_markdown,
#         #     file_name="mitigations.md",
#         #     mime="text/markdown",
#         # )
#     else:
#         st.error("Please generate a threat model first before suggesting mitigations.")






# #Create a collapsible section for Mitigations

# with st.expander("Mitigations", expanded=True):
#     # Create a submit button for Mitigations
#     mitigations_submit_button = st.button(label="Suggest Mitigations")

#     # If the Suggest Mitigations button is clicked and the user has identified threats
#     if mitigations_submit_button:
#         # Check if threat_model data exists
#         if 'threat_model' in st.session_state and st.session_state['threat_model']:
#             # Convert the threat_model data into a Markdown list
#             threats_markdown = json_to_markdown(st.session_state['threat_model'], [])
#             # Generate the prompt using the create_mitigations_prompt function
#             mitigations_prompt = create_mitigations_prompt(methodology, threats_markdown)

#             # Show a spinner while suggesting mitigations
#             with st.spinner("Suggesting mitigations..."):
#                 max_retries = 3
#                 retry_count = 0
#                 while retry_count < max_retries:
#                     try:
#                         # Call to either of the get_mitigations functions with the generated prompt
#                         if model_provider == "OpenAI API":
#                             mitigations_markdown = get_mitigations(openai_api_key, selected_model, mitigations_prompt)

#                         # Display the suggested mitigations in Markdown
#                         st.markdown(mitigations_markdown)
#                         break  # Exit the loop if successful
#                     except Exception as e:
#                         retry_count += 1
#                         if retry_count == max_retries:
#                             st.error(f"Error suggesting mitigations after {max_retries} attempts: {e}")
#                             mitigations_markdown = ""
#                         else:
#                             st.warning(f"Error suggesting mitigations. Retrying attempt {retry_count+1}/{max_retries}...")
            
#             st.markdown("")

#             # Add a button to allow the user to download the mitigations as a Markdown file
#             st.download_button(
#                 label="Download Mitigations",
#                 data=mitigations_markdown,
#                 file_name="mitigations.md",
#                 mime="text/markdown",
#             )
#         else:
#             st.error("Please generate a threat model first before suggesting mitigations.")
'''










#main.py
import os
import base64
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import cv2
#from dotenv import load_dotenv


from threat_model import create_threat_model_prompt, get_threat_model_openai, get_threat_model_google, create_image_analysis_prompt, get_image_analysis, json_to_markdown
from attack_tree import create_attack_tree_prompt, get_attack_tree_openai
from mitigations import create_mitigations_prompt, get_mitigations_openai, get_mitigations_google

# ------------------------------------ Helper Functions ------------------------------------ #

# Function to get user input for the application description and key details
def get_input():
    input_text = st.text_area(
        label="Describe the application to be modelled",
        placeholder="Enter your application details...",
        height=150,
        key="app_input",
        help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
    )
    return input_text

# Function to render Mermaid diagram
def mermaid(code: str, height: int = 500) -> None:
    components.html(
        f"""
        <pre class="mermaid" style="height: {height}px;">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=height,
    )


# ------------------ Streamlit UI Configuration ------------------ #

st.set_page_config(
    page_title="ThreatGPT",
    page_icon=":material/security:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Create three columns
col1, col2, col3 = st.columns([1,1,1])

# Use the middle column to display the logo, which will be centered

#with col1:
#    st.image("deloitte-logo1.png", width=150)



# ------------------ Sidebar ------------------ #

#st.sidebar.header("ThreatGPT")

with st.sidebar:
    
    # Add model selection input field to the sidebar
    model_provider = st.selectbox(
        "Select your preferred model provider:",
        ["OpenAI", "Google Gemini"],
        key="model_provider",
        help="Select the LLM model provider you would like to use.", 
    )

    # if model_provider == "OpenAI API":
        
    #     # Load OpenAI API key
    #     load_dotenv(override=True)
    #     openai_api_key = os.getenv("OPENAI_API_KEY")
    #     # Add model selection input field to the sidebar
    #     selected_model = st.selectbox(
    #         "Select the model you would like to use:",
    #         ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
    #         key="selected_model",
    #         #help="The model points to the latest available version.",
    #     )

    methodology = st.selectbox(
        label="Select the methodology to model the application",
        options=["DREAD", "STRIDE", "MITRE ATT&CK"],
        key="methodology",
    )

#model_provider = "OpenAI"
selected_model = "gpt-4o"

# model_provider = "Gemini"
# selected_model = "gemini-1.5-pro"

#Load OpenAI and Google Gemini API key
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")   
google_api_key = os.getenv("GOOGLE_API_KEY")

# ------------------ Main App UI ------------------ #

col1, col2, col3 = st.columns([1,1,1])

with col2:
    st.title("ThreatGPT")


def load_image(uploaded_file):
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

    # Now do something with the image! For example, let's display it:
    st.image(opencv_image, channels="BGR")  



if 'app_input' not in st.session_state:
    st.session_state['app_input'] = ''

#uploaded_file = st.file_uploader("Upload architecture diagram", type=["jpg", "jpeg", "png"])

if model_provider == "OpenAI" and selected_model in ["gpt-4-turbo", "gpt-4o", "gpt-4o-mini"]:
    uploaded_file = st.file_uploader("Upload architecture diagram", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file)
        if not openai_api_key:
            st.error("Please enter your OpenAI API key to analyse the image.")
        else:
            if 'uploaded_file' not in st.session_state or st.session_state.uploaded_file != uploaded_file:
                st.session_state.uploaded_file = uploaded_file
                with st.spinner("Analysing the uploaded image..."):
                    def encode_image(uploaded_file):
                        return base64.b64encode(uploaded_file.read()).decode('utf-8')

                    base64_image = encode_image(uploaded_file)

                    image_analysis_prompt = create_image_analysis_prompt()

                    try:
                        image_analysis_output = get_image_analysis(openai_api_key, selected_model, image_analysis_prompt, base64_image)
                        if image_analysis_output and 'choices' in image_analysis_output and image_analysis_output['choices'][0]['message']['content']:
                            image_analysis_content = image_analysis_output['choices'][0]['message']['content']
                            st.session_state.image_analysis_content = image_analysis_content
                            # Update app_input session state
                            st.session_state['app_input'] = image_analysis_content
                        else:
                            st.error("Failed to analyze the image. Please check the API key and try again.")
                    except KeyError as e:
                        st.error("Failed to analyze the image. Please check the API key and try again1.")
                        print(f"Error: {e}")
                    except Exception as e:
                        st.error("An unexpected error occurred while analyzing the image.")
                        print(f"Error: {e}")    

    # Use text_area with the session state value and update the session state on change
    app_input = st.text_area(
        label="Describe the application to be modelled",
        value=st.session_state['app_input'],
        key="app_input_widget",
        help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
    )
    # Update session state only if the text area content has changed
    if app_input != st.session_state['app_input']:
        st.session_state['app_input'] = app_input


else:
    # For other model providers or models, use the get_input() function
    app_input = get_input()
    # Update session state
    st.session_state['app_input'] = app_input

# Ensure app_input is always up to date in the session state
app_input = st.session_state['app_input']




# Create two columns layout for input fields
col1, col2 = st.columns(2)

# Create input fields for app_type, sensitive_data and pam
with col1:
    
    app_type = st.selectbox(
        label="Select the application type",
        options=[
            "Other",
            "Web application",
            "Mobile application",
            "Desktop application",
            "Cloud application",
            "IoT application",
        ],
        key="app_type",
    )

    sensitive_data = st.selectbox(
        label="What is the highest sensitivity level of the data processed by the application?",
        options=[
            "None",
            "Top Secret",
            "Secret",
            "Confidential",
            "Restricted",
            "Unclassified",
        ],
        key="sensitive_data",
    )

    pam = st.selectbox(
        label="Are privileged accounts stored in a PAM solution?",
        options=["No","Yes"],
        key="pam",
    )
    

# Create input fields for internet_facing and authentication
with col2:
    internet_facing = st.selectbox(
        label="Is the application internet-facing?",
        options=["No", "Yes"],
        key="internet_facing",
    )

    authentication = st.multiselect(
        "What authentication methods are supported by the application?",
        ["None", "SSO", "MFA", "OAUTH2", "Basic"],
        key="authentication",
    )

# ------------------ Threat Model Generation ------------------ #

# Create a collapsible section for Threat Modeling
with st.expander("Threat Model", expanded=True):    
    # Create a submit button for Threat Modelling
    threat_model_submit_button = st.button(label="Generate Threat Model")

    # If the Generate Threat Model button is clicked and the user has provided an application description
    if threat_model_submit_button and app_input:
        # Generate the prompt using the create_prompt function
        threat_model_prompt = create_threat_model_prompt(methodology, app_type, authentication, internet_facing, sensitive_data, pam, app_input)

        # Show a spinner while generating the threat model
        with st.spinner("Analysing potential threats..."):
            max_retries = 3
            retry_count = 0
            while retry_count < max_retries:
                try:    
                    # Call one of the get_threat_model functions with the generated prompt
                    if model_provider == "OpenAI":
                        selected_model = "gpt-4o"
                        model_output = get_threat_model_openai(openai_api_key, selected_model, threat_model_prompt)

                    if model_provider == "Google Gemini":
                        selected_model = "gemini-1.5-pro"
                        model_output = get_threat_model_google(google_api_key, selected_model, threat_model_prompt)

                    # Access the threat model and improvement suggestions from the parsed content
                    threat_model = model_output.get("threat_model", [])
                    suggestions_summary = model_output.get("suggestions_summary", [])

                    # Save the threat model to the session state for later use in mitigations
                    st.session_state['threat_model'] = threat_model
                    break  # Exit the loop if successful
                except Exception as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        st.error(f"Error generating threat model after {max_retries} attempts: {e}")
                        threat_model = []
                        suggestions_summary = []
                    else:
                        st.warning(f"Error generating threat model. Retrying attempt {retry_count+1}/{max_retries}...")

        # Convert the threat model JSON to Markdown
        markdown_output = json_to_markdown(threat_model, suggestions_summary)

        # Display the threat model in Markdown
        st.markdown(markdown_output)


        # Add a button to allow the user to download the output as a Markdown file
        st.download_button(
            label="Download Threat Model (Markdown)",
            data=markdown_output,  # Use the Markdown output
            file_name="threatGPT_threatModel.md", 
            mime="text/markdown",
        )


    # If the submit button is clicked and the user has not provided an application description
    if threat_model_submit_button and not app_input:
        st.error("Please enter your application details before submitting.")



# ------------------ Attack Tree Generation ------------------ #

# # Create a collapsible section for Attack Tree
# with st.expander("Attack Tree", expanded=True):

#     # Create a submit button for Attack Tree
#     attack_tree_submit_button = st.button(label="Generate Attack Tree")

#     # If the Generate Attack Tree button is clicked and the user has provided an application description
#     if attack_tree_submit_button and app_input:
#         # Generate the prompt using the create_attack_tree_prompt function
#         attack_tree_prompt = create_attack_tree_prompt(methodology, app_type, authentication, internet_facing, sensitive_data, pam, app_input)

#         # Show a spinner while generating the attack tree
#         with st.spinner("Generating attack tree..."):
#             try:
#                 # Call to either of the get_attack_tree functions with the generated prompt
#                 if model_provider == "OpenAI":
#                     mermaid_code = get_attack_tree_openai(openai_api_key, selected_model, attack_tree_prompt)
#                 # elif model_provider == "Google Gemini":
#                 #     mermaid_code = get_attack_tree(google_api_key, selected_model, attack_tree_prompt)

#                 # Display the generated attack tree code
#                 st.write("Attack Tree Code:")
#                 st.code(mermaid_code)

#                 # Visualise the attack tree using the Mermaid custom component
#                 st.write("Attack Tree Diagram Preview:")
#                 mermaid(mermaid_code)
                
#                 col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
                
#                 with col1:              
#                     # Add a button to allow the user to download the Mermaid code
#                     st.download_button(
#                         label="Download Diagram Code",
#                         data=mermaid_code,
#                         file_name="attack_tree.md",
#                         mime="text/plain",
#                         help="Download the Mermaid code for the attack tree diagram."
#                     )

#                 with col2:
#                     # Add a button to allow the user to open the Mermaid Live editor
#                     mermaid_live_button = st.link_button("Open Mermaid Live", "https://mermaid.live")
                
#                 with col3:
#                     # Blank placeholder
#                     st.write("")
                
#                 with col4:
#                     # Blank placeholder
#                     st.write("")
                
#                 with col5:
#                     # Blank placeholder
#                     st.write("")

#             except Exception as e:
#                 st.error(f"Error generating attack tree: {e}")

#     if attack_tree_submit_button and not app_input:
#         st.error("Please enter your application details before submitting.")

# ------------------ Mitigations Generation ------------------ #


# st.write("Mitigations")
# # Create a submit button for Mitigations
# mitigations_submit_button = st.button(label="Suggest Mitigations")

# # If the Suggest Mitigations button is clicked and the user has identified threats
# if mitigations_submit_button:
#     # Check if threat_model data exists
#     if 'threat_model' in st.session_state and st.session_state['threat_model']:
#         # Convert the threat_model data into a Markdown list
#         threats_markdown = json_to_markdown(st.session_state['threat_model'], [])
#         # Generate the prompt using the create_mitigations_prompt function
#         mitigations_prompt = create_mitigations_prompt(methodology, threats_markdown)

#         # Show a spinner while suggesting mitigations
#         with st.spinner("Suggesting mitigations..."):
#             max_retries = 3
#             retry_count = 0
#             while retry_count < max_retries:
#                 try:
#                     # Call to either of the get_mitigations functions with the generated prompt
#                     if model_provider == "OpenAI API":
#                         mitigations_markdown = get_mitigations(openai_api_key, selected_model, mitigations_prompt)

#                     # Display the suggested mitigations in Markdown
#                     with st.container():
#                         st.markdown(mitigations_markdown)
#                     break  # Exit the loop if successful
#                 except Exception as e:
#                     retry_count += 1
#                     if retry_count == max_retries:
#                         st.error(f"Error suggesting mitigations after {max_retries} attempts: {e}")
#                         mitigations_markdown = ""
#                     else:
#                         st.warning(f"Error suggesting mitigations. Retrying attempt {retry_count+1}/{max_retries}...")
        
#         #st.markdown("")

#         # # Add a button to allow the user to download the mitigations as a Markdown file
#         # st.download_button(
#         #     label="Download Mitigations",
#         #     data=mitigations_markdown,
#         #     file_name="mitigations.md",
#         #     mime="text/markdown",
#         # )
#     else:
#         st.error("Please generate a threat model first before suggesting mitigations.")






# #Create a collapsible section for Mitigations

# with st.expander("Mitigations", expanded=True):
#     # Create a submit button for Mitigations
#     mitigations_submit_button = st.button(label="Suggest Mitigations")

#     # If the Suggest Mitigations button is clicked and the user has identified threats
#     if mitigations_submit_button:
#         # Check if threat_model data exists
#         if 'threat_model' in st.session_state and st.session_state['threat_model']:
#             # Convert the threat_model data into a Markdown list
#             threats_markdown = json_to_markdown(st.session_state['threat_model'], [])
#             # Generate the prompt using the create_mitigations_prompt function
#             mitigations_prompt = create_mitigations_prompt(methodology, threats_markdown)

#             # Show a spinner while suggesting mitigations
#             with st.spinner("Suggesting mitigations..."):
#                 max_retries = 3
#                 retry_count = 0
#                 while retry_count < max_retries:
#                     try:
#                         # Call to either of the get_mitigations functions with the generated prompt
#                         if model_provider == "OpenAI API":
#                             mitigations_markdown = get_mitigations(openai_api_key, selected_model, mitigations_prompt)

#                         # Display the suggested mitigations in Markdown
#                         st.markdown(mitigations_markdown)
#                         break  # Exit the loop if successful
#                     except Exception as e:
#                         retry_count += 1
#                         if retry_count == max_retries:
#                             st.error(f"Error suggesting mitigations after {max_retries} attempts: {e}")
#                             mitigations_markdown = ""
#                         else:
#                             st.warning(f"Error suggesting mitigations. Retrying attempt {retry_count+1}/{max_retries}...")
            
#             st.markdown("")

#             # Add a button to allow the user to download the mitigations as a Markdown file
#             st.download_button(
#                 label="Download Mitigations",
#                 data=mitigations_markdown,
#                 file_name="mitigations.md",
#                 mime="text/markdown",
#             )
#         else:
#             st.error("Please generate a threat model first before suggesting mitigations.")



