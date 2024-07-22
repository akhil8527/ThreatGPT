import streamlit as st

st.set_page_config(
    page_title="ThreatGPT",
    page_icon=":material/security:",
    layout='wide',
    initial_sidebar_state="expanded",
)

col1, col2, col3 = st.columns([1,1,1])

with col2:
    st.title("ThreatGPT")

col4, col5, col6 = st.columns([5,10,1])
with col5:
    st.subheader("**Welcome to ThreatGPT !!!**")

st.write("""  
         ThreatGPT is an GenAI-powered threat modeling tool which aims to utilize the capabilities of LLMs to generate comprehensive 
threat models and attack trees based on the details provided by users about their applications. This tool will assist 
security professionals by providing an initial, robust threat analysis, which can be further refined and tailored to 
specific needs. The goal is to make threat modeling more accessible, efficient, and comprehensive, thereby improving the 
security posture of applications from the early stages of development.

**Features of ThreatGPT**:

- **Automated Threat Model Generation**:  
         Utilize LLMs to automatically generate detailed threat models based on user input 
         about application architecture, technologies used, and potential attack surfaces.
- **Methodology Selection**:  
         The tool incorporates well-known methodologies such as MITRE ATT&CK, DREAD, and STRIDE to ensure a 
         structured and thorough analysis of potential threats.
- **Enhance Threat Identification and Mitigation**:  
         Identify potential threats and vulnerabilities specific to the application's
         context and suggest tailored mitigation strategies and security controls.
- **User Friendly Interface**:  
         An intuitive GUI that allows security professionals and non-experts to input application details 
         and interpret the generated threat models and attack trees easily.
- **Leverage Gen AI for Contextual Analysis**:  
         Utilize the contextual understanding of LLMs to analyze complex application 
         architectures and identify subtle or non-obvious threat vectors.
""")


st.caption("Developed by Deloitte India")



# - **Create Dynamic Attack Trees**:  
#          Develop attack trees that visually represent the steps an attacker might take to exploit 
#          vulnerabilities within the application.
