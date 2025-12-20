# arXiv Submission Text

## Abstract Field (1898/1920 characters - 22 chars remaining)

AI assistants produce vulnerable code in 45% of security-relevant scenarios, introducing flaws into production systems at scale. Yet existing secure coding datasets fall short. They lack incident grounding, don't provide the scale modern training requires, and miss the operational security context developers need for production deployments.

We present SecureCode v2.0, a production-grade dataset of 1,215 security-focused coding examples that passed structural validation and expert security review. Every example ties to actual documented security incidents with CVE references, provides vulnerable and secure implementations, demonstrates concrete attacks, and includes defense-in-depth operational guidance. The dataset covers 11 vulnerability categories (complete OWASP Top 10:2025 plus AI/ML Security Threats) across 11 languages (Python, JavaScript, Java, Go, PHP, C#, TypeScript, Ruby, Rust, Kotlin, and YAML for infrastructure-as-code).

Our quality assurance framework ensures complete incident grounding. Each example includes SIEM integration strategies, infrastructure hardening recommendations (Docker, AppArmor, WAF configurations), and testing approaches using language-appropriate frameworks. The dataset uses a 4-turn conversational structure mirroring actual developer-AI interactions, escalating from basic implementations to advanced security considerations and defense-in-depth guidance.

Our contributions: (1) 1,215 rigorously validated examples split into 989 training, 122 validation, and 104 test sets, (2) an automated validation framework ensuring dataset consistency, (3) a 4-turn conversational structure capturing realistic security workflows, (4) comprehensive operational security guidance with SIEM integration strategies, (5) complete language-specific implementation fidelity, and (6) open-source release of data, validation tools, and benchmarking protocols.

---

## Comments Field

37 pages, 5 figures. Dataset available at https://huggingface.co/datasets/scthornton/securecode-v2 . Code and validation tools at https://github.com/scthornton/securecode-v2 . Published version at https://perfecxion.ai/articles/securecode-v2-dataset-paper.html

---

## Submission Metadata

**Title:** SecureCode v2.0: A Production-Grade Dataset for Training Security-Aware Code Generation Models

**Author:** Scott Thornton (perfecXion.ai)

**Primary Category:** cs.CR (Cryptography and Security)

**Secondary Categories:** cs.SE (Software Engineering), cs.LG (Machine Learning)

**License:** CC BY-NC-SA 4.0

---

## Changes from LaTeX Abstract

To fit the 1920 character limit, the following edits were made:

1. Removed redundant "Every example" from second paragraph
2. Shortened "defense-in-depth operational guidance" to "defense-in-depth guidance" in paragraph 3
3. Made first paragraph more concise by combining clauses

**Original:** 1930 characters
**Optimized:** 1898 characters ✓
**Saved:** 32 characters
**Remaining buffer:** 22 characters

---

## Endorsement Information

You will need endorsement for the cs.CR category.

**Your endorsement code:** YF9OXP

Forward the endorsement email to:
- Your thesis advisor (if applicable)
- A colleague who has published 3+ papers in cs.* categories in the last 5 years
- A researcher in AI security whose work relates to your paper

---

## Next Steps

1. Go to https://arxiv.org/submit
2. Log in with your arXiv account
3. Click "Start New Submission"
4. **Metadata Section:**
   - Title: (copy from above)
   - Authors: Scott Thornton
   - Abstract: (copy from Abstract Field above)
   - Comments: (copy from Comments Field above)
   - Primary category: cs.CR
   - Secondary categories: cs.SE, cs.LG

5. **Upload Files:**
   - Upload `securecode-v2-arxiv-package.zip` (or `.tar.gz`)
   - arXiv will automatically extract and compile

6. **Process and Preview:**
   - Click "Process Files"
   - Wait for compilation
   - Download and review PDF preview
   - Verify all 5 figures appear correctly

7. **Submit:**
   - If preview looks good, click "Submit"
   - Wait for endorsement approval (code: YF9OXP)
   - Paper will go live after moderation

---

## Important Notes

- **No LaTeX formatting in abstract:** The abstract above has all `\textbf{}` and `\#` removed
- **Comments field is not cumulative:** If you replace the paper, you must resubmit all comments
- **URL spacing:** Ensure spaces after URLs to prevent parsing issues
- **Page count:** 37 pages verified from compiled PDF
- **Figures:** All 5 figures included in upload package
