# OWASP Top 10:2021 - Complete Documentation

**Release Date**: Originally 24 September 2021, v1.1 released 13 July 2025
**Status**: Current Production Version

---

## Table of Contents

1. [Introduction](#introduction)
2. [Complete Category List](#complete-category-list)
3. [Detailed Category Descriptions](#detailed-category-descriptions)
4. [Methodology](#methodology)
5. [How to Use the OWASP Top 10](#how-to-use)
6. [How to Start an AppSec Program](#how-to-start-appsec)

---

## Introduction

Welcome to the OWASP Top 10:2021 documentation.

The OWASP Top 10 is a standard awareness document for developers and web application security. It represents a broad consensus about the most critical security risks to web applications.

### Lead Authors

- Andrew van der Stock (twitter: @vanderaj)
- Brian Glas (twitter: @infosecdad)
- Neil Smithline (twitter: @appsecneil)
- Torsten Gigler (twitter: @torsten_tweet)

### What's Changed in the Top 10 for 2021

There are three new categories, four categories with naming and scoping changes, and some consolidation in the Top 10 for 2021.

**Three New Categories:**
- **A04:2021 - Insecure Design** - New category focused on design flaws
- **A08:2021 - Software and Data Integrity Failures** - New category focused on integrity assumptions
- **A10:2021 - Server-Side Request Forgery (SSRF)** - Added from community survey (#1)

**Four Categories with Changes:**
- **A02:2021 - Cryptographic Failures** (was "Sensitive Data Exposure")
- **A05:2021 - Security Misconfiguration** (now includes XXE)
- **A07:2021 - Identification and Authentication Failures** (was "Broken Authentication")
- **A09:2021 - Security Logging and Monitoring Failures** (was "Insufficient Logging & Monitoring")

---

## Complete Category List (2021)

1. **A01:2021 - Broken Access Control** (maintained #1 position)
2. **A02:2021 - Cryptographic Failures** (was #2 in 2017 as "Sensitive Data Exposure")
3. **A03:2021 - Injection** (down from #1 in 2017)
4. **A04:2021 - Insecure Design** (NEW for 2021)
5. **A05:2021 - Security Misconfiguration** (up from #6 in 2017)
6. **A06:2021 - Vulnerable and Outdated Components** (up from #9 in 2017)
7. **A07:2021 - Identification and Authentication Failures** (was #2 in 2017)
8. **A08:2021 - Software and Data Integrity Failures** (NEW for 2021)
9. **A09:2021 - Security Logging and Monitoring Failures** (up from #10 in 2017)
10. **A10:2021 - Server-Side Request Forgery (SSRF)** (NEW for 2021)

---

## Detailed Category Descriptions

### A01:2021 - Broken Access Control

**Position**: #1 (maintained from 2017 #5)

#### Factors
| CWEs Mapped | Max Incidence Rate | Avg Incidence Rate | Avg Weighted Exploit | Avg Weighted Impact | Max Coverage | Avg Coverage | Total Occurrences | Total CVEs |
|---|---|---|---|---|---|---|---|---|
| 34 | 55.97% | 3.81% | 6.92 | 5.93 | 94.55% | 47.72% | 318,487 | 19,013 |

#### Overview
Broken Access Control moves up from the fifth position to #1. 94% of applications were tested for some form of access control with an average incidence rate of 3.81%, and has the most occurrences in the contributed dataset with over 318k. Notable CWEs include:
- CWE-200: Exposure of Sensitive Information to an Unauthorized Actor
- CWE-201: Insertion of Sensitive Information Into Sent Data
- CWE-352: Cross-Site Request Forgery (CSRF)

#### Description
Access control enforces policy such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized information disclosure, modification, or destruction of all data or performing a business function outside the user's limits. Common access control vulnerabilities include:

- Violation of the principle of least privilege or deny by default
- Bypassing access control checks by modifying the URL, internal application state, or HTML page
- Permitting viewing or editing someone else's account by providing its unique identifier (insecure direct object references)
- Accessing API with missing access controls for POST, PUT and DELETE
- Elevation of privilege (acting as a user without being logged in or acting as an admin when logged in as a user)
- Metadata manipulation, such as replaying or tampering with JWT access control token
- CORS misconfiguration allows API access from unauthorized/untrusted origins
- Force browsing to authenticated pages as an unauthenticated user

#### How to Prevent
Access control is only effective in trusted server-side code or server-less API, where the attacker cannot modify the access control check or metadata.

- Except for public resources, deny by default
- Implement access control mechanisms once and re-use them throughout the application, including minimizing Cross-Origin Resource Sharing (CORS) usage
- Model access controls should enforce record ownership rather than accepting that the user can create, read, update, or delete any record
- Unique application business limit requirements should be enforced by domain models
- Disable web server directory listing and ensure file metadata and backup files are not present within web roots
- Log access control failures, alert admins when appropriate
- Rate limit API and controller access to minimize the harm from automated attack tooling
- Stateful session identifiers should be invalidated on the server after logout

#### Example Attack Scenarios

**Scenario #1**: Application uses unverified data in SQL call accessing account information:
```
pstmt.setString(1, request.getParameter("acct"));
ResultSet results = pstmt.executeQuery();
```
Attacker modifies 'acct' parameter in browser to send whatever account number they want. If not properly verified, attacker can access any user's account.
```
https://example.com/app/accountInfo?acct=notmyacct
```

**Scenario #2**: Attacker force browses to target URLs. Admin rights required for access to admin page.
```
https://example.com/app/getappInfo
https://example.com/app/admin_getappInfo
```
If unauthenticated user can access either page, it's a flaw. If a non-admin can access the admin page, this is a flaw.

#### List of Mapped CWEs
CWE-22, CWE-23, CWE-35, CWE-59, CWE-200, CWE-201, CWE-219, CWE-264, CWE-275, CWE-276, CWE-284, CWE-285, CWE-352, CWE-359, CWE-377, CWE-402, CWE-425, CWE-441, CWE-497, CWE-538, CWE-540, CWE-548, CWE-552, CWE-566, CWE-601, CWE-639, CWE-651, CWE-668, CWE-706, CWE-862, CWE-863, CWE-913, CWE-922, CWE-1275

---

### A02:2021 - Cryptographic Failures

**Position**: #2 (was #3 in 2017 as "Sensitive Data Exposure")

#### Factors
| CWEs Mapped | Max Incidence Rate | Avg Incidence Rate | Avg Weighted Exploit | Avg Weighted Impact | Max Coverage | Avg Coverage | Total Occurrences | Total CVEs |
|---|---|---|---|---|---|---|---|---|
| 29 | 46.44% | 4.49% | 7.29 | 6.81 | 79.33% | 34.85% | 233,788 | 3,075 |

#### Overview
Previously known as "Sensitive Data Exposure" (broad symptom rather than root cause). The renewed focus on failures related to cryptography often leads to sensitive data exposure or system compromise. Notable CWEs:
- CWE-259: Use of Hard-coded Password
- CWE-327: Broken or Risky Cryptographic Algorithm
- CWE-331: Insufficient Entropy

#### Description
First, determine protection needs of data in transit and at rest. Passwords, credit card numbers, health records, personal information, and business secrets require extra protection, particularly if that data falls under privacy laws (e.g., EU's GDPR), regulations (e.g., financial data protection like PCI DSS).

You are vulnerable if:
- Data transmitted in clear text (HTTP, SMTP, FTP protocols)
- Old or weak cryptographic algorithms or protocols used by default or in older code
- Default crypto keys in use, weak crypto keys generated or re-used
- Encryption not enforced (missing security directives or headers)
- Received server certificate and trust chain not properly validated
- Passwords not using strong adaptive and salted hashing functions

#### How to Prevent
At minimum:
- Classify data processed, stored, or transmitted by application
- Don't store sensitive data unnecessarily; discard ASAP
- Ensure all sensitive data is encrypted at rest
- Ensure up-to-date and strong standard algorithms, protocols, and keys; use proper key management
- Encrypt all data in transit with secure protocols (TLS with PFS ciphers, cipher prioritization by server, secure parameters)
- Disable caching for responses containing sensitive data
- Apply required security controls as per data classification
- Store passwords using strong adaptive and salted hashing functions (Argon2, scrypt, bcrypt, PBKDF2)
- Initialization vectors must be chosen appropriate for the mode of operation
- Verify independently the effectiveness of configuration and settings

#### Example Attack Scenarios

**Scenario #1**: Application encrypts credit card numbers using automatic database encryption. Data is decrypted automatically when retrieved, allowing SQL injection flaw to retrieve credit card numbers in clear text.

**Scenario #2**: Site doesn't use or enforce TLS for all pages or supports weak encryption. Attacker monitors network traffic, downgrades connections from HTTPS to HTTP, intercepts requests, steals session cookie. Attacker replays cookie, hijacks authenticated session, accesses/modifies user's private data.

**Scenario #3**: Password database uses unsalted or simple hashes. File upload flaw allows attacker to retrieve password database. All unsalted hashes can be exposed with rainbow table of pre-calculated hashes. Hashes generated by simple or fast hash functions may be cracked by GPUs even if salted.

#### List of Mapped CWEs
CWE-261, CWE-296, CWE-310, CWE-319, CWE-321, CWE-322, CWE-323, CWE-324, CWE-325, CWE-326, CWE-327, CWE-328, CWE-329, CWE-330, CWE-331, CWE-335, CWE-336, CWE-337, CWE-338, CWE-340, CWE-347, CWE-523, CWE-720, CWE-757, CWE-759, CWE-760, CWE-780, CWE-818, CWE-916

---

### A03:2021 - Injection

**Position**: #3 (down from #1 in 2017)

#### Factors
| CWEs Mapped | Max Incidence Rate | Avg Incidence Rate | Avg Weighted Exploit | Avg Weighted Impact | Max Coverage | Avg Coverage | Total Occurrences | Total CVEs |
|---|---|---|---|---|---|---|---|---|
| 33 | 19.09% | 3.37% | 7.25 | 7.15 | 94.04% | 47.90% | 274,228 | 32,078 |

#### Overview
Injection slides down to third position. 94% of applications were tested for some form of injection with max incidence rate of 19%, average incidence rate of 3.37%, and 274k occurrences. Notable CWEs:
- CWE-79: Cross-site Scripting (XSS)
- CWE-89: SQL Injection
- CWE-73: External Control of File Name or Path

#### Description
An application is vulnerable when:
- User-supplied data not validated, filtered, or sanitized
- Dynamic queries or non-parameterized calls without context-aware escaping used directly
- Hostile data used within ORM search parameters to extract additional sensitive records
- Hostile data directly used or concatenated

Common injections: SQL, NoSQL, OS command, ORM, LDAP, Expression Language (EL), Object Graph Navigation Library (OGNL). Source code review is best method to detect injection vulnerabilities. Automated testing of all parameters, headers, URL, cookies, JSON, SOAP, XML data inputs strongly encouraged.

#### How to Prevent
Preventing injection requires keeping data separate from commands and queries:
- Preferred: use safe API avoiding interpreter entirely, provides parameterized interface, or migrate to ORMs
- Use positive server-side input validation (not complete defense)
- For residual dynamic queries, escape special characters using specific escape syntax
- Use LIMIT and other SQL controls within queries to prevent mass disclosure

**Note**: SQL structures (table names, column names) cannot be escaped; user-supplied structure names are dangerous.

#### Example Attack Scenarios

**Scenario #1**: Application uses untrusted data in vulnerable SQL call:
```
String query = "SELECT * FROM accounts WHERE custID='" + request.getParameter("id") + "'";
```

**Scenario #2**: Framework blind trust results in vulnerable queries (e.g., HQL):
```
Query HQLQuery = session.createQuery("FROM accounts WHERE custID='" + request.getParameter("id") + "'");
```

Attacker modifies 'id' parameter to send: `' UNION SLEEP(10);--`
```
http://example.com/app/accountView?id=' UNION SELECT SLEEP(10);--
```
Changes query meaning to return all records. More dangerous attacks could modify/delete data or invoke stored procedures.

#### List of Mapped CWEs
CWE-20, CWE-74, CWE-75, CWE-77, CWE-78, CWE-79, CWE-80, CWE-83, CWE-87, CWE-88, CWE-89, CWE-90, CWE-91, CWE-93, CWE-94, CWE-95, CWE-96, CWE-97, CWE-98, CWE-99, CWE-100, CWE-113, CWE-116, CWE-138, CWE-184, CWE-470, CWE-471, CWE-564, CWE-610, CWE-643, CWE-644, CWE-652, CWE-917

---

### A04:2021 - Insecure Design

**Position**: #4 (NEW for 2021)

#### Overview
New category for 2021 focusing on risks related to design flaws. Need more threat modeling, secure design patterns and principles, and reference architectures. Insecure design cannot be fixed by perfect implementation - needed security controls were never created to defend against specific attacks.

#### Description
Insecure design is a broad category representing different weaknesses, expressed as "missing or ineffective control design." Not the source for all other Top 10 risk categories. Difference between insecure design and insecure implementation:
- Design flaw: authentication control allowing 1,000 login attempts per minute (design issue)
- Implementation flaw: authentication implemented but rate limiting not applied (implementation issue)

We need:
- Secure development lifecycle with AppSec professionals
- Establish and use secure design patterns/paved road component library
- Use threat modeling for critical authentication, access control, business logic, key flows
- Integrate security language and controls into user stories
- Integrate plausibility checks at each tier (from frontend to backend)
- Write unit and integration tests to validate all critical flows resistant to threat model
- Segregate tier layers on system and network layers
- Segregate tenants robustly by design throughout all tiers
- Limit resource consumption by user or service

#### How to Prevent
- Establish and use secure development lifecycle with AppSec professionals
- Establish and use library of secure design patterns or paved road ready-to-use components
- Use threat modeling for critical authentication, access control, business logic, key flows
- Integrate security language and controls into user stories
- Integrate plausibility checks at each tier
- Write unit and integration tests to validate all critical flows resistant to threat model
- Segregate tier layers on system and network layers depending on exposure and protection needs
- Segregate tenants robustly by design throughout all tiers
- Limit resource consumption by user or service

#### Example Attack Scenarios

**Scenario #1**: Credential recovery workflow includes "questions and answers" defeated by OSINT. Code cannot defend against insecurely designed workflow.

**Scenario #2**: Cinema chain allows group booking discounts, capping max 15 attendees before requiring deposit. Attackers threat model flow, test if they can book 600 seats across all cinemas at once (few requests), causing massive loss of income.

**Scenario #3**: Retail chain's e-commerce website has no protection against bots run by scalpers buying high-end GPUs to resell. Creates terrible publicity and unhappy enthusiasts/retailers. Careful anti-bot design and domain logic rules (e.g., rapid purchases not appearing human, 1-5 minute delays) may identify inauthentic purchases and reject transactions.

---

### A05:2021 - Security Misconfiguration

**Position**: #5 (up from #6 in 2017)

#### Factors
| CWEs Mapped | Max Incidence Rate | Avg Incidence Rate | Avg Weighted Exploit | Avg Weighted Impact | Max Coverage | Avg Coverage | Total Occurrences | Total CVEs |
|---|---|---|---|---|---|---|---|---|
| 20 | 19.84% | 4.51% | 8.12 | 6.56 | 89.58% | 44.84% | 208,387 | 789 |

#### Overview
Moves up from #6; 90% of applications tested for misconfiguration with average incidence rate of 4.51%, over 208k occurrences. Notable shift into highly configurable software. Notable CWEs:
- CWE-16: Configuration
- CWE-611: Improper Restriction of XML External Entity Reference (XXE)

#### Description
Application might be vulnerable if:
- Missing appropriate security hardening across any application stack or improperly configured permissions on cloud services
- Unnecessary features enabled/installed
- Default accounts and passwords still enabled/unchanged
- Error handling reveals stack traces or overly informative error messages
- Latest security features disabled/not configured securely
- Security settings in application servers, frameworks, libraries, databases not set to secure values
- Server doesn't send security headers/directives or not set to secure values
- Software out of date or vulnerable

#### How to Prevent
Secure installation processes:
- Repeatable hardening process makes deploying another environment properly locked down fast/easy
- Minimal platform without unnecessary features, components, documentation, samples
- Task to review and update configurations appropriate to all security notes, updates, patches
- Segmented application architecture providing effective separation between components/tenants
- Sending security directives to clients (e.g., Security Headers)
- Automated process to verify effectiveness of configurations/settings in all environments

#### Example Attack Scenarios

**Scenario #1**: Application server with sample applications not removed. Sample apps have known flaws attackers use to compromise server. Admin console default install/passwords unchanged.

**Scenario #2**: Directory listing not disabled. Attacker discovers they can list directories, finds/downloads compiled Java classes, decompiles/reverse engineers code to view flaws, then finds serious access control flaw.

**Scenario #3**: Application server config allows detailed error messages (stack traces) returned. Exposes potentially sensitive info or underlying flaws (component versions known vulnerable).

**Scenario #4**: Cloud service provider has default sharing permissions open to Internet by other CSP users. Allows sensitive data stored within cloud storage to be accessed.

---

### A06:2021 - Vulnerable and Outdated Components

**Position**: #6 (up from #9 in 2017)

#### Factors
| CWEs Mapped | Max Incidence Rate | Avg Incidence Rate | Avg Weighted Exploit | Avg Weighted Impact | Max Coverage | Avg Coverage | Total Occurrences | Total CVEs |
|---|---|---|---|---|---|---|---|---|
| 3 | 27.96% | 8.77% | 5.00 | 5.00 | 51.78% | 22.47% | 30,457 | 0 |

#### Overview
Was #2 from Top 10 community survey but also had enough data. Known issue we struggle to test and assess risk. Only category not to have any CVEs mapped to included CWEs, so default exploits/impact weight of 5.0 used. Notable CWEs:
- CWE-1104: Use of Unmaintained Third-Party Components
- Two CWEs from Top 10 2013 and 2017

#### Description
You are likely vulnerable if:
- Don't know versions of all components (client-side and server-side), including nested dependencies
- Software vulnerable, unsupported, or out of date (OS, web/application server, DBMS, applications, APIs, components, runtime environments, libraries)
- Don't scan for vulnerabilities regularly and subscribe to security bulletins
- Don't fix or upgrade underlying platform, frameworks, dependencies in risk-based, timely fashion
- Software developers don't test compatibility of updated/upgraded/patched libraries
- Don't secure components' configurations

#### How to Prevent
Patch management process should:
- Remove unused dependencies, unnecessary features, components, files, documentation
- Continuously inventory versions of client-side and server-side components and dependencies using tools
- Continuously monitor sources like CVE and NVD for vulnerabilities
- Only obtain components from official sources over secure links; prefer signed packages
- Monitor for libraries/components unmaintained or not creating security patches
- Ensure ongoing plan for monitoring, triaging, applying updates for application/portfolio lifetime

#### Example Attack Scenarios

**Scenario #1**: Components run with same privileges as application, so flaws can result in serious impact. Example exploitable vulnerabilities:
- CVE-2017-5638, Struts 2 remote code execution enabling arbitrary code execution on server
- While IoT frequently difficult/impossible to patch, importance of patching can be great (e.g., biomedical devices)

Automated tools help attackers find unpatched/misconfigured systems (e.g., Shodan IoT search engine for Heartbleed vulnerability from April 2014).

---

### A07:2021 - Identification and Authentication Failures

**Position**: #7 (was #2 in 2017 as "Broken Authentication")

#### Overview
Previously "Broken Authentication," sliding down from second position. Now includes CWEs more related to identification failures. Still integral part of Top 10; increased availability of standardized frameworks helping.

#### Description
Confirmation of user's identity, authentication, and session management critical to protect against authentication-related attacks. May be authentication weaknesses if application:
- Permits automated attacks (credential stuffing - attacker has list of valid usernames/passwords)
- Permits brute force or other automated attacks
- Permits default, weak, or well-known passwords
- Uses weak/ineffective credential recovery/forgot-password processes
- Uses plain text, encrypted, or weakly hashed passwords data stores
- Has missing/ineffective multi-factor authentication
- Exposes session identifier in URL
- Reuses session identifier after successful login
- Doesn't correctly invalidate Session IDs (user sessions/authentication tokens not properly invalidated during logout/period of inactivity)

#### How to Prevent
- Implement multi-factor authentication where possible
- Do not ship or deploy with default credentials
- Implement weak password checks
- Align password length, complexity, rotation policies with guidelines
- Ensure registration, credential recovery, API pathways hardened against account enumeration
- Limit or increasingly delay failed login attempts; log all failures, alert administrators
- Use server-side, secure, built-in session manager generating new random session ID with high entropy after login
- Session identifiers should not be in URL, securely stored, invalidated after logout, idle, absolute timeouts

#### Example Attack Scenarios

**Scenario #1**: Credential stuffing (use of lists of known passwords) common attack. No automated threat or credential stuffing protections. Application can be used as password oracle to determine if credentials valid.

**Scenario #2**: Most authentication attacks due to continued use of passwords as sole factor. Best practices (password rotation, complexity requirements) viewed encouraging users to use/reuse weak passwords. Organizations recommended stop these practices per NIST 800-63 and use multi-factor authentication.

**Scenario #3**: Application session timeouts not set properly. User uses public computer, doesn't logout but closes browser tab. Attacker uses same browser hour later; user still authenticated.

---

### A08:2021 - Software and Data Integrity Failures

**Position**: #8 (NEW for 2021)

#### Overview
New category for 2021 focusing on making assumptions related to software updates, critical data, CI/CD pipelines without verifying integrity. One of highest weighted impacts from CVE/CVSS data. Notable CWEs:
- CWE-829: Inclusion of Functionality from Untrusted Control Sphere
- CWE-494: Download of Code Without Integrity Check
- CWE-502: Deserialization of Untrusted Data

#### Description
Software and data integrity failures relate to code and infrastructure that doesn't protect against integrity violations. Example: application relies on plugins, libraries, modules from untrusted sources, repositories, CDNs. Insecure CI/CD pipeline can introduce potential for unauthorized access, malicious code, or system compromise. Many applications now include auto-update functionality where updates downloaded without sufficient integrity verification applied to updates.

Attackers upload own updates distributed/run on all installations. Another example: objects/data encoded or serialized into structure attacker can see/modify vulnerable to insecure deserialization.

#### How to Prevent
- Use digital signatures or similar to verify software/data from expected source and not altered
- Ensure libraries and dependencies (npm, Maven) consuming trusted repositories
- Use software supply chain security tool (OWASP Dependency Check, OWASP CycloneDX) to verify components don't contain known vulnerabilities
- Ensure review process for code and configuration changes to minimize chance malicious code/configuration could be introduced
- Ensure CI/CD pipeline has proper segregation, configuration, access control to ensure integrity of code flowing through build/deploy processes
- Ensure unsigned/unencrypted serialized data not sent to untrusted clients without integrity check or digital signature

#### Example Attack Scenarios

**Scenario #1**: Update without signing. Attacker downloads firmware, extracts proprietary encoding algorithms, then builds malicious update sending to all installations via built-in update mechanism.

**Scenario #2**: SolarWinds malicious update affecting over 18,000 organizations. Nation-state actors compromised supply chain, trojanizing software update systems to distribute malware.

**Scenario #3**: Application uses React JavaScript library's CDN. CDN gets compromised, attacker injects malicious code into React library on CDN. All visiting applications would unknowingly execute malicious code.

---

### A09:2021 - Security Logging and Monitoring Failures

**Position**: #9 (was #10 in 2017 as "Insufficient Logging & Monitoring")

#### Overview
Previously "Insufficient Logging & Monitoring," added from Top 10 community survey (#3). Expanded to include more failure types, challenging to test, not well represented in CVE/CVSS data. Failures can directly impact visibility, incident alerting, forensics.

#### Description
Returning to OWASP Top 10 2021, this category helps detect, escalate, respond to active breaches. Without logging and monitoring, breaches cannot be detected. Insufficient logging, detection, monitoring, and active response occurs when:
- Auditable events (logins, failed logins, high-value transactions) not logged
- Warnings and errors generate no, inadequate, or unclear log messages
- Logs of applications and APIs not monitored for suspicious activity
- Logs only stored locally
- Appropriate alerting thresholds and response escalation processes not in place or effective
- Penetration testing and scans by dynamic application security testing (DAST) tools don't trigger alerts
- Application cannot detect, escalate, or alert for active attacks in real-time or near real-time

Vulnerable to information leakage by making logging and alerting events visible to user or attacker.

#### How to Prevent
Developers should implement some/all controls depending on application risk:
- Ensure all login, access control, server-side input validation failures logged with sufficient user context for suspicious/malicious accounts, held for time to allow delayed forensic analysis
- Ensure logs generated in format log management solutions can easily consume
- Ensure log data encoded correctly to prevent injections/attacks on logging or monitoring systems
- Ensure high-value transactions have audit trail with integrity controls
- DevSecOps teams should establish effective monitoring and alerting
- Establish or adopt incident response and recovery plan

#### Example Attack Scenarios

**Scenario #1**: Children's health plan provider website operator couldn't detect breach due to lack of monitoring/logging. External party informed after data breach, including over 3.5M children's PII.

**Scenario #2**: Major Indian airline had data breach involving 10+ years of personal data including passport and credit card data. Data breach occurred at third-party cloud hosting provider who notified airline of breach after some time.

**Scenario #3**: Major European airline suffered GDPR reportable breach. Breach reportedly caused by payment application security vulnerabilities exploited by attackers who harvested 400,000+ customer payment records. Airline fined £20 million by privacy regulator.

---

### A10:2021 - Server-Side Request Forgery (SSRF)

**Position**: #10 (NEW for 2021)

#### Overview
Added from Top 10 community survey (#1). Data shows relatively low incidence rate with above average testing coverage and above-average Exploit and Impact potential ratings. Represents scenario where security community members indicate importance even though not illustrated in data at this time.

#### Description
SSRF flaws occur whenever web application fetching remote resource without validating user-supplied URL. Allows attacker to coerce application to send crafted request to unexpected destination, even when protected by firewall, VPN, or another type of network access control list (ACL).

Modern web applications provide end-users with convenient features, fetching URL becoming common. As result, incidence of SSRF increasing. Also, severity of SSRF becoming higher due to cloud services and architecture complexity.

#### How to Prevent
Developers can prevent SSRF by implementing some/all defense-in-depth controls:

**From Network Layer:**
- Segment remote resource access functionality in separate networks
- Enforce "deny by default" firewall policies or network access control rules

**From Application Layer:**
- Sanitize and validate all client-supplied input data
- Enforce URL schema, port, and destination with positive allow list
- Do not send raw responses to clients
- Disable HTTP redirections
- Be aware of URL consistency to avoid attacks such as DNS rebinding and "time of check, time of use" (TOCTOU) race conditions

**Additional Measures:**
- Don't mitigate SSRF via use of deny list or regular expression
- Don't deploy relevant services on front systems (OpenID)
- For frontends with dedicated/separate networks, consider network encryption

#### Example Attack Scenarios

Attackers can use SSRF to attack systems protected behind web application firewalls, firewalls, or network ACLs using scenarios:

**Scenario #1**: Port scan internal servers. If network architecture unsegmented, attackers can map out internal networks and determine if ports open/closed on internal servers from connection results or elapsed time to connect/reject SSRF payload connections.

**Scenario #2**: Sensitive data exposure. Attackers can access local files (file:///) or internal services to gain sensitive information.

**Scenario #3**: Access metadata storage of cloud services. Most cloud providers have metadata storage (169.254.169.254). Attacker can read metadata to gain sensitive information.

**Scenario #4**: Compromise internal services. Attacker can abuse internal services to conduct further attacks (Remote Code Execution, Denial of Service).

---

## Methodology

### Data-Driven Approach

This Top 10 installment is more data-driven than ever but not blindly data-driven:
- Selected **8 of 10 categories** from contributed data
- Selected **2 categories** from Top 10 community survey

**Why community survey?**: Looking at contributed data = looking into past. AppSec researchers take time to find new vulnerabilities and test methods. Takes time to integrate tests into tools/processes. By time we can reliably test weakness at scale, years have passed.

### Data Collection Process

**Formalized at Open Security Summit 2017**:
- Published call for data through social media
- Listed data elements, structure, submission process
- Provided example files as templates on GitHub
- Worked with organizations to help with structure and CWE mapping

**Data Sources**:
- Testing vendors by trade
- Bug bounty vendors
- Organizations contributing internal testing data

**Analysis Process**:
- Load data together
- Run fundamental analysis of CWEs mapping to risk categories
- Document and publish all decisions for transparency

### Category Selection

1. Look at **8 categories with highest incidence rates**
2. Look at **Top 10 community survey results**
3. Select **top 2 votes not present in data** for other two places

### How Data is Used

**In 2017**: Selected categories by incidence rate, then ranked by team discussion based on decades of experience

**For 2021**: Use data for _Exploitability_ and _(Technical) Impact_ if possible:
- Downloaded OWASP Dependency Check
- Extracted CVSS Exploit and Impact scores
- Grouped by related CWEs
- Calculated weighted averages

### Data Factors

For each Top 10 category:
- **CWEs Mapped**: Number of CWEs mapped to category
- **Incidence Rate**: % of applications vulnerable to CWE from tested population
- **(Testing) Coverage**: % of applications tested by all organizations for given CWE
- **Weighted Exploit**: Exploit sub-score from CVSSv2/v3 assigned to CVEs mapped to CWEs (normalized, 10pt scale)
- **Weighted Impact**: Impact sub-score from CVSSv2/v3 assigned to CVEs mapped to CWEs (normalized, 10pt scale)
- **Total Occurrences**: Total applications found to have CWEs mapped to category
- **Total CVEs**: Total CVEs in NVD DB mapped to CWEs mapped to category

### Why Not Pure Statistical Data?

Results limited to what we can test for in automated fashion. AppSec professionals find stuff and see trends not yet in data. Takes time to:
1. Develop testing methodologies for vulnerability types
2. Automate tests
3. Run against large population

Everything we find looks back in past, might miss trends from last year not present in data.

### Why Incidence Rate Instead of Frequency?

**Three primary data sources**:
- **Tooling**: High-frequency finding generators
- **Human-assisted Tooling (HaT)**: High-frequency
- **Tool-assisted Human (TaH)**: Broader range but lower frequency

Using frequency, Tooling and HaT data would drown more accurate TaH data. **Incidence rate** asks: what % of application population had ≥1 instance of vulnerability type? Provides clearer view across multiple testing types.

### Data Contributors

Organizations that donated data for **over 500,000 applications**:
- AppSec Labs
- Cobalt.io
- Contrast Security
- GitLab
- HackerOne
- HCL Technologies
- Micro Focus
- PenTest-Tools
- Probely
- Sqreen
- Veracode
- WhiteHat (NTT)

---

## How to Use the OWASP Top 10 as a Standard

The OWASP Top 10 is primarily an **awareness document**. However, many organizations use it as de facto industry AppSec standard since 2003.

### Important Notes

If using OWASP Top 10 as coding or testing standard:
- Know it's the **bare minimum** and just a **starting point**
- Some risks are beyond scope of most testing forms (e.g., A04:2021-Insecure Design)
- Testing for effective logging/monitoring can only be done via interviews and incident response sampling

### Use Case Matrix

| Use Case | OWASP Top 10 2021 | OWASP ASVS |
|---|---|---|
| Awareness | Yes | - |
| Training | Entry level | Comprehensive |
| Design and architecture | Occasionally | Yes |
| Coding standard | Bare minimum | Yes |
| Secure Code review | Bare minimum | Yes |
| Peer review checklist | Bare minimum | Yes |
| Unit testing | Occasionally | Yes |
| Integration testing | Occasionally | Yes |
| Penetration testing | Bare minimum | Yes |
| Tool support | Bare minimum | Yes |
| Secure Supply Chain | Occasionally | Yes |

### Recommendations

Anyone wanting to adopt application security standard should use **OWASP Application Security Verification Standard (ASVS)**:
- Designed to be verifiable and tested
- Can be used in all parts of secure development lifecycle
- Only acceptable choice for tool vendors

**Note**: Tools cannot comprehensively detect, test, or protect against OWASP Top 10 due to nature of several risks (reference A04:2021-Insecure Design). OWASP discourages claims of full Top 10 coverage.

---

## How to Start an AppSec Program with the OWASP Top 10

Previously, OWASP Top 10 was never designed to be basis for AppSec program. However, essential to start somewhere for many organizations just starting out.

### Stage 1: Identify Gaps and Goals

Use **OWASP Software Assurance Maturity Model (SAMM)** to:
- Evaluate where you are now
- Identify gaps in governance, design, implementation, verification, operations
- Prioritize implementing/improving 15 OWASP SAMM security practices
- Plan improvements over 1-3 year period

### Stage 2: Plan for Paved Road Secure Development Lifecycle

**Paved Road Concept**: "The easiest way is also the most secure way"

Involves:
- Deep partnerships between development and security teams
- Enterprise-wide library of drop-in secured replacements
- Tooling to help see where improvements can be made
- Continuous improvement, measure, detect, replace insecure alternatives

### Stage 3: Implement Paved Road

Build with:
- Consent and direct involvement of relevant development/operations teams
- Alignment with business strategy
- Holistic exercise covering entire enterprise/application ecosystem

### Stage 4: Migrate Applications

- Add paved road detection tools
- Provide information to development teams
- Implement continuous integration checks
- Prevent insecure options from creeping into code
- Warnings should link to secure alternative

### Stage 5: Test Paved Road Effectiveness

- Ensure paved road components address OWASP Top 10 issues
- Continuously evaluate and improve security of components
- Communicate upgrades to consumers

### Stage 6: Build Mature AppSec Program

Don't stop at OWASP Top 10:
- Adopt Application Security Verification Standard
- Progressively add paved road components and tests for Level 1, 2, 3

### Going Beyond

All great AppSec programs include:
- **Conceptual integrity**: Security architecture, threat modeling
- **Automation and scale**: Automate deliverables, scripts, static code analysis tools
- **Culture**: Build out insecure design, eliminate technical debt, be part of development team
- **Continuous improvement**: If not working, stop doing it; measure, evaluate, improve

---

## Copyright and License

Copyright © 2003-2025 The OWASP® Foundation, Inc.

This document is released under the **Creative Commons Attribution Share-Alike 4.0 license**.

For any reuse or distribution, you must make it clear to others the license terms of this work.

---

**End of OWASP Top 10:2021 Documentation**
