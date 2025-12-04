
import json
import random

def assess_data_quality(file_path, num_samples):
    """
    Assesses the data quality of a JSONL file by sampling and checking examples.

    Args:
        file_path (str): The path to the JSONL file.
        num_samples (int): The number of examples to sample.

    Returns:
        dict: A dictionary containing the assessment results.
    """
    perfect_examples = 0
    issue_counts = {
        "structural_validity": 0,
        "code_quality": 0,
        "security_accuracy": 0,
        "real_world_context": 0,
        "completeness": 0,
        "production_readiness": 0,
    }
    issues_found = []

    with open(file_path, 'r') as f:
        lines = f.readlines()

    if len(lines) < num_samples:
        print(f"Warning: Number of lines in file ({len(lines)}) is less than num_samples ({num_samples}).")
        num_samples = len(lines)

    sampled_lines = random.sample(lines, num_samples)

    for i, line in enumerate(sampled_lines):
        try:
            example = json.loads(line)
            is_perfect = True

            # 1. Structural Validity
            if not isinstance(example.get('conversations'), list) or len(example.get('conversations', [])) != 4:
                issue_counts["structural_validity"] += 1
                issues_found.append({"example_id": example.get('id'), "issue": "Structural Validity", "details": "Incorrect number of conversations or format."})
                is_perfect = False

            # 2. Code Quality (simple check for now)
            for conv in example.get('conversations', []):
                if "```" in conv.get('value', ''):
                    # This is a very basic check. A more advanced check would involve linters.
                    pass # Placeholder for more advanced check

            # 3. Security Accuracy
            if not example.get('metadata', {}).get('cwe'):
                issue_counts["security_accuracy"] += 1
                issues_found.append({"example_id": example.get('id'), "issue": "Security Accuracy", "details": "Missing CWE."})
                is_perfect = False

            # 4. Real-World Context
            if not example.get('context', {}).get('real_world_incident'):
                issue_counts["real_world_context"] += 1
                issues_found.append({"example_id": example.get('id'), "issue": "Real-World Context", "details": "Missing real-world incident."})
                is_perfect = False

            # 5. Completeness
            turns = {conv.get('turn') for conv in example.get('conversations', [])}
            if len(turns) != 4:
                issue_counts["completeness"] += 1
                issues_found.append({"example_id": example.get('id'), "issue": "Completeness", "details": "Missing one or more conversation turns."})
                is_perfect = False


            # 6. Production Readiness (simple check for now)
            if example.get('conversations') and "PRODUCTION PATTERN" not in example['conversations'][3].get('value',''):
                issue_counts["production_readiness"] += 1
                issues_found.append({"example_id": example.get('id'), "issue": "Production Readiness", "details": "Missing 'PRODUCTION PATTERN' in the final turn."})
                is_perfect = False

            if is_perfect:
                perfect_examples += 1

        except json.JSONDecodeError:
            issue_counts["structural_validity"] += 1
            issues_found.append({"example_id": f"sample_{i}", "issue": "Structural Validity", "details": "JSONDecodeError"})


    quality_score = (perfect_examples / num_samples) * 100 if num_samples > 0 else 0

    return {
        "num_samples": num_samples,
        "perfect_examples": perfect_examples,
        "quality_score": quality_score,
        "issue_counts": issue_counts,
        "issues_found": issues_found
    }

if __name__ == "__main__":
    results = assess_data_quality("v2/consolidated/train.jsonl", 60)
    print(json.dumps(results, indent=4))
