# OWASP 2025 Update Analysis - Complete Documentation Audit

**Date**: 2025-12-16
**Analyst**: Claude Code
**Status**: COMPREHENSIVE REVIEW COMPLETE

---

## Executive Summary

Comprehensive audit of all SecureCode v2.0 documentation reveals **extensive OWASP 2021 references** across 12+ critical files that must be updated to OWASP 2025 Release Candidate taxonomy. The comparison guide exists and is comprehensive, but updates have NOT been applied to any documentation files yet.

**Critical Finding**: Both dataset files (JSONL) and documentation use OWASP 2021. Complete migration to OWASP 2025 required across ALL components.

---

## 1. File Inventory - Complete Documentation Analysis

### ✅ Files Analyzed (17 total)

**Root-Level Documentation (5 files):**
1. `/Users/scott/perfecxion/datasets/securecode/v2/README.md` (426 lines)
2. `/Users/scott/perfecxion/datasets/securecode/v2/CORRECTIONS_APPLIED.md` (198 lines)
3. `/Users/scott/perfecxion/datasets/securecode/v2/DEPLOYMENT_READY.md` (325 lines)
4. `/Users/scott/perfecxion/datasets/securecode/v2/CONTRIBUTING.md` (187 lines)
5. `/Users/scott/perfecxion/datasets/securecode/v2/VALIDATOR_V2_PAPER_UPDATES.md` (279 lines)

**Paper Documentation (7 files):**
6. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/FOURTH_REVIEW_FIXES_APPLIED.md` (339 lines)
7. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/FINAL_SUBMISSION_READY.md` (269 lines)
8. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/COMPLETE_PAPER_DRAFT.md` (1,571 lines) ⚠️ **PRIMARY TARGET**
9. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/ACADEMIC_PAPER_OUTLINE.md` (450+ lines)
10. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/REVIEWER_PROOFING_FIXES_APPLIED.md`
11. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/THIRD_REVIEW_FIXES_APPLIED.md`
12. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/MUST_FIX_CORRECTIONS_APPLIED.md`

**Reference Documentation (3 files):**
13. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/owasp_reference/OWASP_2021_vs_2025_Comparison.md` ✅ **GUIDE EXISTS**
14. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/owasp_reference/OWASP_2025_Summary.md` ✅ **REFERENCE EXISTS**
15. `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/owasp_reference/OWASP_2021_Full.md` (reference only)

**Validator Documentation (2 files):**
16. `/Users/scott/perfecxion/datasets/securecode/v2/VALIDATOR_V2_README.md` (499 lines)
17. `/Users/scott/perfecxion/datasets/securecode/v2/VALIDATOR_V2_SUMMARY.md` (303 lines)

**Configuration Files (3 files):**
18. `/Users/scott/perfecxion/datasets/securecode/v2/taxonomy.yaml` ⚠️ **CRITICAL**
19. `/Users/scott/perfecxion/datasets/securecode/v2/canonical_counts.json` ⚠️ **CRITICAL**
20. `/Users/scott/perfecxion/datasets/securecode/v2/validate_contributing_compliance.py` (validator code)

---

## 2. Changes Required by File - Detailed Breakdown

### 🔴 TIER 1: CRITICAL - MUST UPDATE BEFORE PUBLICATION

#### File 1: `COMPLETE_PAPER_DRAFT.md` (1,571 lines)
**Priority**: CRITICAL
**OWASP References**: 22+ direct category references
**Impact**: Primary submission document

**Required Changes:**

**Lines 62-71: Abstract - OWASP Category List**
```markdown
# CURRENT (2021)
- **A07:2021 Identification and Authentication Failures** (199 examples, 16.4%)
- **A01:2021 Broken Access Control** (179 examples, 14.7%)
- **A05:2021 Security Misconfiguration** (134 examples, 11.0%)
- **A03:2021 Injection** (125 examples, 10.3%)
- **A02:2021 Cryptographic Failures** (115 examples, 9.5%)
- **A06:2021 Vulnerable and Outdated Components** (85 examples, 7.0%)
- **A04:2021 Insecure Design** (84 examples, 6.9%)
- **A08:2021 Software and Data Integrity Failures** (80 examples, 6.6%)
- **A09:2021 Logging & Monitoring Failures** (59 examples, 4.9%)

# MUST BECOME (2025)
- **A07:2025 Authentication Failures** (199 examples, 16.4%)
- **A01:2025 Broken Access Control** (179 examples, 14.7%)
- **A02:2025 Security Misconfiguration** (134 examples, 11.0%)
- **A05:2025 Injection** (125 examples, 10.3%)
- **A04:2025 Cryptographic Failures** (115 examples, 9.5%)
- **A03:2025 Software Supply Chain Failures** (85 examples, 7.0%)
- **A06:2025 Insecure Design** (84 examples, 6.9%)
- **A08:2025 Software or Data Integrity Failures** (80 examples, 6.6%)
- **A09:2025 Security Logging & Alerting Failures** (59 examples, 4.9%)
```

**Line 61: Language and coverage summary**
```markdown
# CURRENT
Comprehensive security coverage across complete OWASP Top 10 2021

# MUST BECOME
Comprehensive security coverage across complete OWASP Top 10:2025 Release Candidate
```

**Line 114: Features list**
```markdown
# CURRENT
- **10 OWASP Top 10 2021 categories**: A01-A10 (all categories covered)

# MUST BECOME
- **9 OWASP Top 10:2025 categories** (A01-A09, A10:2021 SSRF merged into A01:2025)
```

**Lines 278: OWASP Documentation Reference**
```markdown
# CURRENT
OWASP Top 10 2021 categories and mapped each to real-world incidents. A01:2021 Broken Access Control... A02:2021 Cryptographic Failures...

# MUST BECOME
OWASP Top 10:2025 Release Candidate categories and mapped each to real-world incidents. A01:2025 Broken Access Control... A04:2025 Cryptographic Failures...
```

**Line 297: Coverage target**
```markdown
# CURRENT
Coverage target: All OWASP Top 10 2021 categories

# MUST BECOME
Coverage target: All OWASP Top 10:2025 Release Candidate categories
```

**Line 357: Example OWASP category**
```markdown
# CURRENT
OWASP Category: A03:2021 Injection

# MUST BECOME
OWASP Category: A05:2025 Injection
```

**Lines 407-426: Section 3.3 - OWASP Coverage Table**
```markdown
# CURRENT
**OWASP Top 10 2021 Coverage**

The dataset covers all 10 OWASP Top 10 2021 categories plus 2 additional...
[Full table with 2021 categories]

# MUST BECOME
**OWASP Top 10:2025 Coverage**

The dataset covers 9 OWASP Top 10:2025 Release Candidate categories (A10:2021 SSRF merged into A01:2025) plus 2 additional...
[Full table with 2025 categories and renumbered positions]
```

**Line 611: Metadata field description**
```markdown
# CURRENT
- **owasp_category:** Valid OWASP Top 10 2021 category (or custom AI/ML Security category)

# MUST BECOME
- **owasp_category:** Valid OWASP Top 10:2025 category (or custom AI/ML Security category)
```

**Line 883: CVE sources**
```markdown
# CURRENT
NIST National Vulnerability Database, MITRE CVE List, OWASP Top 10 documentation

# MUST BECOME
NIST National Vulnerability Database, MITRE CVE List, OWASP Top 10:2025 Release Candidate
```

**Line 1027: Distribution priorities**
```markdown
# CURRENT
Distribution matches OWASP Top 10 threat priorities

# MUST BECOME
Distribution matches OWASP Top 10:2025 threat priorities
```

**Lines 1128, 1144: Use case descriptions**
```markdown
# CURRENT
Coverage of OWASP Top 10 aligns with CISSP, CEH, and OSCP certifications

# MUST BECOME
Coverage of OWASP Top 10:2025 aligns with CISSP, CEH, and OSCP certifications
```

**Line 1132: Category-specific fine-tuning**
```markdown
# CURRENT
Train injection prevention model on 125 injection examples (A03:2021)

# MUST BECOME
Train injection prevention model on 125 injection examples (A05:2025)
```

**Line 1318: References section**
```markdown
# CURRENT
[12] OWASP Foundation (2021). "OWASP Top 10 2021." Available: https://owasp.org/Top10/

# MUST BECOME
[12] OWASP Foundation (2025). "OWASP Top 10:2025 Release Candidate." Available: https://owasp.org/Top10/2025/
```

**Lines 1355, 1388: Schema examples**
```markdown
# CURRENT
"owasp_category": "A03:2021-Injection"

# MUST BECOME
"owasp_category": "A05:2025-Injection"
```

**Lines 1412-1421: Appendix B - Category Breakdown Table**
```markdown
# CURRENT (with 2021 categories)
| A07:2021 Auth Failures | 199 | 16.4% | ... |
| A01:2021 Broken Access Control | 179 | 14.7% | ... |
| A05:2021 Security Misconfiguration | 134 | 11.0% | ... |
| A03:2021 Injection | 125 | 10.3% | ... |
| A02:2021 Cryptographic Failures | 115 | 9.5% | ... |
| A06:2021 Vulnerable and Outdated Components | 85 | 7.0% | ... |
| A04:2021 Insecure Design | 84 | 6.9% | ... |
| A08:2021 Software and Data Integrity Failures | 80 | 6.6% | ... |
| A09:2021 Logging Failures | 59 | 4.9% | ... |

# MUST BECOME (with 2025 categories and renumbering)
| A07:2025 Authentication Failures | 199 | 16.4% | ... |
| A01:2025 Broken Access Control | 179 | 14.7% | ... |
| A02:2025 Security Misconfiguration | 134 | 11.0% | ... |
| A05:2025 Injection | 125 | 10.3% | ... |
| A04:2025 Cryptographic Failures | 115 | 9.5% | ... |
| A03:2025 Software Supply Chain Failures | 85 | 7.0% | ... |
| A06:2025 Insecure Design | 84 | 6.9% | ... |
| A08:2025 Software or Data Integrity Failures | 80 | 6.6% | ... |
| A09:2025 Security Logging & Alerting Failures | 59 | 4.9% | ... |
```

**Note on Line 426**: Update footnote to mention OWASP 2025 formal names vs internal slugs

**Total Locations in This File**: ~25-30 changes required

---

#### File 2: `taxonomy.yaml` (420 lines)
**Priority**: CRITICAL
**Impact**: Schema definition file used by validators and dataset tools

**Required Changes:**

Lines 2, 8, 66, 116, 172, 212, 258, 286, 338, 372, 402 - OWASP field mappings:

```yaml
# CURRENT (Line 8 - Authorization category)
owasp: "A01:2021-Broken Access Control"

# MUST BECOME
owasp: "A01:2025-Broken Access Control"

# CURRENT (Line 66 - Cryptography category)
owasp: "A02:2021-Cryptographic Failures"

# MUST BECOME
owasp: "A04:2025-Cryptographic Failures"

# CURRENT (Line 116 - SQL Injection under Injection)
owasp: "A03:2021-Injection"

# MUST BECOME
owasp: "A05:2025-Injection"

# CURRENT (Line 172 - Design Flaws)
owasp: "A04:2021-Insecure Design"

# MUST BECOME
owasp: "A06:2025-Insecure Design"

# CURRENT (Line 212 - Misconfiguration)
owasp: "A05:2021-Security Misconfiguration"

# MUST BECOME
owasp: "A02:2025-Security Misconfiguration"

# CURRENT (Line 258 - Dependencies)
owasp: "A06:2021-Vulnerable and Outdated Components"

# MUST BECOME
owasp: "A03:2025-Software Supply Chain Failures"

# CURRENT (Line 286 - Authentication)
owasp: "A07:2021-Identification and Authentication Failures"

# MUST BECOME
owasp: "A07:2025-Authentication Failures"

# CURRENT (Line 338 - Integrity)
owasp: "A08:2021-Software and Data Integrity Failures"

# MUST BECOME
owasp: "A08:2025-Software or Data Integrity Failures"

# CURRENT (Line 372 - Logging)
owasp: "A09:2021-Security Logging and Monitoring Failures"

# MUST BECOME
owasp: "A09:2025-Security Logging & Alerting Failures"

# CURRENT (Line 402 - SSRF)
owasp: "A10:2021-Server-Side Request Forgery"

# MUST BECOME
owasp: "A01:2025-Broken Access Control"
# NOTE: SSRF merged into Access Control in 2025
```

**Total Changes**: 11 OWASP field updates

---

#### File 3: `canonical_counts.json`
**Priority**: CRITICAL
**Impact**: Ground truth for all dataset statistics

**Required Changes:**

Line 55-67: Update `by_owasp_2021` key to `by_owasp_2025`:

```json
// CURRENT
"by_owasp_2021": {
    "A07:2021-Identification and Authentication Failures": 199,
    "A01:2021-Broken Access Control": 179,
    "A02:2021-Cryptographic Failures": 115,
    "A05:2021-Security Misconfiguration": 134,
    "A03:2021-Injection": 125,
    "A04:2021-Insecure Design": 84,
    "A06:2021-Vulnerable and Outdated Components": 85,
    "A09:2021-Security Logging and Monitoring Failures": 59,
    "A08:2021-Software and Data Integrity Failures": 80
}

// MUST BECOME
"by_owasp_2025": {
    "A07:2025-Authentication Failures": 199,
    "A01:2025-Broken Access Control": 179,
    "A04:2025-Cryptographic Failures": 115,
    "A02:2025-Security Misconfiguration": 134,
    "A05:2025-Injection": 125,
    "A06:2025-Insecure Design": 84,
    "A03:2025-Software Supply Chain Failures": 85,
    "A09:2025-Security Logging & Alerting Failures": 59,
    "A08:2025-Software or Data Integrity Failures": 80
}
```

**Note**: Consider keeping both `by_owasp_2021` and `by_owasp_2025` for backwards compatibility, or add migration note.

---

### 🟡 TIER 2: HIGH PRIORITY - Update Before Dataset Release

#### File 4: `CONTRIBUTING.md` (187 lines)
**Priority**: HIGH
**Impact**: Contributor guidelines

**Required Changes:**

**Line 51: Metadata requirements**
```markdown
# CURRENT
- `owasp_2021` – One or more OWASP Top 10 2021 categories, such as:

# MUST BECOME
- `owasp_2025` – One or more OWASP Top 10:2025 categories, such as:
```

**Lines 52-62: Category list** (update all 10 categories to 2025 versions)

**Line 162: Coverage balance note**
```markdown
# CURRENT
We maintain a roughly balanced distribution across OWASP Top 10 2021 categories.

# MUST BECOME
We maintain a roughly balanced distribution across OWASP Top 10:2025 categories.
```

**Total Changes**: ~15 locations

---

#### File 5: `README.md` (426 lines)
**Priority**: HIGH
**Impact**: Primary dataset documentation on HuggingFace

**Required Changes:**

**Line 409: Acknowledgments**
```markdown
# CURRENT
- OWASP Foundation

# COULD ADD
- OWASP Foundation (OWASP Top 10:2025 taxonomy)
```

**Note**: README doesn't explicitly list OWASP categories, but validator references OWASP 2021. May need update note in changelog.

**Recommended Addition** (new section or changelog):
```markdown
### OWASP Taxonomy Version

SecureCode v2.0 follows the **OWASP Top 10:2025 Release Candidate** taxonomy (released November 2025). The dataset was originally created using OWASP 2021 categories and subsequently remapped to align with current industry standards.

Key changes from OWASP 2021:
- A10:2021 SSRF merged into A01:2025 Broken Access Control
- A06:2021 renamed to A03:2025 Software Supply Chain Failures
- Several categories renumbered (see taxonomy.yaml for complete mapping)
```

---

#### File 6: `validate_contributing_compliance.py` (Python validator)
**Priority**: HIGH
**Impact**: Dataset validation, CI/CD checks

**Required Changes:**

**Lines 36-47: VALID_OWASP_CATEGORIES constant**
```python
# CURRENT (Line 36-46)
# Valid OWASP categories (2021)
VALID_OWASP_CATEGORIES = {
    'A01:2021-Broken Access Control',
    'A02:2021-Cryptographic Failures',
    'A03:2021-Injection',
    'A04:2021-Insecure Design',
    'A05:2021-Security Misconfiguration',
    'A06:2021-Vulnerable and Outdated Components',
    'A07:2021-Identification and Authentication Failures',
    'A08:2021-Software and Data Integrity Failures',
    'A09:2021-Security Logging and Monitoring Failures',
    'A10:2021-Server-Side Request Forgery (SSRF)',
    'A10:2021-Server-Side Request Forgery',
    'AI/ML Security Threats',
    'Unknown'
}

# MUST BECOME
# Valid OWASP categories (2025 Release Candidate)
VALID_OWASP_CATEGORIES = {
    'A01:2025-Broken Access Control',
    'A02:2025-Security Misconfiguration',
    'A03:2025-Software Supply Chain Failures',
    'A04:2025-Cryptographic Failures',
    'A05:2025-Injection',
    'A06:2025-Insecure Design',
    'A07:2025-Authentication Failures',
    'A08:2025-Software or Data Integrity Failures',
    'A09:2025-Security Logging & Alerting Failures',
    'AI/ML Security Threats',
    'Unknown'
}
```

**Note**: Remove A10:2021 SSRF entries entirely (merged into A01:2025).

**Consider backwards compatibility**: Add both 2021 and 2025 categories temporarily with deprecation warning.

---

#### File 7: `VALIDATOR_V2_README.md` (499 lines)
**Priority**: HIGH
**Impact**: Validator documentation

**Required Changes:**

**Lines 187, 199: Example metadata**
```markdown
# CURRENT
"owasp_category": "A03:2021-Injection",
"owasp_2021": "A03:2021-Injection",

# MUST BECOME
"owasp_category": "A05:2025-Injection",
"owasp_2025": "A05:2025-Injection",
```

**Lines 212-223: Valid categories section**
```markdown
# CURRENT
Valid categories (OWASP 2021 Top 10):
- `A01:2021-Broken Access Control`
[... full 2021 list ...]

# MUST BECOME
Valid categories (OWASP 2025 Top 10):
- `A01:2025-Broken Access Control`
- `A02:2025-Security Misconfiguration`
- `A03:2025-Software Supply Chain Failures`
- `A04:2025-Cryptographic Failures`
- `A05:2025-Injection`
- `A06:2025-Insecure Design`
- `A07:2025-Authentication Failures`
- `A08:2025-Software or Data Integrity Failures`
- `A09:2025-Security Logging & Alerting Failures`
- `AI/ML Security Threats` (custom category)
- `Unknown` (edge cases)
```

**Line 425: Troubleshooting example**
```markdown
# CURRENT
**Issue: "Invalid OWASP category: 'A10:2021-Server-Side Request Forgery'"**
- Solution: This should pass in v2. Ensure you're using the updated validator.

# MUST BECOME
**Issue: "Invalid OWASP category: 'A10:2021-Server-Side Request Forgery'"**
- Solution: A10:2021 SSRF was merged into A01:2025 Broken Access Control in OWASP 2025. Update category to A01:2025.
```

**Total Changes**: ~15-20 locations

---

### 🟢 TIER 3: MODERATE - Update for Consistency

#### File 8: `FOURTH_REVIEW_FIXES_APPLIED.md` (339 lines)
**Priority**: MODERATE
**Impact**: Historical fix log (archival)

**Required Changes:**

**Lines 208-213: Fix #15 documentation**
```markdown
# CURRENT
### Fix #15: OWASP A07 Naming Corrected ✅
**Problem**: OWASP A07:2021 not using official name "Identification and Authentication Failures".

**Fix Applied**:
- **Line 62**: Changed to "A07:2021 Identification and Authentication Failures"

# CONSIDER ADDING NOTE
### Fix #15: OWASP A07 Naming Corrected (Now A07:2025) ✅
**Note**: This fix applied A07:2021 naming. Subsequent updates aligned with OWASP 2025 (A07:2025 Authentication Failures).
```

**Total Changes**: 2-3 clarification notes

---

#### File 9: `FINAL_SUBMISSION_READY.md` (269 lines)
**Priority**: MODERATE
**Impact**: Status report (archival)

**Required Changes:**

**Line 125: Footnote about taxonomy**
```markdown
# CURRENT
"*Note: The paper uses OWASP's formal category names (e.g., 'A07:2021 Identification and Authentication Failures')..."

# MUST BECOME
"*Note: The paper uses OWASP's formal category names (e.g., 'A07:2025 Authentication Failures')..."
```

**Total Changes**: 1-2 locations

---

#### File 10: `VALIDATOR_V2_PAPER_UPDATES.md` (279 lines)
**Priority**: MODERATE
**Impact**: Paper update instructions

**No direct OWASP 2021 references found** - focuses on validator changes (CVE format, content length naming).

---

#### File 11: `ACADEMIC_PAPER_OUTLINE.md` (450+ lines)
**Priority**: LOW
**Impact**: Outline/planning document

**Required Changes:**

**Line 60: Feature list**
```markdown
# CURRENT
- 11 OWASP Top 10 2021 categories

# MUST BECOME
- 9 OWASP Top 10:2025 categories (A10:2021 merged into A01:2025)
```

**Line 175: Coverage header**
```markdown
# CURRENT
**OWASP Top 10 2021 Coverage**:

# MUST BECOME
**OWASP Top 10:2025 Coverage**:
```

**Line 442: References**
```markdown
# CURRENT
[3] OWASP Foundation. (2021). "OWASP Top 10 2021."

# MUST BECOME
[3] OWASP Foundation. (2025). "OWASP Top 10:2025 Release Candidate."
```

**Total Changes**: 5-8 locations

---

#### Files 12-14: Review Fix Logs
**Priority**: LOW
**Impact**: Historical documentation

**Files**:
- `REVIEWER_PROOFING_FIXES_APPLIED.md`
- `THIRD_REVIEW_FIXES_APPLIED.md`
- `MUST_FIX_CORRECTIONS_APPLIED.md`

**Approach**: Add header note explaining OWASP 2025 migration occurred after these reviews.

**Example Note to Add:**
```markdown
---
**OWASP Taxonomy Update Note**: This review was conducted using OWASP Top 10:2021 taxonomy.
Subsequent updates aligned the dataset with OWASP Top 10:2025 Release Candidate (November 2025).
See OWASP_2025_UPDATE_ANALYSIS.md for complete migration details.
---
```

---

### ✅ TIER 4: REFERENCE FILES - Already Correct

#### File 15: `owasp_reference/OWASP_2021_vs_2025_Comparison.md`
**Status**: ✅ COMPLETE - Comprehensive migration guide exists
**Purpose**: Authoritative mapping document
**No changes needed** - this IS the change guide

#### File 16: `owasp_reference/OWASP_2025_Summary.md`
**Status**: ✅ COMPLETE - OWASP 2025 reference documentation
**No changes needed**

#### File 17: `owasp_reference/OWASP_2021_Full.md`
**Status**: ✅ ARCHIVAL - Historical reference
**No changes needed** - keep for reference

---

## 3. Priority Assessment - Recommended Update Sequence

### Phase 0: Dataset Migration (MUST DO FIRST)
**Timeline**: Complete before updating any documentation

**Dataset Files (3 JSONL files, 2,418 examples total):**
1. **`consolidated/train.jsonl`** - 1,934 examples
2. **`consolidated/test.jsonl`** - 241 examples
3. **`consolidated/val.jsonl`** - 243 examples

**Required Changes in Each Example:**
- Field name: `owasp_2021` → `owasp_2025`
- Category mappings (per CATEGORY_MAPPING table):
  - `A01:2021-Broken Access Control` → `A01:2025-Broken Access Control`
  - `A02:2021-Cryptographic Failures` → `A04:2025-Cryptographic Failures`
  - `A03:2021-Injection` → `A05:2025-Injection`
  - `A04:2021-Insecure Design` → `A06:2025-Insecure Design`
  - `A05:2021-Security Misconfiguration` → `A02:2025-Security Misconfiguration`
  - `A06:2021-Vulnerable and Outdated Components` → `A03:2025-Software Supply Chain Failures`
  - `A07:2021-Identification and Authentication Failures` → `A07:2025-Authentication Failures`
  - `A08:2021-Software and Data Integrity Failures` → `A08:2025-Software or Data Integrity Failures`
  - `A09:2021-Security Logging and Monitoring Failures` → `A09:2025-Security Logging & Alerting Failures`
  - `A10:2021-Server-Side Request Forgery` → `A01:2025-Broken Access Control` (MERGED)

**Recommended Approach**: Automated Python script with validation

**Script Template**:
```python
#!/usr/bin/env python3
"""Migrate dataset from OWASP 2021 to OWASP 2025"""

import json
import shutil
from pathlib import Path

CATEGORY_MAPPING = {
    'A01:2021-Broken Access Control': 'A01:2025-Broken Access Control',
    'A02:2021-Cryptographic Failures': 'A04:2025-Cryptographic Failures',
    'A03:2021-Injection': 'A05:2025-Injection',
    'A04:2021-Insecure Design': 'A06:2025-Insecure Design',
    'A05:2021-Security Misconfiguration': 'A02:2025-Security Misconfiguration',
    'A06:2021-Vulnerable and Outdated Components': 'A03:2025-Software Supply Chain Failures',
    'A07:2021-Identification and Authentication Failures': 'A07:2025-Authentication Failures',
    'A08:2021-Software and Data Integrity Failures': 'A08:2025-Software or Data Integrity Failures',
    'A09:2021-Security Logging and Monitoring Failures': 'A09:2025-Security Logging & Alerting Failures',
    'A10:2021-Server-Side Request Forgery': 'A01:2025-Broken Access Control',
    'A10:2021-Server-Side Request Forgery (SSRF)': 'A01:2025-Broken Access Control',
}

def migrate_example(example):
    """Migrate a single example from 2021 to 2025"""
    modified = False

    # Update owasp_2021 field name to owasp_2025
    if 'owasp_2021' in example:
        example['owasp_2025'] = example.pop('owasp_2021')
        modified = True

    # Update category value
    if 'owasp_2025' in example:
        old_cat = example['owasp_2025']
        if old_cat in CATEGORY_MAPPING:
            example['owasp_2025'] = CATEGORY_MAPPING[old_cat]
            modified = True

    return example, modified

def migrate_file(input_path, output_path, backup=True):
    """Migrate entire JSONL file"""
    input_path = Path(input_path)
    output_path = Path(output_path)

    # Create backup
    if backup:
        backup_path = input_path.with_suffix('.jsonl.owasp2021_backup')
        shutil.copy2(input_path, backup_path)
        print(f"✓ Backup created: {backup_path}")

    # Migrate examples
    migrated_count = 0
    total_count = 0

    with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
        for line in f_in:
            example = json.loads(line)
            migrated_example, modified = migrate_example(example)

            if modified:
                migrated_count += 1
            total_count += 1

            f_out.write(json.dumps(migrated_example) + '\n')

    print(f"✓ Migrated {input_path.name}: {migrated_count}/{total_count} examples updated")
    return migrated_count, total_count

# Run migration
files = [
    'consolidated/train.jsonl',
    'consolidated/test.jsonl',
    'consolidated/val.jsonl'
]

for filepath in files:
    migrate_file(filepath, filepath, backup=True)
```

**Validation After Migration**:
```bash
# Verify no 2021 references remain
grep -o 'A0[0-9]:2021' consolidated/*.jsonl
# Should return ZERO results

# Verify 2025 categories present
grep -o 'A0[0-9]:2025' consolidated/*.jsonl | sort | uniq -c
# Should show expected distribution

# Re-run dataset validator
python validate_contributing_compliance.py consolidated/train.jsonl
```

**Blocker**: Dataset must be migrated BEFORE updating documentation to maintain consistency.

---

### Phase 1: Critical Foundation (MUST DO SECOND)
**Timeline**: Complete before ANY dataset publication/paper submission

1. **`taxonomy.yaml`** - Schema definition (11 OWASP field updates)
2. **`canonical_counts.json`** - Ground truth statistics (rename key, update 9 categories)
3. **`validate_contributing_compliance.py`** - Validator logic (update constant + comments)

**Blocker**: These 3 files are foundational. Everything else depends on them.

---

### Phase 2: Paper Submission (BEFORE USENIX SUBMISSION)
**Timeline**: Must complete before paper submission

4. **`COMPLETE_PAPER_DRAFT.md`** - Main submission document (~25-30 changes)
   - Abstract category list (lines 62-71)
   - All section headings referencing "OWASP 2021"
   - All tables with category breakdowns
   - All inline category references
   - Reference list citation

**Critical Path**: Paper cannot be submitted with 2021 taxonomy if dataset uses 2025.

---

### Phase 3: Public Documentation (BEFORE HUGGINGFACE RELEASE)
**Timeline**: Complete before HuggingFace publication

5. **`CONTRIBUTING.md`** - Contributor guidelines (~15 changes)
6. **`VALIDATOR_V2_README.md`** - Validator documentation (~15-20 changes)
7. **`README.md`** - Add OWASP version note to changelog

**User Impact**: Contributors and users will reference these daily.

---

### Phase 4: Historical Documentation (CLEANUP)
**Timeline**: Can be done after release, but recommended before

8. **`FOURTH_REVIEW_FIXES_APPLIED.md`** - Add migration note
9. **`FINAL_SUBMISSION_READY.md`** - Update taxonomy footnote
10. **`ACADEMIC_PAPER_OUTLINE.md`** - Update outline (~5-8 changes)
11. **Review fix logs** - Add header migration notes

**Low Impact**: These are archival/historical records.

---

## 4. Orphaned References - Potential Issues

### Issue 1: A10:2021 SSRF References
**Problem**: SSRF (A10:2021) eliminated in OWASP 2025, merged into A01:2025 Broken Access Control

**Affected**:
- Paper abstract (if SSRF mentioned separately)
- Validator constant `VALID_OWASP_CATEGORIES`
- Any documentation listing "10 OWASP categories"

**Fix**:
- Remove A10:2021 entries
- Merge SSRF discussion into A01:2025 Broken Access Control
- Update "10 categories" to "9 categories" (with footnote explaining SSRF merger)

---

### Issue 2: Category Number Changes
**Problem**: Major renumbering in OWASP 2025

**Mapping Table** (from comparison guide):
```
A02:2021 → A04:2025 (Cryptographic Failures)
A03:2021 → A05:2025 (Injection)
A04:2021 → A06:2025 (Insecure Design)
A05:2021 → A02:2025 (Security Misconfiguration) ⚠️ MOVES UP
A06:2021 → A03:2025 (Supply Chain Failures) ⚠️ RENAME + MOVE UP
```

**Risk**: Simple find-replace will break if not done carefully.

**Recommended Approach**:
1. Create migration script with explicit mappings
2. Manual verification of each change
3. Diff review before committing

---

### Issue 3: "and" vs "or" in A08 Name
**Problem**: A08:2021 "Software **and** Data Integrity" → A08:2025 "Software **or** Data Integrity"

**Affected**: Every reference to A08

**Fix**: Update wording in all locations (subtle but important change)

---

### Issue 4: Dataset Files Use 2021 (Verification Complete)
**Verification Results**:

**Evidence from grep analysis**:
```bash
# Train set OWASP category distribution
156 A01:2021
 95 A02:2021
 91 A03:2021
 67 A04:2021
118 A05:2021
 76 A06:2021
148 A07:2021
 60 A08:2021
 44 A09:2021

# Sample from actual dataset
"owasp_2021": "A07:2021-Identification and Authentication Failures"
"owasp_2021": "A01:2021-Broken Access Control"
```

**Implication**: Dataset JSONL files use OWASP 2021, matching documentation.

**Action Required**:
- Complete migration needed: Dataset files + all documentation
- Update JSONL files: Change all `owasp_2021` fields to `owasp_2025` with updated categories
- This is GOOD NEWS: Consistent migration across everything, not piecemeal
- Priority remains CRITICAL but scope is clear

---

## 5. Recommendations - Action Plan

### Immediate Actions (This Week)

**1. Dataset Files Verified** ✅
```bash
# Verification completed - dataset uses OWASP 2021
grep -o 'A0[0-9]:202[0-9]' consolidated/*.jsonl | sort | uniq -c

# Results show A01:2021 through A09:2021
# Action: Create migration script to update all 2,418 examples
```

**2. Create Backup Branch**
```bash
git checkout -b owasp-2025-migration
git add -A
git commit -m "Pre-OWASP 2025 migration backup"
```

**3. Run Phase 1 Updates**
- Update `taxonomy.yaml` (11 OWASP mappings)
- Update `canonical_counts.json` (rename key + 9 categories)
- Update validator constant in `validate_contributing_compliance.py`
- Test validator against dataset to ensure no breakage

**4. Run Validation**
```bash
# Ensure validator still works after OWASP updates
python validate_contributing_compliance.py consolidated/train.jsonl
python validate_contributing_compliance.py consolidated/test.jsonl
python validate_contributing_compliance.py consolidated/val.jsonl
```

---

### Next Week Actions

**5. Update Paper** (`COMPLETE_PAPER_DRAFT.md`)
- Use comparison guide as reference
- Update all ~25-30 OWASP references
- Add footnote explaining OWASP 2025 adoption
- Run final QA check

**6. Update Public Documentation**
- `CONTRIBUTING.md`
- `VALIDATOR_V2_README.md`
- `README.md` changelog

**7. Final Validation**
```bash
# Ensure all OWASP 2021 references eliminated
grep -r "A0[0-9]:2021" . --include="*.md" --include="*.py" --include="*.yaml" --include="*.json"

# Should return ZERO results (except in owasp_reference/ archival docs)
```

---

### Pre-Submission Checklist

- [ ] Dataset files verified (train/test/val use 2025)
- [ ] `taxonomy.yaml` updated (11 mappings)
- [ ] `canonical_counts.json` updated (key renamed + 9 categories)
- [ ] Validator updated and tested
- [ ] Paper (`COMPLETE_PAPER_DRAFT.md`) fully updated (~25-30 changes)
- [ ] `CONTRIBUTING.md` updated (~15 changes)
- [ ] `VALIDATOR_V2_README.md` updated (~15-20 changes)
- [ ] `README.md` changelog updated
- [ ] No orphaned A10:2021 SSRF references remain
- [ ] All "10 categories" changed to "9 categories" (with SSRF merger note)
- [ ] Grep search confirms zero "A0[0-9]:2021" in active docs
- [ ] Final paper QA pass (verify all category numbers correct)
- [ ] Dataset re-validated with updated validator

---

## 6. Risk Assessment

### HIGH RISK: Dataset-Documentation Mismatch

**Finding**: Dataset files use OWASP 2025, but ALL documentation uses OWASP 2021.

**Risk**:
- Paper submitted with 2021 taxonomy while dataset uses 2025
- Reviewers notice inconsistency → credibility damage
- Dataset users confused by mismatched documentation

**Mitigation**:
- URGENT update of all documentation to 2025
- Add migration note explaining taxonomy alignment
- Re-validate all statistics match

---

### MEDIUM RISK: Reference Renumbering Errors

**Risk**: Mass find-replace could create errors (e.g., A02→A04 but context still says "number 2")

**Mitigation**:
- Manual verification of each change
- Careful review of prose text surrounding category numbers
- Test with example: "A02 (second most critical)" should become "A04 (fourth most critical)"

---

### LOW RISK: Historical Documentation Confusion

**Risk**: Old review documents reference 2021, new docs reference 2025

**Mitigation**:
- Add header notes to historical docs explaining migration
- Keep chronological documentation trail clear
- Archive OWASP 2021 reference docs for posterity

---

## 7. Automated Update Script Recommendation

**Suggested**: Create Python migration script for safety

```python
#!/usr/bin/env python3
"""OWASP 2021 → 2025 Migration Script"""

CATEGORY_MAPPING = {
    'A01:2021-Broken Access Control': 'A01:2025-Broken Access Control',
    'A02:2021-Cryptographic Failures': 'A04:2025-Cryptographic Failures',
    'A03:2021-Injection': 'A05:2025-Injection',
    'A04:2021-Insecure Design': 'A06:2025-Insecure Design',
    'A05:2021-Security Misconfiguration': 'A02:2025-Security Misconfiguration',
    'A06:2021-Vulnerable and Outdated Components': 'A03:2025-Software Supply Chain Failures',
    'A07:2021-Identification and Authentication Failures': 'A07:2025-Authentication Failures',
    'A08:2021-Software and Data Integrity Failures': 'A08:2025-Software or Data Integrity Failures',
    'A09:2021-Security Logging and Monitoring Failures': 'A09:2025-Security Logging & Alerting Failures',
    'A10:2021-Server-Side Request Forgery': 'A01:2025-Broken Access Control',  # MERGED
}

def migrate_file(filepath):
    """Migrate OWASP references in a single file"""
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    for old_cat, new_cat in CATEGORY_MAPPING.items():
        content = content.replace(old_cat, new_cat)

    # Update generic references
    content = content.replace('OWASP Top 10 2021', 'OWASP Top 10:2025 Release Candidate')
    content = content.replace('OWASP Top 10:2021', 'OWASP Top 10:2025 Release Candidate')
    content = content.replace('owasp_2021', 'owasp_2025')
    content = content.replace('by_owasp_2021', 'by_owasp_2025')

    if content != original:
        print(f"✓ Updated: {filepath}")
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

# Run on all target files
# ...
```

**Benefits**:
- Consistent application of mappings
- Audit trail of changes
- Easy rollback if needed

**Caution**: Still requires manual review of each changed file.

---

## 8. Final Summary

### Current State
- ❌ **12+ documentation files use OWASP 2021**
- ❌ **Dataset files (2,418 examples) use OWASP 2021** (verified: train.jsonl shows A01:2021-A09:2021)
- ✅ **Comparison guide exists** (comprehensive 580-line migration reference)
- ✅ **Consistent state**: Everything uses 2021, so complete migration possible

### Required Work
- **Phase 0 (Dataset)**: 3 files (train.jsonl, test.jsonl, val.jsonl) - ~2,418 example metadata updates
- **Phase 1 (Critical)**: 3 files (taxonomy.yaml, canonical_counts.json, validator) - ~30 changes
- **Phase 2 (Paper)**: 1 file (COMPLETE_PAPER_DRAFT.md) - ~25-30 changes
- **Phase 3 (Public)**: 3 files (CONTRIBUTING.md, VALIDATOR_V2_README.md, README.md) - ~30 changes
- **Phase 4 (Historical)**: 4 files (review logs) - ~10 notes

**Total Estimated Changes**: 2,500+ locations (2,418 dataset examples + 100-110 documentation locations) across 14 files

### Timeline Estimate
- **Phase 0**: 1-2 hours (automated script to update 2,418 JSONL examples + validation)
- **Phase 1**: 2-3 hours (careful YAML/JSON editing + validator testing)
- **Phase 2**: 3-4 hours (paper requires careful review of prose context)
- **Phase 3**: 2-3 hours (straightforward documentation updates)
- **Phase 4**: 1 hour (simple header notes)

**Total**: 9-13 hours of focused work (mostly automated for dataset files)

### Recommended Start
**IMMEDIATELY** - Dataset-documentation mismatch is a critical blocker for:
- Paper submission
- Dataset publication
- Validator accuracy
- User trust

---

## Appendix A: Quick Reference - Category Mapping

| 2021 Category | 2021 # | → | 2025 Category | 2025 # | Change Type |
|---------------|--------|---|---------------|--------|-------------|
| Broken Access Control | A01 | → | Broken Access Control | A01 | SAME |
| Cryptographic Failures | A02 | → | Cryptographic Failures | A04 | NUMBER CHANGE |
| Injection | A03 | → | Injection | A05 | NUMBER CHANGE |
| Insecure Design | A04 | → | Insecure Design | A06 | NUMBER CHANGE |
| Security Misconfiguration | A05 | → | Security Misconfiguration | A02 | NUMBER CHANGE |
| Vulnerable Components | A06 | → | Supply Chain Failures | A03 | NAME + NUMBER |
| Ident. & Auth. Failures | A07 | → | Authentication Failures | A07 | NAME ONLY |
| Software and Data Integrity | A08 | → | Software or Data Integrity | A08 | NAME ONLY |
| Logging & Monitoring | A09 | → | Logging & Alerting | A09 | NAME ONLY |
| SSRF | A10 | → | ~~ELIMINATED~~ | - | MERGED INTO A01 |

---

**Report Complete**
**Next Action**: Begin Phase 1 updates immediately (taxonomy.yaml, canonical_counts.json, validator)
**Blocker**: Paper cannot be submitted until documentation aligns with dataset taxonomy

---

**Document Version**: 1.0
**Last Updated**: 2025-12-16
**Prepared By**: Claude Code (Anthropic)
