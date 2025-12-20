---
license: cc-by-nc-sa-4.0
task_categories:
- text-generation
- question-answering
language:
- code
tags:
- security
- owasp
- cve
- secure-coding
- vulnerability-detection
- cybersecurity
- code-security
- ai-safety
- siem
- penetration-testing
- incident-grounding
- defense-in-depth
size_categories:
- 1K<n<10K
pretty_name: SecureCode v2.0
dataset_info:
  features:
  - name: messages
    sequence:
    - name: role
      dtype: string
    - name: content
      dtype: string
  splits:
  - name: train
    num_examples: 989
  - name: validation
    num_examples: 122
  - name: test
    num_examples: 104
configs:
- config_name: default
  data_files:
  - split: train
    path: consolidated/train.jsonl
  - split: validation
    path: consolidated/val.jsonl
  - split: test
    path: consolidated/test.jsonl
---

# SecureCode v2.0: Production-Grade Dataset for Security-Aware Code Generation

<div align="center">

![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-blue.svg)
![Examples](https://img.shields.io/badge/examples-1,215-green.svg)
![Languages](https://img.shields.io/badge/languages-11-orange.svg)
![Quality](https://img.shields.io/badge/quality-100%25_validated-brightgreen.svg)
![CVE Grounding](https://img.shields.io/badge/CVE_grounding-100%25-blue.svg)

**Production-grade security vulnerability dataset with complete incident grounding, 4-turn conversational structure, and comprehensive operational guidance**

[📄 Paper](https://perfecxion.ai/articles/securecode-v2-dataset-paper.html) | [💻 GitHub](https://github.com/scthornton/securecode-v2) | [🤗 Dataset](https://huggingface.co/datasets/scthornton/securecode-v2)

</div>

---

## 🎯 Overview

SecureCode v2.0 is a rigorously validated dataset of **1,215 security-focused coding examples** designed to train security-aware AI code generation models. Every example is grounded in real-world security incidents (CVEs, breach reports), provides both vulnerable and secure implementations, demonstrates concrete attacks, and includes defense-in-depth operational guidance.

### Why SecureCode v2.0?

**The Problem:** AI coding assistants produce vulnerable code in 45% of security-relevant scenarios (Veracode 2025), introducing security flaws at scale.

**The Solution:** SecureCode v2.0 provides production-grade training data with:

- ✅ **100% Incident Grounding** – Every example ties to documented CVEs or security incidents
- ✅ **4-Turn Conversational Structure** – Mirrors real developer-AI workflows
- ✅ **Complete Operational Guidance** – SIEM integration, logging, monitoring, detection
- ✅ **Full Language Fidelity** – Language-specific syntax, idioms, and frameworks
- ✅ **Rigorous Validation** – 100% compliance with structural and security standards

---

## 📊 Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Unique Examples** | 1,215 |
| **Train Split** | 989 examples (81.4%) |
| **Validation Split** | 122 examples (10.0%) |
| **Test Split** | 104 examples (8.6%) |
| **Vulnerability Categories** | 11 (complete OWASP Top 10:2025 + AI/ML Security) |
| **Programming Languages** | 11 total (10 languages + YAML IaC) |
| **Average Conversation Length** | 4 turns (user → assistant → user → assistant) |

### Vulnerability Coverage (OWASP Top 10:2025)

| Category | Examples | Percentage |
|----------|----------|------------|
| **A01: Broken Access Control** | 224 | 18.4% |
| **A07: Authentication Failures** | 199 | 16.4% |
| **A02: Security Misconfiguration** | 134 | 11.0% |
| **A05: Injection** | 125 | 10.3% |
| **A04: Cryptographic Failures** | 115 | 9.5% |
| **A06: Insecure Design** | 103 | 8.5% |
| **A08: Software Integrity Failures** | 90 | 7.4% |
| **A03: Sensitive Data Exposure** | 80 | 6.6% |
| **A09: Logging & Monitoring Failures** | 74 | 6.1% |
| **A10: SSRF** | 71 | 5.8% |
| **AI/ML Security Threats** | (included across categories) |
| **Total** | **1,215** | **100%** |

### Programming Language Distribution

| Language | Examples | Frameworks/Tools |
|----------|----------|------------------|
| **Python** | 255 (21.0%) | Django, Flask, FastAPI |
| **JavaScript** | 245 (20.2%) | Express, NestJS, React, Vue |
| **Java** | 189 (15.6%) | Spring Boot |
| **Go** | 159 (13.1%) | Gin framework |
| **PHP** | 123 (10.1%) | Laravel, Symfony |
| **TypeScript** | 89 (7.3%) | NestJS, Angular |
| **C#** | 78 (6.4%) | ASP.NET Core |
| **Ruby** | 56 (4.6%) | Ruby on Rails |
| **Rust** | 12 (1.0%) | Actix, Rocket |
| **Kotlin** | 9 (0.7%) | Spring Boot |
| **YAML** | (IaC configurations) |

### Severity Distribution

| Severity | Examples | Percentage |
|----------|----------|------------|
| **CRITICAL** | 795 | 65.4% |
| **HIGH** | 384 | 31.6% |
| **MEDIUM** | 36 | 3.0% |

---

## 🔍 What Makes This Different?

### 1. Incident Grounding

Every example references real security incidents:
- **Equifax breach (CVE-2017-5638)** - $425M cost from Apache Struts RCE
- **Capital One SSRF attack (2019)** - 100M customer records exposed
- **SolarWinds supply chain (CVE-2020-10148)** - Documented authentication bypasses

### 2. 4-Turn Conversational Structure

Unlike code-only datasets, each example follows realistic developer workflows:

**Turn 1:** Developer requests functionality ("build JWT authentication")  
**Turn 2:** Assistant provides vulnerable + secure implementations with attack demos  
**Turn 3:** Developer asks advanced questions ("how does this scale to 10K users?")  
**Turn 4:** Assistant delivers defense-in-depth operational guidance

### 3. Comprehensive Operational Guidance

Every example includes:
- **SIEM Integration** - Splunk/Elasticsearch detection rules
- **Logging Strategies** - Security event capture patterns
- **Monitoring Recommendations** - Metrics and alerting
- **Infrastructure Hardening** - Docker, AppArmor, WAF configs
- **Testing Approaches** - Language-specific security testing

### 4. Rigorous Quality Validation

- ✅ **100% CVE Format Compliance** - All CVE references validated
- ✅ **100% Language Tag Validity** - Proper language assignments
- ✅ **100% Structural Compliance** - 4-turn conversation format
- ✅ **Expert Security Review** - Independent validation by security professionals
- ✅ **Zero Content Duplicates** - 1,203 duplicates removed

---

## 📁 Dataset Structure

```
securecode-v2/
├── consolidated/
│   ├── train.jsonl              # 989 training examples
│   ├── val.jsonl                # 122 validation examples
│   └── test.jsonl               # 104 test examples
├── docs/
│   └── paper/
│       ├── secure-code-v2.md    # Full research paper (markdown)
│       ├── secure-code-v2.tex   # LaTeX version
│       └── *.png                # Paper figures and charts
├── scripts/
│   └── validate_contributing_compliance.py
├── README.md                    # This file
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # CC BY-NC-SA 4.0 license
├── CITATION.bib                 # Citation information
├── schema_v2.json               # Dataset schema
└── taxonomy.yaml                # OWASP vulnerability taxonomy
```

### Example Format

Each example is a 4-turn conversation in JSON format:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "How do I implement secure JWT authentication in Express.js?"
    },
    {
      "role": "assistant",
      "content": "# Real-World Incident\nCVE-2022-23529: JWT authentication bypass in production systems...\n\n## Vulnerable Implementation\n[Code showing vulnerability]\n\n## Secure Implementation\n[Code showing fix]\n\n## Attack Demonstration\n[Concrete exploit]"
    },
    {
      "role": "user",
      "content": "How does this scale to 10,000 concurrent users?"
    },
    {
      "role": "assistant",
      "content": "# Production Scaling & Defense-in-Depth\n\n## Performance Considerations\n[Scaling strategies]\n\n## SIEM Integration\n[Detection rules]\n\n## Monitoring & Logging\n[Operational security]"
    }
  ]
}
```

---

## 🚀 Usage

### Load with Hugging Face Datasets

```python
from datasets import load_dataset

# Load the full dataset
dataset = load_dataset("scthornton/securecode-v2")

# Access splits
train_data = dataset["train"]
val_data = dataset["validation"]
test_data = dataset["test"]

# Inspect an example
print(train_data[0]["messages"])
```

### Fine-Tuning Example

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

model_name = "meta-llama/Llama-3.2-3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Prepare dataset for training
def format_conversation(example):
    formatted = tokenizer.apply_chat_template(
        example["messages"],
        tokenize=False
    )
    return {"text": formatted}

train_dataset = dataset["train"].map(format_conversation)

# Configure training
training_args = TrainingArguments(
    output_dir="./securecode-finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-5,
    logging_steps=100,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

trainer.train()
```

---

## 📖 Citation

If you use SecureCode v2.0 in your research, please cite:

```bibtex
@misc{thornton2025securecode,
  title={SecureCode v2.0: A Production-Grade Dataset for Training Security-Aware Code Generation Models},
  author={Thornton, Scott},
  year={2025},
  month={December},
  publisher={perfecXion.ai},
  url={https://perfecxion.ai/articles/securecode-v2-dataset-paper.html},
  note={Dataset: https://huggingface.co/datasets/scthornton/securecode-v2}
}
```

---

## 📄 License

This dataset is released under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**.

**What this means:**
- ✅ **Free for Research & Education** - Use freely in academic research, publications, and teaching
- ✅ **Derivative Works Allowed** - You can modify, extend, and improve the dataset
- ✅ **Share-Alike** - Derivatives must use the same CC BY-NC-SA 4.0 license
- ✅ **Attribution Required** - Credit the original work when used
- ❌ **No Commercial Use** - Cannot be used in commercial products or services without permission

For commercial licensing inquiries, contact: scott@perfecxion.ai

---

## 🔗 Links

- **📄 Research Paper**: [https://perfecxion.ai/articles/securecode-v2-dataset-paper.html](https://perfecxion.ai/articles/securecode-v2-dataset-paper.html)
- **💻 GitHub Repository**: [https://github.com/scthornton/securecode-v2](https://github.com/scthornton/securecode-v2)
- **🤗 HuggingFace Dataset**: [https://huggingface.co/datasets/scthornton/securecode-v2](https://huggingface.co/datasets/scthornton/securecode-v2)
- **🛠️ Validation Framework**: [validate_contributing_compliance.py](https://github.com/scthornton/securecode-v2/blob/main/validate_contributing_compliance.py)

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding new vulnerability examples
- Improving existing content
- Validation and quality assurance
- Documentation improvements

---

## 🙏 Acknowledgments

- Security research community for responsible disclosure practices
- Three anonymous security experts who provided independent validation
- OWASP Foundation for maintaining the Top 10 taxonomy
- MITRE Corporation for the CVE database

---

## 📊 Quality Metrics

| Metric | Result |
|--------|--------|
| CVE Format Compliance | 100% (1,215/1,215) |
| Language Tag Validity | 100% (1,215/1,215) |
| Content Quality Standards | 100% (1,215/1,215) |
| 4-Turn Structure Compliance | 100% (1,215/1,215) |
| Incident Grounding | 100% (all examples tied to real incidents) |
| Expert Security Review | Complete (3 independent validators) |
| Content Deduplication | 1,203 duplicates removed |

