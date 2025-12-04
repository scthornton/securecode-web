#!/usr/bin/env python3
"""
Perform manual quality review of random sample from SecureCode v2.0 dataset
"""

import json
import random
from pathlib import Path
from collections import Counter

def load_dataset():
    """Load all examples"""
    data_dir = Path(__file__).parent.parent.parent / 'consolidated'

    examples = []
    for split in ['train', 'val', 'test']:
        split_file = data_dir / f'{split}.jsonl'
        with open(split_file) as f:
            for line in f:
                examples.append(json.loads(line))

    return examples

def select_stratified_sample(examples, n=50):
    """Select stratified random sample"""
    # Group by category
    by_category = {}
    for ex in examples:
        cat = ex.get('metadata', {}).get('category', 'unknown')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(ex)

    # Sample proportionally from each category
    sample = []
    random.seed(42)

    for cat, cat_examples in by_category.items():
        cat_sample_size = max(1, int(len(cat_examples) / len(examples) * n))
        sample.extend(random.sample(cat_examples, min(cat_sample_size, len(cat_examples))))

    # If we need more to reach n, sample randomly
    if len(sample) < n:
        remaining = [ex for ex in examples if ex not in sample]
        sample.extend(random.sample(remaining, n - len(sample)))

    return sample[:n]

def check_json_structure(example):
    """Verify JSON structure is correct"""
    issues = []

    # Check required top-level fields
    required_fields = ['id', 'metadata', 'context', 'conversations']
    for field in required_fields:
        if field not in example:
            issues.append(f"Missing field: {field}")

    # Check metadata
    if 'metadata' in example:
        meta = example['metadata']
        required_meta = ['lang', 'category', 'subcategory', 'severity']
        for field in required_meta:
            if field not in meta:
                issues.append(f"Missing metadata.{field}")

    # Check conversations
    if 'conversations' in example:
        convs = example['conversations']
        if len(convs) != 4:
            issues.append(f"Expected 4 conversations, got {len(convs)}")

        for i, conv in enumerate(convs):
            if 'from' not in conv or 'value' not in conv:
                issues.append(f"Conversation {i+1} missing 'from' or 'value'")

    return issues

def check_code_quality(example):
    """Check code quality indicators"""
    issues = []

    # Check for code blocks
    content = ' '.join([c.get('value', '') for c in example.get('conversations', [])])

    vulnerable_count = content.count('```')
    if vulnerable_count < 2:
        issues.append(f"Only {vulnerable_count} code blocks found (expected 4+)")

    # Check for key security terms
    security_terms = ['vulnerable', 'secure', 'attack', 'defense', 'exploit', 'protect']
    found_terms = [term for term in security_terms if term.lower() in content.lower()]

    if len(found_terms) < 3:
        issues.append(f"Few security terms found: {found_terms}")

    # Check length
    if len(content) < 2000:
        issues.append(f"Content seems short: {len(content)} chars")

    return issues

def check_real_world_context(example):
    """Check real-world incident quality"""
    issues = []

    context = example.get('context', {})

    # Check incident field
    incident = context.get('real_world_incident', '')
    if not incident or len(incident) < 10:
        issues.append("Missing or weak real_world_incident")

    # Check impact
    impact = context.get('impact', '')
    if not impact or len(impact) < 20:
        issues.append("Missing or weak impact description")

    # Check CVE (optional but good to have)
    cve = context.get('cve', '')
    if cve and cve != 'N/A':
        if not cve.startswith('CVE-20'):
            issues.append(f"Questionable CVE format: {cve}")

    # Check year
    year = context.get('year')
    if not year or year < 2018 or year > 2025:
        issues.append(f"Questionable year: {year}")

    return issues

def review_example(example, idx):
    """Comprehensive review of single example"""
    print(f"\n{'='*80}")
    print(f"EXAMPLE {idx + 1}")
    print(f"{'='*80}")
    print(f"ID: {example.get('id', 'MISSING')}")
    print(f"Category: {example.get('metadata', {}).get('category', 'MISSING')}")
    print(f"Language: {example.get('metadata', {}).get('lang', 'MISSING')}")
    print(f"Severity: {example.get('metadata', {}).get('severity', 'MISSING')}")

    # Context
    context = example.get('context', {})
    print(f"\nIncident: {context.get('real_world_incident', 'MISSING')[:80]}...")
    print(f"CVE: {context.get('cve', 'N/A')}")
    print(f"Year: {context.get('year', 'MISSING')}")

    # Quality checks
    all_issues = []

    struct_issues = check_json_structure(example)
    if struct_issues:
        print(f"\n⚠️  Structure Issues:")
        for issue in struct_issues:
            print(f"   - {issue}")
        all_issues.extend(struct_issues)

    code_issues = check_code_quality(example)
    if code_issues:
        print(f"\n⚠️  Code Quality Issues:")
        for issue in code_issues:
            print(f"   - {issue}")
        all_issues.extend(code_issues)

    context_issues = check_real_world_context(example)
    if context_issues:
        print(f"\n⚠️  Context Issues:")
        for issue in context_issues:
            print(f"   - {issue}")
        all_issues.extend(context_issues)

    if not all_issues:
        print(f"\n✅ No issues found - Example looks excellent!")

    return len(all_issues) == 0

def main():
    """Main quality review process"""
    print("=" * 80)
    print("SECURECODE v2.0 QUALITY REVIEW")
    print("=" * 80)

    # Load dataset
    print("\nLoading dataset...")
    examples = load_dataset()
    print(f"Loaded {len(examples)} examples")

    # Select sample
    print("\nSelecting stratified random sample (n=50)...")
    sample = select_stratified_sample(examples, n=50)

    # Show sample distribution
    categories = Counter(ex.get('metadata', {}).get('category') for ex in sample)
    languages = Counter(ex.get('metadata', {}).get('lang') for ex in sample)

    print(f"\nSample distribution:")
    print(f"  Categories: {dict(categories)}")
    print(f"  Languages: {dict(languages)}")

    # Review each example
    print("\n" + "=" * 80)
    print("REVIEWING SAMPLE")
    print("=" * 80)

    perfect_count = 0
    issue_count = 0

    for idx, example in enumerate(sample):
        is_perfect = review_example(example, idx)
        if is_perfect:
            perfect_count += 1
        else:
            issue_count += 1

    # Summary
    print("\n" + "=" * 80)
    print("QUALITY REVIEW SUMMARY")
    print("=" * 80)
    print(f"\nSample size: {len(sample)}")
    print(f"Perfect examples: {perfect_count} ({perfect_count/len(sample)*100:.1f}%)")
    print(f"Examples with issues: {issue_count} ({issue_count/len(sample)*100:.1f}%)")

    if perfect_count / len(sample) >= 0.90:
        print(f"\n✅ EXCELLENT - Quality threshold exceeded (>90% perfect)")
    elif perfect_count / len(sample) >= 0.75:
        print(f"\n✅ GOOD - Quality acceptable (>75% perfect)")
    else:
        print(f"\n⚠️  NEEDS ATTENTION - Quality below threshold (<75% perfect)")

    print("\nNote: This is an automated review. Manual inspection of code execution")
    print("and CVE accuracy would require additional human review.")

if __name__ == '__main__':
    main()
