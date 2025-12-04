
import json
import random

def select_examples_for_validation(file_path, num_examples_per_lang=1):
    """
    Selects a specified number of examples for each of the top 10 languages.

    Args:
        file_path (str): The path to the JSONL file.
        num_examples_per_lang (int): The number of examples to select per language.

    Returns:
        list: A list of selected examples.
    """
    examples_by_lang = {}
    with open(file_path, 'r') as f:
        for line in f:
            example = json.loads(line)
            lang = example.get('metadata', {}).get('lang')
            if lang:
                if lang not in examples_by_lang:
                    examples_by_lang[lang] = []
                examples_by_lang[lang].append(example)

    # Get the top 10 languages by number of examples
    top_10_langs = sorted(examples_by_lang, key=lambda lang: len(examples_by_lang[lang]), reverse=True)[:10]

    selected_examples = []
    for lang in top_10_langs:
        selected_examples.extend(random.sample(examples_by_lang[lang], min(num_examples_per_lang, len(examples_by_lang[lang]))))

    return selected_examples

if __name__ == "__main__":
    selected = select_examples_for_validation("v2/consolidated/train.jsonl")
    print(json.dumps(selected, indent=4))
