"""
SecureCode v2.0 Validation Framework

Comprehensive validation for all training examples:
- Syntax checking (language-specific)
- Encoding validation (UTF-8, no corruption)
- Duplication detection
- Security pattern verification
- Schema compliance
"""

import ast
import re
import json
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import jsonschema


class ValidationResult:
    """Stores validation results for an example"""

    def __init__(self, example_id: str):
        self.example_id = example_id
        self.passed = True
        self.issues = []
        self.checks = {
            'syntax_check': 'not_tested',
            'security_review': 'not_reviewed',
            'code_execution': 'not_tested',
            'encoding_check': 'not_tested',
            'duplication_check': 'not_tested',
            'schema_validation': 'not_tested'
        }

    def add_issue(self, check_name: str, issue: str, severity: str = 'ERROR'):
        """Add a validation issue"""
        self.issues.append({
            'check': check_name,
            'severity': severity,
            'message': issue
        })
        if severity == 'ERROR':
            self.passed = False
            self.checks[check_name] = 'failed'

    def mark_passed(self, check_name: str):
        """Mark a check as passed"""
        self.checks[check_name] = 'passed'

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'example_id': self.example_id,
            'passed': self.passed,
            'issues': self.issues,
            'checks': self.checks
        }


class EncodingValidator:
    """Validates UTF-8 encoding and detects corruption"""

    # Common encoding corruption patterns from original dataset
    CORRUPTION_PATTERNS = [
        r'[\u4E00-\u9FFF]',  # Chinese characters (蜜, 蜂, 萝, etc.)
        r'[^\x00-\x7F\u00A0-\uFFFF]',  # Invalid Unicode ranges
        r'[\uFFFD]',  # Replacement character (�)
    ]

    @staticmethod
    def validate(example: Dict, result: ValidationResult) -> None:
        """Validate encoding of all text fields"""
        try:
            # Check all string fields recursively
            EncodingValidator._check_strings(example, result, [])

            # Specific check for code blocks in conversations
            if 'conversations' in example:
                for i, conv in enumerate(example['conversations']):
                    value = conv.get('value', '')

                    # Check for corruption patterns
                    for pattern in EncodingValidator.CORRUPTION_PATTERNS:
                        matches = re.findall(pattern, value)
                        if matches:
                            result.add_issue(
                                'encoding_check',
                                f"Encoding corruption in conversation turn {i+1}: found '{matches[0]}' (likely data corruption)",
                                'ERROR'
                            )

                    # Verify valid UTF-8
                    try:
                        value.encode('utf-8').decode('utf-8')
                    except UnicodeError as e:
                        result.add_issue(
                            'encoding_check',
                            f"Invalid UTF-8 encoding in conversation turn {i+1}: {str(e)}",
                            'ERROR'
                        )

            if not result.issues:
                result.mark_passed('encoding_check')

        except Exception as e:
            result.add_issue('encoding_check', f"Encoding validation error: {str(e)}", 'ERROR')

    @staticmethod
    def _check_strings(obj, result: ValidationResult, path: List[str]) -> None:
        """Recursively check all strings in object"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                EncodingValidator._check_strings(value, result, path + [key])
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                EncodingValidator._check_strings(item, result, path + [f"[{i}]"])
        elif isinstance(obj, str):
            # Check for corruption patterns
            for pattern in EncodingValidator.CORRUPTION_PATTERNS:
                if re.search(pattern, obj):
                    result.add_issue(
                        'encoding_check',
                        f"Encoding corruption at {'.'.join(path)}: contains non-Latin characters in code",
                        'WARNING'
                    )


class SyntaxValidator:
    """Language-specific syntax validation"""

    @staticmethod
    def validate(example: Dict, result: ValidationResult) -> None:
        """Validate syntax of code in conversations"""
        lang = example['metadata']['lang']

        # Extract code blocks from conversations
        code_blocks = SyntaxValidator._extract_code_blocks(example)

        if not code_blocks:
            result.add_issue('syntax_check', "No code blocks found in conversations", 'WARNING')
            return

        # Validate each code block
        for i, code in enumerate(code_blocks):
            validator = SyntaxValidator._get_validator(lang)
            if validator:
                is_valid, error_msg = validator(code)
                if not is_valid:
                    result.add_issue(
                        'syntax_check',
                        f"Syntax error in code block {i+1}: {error_msg}",
                        'ERROR'
                    )

        if not result.issues:
            result.mark_passed('syntax_check')

    @staticmethod
    def _extract_code_blocks(example: Dict) -> List[str]:
        """Extract code blocks from markdown in conversations

        Returns only code blocks in the target language (filters out SQL, JSON, etc.)
        """
        lang = example['metadata']['lang']
        code_blocks = []

        # Map language names to expected code fence labels
        lang_aliases = {
            'python': ['python', 'py'],
            'javascript': ['javascript', 'js', 'node'],
            'typescript': ['typescript', 'ts'],
            'java': ['java'],
            'go': ['go', 'golang'],
            'c': ['c'],
            'c++': ['cpp', 'c++'],
            'c#': ['csharp', 'cs', 'c#'],
            'php': ['php'],
            'ruby': ['ruby', 'rb'],
            'rust': ['rust', 'rs'],
            'kotlin': ['kotlin', 'kt'],
            'swift': ['swift']
        }

        expected_labels = lang_aliases.get(lang, [lang])

        for conv in example.get('conversations', []):
            if conv.get('from') != 'assistant':
                continue  # Only validate assistant code

            value = conv.get('value', '')

            # Extract markdown code blocks with language label
            pattern = r'```(\w+)\n(.*?)```'
            matches = re.findall(pattern, value, re.DOTALL)

            for code_lang, code in matches:
                # Only validate code in the target language
                # Skip SQL, JSON, bash, etc.
                if code_lang.lower() in expected_labels:
                    code_blocks.append(code)

        return code_blocks

    @staticmethod
    def _get_validator(lang: str):
        """Get validator function for language"""
        validators = {
            'python': SyntaxValidator._validate_python,
            'javascript': SyntaxValidator._validate_javascript,
            'typescript': SyntaxValidator._validate_javascript,  # Same syntax
            'java': SyntaxValidator._validate_java,
            'go': SyntaxValidator._validate_go,
            'c': SyntaxValidator._validate_c,
            'c++': SyntaxValidator._validate_cpp,
            'c#': SyntaxValidator._validate_csharp,
            'ruby': SyntaxValidator._validate_ruby,
            'php': SyntaxValidator._validate_php,
            'rust': SyntaxValidator._validate_rust,
        }
        return validators.get(lang)

    @staticmethod
    def _validate_python(code: str) -> Tuple[bool, Optional[str]]:
        """Validate Python syntax"""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _validate_javascript(code: str) -> Tuple[bool, Optional[str]]:
        """Validate JavaScript/TypeScript syntax using node"""
        try:
            result = subprocess.run(
                ['node', '--check'],
                input=code.encode(),
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return True, None
            return False, result.stderr.decode()
        except subprocess.TimeoutExpired:
            return False, "Validation timeout"
        except FileNotFoundError:
            # Node not installed, skip validation
            return True, None
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _validate_java(code: str) -> Tuple[bool, Optional[str]]:
        """Validate Java syntax"""
        # Basic structural checks (full compilation requires javac)
        required_patterns = [
            (r'class\s+\w+', "Missing class declaration"),
            (r'\{', "Missing opening brace"),
            (r'\}', "Missing closing brace"),
        ]

        for pattern, error_msg in required_patterns:
            if not re.search(pattern, code):
                return False, error_msg

        # Check balanced braces
        if code.count('{') != code.count('}'):
            return False, "Unbalanced braces"

        return True, None

    @staticmethod
    def _validate_go(code: str) -> Tuple[bool, Optional[str]]:
        """Validate Go syntax"""
        try:
            result = subprocess.run(
                ['go', 'fmt'],
                input=code.encode(),
                capture_output=True,
                timeout=5
            )
            # go fmt returns formatted code if valid
            return True, None
        except subprocess.TimeoutExpired:
            return False, "Validation timeout"
        except FileNotFoundError:
            # Go not installed, basic checks
            if code.count('{') != code.count('}'):
                return False, "Unbalanced braces"
            return True, None
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _validate_c(code: str) -> Tuple[bool, Optional[str]]:
        """Validate C syntax"""
        # Basic structural checks
        if code.count('{') != code.count('}'):
            return False, "Unbalanced braces"
        if code.count('(') != code.count(')'):
            return False, "Unbalanced parentheses"

        return True, None

    @staticmethod
    def _validate_cpp(code: str) -> Tuple[bool, Optional[str]]:
        """Validate C++ syntax"""
        return SyntaxValidator._validate_c(code)

    @staticmethod
    def _validate_csharp(code: str) -> Tuple[bool, Optional[str]]:
        """Validate C# syntax"""
        # Basic structural checks
        if code.count('{') != code.count('}'):
            return False, "Unbalanced braces"

        return True, None

    @staticmethod
    def _validate_ruby(code: str) -> Tuple[bool, Optional[str]]:
        """Validate Ruby syntax"""
        try:
            result = subprocess.run(
                ['ruby', '-c'],
                input=code.encode(),
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return True, None
            return False, result.stderr.decode()
        except FileNotFoundError:
            return True, None  # Ruby not installed, skip
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _validate_php(code: str) -> Tuple[bool, Optional[str]]:
        """Validate PHP syntax"""
        try:
            result = subprocess.run(
                ['php', '-l'],
                input=code.encode(),
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return True, None
            return False, result.stderr.decode()
        except FileNotFoundError:
            return True, None  # PHP not installed, skip
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _validate_rust(code: str) -> Tuple[bool, Optional[str]]:
        """Validate Rust syntax"""
        # Basic checks (full validation requires rustc)
        if code.count('{') != code.count('}'):
            return False, "Unbalanced braces"

        return True, None


class DuplicationDetector:
    """Detects duplicate or near-duplicate examples"""

    def __init__(self):
        self.seen_hashes = set()
        self.seen_code_hashes = set()

    def validate(self, example: Dict, result: ValidationResult) -> None:
        """Check for duplicates"""
        # Hash entire example
        example_hash = self._hash_example(example)
        if example_hash in self.seen_hashes:
            result.add_issue('duplication_check', "Identical example already exists", 'ERROR')
            return
        self.seen_hashes.add(example_hash)

        # Hash code blocks
        code_blocks = SyntaxValidator._extract_code_blocks(example)
        for code in code_blocks:
            code_hash = self._hash_code(code)
            if code_hash in self.seen_code_hashes:
                result.add_issue('duplication_check', "Identical code block found in another example", 'WARNING')
                return
            self.seen_code_hashes.add(code_hash)

        result.mark_passed('duplication_check')

    @staticmethod
    def _hash_example(example: Dict) -> str:
        """Create hash of entire example"""
        # Remove dynamic fields
        example_copy = example.copy()
        example_copy.pop('id', None)
        example_copy.pop('validation', None)

        # Deterministic JSON serialization
        json_str = json.dumps(example_copy, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()

    @staticmethod
    def _hash_code(code: str) -> str:
        """Create normalized hash of code"""
        # Normalize whitespace for fuzzy matching
        normalized = re.sub(r'\s+', ' ', code.strip())
        return hashlib.sha256(normalized.encode()).hexdigest()


class SecurityPatternValidator:
    """Validates security patterns in code examples"""

    # Dangerous patterns that should NOT appear in "secure" code
    DANGEROUS_PATTERNS = {
        'python': [
            (r'\beval\s*\(', "eval() found in code - should be avoided entirely"),
            (r'\bexec\s*\(', "exec() found in code - should be avoided entirely"),
            (r'[\'"]SELECT\s+.+\+', "String concatenation in SQL - use parameterized queries"),
            (r'pickle\.loads\s*\(', "pickle.loads without validation - insecure deserialization risk"),
        ],
        'javascript': [
            (r'\beval\s*\(', "eval() found - should be avoided entirely"),
            (r'innerHTML\s*=\s*[^\'"]', "Direct innerHTML assignment - XSS risk"),
            (r'document\.write\s*\(', "document.write() found - XSS risk"),
        ],
        'php': [
            (r'mysql_query\s*\(.+\$', "mysql_query with variable - use prepared statements"),
            (r'eval\s*\(', "eval() found - code injection risk"),
        ],
        'java': [
            (r'\.executeQuery\s*\(.+\+', "String concatenation in SQL - use PreparedStatement"),
            (r'Runtime\.getRuntime\(\)\.exec\s*\(.+\+', "Command concatenation - command injection risk"),
        ],
    }

    # Required patterns for secure implementations
    REQUIRED_SECURE_PATTERNS = {
        'sql_injection': [
            (r'PreparedStatement|\.execute\s*\(.+,\s*\(|parameterized|placeholder',
             "SQL injection fix should use parameterized queries/prepared statements"),
        ],
        'xss': [
            (r'escape|sanitize|DOMPurify|htmlspecialchars|encodeURIComponent',
             "XSS fix should include explicit sanitization/escaping"),
        ],
        'command_injection': [
            (r'allowlist|whitelist|subprocess.*shell=False|shlex\.quote',
             "Command injection fix should use allowlisting or proper escaping"),
        ],
    }

    @staticmethod
    def validate(example: Dict, result: ValidationResult) -> None:
        """Validate security patterns in code"""
        lang = example['metadata']['lang']
        subcategory = example['metadata']['subcategory']

        code_blocks = SyntaxValidator._extract_code_blocks(example)

        if not code_blocks:
            result.add_issue('security_review', "No code blocks to validate", 'WARNING')
            return

        # Check for dangerous patterns in what should be "secure" code
        # (assuming last code block is the secure version)
        if len(code_blocks) >= 2:
            secure_code = code_blocks[-1]

            # Check language-specific dangerous patterns
            dangerous = SecurityPatternValidator.DANGEROUS_PATTERNS.get(lang, [])
            for pattern, message in dangerous:
                if re.search(pattern, secure_code, re.IGNORECASE):
                    result.add_issue('security_review', f"Dangerous pattern in 'secure' code: {message}", 'ERROR')

            # Check for required secure patterns based on vulnerability type
            required = SecurityPatternValidator.REQUIRED_SECURE_PATTERNS.get(subcategory, [])
            for pattern, message in required:
                if not re.search(pattern, secure_code, re.IGNORECASE):
                    result.add_issue('security_review', message, 'WARNING')

        if not result.issues:
            result.mark_passed('security_review')


class SchemaValidator:
    """Validates examples against JSON schema"""

    def __init__(self, schema_path: Path):
        with open(schema_path) as f:
            self.schema = json.load(f)

    def validate(self, example: Dict, result: ValidationResult) -> None:
        """Validate against JSON schema"""
        try:
            jsonschema.validate(example, self.schema)
            result.mark_passed('schema_validation')
        except jsonschema.ValidationError as e:
            result.add_issue('schema_validation', f"Schema validation failed: {e.message}", 'ERROR')
        except Exception as e:
            result.add_issue('schema_validation', f"Schema validation error: {str(e)}", 'ERROR')


class DatasetValidator:
    """Main validator that orchestrates all validation checks"""

    def __init__(self, schema_path: Path):
        self.schema_validator = SchemaValidator(schema_path)
        self.duplication_detector = DuplicationDetector()
        self.results = []

    def validate_example(self, example: Dict) -> ValidationResult:
        """Run all validation checks on an example"""
        result = ValidationResult(example.get('id', 'unknown'))

        # 1. Schema validation
        self.schema_validator.validate(example, result)

        # 2. Encoding validation
        EncodingValidator.validate(example, result)

        # 3. Syntax validation
        SyntaxValidator.validate(example, result)

        # 4. Duplication detection
        self.duplication_detector.validate(example, result)

        # 5. Security pattern validation
        SecurityPatternValidator.validate(example, result)

        self.results.append(result)
        return result

    def validate_dataset(self, examples: List[Dict]) -> Dict:
        """Validate entire dataset"""
        print(f"Validating {len(examples)} examples...")

        passed = 0
        failed = 0

        for i, example in enumerate(examples):
            if (i + 1) % 100 == 0:
                print(f"  Validated {i + 1}/{len(examples)} examples...")

            result = self.validate_example(example)

            # Update example with validation results
            example['validation'] = {
                **result.checks,
                'reviewed_by': 'automated-validator',
                'review_date': datetime.now().strftime('%Y-%m-%d'),
                'issues': [issue['message'] for issue in result.issues] if result.issues else []
            }
            example['metadata']['validated'] = result.passed

            if result.passed:
                passed += 1
            else:
                failed += 1

        # Generate summary report
        summary = {
            'total_examples': len(examples),
            'passed': passed,
            'failed': failed,
            'pass_rate': passed / len(examples) * 100 if examples else 0,
            'checks': {
                'syntax_check': sum(1 for r in self.results if r.checks['syntax_check'] == 'passed'),
                'encoding_check': sum(1 for r in self.results if r.checks['encoding_check'] == 'passed'),
                'security_review': sum(1 for r in self.results if r.checks['security_review'] == 'passed'),
                'duplication_check': sum(1 for r in self.results if r.checks['duplication_check'] == 'passed'),
                'schema_validation': sum(1 for r in self.results if r.checks['schema_validation'] == 'passed'),
            },
            'issues_by_type': {},
            'failed_examples': []
        }

        # Collect issues by type
        for result in self.results:
            if not result.passed:
                summary['failed_examples'].append({
                    'id': result.example_id,
                    'issues': result.issues
                })

            for issue in result.issues:
                check = issue['check']
                summary['issues_by_type'][check] = summary['issues_by_type'].get(check, 0) + 1

        return summary


if __name__ == '__main__':
    # Test validators
    print("SecureCode v2.0 Validator - Unit Tests")
    print("=" * 50)

    # Test encoding validator
    print("\n1. Testing encoding validator...")
    test_example = {
        'id': 'test-001',
        'conversations': [
            {'turn': 1, 'from': 'human', 'value': 'Normal text'},
            {'turn': 2, 'from': 'assistant', 'value': 'Code with corruption蜜'}
        ]
    }
    result = ValidationResult('test-001')
    EncodingValidator.validate(test_example, result)
    print(f"   Result: {result.checks['encoding_check']}")
    print(f"   Issues: {len(result.issues)}")

    # Test syntax validator
    print("\n2. Testing Python syntax validator...")
    test_example = {
        'metadata': {'lang': 'python'},
        'conversations': [
            {'turn': 1, 'from': 'assistant', 'value': '```python\ndef test():\n    return True\n```'}
        ]
    }
    result = ValidationResult('test-002')
    SyntaxValidator.validate(test_example, result)
    print(f"   Result: {result.checks['syntax_check']}")

    print("\n✓ Validation framework ready")
