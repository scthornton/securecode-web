# SecureCode v2.0 Validator - Version 2

## Overview

`validate_contributing_compliance_v2.py` is a comprehensive dataset quality assurance tool that ensures SecureCode v2.0 examples meet all contribution standards. This validator combines structural validation, metadata verification, and content quality checks with detailed error reporting.

## Key Improvements Over v1

### 1. **CVE Format Validator - Bug Fixed** ✓
- **Old bug**: Limited CVE numbers to 5 digits (`\d{1,5}`)
- **Fixed**: Accepts 4+ digits with no maximum (`\d{4,}`)
- **Why**: Modern CVEs use 7+ digit sequences (e.g., CVE-2024-1000000)

### 2. **Honest Naming** ✓
- Renamed `validate_content_quality` → `validate_content_length`
- Only checks character counts, NOT semantic quality
- Thresholds: ≥50 chars (user turns), ≥100 chars (assistant turns)

### 3. **Enhanced Validation** ✓
- Turn 2 section detection (vulnerable/attack/secure code)
- Turn 4 operational guidance (logging/monitoring keywords)
- Example ID presence checking
- All enhanced checks issue warnings, not failures

### 4. **Flexible Metadata Support** ✓
- Accepts both old (root-level) and new (nested) formats
- Handles multiple field name variations (lang/language, cve/cve_id)
- Extracts year from created date if incident_year missing

### 5. **Structured Results** ✓
- Dataclass-based architecture for JSON serialization
- Per-check results with detailed error messages
- Programmatic result analysis for CI/CD integration

## Installation

No dependencies required beyond Python 3.7+ standard library.

```bash
# Make executable
chmod +x validate_contributing_compliance_v2.py

# Run directly
./validate_contributing_compliance_v2.py consolidated/train.jsonl
```

## Usage

### Basic Validation

```bash
python validate_contributing_compliance_v2.py consolidated/train.jsonl
```

Output:
```
================================================================================
VALIDATION COMPLETE
================================================================================

Total Examples: 1934
Passed: 1912 (98.9%)
Failed: 4
Warnings: 18

✓ VALIDATION PASSED - All examples comply with standards
```

### Strict Mode

Treat warnings as failures (useful for pre-publication checks):

```bash
python validate_contributing_compliance_v2.py consolidated/train.jsonl --strict
```

### Generate JSON Report

```bash
python validate_contributing_compliance_v2.py consolidated/train.jsonl --report validation_report.json
```

Report structure:
```json
{
  "summary": {
    "total_examples": 1934,
    "passed": 1912,
    "failed": 4,
    "warnings": 18,
    "failures_by_check": {
      "cve_format": 4
    },
    "warnings_by_check": {
      "turn4_operational": 18
    }
  },
  "failed_or_warned_examples": [
    {
      "example_id": "authentication-000001",
      "index": 263,
      "overall_result": "FAIL",
      "checks": [
        {
          "check_name": "cve_format",
          "result": "FAIL",
          "message": "Invalid CVE format: '' (expected CVE-YYYY-NNNN with 4+ digits)",
          "details": {"cve_id": "", "pattern": "CVE-YYYY-NNNN (4+ digits)"}
        }
      ]
    }
  ]
}
```

### Quiet Mode

Suppress progress output (only show summary):

```bash
python validate_contributing_compliance_v2.py consolidated/train.jsonl --quiet
```

### Disable Enhanced Validators

Run only core compliance checks:

```bash
python validate_contributing_compliance_v2.py consolidated/train.jsonl --no-enhanced
```

### Custom Failure Display Limit

```bash
python validate_contributing_compliance_v2.py consolidated/train.jsonl --max-failures 20
```

## Validation Checks

### Core Validators (Required)

| Check | Description | Failure Condition |
|-------|-------------|-------------------|
| **structure** | 4-turn conversation format | Missing messages, wrong role order, missing fields |
| **cve_format** | CVE-YYYY-NNNN+ (4+ digits) | Invalid format, wrong type, out-of-range year |
| **metadata** | Required fields present/valid | Missing fields, invalid OWASP category/severity |
| **language** | Supported programming language | Unsupported language tag |
| **content_length** | Minimum character counts | User turns <50 chars, assistant turns <100 chars |
| **incident_grounding** | Real-world incident when no CVE | Missing grounding when cve_id is null |

### Enhanced Validators (Nice-to-Have)

| Check | Description | Result |
|-------|-------------|--------|
| **turn2_sections** | Expected sections in Turn 2 | WARN if <2 sections found |
| **turn4_operational** | Operational security keywords | WARN if <2 keywords found |
| **example_id** | Unique identifier present | WARN if missing |

## Validation Details

### CVE Format Rules

**Accepted:**
- `null` - Explicit null for incidents without CVE assignments
- `CVE-1999-1000` - Minimum: year 1999, 4-digit sequence
- `CVE-2024-1234` - Standard format
- `CVE-2024-1000000` - High-volume 7-digit sequences
- `CVE-2026-5678` - Next year allowed for upcoming assignments

**Rejected:**
- `""` - Empty string (use `null` instead)
- `CVE-2024-123` - Only 3 digits (minimum 4 required)
- `CVE-1998-1234` - Year before 1999 (CVE program start)
- `CVE-2030-1234` - Future year beyond next year
- `cve-2024-1234` - Lowercase (must be uppercase)

### Metadata Flexibility

The validator accepts metadata in multiple formats:

**Format 1: Root-level fields**
```json
{
  "cve_id": "CVE-2024-1234",
  "severity": "HIGH",
  "language": "python",
  "owasp_category": "A03:2021-Injection",
  "incident_year": 2024,
  "business_impact": "Data breach..."
}
```

**Format 2: Nested metadata/context**
```json
{
  "metadata": {
    "severity": "HIGH",
    "lang": "python",
    "owasp_2021": "A03:2021-Injection",
    "created": "2024-01-15"
  },
  "context": {
    "cve": "CVE-2024-1234",
    "year": 2024,
    "business_impact": "Data breach..."
  }
}
```

### OWASP Categories

Valid categories (OWASP 2021 Top 10):
- `A01:2021-Broken Access Control`
- `A02:2021-Cryptographic Failures`
- `A03:2021-Injection`
- `A04:2021-Insecure Design`
- `A05:2021-Security Misconfiguration`
- `A06:2021-Vulnerable and Outdated Components`
- `A07:2021-Identification and Authentication Failures`
- `A08:2021-Software and Data Integrity Failures`
- `A09:2021-Security Logging and Monitoring Failures`
- `A10:2021-Server-Side Request Forgery (SSRF)` or `A10:2021-Server-Side Request Forgery`
- `AI/ML Security Threats` (custom category)
- `Unknown` (edge cases)

### Severity Levels

- `CRITICAL` - Critical vulnerabilities (RCE, authentication bypass)
- `HIGH` - High-impact vulnerabilities (SQL injection, XSS)
- `MEDIUM` - Medium-impact issues (information disclosure)
- `LOW` - Low-impact issues (missing security headers)

### Supported Languages

`python`, `javascript`, `java`, `php`, `csharp`, `c#`, `ruby`, `go`, `typescript`, `rust`, `kotlin`, `yaml`, `c`, `c++`, `cpp`, `swift`, `bash`, `shell`, `sql`

## Exit Codes

- `0` - All validations passed (or only warnings in non-strict mode)
- `1` - One or more failures (or warnings in strict mode)

Use in CI/CD:
```bash
python validate_contributing_compliance_v2.py dataset.jsonl || exit 1
```

## Current Dataset Compliance

As of 2025-12-15:

**Training Set (train.jsonl):**
- Total: 1,934 examples
- Passed: 1,912 (98.9%)
- Failed: 4 (CVE format - empty strings)
- Warnings: 18 (operational guidance)

**Test Set (test.jsonl):**
- Total: 241 examples
- Passed: 238 (98.8%)
- Failed: 0
- Warnings: 3 (operational guidance)

**Validation Set (val.jsonl):**
- Total: 243 examples
- Passed: 240 (98.8%)
- Failed: 0
- Warnings: 3 (operational guidance)

### Known Issues

**Training Set Failures (4 examples):**
- Examples #263, #965, #1102, #1921
- Issue: Empty string `""` for CVE ID instead of `null`
- Fix: Replace `"cve": ""` with `"cve": null`

**Warnings (24 examples total):**
- Minimal operational security keywords in Turn 4
- Recommendation: Add logging/monitoring/detection guidance

## Architecture

### Dataclass-Based Results

```python
@dataclass
class ValidationReport:
    check_name: str
    result: ValidationResult  # PASS/FAIL/WARN/SKIP
    message: str
    details: Optional[Dict[str, Any]] = None

@dataclass
class ExampleValidationResult:
    example_id: str
    index: int
    overall_result: ValidationResult
    checks: List[ValidationReport]
```

### Validator Functions

Each validator returns a `ValidationReport`:

```python
def validate_cve_format(cve_id: Any) -> ValidationReport:
    """Validates CVE format with detailed error reporting"""
    if cve_id is None:
        return ValidationReport(
            check_name='cve_format',
            result=ValidationResult.PASS,
            message="Explicit null accepted (no CVE assigned)"
        )

    pattern = r'^CVE-(\d{4})-(\d{4,})$'  # 4+ digits, no max
    # ... validation logic ...
```

## Extending the Validator

### Adding a New Validator

1. Create validator function returning `ValidationReport`:

```python
def validate_example_complexity(example: Dict[str, Any]) -> ValidationReport:
    """Check if example meets complexity requirements"""
    complexity = example.get('metadata', {}).get('complexity')

    if complexity not in {'basic', 'moderate', 'advanced'}:
        return ValidationReport(
            check_name='complexity',
            result=ValidationResult.WARN,
            message=f"Unexpected complexity: {complexity}"
        )

    return ValidationReport(
        check_name='complexity',
        result=ValidationResult.PASS,
        message=f"Valid complexity: {complexity}"
    )
```

2. Add to `validate_example()`:

```python
def validate_example(example, index, enable_enhanced=True):
    checks = []

    # Core validators
    checks.append(validate_structure(example))
    # ... existing validators ...

    # Your new validator
    checks.append(validate_example_complexity(example))
```

## Testing

### Unit Tests

Run CVE validation tests:
```bash
python test_cve_validation.py
```

### Full Dataset Validation

```bash
# Validate all splits
python validate_contributing_compliance_v2.py consolidated/train.jsonl
python validate_contributing_compliance_v2.py consolidated/test.jsonl
python validate_contributing_compliance_v2.py consolidated/val.jsonl

# Or use a loop
for split in train test val; do
    echo "Validating $split..."
    python validate_contributing_compliance_v2.py consolidated/${split}.jsonl --quiet
done
```

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Dataset Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Validate dataset
        run: |
          python validate_contributing_compliance_v2.py consolidated/train.jsonl --strict
          python validate_contributing_compliance_v2.py consolidated/test.jsonl --strict
          python validate_contributing_compliance_v2.py consolidated/val.jsonl --strict

      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: validation-report
          path: '*_validation_report.json'
```

## Troubleshooting

### Common Issues

**Issue: "Missing messages/conversations field"**
- Solution: Ensure your example has either `messages` or `conversations` array

**Issue: "Invalid CVE format: '' (expected CVE-YYYY-NNNN with 4+ digits)"**
- Solution: Replace empty string `""` with `null` for missing CVEs

**Issue: "Invalid OWASP category: 'A10:2021-Server-Side Request Forgery'"**
- Solution: This should pass in v2. Ensure you're using the updated validator.

**Issue: "Missing incident_year"**
- Solution: Add `year` field to context, or ensure `metadata.created` exists

**Issue: "Unsupported language: 'js'"**
- Solution: Use `javascript` instead of `js`

### Debug Mode

For detailed debugging, modify the validator to print intermediate values:

```python
# Add at start of validate_example()
import json
print(f"Validating example {index}:")
print(json.dumps(example, indent=2)[:500])
```

## FAQ

**Q: Why are warnings not treated as failures by default?**
- A: Warnings indicate nice-to-have improvements, not compliance violations. Use `--strict` if you want to enforce warnings.

**Q: Can I disable specific validators?**
- A: Currently, you can disable all enhanced validators with `--no-enhanced`. For fine-grained control, modify the `validate_example()` function.

**Q: How do I fix the 4 CVE format failures in train.jsonl?**
- A: Find examples with `"cve": ""` and change to `"cve": null`. Example:
  ```bash
  # Find problematic examples
  grep -n '"cve": ""' consolidated/train.jsonl

  # Fix with sed (backup first!)
  sed -i.bak 's/"cve": ""/"cve": null/g' consolidated/train.jsonl
  ```

**Q: What's the difference between v1 and v2 validators?**
- A: v2 fixes CVE validator bug (4+ digits), renames content_quality→content_length, adds enhanced validators, supports flexible metadata formats, and uses structured results.

**Q: Can I use this validator for my own dataset?**
- A: Yes! Modify the constants at the top of the file (SUPPORTED_LANGUAGES, VALID_OWASP_CATEGORIES, etc.) to match your requirements.

## Contributing

To contribute improvements to the validator:

1. Add tests to `test_cve_validation.py`
2. Implement validator function following existing patterns
3. Update this README with new features
4. Submit PR with validation results on all three splits

## License

Apache 2.0 - See LICENSE file for details

## Contact

Scott Thornton (scott@perfecxion.ai)

## Version History

**v2.0** (2025-12-15)
- Fixed CVE validator bug (4+ digits, no maximum)
- Renamed content_quality → content_length
- Added enhanced validators (turn2_sections, turn4_operational, example_id)
- Flexible metadata format support
- Structured results with dataclasses
- Comprehensive CLI with --strict, --report, --quiet options

**v1.0** (initial release)
- Basic structure, metadata, CVE validation
- Simple pass/fail reporting
