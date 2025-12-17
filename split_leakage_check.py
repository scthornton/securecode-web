#!/usr/bin/env python3
"""
Split Leakage Detection for SecureCode v2.0

Verifies that train/val/test splits do not leak information through:
1. Same incident (CVE/source) appearing across splits
2. Near-duplicate examples crossing splits
3. High-similarity pairs between splits

This is a critical validation step before publication. Any leakage
means evaluation metrics will be inflated and unreliable.
"""

import json
import hashlib
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
import sys

# Optional: for near-duplicate detection
try:
    from datasketch import MinHash, MinHashLSH
    MINHASH_AVAILABLE = True
except ImportError:
    MINHASH_AVAILABLE = False
    print("Warning: datasketch not installed. Near-duplicate detection disabled.")
    print("Install with: pip install datasketch")


@dataclass
class LeakageReport:
    """Results of leakage analysis."""
    total_examples: int
    unique_groups: int
    train_groups: Set[str]
    val_groups: Set[str]
    test_groups: Set[str]
    leaked_groups: Set[str]
    near_duplicates: List[Dict]
    is_leak_free: bool


def compute_split_group_id(example: Dict) -> str:
    """
    Compute grouping key to prevent same incident across splits.

    Priority:
    1. CVE ID (if present) - highest signal
    2. Real world incident name + year (if no CVE)
    3. Content hash (fallback for synthetic examples)

    The goal is to ensure examples from the same security incident
    stay together in one split.
    """
    context = example.get('context', {})

    # Priority 1: CVE ID
    cve_id = context.get('cve')
    if cve_id and cve_id != 'null' and cve_id is not None:
        return f"cve:{cve_id}"

    # Priority 2: Real world incident + year
    incident = context.get('real_world_incident', '')
    year = str(context.get('year', ''))
    if incident and incident.strip():
        # Normalize incident name for matching
        normalized = incident.lower().strip()
        # Hash to prevent issues with special characters
        incident_hash = hashlib.sha256(normalized.encode()).hexdigest()[:16]
        return f"incident:{incident_hash}:{year}"

    # Priority 3: Content-based hash (fallback for synthetic)
    # Use category + technique + language as grouping
    metadata = example.get('metadata', {})
    category = metadata.get('category', '')
    subcategory = metadata.get('subcategory', '')
    technique = metadata.get('technique', '')
    lang = metadata.get('lang', '')

    content = f"{category}|{subcategory}|{technique}|{lang}"
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
    return f"synthetic:{content_hash}"


def load_split(filepath: Path) -> List[Dict]:
    """Load examples from JSONL file."""
    examples = []
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if line.strip():
                try:
                    examples.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON at {filepath}:{line_num}: {e}")
    return examples


def check_group_leakage(
    train: List[Dict],
    val: List[Dict],
    test: List[Dict]
) -> Dict:
    """
    Check if any split_group_id appears in multiple splits.
    Returns detailed breakdown of all overlaps.
    """

    def get_groups_with_ids(examples: List[Dict]) -> Dict[str, List[str]]:
        """Map group_id -> list of example IDs"""
        groups = defaultdict(list)
        for ex in examples:
            group_id = compute_split_group_id(ex)
            example_id = ex.get('id', 'unknown')
            groups[group_id].append(example_id)
        return dict(groups)

    train_groups = get_groups_with_ids(train)
    val_groups = get_groups_with_ids(val)
    test_groups = get_groups_with_ids(test)

    train_group_set = set(train_groups.keys())
    val_group_set = set(val_groups.keys())
    test_group_set = set(test_groups.keys())

    # Find overlaps
    train_val = train_group_set & val_group_set
    train_test = train_group_set & test_group_set
    val_test = val_group_set & test_group_set

    all_leaked = train_val | train_test | val_test

    # Create detailed leak info
    leak_details = []

    for group_id in all_leaked:
        detail = {
            'group_id': group_id,
            'in_train': group_id in train_group_set,
            'in_val': group_id in val_group_set,
            'in_test': group_id in test_group_set,
            'train_examples': train_groups.get(group_id, []),
            'val_examples': val_groups.get(group_id, []),
            'test_examples': test_groups.get(group_id, []),
        }

        # Count total affected examples
        detail['total_affected'] = (
            len(detail['train_examples']) +
            len(detail['val_examples']) +
            len(detail['test_examples'])
        )

        # Identify leak type
        if detail['in_train'] and detail['in_test']:
            detail['leak_type'] = 'train-test'
            detail['severity'] = 'CRITICAL'
        elif detail['in_train'] and detail['in_val']:
            detail['leak_type'] = 'train-val'
            detail['severity'] = 'HIGH'
        else:
            detail['leak_type'] = 'val-test'
            detail['severity'] = 'MEDIUM'

        leak_details.append(detail)

    # Sort by severity and total affected
    severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2}
    leak_details.sort(key=lambda x: (severity_order[x['severity']], -x['total_affected']))

    return {
        'train_groups': len(train_group_set),
        'val_groups': len(val_group_set),
        'test_groups': len(test_group_set),
        'train_val_overlap': list(train_val),
        'train_test_overlap': list(train_test),
        'val_test_overlap': list(val_test),
        'total_leaked_groups': len(all_leaked),
        'leaked_group_ids': list(all_leaked),
        'leak_details': leak_details,
        'is_leak_free': len(all_leaked) == 0,
        'train_group_mapping': train_groups,
        'val_group_mapping': val_groups,
        'test_group_mapping': test_groups,
    }


def get_example_text(example: Dict) -> str:
    """Extract text content for similarity comparison."""
    conv = example.get('conversations', [])
    texts = []
    for turn in conv:
        value = turn.get('value', turn.get('content', ''))
        texts.append(value)
    return ' '.join(texts)


def detect_near_duplicates(
    split1: List[Dict],
    split2: List[Dict],
    split1_name: str,
    split2_name: str,
    threshold: float = 0.8
) -> List[Dict]:
    """
    Detect near-duplicate examples between two splits using MinHash LSH.

    Near-duplicates can leak information even without exact CVE matches
    if the code patterns or explanations are too similar.
    """
    if not MINHASH_AVAILABLE:
        return []

    duplicates = []

    # Build MinHash for split1
    lsh = MinHashLSH(threshold=threshold, num_perm=128)
    split1_hashes = {}
    seen_ids = set()

    for i, ex in enumerate(split1):
        text = get_example_text(ex)
        if not text.strip():
            continue
        m = MinHash(num_perm=128)
        for word in text.lower().split():
            m.update(word.encode('utf8'))
        # Create unique key using index to avoid duplicates
        example_id = ex.get('id', f'{split1_name}_{i}')
        unique_key = f"{split1_name}_{i}_{example_id}"
        if unique_key in seen_ids:
            continue
        seen_ids.add(unique_key)
        split1_hashes[unique_key] = (m, example_id)
        lsh.insert(unique_key, m)

    # Query with split2
    for j, ex in enumerate(split2):
        text = get_example_text(ex)
        if not text.strip():
            continue
        m = MinHash(num_perm=128)
        for word in text.lower().split():
            m.update(word.encode('utf8'))

        example_id = ex.get('id', f'{split2_name}_{j}')

        # Find similar in split1
        results = lsh.query(m)
        for result in results:
            hash_data = split1_hashes.get(result)
            if hash_data is None:
                continue

            split1_hash, split1_id = hash_data

            # Compute actual Jaccard similarity
            similarity = m.jaccard(split1_hash)

            if similarity >= threshold:
                duplicates.append({
                    'split1_example': split1_id,
                    'split2_example': example_id,
                    'similarity': round(similarity, 4),
                    'splits': f"{split1_name}-{split2_name}",
                    'split1_name': split1_name,
                    'split2_name': split2_name,
                })

    return duplicates


def analyze_cve_distribution(train: List[Dict], val: List[Dict], test: List[Dict]) -> Dict:
    """
    Analyze CVE distribution across splits for detailed reporting.
    """
    def extract_cves(examples: List[Dict]) -> Dict[str, List[str]]:
        """Extract CVE -> example IDs mapping"""
        cve_map = defaultdict(list)
        for ex in examples:
            cve = ex.get('context', {}).get('cve')
            if cve and cve != 'null' and cve is not None:
                cve_map[cve].append(ex.get('id', 'unknown'))
        return dict(cve_map)

    train_cves = extract_cves(train)
    val_cves = extract_cves(val)
    test_cves = extract_cves(test)

    train_cve_set = set(train_cves.keys())
    val_cve_set = set(val_cves.keys())
    test_cve_set = set(test_cves.keys())

    # Find overlaps
    train_val_cves = train_cve_set & val_cve_set
    train_test_cves = train_cve_set & test_cve_set
    val_test_cves = val_cve_set & test_cve_set

    all_overlapping = train_val_cves | train_test_cves | val_test_cves

    # Create detailed CVE leak report
    cve_leak_details = []
    for cve in all_overlapping:
        detail = {
            'cve': cve,
            'train_examples': train_cves.get(cve, []),
            'val_examples': val_cves.get(cve, []),
            'test_examples': test_cves.get(cve, []),
            'train_count': len(train_cves.get(cve, [])),
            'val_count': len(val_cves.get(cve, [])),
            'test_count': len(test_cves.get(cve, [])),
        }

        if cve in train_test_cves:
            detail['leak_type'] = 'train-test'
            detail['severity'] = 'CRITICAL'
        elif cve in train_val_cves:
            detail['leak_type'] = 'train-val'
            detail['severity'] = 'HIGH'
        else:
            detail['leak_type'] = 'val-test'
            detail['severity'] = 'MEDIUM'

        cve_leak_details.append(detail)

    # Sort by severity
    severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2}
    cve_leak_details.sort(key=lambda x: severity_order[x['severity']])

    return {
        'train_unique_cves': len(train_cve_set),
        'val_unique_cves': len(val_cve_set),
        'test_unique_cves': len(test_cve_set),
        'train_val_overlap_count': len(train_val_cves),
        'train_test_overlap_count': len(train_test_cves),
        'val_test_overlap_count': len(val_test_cves),
        'total_overlapping_cves': len(all_overlapping),
        'overlapping_cves': list(all_overlapping),
        'cve_leak_details': cve_leak_details,
        'is_cve_leak_free': len(all_overlapping) == 0,
    }


def analyze_incident_distribution(train: List[Dict], val: List[Dict], test: List[Dict]) -> Dict:
    """
    Analyze real-world incident distribution across splits.
    """
    def extract_incidents(examples: List[Dict]) -> Dict[str, List[str]]:
        """Extract incident -> example IDs mapping"""
        incident_map = defaultdict(list)
        for ex in examples:
            incident = ex.get('context', {}).get('real_world_incident', '')
            if incident and incident.strip():
                # Normalize
                normalized = incident.lower().strip()
                incident_map[normalized].append(ex.get('id', 'unknown'))
        return dict(incident_map)

    train_incidents = extract_incidents(train)
    val_incidents = extract_incidents(val)
    test_incidents = extract_incidents(test)

    train_set = set(train_incidents.keys())
    val_set = set(val_incidents.keys())
    test_set = set(test_incidents.keys())

    train_val = train_set & val_set
    train_test = train_set & test_set
    val_test = val_set & test_set

    all_overlapping = train_val | train_test | val_test

    return {
        'train_unique_incidents': len(train_set),
        'val_unique_incidents': len(val_set),
        'test_unique_incidents': len(test_set),
        'train_val_overlap_count': len(train_val),
        'train_test_overlap_count': len(train_test),
        'val_test_overlap_count': len(val_test),
        'total_overlapping_incidents': len(all_overlapping),
        'overlapping_incidents': list(all_overlapping)[:50],  # Limit for readability
        'is_incident_leak_free': len(all_overlapping) == 0,
    }


def generate_leakage_report(
    train_path: Path,
    val_path: Path,
    test_path: Path,
    output_path: Path
) -> Dict:
    """Generate comprehensive leakage report."""

    print("=" * 60)
    print("SecureCode v2.0 Split Leakage Analysis")
    print("=" * 60)
    print()

    print("Loading splits...")
    train = load_split(train_path)
    val = load_split(val_path)
    test = load_split(test_path)

    total = len(train) + len(val) + len(test)
    print(f"  Train: {len(train):,} examples")
    print(f"  Val:   {len(val):,} examples")
    print(f"  Test:  {len(test):,} examples")
    print(f"  Total: {total:,} examples")
    print()

    # Check group leakage
    print("Analyzing group leakage...")
    group_results = check_group_leakage(train, val, test)
    print(f"  Unique groups in train: {group_results['train_groups']}")
    print(f"  Unique groups in val:   {group_results['val_groups']}")
    print(f"  Unique groups in test:  {group_results['test_groups']}")
    print(f"  Leaked groups:          {group_results['total_leaked_groups']}")
    print()

    # Analyze CVE distribution
    print("Analyzing CVE distribution...")
    cve_results = analyze_cve_distribution(train, val, test)
    print(f"  Unique CVEs in train: {cve_results['train_unique_cves']}")
    print(f"  Unique CVEs in val:   {cve_results['val_unique_cves']}")
    print(f"  Unique CVEs in test:  {cve_results['test_unique_cves']}")
    print(f"  Train-Test CVE overlap: {cve_results['train_test_overlap_count']}")
    print(f"  Train-Val CVE overlap:  {cve_results['train_val_overlap_count']}")
    print(f"  Val-Test CVE overlap:   {cve_results['val_test_overlap_count']}")
    print()

    # Analyze incident distribution
    print("Analyzing incident distribution...")
    incident_results = analyze_incident_distribution(train, val, test)
    print(f"  Unique incidents in train: {incident_results['train_unique_incidents']}")
    print(f"  Unique incidents in val:   {incident_results['val_unique_incidents']}")
    print(f"  Unique incidents in test:  {incident_results['test_unique_incidents']}")
    print(f"  Train-Test incident overlap: {incident_results['train_test_overlap_count']}")
    print()

    # Check near-duplicates (if available)
    near_dupes = []
    if MINHASH_AVAILABLE:
        print("Checking near-duplicates (this may take a few minutes)...")
        print("  Checking train-test pairs...")
        near_dupes.extend(detect_near_duplicates(train, test, 'train', 'test'))
        print(f"    Found {len([d for d in near_dupes if d['splits'] == 'train-test'])} pairs")

        print("  Checking train-val pairs...")
        train_val_dupes = detect_near_duplicates(train, val, 'train', 'val')
        near_dupes.extend(train_val_dupes)
        print(f"    Found {len(train_val_dupes)} pairs")

        print("  Checking val-test pairs...")
        val_test_dupes = detect_near_duplicates(val, test, 'val', 'test')
        near_dupes.extend(val_test_dupes)
        print(f"    Found {len(val_test_dupes)} pairs")
    else:
        print("Skipping near-duplicate detection (datasketch not installed)")
    print()

    # Determine overall status
    is_leak_free = (
        group_results['is_leak_free'] and
        cve_results['is_cve_leak_free'] and
        len(near_dupes) == 0
    )

    # Generate recommendations
    recommendations = []

    if cve_results['train_test_overlap_count'] > 0:
        recommendations.append({
            'priority': 'CRITICAL',
            'issue': f"{cve_results['train_test_overlap_count']} CVEs appear in both train and test",
            'action': "Re-split dataset ensuring same CVE stays in one split only. Group examples by CVE before splitting.",
            'affected_count': cve_results['train_test_overlap_count']
        })

    if cve_results['train_val_overlap_count'] > 0:
        recommendations.append({
            'priority': 'HIGH',
            'issue': f"{cve_results['train_val_overlap_count']} CVEs appear in both train and validation",
            'action': "Re-split ensuring CVE grouping. This affects hyperparameter tuning reliability.",
            'affected_count': cve_results['train_val_overlap_count']
        })

    if cve_results['val_test_overlap_count'] > 0:
        recommendations.append({
            'priority': 'MEDIUM',
            'issue': f"{cve_results['val_test_overlap_count']} CVEs appear in both val and test",
            'action': "Re-split ensuring CVE grouping for clean evaluation.",
            'affected_count': cve_results['val_test_overlap_count']
        })

    if near_dupes:
        train_test_dupes = [d for d in near_dupes if d['splits'] == 'train-test']
        if train_test_dupes:
            recommendations.append({
                'priority': 'HIGH',
                'issue': f"{len(train_test_dupes)} near-duplicate pairs between train and test",
                'action': "Review these pairs and consolidate or separate. May indicate examples derived from same source.",
                'affected_count': len(train_test_dupes)
            })

    if is_leak_free:
        recommendations.append({
            'priority': 'INFO',
            'issue': 'No leakage detected',
            'action': 'Dataset splits are ready for publication.',
            'affected_count': 0
        })

    # Generate report
    report = {
        'metadata': {
            'generated_at': datetime.utcnow().isoformat(),
            'tool_version': '1.0.0',
            'dataset': 'SecureCode v2.0',
            'minhash_available': MINHASH_AVAILABLE,
            'near_duplicate_threshold': 0.8 if MINHASH_AVAILABLE else None,
        },
        'summary': {
            'total_examples': total,
            'train_examples': len(train),
            'val_examples': len(val),
            'test_examples': len(test),
            'is_leak_free': is_leak_free,
            'total_issues': len([r for r in recommendations if r['priority'] != 'INFO']),
            'critical_issues': len([r for r in recommendations if r['priority'] == 'CRITICAL']),
            'high_issues': len([r for r in recommendations if r['priority'] == 'HIGH']),
        },
        'group_leakage': {
            'train_groups': group_results['train_groups'],
            'val_groups': group_results['val_groups'],
            'test_groups': group_results['test_groups'],
            'train_val_overlap': len(group_results['train_val_overlap']),
            'train_test_overlap': len(group_results['train_test_overlap']),
            'val_test_overlap': len(group_results['val_test_overlap']),
            'total_leaked_groups': group_results['total_leaked_groups'],
            'is_leak_free': group_results['is_leak_free'],
        },
        'cve_analysis': cve_results,
        'incident_analysis': incident_results,
        'near_duplicates': {
            'enabled': MINHASH_AVAILABLE,
            'threshold': 0.8,
            'total_pairs': len(near_dupes),
            'train_test_pairs': len([d for d in near_dupes if d['splits'] == 'train-test']),
            'train_val_pairs': len([d for d in near_dupes if d['splits'] == 'train-val']),
            'val_test_pairs': len([d for d in near_dupes if d['splits'] == 'val-test']),
            'pairs': near_dupes[:100],  # Limit for readability
        },
        'recommendations': recommendations,
    }

    # Save report
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print()

    if is_leak_free:
        print("  STATUS: PASS - No leakage detected")
    else:
        print("  STATUS: FAIL - Leakage detected")
        print()
        print("  Critical Issues:")
        for rec in recommendations:
            if rec['priority'] == 'CRITICAL':
                print(f"    - {rec['issue']}")
        print()
        print("  High Priority Issues:")
        for rec in recommendations:
            if rec['priority'] == 'HIGH':
                print(f"    - {rec['issue']}")

    print()
    print(f"Full report saved to: {output_path}")
    print()

    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Detect data leakage in SecureCode v2.0 train/val/test splits"
    )
    parser.add_argument('--train', type=Path, required=True,
                        help='Path to train.jsonl')
    parser.add_argument('--val', type=Path, required=True,
                        help='Path to val.jsonl')
    parser.add_argument('--test', type=Path, required=True,
                        help='Path to test.jsonl')
    parser.add_argument('--output', type=Path, default=Path('split_leakage_report.json'),
                        help='Output path for JSON report')
    args = parser.parse_args()

    report = generate_leakage_report(args.train, args.val, args.test, args.output)

    # Exit with error code if leakage detected
    if not report['summary']['is_leak_free']:
        sys.exit(1)
