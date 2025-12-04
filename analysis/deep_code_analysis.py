#!/usr/bin/env python3
"""
Deep code analysis for SecureCode v2.0 dataset
Examines specific examples for security accuracy and code realism
"""

import json
import re
import ast
import random
from pathlib import Path
from typing import Dict, List, Tuple, Any
from collections import defaultdict

def extract_code_blocks(text: str) -> List[Tuple[str, str]]:
    """Extract all code blocks from markdown text with their language tags."""
    pattern = r'```(\w+)\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


def analyze_security_patterns(code: str, language: str, label: str = 'unknown') -> Dict[str, Any]:
    """
    Analyze code for security patterns - both vulnerabilities and fixes.
    """
    issues = []
    good_practices = []

    if language == 'python':
        # Check for SQL injection vulnerabilities
        if 'execute(' in code or 'executemany(' in code:
            if any(pattern in code for pattern in [' + ', '.format(', 'f"', "f'"]):
                issues.append('SQL injection risk: string concatenation in SQL query')
            if 'cursor.execute' in code and '?' in code:
                good_practices.append('Uses parameterized queries with placeholders')

        # Check for hardcoded credentials
        if re.search(r'(password|secret|key)\s*=\s*["\'][^"\']+["\']', code, re.IGNORECASE):
            issues.append('Hardcoded credentials detected')

        # Check for secure practices
        if 'os.getenv' in code or 'environ' in code:
            good_practices.append('Uses environment variables for configuration')

        if 'try:' in code and 'except' in code:
            good_practices.append('Includes error handling')

        if 'bcrypt' in code or 'pbkdf2' in code or 'scrypt' in code or 'argon2' in code:
            good_practices.append('Uses secure password hashing')

        if 'secrets.compare_digest' in code:
            good_practices.append('Uses timing-safe comparison')

    elif language == 'javascript' or language == 'typescript':
        # Check for XSS vulnerabilities
        if 'innerHTML' in code or 'dangerouslySetInnerHTML' in code:
            issues.append('XSS risk: innerHTML or dangerouslySetInnerHTML usage')

        if 'eval(' in code:
            issues.append('Code injection risk: eval() usage')

        # Check for good practices
        if 'DOMPurify' in code or 'sanitize' in code:
            good_practices.append('Uses input sanitization')

        if 'helmet' in code:
            good_practices.append('Uses Helmet.js for security headers')

        if 'express-validator' in code or 'joi' in code or 'zod' in code:
            good_practices.append('Uses input validation library')

    elif language == 'java':
        # Check for SQL injection
        if 'Statement' in code and 'executeQuery' in code:
            if '+' in code:
                issues.append('SQL injection risk: string concatenation in SQL')

        if 'PreparedStatement' in code:
            good_practices.append('Uses PreparedStatement for SQL queries')

        # Check for deserialization issues
        if 'readObject' in code and 'ObjectInputStream' in code:
            issues.append('Deserialization vulnerability risk')

    elif language == 'go':
        # Check for SQL injection
        if 'db.Query' in code or 'db.Exec' in code:
            if 'fmt.Sprintf' in code or '+' in code:
                issues.append('SQL injection risk: string formatting in SQL')
            if '?' in code or '$1' in code:
                good_practices.append('Uses parameterized queries')

        # Check for error handling
        if 'if err != nil' in code:
            good_practices.append('Proper Go error handling')

    elif language == 'php':
        # Check for SQL injection
        if 'mysql_query' in code or 'mysqli_query' in code:
            if '.' in code:  # concatenation
                issues.append('SQL injection risk: string concatenation in SQL')

        if 'PDO' in code or 'prepare(' in code:
            good_practices.append('Uses prepared statements')

        # Check for XSS
        if 'echo' in code and '$_GET' in code or '$_POST' in code:
            issues.append('XSS risk: direct output of user input')

        if 'htmlspecialchars' in code or 'htmlentities' in code:
            good_practices.append('Uses HTML escaping')

    return {
        'security_issues': issues,
        'good_practices': good_practices,
        'has_vulnerability': len(issues) > 0,
        'has_fix': len(good_practices) > 0
    }


def validate_vulnerability_fix_pair(vulnerable_code: str, secure_code: str, language: str) -> Dict[str, Any]:
    """
    Validate that a vulnerable/secure code pair actually demonstrates the vulnerability and fix.
    """
    vuln_analysis = analyze_security_patterns(vulnerable_code, language, 'vulnerable')
    secure_analysis = analyze_security_patterns(secure_code, language, 'secure')

    return {
        'vulnerable_code_has_issues': vuln_analysis['has_vulnerability'],
        'secure_code_has_fixes': secure_analysis['has_fix'],
        'vulnerable_issues': vuln_analysis['security_issues'],
        'secure_practices': secure_analysis['good_practices'],
        'valid_pair': vuln_analysis['has_vulnerability'] and secure_analysis['has_fix']
    }


def extract_example_code_structure(example: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and categorize code blocks from an example.
    """
    conversations = example.get('conversations', [])

    # Usually: turn 1 = question, turn 2 = vulnerable code + explanation,
    #          turn 3 = followup, turn 4 = production pattern

    all_code_blocks = []
    for turn in conversations:
        text = turn.get('value', '')
        blocks = extract_code_blocks(text)
        all_code_blocks.extend(blocks)

    # Try to identify vulnerable vs secure code
    # Typically first few blocks are vulnerable, later blocks are secure
    vulnerable_blocks = []
    secure_blocks = []

    for lang, code in all_code_blocks:
        # Heuristics to identify vulnerable code
        if any(marker in code.lower() for marker in [
            'vulnerable', 'bad:', '# bad', '// bad', 'insecure',
            'do not use', "don't use", 'dangerous'
        ]):
            vulnerable_blocks.append((lang, code))
        elif any(marker in code.lower() for marker in [
            'secure', 'good:', '# good', '// good', 'safe',
            'defense', 'protection', 'sanitize'
        ]):
            secure_blocks.append((lang, code))

    return {
        'total_blocks': len(all_code_blocks),
        'all_blocks': all_code_blocks,
        'vulnerable_blocks': vulnerable_blocks,
        'secure_blocks': secure_blocks
    }


def test_python_execution(code: str) -> Dict[str, Any]:
    """
    Test if Python code can be executed (imports, basic structure).
    """
    result = {
        'parseable': False,
        'has_imports': False,
        'has_functions': False,
        'has_classes': False,
        'error': None
    }

    try:
        tree = ast.parse(code)
        result['parseable'] = True

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                result['has_imports'] = True
            if isinstance(node, ast.FunctionDef):
                result['has_functions'] = True
            if isinstance(node, ast.ClassDef):
                result['has_classes'] = True

    except SyntaxError as e:
        result['error'] = f"SyntaxError: {e.msg} at line {e.lineno}"
    except Exception as e:
        result['error'] = f"Parse error: {str(e)}"

    return result


def analyze_example_realism(example: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assess whether the example contains realistic, production-quality code.
    """
    metadata = example.get('metadata', {})
    context = example.get('context', {})
    code_structure = extract_example_code_structure(example)

    # Check if references real CVE
    has_real_cve = context.get('cve', 'N/A').startswith('CVE-')
    has_real_impact = 'impact' in context and len(context.get('impact', '')) > 20

    # Check code quality indicators
    all_blocks = code_structure['all_blocks']
    total_lines = sum(len(code.split('\n')) for _, code in all_blocks)
    avg_lines = total_lines / len(all_blocks) if all_blocks else 0

    realism_score = 0
    reasons = []

    if has_real_cve:
        realism_score += 2
        reasons.append(f"References real CVE: {context.get('cve')}")

    if has_real_impact:
        realism_score += 1
        reasons.append("Includes detailed impact information")

    if avg_lines > 30:
        realism_score += 2
        reasons.append(f"Substantial code blocks (avg {avg_lines:.0f} lines)")

    # Check for production patterns
    lang = metadata.get('lang', 'unknown')
    production_indicators = 0

    for _, code in all_blocks:
        if 'import ' in code or 'require(' in code or 'use ' in code:
            production_indicators += 1
        if 'class ' in code or 'interface ' in code or 'struct ' in code:
            production_indicators += 1
        if 'try ' in code or 'catch ' in code or 'except ' in code:
            production_indicators += 1

    if production_indicators >= 3:
        realism_score += 2
        reasons.append(f"Production patterns present: {production_indicators} indicators")

    return {
        'realism_score': realism_score,
        'max_score': 7,
        'reasons': reasons,
        'has_real_cve': has_real_cve,
        'has_real_impact': has_real_impact,
        'avg_code_lines': avg_lines,
        'total_code_blocks': len(all_blocks)
    }


def main():
    """Main analysis workflow."""
    random.seed(42)

    print("=" * 80)
    print("SecureCode v2.0 - Deep Code Analysis Report")
    print("=" * 80)

    dataset_path = Path('/Users/scott/perfecxion/datasets/securecode/v2/consolidated')
    train_path = dataset_path / 'train.jsonl'

    # Load all examples
    examples = []
    with open(train_path, 'r') as f:
        for line in f:
            examples.append(json.loads(line))

    print(f"\n[1] SECURITY PATTERN ANALYSIS")
    print("-" * 80)

    # Sample 10 examples for deep analysis
    sample_size = 10
    sampled = random.sample(examples, sample_size)

    security_results = []
    realism_results = []

    for i, example in enumerate(sampled, 1):
        metadata = example.get('metadata', {})
        example_id = example.get('id', 'unknown')
        category = metadata.get('category', 'unknown')
        subcategory = metadata.get('subcategory', 'unknown')
        language = metadata.get('lang', 'unknown')

        print(f"\n{i}. {example_id}")
        print(f"   Category: {category}/{subcategory}")
        print(f"   Language: {language}")

        # Extract code structure
        code_structure = extract_example_code_structure(example)
        print(f"   Total code blocks: {code_structure['total_blocks']}")

        # Analyze vulnerable/secure pairs
        lang_normalized = language.lower()
        if lang_normalized in ['python', 'javascript', 'typescript', 'java', 'go', 'php']:
            # Find first programming language block
            prog_blocks = [
                (lang, code) for lang, code in code_structure['all_blocks']
                if lang.lower() in [lang_normalized, 'python', 'javascript', 'java', 'go', 'php']
            ]

            if len(prog_blocks) >= 2:
                # Assume first is vulnerable, second is secure
                vuln_lang, vuln_code = prog_blocks[0]
                secure_lang, secure_code = prog_blocks[1] if len(prog_blocks) > 1 else prog_blocks[0]

                pair_analysis = validate_vulnerability_fix_pair(
                    vuln_code, secure_code, lang_normalized
                )

                print(f"   Vulnerability analysis:")
                print(f"     - Vulnerable code has issues: {pair_analysis['vulnerable_code_has_issues']}")
                print(f"     - Issues found: {', '.join(pair_analysis['vulnerable_issues']) if pair_analysis['vulnerable_issues'] else 'None detected'}")
                print(f"   Secure code analysis:")
                print(f"     - Secure code has fixes: {pair_analysis['secure_code_has_fixes']}")
                print(f"     - Good practices: {', '.join(pair_analysis['secure_practices']) if pair_analysis['secure_practices'] else 'None detected'}")

                security_results.append(pair_analysis)

        # Realism assessment
        realism = analyze_example_realism(example)
        print(f"   Realism score: {realism['realism_score']}/{realism['max_score']}")
        for reason in realism['reasons']:
            print(f"     - {reason}")

        realism_results.append(realism)

    # Summary statistics
    print(f"\n\n[2] SECURITY ACCURACY SUMMARY")
    print("-" * 80)

    if security_results:
        vuln_detected = sum(1 for r in security_results if r['vulnerable_code_has_issues'])
        fix_detected = sum(1 for r in security_results if r['secure_code_has_fixes'])
        valid_pairs = sum(1 for r in security_results if r['valid_pair'])

        print(f"\nVulnerable code with detected issues: {vuln_detected}/{len(security_results)} ({vuln_detected/len(security_results)*100:.1f}%)")
        print(f"Secure code with detected fixes:      {fix_detected}/{len(security_results)} ({fix_detected/len(security_results)*100:.1f}%)")
        print(f"Valid vulnerability/fix pairs:        {valid_pairs}/{len(security_results)} ({valid_pairs/len(security_results)*100:.1f}%)")

        print(f"\nNote: Some patterns may not be detected by basic static analysis.")
        print(f"Manual review is recommended for comprehensive validation.")

    print(f"\n\n[3] CODE REALISM SUMMARY")
    print("-" * 80)

    avg_realism = sum(r['realism_score'] for r in realism_results) / len(realism_results)
    max_possible = realism_results[0]['max_score'] if realism_results else 7

    print(f"\nAverage realism score: {avg_realism:.1f}/{max_possible} ({avg_realism/max_possible*100:.1f}%)")

    with_cve = sum(1 for r in realism_results if r['has_real_cve'])
    with_impact = sum(1 for r in realism_results if r['has_real_impact'])

    print(f"Examples with real CVE references: {with_cve}/{len(realism_results)} ({with_cve/len(realism_results)*100:.1f}%)")
    print(f"Examples with detailed impact:     {with_impact}/{len(realism_results)} ({with_impact/len(realism_results)*100:.1f}%)")

    avg_code_lines = sum(r['avg_code_lines'] for r in realism_results) / len(realism_results)
    print(f"Average lines per code block:      {avg_code_lines:.1f}")

    print(f"\n\n[4] PYTHON CODE EXECUTION TESTING")
    print("-" * 80)

    # Test Python examples specifically
    python_examples = [ex for ex in sampled if ex.get('metadata', {}).get('lang') == 'python']

    if python_examples:
        print(f"\nTesting {len(python_examples)} Python examples...")

        for example in python_examples:
            example_id = example.get('id')
            code_structure = extract_example_code_structure(example)

            print(f"\n{example_id}:")

            python_blocks = [
                code for lang, code in code_structure['all_blocks']
                if lang.lower() == 'python'
            ]

            for i, code in enumerate(python_blocks[:3], 1):  # Test first 3 blocks
                result = test_python_execution(code)
                status = "✓" if result['parseable'] else "✗"
                print(f"  Block {i}: {status} ", end='')

                if result['parseable']:
                    features = []
                    if result['has_imports']:
                        features.append("imports")
                    if result['has_functions']:
                        features.append("functions")
                    if result['has_classes']:
                        features.append("classes")
                    print(f"Parseable ({', '.join(features) if features else 'basic code'})")
                else:
                    print(f"Error: {result['error']}")

    print("\n" + "=" * 80)
    print("DEEP ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
