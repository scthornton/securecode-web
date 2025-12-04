# SecureCode v2.0: Security Improvement Action Plan

**Date:** December 3, 2025
**Current Score:** 87/100 (B+)
**Target Score:** 95/100 (A)
**Estimated Effort:** 150-200 new examples (~80-100 hours)

---

## Overview

This action plan provides specific, prioritized recommendations to elevate SecureCode v2.0 from a **B+ quality dataset** to an **A-grade gold standard**. All recommendations are based on comprehensive security analysis of 1,209 examples, CVE validation, and OWASP coverage assessment.

---

## Priority 1: OWASP Category Rebalancing (HIGH PRIORITY)

**Goal:** Bring all OWASP categories to 8-15% representation
**Impact:** +10 points to overall score (87 → 97)
**Effort:** 150-200 new examples (~80-100 hours)

### 1.1 SSRF (A10) - Add 50 Examples

**Current:** 45 examples (3.7%)
**Target:** 95 examples (8%)
**Gap:** 50 examples needed

#### Specific Examples to Create

**Cloud Metadata SSRF (20 examples):**
1. AWS EC2 metadata service (169.254.169.254)
   - Python boto3 vulnerable to SSRF
   - Node.js AWS SDK SSRF via user-controlled endpoints
   - Java Spring Cloud AWS metadata exposure
   - Go AWS Lambda internal service access

2. Azure Instance Metadata Service
   - C# Azure SDK SSRF vulnerabilities
   - REST API SSRF to Azure IMDS
   - Managed identity theft via SSRF

3. Google Cloud Metadata Service
   - Python GCP SDK SSRF
   - Kubernetes pod metadata access
   - GKE workload identity SSRF

**DNS Rebinding Advanced (15 examples):**
1. Time-of-check vs time-of-use (TOCTOU) DNS attacks
2. Multi-stage DNS rebinding with cache poisoning
3. Browser-based DNS rebinding attacks
4. WebSocket DNS rebinding
5. PDF generation SSRF via DNS rebinding

**Webhook SSRF (10 examples):**
1. GitHub/GitLab webhook SSRF to internal services
2. Slack/Discord webhook SSRF exploitation
3. Payment gateway webhook SSRF (Stripe, PayPal)
4. CI/CD webhook SSRF (Jenkins, CircleCI)

**URL Parser Bypass (5 examples):**
1. URL encoding bypass techniques
2. IPv6 representation tricks
3. Decimal/octal IP notation
4. Unicode domain bypass
5. Protocol handler confusion

**CVE References to Include:**
- CVE-2019-4142 (Capital One AWS SSRF)
- CVE-2021-22214 (GitLab SSRF)
- CVE-2023-23529 (WebKit DNS rebinding)
- CVE-2022-24990 (TerraMaster SSRF)

### 1.2 AI/ML Security - Add 50 Examples

**Current:** 50 examples (4.1%)
**Target:** 100 examples (8.3%)
**Gap:** 50 examples needed

#### Specific Examples to Create

**Prompt Injection (15 examples):**
1. Direct prompt injection attacks
   - System prompt override
   - Role manipulation ("You are now...")
   - Instruction hierarchy attacks

2. Indirect prompt injection
   - Data poisoning via training data
   - Web page injection via retrieval
   - Email injection attacks
   - Document-based injection (PDFs, Office docs)

**Model Theft & Extraction (10 examples):**
1. Model architecture extraction via API probing
2. Weight extraction through gradient attacks
3. Distillation attacks on proprietary models
4. Membership inference attacks
5. Training data extraction

**RAG Poisoning (10 examples):**
1. Vector database poisoning
2. Document corpus manipulation
3. Embedding space attacks
4. Context window exploitation
5. Citation manipulation attacks

**Adversarial Examples (8 examples):**
1. Image adversarial patches (physical world)
2. Text adversarial examples
3. Audio adversarial attacks
4. Video perturbation attacks

**Agent Hijacking (7 examples):**
1. Function calling manipulation
2. Tool use poisoning
3. Multi-agent coordination attacks
4. Memory corruption in agentic systems

**CVE References to Include:**
- CVE-2022-45907 (PyTorch supply chain)
- CVE-2024-5480 (PyTorch Model Hub)
- Research papers: Jailbreak prompts, indirect injection (Greshake et al.)

### 1.3 Logging Failures (A09) - Add 40 Examples

**Current:** 59 examples (4.9%)
**Target:** 99 examples (8.2%)
**Gap:** 40 examples needed

#### Specific Examples to Create

**SIEM Integration (12 examples):**
1. Splunk secure logging patterns
2. ELK Stack security event correlation
3. Datadog security monitoring
4. Azure Sentinel integration
5. Chronicle Security logging

**Audit Trail Best Practices (10 examples):**
1. Immutable audit logs (blockchain/WORM storage)
2. Cryptographic log signing
3. Audit trail completeness verification
4. High-privilege action logging
5. Bulk operation audit patterns

**Forensic Logging (8 examples):**
1. Attack timeline reconstruction
2. Evidence preservation patterns
3. Chain of custody logging
4. Incident response logging

**Log Tampering Prevention (5 examples):**
1. Append-only log systems
2. Remote syslog forwarding
3. Log integrity verification
4. Centralized logging security

**Performance-Optimized Logging (5 examples):**
1. Asynchronous logging patterns
2. Log sampling strategies
3. Structured logging (JSON) best practices
4. High-throughput logging systems

**CVE References to Include:**
- CVE-2023-38547 (Okta breach - insufficient logging)
- CVE-2023-5950 (Okta HAR file exposure)
- CVE-2021-45046 (Log4j - logging vulnerability)

### 1.4 Integrity Failures (A08) - Add 20 Examples

**Current:** 80 examples (6.6%)
**Target:** 100 examples (8.3%)
**Gap:** 20 examples needed

#### Specific Examples to Create

**Supply Chain Attacks (10 examples):**
1. Dependency confusion attacks
2. Typosquatting package attacks
3. Compromised package maintainer accounts
4. Malicious package updates
5. Build pipeline compromise

**Software Composition Analysis (5 examples):**
1. SBOM generation and validation
2. Transitive dependency scanning
3. License compliance checking
4. Vulnerability tracking in dependencies

**Code Signing & Integrity (5 examples):**
1. Binary signing verification
2. Container image signing (Sigstore/Notary)
3. Package signature validation
4. Firmware integrity checks

**CVE References to Include:**
- CVE-2024-3094 (xz utils backdoor)
- CVE-2021-43138 (Codecov supply chain)
- CVE-2022-23812 (PyTorch dependency confusion)

### 1.5 Insecure Design (A04) - Add 15 Examples

**Current:** 84 examples (6.9%)
**Target:** 99 examples (8.2%)
**Gap:** 15 examples needed

#### Specific Examples to Create

**Business Logic Vulnerabilities (8 examples):**
1. Payment bypass attacks
2. Discount code abuse
3. Referral system exploitation
4. Booking/reservation race conditions
5. Multi-currency arbitrage

**Threat Modeling Failures (4 examples):**
1. Missing threat model documentation
2. Unvalidated trust boundaries
3. Insufficient attack surface analysis

**Workflow Vulnerabilities (3 examples):**
1. Approval bypass attacks
2. State machine exploitation
3. Multi-step process vulnerabilities

**CVE References to Include:**
- CVE-2023-44487 (HTTP/2 rapid reset)
- CVE-2024-21626 (Docker TOCTOU)

### 1.6 Vulnerable Components (A06) - Add 15 Examples

**Current:** 85 examples (7.0%)
**Target:** 100 examples (8.3%)
**Gap:** 15 examples needed

#### Specific Examples to Create

**Outdated Dependencies (8 examples):**
1. Critical version updates (Log4j, Spring4Shell)
2. End-of-life software usage
3. Unpatched CVE exploitation
4. Legacy framework vulnerabilities

**Transitive Dependencies (4 examples):**
1. Deep dependency chain vulnerabilities
2. Version conflict exploitation
3. Dependency tree poisoning

**Third-Party Integrations (3 examples):**
1. SDK vulnerabilities
2. Plugin/extension security
3. API client library flaws

**CVE References to Include:**
- CVE-2022-22965 (Spring4Shell)
- CVE-2017-9841 (PHPUnit RCE)
- CVE-2021-3129 (Laravel Debug Mode)

---

## Priority 2: Severity Distribution Rebalancing (MEDIUM PRIORITY)

**Goal:** Realistic severity distribution to prevent training bias
**Impact:** +5 points to overall score
**Effort:** 150 new examples (~40 hours) OR re-rating existing examples (~10 hours)

### Current vs Target Distribution

| Severity | Current | Target | Action Needed |
|----------|---------|--------|---------------|
| CRITICAL | 791 (65.4%) | 484 (40%) | Reclassify or dilute |
| HIGH | 394 (32.6%) | 484 (40%) | Maintain/add |
| MEDIUM | 24 (2.0%) | 181 (15%) | **Add 157 examples** |
| LOW | 0 (0.0%) | 60 (5%) | **Add 60 examples** |

### Approach Options

**Option A: Add New Examples (Recommended)**
- Add 157 MEDIUM severity examples
- Add 60 LOW severity examples
- Maintains dataset size growth
- Total effort: ~40 hours

**Option B: Re-rate Existing Examples**
- Review 200 CRITICAL examples
- Downgrade ~100 to HIGH
- Downgrade ~50 to MEDIUM
- Total effort: ~10 hours
- Risk: May reduce dataset quality perception

### MEDIUM Severity Example Types (157 needed)

1. **Information Disclosure (50 examples)**
   - Error message information leakage
   - Comment exposure in production code
   - Debug endpoints left enabled
   - Git metadata exposure (.git folder)
   - Backup file exposure (.bak, .old)

2. **Security Misconfiguration (40 examples)**
   - Directory listing enabled
   - Unnecessary services running
   - Default credentials not changed
   - Permissive CORS policies
   - Weak security headers

3. **Insufficient Monitoring (30 examples)**
   - Missing rate limiting
   - No brute force detection
   - Inadequate log retention
   - Missing alerting

4. **Minor Crypto Issues (20 examples)**
   - Weak random number generation (non-cryptographic)
   - Short session timeouts
   - Cookie security flags missing

5. **Client-Side Validation Only (17 examples)**
   - JavaScript-only input validation
   - Client-side authorization checks
   - Trust in client-side timestamps

### LOW Severity Example Types (60 needed)

1. **Informational Findings (30 examples)**
   - Software version disclosure
   - Banner grabbing vulnerabilities
   - HTML comments with minor info
   - Missing security headers (non-critical)

2. **Minor Misconfigurations (20 examples)**
   - HTTP allowed alongside HTTPS
   - Long session timeouts
   - Minor CSP violations
   - Non-sensitive HTTP cookies

3. **Best Practice Deviations (10 examples)**
   - Missing HTTP security headers
   - Verbose error pages
   - Open redirects (limited impact)

---

## Priority 3: CVE Cleanup (LOW PRIORITY)

**Goal:** 100% valid CVE format
**Impact:** +1 point to overall score
**Effort:** 2-3 hours

### 9 CVEs Requiring Cleanup

| Current CVE | Issue | Recommended Replacement |
|-------------|-------|------------------------|
| CVE-2023-OPTUS | Internal designation | N/A - Optus breach (documented 2022-09-22) |
| CVE-2021-PARLER | No formal CVE | N/A - Parler data scraping incident (2021) |
| CVE-2022-* | Wildcard | CVE-2022-46381 (LastPass infrastructure) |
| CVE-2019-CAPONE | Duplicate | CVE-2019-11510 (Capital One breach) |
| CVE-2019-CAPITAL-ONE | Duplicate | CVE-2019-11510 (Capital One breach) |
| CVE-2023-TAPI | Internal designation | N/A - T-Mobile API breach (2023) |
| CVE-2023-OPTUS-API | Duplicate | N/A - Optus breach (already addressed) |
| CVE-2023-XXXX | Placeholder | Research specific CVE or use N/A |

### Implementation Steps

1. Search for each invalid CVE ID in dataset:
   ```bash
   grep -r "CVE-2023-OPTUS" consolidated/
   ```

2. Replace with appropriate value:
   ```json
   {
     "cve": "N/A - Documented breach without formal CVE assignment",
     "internal_ref": "OPTUS-2022-09-22",
     "incident": "2022 Optus Data Breach"
   }
   ```

3. Validate no wildcards remain:
   ```bash
   grep -E "CVE-[0-9]{4}-\*" consolidated/
   ```

---

## Priority 4: Technique Taxonomy Normalization (LOW PRIORITY)

**Goal:** Consistent technique naming
**Impact:** +1 point (improves filtering/analysis)
**Effort:** 4-6 hours

### Duplicates to Merge

| Duplicates | Merge To | Count |
|------------|----------|-------|
| unsafe_deserialization, insecure_deserialization, Insecure deserialization | insecure_deserialization | 82 |
| sql_injection, SQL injection, SQL Injection | sql_injection | ~60 |
| xss, XSS, cross_site_scripting | xss | ~50 |

### Implementation Steps

1. Create technique taxonomy document (`taxonomy/techniques.yaml`)
2. Run normalization script:
   ```python
   technique_mappings = {
       'unsafe_deserialization': 'insecure_deserialization',
       'Insecure deserialization': 'insecure_deserialization',
   }
   ```
3. Update all examples
4. Validate consistency

---

## Priority 5: Add Timeframe Metrics (NICE-TO-HAVE)

**Goal:** 20% of examples include time-to-detection data
**Impact:** +1 point (improves incident realism)
**Effort:** 10-15 hours (research time)

### Current vs Target

- **Current:** 7% include timeframes
- **Target:** 20% include time-to-detection, attack duration, or exploitation timeline

### Metrics to Add

1. **Time-to-Detection:** "Breach went undetected for 14 days"
2. **Time-to-Exploitation:** "Exploit published 24 hours after CVE disclosure"
3. **Attack Duration:** "Attackers maintained access for 6 months"
4. **Remediation Time:** "Patch deployed to 80% of systems within 48 hours"

### Example Enhancement

**Before:**
```json
{
  "impact": "$80M fine, 106M records exposed"
}
```

**After:**
```json
{
  "impact": "$80M fine, 106M records exposed over 6-month breach period",
  "detection_time": "Breach detected after 6 months of unauthorized access",
  "timeline": "March-July 2019"
}
```

---

## Implementation Roadmap

### Week 1-2: High-Priority SSRF & AI/ML (50 hours)
- **Output:** 100 new examples (50 SSRF + 50 AI/ML)
- **Activities:**
  - Research CVE references for SSRF
  - Create cloud metadata SSRF examples (AWS/Azure/GCP)
  - Develop prompt injection examples
  - Create RAG poisoning patterns
- **Deliverable:** +100 examples → Dataset reaches 1,309 total

### Week 3: Logging Failures (20 hours)
- **Output:** 40 new logging examples
- **Activities:**
  - SIEM integration patterns
  - Audit trail best practices
  - Log tampering prevention
- **Deliverable:** +40 examples → Dataset reaches 1,349 total

### Week 4: Remaining Categories (20 hours)
- **Output:** 50 examples (Integrity, Insecure Design, Vuln Components)
- **Deliverable:** +50 examples → Dataset reaches 1,399 total

### Week 5: Severity Rebalancing (10-40 hours)
- **Option A:** Re-rate 150 existing examples (~10 hours)
- **Option B:** Create 217 new MEDIUM/LOW examples (~40 hours)
- **Deliverable:** Balanced severity distribution

### Week 6: Cleanup & Polish (6 hours)
- CVE cleanup (3 hours)
- Technique normalization (3 hours)
- Final validation

---

## Expected Outcomes

### After Priority 1 Completion (OWASP Rebalancing)

**Before:**
- Total examples: 1,209
- OWASP balance: 6 categories underrepresented
- Security score: 87/100 (B+)

**After:**
- Total examples: 1,399 (+190)
- OWASP balance: All categories 8-15%
- Security score: **95/100 (A-)**

### After Priority 2 Completion (Severity Rebalancing)

**Before:**
- CRITICAL: 65.4%, HIGH: 32.6%, MEDIUM: 2.0%, LOW: 0%
- Severity score: 70/100

**After:**
- CRITICAL: 40%, HIGH: 40%, MEDIUM: 15%, LOW: 5%
- Severity score: **95/100**
- **Overall score: 96/100 (A)**

### After All Priorities

**Final Dataset:**
- Examples: 1,400-1,600
- OWASP coverage: ✅ Balanced
- Severity distribution: ✅ Realistic
- CVE validity: ✅ 100%
- Technique consistency: ✅ Normalized
- **Security score: 97-98/100 (A/A+)**

---

## Resource Requirements

### Time Investment

| Priority | Effort | Expected Output |
|----------|--------|-----------------|
| P1: OWASP Rebalancing | 80-100 hours | +190 examples |
| P2: Severity | 10-40 hours | +217 examples OR re-rating |
| P3: CVE Cleanup | 2-3 hours | 9 fixes |
| P4: Taxonomy | 4-6 hours | Consistent naming |
| P5: Timeframes | 10-15 hours | 150+ enhancements |
| **TOTAL** | **106-164 hours** | **+407 examples** |

### Expertise Required

- **Security Research:** Incident documentation, CVE analysis
- **Programming:** Multi-language code examples (Python, JS, Java, Go, etc.)
- **LLM Prompt Engineering:** Generating conversational examples
- **Quality Assurance:** Code validation, security review

### Tooling

- **GPT-4 or Claude Opus:** Example generation
- **CVE Database Access:** NVD, MITRE, vendor advisories
- **Code Validators:** Language-specific linters
- **Version Control:** Git for tracking changes

---

## Success Metrics

### Dataset Quality Targets

| Metric | Current | Target | Success Criteria |
|--------|---------|--------|------------------|
| OWASP Balance | 6 underrepresented | 0 underrepresented | All 8-15% |
| CVE Validity | 99.0% | 100.0% | No invalid formats |
| Severity Distribution | 65% CRITICAL | 40% CRITICAL | Realistic spread |
| Security Score | 87/100 | 95-97/100 | A rating |

### Validation Gates

**Before Accepting New Examples:**
1. ✅ CVE references validate against NVD
2. ✅ Incident descriptions cite public sources
3. ✅ Code examples are syntactically correct
4. ✅ Severity matches CVSS score ±1 level
5. ✅ Defense-in-depth patterns present in Turn 4

---

## Risk Mitigation

### Risk: Quality Dilution

**Mitigation:**
- Use same generation process as original dataset
- Mandatory security review of all new examples
- Spot-check 10% of new examples for CVE accuracy

### Risk: Timeline Overrun

**Mitigation:**
- Focus on P1 only (OWASP balance) for minimum viable improvement
- P1 alone raises score to 95/100 (A-)
- P2-P5 are optional enhancements

### Risk: Inconsistent Style

**Mitigation:**
- Create example templates for each OWASP category
- Use automated style checking
- Reference existing high-quality examples

---

## Conclusion

This action plan provides a clear path from **87/100 (B+)** to **95-97/100 (A/A+)**. Priority 1 alone (OWASP rebalancing) provides the greatest impact, elevating the dataset to A- rating.

**Recommended Approach:**
1. **Execute Priority 1 fully** (80-100 hours) → Achieves 95/100
2. **Evaluate need for Priority 2** based on use case
3. **Complete Priority 3-5** if targeting gold standard (97+/100)

**Quick Win:** Focus on SSRF and AI/ML Security (50 hours) for immediate differentiation and 90/100 score.

---

**Prepared By:**
Scott Thornton
AI Security Researcher
perfecXion.ai

**Contact:** scott@perfecxion.ai
**Related Documents:**
- `SECURITY_ANALYSIS_REPORT.md` - Full analysis
- `EXECUTIVE_SUMMARY.md` - Executive briefing
