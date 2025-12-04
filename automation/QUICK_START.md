# Quick Start: Generate 910 Examples in 3 Steps

## Step 1: Set API Keys (2 minutes)

```bash
# Open your terminal in the project directory
cd /Users/scott/perfecxion/datasets/securecode/v2

# Set your API keys (you can use one or both)
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
export OPENAI_API_KEY='sk-your-key-here'

# Verify keys are set
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY
```

**API Key Info:**
- **Claude**: Get from https://console.anthropic.com/
- **OpenAI**: Get from https://platform.openai.com/api-keys

---

## Step 2: Test the System (5 minutes, ~$0.50 cost)

```bash
./automation/scripts/test_generation.sh
```

This will:
1. ✅ Verify your API keys work
2. ✅ Generate 2 test examples
3. ✅ Validate them automatically
4. ✅ Confirm everything is ready

**Expected output:**
```
Test 1: Dry run (verifying configuration)
✓ Configuration valid

Test 2: Generate 2 examples (real API calls)
Continue? (y/n) y
✓ Generated xss-000001 (tokens: 1243/2891)
✓ Generated xss-000002 (tokens: 1198/2754)
✓ Test generation complete

Test 3: Validate generated examples
✓ PASSED: xss-000001
✓ PASSED: xss-000002

✓ ALL TESTS PASSED
```

---

## Step 3: Run Full Generation (6-12 hours, ~$100 cost)

### Option A: Full Automated Generation (Recommended)

```bash
# This generates all 910 examples automatically
./automation/scripts/run_generation.sh
```

**What happens:**
- Runs through all 11 phases (injection → auth → access control → ... → AI/ML)
- Uses Claude for complex patterns, OpenAI GPT-5.1 for simpler patterns
- Automatically validates each batch
- Saves detailed logs
- Estimated time: 6-12 hours (mostly unattended)
- Estimated cost: ~$100

**You can:**
- ✅ Run overnight
- ✅ Pause anytime (Ctrl+C)
- ✅ Resume from any batch
- ✅ Monitor logs in real-time

### Option B: Generate One Batch at a Time

```bash
# Generate just Batch 011 (XSS Expansion Part 2 - 10 examples)
python3 automation/scripts/api_generator.py \
    --batch 011 \
    --provider openai \
    --parallel 3

# Check results
python3 generation/validate_all_batches.py
```

**Batch numbering:**
- `011-015`: Complete injection category (50 examples)
- `016-030`: Authentication failures (150 examples)
- `031-045`: Broken access control (150 examples)
- `046-057`: Security misconfigurations (120 examples)
- `058-067`: Cryptographic failures (100 examples)
- `068-075`: Insecure design (80 examples)
- `076-083`: Vulnerable components (80 examples)
- `084-091`: Integrity failures (80 examples)
- `092-097`: Logging failures (60 examples)
- `098-102`: SSRF (50 examples)
- `103-117`: AI/ML security (150 examples)

---

## Monitoring Progress

### Watch generation in real-time:

```bash
# In another terminal window
tail -f automation/logs/generation_*.log
```

### Check how many examples have been generated:

```bash
# Count JSONL files
ls -1 data/*.jsonl | wc -l

# Count total examples
cat data/*.jsonl | wc -l
```

---

## What to Do If Something Fails

### Issue: "No API key found"

**Fix:**
```bash
export ANTHROPIC_API_KEY='your-key'
# or
export OPENAI_API_KEY='your-key'
```

### Issue: "Rate limit exceeded"

**Fix:** Use lower parallelism
```bash
# Instead of --parallel 10, use:
python3 automation/scripts/api_generator.py --batch 011 --provider claude --parallel 2
```

### Issue: Some examples failed validation

**Fix:** Regenerate that specific batch
```bash
python3 automation/scripts/api_generator.py --batch 011 --provider claude
```

---

## After Generation is Complete

### 1. Validate Everything

```bash
python3 generation/validate_all_batches.py
```

**Expected result:**
```
Total Examples: 1,000
Passed: 950 (95.0%)
Failed: 50 (5.0%)
```

### 2. Review Failures (if any)

```bash
python3 generation/analyze_all_failures.py
```

### 3. Fix Failed Examples

Either:
- **Regenerate the batch**: `python3 automation/scripts/api_generator.py --batch 011`
- **Manual fixes**: Similar to how we fixed Batch 010

### 4. Create Final Dataset Splits

```bash
# Create train/validation/test splits (800/100/100)
python3 generation/create_splits.py
```

---

## Cost Breakdown

| Phase | Category | Examples | Provider | Cost |
|-------|----------|----------|----------|------|
| Current | Batches 001-010 | 90 | Manual | $0 |
| Phase 1 | Injection (remaining) | 50 | Mixed | $6 |
| Phase 2 | Authentication | 150 | Claude | $18 |
| Phase 3 | Access Control | 150 | Claude | $18 |
| Phase 4 | Misconfigurations | 120 | OpenAI | $12 |
| Phase 5 | Cryptography | 100 | Claude | $12 |
| Phase 6 | Design Flaws | 80 | Claude | $10 |
| Phase 7 | Dependencies | 80 | OpenAI | $8 |
| Phase 8 | Integrity | 80 | Claude | $10 |
| Phase 9 | Logging | 60 | OpenAI | $6 |
| Phase 10 | SSRF | 50 | Claude | $6 |
| Phase 11 | AI/ML Security | 150 | Claude | $18 |
| **TOTAL** | **1,000 examples** | **1,000** | **Mixed** | **~$124** |

**Note**: Actual costs may vary based on:
- Retry attempts (failed examples regenerated)
- Token usage per example
- API pricing changes

---

## Time Estimates

| Approach | Time | Attention Required |
|----------|------|-------------------|
| **Full automated** | 6-12 hours | 30 min (setup + monitoring) |
| **Batch by batch** | 1-2 weeks | 2-3 hours/day |
| **Current manual method** | 180+ hours | Full attention |

---

## Tips for Success

### ✅ DO:
- Start with test_generation.sh to verify everything works
- Run full generation overnight or during work hours
- Monitor logs occasionally
- Keep API keys secure (don't commit to git)
- Use Claude for complex security patterns
- Use OpenAI GPT-5.1 for simpler/bulk generation

### ❌ DON'T:
- Don't interrupt generation mid-batch (let batches complete)
- Don't use --parallel > 5 with Claude (rate limits)
- Don't commit API keys to version control
- Don't skip validation step

---

## Commands Cheat Sheet

```bash
# Test everything
./automation/scripts/test_generation.sh

# Generate all remaining examples
./automation/scripts/run_generation.sh

# Generate one batch
python3 automation/scripts/api_generator.py --batch 011 --provider claude

# Generate with parallelism
python3 automation/scripts/api_generator.py --batch 011 --provider openai --parallel 4

# Dry run (see what would be generated)
python3 automation/scripts/api_generator.py --batch 011 --dry-run

# Validate all batches
python3 generation/validate_all_batches.py

# Check logs
tail -f automation/logs/generation_*.log

# Count examples
cat data/*.jsonl | wc -l
```

---

## You're Ready!

**Start here:**

```bash
cd /Users/scott/perfecxion/datasets/securecode/v2
export ANTHROPIC_API_KEY='your-key'
export OPENAI_API_KEY='your-key'
./automation/scripts/test_generation.sh
```

**Then when ready:**

```bash
./automation/scripts/run_generation.sh
```

**Questions?** Check `automation/README.md` for detailed documentation.

---

**Good luck! 🚀**
