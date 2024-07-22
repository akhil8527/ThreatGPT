## Threat Model

|  Threat Type  |  Scenario  |  Potential Impact  |  Suggested Mitigations  |
|---------------|------------|--------------------|-------------------------|
| Damage | An attacker gains unauthorized access to admin account due to weak passwords and poor access controls. | The attacker could manipulate user data, disrupt services, and extract sensitive data leading to significant financial losses and reputational damage. | Implement stricter password policies and enforce regular password changes. Introduce Privileged Access Management (PAM) to limit admin access to sensitive areas.  |
| Damage | Denial of Service (DoS) attack overwhelms the application’s services, making it unavailable to legitimate users. | Customers lose access to banking services which could lead to loss of trust and financial losses for SecureBankingApp. | Utilize AWS Shield and AWS CloudFront to mitigate DDoS attacks. Ensure regular performance testing and monitoring to identify and respond to traffic spikes.  |
| Damage | Data breach through an unpatched vulnerability in the React.js frontend framework. | Sensitive user data including personal and financial information could be exposed, leading to legal consequences and loss of customer trust. | Follow regular patch management practices and keep all components of the technology stack up-to-date. Incorporate continuous integration/delivery for smoother application updates.  |
| Reproducibility | Cross-Site Scripting (XSS) vulnerabilities allow an attacker to inject malicious scripts into web pages viewed by other users. | Attackers can steal session tokens, perform actions on behalf of users, or redirect users to malicious websites. | Implement a Content Security Policy (CSP), use security headers, and sanitize all inputs to prevent injection attacks.  |
| Reproducibility | Replay attacks in the OAuth 2.0 flow where attackers capture and reuse authentication tokens. | This enables unauthorized access to user accounts and sensitive information, potentially compromising the entire application. | Implement nonce values and timestamps in the OAuth token exchange process to prevent replay attacks. Ensure tokens have limited lifespans and use HTTPS for token transmission.  |
| Reproducibility | SQL Injection through user input fields not properly validated or sanitized. | Attackers can manipulate database queries, leading to unauthorized data access or data manipulation. | Employ parameterized queries and prepared statements for database interactions. Regularly test the application using automated SQL injection tools.  |
| Exploitability | Weak or misconfigured AWS S3 bucket permissions exposing sensitive documents. | Leakage of confidential user data and potential legal ramifications for mishandling sensitive information. | Review and strengthen S3 bucket policies to restrict access. Use AWS Identity and Access Management (IAM) roles to control access to resources.  |
| Exploitability | Exploitation of insecure code in AWS Lambda functions leading to data exfiltration. | Attackers could gain access to sensitive data processed by the serverless functions and use it for malicious purposes. | Employ the principle of least privilege for roles and permissions. Regularly review and update Lambda code with security in mind.  |
| Exploitability | Man-in-the-Middle (MitM) attacks due to improper use of HTTPS/TLS for data in transit. | Sensitive data such as authentication tokens and personal information can be intercepted and altered by an attacker. | Enforce HTTPS across all routes and implement HSTS (HTTP Strict Transport Security). Use properly configured TLS certificates.  |
| Affected Users | Phishing attacks targeting users and exploiting the absence of email domain security. | Users may fall victim to phishing attempts, leading to credential theft and unauthorized access to their banking accounts. | Implement email authentication protocols such as SPF, DKIM and DMARC. Educate users on recognizing and reporting phishing scams.  |
| Affected Users | Account takeover via weak or compromised Multi-Factor Authentication (MFA) mechanisms. | An attacker can gain full access to user accounts, exposing all sensitive data and performing unauthorized transactions. | Utilize hardware-based tokens for MFA and ensure robust implementation of time-based one-time passwords (TOTP). Regularly audit and test MFA systems.  |
| Affected Users | Data leakage due to insufficient data encryption at rest. | Exposure of sensitive data leads to privacy violations, legal consequences, and loss of trust from users. | Ensure all sensitive data is encrypted using strong encryption standards such as AES-256. Regularly review and rotate encryption keys.  |
| Discoverability | Sensitive information exposed through verbose error messages. | Attackers can gain insights into the application’s inner workings, making it easier to find and exploit vulnerabilities. | Implement user-friendly yet generic error messages and log detailed error information securely for internal use.  |
| Discoverability | Public exposure of debug information and developer comments in the source code. | Attackers can leverage exposed information to discover and exploit vulnerabilities within the application. | Ensure all debug information and comments are removed from the production code. Automate static code analysis to catch such instances before deployment.  |
| Discoverability | Unrestricted access to sensitive endpoints due to poor API security. | Attackers can discover and exploit unsecured endpoints to gain access to confidential data and functionality. | Use API gateways to manage and secure endpoints. Implement proper authentication, authorization, and rate limiting for APIs.  |


## Suggestions Summary

- Implement stricter password policies and enforce regular password changes.
- Introduce Privileged Access Management (PAM) to limit admin access to sensitive areas.
- Utilize AWS Shield and AWS CloudFront to mitigate DDoS attacks.
- Follow regular patch management practices for all components of the technology stack.
- Implement a Content Security Policy (CSP) and use security headers.
- Utilize nonce values and timestamps in OAuth token exchanges.
- Employ parameterized queries and prepared statements.
- Review and strengthen S3 bucket policies to restrict access.
- Employ the principle of least privilege for roles and permissions.
- Enforce HTTPS across all routes and implement HSTS.
- Implement email authentication protocols such as SPF, DKIM and DMARC.
- Utilize hardware-based tokens for MFA and ensure robust implementation of TOTP.
- Ensure all sensitive data is encrypted using strong encryption standards.
- Implement user-friendly yet generic error messages, logging detailed error information securely.
- Ensure all debug information and comments are removed from the production code.
- Use API gateways to manage and secure endpoints, ensuring proper authentication, authorization, and rate limiting.
