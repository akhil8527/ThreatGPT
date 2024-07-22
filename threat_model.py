#threat_model.py

import json
import requests
import google.generativeai as genai
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
from openai import AzureOpenAI
import streamlit as st
import textwrap


# Function to convert JSON to Markdown for display.    
def json_to_markdown(threat_model, suggestions_summary):
    markdown_output = "## Threat Model\n\n"

    # Start the markdown table with headers
    markdown_output += "|  Threat Type  |  Scenario  |  Potential Impact  |  Suggested Mitigations  |\n"#  Reference Links  |\n"
    markdown_output += "|---------------|------------|--------------------|-------------------------|\n"#-------------------|\n"

    # Fill the table rows with the threat model data
    for threat in threat_model:
        markdown_output += f"| { threat['Threat Type'] } | { threat['Scenario'] } | { threat['Potential Impact'] } | { threat['Suggested Mitigations'] }  | { threat['Reference Links'] } |\n"     ##textwrap.shorten( threat['Reference Links'], width=15, placeholder='...' )
    
    markdown_output += "\n\n## Suggestions Summary\n\n"
    for suggestion in suggestions_summary:
        markdown_output += f"- {suggestion}\n"
    
    return markdown_output


# Function to create a prompt for generating a threat model
def create_threat_model_prompt(methodology, app_type, authentication, internet_facing, sensitive_data, pam, app_input):
    
    if methodology=="STRIDE":
        long_form = "Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege"
    elif methodology=="DREAD":
        long_form = "Damage, Reproducibility, Exploitability, Affected Users, and Discoverability"
    elif methodology=="MITRE ATT&CK":
        long_form = "Adversarial Tactics, Techniques and Common Knowledge"
    
    prompt = f"""
Act as a cyber security expert with more than 20 years experience of using the {methodology} threat modelling methodology 
to produce comprehensive threat models for a wide range of applications. Your task is to use the application description 
and additional details provided to you to produce a list of specific threats for the application.

For each of the {methodology} categories ({long_form}), list multiple (3, 4 or more) credible threats if applicable. Each threat 
scenario should provide a credible Scenario in which the threat could occur in the context of the application. Along with threat
scenario, provide the Potential Impact of the threat scenario and most importantly, provide Technical Improvement Suggestions for 
each threat scenario. Refrain from giving generic suggestions. Also list one credible Reference Link for the 
security team to work on the suggestions given. You have to make sure that the reference link is working and is not dead end. 
This is a very crucial aspect of the response. It is very important that your responses are tailored to incorporate and reflect the 
additional details you are given below.

METHODOLOGY: {methodology}
APPLICATION TYPE: {app_type}
AUTHENTICATION METHODS: {authentication}
INTERNET FACING: {internet_facing}
SENSITIVE DATA: {sensitive_data}
PRIVILEGED ACCESS MANAGEMENT: {pam}
APPLICATION DESCRIPTION: {app_input}

When providing the threat model, use a JSON formatted response with the keys "threat_model" and "suggestions_summary". 
Under "threat_model", include an array of objects with the keys "Threat Type", "Scenario", "Potential Impact", "Suggested Mitigations" 
and "Reference Links". 

Under "suggestions_summary", list an array of strings giving summary of suggestions provided for each threat scenario on how the 
threat modeler can improve their application description in order to allow the tool to produce a more comprehensive threat model.


Example of expected JSON response format:
 
    {{
      "threat_model": [
        {{
          "Threat Type": "Spoofing",
          "Scenario": "Example Scenario 1",
          "Potential Impact": "Example Potential Impact 1",
          "Suggested Mitigations": "Example Suggestion 1",
          "Reference Links": "Example Reference Link 1"
        }},
        {{
          "Threat Type": "Damage",
          "Scenario": "Example Scenario 2",
          "Potential Impact": "Example Potential Impact 2",
          "Suggested Mitigations": "Example Suggestion 2",
          "Reference Links": "Example Reference Link 2"
        }},
        // ... more threats
      ],
      "suggestions_summary": [
        "Example summary suggestion 1.",
        "Example summary suggestion 2.",
        // ... more suggestions summary
      ]
    }}
"""
    return prompt



def create_image_analysis_prompt():
    prompt = """
    You are a Senior Solution Architect with experience of 20 years who is tasked with explaining the following 
    architecture diagram to a Security Architect to support the threat modelling of the system.

    In order to complete this task you must:

      1. Analyse the diagram
      2. Explain the system architecture to the Security Architect. Your explanation should cover the key 
         components, their interactions, and any technologies used.
    
    Provide a direct explanation of the diagram in a clear, structured format, suitable for a professional 
    discussion.
    
    IMPORTANT INSTRUCTIONS:
     - Do not include any words before or after the explanation itself. For example, do not start your
    explanation with "The image shows..." or "The diagram shows..." just start explaining the key components
    and other relevant details.
     - Do not infer or speculate about information that is not visible in the diagram. Only provide information that can be
    directly determined from the diagram itself.
    """
    return prompt



# Function to get analyse uploaded architecture diagrams.
def get_image_analysis(api_key, model_name, prompt, base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                }
            ]
        }
    ]

    payload = {
        "model": model_name,
        "messages": messages,
        "max_tokens": 4000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Log the response for debugging
    try:
        response.raise_for_status()  # Raise an HTTPError for bad responses
        response_content = response.json()
        return response_content
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error
    except Exception as err:
        print(f"Other error occurred: {err}")  # Other errors

    print(f"Response content: {response.content}")  # Log the response content for further inspection
    return None



# Function to get threat model from the GPT response.

def get_threat_model_openai(api_key, model_name, prompt):
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model=model_name,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        #max_tokens=2000,
    )

    # Convert the JSON string in the 'content' field to a Python dictionary
    response_content = json.loads(response.choices[0].message.content)

    return response_content



# Function to get threat model from the Google response.
def get_threat_model_google(google_api_key, google_model, prompt):
    genai.configure(api_key=google_api_key)
    
    model = genai.GenerativeModel(
        google_model,
        generation_config={"response_mime_type": "application/json"})
    
    response = model.generate_content(prompt)
    
    try:
        # Access the JSON content from the 'parts' attribute of the 'content' object
        response_content = json.loads(response.candidates[0].content.parts[0].text)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        print("Raw JSON string:")
        print(response.candidates[0].content.parts[0].text)
        return None

    return response_content
