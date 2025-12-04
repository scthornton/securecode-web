# SecureCode v2.0 Dataset Review & Assessment Prompt

## Task Overview
Conduct a comprehensive quality review and assessment of the SecureCode v2.0 secure coding training dataset located at `/Users/scott/perfecxion/datasets/securecode/v2/`.

## Dataset Context
- **Total Examples**: 1,209 secure coding examples
- **Purpose**: Training LLMs on secure coding, vulnerability detection, and security best practices
- **Coverage**: OWASP Top 10 2021 + AI/ML Security across 11 programming languages

## Review Objectives

### 1. Data Quality Assessment (Priority: HIGH)
Randomly sample **50-75 examples** from `consolidated/train.jsonl` and evaluate:

- **Structural Validity**: All 4 conversations present and properly formatted?
- **Code Quality**: Are code examples syntactically correct and realistic?
- **Security Accuracy**: Do vulnerability explanations match real-world security issues?
- **Real-World Context**: Are CVE references, incident details, and impacts accurate and relevant?
- **Completeness**: Does each example include vulnerable code, secure fix, advanced attack, and defense-in-depth?
- **Production Readiness**: Do examples include logging, error handling, and monitoring patterns?

**Deliverable**: Quality score (% perfect examples) with breakdown by issue type

### 2. Coverage Analysis (Priority: HIGH)
Analyze `consolidated/metadata.json` and verify:

- **OWASP Coverage**: Are all Top 10 2021 categories well-represented (10-15% each)?
- **Language Distribution**: Is representation balanced across 11 languages?
- **Severity Distribution**: Appropriate mix of CRITICAL/HIGH/MEDIUM severity examples?
- **Technique Diversity**: Are there 200+ unique attack/defense patterns?
- **Real-World Incidents**: 95%+ of examples document actual breaches/CVEs?

**Deliverable**: Coverage report identifying any gaps or imbalances

### 3. Technical Validation (Priority: MEDIUM)
Select **10 examples** spanning different languages and validate:

- **Code Syntax**: Run language-specific syntax checkers (Python: ast, JavaScript: esprima, etc.)
- **Security Patterns**: Verify vulnerability and fix patterns are technically sound
- **CVE Accuracy**: Spot-check 5-10 CVE references against NVD database
- **Incident Details**: Verify 3-5 breach descriptions against public reports

**Deliverable**: Technical validation report with error count and severity

### 4. Consistency Check (Priority: MEDIUM)
Verify consistency across the dataset:

- **Naming Conventions**: Are example IDs, categories, subcategories standardized?
- **Format Adherence**: Do all examples follow the 4-turn conversation structure?
- **Metadata Completeness**: Are `lang`, `category`, `severity`, `owasp_2021`, `cwe` fields present?
- **Encoding**: No UTF-8 encoding issues or corrupted characters?

**Deliverable**: Consistency report with any deviations documented

### 5. Comparison with Design Spec (Priority: LOW)
Compare actual dataset against design specification in `DATASET_DESIGN.md`:

- Does the dataset meet the original 1,000 example target?
- Are the specified OWASP categories fully covered?
- Does language distribution match the design goals?
- Are multi-turn conversations (2-8 turns) predominant?

**Deliverable**: Design compliance report

## Access Points

**Primary Data Files:**
- `consolidated/train.jsonl` (841 examples, 70%)
- `consolidated/val.jsonl` (175 examples, 15%)
- `consolidated/test.jsonl` (193 examples, 15%)
- `consolidated/metadata.json` (dataset statistics)

**Documentation:**
- `README.md` - Dataset overview and usage
- `PROJECT_DESCRIPTION.md` - Project summary and accomplishments
- `DATASET_DESIGN.md` - Original design specification
- `FULL_DATASET_PLAN.md` - Complete generation plan

**Source Data:**
- `data/*_batch_*.jsonl` - Individual batch files (129 batches)
- `archive/old_reports/` - Historical status reports

## Expected Output

Provide a comprehensive assessment report covering:

1. **Executive Summary**: 2-3 paragraphs summarizing overall quality and readiness
2. **Quality Metrics**:
   - Overall quality score (% perfect examples)
   - Error breakdown by category
   - Critical issues requiring immediate attention
3. **Coverage Analysis**:
   - OWASP category distribution with gaps
   - Language representation analysis
   - Technique diversity assessment
4. **Technical Findings**:
   - Syntax validation results
   - Security accuracy assessment
   - CVE/incident verification summary
5. **Recommendations**:
   - High-priority fixes (if any)
   - Suggested improvements
   - Publication readiness assessment

## Success Criteria

The dataset is **publication-ready** if:
- ✅ 80%+ of sampled examples are perfect (no structural, technical, or content issues)
- ✅ All OWASP Top 10 2021 categories have 8%+ representation
- ✅ No critical syntax errors or security inaccuracies
- ✅ 95%+ real-world incident coverage maintained
- ✅ Consistent formatting and metadata across all examples

## Timeline
Target completion: 2-3 hours for comprehensive review

---

**Note**: This is a production dataset intended for LLM training and publication. Rigor and thoroughness are essential.
2
