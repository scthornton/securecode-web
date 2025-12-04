#!/usr/bin/env python3
"""
Add defense-in-depth discussion to turn 4 where missing
Per CONTRIBUTING.md: Turn 4 should include logging, monitoring, detection, least privilege, rate limiting
"""

import json
from pathlib import Path

DEFENSE_KEYWORDS = ['defense', 'monitoring', 'logging', 'detection', 'least privilege', 'rate limit']

DEFENSE_ADDENDUM = """

**Operational Security Considerations:**

- **Logging & Monitoring**: Log all security-relevant events (authentication attempts, authorization failures, suspicious patterns) to a centralized logging system for detection and forensic analysis.
- **Detection**: Implement alerts for anomalous behavior such as repeated failed attempts, unusual access patterns, or privilege escalation attempts.
- **Least Privilege**: Ensure services and users operate with minimum necessary permissions to limit blast radius of potential compromises.
- **Defense-in-Depth**: Layer multiple security controls (input validation, parameterized queries, WAF, rate limiting, network segmentation) so that failure of one control doesn't lead to full compromise.
"""

def needs_defense_in_depth(example):
    """
    Check if turn 4 needs defense-in-depth enhancement
    """
    conversations = example.get('conversations', [])
    if len(conversations) < 4:
        return False

    turn_4_content = conversations[3].get('value', '').lower()

    # Check if defense keywords are present
    has_defense = any(keyword in turn_4_content for keyword in DEFENSE_KEYWORDS)

    return not has_defense

def add_defense_in_depth(example):
    """
    Add defense-in-depth content to turn 4
    """
    conversations = example.get('conversations', [])
    if len(conversations) < 4:
        return False

    # Append defense-in-depth content to turn 4
    current_content = conversations[3].get('value', '')

    # Only add if not already present
    if 'Operational Security Considerations' not in current_content:
        conversations[3]['value'] = current_content + DEFENSE_ADDENDUM
        return True

    return False

def process_file(file_path):
    """Process a single JSONL file"""
    print(f"\nProcessing: {file_path.name}")

    examples = []
    enhanced_count = 0

    with open(file_path) as f:
        for line_num, line in enumerate(f, 1):
            example = json.loads(line)

            if needs_defense_in_depth(example):
                was_enhanced = add_defense_in_depth(example)
                if was_enhanced:
                    enhanced_count += 1
                    if enhanced_count <= 5:
                        print(f"  ✓ Enhanced {example.get('id', f'line_{line_num}')} with defense-in-depth content")

            examples.append(example)

    # Write back
    with open(file_path, 'w') as f:
        for example in examples:
            f.write(json.dumps(example) + '\n')

    print(f"  Enhanced {enhanced_count}/{len(examples)} examples")
    return enhanced_count, len(examples)

def main():
    print("="*80)
    print("DEFENSE-IN-DEPTH ENHANCEMENT")
    print("="*80)
    print("\nAdding defense-in-depth discussion to turn 4 where missing...")
    print(f"Keywords checked: {', '.join(DEFENSE_KEYWORDS)}\n")

    # Process data files
    data_dir = Path(__file__).parent.parent.parent / 'data'
    batch_files = sorted(data_dir.glob('*_batch_*.jsonl'))

    total_enhanced = 0
    total_examples = 0

    for batch_file in batch_files:
        enhanced, total = process_file(batch_file)
        total_enhanced += enhanced
        total_examples += total

    # Process consolidated files
    consolidated_dir = Path(__file__).parent.parent.parent / 'consolidated'
    for split_file in ['train.jsonl', 'val.jsonl', 'test.jsonl']:
        split_path = consolidated_dir / split_file
        if split_path.exists():
            enhanced, total = process_file(split_path)
            total_enhanced += enhanced
            total_examples += total

    print("\n" + "="*80)
    print(f"COMPLETE: Enhanced {total_enhanced} examples with defense-in-depth content")
    print("="*80)

if __name__ == '__main__':
    main()
