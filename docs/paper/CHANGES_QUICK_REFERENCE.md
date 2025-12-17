# OWASP 2021→2025 Migration: Quick Reference

**Status:** ✅ COMPLETE
**Date:** December 17, 2025

---

## Changes Made (12 Total)

| # | Line | Section | Change |
|---|------|---------|--------|
| 1 | 113 | Dataset Overview | "OWASP Top 10 2021" → "OWASP Top 10:2025" |
| 2 | 125 | Figure 3 Caption | Updated counts (224 for A01) and names (Authentication Failures) |
| 3 | 277 | Data Collection | Updated OWASP version and category numbers (A01:2025, A04:2025) |
| 4 | 296 | Coverage Target | "OWASP Top 10 2021" → "OWASP Top 10:2025" |
| 5 | 356 | Prompt Template | "A03:2021 Injection" → "A05:2025 Injection" |
| 6 | 634 | Metadata Validation | "OWASP Top 10 2021" → "OWASP Top 10:2025" |
| 7 | 1151 | Enterprise Guidance | Added ":2025" to OWASP reference |
| 8 | 1155 | Fine-tuning Example | "A03:2021" → "A05:2025" |
| 9 | 1167 | Certification Prep | Added ":2025" to OWASP reference |
| 10 | 1341-1343 | References | Added [12] for 2025, kept [12b] for 2021 historical |
| 11 | 1380 | Schema Example | "A03:2021-Injection" → "A05:2025-Injection" |
| 12 | 1413 | Schema Docs | "OWASP Top 10 2021" → "OWASP Top 10:2025" |

---

## Category Number Changes

| Category | 2021 | 2025 | Notes |
|----------|------|------|-------|
| Broken Access Control | A01 | **A01** | Count: 179→224 (+45 SSRF) |
| Cryptographic Failures | A02 | **A04** | Changed |
| Injection | A03 | **A05** | Changed |
| Insecure Design | A04 | **A06** | Changed |
| Security Misconfiguration | A05 | **A02** | Priority elevated |
| Supply Chain | A06 | **A03** | Name + number changed |
| Authentication | A07 | **A07** | Name simplified |
| Integrity | A08 | **A08** | Name clarified |
| Logging | A09 | **A09** | Name expanded |
| SSRF | A10 | **MERGED** | Into A01:2025 |

---

## Category Name Changes

| 2021 Name | 2025 Name |
|-----------|-----------|
| Identification and Authentication Failures | **Authentication Failures** |
| Vulnerable and Outdated Components | **Software Supply Chain Failures** |
| Software and Data Integrity Failures | **Software or Data Integrity Failures** |
| Security Logging and Monitoring Failures | **Security Logging & Alerting Failures** |

---

## Verification Commands

```bash
# Should show only historical reference in References section
grep -n "OWASP Top 10 2021" COMPLETE_PAPER_DRAFT.md

# Should be empty (all updated to A05:2025)
grep -n "A03:2021" COMPLETE_PAPER_DRAFT.md

# Should show 6 occurrences (all sections updated)
grep -n "A05:2025" COMPLETE_PAPER_DRAFT.md
```

---

## Key Numbers to Remember

- **A01:2025 Broken Access Control:** 224 examples (18.4%)
  - Was 179 in A01:2021
  - Added 45 from A10:2021 SSRF merge

- **A07:2025 Authentication Failures:** 199 examples (16.4%)
  - Same count, simplified name

- **A05:2025 Injection:** 125 examples (10.3%)
  - Was A03:2021

- **Total Examples:** 1,215 (unchanged)

---

## Already Completed Sections (Don't Re-do)

✅ Appendix B table (lines 1406-1434)
✅ Section 3.3 category listing (lines 407-429)
✅ Section 1.5 introduction listing (lines 61-74)
✅ Section 3.2.3 taxonomy evolution (lines 402-423)

---

## Files Created

1. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/OWASP_2021_TO_2025_MIGRATION_SUMMARY.md`
   - Complete detailed change log with before/after text

2. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/MIGRATION_VERIFICATION_REPORT.md`
   - Test results and verification proof

3. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/CHANGES_QUICK_REFERENCE.md`
   - This file - quick lookup reference

---

**Status:** ✅ Migration complete and verified
**Updated File:** `COMPLETE_PAPER_DRAFT.md`
**Verification:** All tests pass
