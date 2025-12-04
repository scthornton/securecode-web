# SecureCode v2.0 - Complete Dataset Generation Plan
## Roadmap from 70 Examples → 1,000 Examples

**Created**: December 1, 2025
**Current Progress**: 70/1,000 examples (7%)
**Target**: 1,000 comprehensive security training examples
**Estimated Timeline**: ~90 batches × 1 hour = ~90 hours

---

## Overview

This document provides a complete roadmap for scaling SecureCode v2.0 from the current 70 injection examples to a comprehensive 1,000-example dataset covering all OWASP Top 10 2021 categories plus modern AI/ML security threats.

---

## Current Status (December 1, 2025)

✅ **Completed**: 70 injection examples across 7 batches (100% pass rate)
🔄 **In Progress**: Injection category expansion (70/140 complete - 50%)
⏳ **Pending**: 9 additional OWASP categories + AI/ML security

---

## Phase 1: Complete Injection Category (70 → 140 examples)
### Timeline: 7 batches × 1 hour = ~7 hours

### Batch 009: Template Injection (SSTI) Part 1 (10 examples)
**Focus**: Server-Side Template Injection vulnerabilities

| Example | Language/Framework | Technique |
|---------|-------------------|-----------|
| ssti-000001 | Python/Jinja2 | Basic template injection to RCE |
| ssti-000002 | PHP/Twig | Template sandbox escape |
| ssti-000003 | Java/FreeMarker | ObjectConstructor exploitation |
| ssti-000004 | Ruby/ERB | ERB template injection |
| ssti-000005 | JavaScript/Handlebars | Prototype pollution via templates |
| ssti-000006 | Python/Mako | Mako template injection |
| ssti-000007 | PHP/Smarty | Smarty template injection |
| ssti-000008 | Java/Velocity | Velocity template injection |
| ssti-000009 | Python/Tornado | Tornado template injection |
| ssti-000010 | Go/text/template | Go template injection |

**Security Patterns**:
- Template sandboxing
- Input validation before template rendering
- Safe template context objects
- Allowlisting template variables

---

### Batch 010: SQL Injection Advanced (10 examples)
**Focus**: Advanced SQL injection techniques and WAF bypass

| Example | Language | Technique |
|---------|----------|-----------|
| sql-injection-000021 | Python | UNION-based injection (data extraction) |
| sql-injection-000022 | PHP | Error-based injection (information disclosure) |
| sql-injection-000023 | Java | Out-of-band (OOB) injection (DNS exfiltration) |
| sql-injection-000024 | JavaScript | Time-based blind injection (boolean inference) |
| sql-injection-000025 | Go | WAF bypass techniques (encoding, comments) |
| sql-injection-000026 | C# | Polyglot SQL injection payloads |
| sql-injection-000027 | Python | Truncation-based injection |
| sql-injection-000028 | PHP | SQL injection in stored procedures |
| sql-injection-000029 | Java | SQL injection via XML/JSON functions |
| sql-injection-000030 | Ruby | GraphQL injection (GQL) |

**Security Patterns**:
- Comprehensive input validation
- Query complexity limits
- Rate limiting for blind injection prevention
- Error message sanitization

---

### Batch 011: XSS Expansion Part 2 (10 examples)
**Focus**: Advanced XSS techniques and modern contexts

| Example | Language/Context | Technique |
|---------|------------------|-----------|
| xss-000021 | JavaScript | CSP bypass (nonce reuse, JSONP) |
| xss-000022 | JavaScript | XSS in JSON contexts |
| xss-000023 | JavaScript | SVG/XML-based XSS |
| xss-000024 | Swift/iOS | XSS in mobile WebViews |
| xss-000025 | Kotlin/Android | WebView XSS exploitation |
| xss-000026 | JavaScript | Self-XSS to stored XSS escalation |
| xss-000027 | Python | XSS via markdown renderers |
| xss-000028 | JavaScript | XSS in rich email clients |
| xss-000029 | React Native | XSS in hybrid mobile apps |
| xss-000030 | JavaScript | DOM clobbering attacks |

**Security Patterns**:
- Strict CSP policies
- Context-aware output encoding
- WebView security configurations
- Markdown sanitization libraries

---

### Batch 012: NoSQL + Command Injection Advanced (10 examples)
**Focus**: Advanced techniques for NoSQL and command injection

**NoSQL Advanced (5 examples)**:
| Example | Database | Technique |
|---------|----------|-----------|
| nosql-injection-000026 | MongoDB | JavaScript injection in $where |
| nosql-injection-000027 | MongoDB | Aggregation pipeline injection |
| nosql-injection-000028 | MongoDB | Blind NoSQL injection (boolean-based) |
| nosql-injection-000029 | Redis | Time-based NoSQL injection |
| nosql-injection-000030 | Elasticsearch | Script injection via Painless |

**Command Injection Advanced (5 examples)**:
| Example | Language | Technique |
|---------|----------|-----------|
| command-injection-000026 | Python | DNS exfiltration via command injection |
| command-injection-000027 | Java | Blind command injection detection |
| command-injection-000028 | JavaScript | Command injection in API endpoints |
| command-injection-000029 | Go | CRLF injection |
| command-injection-000030 | PHP | LDAP command injection |

---

### Batch 013: XML/XXE Injection (10 examples)
**Focus**: XML External Entity injection attacks

| Example | Language | Technique |
|---------|----------|-----------|
| xxe-000001 | Java | Basic XXE file disclosure |
| xxe-000002 | Python | XXE SSRF attacks |
| xxe-000003 | PHP | Blind XXE with OOB |
| xxe-000004 | C# | XXE in SOAP web services |
| xxe-000005 | Java | XXE in document parsers (DOCX) |
| xxe-000006 | Python | XXE in XML-RPC |
| xxe-000007 | Go | XXE prevention in Go |
| xxe-000008 | Java | XInclude attacks |
| xxe-000009 | PHP | XXE via SVG upload |
| xxe-000010 | C# | Billion laughs attack (XML bomb) |

**Security Patterns**:
- Disable external entity processing
- Use safe XML parsers
- Input validation for XML data
- XML schema validation

---

### Batch 014: Template Injection + XSS Final (10 examples)
**Focus**: Completing SSTI and XSS coverage

**SSTI Part 2 (5 examples)**:
| Example | Framework | Technique |
|---------|-----------|-----------|
| ssti-000011 | Java/Velocity | Advanced Velocity exploitation |
| ssti-000012 | JavaScript/Pug | Pug template injection |
| ssti-000013 | Java/Thymeleaf | Thymeleaf expression injection |
| ssti-000014 | Go/html/template | Go template action injection |
| ssti-000015 | Python/Django | Django template filter bypass |

**XSS Part 3 (5 examples)**:
| Example | Context | Technique |
|---------|---------|-----------|
| xss-000031 | Python | XSS in PDF generators |
| xss-000032 | JavaScript | Polyglot XSS payloads |
| xss-000033 | JavaScript | XSS via file upload |
| xss-000034 | Go | XSS in server-side rendering |
| xss-000035 | Ruby | XSS in ActionMailer |

---

### Batch 015: SQL Injection + LDAP Final (10 examples)
**Focus**: Edge cases and LDAP injection

**SQL Edge Cases (5 examples)**:
| Example | Language | Technique |
|---------|----------|-----------|
| sql-injection-000031 | Python | ORDER BY clause injection |
| sql-injection-000032 | PHP | LIMIT clause injection |
| sql-injection-000033 | Java | JSON function injection |
| sql-injection-000034 | JavaScript | GQL (Graph Query Language) injection |
| sql-injection-000035 | Go | SQL injection in migrations |

**LDAP Injection (5 examples)**:
| Example | Language | Technique |
|---------|----------|-----------|
| ldap-000001 | Java | LDAP filter injection |
| ldap-000002 | Python | LDAP DN injection |
| ldap-000003 | PHP | Blind LDAP injection |
| ldap-000004 | C# | LDAP injection in Active Directory |
| ldap-000005 | Java | LDAP authentication bypass |

**✅ Injection Category Complete: 140/140 examples**

---

## Phase 2: Authentication Failures (A07) - 150 examples
### Timeline: 15 batches × 1 hour = ~15 hours

### Categories (150 total)

**Weak Password Policies (30 examples)**:
- Batch 016-018: Password complexity, storage, reset mechanisms

**Session Management (30 examples)**:
- Batch 019-021: Session fixation, hijacking, timeout issues

**JWT Vulnerabilities (25 examples)**:
- Batch 022-024: Algorithm confusion, weak secrets, key confusion

**OAuth/OpenID Vulnerabilities (25 examples)**:
- Batch 025-027: Redirect URI validation, CSRF, state parameter

**Multi-Factor Authentication (20 examples)**:
- Batch 028-029: MFA bypass, backup codes, TOTP vulnerabilities

**Authentication Bypass (20 examples)**:
- Batch 030-031: Logic flaws, race conditions, timing attacks

---

## Phase 3: Broken Access Control (A01) - 150 examples
### Timeline: 15 batches × 1 hour = ~15 hours

### Categories (150 total)

**IDOR (Insecure Direct Object References) (40 examples)**:
- Batch 032-035: Predictable IDs, UUID enumeration, GraphQL IDOR

**Vertical Privilege Escalation (30 examples)**:
- Batch 036-038: Admin access bypass, role manipulation

**Horizontal Privilege Escalation (30 examples)**:
- Batch 039-041: Cross-user data access, tenant isolation

**Path Traversal (25 examples)**:
- Batch 042-044: Directory traversal, file inclusion

**CORS Misconfiguration (15 examples)**:
- Batch 045-046: Credential leakage, origin validation

**Missing Function-Level Access Control (10 examples)**:
- Batch 047: API endpoint authorization

---

## Phase 4: Security Misconfiguration (A05) - 120 examples
### Timeline: 12 batches × 1 hour = ~12 hours

### Categories (120 total)

**Default Credentials (20 examples)**:
- Batch 048-049: Database, admin panels, cloud services

**Unnecessary Features Enabled (20 examples)**:
- Batch 050-051: Debug mode, directory listing, stack traces

**Missing Security Headers (20 examples)**:
- Batch 052-053: HSTS, X-Frame-Options, CSP

**Cloud Misconfigurations (30 examples)**:
- Batch 054-056: S3 buckets, IAM roles, security groups

**Container Security (20 examples)**:
- Batch 057-058: Docker misconfigurations, Kubernetes RBAC

**API Misconfigurations (10 examples)**:
- Batch 059: Rate limiting, HTTPS enforcement

---

## Phase 5: Cryptographic Failures (A02) - 100 examples
### Timeline: 10 batches × 1 hour = ~10 hours

### Categories (100 total)

**Weak Encryption (25 examples)**:
- Batch 060-062: DES, MD5, weak RSA keys

**Insecure Random Number Generation (20 examples)**:
- Batch 063-064: Predictable tokens, weak session IDs

**Improper Certificate Validation (20 examples)**:
- Batch 065-066: TLS/SSL bypass, certificate pinning

**Sensitive Data Exposure (20 examples)**:
- Batch 067-068: Plaintext passwords, PII leakage

**Key Management Issues (15 examples)**:
- Batch 069: Hardcoded keys, insecure storage

---

## Phase 6: Insecure Design (A04) - 80 examples
### Timeline: 8 batches × 1 hour = ~8 hours

### Categories (80 total)

**Business Logic Flaws (30 examples)**:
- Batch 070-072: Race conditions, integer overflow, logic bypass

**Insufficient Rate Limiting (20 examples)**:
- Batch 073-074: Brute force, scraping, API abuse

**Missing Security Controls (20 examples)**:
- Batch 075-076: No input validation, missing authorization

**Design-Level Vulnerabilities (10 examples)**:
- Batch 077: Architectural flaws, insecure workflows

---

## Phase 7: Vulnerable Components (A06) - 80 examples
### Timeline: 8 batches × 1 hour = ~8 hours

### Categories (80 total)

**Outdated Dependencies (30 examples)**:
- Batch 078-080: npm, pip, Maven vulnerabilities

**Known CVEs (30 examples)**:
- Batch 081-083: Log4Shell, Spring4Shell, Struts

**Supply Chain Attacks (20 examples)**:
- Batch 084-085: Dependency confusion, typosquatting

---

## Phase 8: Software/Data Integrity Failures (A08) - 80 examples
### Timeline: 8 batches × 1 hour = ~8 hours

### Categories (80 total)

**Insecure Deserialization (30 examples)**:
- Batch 086-088: Java, Python pickle, PHP unserialize

**Insufficient Integrity Verification (25 examples)**:
- Batch 089-091: Code signing, checksums, CI/CD integrity

**Insecure CI/CD Pipelines (25 examples)**:
- Batch 092-094: Pipeline injection, secrets in logs

---

## Phase 9: Logging/Monitoring Failures (A09) - 60 examples
### Timeline: 6 batches × 1 hour = ~6 hours

### Categories (60 total)

**Insufficient Logging (20 examples)**:
- Batch 095-096: Missing audit logs, incomplete traces

**Log Injection (20 examples)**:
- Batch 097-098: CRLF, log forging

**Missing Monitoring/Alerting (20 examples)**:
- Batch 099-100: No intrusion detection, delayed response

---

## Phase 10: Server-Side Request Forgery (A10) - 50 examples
### Timeline: 5 batches × 1 hour = ~5 hours

### Categories (50 total)

**Basic SSRF (15 examples)**:
- Batch 101-102: Internal service access, cloud metadata

**Blind SSRF (15 examples)**:
- Batch 103: DNS exfiltration, time-based detection

**SSRF in Cloud Environments (20 examples)**:
- Batch 104-105: AWS metadata, GCP metadata, Azure IMDS

---

## Phase 11: AI/ML Security Threats - 150 examples
### Timeline: 15 batches × 1 hour = ~15 hours

### Categories (150 total)

**Prompt Injection Attacks (40 examples)**:
- Batch 106-109: Direct injection, indirect injection, jailbreaks

**Model Extraction/Inversion (30 examples)**:
- Batch 110-112: Model stealing, membership inference

**Data Poisoning (25 examples)**:
- Batch 113-115: Training data manipulation, backdoors

**Adversarial Examples (25 examples)**:
- Batch 116-118: Image adversarial attacks, text perturbations

**RAG Poisoning (20 examples)**:
- Batch 119-120: Knowledge base manipulation, retrieval attacks

**AI Supply Chain (10 examples)**:
- Batch 121: Model provenance, poisoned pretrained models

---

## Summary: Complete Dataset Breakdown

| OWASP Category | Examples | Batches | Est. Hours |
|----------------|----------|---------|------------|
| **A03: Injection** | 140 | 15 (7 done) | 15 (7 done) |
| A07: Authentication | 150 | 15 | 15 |
| A01: Access Control | 150 | 15 | 15 |
| A05: Misconfiguration | 120 | 12 | 12 |
| A02: Cryptographic | 100 | 10 | 10 |
| A04: Insecure Design | 80 | 8 | 8 |
| A06: Vulnerable Components | 80 | 8 | 8 |
| A08: Data Integrity | 80 | 8 | 8 |
| A09: Logging/Monitoring | 60 | 6 | 6 |
| A10: SSRF | 50 | 5 | 5 |
| **Subtotal OWASP** | **870** | **87** | **87** |
| AI/ML Security | 150 | 15 | 15 |
| **TOTAL** | **1,020** | **102** | **102** |

*Note: Target is 1,000; slight overage provides flexibility for adjustments*

---

## Estimated Timeline

### Conservative Estimate (1 batch/day, 5 days/week)
- **Remaining batches**: 95 (102 total - 7 complete)
- **Timeline**: ~19 weeks (~5 months)
- **Completion Date**: ~May 2026

### Aggressive Estimate (2-3 batches/day)
- **Timeline**: ~6-8 weeks
- **Completion Date**: ~January 2026

### Realistic Target (1.5 batches/day average)
- **Timeline**: ~10-12 weeks (~3 months)
- **Completion Date**: ~March 2026

---

## Quality Assurance Strategy

### Per-Batch Validation
- Run `validate_all_batches.py` after each batch
- Fix any validation failures immediately
- Maintain 90%+ pass rate target (100% ideal)

### Milestone Reviews
- Full validation at 25%, 50%, 75%, 100% completion
- Manual security review of 10% sample
- Language distribution check
- Real-world context audit

### Continuous Improvement
- Update generator templates based on lessons learned
- Refine validation patterns (reduce false positives)
- Expand CVE database for recent incidents
- Improve example diversity

---

## Resource Requirements

### Development Environment
- Python 3.8+, Node.js 16+, Java 11+, Go 1.18+, etc.
- jsonschema, pyyaml, language-specific compilers/interpreters
- ~10 GB disk space for full dataset

### Time Investment
- **Generation**: ~100 hours (1 hour per batch)
- **Validation**: ~20 hours (fixing issues, manual reviews)
- **Documentation**: ~10 hours (updating reports, READMEs)
- **Total**: ~130 hours

### Team Size
- **Solo developer**: 3-6 months (part-time)
- **2-3 developers**: 1-2 months (full-time)

---

## Success Metrics

### Quantitative
- ✅ 1,000 examples generated
- ✅ 90%+ validation pass rate
- ✅ 11+ programming languages
- ✅ 100% 4-turn conversations
- ✅ Zero encoding errors
- ✅ <5% syntax errors (excluding validator limitations)

### Qualitative
- ✅ Production-ready code examples
- ✅ Real-world incident references (70%+)
- ✅ Progressive learning (vulnerable → secure → advanced)
- ✅ Attack demonstrations included
- ✅ Comprehensive security explanations

---

## Risk Mitigation

### Risk: Quality Degradation at Scale
**Mitigation**: Mandatory validation after each batch, periodic manual reviews

### Risk: Validator Limitations
**Mitigation**: Accept known limitations (TypeScript), focus on code correctness over tool compliance

### Risk: Scope Creep
**Mitigation**: Stick to defined batch structure, resist adding "just one more example"

### Risk: Burnout
**Mitigation**: Take breaks between phases, celebrate milestones, vary example types

---

## Next Steps (Immediate)

1. **Complete Batch 009** (SSTI Part 1) - 10 examples
2. **Validate and document** results
3. **Continue with Batch 010-015** to finish injection category
4. **Celebrate 140 injection examples milestone**
5. **Begin Phase 2** (Authentication Failures)

---

**Plan Status**: READY TO EXECUTE 🚀
**Next Batch**: Batch 009 (SSTI Part 1)
**Target Completion**: Q1-Q2 2026

---

**Last Updated**: December 1, 2025
**Next Review**: After Batch 015 (140 injection examples complete)
