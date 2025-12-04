# SecureCode v2.0 - API-Driven Generation System

**Automated generation of 910 remaining examples using Claude and OpenAI APIs**

---

## Quick Start

### 1. Set Up API Keys

```bash
# For Claude (recommended for complex security patterns)
export ANTHROPIC_API_KEY='sk-ant-...'

# For OpenAI (good for bulk generation)
export OPENAI_API_KEY='sk-...'

# You can use both - the system will choose based on generation_plan.yaml
```

### 2. Test Configuration

```bash
cd /Users/scott/perfecxion/datasets/securecode/v2
./automation/scripts/test_generation.sh
```

This will:
- ✅ Verify API keys
- ✅ Generate 2 test examples (~$0.50)
- ✅ Validate the results
- ✅ Confirm everything is working

### 3. Run Full Generation

```bash
./automation/scripts/run_generation.sh
```

**Estimated:**
- **Time**: 6-12 hours (mostly automated)
- **Cost**: $60-100 in API fees
- **Output**: 910 new examples (90 → 1,000 total)

---

## System Overview

### Architecture

```
automation/
├── config/
│   └── generation_plan.yaml      # Defines all 910 examples to generate
├── prompts/
│   └── master_prompt_template.txt # Quality standards and requirements
├── scripts/
│   ├── api_generator.py           # Main generation engine
│   ├── test_generation.sh         # Test script
│   └── run_generation.sh          # Full execution script
└── logs/
    └── generation_YYYYMMDD_HHMMSS.log  # Detailed logs
```

### Generation Plan

The `generation_plan.yaml` defines **91 batches** across **11 phases**:

| Phase | Category | Examples | Provider | Cost Est. |
|-------|----------|----------|----------|-----------|
| 1 | A03: Injection (remaining) | 50 | Mixed | $6 |
| 2 | A07: Auth Failures | 150 | Claude | $18 |
| 3 | A01: Broken Access Control | 150 | Claude | $18 |
| 4 | A05: Security Misconfiguration | 120 | OpenAI | $12 |
| 5 | A02: Cryptographic Failures | 100 | Claude | $12 |
| 6 | A04: Insecure Design | 80 | Claude | $10 |
| 7 | A06: Vulnerable Components | 80 | OpenAI | $8 |
| 8 | A08: Integrity Failures | 80 | Claude | $10 |
| 9 | A09: Logging Failures | 60 | OpenAI | $6 |
| 10 | A10: SSRF | 50 | Claude | $6 |
| 11 | AI/ML Security | 150 | Claude | $18 |
| **TOTAL** | **ALL CATEGORIES** | **910** | **Mixed** | **~$100** |

---

## Manual Generation (Single Batch)

### Generate One Batch

```bash
# Using Claude (best for complex security patterns)
python3 automation/scripts/api_generator.py \
    --batch 011 \
    --provider claude \
    --parallel 2

# Using OpenAI (faster, cheaper for simpler patterns)
python3 automation/scripts/api_generator.py \
    --batch 011 \
    --provider openai \
    --parallel 4
```

### Options

- `--batch BATCH_ID` - Generate specific batch (e.g., "011", "016")
- `--provider {claude,openai,gemini}` - API provider to use
- `--parallel N` - Number of parallel API calls (1-10)
- `--dry-run` - Show what would be generated without calling APIs
- `--api-key KEY` - Override API key (or use environment variable)

### Examples

```bash
# Dry run to see what batch 011 would generate
python3 automation/scripts/api_generator.py --batch 011 --dry-run

# Generate batch 011 with Claude (2 parallel calls)
python3 automation/scripts/api_generator.py \
    --batch 011 \
    --provider claude \
    --parallel 2

# Generate batch 016-025 (auth failures) with Claude
for i in {016..025}; do
    python3 automation/scripts/api_generator.py \
        --batch $i \
        --provider claude \
        --parallel 3
    sleep 10
done
```

---

## Quality Standards

Every generated example follows these standards:

### 1. Structure
- ✅ **4-turn conversation** (8 total messages)
- ✅ Turn 1: Basic question
- ✅ Turn 2: Vulnerable → Secure code with explanations
- ✅ Turn 3: Advanced follow-up question
- ✅ Turn 4: Production-ready pattern with defense in depth

### 2. Code Quality
- ✅ **Syntactically valid** code for all 11 languages
- ✅ Complete implementations (not just snippets)
- ✅ Includes imports, class declarations, error handling
- ✅ Proper language-specific patterns

### 3. Security Content
- ✅ **Real CVEs** from 2022-2025 (when available)
- ✅ Specific attack payloads with explanations
- ✅ Quantified impact (dollar amounts, user counts)
- ✅ Multiple defensive layers (defense in depth)
- ✅ Production best practices (monitoring, logging, rate limiting)

### 4. Validation
- ✅ **Automatic validation** after generation
- ✅ Syntax checking for all code blocks
- ✅ Security pattern verification
- ✅ Schema compliance
- ✅ Retry logic for failures (up to 3 attempts)

---

## Validation & Quality Control

### Automatic Validation

The generator includes built-in validation:

```python
# Validates:
- JSON structure compliance
- Required fields present
- 4-turn conversation structure
- Metadata completeness
- Validation field format
```

### Manual Review

After generation, run comprehensive validation:

```bash
# Validate all generated batches
python3 generation/validate_all_batches.py

# Review any failures
python3 generation/analyze_all_failures.py

# Comprehensive QA report
python3 generation/comprehensive_qa.py
```

### Expected Pass Rates

- **Target**: 90%+ validation pass rate
- **Claude examples**: 95%+ (higher quality, fewer retries)
- **OpenAI examples**: 85-90% (may need more fixes)

### Handling Failures

If examples fail validation:

1. **Check logs**: `automation/logs/generation_*.log`
2. **Common issues**:
   - Missing class declarations (Java/C#)
   - SQL payloads in wrong code blocks
   - Incomplete conversation turns
3. **Fix and regenerate**:
   ```bash
   # Regenerate specific batch
   python3 automation/scripts/api_generator.py --batch 011 --provider claude
   ```

---

## Cost Optimization

### Provider Selection Strategy

**Use Claude for:**
- ✅ Advanced injection techniques (blind SQLi, XXE, SSTI)
- ✅ Authentication & authorization (critical security)
- ✅ Cryptography (precision required)
- ✅ AI/ML security (specialized knowledge)
- ✅ Complex multi-step attacks

**Use OpenAI for:**
- ✅ Simple XSS patterns
- ✅ Security misconfigurations
- ✅ Dependency vulnerabilities
- ✅ Logging failures
- ✅ Bulk generation of similar patterns

### Cost Breakdown

**Claude** (550 examples @ $0.12/example avg):
- Input: ~1.1M tokens @ $3/M = $3.30
- Output: ~3.3M tokens @ $15/M = $49.50
- **Total: ~$53**

**OpenAI** (360 examples @ $0.10/example avg):
- Input: ~0.7M tokens @ $10/M = $7.00
- Output: ~1.8M tokens @ $30/M = $54.00
- **Total: ~$61... wait that's more expensive!**

Let me recalculate:
- OpenAI GPT-4 Turbo: $10/M input, $30/M output
- Per example: ~2K input, ~5K output = $0.02 + $0.15 = $0.17/example
- 360 examples = ~$61

**Revised Recommendation**: Use Claude for everything, it's actually more cost-effective at scale:
- Claude: 910 examples @ $0.12/example = **$109**
- Better quality, fewer retries, better security understanding

### Parallel Generation

```bash
# Conservative (safer, less rate limiting risk)
--parallel 1   # Sequential, slowest

# Balanced (recommended)
--parallel 2-3 # Good throughput, minimal rate limit risk

# Aggressive (fastest, but watch rate limits)
--parallel 5-10 # High throughput, may hit rate limits
```

---

## Monitoring Progress

### Real-time Progress

Watch the generation in real-time:

```bash
tail -f automation/logs/generation_$(date +%Y%m%d)*.log
```

### Statistics

The generator prints stats after each batch:

```
Batch 011 Stats:
  Success: 10/10
  Failed: 0
  API Calls: 13 (3 retries)
  Retries: 3
  Tokens: 45,231
  Estimated Cost: $2.26
```

### Overall Progress

Check the data directory:

```bash
# Count generated examples
ls -1 data/*.jsonl | wc -l

# Count total examples across all files
cat data/*.jsonl | wc -l
```

---

## Troubleshooting

### "No API key found"

```bash
# Set the appropriate API key
export ANTHROPIC_API_KEY='sk-ant-...'
# or
export OPENAI_API_KEY='sk-...'
```

### "Rate limit exceeded"

**Solution**: Reduce parallelism

```bash
# Instead of --parallel 10, use:
--parallel 2

# Add delays between batches
sleep 30
```

### "JSON parsing failed"

**Cause**: API returned invalid JSON
**Solution**: Automatic retry (up to 3 attempts)
**Manual fix**: Check logs for the response, manually fix if needed

### "Validation failed"

**Common issues**:
1. **SQL payloads in Python code blocks**
   - Fix: Change ```python to ```sql for payload examples
2. **Missing class declarations**
   - Fix: Add complete class wrappers to Java/C# code
3. **Incomplete conversation turns**
   - Fix: Regenerate with updated prompt

### "API timeout"

**Solution**: Increase max_tokens or retry

```python
# In api_generator.py, increase timeout:
max_tokens=8192  # Instead of 4096
```

---

## Advanced Usage

### Custom Generation Plan

Edit `automation/config/generation_plan.yaml`:

```yaml
batches:
  - batch_id: "999"
    name: "Custom Batch"
    category: "custom"
    subcategory: "custom_vulnerability"
    count: 10
    provider: "claude"
    languages: ["python", "javascript"]
    techniques:
      - "Custom technique 1"
      - "Custom technique 2"
```

Then generate:

```bash
python3 automation/scripts/api_generator.py --batch 999 --provider claude
```

### Custom Prompts

Modify `automation/prompts/master_prompt_template.txt` to:
- Add new quality requirements
- Change conversation structure
- Include different code patterns
- Add new validation rules

### Batch Management

```bash
# Generate specific range
for i in {011..015}; do
    python3 automation/scripts/api_generator.py --batch $i --provider claude
done

# Resume from specific batch
for i in {025..030}; do
    python3 automation/scripts/api_generator.py --batch $i --provider openai
done
```

---

## Performance Tuning

### Optimal Settings

**For Claude:**
```bash
--provider claude
--parallel 2-3     # Balance speed and quality
```

**For OpenAI:**
```bash
--provider openai
--parallel 4-5     # Can handle more parallelism
```

### Speed vs Quality Trade-off

| Setting | Speed | Quality | Cost | Best For |
|---------|-------|---------|------|----------|
| `--parallel 1` | ⭐ | ⭐⭐⭐⭐⭐ | $$ | Maximum quality |
| `--parallel 2-3` | ⭐⭐⭐ | ⭐⭐⭐⭐ | $$ | **Recommended** |
| `--parallel 5-10` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | $$$ | Bulk generation |

---

## FAQ

**Q: Can I use free tier API keys?**
A: No. This requires paid API access with sufficient rate limits.

**Q: Can I pause and resume generation?**
A: Yes! The script generates batch-by-batch. You can stop anytime and resume by running specific batches.

**Q: What if I run out of API credits midway?**
A: Generation stops. Resume by rerunning with the next batch number.

**Q: Can I generate examples in other languages?**
A: Yes! Edit `generation_plan.yaml` and add languages to the `languages` array.

**Q: How do I regenerate failed examples?**
A: Rerun the same batch: `python3 automation/scripts/api_generator.py --batch 011`

**Q: Can I use local models instead of APIs?**
A: Not currently supported, but you could adapt the script to use Ollama or similar.

---

## Next Steps After Generation

1. **Validate all examples**:
   ```bash
   python3 generation/validate_all_batches.py
   ```

2. **Review failures**:
   ```bash
   python3 generation/analyze_all_failures.py
   ```

3. **Fix failed examples** (manual or regenerate)

4. **Run comprehensive QA**:
   ```bash
   python3 generation/comprehensive_qa.py
   ```

5. **Create train/validation/test splits**:
   ```bash
   python3 generation/create_splits.py
   ```

6. **Package for distribution**:
   ```bash
   python3 generation/package_dataset.py
   ```

---

## Support

**Issues**: Create a GitHub issue or check logs in `automation/logs/`

**Logs**: Detailed generation logs saved to:
- `automation/logs/generation_YYYYMMDD_HHMMSS.log`

**Validation**: Results saved to:
- `validation/reports/`

---

**Ready to generate 910 examples? Start with:**

```bash
./automation/scripts/test_generation.sh
```

Then, when ready:

```bash
./automation/scripts/run_generation.sh
```
