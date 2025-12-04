#!/usr/bin/env python3
"""
Convert generated JSONL files from ChatML format to SecureCode v2 schema format.

Fixes:
1. conversations: role/content -> turn/from/value
2. context: string -> structured object
3. Add validation object
4. Add created/validated to metadata
"""

import json
import sys
from pathlib import Path
from datetime import date


def parse_context_string(context_str):
    """Parse context string and extract structured information."""
    # Try to extract CVE
    cve = None
    import re
    cve_match = re.search(r'CVE-\d{4}-\d+', context_str)
    if cve_match:
        cve = cve_match.group(0)

    # Try to extract year (prefer 2022-2025)
    year_match = re.search(r'\b(202[2-5])\b', context_str)
    year = int(year_match.group(1)) if year_match else 2023

    # First sentence as incident name
    sentences = context_str.split('. ')
    incident = sentences[0] if sentences else context_str[:100]

    # Try to extract dollar amounts or record counts
    impact_matches = re.findall(r'(\$[\d.]+[BMK]|\d+[M+]?\s+(?:organizations|records|users))', context_str)
    impact = ', '.join(impact_matches[:2]) if impact_matches else "Significant security breach"

    # Extract attack vector (usually mentions specific technique)
    attack_vector = "Command/SQL injection vulnerability"
    if "injection" in context_str.lower():
        if "command" in context_str.lower():
            attack_vector = "Command injection through unsanitized user input"
        elif "sql" in context_str.lower():
            attack_vector = "SQL injection via crafted input"
        elif "nosql" in context_str.lower():
            attack_vector = "NoSQL injection through query manipulation"

    return {
        "real_world_incident": incident,
        "impact": impact,
        "attack_vector": attack_vector,
        "cve": cve,
        "year": year
    }


def convert_conversations(conversations):
    """Convert ChatML format to schema format."""
    converted = []
    turn_num = 1

    for conv in conversations:
        role = conv.get('role', conv.get('from', ''))
        content = conv.get('content', conv.get('value', ''))

        # Map role to from field
        from_field = "human" if role in ["user", "human"] else "assistant"

        converted.append({
            "turn": turn_num,
            "from": from_field,
            "value": content
        })
        turn_num += 1

    return converted


def convert_example(example):
    """Convert a single example to schema format."""
    converted = {
        "id": example["id"],
        "metadata": example["metadata"].copy(),
        "conversations": []
    }

    # Add missing metadata fields
    if "created" not in converted["metadata"]:
        converted["metadata"]["created"] = str(date.today())
    if "validated" not in converted["metadata"]:
        converted["metadata"]["validated"] = False

    # Remove non-schema fields from metadata
    converted["metadata"].pop("technique", None)
    converted["metadata"].pop("tags", None)

    # Convert context
    if "context" in example:
        if isinstance(example["context"], str):
            converted["context"] = parse_context_string(example["context"])
        else:
            converted["context"] = example["context"]

    # Convert conversations
    converted["conversations"] = convert_conversations(example["conversations"])

    # Add validation object
    converted["validation"] = {
        "syntax_check": "not_tested",
        "security_review": "not_reviewed",
        "code_execution": "not_tested",
        "encoding_check": "not_tested",
        "duplication_check": "not_tested",
        "reviewed_by": "automated-generator",
        "review_date": str(date.today()),
        "issues": []
    }

    return converted


def convert_file(input_file, output_file=None):
    """Convert an entire JSONL file."""
    input_path = Path(input_file)

    if output_file is None:
        output_file = input_path.parent / f"{input_path.stem}_converted.jsonl"
    else:
        output_file = Path(output_file)

    if not input_path.exists():
        print(f"Error: {input_file} not found")
        return False

    print(f"Converting {input_path.name}...")

    examples = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                example = json.loads(line)
                converted = convert_example(example)
                examples.append(converted)
            except Exception as e:
                print(f"  Error on line {line_num}: {e}")
                return False

    # Write converted examples
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"  ✓ Converted {len(examples)} examples")
    print(f"  ✓ Output: {output_file}")

    return True


def main():
    data_dir = Path(__file__).parent.parent / "data"

    files_to_convert = [
        "sql_injection_batch_005.jsonl",
        "nosql_injection_batch_006.jsonl",
        "command_injection_batch_007.jsonl"
    ]

    print("SecureCode v2 - Format Converter")
    print("=" * 60)

    success_count = 0
    for filename in files_to_convert:
        input_file = data_dir / filename
        output_file = input_file  # Overwrite original

        # Backup original
        backup_file = data_dir / f"{input_file.stem}_backup.jsonl"
        if input_file.exists():
            import shutil
            shutil.copy(input_file, backup_file)
            print(f"Backup created: {backup_file.name}")

        if convert_file(input_file, output_file):
            success_count += 1
        print()

    print("=" * 60)
    print(f"Conversion complete: {success_count}/{len(files_to_convert)} files")

    if success_count == len(files_to_convert):
        print("\n✓ All files converted successfully")
        print("✓ Original files backed up with _backup suffix")
        print("\nNext step: Run validation with 'python3 validate_all_batches.py'")
    else:
        print("\n⚠ Some files failed to convert")
        sys.exit(1)


if __name__ == "__main__":
    main()
