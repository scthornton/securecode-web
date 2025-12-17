# OWASP Top 10:2025 Release Candidate Summary

**Release Date**: November 6, 2025
**Status**: Release Candidate

## Complete Category List (2025)

1. **A01:2025 - Broken Access Control** (STAYS #1)
2. **A02:2025 - Security Misconfiguration** (UP from #5 → #2)
3. **A03:2025 - Software Supply Chain Failures** (UP from #6 → #3, EXPANDED SCOPE)
4. **A04:2025 - Cryptographic Failures** (DOWN from #2 → #4)
5. **A05:2025 - Injection** (DOWN from #3 → #5)
6. **A06:2025 - Insecure Design** (DOWN from #4 → #6)
7. **A07:2025 - Authentication Failures** (STAYS #7, NAME SIMPLIFIED)
8. **A08:2025 - Software or Data Integrity Failures** (STAYS #8, MINOR NAME CHANGE)
9. **A09:2025 - Security Logging & Alerting Failures** (STAYS #9, EMPHASIS ON ALERTING)
10. **A10:2025 - Mishandling of Exceptional Conditions** (NEW CATEGORY)

## Major Changes from 2021

### New Categories
- **A10:2025 - Mishandling of Exceptional Conditions**: Completely new category focusing on improper error handling, logical errors, failing open, and other abnormal condition scenarios (24 CWEs)

### Consolidated/Merged
- **SSRF (A10:2021)** rolled into **A01:2025 Broken Access Control**

### Expanded Scope
- **A03:2025 Software Supply Chain Failures** expanded from "Vulnerable and Outdated Components" to include entire supply chain ecosystem

### Name Changes
- A07:2021 "Identification and Authentication Failures" → A07:2025 "Authentication Failures"
- A08:2021 "Software and Data Integrity Failures" → A08:2025 "Software **or** Data Integrity Failures"
- A09:2021 "Security Logging and Monitoring Failures" → A09:2025 "Security Logging & Alerting Failures"

## Detailed Category Descriptions

### A01:2025 - Broken Access Control
- **Position**: #1 (maintained)
- **40 CWEs** mapped
- **Notable CWEs**: CWE-200, CWE-201, CWE-918 (SSRF), CWE-352 (CSRF)
- **Max Incidence Rate**: 20.15%
- **Avg Incidence Rate**: 3.74%
- **Total Occurrences**: 1,839,701
- **Total CVEs**: 32,654
- **Key Change**: SSRF rolled into this category

### A02:2025 - Security Misconfiguration
- **Position**: #2 (UP from #5)
- **16 CWEs** mapped
- **Notable CWEs**: CWE-16, CWE-611 (XXE)
- **Max Incidence Rate**: 27.70%
- **Avg Incidence Rate**: 3.00%
- **Total Occurrences**: 719,084
- **Total CVEs**: 1,375
- **Why It Moved Up**: "100% of applications tested had some form of misconfiguration"

### A03:2025 - Software Supply Chain Failures
- **Position**: #3 (UP from #6)
- **5 CWEs** mapped
- **Notable CWEs**: CWE-477, CWE-1104, CWE-1329, CWE-1395
- **Max Incidence Rate**: 8.81%
- **Avg Incidence Rate**: 5.19%
- **Total Occurrences**: 215,248
- **Total CVEs**: 11
- **Scope Expansion**: Now includes entire ecosystem (build systems, distribution, CI/CD pipeline)
- **Community Priority**: 50% of survey respondents ranked this #1

### A04:2025 - Cryptographic Failures
- **Position**: #4 (DOWN from #2)
- **32 CWEs** mapped
- **Max Incidence Rate**: 22.83%
- **Avg Incidence Rate**: 3.80%

### A05:2025 - Injection
- **Position**: #5 (DOWN from #3)
- **38 CWEs** mapped (most CWEs of any category)
- **Includes**: SQL Injection, XSS, Command Injection, LDAP, NoSQL
- **Range**: High frequency/low impact (XSS) to low frequency/high impact (SQL Injection)

### A06:2025 - Insecure Design
- **Position**: #6 (DOWN from #4)
- **39 CWEs** mapped
- **Notable CWEs**: CWE-256, CWE-269, CWE-434, CWE-501, CWE-522
- **Note**: "Noticeable improvements in industry related to threat modeling"

### A07:2025 - Authentication Failures
- **Position**: #7 (maintained)
- **36 CWEs** mapped
- **Notable CWEs**: CWE-259, CWE-297, CWE-287, CWE-384, CWE-798
- **Name Change**: Simplified from "Identification and Authentication Failures"

### A08:2025 - Software or Data Integrity Failures
- **Position**: #8 (maintained)
- **14 CWEs** mapped
- **Notable CWEs**: CWE-829, CWE-915, CWE-502
- **Focus**: Lower-level integrity failures than supply chain (insecure deserial, unsigned updates)

### A09:2025 - Security Logging & Alerting Failures
- **Position**: #9 (maintained)
- **5 CWEs** mapped (tied with A03 for fewest)
- **Emphasis Change**: "Great logging with no alerting is of minimal value"

### A10:2025 - Mishandling of Exceptional Conditions
- **Position**: #10 (NEW)
- **24 CWEs** mapped
- **Focus**: Improper error handling, logical errors, failing open

## Data Sources
- **2.8 million applications** analyzed
- **589 CWEs** analyzed (up from ~400 in 2021)
- **248 CWEs** within the 10 categories
- **~175k CVE records** (up from 125k in 2021)

## Methodology Notes
- Data-informed but not data-driven
- 8 categories from data, 2 from community survey
- Focus shifted to root causes over symptoms
- 25 CWEs average per category
- Max 40 CWEs per category (A01 Broken Access Control)

## References
- Release Candidate: November 6, 2025
- Full Documentation: https://owasp.org/Top10/2025/
- GitHub: https://github.com/OWASP/Top10
