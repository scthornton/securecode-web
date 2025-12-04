#!/usr/bin/env python3
"""
Fix SSTI examples missing secure implementation in turn 2
Per CONTRIBUTING.md: Turn 2 must include BOTH vulnerable AND secure implementations
"""

import json
from pathlib import Path

SSTI_FIXES = {
    'ssti-000001': {
        'insert_after': '**Result**: The third payload executes `id` command, returning user context.',
        'secure_addition': '''

---

**SECURE IMPLEMENTATION** (Whitelist Approach):

```python
from flask import Flask, request
import html

app = Flask(__name__)

# Predefined safe greetings (no template execution)
SAFE_GREETINGS = {
    'formal': 'Dear',
    'casual': 'Hi',
    'friendly': 'Hello',
    'professional': 'Greetings'
}

@app.route('/preview')
def preview_email():
    # Allowlist approach - no template rendering
    greeting_type = request.args.get('greeting', 'friendly')
    username = request.args.get('username', 'User')

    # Map to safe predefined greeting
    greeting = SAFE_GREETINGS.get(greeting_type, 'Hello')

    # Escape user input
    safe_username = html.escape(username)

    # Construct response without template engine
    return f'''
    {greeting} {safe_username},

    Thank you for your order!

    Best regards,
    The Team
    '''

if __name__ == '__main__':
    app.run(debug=True)
```

**Why This Is Secure**:
1. **No template rendering** - Plain string formatting only
2. **Allowlist of greetings** - User selects from predefined options
3. **HTML escaping** - All user input escaped before output
4. **No Jinja2 execution** - Removes the entire attack surface'''
    },

    'ssti-000006': {
        'insert_after': '**Result**: Remote code execution, file system access',
        'secure_addition': '''

---

**SECURE IMPLEMENTATION** (Template Files Only):

```python
from mako.lookup import TemplateLookup
from flask import Flask, request, abort
import html

app = Flask(__name__)

# Load templates from directory only (never from strings!)
lookup = TemplateLookup(
    directories=['./templates'],
    strict_undefined=True
)

ALLOWED_TEMPLATES = ['welcome', 'order', 'profile']

@app.route('/render')
def render_template():
    template_name = request.args.get('template', 'welcome')
    name = request.args.get('name', 'User')

    # Validate against allowlist
    if template_name not in ALLOWED_TEMPLATES:
        abort(400, 'Invalid template')

    # Load from file (safe)
    template = lookup.get_template(f'{template_name}.mako')

    # Render with escaped input
    result = template.render(name=html.escape(name))

    return result
```

**Why This Is Secure**:
1. **Template files only** - No user-provided template strings
2. **Allowlist validation** - Only approved templates can be rendered
3. **Strict undefined mode** - Catches undefined variables
4. **Input escaping** - All user data escaped before rendering'''
    },

    'ssti-000007': {
        'insert_after': '**Result**: RCE, file disclosure',
        'secure_addition': '''

---

**SECURE IMPLEMENTATION**:

```php
<?php
use Smarty\\Smarty;

$smarty = new Smarty();
$smarty->setTemplateDir('./templates/');
$smarty->setCompileDir('./templates_c/');

// Disable PHP execution in templates
$smarty->php_handling = Smarty::PHP_REMOVE;

// Allowlist of safe templates
$allowed = ['welcome.tpl', 'order.tpl', 'profile.tpl'];
$template = $_GET['template'] ?? 'welcome.tpl';

// Validate template name
if (!in_array($template, $allowed)) {
    die('Invalid template');
}

// Escape user input
$smarty->assign('name', htmlspecialchars($_GET['name'] ?? 'User'));

// Render file template (safe)
$smarty->display($template);
?>
```

**Why This Is Secure**:
1. **Template files only** - No `fetch('string:...')`
2. **PHP disabled** - `php_handling = PHP_REMOVE`
3. **Allowlist** - Only approved templates allowed
4. **Input escaping** - `htmlspecialchars()` on all user data'''
    },

    'ssti-000009': {
        'insert_after': '**Result**: RCE',
        'secure_addition': '''

---

**SECURE IMPLEMENTATION**:

```python
import tornado.template
import tornado.web
import html
from datetime import date

class SecureTemplateHandler(tornado.web.RequestHandler):
    ALLOWED_TEMPLATES = {
        'welcome': 'welcome.html',
        'order': 'order.html',
        'profile': 'profile.html'
    }

    def get(self):
        template_name = self.get_argument('template', 'welcome')
        name = self.get_argument('name', 'User')

        # Validate against allowlist
        if template_name not in self.ALLOWED_TEMPLATES:
            raise tornado.web.HTTPError(400, 'Invalid template')

        # Load from file (safe)
        loader = tornado.template.Loader("./templates")
        template = loader.load(self.ALLOWED_TEMPLATES[template_name])

        # Render with escaped data
        result = template.generate(
            name=html.escape(name),
            date=date.today().isoformat()
        )

        self.write(result)
```

**Why This Is Secure**:
1. **Template files only** - Never `Template(user_string)`
2. **Allowlist** - Only approved templates
3. **HTML escaping** - All user input escaped
4. **Loader-based** - Templates loaded from directory, not strings'''
    },

    'ssti-000010': {
        'insert_after': '**Result**: Information disclosure, config leakage',
        'secure_addition': '''

---

**SECURE IMPLEMENTATION**:

```go
package main

import (
    "html/template"
    "net/http"
    "path/filepath"
    "time"
)

var allowedTemplates = map[string]string{
    "welcome": "welcome.tmpl",
    "order":   "order.tmpl",
    "profile": "profile.tmpl",
}

func secureHandler(w http.ResponseWriter, r *http.Request) {
    templateName := r.URL.Query().Get("template")
    if templateName == "" {
        templateName = "welcome"
    }

    // Validate against allowlist
    templateFile, ok := allowedTemplates[templateName]
    if !ok {
        http.Error(w, "Invalid template", http.StatusBadRequest)
        return
    }

    // Load from file (safe)
    tmplPath := filepath.Join("templates", templateFile)
    tmpl, err := template.ParseFiles(tmplPath)
    if err != nil {
        http.Error(w, "Template error", http.StatusInternalServerError)
        return
    }

    // Provide only safe data
    data := struct {
        Name string
        Date string
    }{
        Name: template.HTMLEscapeString(r.URL.Query().Get("name")),
        Date: time.Now().Format("2006-01-02"),
    }

    tmpl.Execute(w, data)
}
```

**Why This Is Secure**:
1. **Template files only** - No user-provided template strings
2. **Allowlist** - Only approved templates
3. **Limited data structure** - Only Name and Date fields
4. **HTML escaping** - User input escaped before rendering'''
    }
}

def fix_ssti_example(example):
    """Add secure implementation to turn 2 if it's an SSTI example"""
    example_id = example.get('id', '')

    if example_id not in SSTI_FIXES:
        return False

    conversations = example.get('conversations', [])
    if len(conversations) < 2:
        return False

    turn_2_content = conversations[1].get('value', '')
    fix_config = SSTI_FIXES[example_id]

    # Check if already has secure implementation
    if 'SECURE IMPLEMENTATION' in turn_2_content:
        return False

    # Insert secure code after vulnerable code
    if fix_config['insert_after'] in turn_2_content:
        new_content = turn_2_content.replace(
            fix_config['insert_after'],
            fix_config['insert_after'] + fix_config['secure_addition']
        )
        conversations[1]['value'] = new_content
        return True

    return False

def process_file(file_path):
    """Process a single JSONL file"""
    print(f"\\nProcessing: {file_path.name}")

    examples = []
    fixed_count = 0

    with open(file_path) as f:
        for line in f:
            example = json.loads(line)
            was_fixed = fix_ssti_example(example)

            if was_fixed:
                fixed_count += 1
                print(f"  ✓ Fixed {example.get('id')}: Added secure implementation to turn 2")

            examples.append(example)

    # Write back
    with open(file_path, 'w') as f:
        for example in examples:
            f.write(json.dumps(example) + '\\n')

    print(f"  Fixed {fixed_count} SSTI examples")
    return fixed_count

def main():
    print("="*80)
    print("SSTI SECURE IMPLEMENTATION FIX")
    print("="*80)
    print("\\nAdding secure implementations to turn 2 of SSTI examples...\\n")

    total_fixed = 0

    # Process consolidated files
    consolidated_dir = Path(__file__).parent.parent.parent / 'consolidated'
    for split_file in ['train.jsonl', 'val.jsonl', 'test.jsonl']:
        split_path = consolidated_dir / split_file
        if split_path.exists():
            fixed = process_file(split_path)
            total_fixed += fixed

    # Process data files
    data_dir = Path(__file__).parent.parent.parent / 'data'
    batch_files = sorted(data_dir.glob('*_batch_*.jsonl'))

    for batch_file in batch_files:
        fixed = process_file(batch_file)
        total_fixed += fixed

    print("\\n" + "="*80)
    print(f"COMPLETE: Fixed {total_fixed} SSTI examples")
    print("="*80)

if __name__ == '__main__':
    main()
