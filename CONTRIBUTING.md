# Contributing to SecureCode

SecureCode aims to be an **enterprise-grade, production-ready secure coding dataset**.
The goal is that users can **extend** it – not fix basic issues. Please follow the guidelines below.

---

## Core Principles

1. **Real-World Grounding**
   - Every example must be tied to a real incident, CVE, or a realistic composite scenario.
   - Prefer:
     - Named breaches
     - Public CVEs
     - Well-documented incident patterns
   - If no CVE exists, document clearly in `business_impact` and set `cve` to `null` or `"N/A"`.

2. **Four-Turn Conversation Standard**

All examples must follow this exact 4-turn pattern:

1. **Turn 1 – User (human)**
   User asks for code / feature / design.

2. **Turn 2 – Assistant (model)**
   - Include **vulnerable implementation**.
   - Include **secure implementation** (fixed code).
   - Clearly separate the two in prose and code blocks.

3. **Turn 3 – User (human)**
   - Escalates or asks for an advanced scenario (performance, scale, extra features, etc.).
   - This turn often sets up deeper design or architecture risks.

4. **Turn 4 – Assistant (model)**
   - Provides **defense-in-depth** discussion.
   - Covers secure patterns, logging/monitoring, detection, and operational practices.

No 3-turn, 5-turn, or 8-turn variants. All conversations must be 4 turns.

---

## Required Metadata

Each example must include the following fields:

- `id` – Unique ID, following the project's ID scheme.
- `language` – One of:

  `python`, `javascript`, `java`, `go`, `php`, `csharp`, `typescript`, `ruby`, `rust`, `kotlin`

- `owasp_2021` – One or more OWASP Top 10 2021 categories, such as:
  - `A01: Broken Access Control`
  - `A02: Cryptographic Failures`
  - `A03: Injection`
  - `A04: Insecure Design`
  - `A05: Security Misconfiguration`
  - `A06: Vulnerable and Outdated Components`
  - `A07: Identification and Authentication Failures`
  - `A08: Software and Data Integrity Failures`
  - `A09: Security Logging and Monitoring Failures`
  - `A10: Server-Side Request Forgery (SSRF)`
  - `AI/ML Security` (for ML-specific threats)

- `technique` – A normalized technique name (see "Technique Naming" below).
- `severity` – One of: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` (see severity guidance).
- `business_impact` – Short description of the real impact (e.g., "Account takeover", "Data exfiltration of customer PII").
- `year` – Year of the incident or representative time period.
- `cve` – CVE identifier if one exists; otherwise `null` / `"N/A"`.

Optional but encouraged:

- `framework` / `tags` – e.g., `["django"]`, `["express"]`, `["kubernetes"]`, `["react"]`.

---

## Technique Naming

Use clear, normalized technique names. Examples:

- `SQL Injection` (not `SQLi` or `SQL-injection`)
- `Cross-Site Scripting (XSS)`
- `Cross-Site Request Forgery (CSRF)`
- `Server-Side Request Forgery (SSRF)`
- `Authentication Bypass`
- `Insecure Direct Object Reference (IDOR)`
- `Command Injection`
- `Path Traversal`
- `Deserialization Vulnerability`
- `RAG Prompt Injection`
- `Model Extraction`
- `Supply Chain Compromise`

When adding new techniques:

- Use **Title Case**.
- Prefer full names with abbreviations in parentheses when helpful.
- Avoid one-off abbreviations that are unclear to readers.

---

## Severity Guidance

Use these rough rules when assigning `severity`:

- **CRITICAL**
  - Remote code execution
  - Direct data exfiltration of sensitive data at scale
  - Full account takeover with no mitigation
  - Internet-exposed bugs with trivial exploitation

- **HIGH**
  - Auth/Z flaws limited to some tenants/users
  - Data exposure requiring some preconditions or chaining
  - Attacks with strong impact but some friction

- **MEDIUM**
  - Limited impact, difficult exploitation, or strong preconditions
  - Misconfigurations that are serious but constrained in scope

- **LOW**
  - Nuisance-level issues
  - Very constrained local impact
  - Purely informational issues that still have some security relevance

If in doubt, default to **HIGH** instead of CRITICAL, and explain your reasoning in the `business_impact`.

---

## Code Quality Expectations

- Code should be **syntactically valid** for the given language or clearly marked as a **partial snippet**.
- Use realistic imports and libraries.
- Vulnerable and secure implementations should both:
  - Be understandable
  - Reflect how real systems are actually built in that ecosystem
- Prefer including:
  - Input validation
  - Error handling
  - Logging/monitoring hooks
  - Comments where appropriate

If your example requires a specific framework or dependency (e.g., `Express`, `Spring Boot`, `Django`, `github.com/lib/pq`), mention it in the text and/or tags.

---

## Operational Completeness

Every example should think like a security engineer, not just a coder:

- Include **logging** for relevant security events.
- Mention how issues would be **detected** (e.g., SIEM, alerts, anomaly detection).
- Consider **least privilege**, **rate limiting**, and **defense-in-depth** in the Turn 4 explanation.
- Where relevant, tie detection to:
  - IPs / locations
  - User IDs / sessions
  - API keys / service accounts

---

## OWASP & Coverage Balance

We maintain a roughly balanced distribution across OWASP Top 10 2021 categories.

When adding new examples:

- Prefer underrepresented categories (check current README stats).
- AI/ML and SSRF examples are especially encouraged.
- Do not spam a single category without checking coverage first.

---

## Process for Adding a New Example

1. **Pick a real incident or clear composite scenario.**
2. **Design a 4-turn conversation** following the standard structure.
3. **Write vulnerable and secure code** that is realistic and syntactically correct (or clearly marked as snippet).
4. **Fill all required metadata fields**.
5. **Run validation scripts** (JSON, IDs, basic syntax where applicable).
6. **Submit a PR** with:
   - New example(s)
   - Updated `metadata.json` if needed
   - Any updated stats in README if you materially change distributions

---

By following these guidelines, you help keep SecureCode **clean, trustworthy, and truly production-ready**, so the community can build on it confidently instead of quietly fixing foundational issues.
