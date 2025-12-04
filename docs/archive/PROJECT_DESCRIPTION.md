# SecureCode v2.0 - Project Description

## What is this project?

SecureCode v2.0 is a production-ready training dataset of **1,013+ secure coding examples** designed to teach AI models how to write secure code and detect vulnerabilities. The dataset covers all OWASP Top 10 2021 security categories with real-world incident context, making it ideal for fine-tuning LLMs on security-aware code generation.

## Key Accomplishments

- **1,013 validated examples** with 98.6% real-world incident coverage
- **22-hour automated generation** using Claude Opus 4.5
- **Complete OWASP Top 10 2021 coverage** across 11 programming languages
- **4-turn conversational format**: vulnerable code → secure fix → advanced attack → defense-in-depth
- **Enterprise-grade code** with production patterns (logging, monitoring, error handling)
- **84% perfect quality** in random sample validation
- **Stratified train/test/val splits** (70/15/15) maintaining category balance

## Technical Highlights

### Generation Pipeline
- Automated batch generation system with retry logic and validation
- Multi-stage quality checks (JSON schema, syntax, security patterns)
- Real-time deduplication and encoding validation
- Support for Claude Opus 4.5 and OpenAI GPT-5.1

### Coverage
- **Languages**: Python (24%), JavaScript (23%), Java (18%), Go (15%), PHP (9%), C# (5%), TypeScript, Ruby, Rust, Kotlin, Docker, Kubernetes
- **Categories**: Injection, Authentication Failures, Access Control, Cryptography, Misconfiguration, Vulnerable Components, Integrity Failures, Insecure Design, Logging Failures, SSRF, AI/ML Security
- **Techniques**: 209 unique attack/defense patterns from basic to advanced

### Data Quality
- 72.1% include CVE references (CVE-2023-34362, CVE-2024-21762, etc.)
- 98.6% document real-world incidents (MOVEit breach, Norton LifeLock attack, etc.)
- Average 8,796 characters per example with 7-9 code blocks
- Zero syntax errors, zero encoding corruption

## Use Cases

1. **LLM Fine-Tuning**: Train models like GPT, Claude, CodeLlama on secure coding
2. **Vulnerability Detection**: Build automated code review and security scanning tools
3. **Developer Education**: Interactive security training and CTF challenges
4. **Security Research**: Study vulnerability patterns and defense mechanisms

## Architecture

```
SecureCode v2.0/
├── consolidated/          # Ready-to-use train/val/test splits
│   ├── train.jsonl       (706 examples, 70%)
│   ├── val.jsonl         (147 examples, 15%)
│   └── test.jsonl        (160 examples, 15%)
├── data/                  # Raw batch files (107 batches)
├── automation/
│   ├── scripts/          # Generation and validation tools
│   ├── config/           # Batch plans and configurations
│   └── prompts/          # Master prompt templates
└── analysis/             # Coverage analysis and reporting tools
```

## Dataset Format

Each example follows a structured 4-turn conversation:

```json
{
  "id": "sql-injection-000001",
  "metadata": {
    "lang": "python",
    "category": "injection",
    "severity": "CRITICAL",
    "owasp_2021": "A03:2021-Injection",
    "cwe": "CWE-89"
  },
  "context": {
    "real_world_incident": "2023 MOVEit Transfer SQL Injection",
    "impact": "$9.2B damages, 2,100+ orgs breached",
    "cve": "CVE-2023-34362",
    "year": 2023
  },
  "conversations": [
    {"turn": 1, "from": "human", "value": "[basic question]"},
    {"turn": 2, "from": "assistant", "value": "[vulnerable + secure code]"},
    {"turn": 3, "from": "human", "value": "[advanced question]"},
    {"turn": 4, "from": "assistant", "value": "[defense-in-depth]"}
  ]
}
```

## Project Timeline

- **Days 1-2**: Automated generation system built with Claude Opus 4.5
- **Day 3**: 22-hour continuous generation run (batches 001-107)
- **Day 4**: Quality review, cleanup, validation pipeline
- **Day 5**: Dataset consolidation, documentation, HuggingFace preparation
- **Status**: ✅ Production Ready, exceeds 1,000 example target

## Technical Stack

- **Generation**: Claude Opus 4.5 (primary), OpenAI GPT-5.1 (supplementation)
- **Languages**: Python 3.12+, YAML, JSON
- **Validation**: JSONSchema, language-specific syntax checkers
- **Infrastructure**: Automated batch processing with error recovery
- **Documentation**: Comprehensive coverage analysis and reporting tools

## Quality Metrics

| Metric | Score |
|--------|-------|
| Example Count | 1,013 ✅ |
| Quality (Random Sample) | 84% Perfect ✅ |
| Real-World Coverage | 98.6% ✅ |
| OWASP Coverage | 100% ✅ |
| Syntax Validation | 100% ✅ |
| Encoding Validation | 100% ✅ |

## Next Steps

- ✅ **Complete**: Core dataset generation and validation
- 🔄 **In Progress**: OpenAI supplementation for additional language coverage
- 📋 **Planned**: HuggingFace Hub publication
- 📋 **Planned**: Research paper and technical blog post

## Citation

```bibtex
@dataset{securecode_v2_2025,
  title={SecureCode v2.0: Comprehensive Secure Coding Training Dataset},
  author={Scott Thornton},
  organization={perfecXion.ai},
  year={2025},
  examples={1013},
  url={https://github.com/perfecxion/securecode-v2}
}
```

---

**Built by**: Scott Thornton (perfecXion.ai)
**License**: MIT
**Contact**: scott@perfecxion.ai

