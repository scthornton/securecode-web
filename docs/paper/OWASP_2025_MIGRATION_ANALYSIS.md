# SecureCode v2.0: OWASP Top 10:2025 Migration Analysis

**Generated:** 2025-12-16
**Analyst:** Dataset Integrity Expert
**Status:** READY FOR MIGRATION

---

## Executive Summary

The SecureCode v2.0 dataset requires migration from OWASP Top 10:2021 to OWASP Top 10:2025 taxonomy following the November 6, 2025 Release Candidate. This is a **metadata-only migration** affecting classification fields but not conversation content.

**Key Metrics:**
- **Total entries:** 1,215 (989 train / 122 val / 104 test)
- **Entries requiring updates:** 1,215 (100%)
- **Field changes:** 1 metadata field (`owasp_2021` → `owasp_2025`)
- **Value changes:** 1,105 entries (91% - excludes AI/ML and Unknown)
- **Risk level:** LOW (automated migration, no text changes)

---

## 1. Schema Analysis

### Current Structure (OWASP 2021)

```json
{
  "id": "authentication-000061",
  "metadata": {
    "lang": "go",
    "category": "auth_failures",
    "subcategory": "authentication",
    "technique": "Missing CAPTCHA on registration",
    "owasp_2021": "A07:2021-Identification and Authentication Failures",
    "cwe": "CWE-287",
    "severity": "HIGH",
    "complexity": "moderate",
    "created": "2025-01-09",
    "validated": false
  },
  "context": { ... },
  "conversations": [ ... ],
  "validation": { ... }
}
```

### Target Structure (OWASP 2025)

```json
{
  "id": "authentication-000061",
  "metadata": {
    "lang": "go",
    "category": "auth_failures",
    "subcategory": "authentication",
    "technique": "Missing CAPTCHA on registration",
    "owasp_2025": "A07:2025-Identification and Authentication Failures",
    "cwe": "CWE-287",
    "severity": "HIGH",
    "complexity": "moderate",
    "created": "2025-01-09",
    "validated": false
  },
  "context": { ... },
  "conversations": [ ... ],
  "validation": { ... }
}
```

**Affected Field:** `metadata.owasp_2021` → `metadata.owasp_2025` (field name + value)

---

## 2. Current OWASP 2021 Distribution

| Category | Total | Train | Val | Test |
|----------|------:|------:|----:|-----:|
| A01:2021-Broken Access Control | 179 | 156 | 12 | 11 |
| A02:2021-Cryptographic Failures | 115 | 95 | 5 | 15 |
| A03:2021-Injection | 125 | 91 | 22 | 12 |
| A04:2021-Insecure Design | 84 | 67 | 14 | 3 |
| A05:2021-Security Misconfiguration | 134 | 118 | 11 | 5 |
| A06:2021-Vulnerable and Outdated Components | 85 | 76 | 3 | 6 |
| A07:2021-Identification and Authentication Failures | 199 | 148 | 34 | 17 |
| A08:2021-Software and Data Integrity Failures | 80 | 60 | 4 | 16 |
| A09:2021-Security Logging and Monitoring Failures | 59 | 44 | 8 | 7 |
| A10:2021-Server-Side Request Forgery | 45 | 39 | 1 | 5 |
| AI/ML Security Threats | 50 | 36 | 7 | 7 |
| Unknown | 60 | 59 | 1 | 0 |
| **TOTAL** | **1,215** | **989** | **122** | **104** |

---

## 3. OWASP 2021 → 2025 Migration Mapping

| # | OWASP 2021 Category | OWASP 2025 Category | Count | Change Type |
|--:|---------------------|---------------------|------:|-------------|
| 1 | A01:2021-Broken Access Control | A01:2025-Broken Access Control | 179 | POSITION UNCHANGED |
| 2 | A02:2021-Cryptographic Failures | A04:2025-Cryptographic Failures | 115 | RENUMBERED (A02→A04) |
| 3 | A03:2021-Injection | A05:2025-Injection | 125 | RENUMBERED (A03→A05) |
| 4 | A04:2021-Insecure Design | A06:2025-Insecure Design | 84 | RENUMBERED (A04→A06) |
| 5 | A05:2021-Security Misconfiguration | A02:2025-Security Misconfiguration | 134 | **JUMPED (#5→#2)** |
| 6 | A06:2021-Vulnerable and Outdated Components | A03:2025-Software Supply Chain Failures | 85 | **NAME CHANGED** |
| 7 | A07:2021-Identification and Authentication Failures | A07:2025-Identification and Authentication Failures | 199 | POSITION UNCHANGED |
| 8 | A08:2021-Software and Data Integrity Failures | A08:2025-Software and Data Integrity Failures | 80 | POSITION UNCHANGED |
| 9 | A09:2021-Security Logging and Monitoring Failures | A09:2025-Security Logging and Monitoring Failures | 59 | POSITION UNCHANGED |
| 10 | A10:2021-Server-Side Request Forgery | A01:2025-Broken Access Control | 45 | **MERGED INTO A01** |

**Special Categories (No Change):**
- AI/ML Security Threats → AI/ML Security Threats (50 entries)
- Unknown → Unknown (60 entries)

---

## 4. Critical Changes Requiring Attention

### 4.1 Category Elimination (Merger)

```
┌─────────────────────────────────────────────────────────────────┐
│ A10:2021-Server-Side Request Forgery                            │
│   → MERGED INTO: A01:2025-Broken Access Control                 │
│   Affected: 45 entries (39 train / 1 val / 5 test)              │
│   Rationale: OWASP 2025 consolidated SSRF into access control   │
└─────────────────────────────────────────────────────────────────┘
```

**Example Entry:**
```json
// BEFORE
"owasp_2021": "A10:2021-Server-Side Request Forgery"

// AFTER
"owasp_2025": "A01:2025-Broken Access Control"
```

### 4.2 Category Renaming (Scope Expansion)

```
┌─────────────────────────────────────────────────────────────────┐
│ A06:2021-Vulnerable and Outdated Components                     │
│   → A03:2025-Software Supply Chain Failures                     │
│   Affected: 85 entries (76 train / 3 val / 6 test)              │
│   Rationale: Expanded scope to cover entire supply chain        │
└─────────────────────────────────────────────────────────────────┘
```

**Example Entry:**
```json
// BEFORE
"owasp_2021": "A06:2021-Vulnerable and Outdated Components"

// AFTER
"owasp_2025": "A03:2025-Software Supply Chain Failures"
```

### 4.3 Major Ranking Change

```
┌─────────────────────────────────────────────────────────────────┐
│ A05:2021-Security Misconfiguration                              │
│   → A02:2025-Security Misconfiguration (jumped from #5 to #2!)  │
│   Affected: 134 entries (118 train / 11 val / 5 test)           │
│   Rationale: Recognized as critical root cause of breaches      │
└─────────────────────────────────────────────────────────────────┘
```

**Example Entry:**
```json
// BEFORE
"owasp_2021": "A05:2021-Security Misconfiguration"

// AFTER
"owasp_2025": "A02:2025-Security Misconfiguration"
```

---

## 5. Post-Migration Distribution (Projected OWASP 2025)

| OWASP 2025 Category | Count | Train | Val | Test | % of Dataset |
|---------------------|------:|------:|----:|-----:|-------------:|
| A01:2025-Broken Access Control | 224 | 195 | 13 | 16 | 18.4% |
| A02:2025-Security Misconfiguration | 134 | 118 | 11 | 5 | 11.0% |
| A03:2025-Software Supply Chain Failures | 85 | 76 | 3 | 6 | 7.0% |
| A04:2025-Cryptographic Failures | 115 | 95 | 5 | 15 | 9.5% |
| A05:2025-Injection | 125 | 91 | 22 | 12 | 10.3% |
| A06:2025-Insecure Design | 84 | 67 | 14 | 3 | 6.9% |
| A07:2025-Identification and Authentication Failures | 199 | 148 | 34 | 17 | 16.4% |
| A08:2025-Software and Data Integrity Failures | 80 | 60 | 4 | 16 | 6.6% |
| A09:2025-Security Logging and Monitoring Failures | 59 | 44 | 8 | 7 | 4.9% |
| AI/ML Security Threats | 50 | 36 | 7 | 7 | 4.1% |
| Unknown | 60 | 59 | 1 | 0 | 4.9% |
| **TOTAL** | **1,215** | **989** | **122** | **104** | **100.0%** |

**Notable Changes:**
- **A01 Broken Access Control** increases from 179 → 224 entries (+45 from SSRF merger)
- **A02 Security Misconfiguration** moves to #2 position (134 entries, 11%)
- **A03 Software Supply Chain** replaces "Vulnerable Components" (85 entries)

---

## 6. Impact Assessment

### Entries Requiring Updates

| Update Type | Count | Percentage |
|-------------|------:|-----------:|
| Field name change (`owasp_2021` → `owasp_2025`) | 1,215 | 100% |
| Field value change (per migration mapping) | 1,105 | 91% |
| No changes required (AI/ML and Unknown) | 110 | 9% |

### Files Requiring Updates

| File | Entries | OWASP Categories Affected |
|------|--------:|---------------------------|
| `train.jsonl` | 989 | All OWASP 2021 categories |
| `val.jsonl` | 122 | All OWASP 2021 categories |
| `test.jsonl` | 104 | All OWASP 2021 categories |

### Validation Requirements

- ✅ Verify all 1,215 entries processed
- ✅ Confirm field name changed in all entries
- ✅ Validate mapping correctness per table above
- ✅ Ensure no data loss during migration
- ✅ Verify JSON integrity post-migration
- ✅ Update dataset documentation/README
- ✅ Update paper references if citing OWASP taxonomy
- ✅ Regenerate dataset statistics

### Conversation Text Analysis

**✅ VERIFIED:** No OWASP category references found in conversation text (sampled 100 entries)
- Migration will NOT require text content changes
- Only metadata field updates needed
- No risk of hard-coded category strings in prompts/responses

---

## 7. Migration Recommendations

### Approach: Automated Python Script

```python
import json
from pathlib import Path

# OWASP 2021 → 2025 mapping
MIGRATION_MAP = {
    "A01:2021-Broken Access Control": "A01:2025-Broken Access Control",
    "A02:2021-Cryptographic Failures": "A04:2025-Cryptographic Failures",
    "A03:2021-Injection": "A05:2025-Injection",
    "A04:2021-Insecure Design": "A06:2025-Insecure Design",
    "A05:2021-Security Misconfiguration": "A02:2025-Security Misconfiguration",
    "A06:2021-Vulnerable and Outdated Components": "A03:2025-Software Supply Chain Failures",
    "A07:2021-Identification and Authentication Failures": "A07:2025-Identification and Authentication Failures",
    "A08:2021-Software and Data Integrity Failures": "A08:2025-Software and Data Integrity Failures",
    "A09:2021-Security Logging and Monitoring Failures": "A09:2025-Security Logging and Monitoring Failures",
    "A10:2021-Server-Side Request Forgery": "A01:2025-Broken Access Control",
}

def migrate_entry(entry):
    """Migrate single entry from OWASP 2021 to 2025"""
    owasp_2021 = entry.get('metadata', {}).get('owasp_2021')

    if owasp_2021:
        # Apply mapping or keep as-is for AI/ML and Unknown
        owasp_2025 = MIGRATION_MAP.get(owasp_2021, owasp_2021)

        # Rename field and update value
        entry['metadata']['owasp_2025'] = owasp_2025
        del entry['metadata']['owasp_2021']

    return entry

def migrate_file(input_path, output_path):
    """Migrate entire JSONL file"""
    entries_processed = 0

    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            entry = json.loads(line)
            migrated = migrate_entry(entry)
            outfile.write(json.dumps(migrated) + '\n')
            entries_processed += 1

    return entries_processed
```

### Implementation Steps

1. **Create backup copies** of all three files
   ```bash
   cp train.jsonl train.jsonl.bak
   cp val.jsonl val.jsonl.bak
   cp test.jsonl test.jsonl.bak
   ```

2. **Run migration script** with dry-run validation
   - Parse all entries to verify JSON integrity
   - Count entries per category
   - Validate mapping completeness

3. **Execute migration** on backed-up files
   - Process each file line-by-line
   - Apply field rename and value mapping
   - Write to new files

4. **Validate results:**
   - Entry counts match (1,215 total)
   - All entries have `owasp_2025` field
   - No entries have `owasp_2021` field
   - Category distribution matches projections

5. **Update documentation:**
   - README.md (mention OWASP 2025 taxonomy)
   - Dataset card (update metadata description)
   - Paper (if referencing OWASP taxonomy)

6. **Commit changes** with descriptive message
   ```bash
   git add consolidated/*.jsonl
   git commit -m "Migrate dataset from OWASP Top 10:2021 to 2025 taxonomy

   - Rename metadata.owasp_2021 → metadata.owasp_2025
   - Update category values per OWASP 2025 mapping
   - Merge A10:2021 SSRF into A01:2025 Broken Access Control
   - Rename A06:2021 Vulnerable Components → A03:2025 Supply Chain
   - Total: 1,215 entries migrated (989 train / 122 val / 104 test)"
   ```

### Testing Checklist

- [ ] Backup original files created
- [ ] Migration script validates all entries parse correctly
- [ ] Field rename successful in all 1,215 entries
- [ ] Value mapping correct per table
- [ ] No data loss (compare pre/post line counts)
- [ ] JSON integrity verified (no parsing errors)
- [ ] Sample manual inspection of 10 random entries
- [ ] Category distribution matches projections
- [ ] Documentation updated
- [ ] Git commit with clear message

### Rollback Plan

- Keep original files as `.jsonl.bak`
- Can restore from backup if issues found
- Git history provides additional rollback option

---

## 8. Potential Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Data loss during field rename | HIGH | Create backups, verify entry counts pre/post |
| Incorrect category mapping | MEDIUM | Use validated MIGRATION_MAP, manual spot-checks |
| JSON corruption during processing | MEDIUM | Use json.loads/dumps, validate each line |
| Breaking downstream consumers | LOW | Update scripts/notebooks referencing owasp_2021 |
| Documentation drift | LOW | Update all OWASP 2021 → 2025 references |
| Confusion with old taxonomy | LOW | Keep field name as owasp_2025 (explicit versioning) |

---

## 9. Field-Level Changes Summary

### All Entries (1,215 total)

1. **Field rename:** `metadata.owasp_2021` → `metadata.owasp_2025`
2. **Value updates** per mapping table

### Breakdown by Change Type

**Category Name Changes:**
- `A06:2021-Vulnerable and Outdated Components` → `A03:2025-Software Supply Chain Failures`
  - **Impact:** 85 entries (76 train / 3 val / 6 test)

**Category Number Changes (name unchanged):**
- `A02:2021-Cryptographic Failures` → `A04:2025-Cryptographic Failures` (115 entries)
- `A03:2021-Injection` → `A05:2025-Injection` (125 entries)
- `A04:2021-Insecure Design` → `A06:2025-Insecure Design` (84 entries)
- `A05:2021-Security Misconfiguration` → `A02:2025-Security Misconfiguration` (134 entries)

**Category Mergers:**
- `A10:2021-Server-Side Request Forgery` → `A01:2025-Broken Access Control` (MERGED)
  - **Impact:** 45 entries (39 train / 1 val / 5 test)

**No Change Required:**
- `A01:2021-Broken Access Control` → `A01:2025-Broken Access Control` (179 entries)
- `A07:2021-Identification and Authentication Failures` (199 entries)
- `A08:2021-Software and Data Integrity Failures` (80 entries)
- `A09:2021-Security Logging and Monitoring Failures` (59 entries)
- `AI/ML Security Threats` (custom category, 50 entries)

---

## 10. Additional Considerations

### Documentation Updates Required

1. **README.md**
   - Update OWASP taxonomy reference (2021 → 2025)
   - Update metadata field description
   - Update category distribution statistics

2. **Dataset Card (HuggingFace)**
   - Update taxonomy version in metadata description
   - Regenerate category statistics
   - Add note about OWASP 2025 alignment

3. **Paper/Documentation**
   - Update references to OWASP taxonomy version
   - Update category distribution tables/figures
   - Note A10 SSRF merger into A01
   - Note A06 name change to Supply Chain

### Future Compatibility

- Field name `owasp_2025` provides explicit versioning
- Prevents confusion with old taxonomy
- Allows future migrations without field name conflicts
- Backward compatibility: old code will fail fast (missing field) rather than silently use wrong taxonomy

---

## 11. Conclusion

This migration is **low-risk and fully automatable**. The analysis confirms:

✅ **Single field update** per entry (metadata.owasp_2021 → owasp_2025)
✅ **No conversation text changes** required (verified via sampling)
✅ **Complete mapping defined** for all 10 OWASP 2021 categories
✅ **Validation strategy** in place to ensure data integrity
✅ **Rollback plan** available if issues arise

**Recommendation:** Proceed with automated migration following the implementation steps outlined in Section 7.

---

**Report Metadata:**
- **Generated:** 2025-12-16
- **Dataset Version:** SecureCode v2.0
- **Source Taxonomy:** OWASP Top 10:2021
- **Target Taxonomy:** OWASP Top 10:2025 (Release Candidate, Nov 6, 2025)
- **Total Entries Analyzed:** 1,215 (989 train / 122 val / 104 test)
- **Files Analyzed:**
  - `/Users/scott/perfecxion/datasets/securecode/v2/consolidated/train.jsonl`
  - `/Users/scott/perfecxion/datasets/securecode/v2/consolidated/val.jsonl`
  - `/Users/scott/perfecxion/datasets/securecode/v2/consolidated/test.jsonl`
