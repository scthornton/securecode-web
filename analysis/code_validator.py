#!/usr/bin/env python3
"""
SecureCode v2.0 Dataset Code Validation Script
Validates syntax and quality of code examples across multiple languages
"""

import json
import re
import ast
import random
from pathlib import Path
from typing import Dict, List, Tuple, Any
from collections import defaultdict, Counter

# Language validation patterns
LANGUAGE_PATTERNS = {
    'python': {
        'syntax_validator': 'ast_parse',
        'file_extension': '.py',
        'basic_checks': ['import', 'def', 'class']
    },
    'javascript': {
        'syntax_validator': 'basic_js',
        'file_extension': '.js',
        'basic_checks': ['function', 'const', 'let', 'var', '=>']
    },
    'typescript': {
        'syntax_validator': 'basic_ts',
        'file_extension': '.ts',
        'basic_checks': ['interface', 'type', 'function', '=>']
    },
    'java': {
        'syntax_validator': 'basic_java',
        'file_extension': '.java',
        'basic_checks': ['public', 'class', 'private', 'import']
    },
    'go': {
        'syntax_validator': 'basic_go',
        'file_extension': '.go',
        'basic_checks': ['package', 'func', 'import']
    },
    'php': {
        'syntax_validator': 'basic_php',
        'file_extension': '.php',
        'basic_checks': ['<?php', 'function', '$']
    },
    'csharp': {
        'syntax_validator': 'basic_csharp',
        'file_extension': '.cs',
        'basic_checks': ['namespace', 'using', 'class', 'public']
    },
    'ruby': {
        'syntax_validator': 'basic_ruby',
        'file_extension': '.rb',
        'basic_checks': ['def', 'class', 'end', 'require']
    },
    'rust': {
        'syntax_validator': 'basic_rust',
        'file_extension': '.rs',
        'basic_checks': ['fn', 'use', 'struct', 'impl']
    },
    'kotlin': {
        'syntax_validator': 'basic_kotlin',
        'file_extension': '.kt',
        'basic_checks': ['fun', 'val', 'var', 'class']
    }
}

# Config-based "languages"
CONFIG_LANGUAGES = ['docker', 'kubernetes', 'react', 'vue', 'angular']


def extract_code_blocks(text: str) -> List[Tuple[str, str]]:
    """Extract all code blocks from markdown text with their language tags."""
    # Pattern: ```language\ncode\n```
    pattern = r'```(\w+)\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


def validate_python_syntax(code: str) -> Tuple[bool, str]:
    """Validate Python code using AST parser."""
    try:
        ast.parse(code)
        return True, "Valid Python syntax"
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg} at line {e.lineno}"
    except Exception as e:
        return False, f"Parse error: {str(e)}"


def validate_javascript_basic(code: str) -> Tuple[bool, str]:
    """Basic JavaScript syntax validation."""
    # Check for common syntax errors
    issues = []

    # Count braces
    open_braces = code.count('{')
    close_braces = code.count('}')
    if open_braces != close_braces:
        issues.append(f"Unmatched braces: {open_braces} open, {close_braces} close")

    # Count parentheses
    open_parens = code.count('(')
    close_parens = code.count(')')
    if open_parens != close_parens:
        issues.append(f"Unmatched parentheses: {open_parens} open, {close_parens} close")

    # Count brackets
    open_brackets = code.count('[')
    close_brackets = code.count(']')
    if open_brackets != close_brackets:
        issues.append(f"Unmatched brackets: {open_brackets} open, {close_brackets} close")

    # Check for obvious syntax errors
    if ';;' in code:
        issues.append("Double semicolons found")

    if issues:
        return False, "; ".join(issues)
    return True, "Basic syntax checks passed"


def validate_java_basic(code: str) -> Tuple[bool, str]:
    """Basic Java syntax validation."""
    issues = []

    # Check for class definition
    if 'class ' in code and not re.search(r'class\s+\w+', code):
        issues.append("Invalid class definition")

    # Count braces
    open_braces = code.count('{')
    close_braces = code.count('}')
    if open_braces != close_braces:
        issues.append(f"Unmatched braces: {open_braces} open, {close_braces} close")

    # Check for basic structure
    if 'public ' in code or 'private ' in code:
        if not re.search(r'(public|private)\s+(class|void|int|String)', code):
            issues.append("Invalid access modifier usage")

    if issues:
        return False, "; ".join(issues)
    return True, "Basic syntax checks passed"


def validate_go_basic(code: str) -> Tuple[bool, str]:
    """Basic Go syntax validation."""
    issues = []

    # Must have package declaration
    if 'package ' not in code and len(code) > 50:
        issues.append("Missing package declaration (may be snippet)")

    # Count braces
    open_braces = code.count('{')
    close_braces = code.count('}')
    if open_braces != close_braces:
        issues.append(f"Unmatched braces: {open_braces} open, {close_braces} close")

    if issues:
        return False, "; ".join(issues)
    return True, "Basic syntax checks passed"


def validate_php_basic(code: str) -> Tuple[bool, str]:
    """Basic PHP syntax validation."""
    issues = []

    # Should start with <?php
    if '<?php' not in code and len(code) > 20:
        issues.append("Missing <?php opening tag")

    # Count braces
    open_braces = code.count('{')
    close_braces = code.count('}')
    if open_braces != close_braces:
        issues.append(f"Unmatched braces: {open_braces} open, {close_braces} close")

    if issues:
        return False, "; ".join(issues)
    return True, "Basic syntax checks passed"


def assess_code_quality(code: str, language: str) -> Dict[str, Any]:
    """Assess code quality metrics."""
    metrics = {
        'line_count': len(code.split('\n')),
        'has_comments': '#' in code or '//' in code or '/*' in code,
        'has_error_handling': False,
        'has_imports': False,
        'complexity': 'unknown'
    }

    # Check for imports
    if language == 'python':
        metrics['has_imports'] = 'import ' in code or 'from ' in code
        metrics['has_error_handling'] = 'try:' in code or 'except ' in code
    elif language in ['javascript', 'typescript']:
        metrics['has_imports'] = 'import ' in code or 'require(' in code
        metrics['has_error_handling'] = 'try ' in code or 'catch ' in code
    elif language == 'java':
        metrics['has_imports'] = 'import ' in code
        metrics['has_error_handling'] = 'try ' in code or 'catch ' in code
    elif language == 'go':
        metrics['has_imports'] = 'import ' in code
        metrics['has_error_handling'] = 'if err != nil' in code
    elif language == 'php':
        metrics['has_imports'] = 'require' in code or 'include' in code
        metrics['has_error_handling'] = 'try ' in code or 'catch ' in code

    # Assess complexity
    if metrics['line_count'] < 10:
        metrics['complexity'] = 'trivial'
    elif metrics['line_count'] < 30:
        metrics['complexity'] = 'simple'
    elif metrics['line_count'] < 100:
        metrics['complexity'] = 'moderate'
    else:
        metrics['complexity'] = 'complex'

    return metrics


def validate_example(example: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a single training example."""
    metadata = example.get('metadata', {})
    result = {
        'example_id': example.get('id', 'unknown'),
        'category': metadata.get('category', 'unknown'),
        'subcategory': metadata.get('subcategory', 'unknown'),
        'language': metadata.get('lang', 'unknown'),
        'difficulty': metadata.get('complexity', 'unknown'),
        'severity': metadata.get('severity', 'unknown'),
        'cve': example.get('context', {}).get('cve', 'N/A'),
        'code_blocks_found': 0,
        'code_blocks_validated': [],
        'syntax_errors': [],
        'quality_metrics': {},
        'overall_valid': True
    }

    # Extract all conversation turns
    conversations = example.get('conversations', [])
    full_text = '\n\n'.join(turn.get('value', '') for turn in conversations)

    # Extract all code blocks
    code_blocks = extract_code_blocks(full_text)
    result['code_blocks_found'] = len(code_blocks)

    if not code_blocks:
        result['overall_valid'] = False
        result['syntax_errors'].append("No code blocks found in example")
        return result

    # Validate each code block
    for lang_tag, code in code_blocks:
        block_result = {
            'language_tag': lang_tag,
            'code_length': len(code),
            'line_count': len(code.split('\n'))
        }

        # Normalize language tag
        lang_normalized = lang_tag.lower()

        # Validate syntax based on language
        if lang_normalized == 'python':
            valid, msg = validate_python_syntax(code)
            block_result['syntax_valid'] = valid
            block_result['validation_message'] = msg
            if not valid:
                result['syntax_errors'].append(f"Python: {msg}")
                result['overall_valid'] = False

        elif lang_normalized in ['javascript', 'js']:
            valid, msg = validate_javascript_basic(code)
            block_result['syntax_valid'] = valid
            block_result['validation_message'] = msg
            if not valid:
                result['syntax_errors'].append(f"JavaScript: {msg}")

        elif lang_normalized == 'java':
            valid, msg = validate_java_basic(code)
            block_result['syntax_valid'] = valid
            block_result['validation_message'] = msg
            if not valid:
                result['syntax_errors'].append(f"Java: {msg}")

        elif lang_normalized == 'go':
            valid, msg = validate_go_basic(code)
            block_result['syntax_valid'] = valid
            block_result['validation_message'] = msg
            if not valid:
                result['syntax_errors'].append(f"Go: {msg}")

        elif lang_normalized == 'php':
            valid, msg = validate_php_basic(code)
            block_result['syntax_valid'] = valid
            block_result['validation_message'] = msg
            if not valid:
                result['syntax_errors'].append(f"PHP: {msg}")

        else:
            block_result['syntax_valid'] = None
            block_result['validation_message'] = f"No validator for {lang_tag}"

        # Assess code quality
        quality = assess_code_quality(code, lang_normalized)
        block_result['quality'] = quality

        result['code_blocks_validated'].append(block_result)

    # Overall quality metrics
    if result['code_blocks_validated']:
        total_lines = sum(b['line_count'] for b in result['code_blocks_validated'])
        has_imports = any(b.get('quality', {}).get('has_imports') for b in result['code_blocks_validated'])
        has_error_handling = any(b.get('quality', {}).get('has_error_handling') for b in result['code_blocks_validated'])

        result['quality_metrics'] = {
            'total_code_lines': total_lines,
            'has_imports': has_imports,
            'has_error_handling': has_error_handling,
            'complexity_distribution': [b.get('quality', {}).get('complexity', 'unknown')
                                       for b in result['code_blocks_validated']]
        }

    return result


def sample_dataset(jsonl_path: Path, sample_size: int = 20) -> List[Dict[str, Any]]:
    """Load a stratified sample from the dataset."""
    examples = []
    with open(jsonl_path, 'r') as f:
        for line in f:
            examples.append(json.loads(line))

    # Stratify by language
    by_language = defaultdict(list)
    for ex in examples:
        lang = ex.get('metadata', {}).get('lang', 'unknown')
        by_language[lang].append(ex)

    # Sample proportionally from each language
    sampled = []
    languages = list(by_language.keys())
    samples_per_lang = max(1, sample_size // len(languages))

    for lang in languages:
        lang_examples = by_language[lang]
        n_samples = min(samples_per_lang, len(lang_examples))
        sampled.extend(random.sample(lang_examples, n_samples))

    # If we need more samples, add randomly
    if len(sampled) < sample_size:
        remaining = [ex for ex in examples if ex not in sampled]
        additional = min(sample_size - len(sampled), len(remaining))
        sampled.extend(random.sample(remaining, additional))

    return sampled[:sample_size]


def analyze_language_distribution(jsonl_path: Path) -> Dict[str, Any]:
    """Analyze the actual language distribution in the dataset."""
    language_counts = Counter()
    framework_counts = Counter()
    config_counts = Counter()
    category_counts = Counter()

    with open(jsonl_path, 'r') as f:
        for line in f:
            example = json.loads(line)
            metadata = example.get('metadata', {})
            lang = metadata.get('lang', 'unknown')
            category = metadata.get('category', 'unknown')

            category_counts[category] += 1

            if lang in CONFIG_LANGUAGES:
                config_counts[lang] += 1
            elif lang in ['react', 'vue', 'angular']:
                framework_counts[lang] += 1
            else:
                language_counts[lang] += 1

    return {
        'programming_languages': dict(language_counts),
        'frameworks': dict(framework_counts),
        'config_tools': dict(config_counts),
        'categories': dict(category_counts),
        'total_examples': sum(language_counts.values()) + sum(framework_counts.values()) + sum(config_counts.values())
    }


def main():
    """Main validation workflow."""
    random.seed(42)

    print("=" * 80)
    print("SecureCode v2.0 - Technical Code Validation Report")
    print("=" * 80)

    dataset_path = Path('/Users/scott/perfecxion/datasets/securecode/v2/consolidated')
    train_path = dataset_path / 'train.jsonl'

    # 1. Language Distribution Analysis
    print("\n[1] LANGUAGE DISTRIBUTION ANALYSIS")
    print("-" * 80)
    distribution = analyze_language_distribution(train_path)

    print(f"\nTotal Examples: {distribution['total_examples']}")

    print(f"\nOWASP Categories:")
    for cat, count in sorted(distribution['categories'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:25s}: {count:4d} examples")

    print(f"\nProgramming Languages:")
    for lang, count in sorted(distribution['programming_languages'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {lang:15s}: {count:4d} examples")

    if distribution['frameworks']:
        print(f"\nFrameworks (JavaScript-based):")
        for fw, count in sorted(distribution['frameworks'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {fw:15s}: {count:4d} examples")

    if distribution['config_tools']:
        print(f"\nConfiguration/Container Tools:")
        for cfg, count in sorted(distribution['config_tools'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {cfg:15s}: {count:4d} examples")

    # 2. Sample and Validate Code
    print("\n\n[2] CODE SYNTAX VALIDATION (20 SAMPLE EXAMPLES)")
    print("-" * 80)

    samples = sample_dataset(train_path, sample_size=20)
    validation_results = []

    print(f"\nValidating {len(samples)} sampled examples...")

    for i, example in enumerate(samples, 1):
        result = validate_example(example)
        validation_results.append(result)

        # Print summary
        status = "✓ PASS" if result['overall_valid'] else "✗ FAIL"
        print(f"\n{i:2d}. {result['example_id']}")
        print(f"    Category: {result['category']:15s}/{result['subcategory']:15s} Lang: {result['language']:8s} Severity: {result['severity']:8s} {status}")
        print(f"    Code Blocks: {result['code_blocks_found']:2d}   Complexity: {result['difficulty']:10s}  CVE: {result['cve']}")

        if result['syntax_errors']:
            print(f"    ERRORS: {', '.join(result['syntax_errors'])}")

        # Print code block details
        for j, block in enumerate(result['code_blocks_validated'], 1):
            valid_status = "✓" if block.get('syntax_valid') else ("✗" if block.get('syntax_valid') is False else "?")
            print(f"      Block {j}: {block['language_tag']:10s} {valid_status} {block['line_count']:3d} lines - {block.get('validation_message', 'N/A')}")

    # 3. Summary Statistics
    print("\n\n[3] VALIDATION SUMMARY STATISTICS")
    print("-" * 80)

    total_examples = len(validation_results)
    valid_examples = sum(1 for r in validation_results if r['overall_valid'])
    total_blocks = sum(r['code_blocks_found'] for r in validation_results)

    syntax_validated = sum(
        1 for r in validation_results
        for b in r['code_blocks_validated']
        if b.get('syntax_valid') is not None
    )
    syntax_passed = sum(
        1 for r in validation_results
        for b in r['code_blocks_validated']
        if b.get('syntax_valid') is True
    )

    print(f"\nExamples Validated: {total_examples}")
    print(f"Examples Passed:    {valid_examples} ({valid_examples/total_examples*100:.1f}%)")
    print(f"Examples Failed:    {total_examples - valid_examples} ({(total_examples-valid_examples)/total_examples*100:.1f}%)")

    print(f"\nTotal Code Blocks:  {total_blocks}")
    print(f"Blocks Validated:   {syntax_validated}")
    if syntax_validated > 0:
        print(f"Validation Passed:  {syntax_passed} ({syntax_passed/syntax_validated*100:.1f}% of validated)")
    else:
        print(f"Validation Passed:  {syntax_passed} (no blocks validated)")

    # Language-specific pass rates
    by_language = defaultdict(lambda: {'total': 0, 'passed': 0})
    for r in validation_results:
        lang = r['language']
        by_language[lang]['total'] += 1
        if r['overall_valid']:
            by_language[lang]['passed'] += 1

    print(f"\nPass Rate by Language:")
    for lang in sorted(by_language.keys()):
        stats = by_language[lang]
        rate = stats['passed'] / stats['total'] * 100
        print(f"  {lang:15s}: {stats['passed']:2d}/{stats['total']:2d} ({rate:5.1f}%)")

    # 4. Code Quality Assessment
    print("\n\n[4] CODE QUALITY ASSESSMENT")
    print("-" * 80)

    has_imports = sum(1 for r in validation_results if r.get('quality_metrics', {}).get('has_imports'))
    has_error_handling = sum(1 for r in validation_results if r.get('quality_metrics', {}).get('has_error_handling'))

    print(f"\nExamples with imports:        {has_imports}/{total_examples} ({has_imports/total_examples*100:.1f}%)")
    print(f"Examples with error handling: {has_error_handling}/{total_examples} ({has_error_handling/total_examples*100:.1f}%)")

    # Complexity distribution
    complexity_counts = Counter()
    for r in validation_results:
        for comp in r.get('quality_metrics', {}).get('complexity_distribution', []):
            complexity_counts[comp] += 1

    print(f"\nCode Complexity Distribution:")
    for comp in ['trivial', 'simple', 'moderate', 'complex', 'unknown']:
        if comp in complexity_counts:
            print(f"  {comp:10s}: {complexity_counts[comp]:3d} blocks")

    # Average lines per code block
    total_lines = sum(r.get('quality_metrics', {}).get('total_code_lines', 0) for r in validation_results)
    avg_lines = total_lines / total_blocks if total_blocks > 0 else 0
    print(f"\nAverage lines per code block: {avg_lines:.1f}")

    # 5. Save detailed results
    output_path = Path('/Users/scott/perfecxion/datasets/securecode/v2/analysis/validation_results.json')
    output_data = {
        'language_distribution': distribution,
        'validation_summary': {
            'total_examples': total_examples,
            'valid_examples': valid_examples,
            'pass_rate': valid_examples / total_examples,
            'total_code_blocks': total_blocks,
            'syntax_validated': syntax_validated,
            'syntax_passed': syntax_passed
        },
        'detailed_results': validation_results
    }

    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\n\n[5] DETAILED RESULTS SAVED")
    print("-" * 80)
    print(f"Full validation results saved to:\n{output_path}")

    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
