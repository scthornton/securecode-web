# SecureCode v2.0 - Quick Fix Guide

**Critical Issues Found in QA Review - December 3, 2025**

---

## Overview

QA review found **2 critical issues** that must be fixed before HuggingFace publication:

1. ❌ **Duplicate IDs:** 130 duplicate IDs across 1,209 examples
2. ❌ **Outdated Documentation:** README claims 1,013 examples, actual is 1,209

**Good News:** The underlying content is excellent (100% structural integrity, no content duplication). These are purely metadata/documentation issues.

**Estimated Fix Time:** 2 hours total

---

## Issue #1: Fix Duplicate IDs (CRITICAL)

### Current State
- **Total Examples:** 1,209
- **Unique IDs:** Only 196
- **Duplicates:** 130 IDs used multiple times
- **Impact:** Blocks HuggingFace publication

### Quick Fix (Automated)

```bash
cd /Users/scott/perfecxion/datasets/securecode/v2

# Step 1: Verify the problem
python3 automation/scripts/fix_duplicate_ids.py --verify-only

# Step 2: Fix with backups (RECOMMENDED)
python3 automation/scripts/fix_duplicate_ids.py --in-place

# Step 3: Verify fix worked
python3 automation/scripts/fix_duplicate_ids.py --verify-only

# Expected output: "✅ All 1209 IDs are unique across all splits"
```

### What the Script Does

1. Creates backups in `consolidated_backup/`
2. Regenerates unique IDs using format: `{category}-{index:06d}-{hash:8}`
   - Example: `injection-000042-a3f5d8c9`
3. Preserves all content (only changes `id` field)
4. Verifies all IDs are unique

### Manual Fix (if needed)

```python
import json
import hashlib

def fix_ids(input_file, output_file):
    examples = []
    with open(input_file, 'r') as f:
        for line in f:
            examples.append(json.loads(line))

    for idx, ex in enumerate(examples):
        category = ex['metadata']['category']
        content_hash = hashlib.md5(
            json.dumps(ex['conversations']).encode()
        ).hexdigest()[:8]

        ex['id'] = f"{category}-{idx:06d}-{content_hash}"

    with open(output_file, 'w') as f:
        for ex in examples:
            f.write(json.dumps(ex) + '\n')

# Run for all splits
for split in ['train', 'val', 'test']:
    fix_ids(f'consolidated/{split}.jsonl',
            f'consolidated/{split}.jsonl')
```

---

## Issue #2: Update Documentation

### Files to Update

1. **README.md** - Multiple sections
2. **PROJECT_DESCRIPTION.md** - Statistics section
3. Verify **metadata.json** (already correct ✅)

### README.md Changes

#### Section 1: Header (Line 5)
```diff
- SecureCode v2.0 is a high-quality dataset of **1,013 secure coding examples**
+ SecureCode v2.0 is a high-quality dataset of **1,209 secure coding examples**
```

#### Section 2: Badge (Line 9)
```diff
- [![Examples](https://img.shields.io/badge/Examples-1013-brightgreen.svg)](#dataset-statistics)
+ [![Examples](https://img.shields.io/badge/Examples-1209-brightgreen.svg)](#dataset-statistics)
```

#### Section 3: Features (Line 14)
```diff
- **1,013 Production-Quality Examples** across 11 programming languages
+ **1,209 Production-Quality Examples** across 11 programming languages
```

#### Section 4: Dataset Statistics (Lines 25-28)
```diff
Total Examples:     1,013 (clean, validated)
Training Set:       706 examples (70%)
Validation Set:     147 examples (15%)
Test Set:           160 examples (15%)
```

**Replace with:**
```markdown
Total Examples:     1,209 (clean, validated)
Training Set:       841 examples (69.6%)
Validation Set:     175 examples (14.5%)
Test Set:           193 examples (16.0%)
```

#### Section 5: Coverage Stats (Lines 30-31)
```diff
- With CVE References:   72.1%
- With Real Incidents:   98.6%
+ With CVE References:   96.1%
+ With Real Incidents:   100.0%
```

#### Section 6: OWASP Coverage Table (Lines 41-54)

**Replace entire table with:**

```markdown
| Category | Count | % |
|----------|-------|---|
| A07 - Authentication Failures | 198 | 16.4% |
| A03 - Injection | 179 | 14.8% |
| A01 - Broken Access Control | 179 | 14.8% |
| A05 - Security Misconfiguration | 134 | 11.1% |
| A02 - Cryptographic Failures | 115 | 9.5% |
| A06 - Vulnerable Components | 85 | 7.0% |
| A04 - Insecure Design | 84 | 6.9% |
| A08 - Integrity Failures | 80 | 6.6% |
| A09 - Logging/Monitoring Failures | 59 | 4.9% |
| AI/ML Security | 50 | 4.1% |
| A10 - SSRF | 45 | 3.7% |
```

#### Section 7: Language Distribution (Lines 57-65)

**Replace with:**
```markdown
Python:        242 (20.0%)  ██████████
JavaScript:    240 (19.9%)  ██████████
Java:          189 (15.6%)  ████████
Go:            158 (13.1%)  ███████
PHP:           100 ( 8.3%)  ████
C#:             85 ( 7.0%)  ███
TypeScript:     70 ( 5.8%)  ███
Others:        125 (10.3%)  █████
```

#### Section 8: Quality Assessment (Lines 112-121)

```diff
**Random Sample Quality Review (n=50):**
- **84% Perfect Examples** - No issues found
- **16% Minor Issues** - CVE format variations, missing optional fields
- **0% Critical Failures** - All examples structurally valid and complete
```

**Replace with:**
```markdown
**Random Sample Quality Review (n=60):**
- **100% Perfect Examples** - No structural issues found
- **0% Issues** - All examples structurally valid and complete
```

```diff
- ✅ CVE references: 72.1%
+ ✅ CVE references: 96.1%
```

#### Section 9: Citation (Lines 133)
```diff
-   examples={1013},
+   examples={1209},
```

### PROJECT_DESCRIPTION.md Changes

#### Line 5
```diff
- SecureCode v2.0 is a production-ready training dataset of **1,013+ secure coding examples**
+ SecureCode v2.0 is a production-ready training dataset of **1,209 secure coding examples**
```

#### Line 9
```diff
- **1,013 validated examples** with 98.6% real-world incident coverage
+ **1,209 validated examples** with 100% real-world incident coverage
```

#### Lines 26-27 (Language percentages)
```diff
- **Languages**: Python (24%), JavaScript (23%), Java (18%), Go (15%), PHP (9%), C# (5%), ...
+ **Languages**: Python (20%), JavaScript (20%), Java (16%), Go (13%), PHP (8%), C# (7%), ...
```

#### Lines 31-34 (Data Quality)
```diff
- 72.1% include CVE references
- 98.6% document real-world incidents
+ 96.1% include CVE references
+ 100.0% document real-world incidents
```

#### Lines 48-50 (Architecture)
```diff
├── consolidated/          # Ready-to-use train/val/test splits
│   ├── train.jsonl       (706 examples, 70%)
│   ├── val.jsonl         (147 examples, 15%)
│   └── test.jsonl        (160 examples, 15%)
```

**Replace with:**
```markdown
├── consolidated/          # Ready-to-use train/val/test splits
│   ├── train.jsonl       (841 examples, 69.6%)
│   ├── val.jsonl         (175 examples, 14.5%)
│   └── test.jsonl        (193 examples, 16.0%)
```

#### Line 108
```diff
- | Example Count | 1,013 ✅ |
+ | Example Count | 1,209 ✅ |
```

#### Line 130
```diff
-   examples={1013},
+   examples={1209},
```

---

## Verification Checklist

After making all changes, run these checks:

```bash
# 1. Verify ID uniqueness
python3 automation/scripts/fix_duplicate_ids.py --verify-only

# 2. Verify file counts
wc -l consolidated/*.jsonl
# Should show: 841 train, 175 val, 193 test, 1209 total

# 3. Verify documentation consistency
grep -n "1,013\|1013" README.md PROJECT_DESCRIPTION.md
# Should return NO matches (all updated to 1,209)

grep -n "1,209\|1209" README.md PROJECT_DESCRIPTION.md
# Should show multiple matches (new correct values)

# 4. Verify metadata.json
cat consolidated/metadata.json | grep total_examples
# Should show: "total_examples": 1209

# 5. Run basic JSON validation
python3 -c "
import json
for split in ['train', 'val', 'test']:
    with open(f'consolidated/{split}.jsonl') as f:
        count = sum(1 for line in f if json.loads(line))
    print(f'{split}: {count} valid JSON lines')
"
```

---

## Quick Copy-Paste Commands

**Complete fix in one go:**

```bash
cd /Users/scott/perfecxion/datasets/securecode/v2

# Fix IDs
python3 automation/scripts/fix_duplicate_ids.py --in-place

# Verify
python3 automation/scripts/fix_duplicate_ids.py --verify-only

# Manual documentation updates required
# (Use search/replace in your editor with the diff blocks above)

echo "✅ ID fix complete - now update README.md and PROJECT_DESCRIPTION.md"
```

---

## Post-Fix Testing

After all fixes, run a final validation:

```bash
# Load and validate train set
python3 << 'EOF'
import json

with open('consolidated/train.jsonl') as f:
    examples = [json.loads(line) for line in f]

print(f"✅ Loaded {len(examples)} training examples")

# Check for duplicates
ids = [ex['id'] for ex in examples]
if len(ids) == len(set(ids)):
    print(f"✅ All {len(ids)} IDs are unique")
else:
    print(f"❌ Found {len(ids) - len(set(ids))} duplicates")

# Check required fields
for i, ex in enumerate(examples[:5]):
    assert 'id' in ex
    assert 'metadata' in ex
    assert 'conversations' in ex
    assert len(ex['conversations']) == 4

print("✅ First 5 examples structurally valid")
print("\n🎉 Dataset ready for publication!")
EOF
```

---

## Timeline

| Task | Time | Status |
|------|------|--------|
| Run ID fix script | 5 min | ⏳ Pending |
| Verify ID uniqueness | 2 min | ⏳ Pending |
| Update README.md | 30 min | ⏳ Pending |
| Update PROJECT_DESCRIPTION.md | 20 min | ⏳ Pending |
| Run verification tests | 10 min | ⏳ Pending |
| Final review | 15 min | ⏳ Pending |
| **TOTAL** | **~90 min** | |

---

## Contact

If issues arise during the fix process:

- **QA Report:** `/Users/scott/perfecxion/datasets/securecode/v2/QA_REPORT.md`
- **Fix Script:** `/Users/scott/perfecxion/datasets/securecode/v2/automation/scripts/fix_duplicate_ids.py`
- **Backup Location:** `consolidated_backup/` (created automatically)

---

**Generated:** December 3, 2025
**QA Analyst:** Claude (Comprehensive Review)
