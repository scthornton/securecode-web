# SecureCode v2.0 - Scaling Roadmap

**Date**: December 1, 2025
**Phase**: Injection Category - 57% Complete
**Target**: 140 Injection Examples (A03:2021-Injection) → 940 OWASP Top 10 → 1,000 Total

---

## 🎯 Scaling Objective

Scale from 80 validated injection examples (57% complete) to full OWASP Top 10 coverage (940 examples) plus AI/ML security threats (150 examples) for a total of 1,000 comprehensive security training examples.

---

## ✅ Injection Category - 57% Complete (80/140 examples)

### Completed Batches (8)

- **Batch 001**: SQL Injection (10 examples) ✅ 100% pass rate
- **Batch 002**: Command Injection (10 examples) ✅ 100% pass rate
- **Batch 003**: XSS (10 examples) ✅ 100% pass rate
- **Batch 005**: SQL Injection Expansion (10 examples) ✅ 100% pass rate
- **Batch 006**: NoSQL Injection (10 examples) ✅ 100% pass rate
- **Batch 007**: Command Injection Expansion (10 examples) ✅ 100% pass rate
- **Batch 008**: XSS Expansion Part 1 (10 examples) ✅ 100% pass rate
- **Batch 009**: Template Injection (SSTI) Part 1 (10 examples) ✅ 100% pass rate

**Quality Metrics Achieved:**
- **100% validation pass rate** (80/80 examples passing)
- 100% 4-turn conversations
- ~70% real-world CVE/incident context
- Zero critical syntax/encoding errors
- 11 programming languages covered
- Production-ready implementations

---

## 📋 Injection Category Breakdown (140 Total)

### A03:2021-Injection Subcategories

| Subcategory | Total Target | Completed | Remaining | Progress | Priority |
|-------------|--------------|-----------|-----------|----------|----------|
| **SQL Injection** | 35 | 20 | 15 | 57% | HIGH |
| **Command Injection** | 25 | 20 | 5 | 80% | HIGH |
| **XSS** | 35 | 20 | 15 | 57% | HIGH |
| **NoSQL Injection** | 15 | 10 | 5 | 67% | HIGH |
| **Template Injection (SSTI)** | 15 | 10 | 5 | 67% | HIGH |
| **XML/XXE Injection** | 10 | 0 | 10 | 0% | MEDIUM |
| **LDAP Injection** | 5 | 0 | 5 | 0% | LOW |
| **Total** | **140** | **80** | **60** | **57%** | - |

---

## 🚀 Batch Generation Plan

### Phase 1: High-Priority Expansions (Batches 005-012, 80 examples)

**Week 1: Core Injection Types**

**Batch 005: SQL Injection Expansion** (10 examples)
- Advanced SQL injection techniques
- Second-order SQL injection
- Blind SQL injection (boolean-based, time-based)
- ORM injection (SQLAlchemy, Hibernate, Sequelize)
- Stored procedure injection
- Languages: Python, Java, PHP, JavaScript, C#, Ruby, Go

**Batch 006: NoSQL Injection** (10 examples)
- MongoDB injection (query, aggregation)
- Redis injection
- Cassandra CQL injection
- DynamoDB injection
- Elasticsearch injection
- Languages: Python, JavaScript, Java, Go, PHP

**Batch 007: Command Injection Expansion** (10 examples)
- Windows command injection (PowerShell, cmd)
- Path traversal via command injection
- Argument injection
- Shell metacharacter bypass
- Container escape via command injection
- Languages: Python, Java, Go, C#, Ruby, PHP

**Batch 008: XSS Expansion Part 1** (10 examples)
- Reflected XSS with WAF bypass
- Stored XSS in rich text editors
- DOM-based XSS with complex sources/sinks
- Mutation XSS (mXSS)
- Universal XSS (UXSS)
- Languages: JavaScript, TypeScript, React, Vue, Angular

**Week 2: Template & XML Injection**

**Batch 009: Template Injection (SSTI) Part 1** (10 examples)
- Jinja2 SSTI (Python/Flask)
- Twig SSTI (PHP)
- FreeMarker SSTI (Java)
- ERB SSTI (Ruby)
- Handlebars SSTI (JavaScript)
- Languages: Python, PHP, Java, Ruby, JavaScript

**Batch 010: SQL Injection Advanced** (10 examples)
- Union-based injection
- Error-based injection
- Out-of-band (OOB) injection
- WAF bypass techniques
- Polyglot injection payloads
- Languages: Python, Java, PHP, Go, C#

**Batch 011: XSS Expansion Part 2** (10 examples)
- Content Security Policy (CSP) bypass
- XSS in JSON contexts
- XSS in SVG/XML contexts
- Self-XSS to stored XSS escalation
- XSS in mobile WebViews
- Languages: JavaScript, Swift, Kotlin, React Native

**Batch 012: Command Injection Advanced** (10 examples)
- DNS exfiltration via command injection
- Blind command injection detection
- Command injection in APIs
- CRLF injection
- LDAP injection via command parameters
- Languages: Python, Java, Go, PHP, Node.js

### Phase 2: Specialized Injection Types (Batches 013-018, 44 examples)

**Week 3: Advanced Techniques**

**Batch 013: NoSQL Injection Advanced** (5 examples)
- Aggregation pipeline injection
- JavaScript injection in MongoDB
- NoSQL blind injection
- Time-based NoSQL injection
- Languages: Python, JavaScript, Java, Go, PHP

**Batch 014: Template Injection Part 2** (5 examples)
- Velocity SSTI (Java)
- Pug SSTI (Node.js)
- Thymeleaf SSTI (Java/Spring)
- Go template injection
- Languages: Java, JavaScript, Go

**Batch 015: XML/XXE Injection** (10 examples)
- XXE file disclosure
- XXE SSRF attacks
- Blind XXE with OOB
- XXE in SOAP services
- XXE in document parsers (DOCX, XLSX)
- Languages: Java, Python, PHP, C#, Go

**Batch 016: XSS Expansion Part 3** (10 examples)
- XSS in rich email clients
- XSS in PDF generators
- Polyglot XSS payloads
- XSS via file upload
- XSS in markdown renderers
- Languages: Python, JavaScript, Java, Go, Ruby

**Batch 017: SQL Injection Edge Cases** (10 examples)
- SQL injection in ORDER BY clause
- SQL injection in LIMIT clause
- Truncation-based injection
- SQL injection in JSON functions
- GQL (Graph Query Language) injection
- Languages: Python, JavaScript, Java, PHP, Go

**Batch 018: LDAP Injection** (4 examples)
- LDAP filter injection
- LDAP DN injection
- Blind LDAP injection
- Languages: Java, Python, PHP, C#

### Phase 3: Final Push (Batches 019-020, 20 examples)

**Week 4: Completion**

**Batch 019: Command Injection Final** (10 examples)
- Mail command injection
- ImageMagick command injection
- FFmpeg command injection
- Git command injection
- SQL via command injection (sqlite3, psql)
- Languages: Python, Ruby, PHP, Go, Java

**Batch 020: XSS Final + Remaining** (10 examples)
- XSS in WebSockets
- XSS in PostMessage handlers
- XSS via CSS injection
- XSS in Web Workers
- Remaining edge cases
- Languages: JavaScript, TypeScript, Go, Python

---

## 📊 Generation Strategy

### Batch Size & Timing
- **Batch size**: 10 examples per batch (manageable, validates quickly)
- **Generation time**: 45-60 minutes per batch
- **Validation time**: 10-15 minutes per batch
- **Total time**: ~20 batches × 1 hour = 20 hours of generation

### Quality Assurance
- Run validation after each batch
- Fix any issues before moving to next batch
- Maintain 85%+ validation pass rate
- Document any validator limitations (like ES6 modules)

### Language Distribution (Per Batch)
- Python: 2-3 examples
- JavaScript/Node.js: 2-3 examples
- Java: 1-2 examples
- PHP: 1-2 examples
- Go: 1-2 examples
- Other (C#, Ruby, Rust): 0-1 examples

### Real-World Context Target
- Maintain 60%+ CVE/incident references
- Focus on 2022-2024 incidents
- Include quantified impact (dollar amounts, user counts)

---

## 🔧 Technical Approach

### Generator Template Structure
```python
def create_injection_example(
    example_id,
    language,
    subcategory,
    technique,
    cve_context=None
):
    return {
        "id": example_id,
        "metadata": {
            "lang": language,
            "category": "injection",
            "subcategory": subcategory,
            "technique": technique,  # NEW: specific technique
            "owasp_2021": "A03:2021-Injection",
            "cwe": get_cwe_for_subcategory(subcategory),
            "severity": "CRITICAL" or "HIGH",
            "complexity": "moderate" or "advanced",
        },
        "context": cve_context or generate_context(subcategory),
        "conversations": [
            turn_1_basic_question(),
            turn_2_vulnerable_to_secure(),
            turn_3_advanced_question(),
            turn_4_production_pattern()
        ]
    }
```

### Automation Opportunities
1. **Template reuse**: Extract common patterns into functions
2. **CVE database**: Load CVE contexts from YAML
3. **Code snippet library**: Reuse common secure patterns
4. **Batch generators**: Single script generates 10 examples

---

## 📈 Success Metrics

### Per-Batch Targets
- ✅ Validation pass rate: 85%+
- ✅ Real-world context: 60%+
- ✅ All 4-turn conversations
- ✅ Complete implementations
- ✅ Attack payloads included
- ✅ Zero syntax errors (ignoring validator limitations)
- ✅ Zero encoding errors

### Overall Dataset Quality (140 examples)
- ✅ Cross-language coverage: 11+ languages
- ✅ CVE references: 85+ unique CVEs
- ✅ Incident references: 50+ real-world incidents
- ✅ Code quality: Production-ready, linted, tested
- ✅ Educational value: Progressive learning from basic to advanced

---

## 🎯 Milestones

| Milestone | Examples | Completion Date | Status |
|-----------|----------|-----------------|--------|
| Baseline Validation | 15 | Jan 15, 2025 | ✅ COMPLETE |
| First 50 Examples | 50 | Nov 29, 2025 | ✅ COMPLETE |
| **First 70 Examples (50%)** | **70** | **Dec 1, 2025** | ✅ **COMPLETE** |
| First 100 Examples | 100 | Dec 2, 2025 | 🔄 In Progress |
| **140 Injection Examples** | **140** | **Dec 3, 2025** | ⏳ Pending |
| OWASP Top 10 Complete | 940 | TBD | ⏳ Pending |
| Full Dataset (1,000) | 1,000 | TBD | ⏳ Pending |

---

## 💡 Lessons from Baseline

### What Works Well
1. **4-turn structure** - Consistently effective
2. **Builder patterns** - Translate across languages
3. **Real-world context** - Creates urgency
4. **Complete implementations** - Not just snippets
5. **Allowlist validation** - Universal security pattern

### Watch Out For
1. **ES6 module imports** - Validator limitation (not code issue)
2. **Language-specific nuances** - Go error handling, Java boilerplate
3. **CVE availability** - Not all categories have recent CVEs
4. **Batch validation time** - Can take 10-15 minutes for 10 examples

---

## 🚀 Current Status & Next Actions

**Current Milestone**: 70/140 injection examples complete (50%)
**Validation Status**: 100% pass rate maintained across all batches
**Quality**: Production-ready, all examples validated

**Next Action**: Continue with Batch 009 (Template Injection / SSTI Part 1)

### Remaining Batches to Complete Injection Category (7 batches)

1. **Batch 009**: Template Injection (SSTI) Part 1 (10 examples)
   - Jinja2 (Python/Flask), Twig (PHP), FreeMarker (Java)
   - ERB (Ruby/Rails), Handlebars (JavaScript)

2. **Batch 010**: SQL Injection Advanced (10 examples)
   - UNION-based, Error-based, Out-of-band (OOB)
   - WAF bypass, Polyglot payloads

3. **Batch 011**: XSS Expansion Part 2 (10 examples)
   - CSP bypass advanced, JSON contexts, SVG/XML
   - Mobile WebViews, Self-XSS escalation

4. **Batch 012**: NoSQL + Command Advanced (10 examples)
   - 5 NoSQL: JavaScript injection in MongoDB, blind NoSQL, time-based
   - 5 Command: DNS exfiltration, blind detection, API injection

5. **Batch 013**: XML/XXE Injection (10 examples)
   - File disclosure, SSRF attacks, Blind XXE with OOB
   - SOAP services, Document parsers (DOCX, XLSX)

6. **Batch 014**: Template + XSS Final (10 examples)
   - 5 SSTI Part 2: Velocity, Pug, Thymeleaf, Go templates
   - 5 XSS Part 3: Email clients, PDF generators, polyglot XSS

7. **Batch 015**: SQL + LDAP Final (10 examples)
   - 5 SQL: ORDER BY/LIMIT injection, truncation, JSON functions, GQL
   - 5 LDAP: Filter injection, DN injection, blind LDAP

**Timeline**: 7 batches × 1 hour = ~7 hours to complete injection category

---

## 🎯 Beyond Injection: OWASP Top 10 Coverage

After completing 140 injection examples, proceed to full OWASP Top 10:

**Target**: 940 OWASP Top 10 examples + 150 AI/ML = 1,000 total

**Categories** (in priority order):
1. A07: Authentication Failures (150 examples)
2. A01: Broken Access Control (150 examples)
3. A05: Security Misconfiguration (120 examples)
4. A02: Cryptographic Failures (100 examples)
5. A04: Insecure Design (80 examples)
6. A06: Vulnerable Components (80 examples)
7. A08: Software/Data Integrity (80 examples)
8. A09: Logging/Monitoring (60 examples)
9. A10: SSRF (50 examples)
10. AI/ML Security Threats (150 examples)

**Estimated Timeline**: ~90 batches × 1 hour = ~90 hours total

---

**Let's continue scaling! 🚀**
