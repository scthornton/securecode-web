import json
import re
import subprocess
import tempfile
import os


def extract_code_blocks(text):
    """Extract code blocks from markdown text"""
    pattern = r'```(\w+)?\n(.*?)\n```'
    blocks = []
    for match in re.finditer(pattern, text, re.DOTALL):
        lang = match.group(1) or 'unknown'
        code = match.group(2)
        blocks.append((lang.lower(), code))
    return blocks


def validate_python(code):
    """Validate Python code syntax"""
    try:
        import ast
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)


def validate_javascript(code):
    """Validate JavaScript code"""
    try:
        import subprocess
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            f.flush()
            result = subprocess.run(['node', '--check', f.name],
                                    capture_output=True, text=True, timeout=10)
            os.unlink(f.name)
            return result.returncode == 0, result.stderr if result.stderr else None
    except Exception as e:
        return False, str(e)


def validate_java(code):
    """Validate Java code"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
            f.write(code)
            f.flush()
            result = subprocess.run(['javac', f.name],
                                    capture_output=True, text=True, timeout=10)
            os.unlink(f.name)
            return result.returncode == 0, result.stderr if result.stderr else None
    except Exception as e:
        return False, str(e)


def validate_go(code):
    """Validate Go code"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
            f.write(code)
            f.flush()
            result = subprocess.run(['go', 'build', f.name],
                                    capture_output=True, text=True, timeout=10)
            os.unlink(f.name)
            return result.returncode == 0, result.stderr if result.stderr else None
    except Exception as e:
        return False, str(e)


def validate_php(code):
    """Validate PHP code"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.php', delete=False) as f:
            f.write(code)
            f.flush()
            result = subprocess.run(['php', '-l', f.name],
                                    capture_output=True, text=True, timeout=10)
            os.unlink(f.name)
            return result.returncode == 0, result.stderr if result.stderr else None
    except Exception as e:
        return False, str(e)


def validate_csharp(code):
    """Validate C# code"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cs', delete=False) as f:
            f.write(code)
            f.flush()
            result = subprocess.run(['mcs', f.name],
                                    capture_output=True, text=True, timeout=10)
            os.unlink(f.name)
            return result.returncode == 0, result.stderr if result.stderr else None
    except Exception as e:
        return False, str(e)


def validate_rust(code):
    """Validate Rust code"""
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, 'main.rs'), 'w') as f:
                f.write(code)
            result = subprocess.run(['rustc', '--crate-type', 'lib', 'main.rs'],
                                    cwd=tmpdir, capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stderr if result.stderr else None
    except Exception as e:
        return False, str(e)


def validate_typescript(code):
    """Validate TypeScript code"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
            f.write(code)
            f.flush()
            result = subprocess.run(['tsc', '--noEmit', f.name],
                                    capture_output=True, text=True, timeout=10)
            os.unlink(f.name)
            return result.returncode == 0, result.stderr if result.stderr else None
    except Exception as e:
        return False, str(e)


def validate_ruby(code):
    """Validate Ruby code"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.rb', delete=False) as f:
            f.write(code)
            f.flush()
            result = subprocess.run(['ruby', '-c', f.name],
                                    capture_output=True, text=True, timeout=10)
            os.unlink(f.name)
            return result.returncode == 0, result.stderr if result.stderr else None
    except Exception as e:
        return False, str(e)


def validate_kotlin(code):
    """Validate Kotlin code"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.kt', delete=False) as f:
            f.write(code)
            f.flush()
            result = subprocess.run(['kotlinc', f.name],
                                    capture_output=True, text=True, timeout=10)
            os.unlink(f.name)
            return result.returncode == 0, result.stderr if result.stderr else None
    except Exception as e:
        return False, str(e)


VALIDATORS = {
    'python': validate_python,
    'javascript': validate_javascript,
    'java': validate_java,
    'go': validate_go,
    'php': validate_php,
    'csharp': validate_csharp,
    'rust': validate_rust,
    'typescript': validate_typescript,
    'ruby': validate_ruby,
    'kotlin': validate_kotlin
}


def validate_example(example):
    """Validate a single example"""
    results = {
        'id': example.get('id'),
        'lang': example.get('metadata', {}).get('lang'),
        'total_code_blocks': 0,
        'valid_blocks': 0,
        'invalid_blocks': 0,
        'errors': []
    }

    # Extract all text from conversations
    all_text = ''
    for conv in example.get('conversations', []):
        all_text += conv.get('value', '')

    code_blocks = extract_code_blocks(all_text)
    results['total_code_blocks'] = len(code_blocks)

    for lang, code in code_blocks:
        validator = VALIDATORS.get(lang)
        if validator:
            valid, error = validator(code)
            if valid:
                results['valid_blocks'] += 1
            else:
                results['invalid_blocks'] += 1
                results['errors'].append(f"{lang}: {error}")
        else:
            results['errors'].append(f"No validator for {lang}")

    return results


def main():
    with open('tech_validation_sample.jsonl', 'r') as f:
        examples = [json.loads(line) for line in f]

    all_results = []
    for example in examples:
        result = validate_example(example)
        all_results.append(result)

    # Summary
    total_blocks = sum(r['total_code_blocks'] for r in all_results)
    valid_blocks = sum(r['valid_blocks'] for r in all_results)
    invalid_blocks = sum(r['invalid_blocks'] for r in all_results)

    print(f"Technical Validation Results:")
    print(f"Total examples: {len(all_results)}")
    print(f"Total code blocks: {total_blocks}")
    print(f"Valid blocks: {valid_blocks}")
    print(f"Invalid blocks: {invalid_blocks}")
    print(
        f"Success rate: {valid_blocks/total_blocks*100:.1f}%" if total_blocks > 0 else "N/A")

    print("\nPer-example results:")
    for result in all_results:
        print(f"ID: {result['id']}, Lang: {result['lang']}, Blocks: {result['total_code_blocks']}, Valid: {result['valid_blocks']}, Errors: {len(result['errors'])}")

    # Show some errors
    all_errors = []
    for result in all_results:
        for error in result['errors']:
            all_errors.append(f"{result['id']}: {error}")

    if all_errors:
        print(f"\nFirst 10 errors:")
        for error in all_errors[:10]:
            print(f"  {error}")


if __name__ == "__main__":
    main()
