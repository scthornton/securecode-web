
import json
from collections import Counter

def analyze_coverage(file_paths):
    """
    Analyzes the coverage of the dataset based on the JSONL files.

    Args:
        file_paths (list): A list of paths to the JSONL files.

    Returns:
        dict: A dictionary containing the coverage analysis results.
    """
    examples = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            for line in f:
                examples.append(json.loads(line))

    total_examples = len(examples)

    # OWASP Coverage
    owasp_coverage = Counter(item['metadata']['owasp_2021'] for item in examples if item.get('metadata', {}).get('owasp_2021'))
    owasp_distribution = {k: (v / total_examples) * 100 for k, v in owasp_coverage.items()}

    # Language Distribution
    language_coverage = Counter(item['metadata']['lang'] for item in examples if item.get('metadata', {}).get('lang'))
    language_distribution = {k: (v / total_examples) * 100 for k, v in language_coverage.items()}

    # Severity Distribution
    severity_coverage = Counter(item['metadata']['severity'] for item in examples if item.get('metadata', {}).get('severity'))
    severity_distribution = {k: (v / total_examples) * 100 for k, v in severity_coverage.items()}

    # Technique Diversity
    unique_techniques = len(set(item['metadata']['technique'] for item in examples if item.get('metadata', {}).get('technique')))

    # Real-World Incidents
    examples_with_incidents = sum(1 for item in examples if item.get('context', {}).get('real_world_incident'))
    incident_coverage = (examples_with_incidents / total_examples) * 100 if total_examples > 0 else 0

    return {
        "total_examples": total_examples,
        "owasp_distribution": owasp_distribution,
        "language_distribution": language_distribution,
        "severity_distribution": severity_distribution,
        "unique_techniques": unique_techniques,
        "incident_coverage": incident_coverage,
    }

if __name__ == "__main__":
    file_paths = [
        "v2/consolidated/train.jsonl",
        "v2/consolidated/val.jsonl",
        "v2/consolidated/test.jsonl"
    ]
    results = analyze_coverage(file_paths)
    print(json.dumps(results, indent=4))
