# OWASP Top 10: 2021 vs. 2025 Release Candidate
## Detailed Comparison and Remapping Guide for SecureCode v2.0 Paper

**Analysis Date**: December 16, 2025
**Purpose**: Guide remapping of SecureCode v2.0 paper from OWASP 2021 to OWASP 2025 Release Candidate

---

## Executive Summary

### Critical Changes for SecureCode v2.0 Paper

1. **A10:2021 SSRF (45 examples in paper) → NOW PART OF A01:2025 Broken Access Control**
   - Category no longer exists as standalone
   - All 45 SSRF examples must be remapped to A01:2025

2. **A06:2021 Vulnerable and Outdated Components (85 examples) → NOW A03:2025 Software Supply Chain Failures**
   - Scope greatly expanded beyond just "outdated components"
   - Now includes entire supply chain ecosystem (build systems, CI/CD, distribution)
   - Category moved from #6 to #3 (significantly higher priority)

3. **New A10:2025 - Mishandling of Exceptional Conditions**
   - Completely new category (24 CWEs)
   - Paper may need to identify if any examples fit this category

4. **All Category Numbers Shifted**
   - Every category reference in paper needs updating
   - Methodology section needs revision to reflect 2025 changes

---

## Complete Category Mapping: 2021 → 2025

### Category-by-Category Analysis

#### A01: Broken Access Control
**2021**: A01:2021 - Broken Access Control (34 CWEs mapped)
**2025**: A01:2025 - Broken Access Control (40 CWEs mapped)
**Status**: ✅ STAYS #1
**Change Type**: **EXPANDED SCOPE** - SSRF rolled into this category
**CWE Changes**: 34 CWEs → 40 CWEs (added CWE-918 SSRF + 5 others)

**Impact on SecureCode v2.0 Paper**:
- Paper category: "A01:2021 Broken Access Control" → "A01:2025 Broken Access Control"
- Example count: Likely increases (paper's A10 SSRF examples should merge here)
- **ACTION REQUIRED**: Review paper's 45 A10:2021 SSRF examples - should these be recategorized as A01:2025?

---

#### A02: Cryptographic Failures
**2021**: A02:2021 - Cryptographic Failures (29 CWEs)
**2025**: A04:2025 - Cryptographic Failures (32 CWEs)
**Status**: ⬇️ DOWN from #2 → #4
**Change Type**: Minor CWE expansion, major position change
**CWE Changes**: 29 CWEs → 32 CWEs

**Impact on SecureCode v2.0 Paper**:
- Paper reference: "A02:2021" → "A04:2025"
- Position change indicates relative priority shift (still critical, but 3 categories ranked higher)
- **ACTION REQUIRED**: Update all "A02:2021 Cryptographic Failures" → "A04:2025 Cryptographic Failures"

---

#### A03: Injection
**2021**: A03:2021 - Injection (33 CWEs)
**2025**: A05:2025 - Injection (38 CWEs)
**Status**: ⬇️ DOWN from #3 → #5
**Change Type**: CWE expansion, position drop
**CWE Changes**: 33 CWEs → 38 CWEs (5 additional CWEs)

**Impact on SecureCode v2.0 Paper**:
- Paper reference: "A03:2021" → "A05:2025"
- Category scope expanded (more CWEs)
- Includes SQL Injection, XSS, Command Injection, LDAP, NoSQL (same as before)
- **ACTION REQUIRED**: Update all "A03:2021 Injection" → "A05:2025 Injection"

---

#### A04: Insecure Design
**2021**: A04:2021 - Insecure Design (39 CWEs)
**2025**: A06:2025 - Insecure Design (39 CWEs)
**Status**: ⬇️ DOWN from #4 → #6
**Change Type**: Position change only
**CWE Changes**: Same 39 CWEs
**Notable**: OWASP notes "Noticeable improvements in industry related to threat modeling"

**Impact on SecureCode v2.0 Paper**:
- Paper reference: "A04:2021" → "A06:2025"
- Same scope, different number
- **ACTION REQUIRED**: Update all "A04:2021 Insecure Design" → "A06:2025 Insecure Design"

---

#### A05: Security Misconfiguration
**2021**: A05:2021 - Security Misconfiguration (20 CWEs, was #5)
**2025**: A02:2025 - Security Misconfiguration (16 CWEs, now #2)
**Status**: ⬆️ UP from #5 → #2 (MAJOR JUMP)
**Change Type**: **SIGNIFICANT PRIORITY INCREASE**
**CWE Changes**: 20 CWEs → 16 CWEs
**Why It Moved Up**: "100% of applications tested had some form of misconfiguration"

**Impact on SecureCode v2.0 Paper**:
- Paper reference: "A05:2021" → "A02:2025"
- **MAJOR SIGNIFICANCE CHANGE** - now #2 risk (was #5)
- Paper should emphasize this is now 2nd highest priority vulnerability
- **ACTION REQUIRED**: Update all "A05:2021 Security Misconfiguration" → "A02:2025 Security Misconfiguration"
- **CONSIDER**: Adding narrative about dramatic priority increase in methodology section

---

#### A06: Vulnerable and Outdated Components
**2021**: A06:2021 - Vulnerable and Outdated Components (3 CWEs, was #6)
**2025**: A03:2025 - Software Supply Chain Failures (5 CWEs, now #3)
**Status**: ⬆️ UP from #6 → #3 + **MAJOR SCOPE EXPANSION**
**Change Type**: **CRITICALLY IMPORTANT** - Scope greatly expanded, name changed, major priority increase
**CWE Changes**: 3 CWEs → 5 CWEs (added CWE-1104, CWE-1329, CWE-1395)
**Scope Expansion**: Now includes entire supply chain ecosystem:
- Build systems
- Distribution mechanisms
- CI/CD pipelines
- Dependency management
- All supply chain infrastructure

**Community Priority**: 50% of survey respondents ranked this #1

**Impact on SecureCode v2.0 Paper**:
- Paper category: "A06:2021 Vulnerable and Outdated Components" (85 examples, 7.0%)
- **MUST BECOME**: "A03:2025 Software Supply Chain Failures"
- **CRITICAL**: Verify 85 examples still fit expanded scope
- Scope now much broader than just "outdated libraries"
- **ACTION REQUIRED**:
  1. Update all "A06:2021" → "A03:2025"
  2. Change name from "Vulnerable and Outdated Components" → "Software Supply Chain Failures"
  3. Review all 85 examples - do they fit expanded scope?
  4. Update methodology discussion to reflect scope expansion

---

#### A07: Identification and Authentication Failures
**2021**: A07:2021 - Identification and Authentication Failures (36 CWEs)
**2025**: A07:2025 - Authentication Failures (36 CWEs)
**Status**: ✅ STAYS #7
**Change Type**: **NAME SIMPLIFIED** - "Identification and" removed
**CWE Changes**: Same 36 CWEs

**Impact on SecureCode v2.0 Paper**:
- Paper reference: "A07:2021 Identification and Authentication Failures"
- **MUST BECOME**: "A07:2025 Authentication Failures"
- **ACTION REQUIRED**: Update name (remove "Identification and" from all references)

---

#### A08: Software and Data Integrity Failures
**2021**: A08:2021 - Software and Data Integrity Failures (14 CWEs)
**2025**: A08:2025 - Software **or** Data Integrity Failures (14 CWEs)
**Status**: ✅ STAYS #8
**Change Type**: **MINOR NAME CHANGE** - "and" → "or"
**CWE Changes**: Same 14 CWEs
**Focus**: Lower-level integrity failures than supply chain (insecure deserialization, unsigned updates)

**Impact on SecureCode v2.0 Paper**:
- Paper reference: "A08:2021 Software and Data Integrity Failures"
- **MUST BECOME**: "A08:2025 Software **or** Data Integrity Failures"
- **ACTION REQUIRED**: Change "and" → "or" in all references

---

#### A09: Security Logging and Monitoring Failures
**2021**: A09:2021 - Security Logging and Monitoring Failures (5 CWEs)
**2025**: A09:2025 - Security Logging **&** Alerting Failures (5 CWEs)
**Status**: ✅ STAYS #9
**Change Type**: **EMPHASIS CHANGE** - added "Alerting"
**CWE Changes**: Same 5 CWEs
**Emphasis**: "Great logging with no alerting is of minimal value"

**Impact on SecureCode v2.0 Paper**:
- Paper reference: "A09:2021 Security Logging and Monitoring Failures"
- **MUST BECOME**: "A09:2025 Security Logging & Alerting Failures"
- **ACTION REQUIRED**: Update to add "& Alerting" emphasis

---

#### A10: Server-Side Request Forgery (SSRF)
**2021**: A10:2021 - Server-Side Request Forgery (SSRF) - **STANDALONE CATEGORY**
**2025**: **CATEGORY ELIMINATED** - Rolled into A01:2025 Broken Access Control
**Status**: ❌ **CATEGORY NO LONGER EXISTS**
**Change Type**: **CRITICAL** - Merged/consolidated into A01:2025

**Impact on SecureCode v2.0 Paper**:
- Paper category: "A10:2021 Server-Side Request Forgery (SSRF)" (45 examples, 3.7%)
- **CATEGORY DELETED** in 2025
- **ACTION REQUIRED**:
  1. All 45 SSRF examples **MUST** be remapped to "A01:2025 Broken Access Control"
  2. Update Appendix B category breakdown
  3. Recalculate percentages (A01 will increase, A10 SSRF will disappear)
  4. Update methodology section explaining SSRF consolidation

---

#### NEW: A10:2025 - Mishandling of Exceptional Conditions
**2021**: **DID NOT EXIST**
**2025**: A10:2025 - Mishandling of Exceptional Conditions (24 CWEs) - **NEW CATEGORY**
**Status**: ✅ **COMPLETELY NEW**
**Change Type**: New category added in 2025
**Focus**:
- Improper error handling
- Logical errors
- Failing open
- Abnormal condition scenarios

**Impact on SecureCode v2.0 Paper**:
- Paper currently has: "Unknown" category (26 examples, 2.1%)
- **EVALUATE**: Do any "Unknown" examples fit this new category?
- **ACTION REQUIRED**:
  1. Review 26 "Unknown" examples
  2. Determine if any fit A10:2025 Mishandling of Exceptional Conditions
  3. Consider if A10:2025 should be added to paper's 12 categories
  4. Update category count if adopted (12 → 12 or 13 depending on "Unknown" handling)

---

## Summary of All Changes

### Categories That Stayed Same Position
1. **A01:2025 - Broken Access Control** (STAYS #1, but EXPANDED to include SSRF)
2. **A07:2025 - Authentication Failures** (STAYS #7, name simplified)
3. **A08:2025 - Software or Data Integrity Failures** (STAYS #8, minor name change)
4. **A09:2025 - Security Logging & Alerting Failures** (STAYS #9, added "Alerting")

### Categories That Changed Position
1. **A02:2021 Cryptographic Failures** → **A04:2025** (DOWN from #2 → #4)
2. **A03:2021 Injection** → **A05:2025** (DOWN from #3 → #5)
3. **A04:2021 Insecure Design** → **A06:2025** (DOWN from #4 → #6)
4. **A05:2021 Security Misconfiguration** → **A02:2025** (UP from #5 → #2) ⚠️ MAJOR
5. **A06:2021 Vulnerable Components** → **A03:2025 Supply Chain Failures** (UP from #6 → #3) ⚠️ MAJOR

### Categories Eliminated
1. **A10:2021 - Server-Side Request Forgery (SSRF)** → Rolled into **A01:2025 Broken Access Control**

### New Categories
1. **A10:2025 - Mishandling of Exceptional Conditions** (NEW)

---

## Impact on SecureCode v2.0 Paper Structure

### Current Paper Category Breakdown (from Appendix B)

Based on paper's current 2021 taxonomy:

| OWASP 2021 Category | Examples | % | → | OWASP 2025 Category | Action Required |
|---|---|---|---|---|---|
| A01:2021 Broken Access Control | 119 | 9.8% | → | A01:2025 Broken Access Control | Update reference |
| A02:2021 Cryptographic Failures | 74 | 6.1% | → | A04:2025 Cryptographic Failures | Update number |
| A03:2021 Injection | 296 | 24.4% | → | A05:2025 Injection | Update number |
| A04:2021 Insecure Design | 64 | 5.3% | → | A06:2025 Insecure Design | Update number |
| A05:2021 Security Misconfiguration | 93 | 7.7% | → | **A02:2025 Security Misconfiguration** | **Update to #2** |
| **A06:2021 Vulnerable Components** | **85** | **7.0%** | → | **A03:2025 Supply Chain Failures** | **Change name + scope** |
| A07:2021 Ident. & Auth. Failures | 83 | 6.8% | → | A07:2025 Authentication Failures | Update name |
| A08:2021 Software and Data Integrity | 80 | 6.6% | → | A08:2025 Software **or** Data Integrity | Update "and" → "or" |
| A09:2021 Logging & Monitoring | 94 | 7.7% | → | A09:2025 Logging **& Alerting** | Add "Alerting" |
| **A10:2021 SSRF** | **45** | **3.7%** | → | **MERGE INTO A01:2025** | **ELIMINATE category** |
| AI/ML Security (custom) | 156 | 12.8% | → | AI/ML Security (custom) | No change (custom) |
| Unknown | 26 | 2.1% | → | Review for A10:2025? | Evaluate |
| **TOTAL** | **1,215** | **100%** |  |  |  |

### Required Changes to Paper

#### 1. **Immediate Reference Updates** (All occurrences)

**Find and Replace (careful - verify context first)**:
- "A02:2021 Cryptographic Failures" → "A04:2025 Cryptographic Failures"
- "A03:2021 Injection" → "A05:2025 Injection"
- "A04:2021 Insecure Design" → "A06:2025 Insecure Design"
- "A05:2021 Security Misconfiguration" → "A02:2025 Security Misconfiguration"
- "A07:2021 Identification and Authentication Failures" → "A07:2025 Authentication Failures"
- "A08:2021 Software and Data Integrity Failures" → "A08:2025 Software or Data Integrity Failures"
- "A09:2021 Security Logging and Monitoring Failures" → "A09:2025 Security Logging & Alerting Failures"

#### 2. **Major Structural Changes**

**A. Handle A06:2021 → A03:2025 Transformation**
- **Old**: "A06:2021 Vulnerable and Outdated Components (85 examples, 7.0%)"
- **New**: "A03:2025 Software Supply Chain Failures (85 examples, 7.0%)"
- **Update Abstract Line 18** (if mentioned)
- **Update Section 1.1** (if category list present)
- **Update Section 3.3** (severity distribution)
- **Update Appendix B** (category breakdown table)
- **Review methodology discussion** - explain scope expansion

**B. Handle A10:2021 SSRF Elimination**
- **Current**: "A10:2021 Server-Side Request Forgery (SSRF)" listed as separate category with 45 examples
- **Required**: Merge into "A01:2025 Broken Access Control"
- **Impact**:
  - A01 examples: 119 → 164 (if merging all 45)
  - A01 percentage: 9.8% → 13.5%
  - A10 SSRF: 45 examples → 0 (category eliminated)
  - Total categories: 12 → 11 (unless adding new A10:2025)

**C. Update Category Counts**
- **Current**: "12 total categories" (10 OWASP + AI/ML + Unknown)
- **After Changes**:
  - Option 1: "11 total categories" (9 OWASP 2025 + AI/ML + Unknown) - if not adopting A10:2025
  - Option 2: "12 total categories" (10 OWASP 2025 + AI/ML + Unknown) - if adopting A10:2025 and reclassifying Unknown examples

#### 3. **Methodology Section Updates**

**Section requiring revision** (likely Section 2 or Section 3.2):
- Update OWASP version reference: "OWASP Top 10:2021" → "OWASP Top 10:2025 Release Candidate"
- Explain major changes:
  - SSRF consolidation into Broken Access Control
  - Supply Chain Failures scope expansion
  - Security Misconfiguration priority increase (#5 → #2)
  - New A10:2025 Mishandling of Exceptional Conditions (if adopted)

**Add context** (suggested addition to methodology):
```
Dataset creation began in 2024 using OWASP Top 10:2021 taxonomy. As of
December 2025, OWASP released the Top 10:2025 Release Candidate with
significant changes including SSRF consolidation into Broken Access Control
(A01), expansion of Vulnerable Components into Software Supply Chain Failures
(A03), and elevation of Security Misconfiguration to #2 priority. We have
remapped all examples to the 2025 taxonomy to reflect current industry
standards and priorities.
```

#### 4. **Abstract Updates**

**Current Abstract** likely mentions categories. Example lines that may need updating:
- Any mention of specific category numbers (A02, A03, etc.)
- Any mention of "Vulnerable and Outdated Components" → "Software Supply Chain Failures"
- Any mention of "SSRF" as standalone category → now part of "Broken Access Control"

#### 5. **Table and Figure Updates**

**Tables requiring updates**:
- **Table 1** (if present): Category distribution table
- **Table 2** (if present): Severity by category
- **Appendix B**: Complete category breakdown

**Figures requiring updates**:
- Any pie charts or bar charts showing category distribution
- Any figures referencing specific category numbers

---

## Detailed Remapping Recommendations

### Recommended Approach

**Phase 1: Reference Updates (Low Risk)**
1. Update all A07, A08, A09 references (name changes only, same position)
2. Update A01 reference (same position, note SSRF inclusion)

**Phase 2: Position Updates (Medium Risk)**
3. Update A02→A04, A03→A05, A04→A06 (number shifts)
4. Update A05→A02 (major priority change, add context)

**Phase 3: Major Changes (High Risk)**
5. Transform A06:2021 (Vulnerable Components) → A03:2025 (Supply Chain Failures)
6. Eliminate A10:2021 (SSRF) and merge into A01:2025 (Broken Access Control)
7. Evaluate A10:2025 (Exceptional Conditions) for adoption

**Phase 4: Verification (Critical)**
8. Verify all category counts sum to 1,215
9. Verify all percentages sum to 100%
10. Update all cross-references in paper
11. Update methodology narrative
12. Update abstract and introduction

### Data Integrity Checklist

After remapping, verify:
- ✅ Total examples still = 1,215
- ✅ All percentages sum to 100%
- ✅ A01 count increased by 45 (SSRF examples added)
- ✅ A10 SSRF category removed (or count = 0)
- ✅ All category numbers updated consistently throughout
- ✅ Appendix B matches Section 3.3 matches Abstract
- ✅ No references to eliminated A10:2021 SSRF
- ✅ All references to A06 now say "A03" and "Supply Chain Failures"

---

## Search and Replace Guide

### Step 1: Safe Replacements (Same Position, Name Changes)

These are safe to find/replace globally (but verify first):

```
"A07:2021 Identification and Authentication Failures"
→ "A07:2025 Authentication Failures"

"A08:2021 Software and Data Integrity Failures"
→ "A08:2025 Software or Data Integrity Failures"

"A09:2021 Security Logging and Monitoring Failures"
→ "A09:2025 Security Logging & Alerting Failures"
```

### Step 2: Number-Only Changes (Position Shifts)

**CAREFUL**: Only replace when category name also present to avoid false positives

```
"A02:2021 Cryptographic Failures" → "A04:2025 Cryptographic Failures"
"A03:2021 Injection" → "A05:2025 Injection"
"A04:2021 Insecure Design" → "A06:2025 Insecure Design"
```

### Step 3: Major Changes (Manual Verification Required)

**MANUAL REVIEW REQUIRED** - cannot safely batch replace:

```
"A05:2021 Security Misconfiguration"
→ "A02:2025 Security Misconfiguration"
(Note: Now #2 priority instead of #5 - may need contextual narrative update)

"A06:2021 Vulnerable and Outdated Components"
→ "A03:2025 Software Supply Chain Failures"
(Note: Major scope expansion - review all 85 examples for fit)

"A10:2021 Server-Side Request Forgery (SSRF)"
→ "A01:2025 Broken Access Control"
(Note: Category eliminated - merge all 45 examples into A01)
```

### Step 4: Appendix B Table Update

**Old Table Structure** (Appendix B):
```
| Category | Examples | % | Severity Distribution |
|----------|----------|---|-----------------------|
| A01:2021 Broken Access Control | 119 | 9.8% | ... |
| A02:2021 Cryptographic Failures | 74 | 6.1% | ... |
| A03:2021 Injection | 296 | 24.4% | ... |
| A04:2021 Insecure Design | 64 | 5.3% | ... |
| A05:2021 Security Misconfiguration | 93 | 7.7% | ... |
| A06:2021 Vulnerable and Outdated Components | 85 | 7.0% | ... |
| A07:2021 Identification and Authentication Failures | 83 | 6.8% | ... |
| A08:2021 Software and Data Integrity Failures | 80 | 6.6% | ... |
| A09:2021 Security Logging and Monitoring Failures | 94 | 7.7% | ... |
| A10:2021 Server-Side Request Forgery (SSRF) | 45 | 3.7% | ... |
| AI/ML Security | 156 | 12.8% | ... |
| Unknown | 26 | 2.1% | ... |
| **TOTAL** | **1,215** | **100%** | ... |
```

**New Table Structure** (Appendix B after remapping):
```
| Category | Examples | % | Severity Distribution |
|----------|----------|---|-----------------------|
| A01:2025 Broken Access Control | 164 | 13.5% | ... | ← INCREASED (merged SSRF)
| A02:2025 Security Misconfiguration | 93 | 7.7% | ... | ← MOVED UP from #5
| A03:2025 Software Supply Chain Failures | 85 | 7.0% | ... | ← RENAMED/EXPANDED
| A04:2025 Cryptographic Failures | 74 | 6.1% | ... | ← MOVED DOWN from #2
| A05:2025 Injection | 296 | 24.4% | ... | ← MOVED DOWN from #3
| A06:2025 Insecure Design | 64 | 5.3% | ... | ← MOVED DOWN from #4
| A07:2025 Authentication Failures | 83 | 6.8% | ... | ← NAME SIMPLIFIED
| A08:2025 Software or Data Integrity Failures | 80 | 6.6% | ... | ← MINOR NAME CHANGE
| A09:2025 Security Logging & Alerting Failures | 94 | 7.7% | ... | ← ADDED "Alerting"
| [A10:2025 Mishandling of Exceptional Conditions] | [TBD] | [TBD] | ... | ← NEW (if adopted)
| AI/ML Security (custom category) | 156 | 12.8% | ... | ← NO CHANGE
| Unknown | 26 | 2.1% | ... | ← NO CHANGE (or remap to A10:2025)
| **TOTAL** | **1,215** | **100%** | ... |
```

**Note**: A10:2021 SSRF row completely eliminated; 45 examples merged into A01:2025

---

## Critical Decision Points

### Decision 1: How to Handle SSRF Examples

**Option A**: Merge all 45 SSRF examples into A01:2025 Broken Access Control
- **Pro**: Aligns with OWASP 2025 taxonomy exactly
- **Pro**: Simpler paper structure (one less category)
- **Con**: A01 becomes very large (164 examples, 13.5%)
- **Recommendation**: ✅ **RECOMMENDED** - follow OWASP 2025

**Option B**: Keep SSRF as separate category but note it's now part of A01
- **Pro**: Maintains paper's original structure
- **Con**: Doesn't align with current OWASP standard
- **Recommendation**: ❌ **NOT RECOMMENDED** - confusing for readers

### Decision 2: Whether to Adopt A10:2025 Mishandling of Exceptional Conditions

**Option A**: Add A10:2025 and reclassify "Unknown" examples if they fit
- **Pro**: Fully aligned with OWASP 2025
- **Pro**: May resolve "Unknown" category
- **Con**: Requires reviewing all 26 "Unknown" examples
- **Recommendation**: ⚠️ **EVALUATE** - depends on Unknown example content

**Option B**: Keep "Unknown" category as-is, don't add A10:2025
- **Pro**: Minimal changes
- **Pro**: "Unknown" may not fit A10:2025 definition
- **Con**: Paper not fully aligned with OWASP 2025
- **Recommendation**: ✅ **ACCEPTABLE** - if Unknown examples don't fit A10:2025

### Decision 3: How to Present Supply Chain Failures Scope Expansion

**Option A**: Keep same 85 examples, update name and note scope expansion
- **Pro**: No data changes needed
- **Pro**: 85 examples likely still fit (vulnerable components are part of supply chain)
- **Con**: Doesn't fully reflect expanded scope
- **Recommendation**: ✅ **RECOMMENDED** - simplest approach

**Option B**: Review all 85 examples and potentially reclassify some
- **Pro**: More accurate to expanded scope
- **Con**: Time-consuming
- **Con**: May introduce inconsistencies
- **Recommendation**: ❌ **NOT NECESSARY** - unless examples clearly misaligned

---

## Timeline Recommendation

### Week 1: Preparation and Analysis
- ✅ Complete: OWASP 2021 and 2025 documentation gathered
- ✅ Complete: Comparison analysis document created
- ⏳ Pending: Read current paper to identify all category references
- ⏳ Pending: Create master list of all locations requiring updates

### Week 1-2: Execute Remapping
- Phase 1 (Day 1): Safe name changes (A07, A08, A09)
- Phase 2 (Day 2): Position shifts (A02→A04, A03→A05, A04→A06, A05→A02)
- Phase 3 (Day 3): Major changes (A06→A03, eliminate A10 SSRF)
- Phase 4 (Day 4): Verification and consistency checks

### Week 2: Final Review
- Verify all counts and percentages
- Update methodology narrative
- Update abstract and introduction
- Final paper read-through for consistency

---

## Reference Quick Guide

**When citing OWASP in paper:**
- **Old**: "OWASP Top 10:2021"
- **New**: "OWASP Top 10:2025 Release Candidate (November 2025)"

**When referencing taxonomy:**
- **Old**: "Following OWASP Top 10:2021 taxonomy..."
- **New**: "Following OWASP Top 10:2025 Release Candidate taxonomy..."

**When explaining dataset creation:**
- Add note: "Dataset initially created using OWASP 2021 taxonomy, subsequently remapped to OWASP 2025 Release Candidate (November 2025) to reflect current industry standards."

---

## Appendix: Full CWE Mapping Changes

### Categories with CWE Additions

**A01:2025 Broken Access Control** (34 → 40 CWEs):
- Added: CWE-918 (SSRF)
- Added: CWE-200, CWE-352 (CSRF)
- Added: 3 additional CWEs

**A03:2025 Software Supply Chain Failures** (3 → 5 CWEs):
- Added: CWE-1104 (Use of Unmaintained Third-Party Components)
- Added: CWE-1329
- Added: CWE-1395

**A04:2025 Cryptographic Failures** (29 → 32 CWEs):
- Added: 3 CWEs (specific ones not detailed in summary)

**A05:2025 Injection** (33 → 38 CWEs):
- Added: 5 CWEs (specific ones not detailed in summary)

### Categories with CWE Reductions

**A02:2025 Security Misconfiguration** (20 → 16 CWEs):
- Removed: 4 CWEs (likely consolidated or reclassified)
- Notable: Still includes CWE-611 (XXE)

---

**End of Comparison Analysis**

**Next Steps**: Review SecureCode v2.0 paper and begin systematic remapping per recommendations above.
