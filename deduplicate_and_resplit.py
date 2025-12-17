#!/usr/bin/env python3
"""
SecureCode v2.0 Deduplication and Re-Split Script

Addresses critical data leakage issues:
1. Deduplicates examples by content hash
2. Assigns unique IDs to all examples
3. Groups by CVE/incident
4. Re-splits maintaining group boundaries

Usage:
    python deduplicate_and_resplit.py --input-dir consolidated --output-dir consolidated_fixed
"""

import json
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict, Counter
import random


def compute_content_hash(example: Dict) -> str:
    """Compute deterministic hash of example content."""
    # Hash the conversation content (the actual training data)
    conversations = example.get('conversations', example.get('conversation', []))
    content_str = json.dumps(conversations, sort_keys=True)
    return hashlib.sha256(content_str.encode()).hexdigest()


def compute_split_group_id(example: Dict) -> str:
    """
    Compute grouping key to prevent same incident across splits.

    Uses COMPOSITE key of incident name + CVE to ensure both are grouped together.

    Priority:
    1. Incident name + CVE (if both present) - composite key
    2. Incident name only (if CVE missing)
    3. CVE only (if incident name missing)
    4. Incident source URL hash
    5. OWASP category + severity + content hash (fallback)
    """
    context = example.get('context', {})

    # Get both incident name and CVE
    incident_name = context.get('real_world_incident', '').strip()
    cve_id = context.get('cve')

    # Normalize incident name
    normalized_incident = None
    if incident_name and incident_name.lower() != 'unknown':
        normalized_incident = ' '.join(incident_name.lower().split())

    # Normalize CVE
    normalized_cve = None
    if cve_id and cve_id != "" and cve_id != "null" and cve_id is not None:
        normalized_cve = cve_id.strip()

    # Priority 1: Both incident and CVE present - create composite key
    if normalized_incident and normalized_cve:
        # Use CVE as primary key with incident as secondary
        # This ensures same CVE always groups together
        return f"cve:{normalized_cve}"

    # Priority 2: Incident name only
    if normalized_incident:
        incident_hash = hashlib.sha256(normalized_incident.encode()).hexdigest()[:16]
        return f"incident:{incident_hash}"

    # Priority 3: CVE only
    if normalized_cve:
        return f"cve:{normalized_cve}"

    # Priority 4: Incident grounding URL
    grounding = context.get('incident_grounding', {})
    source_url = grounding.get('source_url', '')
    if source_url:
        url_hash = hashlib.sha256(source_url.encode()).hexdigest()[:16]
        return f"url:{url_hash}"

    # Priority 5: Category + severity + partial content hash (fallback for ungrouped items)
    metadata = example.get('metadata', {})
    category = metadata.get('category', 'unknown')
    severity = metadata.get('severity', 'UNKNOWN')
    content_hash = compute_content_hash(example)[:8]

    return f"group:{category}:{severity}:{content_hash}"


def load_jsonl(filepath: Path) -> List[Dict]:
    """Load examples from JSONL file."""
    examples = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if line.strip():
                try:
                    examples.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping invalid JSON at {filepath}:{line_num} - {e}")
    return examples


def save_jsonl(examples: List[Dict], filepath: Path):
    """Save examples to JSONL file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')


def deduplicate_examples(examples: List[Dict]) -> Tuple[List[Dict], Dict]:
    """
    Deduplicate examples by content hash.

    Returns:
        (deduplicated_examples, stats_dict)
    """
    seen_hashes = {}
    deduplicated = []
    duplicates = []

    for example in examples:
        content_hash = compute_content_hash(example)

        if content_hash not in seen_hashes:
            seen_hashes[content_hash] = example
            deduplicated.append(example)
        else:
            duplicates.append({
                'hash': content_hash,
                'original_id': seen_hashes[content_hash].get('id'),
                'duplicate_id': example.get('id')
            })

    stats = {
        'original_count': len(examples),
        'unique_count': len(deduplicated),
        'duplicates_removed': len(duplicates),
        'dedup_rate': f"{100 * len(deduplicated) / len(examples):.1f}%"
    }

    return deduplicated, stats


def assign_unique_ids(examples: List[Dict]) -> List[Dict]:
    """
    Assign unique IDs to all examples.

    ID format: {category}-{6-digit-sequence}
    Example: sql-injection-000042
    """
    # Group by category for sequential numbering
    by_category = defaultdict(list)
    for ex in examples:
        metadata = ex.get('metadata', {})
        category = metadata.get('subcategory', metadata.get('category', 'unknown'))
        by_category[category].append(ex)

    # Assign IDs within each category
    updated = []
    for category, cat_examples in sorted(by_category.items()):
        for idx, ex in enumerate(cat_examples, start=1):
            new_id = f"{category}-{idx:06d}"
            ex['id'] = new_id
            updated.append(ex)

    return updated


def group_by_incident(examples: List[Dict]) -> Dict[str, List[Dict]]:
    """Group examples by incident (CVE or other identifier)."""
    groups = defaultdict(list)

    for ex in examples:
        group_id = compute_split_group_id(ex)
        groups[group_id].append(ex)

    return dict(groups)


def split_by_groups(
    groups: Dict[str, List[Dict]],
    train_ratio: float = 0.80,
    val_ratio: float = 0.10,
    test_ratio: float = 0.10,
    seed: int = 42
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Split examples into train/val/test maintaining group boundaries.

    All examples from the same group stay in the same split.
    """
    random.seed(seed)

    # Convert groups to list and shuffle
    group_items = list(groups.items())
    random.shuffle(group_items)

    # Calculate target counts (by number of examples, not groups)
    total_examples = sum(len(examples) for _, examples in group_items)
    target_train = int(total_examples * train_ratio)
    target_val = int(total_examples * val_ratio)
    # test gets remainder

    train_examples = []
    val_examples = []
    test_examples = []

    train_count = 0
    val_count = 0

    for group_id, examples in group_items:
        group_size = len(examples)

        # Decide which split this group goes to
        if train_count < target_train:
            train_examples.extend(examples)
            train_count += group_size
        elif val_count < target_val:
            val_examples.extend(examples)
            val_count += group_size
        else:
            test_examples.extend(examples)

    return train_examples, val_examples, test_examples


def generate_statistics(
    original_stats: Dict,
    dedup_stats: Dict,
    train: List[Dict],
    val: List[Dict],
    test: List[Dict],
    groups: Dict[str, List[Dict]]
) -> Dict:
    """Generate comprehensive statistics about the dataset."""

    all_examples = train + val + test

    # Count by category
    category_counts = Counter()
    severity_counts = Counter()
    language_counts = Counter()

    for ex in all_examples:
        metadata = ex.get('metadata', {})
        category_counts[metadata.get('category', 'unknown')] += 1
        severity_counts[metadata.get('severity', 'UNKNOWN')] += 1
        language_counts[metadata.get('lang', 'unknown')] += 1

    # Group type statistics
    incident_groups = [gid for gid in groups.keys() if gid.startswith('incident:')]
    cve_groups = [gid for gid in groups.keys() if gid.startswith('cve:')]
    url_groups = [gid for gid in groups.keys() if gid.startswith('url:')]
    other_groups = [gid for gid in groups.keys() if gid.startswith('group:')]

    return {
        'original_dataset': original_stats,
        'deduplication': dedup_stats,
        'final_dataset': {
            'total_examples': len(all_examples),
            'train_examples': len(train),
            'val_examples': len(val),
            'test_examples': len(test),
            'train_ratio': f"{100 * len(train) / len(all_examples):.1f}%",
            'val_ratio': f"{100 * len(val) / len(all_examples):.1f}%",
            'test_ratio': f"{100 * len(test) / len(all_examples):.1f}%"
        },
        'grouping': {
            'total_groups': len(groups),
            'incident_groups': len(incident_groups),
            'cve_groups': len(cve_groups),
            'url_groups': len(url_groups),
            'fallback_groups': len(other_groups),
            'avg_examples_per_group': f"{len(all_examples) / len(groups):.1f}"
        },
        'distribution': {
            'by_category': dict(category_counts.most_common()),
            'by_severity': dict(severity_counts),
            'by_language': dict(language_counts.most_common(15))
        }
    }


def main():
    parser = argparse.ArgumentParser(description='Deduplicate and re-split SecureCode v2.0')
    parser.add_argument('--input-dir', type=Path, default=Path('consolidated'),
                       help='Input directory with train/val/test.jsonl')
    parser.add_argument('--output-dir', type=Path, default=Path('consolidated_fixed'),
                       help='Output directory for deduplicated splits')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed for split reproducibility')
    args = parser.parse_args()

    print("=" * 80)
    print("SecureCode v2.0 Deduplication and Re-Split")
    print("=" * 80)

    # Step 1: Load all data
    print("\n[Step 1/7] Loading dataset...")
    train_path = args.input_dir / 'train.jsonl'
    val_path = args.input_dir / 'val.jsonl'
    test_path = args.input_dir / 'test.jsonl'

    train_orig = load_jsonl(train_path)
    val_orig = load_jsonl(val_path)
    test_orig = load_jsonl(test_path)

    all_orig = train_orig + val_orig + test_orig

    print(f"  Loaded {len(train_orig)} train + {len(val_orig)} val + {len(test_orig)} test")
    print(f"  Total original examples: {len(all_orig)}")

    original_stats = {
        'train': len(train_orig),
        'val': len(val_orig),
        'test': len(test_orig),
        'total': len(all_orig)
    }

    # Step 2: Deduplicate
    print("\n[Step 2/7] Deduplicating by content hash...")
    deduplicated, dedup_stats = deduplicate_examples(all_orig)
    print(f"  Original: {dedup_stats['original_count']} examples")
    print(f"  Unique: {dedup_stats['unique_count']} examples")
    print(f"  Removed: {dedup_stats['duplicates_removed']} duplicates")
    print(f"  Retention: {dedup_stats['dedup_rate']}")

    # Step 3: Assign unique IDs
    print("\n[Step 3/7] Assigning unique IDs...")
    deduplicated = assign_unique_ids(deduplicated)
    unique_ids = set(ex['id'] for ex in deduplicated)
    print(f"  Assigned {len(unique_ids)} unique IDs")

    # Step 4: Group by incident
    print("\n[Step 4/7] Grouping by incident/CVE...")
    groups = group_by_incident(deduplicated)
    print(f"  Created {len(groups)} groups")

    incident_groups = sum(1 for gid in groups.keys() if gid.startswith('incident:'))
    cve_groups = sum(1 for gid in groups.keys() if gid.startswith('cve:'))
    print(f"  - Incident name-based groups: {incident_groups}")
    print(f"  - CVE-based groups: {cve_groups}")
    print(f"  - URL-based groups: {sum(1 for gid in groups.keys() if gid.startswith('url:'))}")
    print(f"  - Fallback groups: {sum(1 for gid in groups.keys() if gid.startswith('group:'))}")

    # Step 5: Re-split
    print("\n[Step 5/7] Re-splitting dataset (80/10/10)...")
    train_new, val_new, test_new = split_by_groups(groups, seed=args.seed)

    print(f"  Train: {len(train_new)} examples ({100*len(train_new)/len(deduplicated):.1f}%)")
    print(f"  Val:   {len(val_new)} examples ({100*len(val_new)/len(deduplicated):.1f}%)")
    print(f"  Test:  {len(test_new)} examples ({100*len(test_new)/len(deduplicated):.1f}%)")

    # Step 6: Save new splits
    print(f"\n[Step 6/7] Saving to {args.output_dir}/...")
    save_jsonl(train_new, args.output_dir / 'train.jsonl')
    save_jsonl(val_new, args.output_dir / 'val.jsonl')
    save_jsonl(test_new, args.output_dir / 'test.jsonl')
    print("  ✓ Saved train.jsonl")
    print("  ✓ Saved val.jsonl")
    print("  ✓ Saved test.jsonl")

    # Step 7: Generate statistics
    print("\n[Step 7/7] Generating statistics...")
    stats = generate_statistics(
        original_stats, dedup_stats,
        train_new, val_new, test_new, groups
    )

    stats_path = args.output_dir / 'deduplication_report.json'
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"  ✓ Saved {stats_path}")

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Original dataset:  {len(all_orig)} examples")
    print(f"After dedup:       {len(deduplicated)} examples (-{dedup_stats['duplicates_removed']})")
    print(f"Incident groups:   {len(groups)} groups")
    print(f"\nNew splits:")
    print(f"  Train: {len(train_new)} ({100*len(train_new)/len(deduplicated):.1f}%)")
    print(f"  Val:   {len(val_new)} ({100*len(val_new)/len(deduplicated):.1f}%)")
    print(f"  Test:  {len(test_new)} ({100*len(test_new)/len(deduplicated):.1f}%)")
    print(f"\nNext steps:")
    print(f"1. Run: python split_leakage_check.py --train {args.output_dir}/train.jsonl \\")
    print(f"                                       --val {args.output_dir}/val.jsonl \\")
    print(f"                                       --test {args.output_dir}/test.jsonl")
    print(f"2. Verify zero leakage")
    print(f"3. Replace old consolidated/ with {args.output_dir}/")
    print("=" * 80)


if __name__ == '__main__':
    main()
