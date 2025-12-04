# SecureCode v2.0 - Quick Start Guide

**Goal**: Build a production-grade secure code training dataset from scratch

---

## 📁 What You Have (Foundation Files)

All files are in: `/Users/scott/perfecxion/datasets/securecode/v2/`

### Documentation
1. **`README.md`** - Main documentation, usage examples, dataset statistics
2. **`PROJECT_SUMMARY.md`** - Complete project overview, what's built, next steps
3. **`DATASET_DESIGN.md`** - Technical specification, target coverage, quality standards
4. **`COMPARISON_v1_vs_v2.md`** - Side-by-side quality comparison
5. **`QUICK_START.md`** - This file

### Technical Files
6. **`schema.json`** - JSON validation schema for examples
7. **`taxonomy.yaml`** - Complete vulnerability taxonomy (OWASP, CWE, incidents)
8. **`generation/validators.py`** - 5-stage validation framework (TESTED ✅)
9. **`generation/generate_examples.py`** - Example generation framework

---

## 🎯 Current Status

✅ **Foundation Complete** - All infrastructure ready
🔄 **Next Phase** - Begin OWASP Top 10 example generation

---

## 🚀 How to Generate Examples

### Option 1: Start Simple (Recommended)
Use the tested framework to generate your first batch:

```bash
cd /Users/scott/perfecxion/datasets/securecode/v2/generation

# Run the generation script
python3 generate_examples.py
```

**What happens:**
- Generates 2 SQL injection examples (Python, JavaScript)
- Runs all 5 validation checks
- Creates `data/train.jsonl`, `data/validation.jsonl`, `data/test.jsonl`
- Generates validation reports

### Option 2: Generate Specific Category
```bash
# Customize the script to generate specific vulnerabilities
python3 generate_examples.py --category injection --count 50
```

### Option 3: AI-Assisted Generation (Hybrid Approach)
Use my expertise to generate examples, then validate:

```python
# In your code or conversation:
from validators import DatasetValidator
from pathlib import Path

# Create example (manually or via AI)
example = {
    "id": "sql-injection-000001",
    "metadata": {...},
    "conversations": [...]
}

# Validate
validator = DatasetValidator(Path('../schema.json'))
result = validator.validate_example(example)

if result.passed:
    print("✓ Ready to add to dataset")
else:
    for issue in result.issues:
        print(f"✗ {issue['message']}")
```

---

## 📊 Target Dataset Structure

### Total: 1,000 examples

**OWASP Top 10 (940 examples):**
- A01: Broken Access Control - 150
- A02: Cryptographic Failures - 120
- A03: Injection - 140 ⭐ **START HERE**
- A04: Insecure Design - 80
- A05: Security Misconfiguration - 100
- A06: Vulnerable Components - 60
- A07: Auth Failures - 130
- A08: Data Integrity Failures - 70
- A09: Logging Failures - 50
- A10: SSRF - 40

**Modern Threats (150 examples):**
- Cloud Security - 50
- API Security - 50
- AI/ML Security - 50

---

## ✅ Validation Checklist

Every example must pass:

1. ✅ **Schema Validation** - Correct JSON structure
2. ✅ **Encoding Validation** - No UTF-8 corruption
3. ✅ **Syntax Validation** - Code compiles/parses
4. ✅ **Security Pattern Validation** - No dangerous patterns in "secure" code
5. ✅ **Duplication Detection** - No identical examples

---

## 📝 Example Template (Copy This)

```json
{
  "id": "vulnerability-######",
  "metadata": {
    "lang": "python",
    "category": "injection",
    "subcategory": "sql_injection",
    "owasp_2021": "A03:2021-Injection",
    "cwe": "CWE-89",
    "severity": "CRITICAL",
    "complexity": "moderate",
    "created": "2025-01-15",
    "validated": false
  },
  "context": {
    "real_world_incident": "2023 MOVEit Transfer SQL injection",
    "impact": "$9.2B damages, 2,100+ orgs, 77M+ records",
    "attack_vector": "Unauthenticated SQL injection via HTTP",
    "cve": "CVE-2023-34362",
    "year": 2023
  },
  "conversations": [
    {
      "turn": 1,
      "from": "human",
      "value": "Show me how to query a database safely"
    },
    {
      "turn": 2,
      "from": "assistant",
      "value": "**Vulnerable Code:**\n```python\n[vulnerable example]\n```\n\n**Why Dangerous:** [explanation]\n\n**Secure Code:**\n```python\n[secure example]\n```\n\n**Key Controls:** [security principles]"
    }
  ],
  "validation": {
    "syntax_check": "not_tested",
    "security_review": "not_reviewed",
    "code_execution": "not_tested",
    "encoding_check": "not_tested",
    "duplication_check": "not_tested",
    "reviewed_by": "not_reviewed",
    "review_date": "2025-01-15",
    "issues": []
  }
}
```

---

## 🎓 Quality Standards

### Every Example Must Have:

- ✅ **Multi-turn conversation** (2-8 turns)
- ✅ **Vulnerable code example** with explanation of WHY it's dangerous
- ✅ **Secure code example** with explanation of WHY it works
- ✅ **Real-world context** (CVE or incident when available)
- ✅ **Attack payload** (show what actual exploit looks like)
- ✅ **Security principles** (list 3-5 key controls)

### Example Quality Checklist:

- [ ] Code is syntactically valid (passes language parser)
- [ ] Vulnerable code is actually exploitable
- [ ] Secure code completely fixes the vulnerability
- [ ] No dangerous patterns in "secure" code (eval, exec, etc.)
- [ ] Includes real dollar amounts or record counts for impact
- [ ] Uses recent incidents (2023-2025 preferred)
- [ ] Conversation flows naturally
- [ ] Explanations are clear and educational

---

## 📈 Recommended Generation Order

### Week 1: Foundation (COMPLETE ✅)
- Schema, taxonomy, validation, documentation

### Week 2: High-Priority Injection (Target: 140 examples)
1. **SQL Injection** - 35 examples (Python, PHP, Java, JavaScript, C#, Ruby)
2. **Command Injection** - 25 examples
3. **Code Injection** - 25 examples
4. **NoSQL Injection** - 15 examples
5. **Template Injection** - 15 examples
6. **XML/XXE Injection** - 15 examples
7. **LDAP Injection** - 10 examples

### Week 3: Access Control + Auth (Target: 280 examples)
- Broken Access Control - 150
- Auth Failures - 130

### Week 4: Crypto + Config (Target: 220 examples)
- Cryptographic Failures - 120
- Security Misconfiguration - 100

### Week 5: Modern Threats (Target: 150 examples)
- Cloud Security - 50
- API Security - 50
- AI/ML Security - 50

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'jsonschema'"
```bash
pip3 install jsonschema pyyaml
# or
python3 -m pip install jsonschema pyyaml
```

### Validation fails with encoding errors
- Check for non-ASCII characters in code blocks
- Use UTF-8 encoding when saving files
- Run: `python3 validators.py` to test

### Need to add new vulnerability type
1. Add to `taxonomy.yaml` under appropriate category
2. Create generator in `generation/templates/{subcategory}.py`
3. Follow `SQLInjectionGenerator` pattern
4. Test with validators before adding to dataset

---

## 📞 Next Steps

**Immediate:** Choose generation approach

1. **Manual Expert Creation** (highest quality)
   - Security experts write each example
   - Slow but guaranteed quality
   - Est. 15-20 min per example

2. **AI-Assisted Generation** (balanced)
   - AI generates examples
   - Expert reviews and validates
   - Est. 5-10 min per example

3. **Hybrid Approach** (recommended)
   - AI generates draft examples
   - Automated validation catches issues
   - Expert spot-checks critical examples
   - Est. 7-12 min per example

**Then:** Start with SQL injection examples (most common, well-understood)

**Goal:** 140 injection examples by end of Week 2

---

## 📊 Progress Tracking

Create a simple tracking file:

```bash
# Track progress
echo "Category,Target,Generated,Validated,Pass Rate" > progress.csv
echo "SQL Injection,35,0,0,0%" >> progress.csv
echo "Command Injection,25,0,0,0%" >> progress.csv
# ... etc
```

---

## 🎯 Success Metrics

Track these as you generate:

| Metric | Target |
|--------|--------|
| Validation Pass Rate | 100% |
| Multi-turn (2+ turns) | 90%+ |
| With Real-World Context | 70%+ |
| Avg Conversation Turns | 3-5 |
| Code Syntax Errors | 0% |
| Encoding Errors | 0% |

---

## 💡 Pro Tips

1. **Start with well-known vulnerabilities** (SQL injection, XSS)
2. **Use real CVEs** - search CVE database for recent incidents
3. **Include actual exploit payloads** - show what attacks look like
4. **Quantify impact** - use real numbers ($9.2B, 77M records)
5. **Multi-turn progression** - start simple, add complexity
6. **Test code** - actually run it to ensure it works
7. **Validate early** - don't generate 100 examples before validating

---

## 📚 Reference Links

- OWASP Top 10 2021: https://owasp.org/Top10/
- CWE Database: https://cwe.mitre.org/
- CVE Search: https://cve.mitre.org/
- Real-world incidents: See `taxonomy.yaml` incidents section

---

**Ready to start generating?** You have everything you need. The foundation is solid and tested.

**Recommended first step:** Generate 5-10 SQL injection examples manually to establish quality standards, then scale up with AI assistance.
