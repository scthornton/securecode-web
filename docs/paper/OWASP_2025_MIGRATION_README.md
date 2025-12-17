# OWASP Top 10:2025 Migration Guide

This document provides step-by-step instructions for migrating the SecureCode v2.0 dataset from OWASP Top 10:2021 to OWASP Top 10:2025 taxonomy.

---

## Quick Start

```bash
# 1. Dry-run validation (no changes made)
cd /Users/scott/perfecxion/datasets/securecode/v2
python scripts/migrate_owasp_2025.py --dry-run

# 2. Execute migration (creates backups)
python scripts/migrate_owasp_2025.py

# 3. Validate migration results
python scripts/validate_owasp_migration.py

# 4. If validation passes, commit changes
git add consolidated/*.jsonl
git commit -m "Migrate dataset from OWASP 2021 to 2025 taxonomy"
```

---

## Background

On **November 6, 2025**, OWASP released the **Top 10:2025 Release Candidate** with significant changes to the taxonomy:

### Major Changes

1. **A10:2021 SSRF Eliminated** - Merged into A01:2025 Broken Access Control
2. **A06:2021 Vulnerable Components** → **A03:2025 Software Supply Chain Failures** (name & scope change)
3. **A05:2021 Security Misconfiguration** → **A02:2025** (jumped from #5 to #2)
4. All other categories renumbered due to reshuffling

### Dataset Impact

- **Total entries:** 1,215 (989 train / 122 val / 104 test)
- **Entries requiring updates:** 1,215 (100%)
- **Field change:** `metadata.owasp_2021` → `metadata.owasp_2025`
- **Value changes:** 1,105 entries (91% - excludes AI/ML and Unknown)

See [OWASP_2025_MIGRATION_ANALYSIS.md](./OWASP_2025_MIGRATION_ANALYSIS.md) for detailed analysis.

---

## Prerequisites

- Python 3.7+
- SecureCode v2.0 dataset (unchanged from original)
- Git repository (for version control)

---

## Migration Process

### Step 1: Pre-Migration Validation

Verify dataset integrity before making any changes:

```bash
# Validate file structure and counts
python scripts/migrate_owasp_2025.py --dry-run
```

**Expected output:**
```
============================================================
DRY-RUN MODE - No changes will be made
============================================================

Processing: train.jsonl
Validating file integrity...
✓ Validation passed (989 entries)
✓ Dry-run validation complete: 989 entries

Processing: val.jsonl
Validating file integrity...
✓ Validation passed (122 entries)
✓ Dry-run validation complete: 122 entries

Processing: test.jsonl
Validating file integrity...
✓ Validation passed (104 entries)
✓ Dry-run validation complete: 104 entries

MIGRATION SUMMARY
Total entries processed: 1215
Entries migrated: 1105
Entries unchanged (AI/ML, Unknown): 110
Errors encountered: 0
```

**If dry-run fails:** Do not proceed. Investigate errors before continuing.

---

### Step 2: Execute Migration

Run the migration script to update all files:

```bash
python scripts/migrate_owasp_2025.py
```

**What happens:**
1. Script prompts for confirmation: `Proceed with migration? (yes/no):`
2. Creates timestamped backups: `train.jsonl.bak_20251216_143022`
3. Processes each file line-by-line
4. Renames `metadata.owasp_2021` → `metadata.owasp_2025`
5. Updates values per OWASP 2025 mapping
6. Writes migrated entries back to original files

**Expected output:**
```
============================================================
LIVE MODE - Files will be modified (backups created)
============================================================

Proceed with migration? (yes/no): yes

============================================================
Processing: train.jsonl
============================================================
Validating file integrity...
✓ Validation passed (989 entries)
✓ Created backup: train.jsonl.bak_20251216_143022
✓ Migration complete: 989 entries processed

[similar output for val.jsonl and test.jsonl]

MIGRATION SUMMARY
Total entries processed: 1215
Entries migrated: 1105
Entries unchanged (AI/ML, Unknown): 110
Errors encountered: 0

CATEGORY DISTRIBUTION AFTER MIGRATION
A01:2025-Broken Access Control                                224 ( 18.4%)
A02:2025-Security Misconfiguration                            134 ( 11.0%)
A03:2025-Software Supply Chain Failures                        85 (  7.0%)
A04:2025-Cryptographic Failures                               115 (  9.5%)
A05:2025-Injection                                            125 ( 10.3%)
A06:2025-Insecure Design                                       84 (  6.9%)
A07:2025-Identification and Authentication Failures           199 ( 16.4%)
A08:2025-Software and Data Integrity Failures                  80 (  6.6%)
A09:2025-Security Logging and Monitoring Failures              59 (  4.9%)
AI/ML Security Threats                                         50 (  4.1%)
Unknown                                                        60 (  4.9%)
```

**Backups created:**
- `consolidated/train.jsonl.bak_YYYYMMDD_HHMMSS`
- `consolidated/val.jsonl.bak_YYYYMMDD_HHMMSS`
- `consolidated/test.jsonl.bak_YYYYMMDD_HHMMSS`

---

### Step 3: Validate Migration Results

Run validation script to ensure migration was successful:

```bash
python scripts/validate_owasp_migration.py
```

**Validation checks:**
- ✅ All files exist and are parseable
- ✅ All entries have `owasp_2025` field
- ✅ No entries have `owasp_2021` field (removed)
- ✅ Entry counts match expectations (989 / 122 / 104)
- ✅ Category distribution matches projections
- ✅ Sample entries manually inspected

**Expected output:**
```
============================================================
SecureCode v2.0: OWASP 2025 Migration Validation
============================================================

FILE STRUCTURE VALIDATION
✓ File exists: train.jsonl
✓ All entries have owasp_2025: train.jsonl
✓ No entries have owasp_2021: train.jsonl
[similar for val.jsonl and test.jsonl]

ENTRY COUNT VALIDATION
✓ Entry count: train.jsonl (989 entries)
✓ Entry count: val.jsonl (122 entries)
✓ Entry count: test.jsonl (104 entries)
✓ Total entry count (1215)

OWASP 2025 CATEGORY DISTRIBUTION
✓ A01:2025-Broken Access Control                                224 (expected: 224)
✓ A02:2025-Security Misconfiguration                            134 (expected: 134)
✓ A03:2025-Software Supply Chain Failures                        85 (expected: 85)
✓ A04:2025-Cryptographic Failures                               115 (expected: 115)
✓ A05:2025-Injection                                            125 (expected: 125)
✓ A06:2025-Insecure Design                                       84 (expected: 84)
✓ A07:2025-Identification and Authentication Failures           199 (expected: 199)
✓ A08:2025-Software and Data Integrity Failures                  80 (expected: 80)
✓ A09:2025-Security Logging and Monitoring Failures              59 (expected: 59)
✓ AI/ML Security Threats                                         50 (expected: 50)
✓ Unknown                                                        60 (expected: 60)
✓ Category distribution matches expectations

SAMPLE ENTRY INSPECTION
TRAIN - Entry ID: authentication-000061
  ✓ Has owasp_2025: A07:2025-Identification and Authentication Failures

VAL - Entry ID: authentication-000164
  ✓ Has owasp_2025: A07:2025-Identification and Authentication Failures

TEST - Entry ID: dependencies-000063
  ✓ Has owasp_2025: A03:2025-Software Supply Chain Failures

✓ Sample entry inspection completed

VALIDATION SUMMARY
Tests passed: 18
Tests failed: 0
Warnings: 0

✅ VALIDATION PASSED
```

**If validation fails:** Do not commit. Investigate failures and rollback if needed.

---

### Step 4: Manual Spot Check (Recommended)

Inspect a few random entries to ensure correctness:

```bash
# Check random entries from train set
head -n 5 consolidated/train.jsonl | python3 -m json.tool | grep -A 2 "metadata"

# Check specific SSRF entries (should now be A01:2025)
grep "Server-Side Request Forgery" consolidated/train.jsonl | head -n 1 | python3 -m json.tool

# Check vulnerable components entries (should now be A03:2025 Supply Chain)
grep "Vulnerable and Outdated" consolidated/train.jsonl | head -n 1 | python3 -m json.tool
```

**What to verify:**
- ✅ `owasp_2021` field is gone
- ✅ `owasp_2025` field exists
- ✅ SSRF entries now have `A01:2025-Broken Access Control`
- ✅ Vulnerable Components now have `A03:2025-Software Supply Chain Failures`

---

### Step 5: Update Documentation

Before committing, update related documentation:

#### 5.1 Update README.md

```diff
- Dataset uses OWASP Top 10:2021 taxonomy
+ Dataset uses OWASP Top 10:2025 taxonomy

  Metadata fields:
- - owasp_2021: OWASP Top 10:2021 category (e.g., "A01:2021-Broken Access Control")
+ - owasp_2025: OWASP Top 10:2025 category (e.g., "A01:2025-Broken Access Control")
```

#### 5.2 Update Dataset Card (HuggingFace)

Update category distribution statistics and metadata field description.

#### 5.3 Update Paper References (if applicable)

If your paper references OWASP taxonomy, update:
- Taxonomy version (2021 → 2025)
- Category names (especially A06 and A10)
- Category distribution tables/figures

---

### Step 6: Commit Changes

```bash
# Stage migrated files
git add consolidated/train.jsonl
git add consolidated/val.jsonl
git add consolidated/test.jsonl

# Commit with descriptive message
git commit -m "Migrate dataset from OWASP Top 10:2021 to 2025 taxonomy

- Rename metadata.owasp_2021 → metadata.owasp_2025
- Update category values per OWASP 2025 Release Candidate (Nov 6, 2025)
- Merge A10:2021 SSRF into A01:2025 Broken Access Control (45 entries)
- Rename A06:2021 Vulnerable Components → A03:2025 Supply Chain (85 entries)
- Update category numbers for A02-A06 due to reshuffling
- Total: 1,215 entries migrated (989 train / 122 val / 104 test)

Validation: All tests passed (18/18)
Backups: Created timestamped .bak files for rollback"

# Push to remote (if desired)
git push origin main
```

---

## Rollback Procedure

If you need to undo the migration:

### Option 1: Automated Rollback

```bash
python scripts/migrate_owasp_2025.py --rollback
```

This restores files from the most recent `.bak_*` backups.

### Option 2: Manual Restore

```bash
# Identify backup files
ls -lt consolidated/*.bak_*

# Restore specific backup (replace timestamp)
cp consolidated/train.jsonl.bak_20251216_143022 consolidated/train.jsonl
cp consolidated/val.jsonl.bak_20251216_143022 consolidated/val.jsonl
cp consolidated/test.jsonl.bak_20251216_143022 consolidated/test.jsonl
```

### Option 3: Git Revert

```bash
# Discard uncommitted changes
git checkout -- consolidated/*.jsonl

# Revert committed changes
git revert HEAD
```

---

## Troubleshooting

### Error: "File not found"

**Cause:** Script cannot find dataset files
**Solution:**
```bash
# Ensure you're in the repository root
cd /Users/scott/perfecxion/datasets/securecode/v2

# Verify files exist
ls -l consolidated/*.jsonl

# Run script from correct directory
python scripts/migrate_owasp_2025.py --dry-run
```

### Error: "JSON parse error"

**Cause:** Corrupted JSONL entry
**Solution:**
1. Note the line number from error message
2. Inspect the problematic line:
   ```bash
   sed -n '<line_number>p' consolidated/train.jsonl | python3 -m json.tool
   ```
3. Fix JSON syntax error manually
4. Re-run migration

### Error: "Category distribution mismatch"

**Cause:** Unexpected category counts after migration
**Solution:**
1. Check which categories have incorrect counts
2. Verify OWASP_MIGRATION_MAP in script is correct
3. Search for entries with unexpected categories:
   ```bash
   grep "unexpected_category" consolidated/*.jsonl
   ```
4. Investigate why mapping failed
5. Rollback and fix mapping

### Warning: "Unexpected categories found"

**Cause:** Dataset has categories not in expected list (AI/ML, Unknown, or OWASP 2021/2025)
**Solution:**
1. Review the unexpected categories
2. If legitimate (new custom category), update EXPECTED_DISTRIBUTION
3. If error, investigate source and fix

---

## Migration Mapping Reference

| OWASP 2021 | OWASP 2025 | Entries | Change Type |
|------------|------------|---------|-------------|
| A01:2021-Broken Access Control | A01:2025-Broken Access Control | 179 | Position unchanged |
| A02:2021-Cryptographic Failures | A04:2025-Cryptographic Failures | 115 | Renumbered (A02→A04) |
| A03:2021-Injection | A05:2025-Injection | 125 | Renumbered (A03→A05) |
| A04:2021-Insecure Design | A06:2025-Insecure Design | 84 | Renumbered (A04→A06) |
| A05:2021-Security Misconfiguration | A02:2025-Security Misconfiguration | 134 | **Jumped (#5→#2)** |
| A06:2021-Vulnerable and Outdated Components | A03:2025-Software Supply Chain Failures | 85 | **Name changed** |
| A07:2021-Identification and Authentication Failures | A07:2025-Identification and Authentication Failures | 199 | Position unchanged |
| A08:2021-Software and Data Integrity Failures | A08:2025-Software and Data Integrity Failures | 80 | Position unchanged |
| A09:2021-Security Logging and Monitoring Failures | A09:2025-Security Logging and Monitoring Failures | 59 | Position unchanged |
| A10:2021-Server-Side Request Forgery | A01:2025-Broken Access Control | 45 | **MERGED into A01** |

**Special categories (unchanged):**
- AI/ML Security Threats → AI/ML Security Threats (50 entries)
- Unknown → Unknown (60 entries)

---

## Post-Migration Distribution

After migration, the dataset will have the following OWASP 2025 distribution:

| Category | Count | % of Dataset |
|----------|------:|-------------:|
| A01:2025-Broken Access Control | 224 | 18.4% |
| A02:2025-Security Misconfiguration | 134 | 11.0% |
| A03:2025-Software Supply Chain Failures | 85 | 7.0% |
| A04:2025-Cryptographic Failures | 115 | 9.5% |
| A05:2025-Injection | 125 | 10.3% |
| A06:2025-Insecure Design | 84 | 6.9% |
| A07:2025-Identification and Authentication Failures | 199 | 16.4% |
| A08:2025-Software and Data Integrity Failures | 80 | 6.6% |
| A09:2025-Security Logging and Monitoring Failures | 59 | 4.9% |
| AI/ML Security Threats | 50 | 4.1% |
| Unknown | 60 | 4.9% |
| **TOTAL** | **1,215** | **100.0%** |

---

## Files Created/Modified

### Created Files

1. `docs/paper/OWASP_2025_MIGRATION_ANALYSIS.md` - Detailed analysis report
2. `docs/paper/OWASP_2025_MIGRATION_README.md` - This file
3. `scripts/migrate_owasp_2025.py` - Migration script
4. `scripts/validate_owasp_migration.py` - Validation script

### Modified Files (after migration)

1. `consolidated/train.jsonl` - 989 entries updated
2. `consolidated/val.jsonl` - 122 entries updated
3. `consolidated/test.jsonl` - 104 entries updated

### Backup Files (created during migration)

1. `consolidated/train.jsonl.bak_YYYYMMDD_HHMMSS`
2. `consolidated/val.jsonl.bak_YYYYMMDD_HHMMSS`
3. `consolidated/test.jsonl.bak_YYYYMMDD_HHMMSS`

---

## Support

For issues or questions:
1. Review [OWASP_2025_MIGRATION_ANALYSIS.md](./OWASP_2025_MIGRATION_ANALYSIS.md)
2. Check "Troubleshooting" section above
3. Verify backups exist before troubleshooting
4. Contact dataset maintainer

---

**Last Updated:** 2025-12-16
**Migration Script Version:** 1.0
**OWASP Source:** Top 10:2025 Release Candidate (Nov 6, 2025)
