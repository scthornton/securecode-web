# OWASP Taxonomy Update - Quick Reference Guide

## Critical Numbers to Update

### A01:2025 Broken Access Control
- **OLD:** 179 examples (14.7%)
- **NEW:** 224 examples (18.4%)
- **Reason:** Merged 45 SSRF examples (A10:2021)
- **Severity:** CRIT: 146, HIGH: 71, MED: 7

### Category Reordering Map

| 2021 Position | 2021 Category | → | 2025 Position | 2025 Category | Change |
|--------------|---------------|---|--------------|---------------|--------|
| A01:2021 | Broken Access Control | → | A01:2025 | Broken Access Control | +45 SSRF examples |
| A02:2021 | Cryptographic Failures | → | A04:2025 | Cryptographic Failures | Number DOWN |
| A03:2021 | Injection | → | A05:2025 | Injection | Number DOWN |
| A04:2021 | Insecure Design | → | A06:2025 | Insecure Design | Number DOWN |
| A05:2021 | Security Misconfiguration | → | A02:2025 | Security Misconfiguration | Number UP (major) |
| A06:2021 | Vulnerable Components | → | A03:2025 | **Supply Chain Failures** | Number UP + NAME |
| A07:2021 | **Identification and** Auth | → | A07:2025 | Authentication Failures | NAME simplified |
| A08:2021 | Software **and** Data Integrity | → | A08:2025 | Software **or** Data Integrity | NAME (and→or) |
| A09:2021 | Logging **and Monitoring** | → | A09:2025 | Logging **& Alerting** | NAME emphasis |
| A10:2021 | **SSRF** | → | **MERGED into A01:2025** | — | ELIMINATED |

---

## Name Changes Only (Same Number)

- **A07:2025:** "Identification and" removed → just "Authentication Failures"
- **A08:2025:** "and" → "or" (Software **or** Data Integrity Failures)
- **A09:2025:** "+ Alerting" added (Security Logging **& Alerting** Failures)

---

## Find/Replace Operations

### Safe Replacements (Same Position)

```
"A07:2021 Identification and Authentication Failures"
→ "A07:2025 Authentication Failures"

"A08:2021 Software and Data Integrity Failures"
→ "A08:2025 Software or Data Integrity Failures"

"A09:2021 Security Logging and Monitoring Failures"
→ "A09:2025 Security Logging & Alerting Failures"
```

### Careful Replacements (Position Changed)

```
"A02:2021 Cryptographic Failures"
→ "A04:2025 Cryptographic Failures"

"A03:2021 Injection"
→ "A05:2025 Injection"

"A04:2021 Insecure Design"
→ "A06:2025 Insecure Design"

"A05:2021 Security Misconfiguration"
→ "A02:2025 Security Misconfiguration"

"A06:2021 Vulnerable and Outdated Components"
→ "A03:2025 Software Supply Chain Failures"
```

### Manual Handling Required

```
"A10:2021 Server-Side Request Forgery" or "A10:2021 SSRF"
→ REMOVE from tables
→ ADD note: "merged into A01:2025 Broken Access Control"
→ UPDATE A01 count: 179 → 224
→ UPDATE A01 percentage: 14.7% → 18.4%
```

---

## Version References

**Replace all instances:**
```
"OWASP Top 10 2021" → "OWASP Top 10:2025"
"OWASP 2021" → "OWASP 2025"
```

**Add historical note where needed:**
```
"Dataset initially created using OWASP 2021 taxonomy,
remapped to OWASP 2025 Release Candidate (November 2025)"
```

---

## Key Statistics to Verify

After all updates, these must be consistent throughout paper:

| Statistic | Value | Locations |
|-----------|-------|-----------|
| Total examples | 1,215 | Abstract, all sections |
| A01 count | 224 | Abstract, Sec 1.5, 3.3, Appendix B |
| A01 percentage | 18.4% | Abstract, Sec 1.5, 3.3, Appendix B |
| A07 count | 199 | All sections (unchanged) |
| A07 percentage | 16.4% | All sections (unchanged) |
| Total categories | 12 | 10 OWASP + AI/ML + Unknown |

---

## Priority Locations (Update First)

### CRITICAL (Do These First)
1. **Appendix B Table (lines 1410-1424)** - Complete table restructure
2. **Section 3.3 Listing (lines 407-424)** - Major category listing
3. **Section 1.5 Intro (lines 61-73)** - Introduction category list
4. **Abstract Stats (line 15)** - Category count statement

### HIGH (Do These Second)
5. Methodology explanation (NEW section 3.2.3)
6. References section (OWASP 2025 citation)
7. Appendix A schema example (line 1355)
8. All narrative A0X:202X references

### MEDIUM (Do These Third)
9. Discussion section OWASP references
10. Coverage notes in Appendix B
11. Validation framework documentation

---

## Validation Checklist

After updates, verify:

- [ ] Search ":2021" → 0 results (except historical context)
- [ ] Search "Identification and Authentication" → 0 results
- [ ] Search "Vulnerable and Outdated Components" → 0 results
- [ ] Search "Software and Data Integrity" → 0 results
- [ ] Search "A10:2021 SSRF" → 0 results (except with merge note)
- [ ] A01 count = 224 in all sections
- [ ] A01 percentage = 18.4% in all sections
- [ ] Total examples = 1,215 in all sections
- [ ] All category percentages sum to 100%
- [ ] Appendix B matches Section 3.3 exactly

---

## New Section Required

**Location:** After Section 3.2 or beginning of 3.3

**Title:** "3.2.3 OWASP Taxonomy Evolution and Dataset Alignment"

**Purpose:** Explain why paper uses 2025 taxonomy when dataset created in 2024

**Length:** ~300 words

**Key Points:**
- Dataset began with 2021 taxonomy (2024)
- OWASP released 2025 RC (November 2025)
- All examples remapped to 2025 taxonomy
- Major changes: SSRF merge, A05→A02 elevation, A06 scope expansion
- No content changed, only categorization updated

---

## Quick Math Reference

### A01:2025 Severity Breakdown
```
Original A01:2021:     CRIT: 117, HIGH: 56, MED: 6  (179 total)
Original A10:2021 SSRF: CRIT: 29,  HIGH: 15, MED: 1  (45 total)
───────────────────────────────────────────────────────────────
Merged A01:2025:       CRIT: 146, HIGH: 71, MED: 7  (224 total)
```

### Percentage Calculation
```
224 / 1,215 × 100 = 18.43% → rounds to 18.4%
```

---

## Color-Coded Priority Map

🔴 **CRITICAL - Must Fix Before Publication**
- Appendix B table
- Section 3.3 listing
- A01 count/percentage everywhere
- Category name changes (all instances)

🟡 **HIGH - Fix During Revision**
- Methodology explanation (new section)
- References update
- Schema examples
- Version references

🟢 **MEDIUM - Clean Up Pass**
- Discussion references
- Coverage notes
- Validation docs
- Minor narrative updates

---

## Time Estimates

- **Critical Updates:** 6-8 hours
- **High Priority:** 4-6 hours
- **Medium Priority:** 3-4 hours
- **Verification:** 3-4 hours
- **Total:** 16-22 hours

---

## Contact for Questions

If inconsistencies found during update:
- Check `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/owasp_reference/` for authoritative mappings
- Verify counts against `canonical_counts.json` (single source of truth)
- Confirm OWASP 2025 details at https://owasp.org/Top10/2025/
