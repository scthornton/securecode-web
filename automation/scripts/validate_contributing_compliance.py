#!/usr/bin/env python3
"""
Validate SecureCode v2.0 compliance with CONTRIBUTING.md standards
"""

import json
from pathlib import Path
from collections import defaultdict
import re

# Valid values from CONTRIBUTING.md
VALID_LANGUAGES = {
    'python', 'javascript', 'java', 'go', 'php', 'csharp',
    'typescript', 'ruby', 'rust', 'kotlin'
}

VALID_SEVERITIES = {'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'}

VALID_OWASP_CATEGORIES = {
    'A01:2021-Broken Access Control',
    'A02:2021-Cryptographic Failures',
    'A03:2021-Injection',
    'A04:2021-Insecure Design',
    'A05:2021-Security Misconfiguration',
    'A06:2021-Vulnerable and Outdated Components',
    'A07:2021-Identification and Authentication Failures',
    'A08:2021-Software and Data Integrity Failures',
    'A09:2021-Security Logging and Monitoring Failures',
    'A10:2021-Server-Side Request Forgery',
    'AI/ML Security'
}

def check_four_turn_conversation(example):
    """
    Verify example follows 4-turn conversation standard
    """
    issues = []
    convs = example.get('conversations', [])

    if len(convs) != 4:
        issues.append(f"Has {len(convs)} turns, requires exactly 4")
        return issues

    # Check turn sequence
    expected_sequence = ['human', 'assistant', 'human', 'assistant']
    for i, conv in enumerate(convs):
        expected_from = expected_sequence[i]
        actual_from = conv.get('from', '')
        if actual_from != expected_from:
            issues.append(f"Turn {i+1}: expected '{expected_from}', got '{actual_from}'")

    # Check turn numbers if present
    for i, conv in enumerate(convs):
        if 'turn' in conv and conv['turn'] != i + 1:
            issues.append(f"Turn number mismatch at position {i+1}: got turn {conv['turn']}")

    # Check content minimums
    #  Turns 1 and 3 (user questions) can be concise (min 50 chars)
    #  Turns 2 and 4 (assistant responses) need more content (min 100 chars)
    for i, conv in enumerate(convs):
        value = conv.get('value', '')

        if i in [0, 2]:  # Turns 1 and 3 - user questions
            min_length = 50
        else:  # Turns 2 and 4 - assistant responses
            min_length = 100

        if len(value) < min_length:
            issues.append(f"Turn {i+1} too short ({len(value)} chars, minimum {min_length})")

    return issues

def check_required_metadata(example):
    """
    Verify all required metadata fields are present
    """
    issues = []
    metadata = example.get('metadata', {})

    # Check required fields
    required_fields = ['lang', 'category', 'severity']
    for field in required_fields:
        if field not in metadata or not metadata[field]:
            issues.append(f"Missing required metadata field: {field}")

    # Validate language
    lang = metadata.get('lang', '').lower()
    if lang and lang not in VALID_LANGUAGES:
        issues.append(f"Invalid language '{lang}', must be one of: {', '.join(sorted(VALID_LANGUAGES))}")

    # Validate severity
    severity = metadata.get('severity', '').upper()
    if severity and severity not in VALID_SEVERITIES:
        issues.append(f"Invalid severity '{severity}', must be one of: {', '.join(VALID_SEVERITIES)}")

    # Check context fields
    context = example.get('context', {})
    if not context.get('real_world_incident'):
        issues.append("Missing 'real_world_incident' in context")

    if not context.get('impact'):
        issues.append("Missing 'impact' in context (business_impact)")

    return issues

def check_code_quality(example):
    """
    Check for code block presence and basic quality indicators
    """
    issues = []

    # Count code blocks
    content = ' '.join([c.get('value', '') for c in example.get('conversations', [])])
    code_block_count = content.count('```')

    if code_block_count < 4:
        issues.append(f"Only {code_block_count // 2} code blocks found, need at least 2 (vulnerable + secure)")

    # Check for vulnerable/insecure keywords in turn 2
    turn_2 = example.get('conversations', [{}])[1].get('value', '').lower() if len(example.get('conversations', [])) >= 2 else ''

    has_vulnerable = any(word in turn_2 for word in ['vulnerable', 'insecure', 'weak', 'unsafe', 'bad practice'])
    has_secure = any(word in turn_2 for word in ['secure', 'safe', 'protected', 'fixed', 'hardened'])

    if not has_vulnerable:
        issues.append("Turn 2 should discuss vulnerable implementation")

    if not has_secure:
        issues.append("Turn 2 should include secure implementation")

    # Check turn 4 for defense-in-depth
    turn_4 = example.get('conversations', [{}])[3].get('value', '').lower() if len(example.get('conversations', [])) >= 4 else ''

    defense_keywords = ['defense', 'monitoring', 'logging', 'detection', 'least privilege', 'rate limit']
    has_defense_in_depth = any(keyword in turn_4 for keyword in defense_keywords)

    if not has_defense_in_depth:
        issues.append("Turn 4 should include defense-in-depth discussion (logging, monitoring, detection)")

    return issues

def check_real_world_grounding(example):
    """
    Verify real-world incident/CVE references
    """
    issues = []
    context = example.get('context', {})

    incident = context.get('real_world_incident', '')
    impact = context.get('impact', '')
    cve = context.get('cve')

    if len(incident) < 10:
        issues.append("real_world_incident too vague or missing")

    if len(impact) < 20:
        issues.append("business impact description too short")

    # CVE format check if present
    if cve and cve not in [None, 'null', 'N/A', '']:
        if not re.match(r'CVE-\d{4}-\d+', cve):
            issues.append(f"Invalid CVE format: {cve} (should be CVE-YYYY-NNNNN)")

    return issues

def validate_dataset(dataset_path):
    """
    Validate entire dataset against CONTRIBUTING.md standards
    """
    print("="*80)
    print("SECURECODE v2.0 - CONTRIBUTING.MD COMPLIANCE VALIDATION")
    print("="*80)

    with open(dataset_path) as f:
        examples = [json.loads(line) for line in f]

    print(f"\nValidating {len(examples)} examples from {dataset_path.name}...\n")

    results = {
        'four_turn_violations': [],
        'metadata_issues': [],
        'code_quality_issues': [],
        'real_world_grounding_issues': [],
        'perfect_examples': 0,
        'total_examples': len(examples)
    }

    for idx, example in enumerate(examples):
        example_id = example.get('id', f'unknown_{idx}')
        all_issues = []

        # Run all checks
        four_turn_issues = check_four_turn_conversation(example)
        metadata_issues = check_required_metadata(example)
        code_quality_issues = check_code_quality(example)
        real_world_issues = check_real_world_grounding(example)

        if four_turn_issues:
            results['four_turn_violations'].append({
                'id': example_id,
                'issues': four_turn_issues
            })
            all_issues.extend(four_turn_issues)

        if metadata_issues:
            results['metadata_issues'].append({
                'id': example_id,
                'issues': metadata_issues
            })
            all_issues.extend(metadata_issues)

        if code_quality_issues:
            results['code_quality_issues'].append({
                'id': example_id,
                'issues': code_quality_issues
            })
            all_issues.extend(code_quality_issues)

        if real_world_issues:
            results['real_world_grounding_issues'].append({
                'id': example_id,
                'issues': real_world_issues
            })
            all_issues.extend(real_world_issues)

        if not all_issues:
            results['perfect_examples'] += 1

    return results

def print_report(results):
    """
    Print validation report
    """
    print("\n" + "="*80)
    print("VALIDATION RESULTS")
    print("="*80)

    total = results['total_examples']
    perfect = results['perfect_examples']
    compliance_rate = (perfect / total * 100) if total > 0 else 0

    print(f"\n📊 Overall Compliance: {perfect}/{total} ({compliance_rate:.1f}%)")
    print(f"✅ Perfect examples: {perfect}")
    print(f"❌ Examples with issues: {total - perfect}")

    print("\n" + "-"*80)
    print("ISSUE BREAKDOWN")
    print("-"*80)

    print(f"\n🔄 Four-Turn Conversation Violations: {len(results['four_turn_violations'])}")
    if results['four_turn_violations']:
        print("   First 5 examples:")
        for item in results['four_turn_violations'][:5]:
            print(f"   ❌ {item['id']}")
            for issue in item['issues'][:2]:
                print(f"      • {issue}")

    print(f"\n📋 Metadata Issues: {len(results['metadata_issues'])}")
    if results['metadata_issues']:
        print("   First 5 examples:")
        for item in results['metadata_issues'][:5]:
            print(f"   ❌ {item['id']}")
            for issue in item['issues'][:2]:
                print(f"      • {issue}")

    print(f"\n💻 Code Quality Issues: {len(results['code_quality_issues'])}")
    if results['code_quality_issues']:
        print("   First 5 examples:")
        for item in results['code_quality_issues'][:5]:
            print(f"   ❌ {item['id']}")
            for issue in item['issues'][:2]:
                print(f"      • {issue}")

    print(f"\n🌍 Real-World Grounding Issues: {len(results['real_world_grounding_issues'])}")
    if results['real_world_grounding_issues']:
        print("   First 5 examples:")
        for item in results['real_world_grounding_issues'][:5]:
            print(f"   ❌ {item['id']}")
            for issue in item['issues'][:2]:
                print(f"      • {issue}")

    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)

    if compliance_rate >= 95:
        print("\n✅ EXCELLENT: Dataset meets CONTRIBUTING.md standards")
        print("   Ready for production use with minimal fixes needed.")
    elif compliance_rate >= 85:
        print("\n⚠️  GOOD: Dataset mostly compliant but needs attention")
        print("   Address high-priority issues before publication.")
    elif compliance_rate >= 70:
        print("\n⚠️  FAIR: Significant compliance gaps")
        print("   Systematic fixes required across multiple categories.")
    else:
        print("\n❌ POOR: Major compliance issues")
        print("   Dataset requires comprehensive review and fixes.")

    print("\n" + "="*80)

def main():
    # Validate consolidated training set
    dataset_path = Path(__file__).parent.parent.parent / 'consolidated' / 'train.jsonl'

    if not dataset_path.exists():
        print(f"❌ Dataset not found: {dataset_path}")
        return

    results = validate_dataset(dataset_path)
    print_report(results)

    # Save detailed results
    output_file = Path(__file__).parent.parent / 'logs' / 'contributing_compliance_report.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Detailed results saved to: {output_file}")

if __name__ == '__main__':
    main()
