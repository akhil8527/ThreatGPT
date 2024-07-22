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

col4, col5, col6 = st.columns([1.1,1,1])
with col5:
    st.subheader("**How to Use ??**")


st.write(
"""
**Usage**

\n*Below is an example description that can be used to test ThreatGPT*
                 
SecureBankingApp is a web-based application designed for online banking. It allows users to perform various banking operations 
such as viewing account balances, transferring funds, paying bills, and managing investments. The application also includes features 
for customer support, fraud detection, and secure messaging with bank representatives.

Technology Stack:
Frontend - React.js, Redux, HTML5, CSS3,
Backend - Node.js with Express.js framework,
Database - PostgreSQL,
Authentication - OAuth 2.0,
APIs - RESTful APIs for all major functionalities,
Hosting - AWS (Amazon Web Services),

Other Services:
AWS RDS for database management,
AWS S3 for storing user documents and transaction records,
AWS Lambda for serverless computing functions,
AWS CloudFront for content delivery,
AWS WAF (Web Application Firewall) for protection against web exploits.

Security Features:
Multi-factor authentication (MFA),
End-to-end encryption for data in transit and at rest,
Role-based access control (RBAC),
Regular security audits and penetration testing.

User Roles:
Customer - Can view account details, transfer funds, pay bills, and contact support, Admin - Can manage user accounts,
         monitor transactions, handle customer inquiries, and perform administrative tasks,
Support Agent - Can assist customers with issues and queries through the secure messaging system.

*Input the information in the application description textbox. Also, you can additionally input other details if required.*  
*Choose the threat modeling methodology from the sidebar and click on Threat Model to generate the threat model for the application.*  
*Please navigate to Threat Modeling section to test ThreatGPT*

**FAQs**

1. *How does ThreatGPT work?*

When you input an application description and other relevant details, the tool employs a GPT model to create a 
threat model for your application. Using this information, the model generates a list of potential threats and categorizes 
each threat based on the selected methodology.    

2. *Does ThreatGPT store the application details provided?*

No, ThreatGPT does not store your application description or other details. All entered data is deleted after you close the 
browser tab.

3. *Should you rely on ThreatGPT 100% ?*

No, the threat models are not 100% accurate. ThreatGPT uses Large Language Models (LLMs) to generate its output. 
The GPT models are powerful, but they sometimes make mistakes and are prone to 'hallucinations'. We recommend to use the output only 
as a starting point for identifying and addressing potential security risks in your applications.
                 

"""
)


st.caption("Developed by Deloitte India")