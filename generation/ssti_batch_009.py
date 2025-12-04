#!/usr/bin/env python3
"""
Batch 009: Server-Side Template Injection (SSTI) Part 1
Generates 10 SSTI examples across different template engines
"""

import json
from datetime import date
from pathlib import Path


def create_base_metadata(language, example_num, template_engine):
    """Create metadata for SSTI example."""
    return {
        "lang": language,
        "category": "injection",
        "subcategory": "template_injection",
        "template_engine": template_engine,
        "owasp_2021": "A03:2021-Injection",
        "cwe": "CWE-94",  # Improper Control of Generation of Code
        "severity": "CRITICAL",
        "complexity": "advanced",
        "created": str(date.today()),
        "validated": False
    }


def example_001_jinja2_basic():
    """Python/Jinja2 - Basic SSTI to RCE."""

    example_id = "ssti-000001"
    metadata = create_base_metadata("python", 1, "jinja2")

    context = {
        "real_world_incident": "2021 Jinja2 SSTI in GitLab",
        "impact": "RCE vulnerability, CVE-2021-22205, 13,000+ servers affected",
        "attack_vector": "Template injection via user-controlled template strings",
        "business_impact": "Complete server compromise, data exfiltration"
    }

    # Turn 1: Basic question
    human_turn_1 = """I'm building a Python Flask application that generates personalized email templates. Users can customize their email greetings. How should I implement this safely?"""

    assistant_turn_1 = """I'll show you the vulnerability in dynamic template rendering and how to fix it.

**VULNERABLE CODE** (Template Injection):

```python
from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

@app.route('/preview')
def preview_email():
    # DANGER: User input directly in template string
    username = request.args.get('username', 'User')
    greeting = request.args.get('greeting', 'Hello')

    # Vulnerable: Rendering user-controlled template
    template = f\"\"\"{greeting} {username},

    Thank you for your order!

    Best regards,
    The Team
    \"\"\"

    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True)
```

**Why This Is Vulnerable**:
1. `render_template_string()` with user input allows template injection
2. Jinja2 template syntax `{{...}}` executes Python code
3. Attacker can inject malicious template expressions

**Attack Example**:
```
GET /preview?greeting={{config}}&username=test
# Exposes Flask config including SECRET_KEY

GET /preview?greeting={{''.__class__.__mro__[1].__subclasses__()}}&username=test
# Lists all Python classes (path to RCE)

GET /preview?greeting={{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}&username=test
# Remote Code Execution - runs shell commands
```

**Result**: The third payload executes `id` command, returning user context."""

    # Turn 2: How to fix it
    human_turn_2 = """That's terrifying! How do I safely allow users to customize greetings without this vulnerability?"""

    assistant_turn_2 = """Use **predefined templates** with **safe variable substitution**:

**SECURE VERSION**:

```python
from flask import Flask, request, render_template, abort
import html

app = Flask(__name__)

# Define allowed greeting templates (allowlist)
GREETING_TEMPLATES = {
    'formal': 'Dear',
    'casual': 'Hi',
    'friendly': 'Hello',
    'professional': 'Greetings'
}

@app.route('/preview')
def preview_email():
    username = request.args.get('username', 'User')
    greeting_type = request.args.get('greeting', 'casual')

    # Validate greeting against allowlist
    if greeting_type not in GREETING_TEMPLATES:
        abort(400, "Invalid greeting type")

    # Escape username to prevent XSS
    safe_username = html.escape(username)
    safe_greeting = GREETING_TEMPLATES[greeting_type]

    # Use template file with safe variable passing
    return render_template('email_preview.html',
                         greeting=safe_greeting,
                         username=safe_username)

if __name__ == '__main__':
    app.run()
```

**Template File** (`templates/email_preview.html`):
```html
<!-- Jinja2 auto-escapes by default -->
<div class="email-preview">
    <p>{{ greeting }} {{ username }},</p>
    <p>Thank you for your order!</p>
    <p>Best regards,<br>The Team</p>
</div>
```

**Why This Is Secure**:
1. **Allowlist approach**: Only predefined greetings accepted
2. **Separate template files**: No dynamic template generation
3. **Variable passing**: Safe Jinja2 variable substitution (auto-escaped)
4. **Input escaping**: `html.escape()` for XSS protection
5. **No `render_template_string()`**: Avoids template injection vector"""

    # Turn 3: Advanced question
    human_turn_3 = """What if I absolutely need more flexibility? Can I safely render user templates in a sandbox?"""

    assistant_turn_3 = """Yes, but it requires **strict sandboxing**. Here's a production approach:

```python
from flask import Flask, request, abort
from jinja2 import Environment, meta, sandbox
import html
import re

app = Flask(__name__)

class SecureTemplateRenderer:
    def __init__(self):
        # Use SandboxedEnvironment
        self.env = sandbox.SandboxedEnvironment(
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Allowed variables only
        self.allowed_vars = {'username', 'order_id', 'date', 'amount'}

        # Maximum template complexity
        self.max_template_length = 500

    def validate_template(self, template_str):
        \"\"\"Validate template before rendering.\"\"\"
        if len(template_str) > self.max_template_length:
            raise ValueError("Template too long")

        # Parse AST to find variables
        try:
            ast = self.env.parse(template_str)
            variables = meta.find_undeclared_variables(ast)
        except Exception as e:
            raise ValueError(f"Invalid template syntax: {e}")

        # Check for disallowed variables
        disallowed = variables - self.allowed_vars
        if disallowed:
            raise ValueError(f"Disallowed variables: {disallowed}")

        # Block dangerous patterns
        dangerous = [
            r'__.*__',  # Dunder methods
            r'config',  # Flask config
            r'request',  # Request object
            r'import',  # Import statements
            r'eval',
            r'exec',
            r'open',
            r'file'
        ]

        for pattern in dangerous:
            if re.search(pattern, template_str, re.IGNORECASE):
                raise ValueError(f"Dangerous pattern detected: {pattern}")

        return True

    def render_safe(self, template_str, context):
        \"\"\"Safely render template with sandboxing.\"\"\"
        try:
            self.validate_template(template_str)
            template = self.env.from_string(template_str)

            # Provide only allowed context
            safe_context = {k: v for k, v in context.items()
                          if k in self.allowed_vars}

            return template.render(**safe_context)
        except Exception as e:
            return f"Template rendering error: {html.escape(str(e))}"

renderer = SecureTemplateRenderer()

@app.route('/custom-preview', methods=['POST'])
def custom_preview():
    template_str = request.form.get('template', '')

    context = {
        'username': html.escape(request.form.get('username', 'User')),
        'order_id': html.escape(request.form.get('order_id', '12345')),
        'date': date.today().strftime('%Y-%m-%d'),
        'amount': html.escape(request.form.get('amount', '0.00'))
    }

    result = renderer.render_safe(template_str, context)
    return result
```

**Security Layers**:
1. **`SandboxedEnvironment`**: Restricts dangerous operations
2. **Variable allowlist**: Only specific variables allowed
3. **AST parsing**: Validates template structure
4. **Pattern blocking**: Regex filters dangerous keywords
5. **Length limit**: Prevents complexity attacks
6. **Context filtering**: Only approved data passed to template
7. **Auto-escaping**: Enabled by default

**Limitations**:
- Still risky - sandbox escapes are possible
- Better to avoid user templates entirely if possible
- Requires constant security updates"""

    # Turn 4: Production patterns
    human_turn_4 = """What's the industry best practice for handling custom templates in production?"""

    assistant_turn_4 = """Best practice: **Avoid user-controlled templates entirely**. Use a **template builder UI** instead:

```python
from flask import Flask, request, jsonify
from dataclasses import dataclass, asdict
from typing import List, Dict
import html
import json

app = Flask(__name__)

@dataclass
class TemplateComponent:
    \"\"\"Structured template component.\"\"\"
    type: str  # 'text', 'variable', 'separator'
    content: str
    style: str = 'normal'

class TemplateBuilder:
    \"\"\"Visual template builder - no template strings.\"\"\"

    ALLOWED_VARIABLES = {
        'username': 'Customer name',
        'order_id': 'Order number',
        'order_date': 'Order date',
        'order_amount': 'Order total',
        'company_name': 'Your company name'
    }

    ALLOWED_STYLES = {'normal', 'bold', 'italic', 'heading'}

    def __init__(self):
        self.components: List[TemplateComponent] = []

    def add_text(self, text: str, style: str = 'normal'):
        \"\"\"Add static text component.\"\"\"
        if style not in self.ALLOWED_STYLES:
            raise ValueError(f"Invalid style: {style}")

        # Sanitize text
        safe_text = html.escape(text)

        self.components.append(
            TemplateComponent('text', safe_text, style)
        )

    def add_variable(self, var_name: str):
        \"\"\"Add variable placeholder.\"\"\"
        if var_name not in self.ALLOWED_VARIABLES:
            raise ValueError(f"Unknown variable: {var_name}")

        self.components.append(
            TemplateComponent('variable', var_name)
        )

    def add_separator(self):
        \"\"\"Add line separator.\"\"\"
        self.components.append(
            TemplateComponent('separator', '---')
        )

    def render(self, context: Dict[str, str]) -> str:
        \"\"\"Render template with context.\"\"\"
        output = []

        for component in self.components:
            if component.type == 'text':
                text = component.content
                if component.style == 'bold':
                    text = f\"<strong>{text}</strong>\"
                elif component.style == 'italic':
                    text = f\"<em>{text}</em>\"
                elif component.style == 'heading':
                    text = f\"<h2>{text}</h2>\"
                output.append(f\"<p>{text}</p>\")

            elif component.type == 'variable':
                value = context.get(component.content, '[MISSING]')
                output.append(f\"<p><strong>{html.escape(value)}</strong></p>\")

            elif component.type == 'separator':
                output.append(\"<hr>\")

        return '\\n'.join(output)

    def to_json(self) -> str:
        \"\"\"Serialize template structure.\"\"\"
        return json.dumps([asdict(c) for c in self.components])

    @classmethod
    def from_json(cls, json_str: str):
        \"\"\"Deserialize template structure.\"\"\"
        builder = cls()
        data = json.loads(json_str)
        for item in data:
            builder.components.append(
                TemplateComponent(**item)
            )
        return builder

@app.route('/template/build', methods=['POST'])
def build_template():
    \"\"\"Build template from structured components.\"\"\"
    try:
        builder = TemplateBuilder()

        # User provides structured data, not template code
        actions = request.json.get('actions', [])

        for action in actions:
            action_type = action.get('type')

            if action_type == 'add_text':
                builder.add_text(
                    action['text'],
                    action.get('style', 'normal')
                )
            elif action_type == 'add_variable':
                builder.add_variable(action['variable'])
            elif action_type == 'add_separator':
                builder.add_separator()

        # Save template structure (not code!)
        template_json = builder.to_json()

        return jsonify({
            'template_id': 'template_' + str(hash(template_json)),
            'preview': builder.render({
                'username': 'John Doe',
                'order_id': '12345',
                'order_date': '2025-01-15',
                'order_amount': '$99.99',
                'company_name': 'Acme Corp'
            })
        })

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/template/render/<template_id>', methods=['POST'])
def render_template_by_id(template_id):
    \"\"\"Render saved template with real data.\"\"\"
    # Load template structure from database
    template_json = load_template_from_db(template_id)

    builder = TemplateBuilder.from_json(template_json)

    context = request.json.get('context', {})
    rendered = builder.render(context)

    return rendered

def load_template_from_db(template_id):
    # Placeholder - load from database
    return '[{\"type\": \"text\", \"content\": \"Hello\", \"style\": \"normal\"}]'
```

**Why This Approach Is Secure**:
1. **No template strings**: Users never write template code
2. **Structured data**: JSON-based component system
3. **Type safety**: Dataclasses enforce structure
4. **Allowlist everything**: Variables, styles, components
5. **Safe serialization**: Store structure, not code
6. **HTML escaping**: Applied during render
7. **Visual builder UI**: Drag-and-drop interface for users

**Frontend Integration**:
```javascript
// React/Vue template builder UI
const actions = [
  { type: 'add_text', text: 'Hello', style: 'heading' },
  { type: 'add_variable', variable: 'username' },
  { type: 'add_separator' },
  { type: 'add_text', text: 'Thank you for your order!' }
];

fetch('/template/build', {
  method: 'POST',
  body: JSON.stringify({ actions }),
  headers: { 'Content-Type': 'application/json' }
});
```

**Key Principle**: **Never let users write code**. Give them a visual builder that generates structured data instead."""

    conversations = [
        {"from": "human", "value": human_turn_1, "turn": 1},
        {"from": "assistant", "value": assistant_turn_1, "turn": 2},
        {"from": "human", "value": human_turn_2, "turn": 3},
        {"from": "assistant", "value": assistant_turn_3, "turn": 4},
    ]

    validation = {
        "syntax_check": "not_tested",
        "security_review": "not_reviewed",
        "code_execution": "not_tested",
        "encoding_check": "not_tested",
        "duplication_check": "not_tested",
        "reviewed_by": "automated-generator",
        "review_date": str(date.today()),
        "issues": []
    }

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": conversations,
        "validation": validation
    }


def example_002_twig():
    """PHP/Twig - Template sandbox escape."""

    example_id = "ssti-000002"
    metadata = create_base_metadata("php", 2, "twig")

    context = {
        "real_world_incident": "2019 Twig SSTI in Craft CMS",
        "impact": "CVE-2019-14235, RCE in popular CMS, thousands of sites affected",
        "attack_vector": "Twig filter chain exploitation",
        "business_impact": "Server compromise, website defacement"
    }

    human_turn_1 = """I'm using Twig templates in my PHP application. Users can customize notification messages. Is it safe to render user-provided template strings?"""

    assistant_turn_1 = """No! Rendering user-controlled Twig templates is extremely dangerous. Let me show you:

**VULNERABLE CODE**:

```php
<?php
require_once 'vendor/autoload.php';

use Twig\\Environment;
use Twig\\Loader\\ArrayLoader;

// DANGER: User input in template string
$userTemplate = $_GET['template'] ?? 'Hello {{ name }}!';
$name = $_GET['name'] ?? 'User';

$loader = new ArrayLoader([]);
$twig = new Environment($loader);

try {
    // Vulnerable: Rendering user-controlled template
    $template = $twig->createTemplate($userTemplate);
    echo $template->render(['name' => $name]);
} catch (Exception $e) {
    echo "Error: " . $e->getMessage();
}
```

**Why This Is Vulnerable**:
1. `createTemplate()` compiles and executes user input
2. Twig has powerful filters that can be chained
3. Even with sandbox, escapes are possible

**Attack Example**:
```php
// Exploit 1: Using _self to access Twig environment
?template={{_self.env.registerUndefinedFilterCallback('system')}}{{_self.env.getFilter('id')}}

// Exploit 2: Filter chain to get PHP functions
?template={{['id']|filter('system')}}

// Exploit 3: Using app global (if available)
?template={{app.request.server.all|join(',')}}
```

**Result**: Remote code execution, server information disclosure"""

    human_turn_2 = """How do I fix this? Can I use Twig's sandbox mode safely?"""

    assistant_turn_2 = """Twig's sandbox helps but isn't foolproof. Better approach: **predefined templates**:

**SECURE VERSION**:

```php
<?php
require_once 'vendor/autoload.php';

use Twig\\Environment;
use Twig\\Loader\\FilesystemLoader;

class SecureNotificationRenderer {
    private $twig;
    private $allowedTemplates = [
        'welcome' => 'templates/welcome.twig',
        'order_confirm' => 'templates/order_confirm.twig',
        'shipping' => 'templates/shipping.twig'
    ];

    public function __construct() {
        $loader = new FilesystemLoader('templates');
        $this->twig = new Environment($loader, [
            'autoescape' => 'html',
            'strict_variables' => true
        ]);
    }

    public function render($templateName, $data) {
        // Validate template name against allowlist
        if (!isset($this->allowedTemplates[$templateName])) {
            throw new InvalidArgumentException('Invalid template');
        }

        // Sanitize all user data
        $safeData = $this->sanitizeData($data);

        // Load template from file (not user string)
        $template = $this->twig->load(
            basename($this->allowedTemplates[$templateName])
        );

        return $template->render($safeData);
    }

    private function sanitizeData($data) {
        return array_map(function($value) {
            if (is_string($value)) {
                return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
            }
            return $value;
        }, $data);
    }
}

// Usage
$renderer = new SecureNotificationRenderer();

$templateName = $_GET['template'] ?? 'welcome';
$userName = $_GET['name'] ?? 'User';

try {
    echo $renderer->render($templateName, [
        'name' => $userName,
        'date' => date('Y-m-d')
    ]);
} catch (Exception $e) {
    echo "Error: Invalid template";
}
```

**Template File** (`templates/welcome.twig`):
```twig
{# Twig auto-escapes by default #}
<div class="notification">
    <h2>Welcome {{ name }}!</h2>
    <p>Your account was created on {{ date }}.</p>
</div>
```

**Why This Is Secure**:
1. **Template files only**: No `createTemplate()` with user input
2. **Allowlist**: Only predefined templates can be loaded
3. **Auto-escaping**: HTML entities escaped automatically
4. **Input sanitization**: Extra layer of protection
5. **Strict variables**: Undefined variables cause errors"""

    human_turn_3 = """What if I really need to use Twig's sandbox for user templates?"""

    assistant_turn_3 = """If you absolutely must, here's a heavily restricted sandbox approach:

```php
<?php
require_once 'vendor/autoload.php';

use Twig\\Environment;
use Twig\\Loader\\ArrayLoader;
use Twig\\Extension\\SandboxExtension;
use Twig\\Sandbox\\SecurityPolicy;

class RestrictedTwigRenderer {
    private $twig;
    private $maxTemplateLength = 500;

    public function __construct() {
        $loader = new ArrayLoader([]);

        // Define security policy
        $tags = ['if', 'for'];  // Only allow these tags
        $filters = ['escape', 'upper', 'lower', 'date'];  // Safe filters only
        $methods = [];  // No method calls allowed
        $properties = [];  // No property access allowed
        $functions = [];  // No functions allowed

        $policy = new SecurityPolicy($tags, $filters, $methods, $properties, $functions);
        $sandbox = new SandboxExtension($policy, true);  // Sandboxed by default

        $this->twig = new Environment($loader, [
            'autoescape' => 'html',
            'strict_variables' => true
        ]);

        $this->twig->addExtension($sandbox);
    }

    public function validateTemplate($templateStr) {
        // Length check
        if (strlen($templateStr) > $this->maxTemplateLength) {
            throw new InvalidArgumentException('Template too long');
        }

        // Block dangerous patterns
        $dangerous = [
            '/_self/',
            '/_context/',
            '/\\bapp\\b/',
            '/\\benv\\b/',
            '/registerUndefined/',
            '/system/',
            '/exec/',
            '/passthru/',
            '/shell_exec/',
            '/popen/',
            '/proc_open/'
        ];

        foreach ($dangerous as $pattern) {
            if (preg_match($pattern, $templateStr)) {
                throw new SecurityException('Dangerous pattern detected');
            }
        }

        return true;
    }

    public function renderSafe($templateStr, $context) {
        try {
            $this->validateTemplate($templateStr);

            // Only allow specific context variables
            $allowedVars = ['name', 'email', 'date', 'order_id'];
            $safeContext = array_intersect_key($context,
                array_flip($allowedVars));

            $template = $this->twig->createTemplate($templateStr);
            return $template->render($safeContext);

        } catch (Exception $e) {
            return 'Template error: ' . htmlspecialchars($e->getMessage());
        }
    }
}

// Usage
$renderer = new RestrictedTwigRenderer();

$userTemplate = $_POST['template'] ?? 'Hello {{ name }}!';
$context = [
    'name' => htmlspecialchars($_POST['name'] ?? 'User'),
    'email' => htmlspecialchars($_POST['email'] ?? 'user@example.com'),
    'date' => date('Y-m-d'),
    'order_id' => htmlspecialchars($_POST['order_id'] ?? '12345')
];

echo $renderer->renderSafe($userTemplate, $context);
```

**Security Layers**:
1. **Sandbox extension**: Restricts available tags/filters
2. **No dangerous filters**: Only safe transformations allowed
3. **No method/property access**: Blocks object exploitation
4. **Pattern blacklist**: Regex blocks known exploits
5. **Variable allowlist**: Only approved data in context
6. **Length limit**: Prevents DoS
7. **Auto-escaping**: XSS protection

**Warning**: Sandbox bypasses are discovered regularly. Avoid if possible."""

    human_turn_4 = """What's the production-grade alternative to user templates?"""

    assistant_turn_4 = """Use a **structured template builder** instead of raw Twig strings:

```php
<?php
class TemplateBuilder {
    private $components = [];

    const ALLOWED_VARS = ['name', 'email', 'order_id', 'date', 'amount'];
    const ALLOWED_STYLES = ['normal', 'bold', 'italic', 'heading'];

    public function addText($text, $style = 'normal') {
        if (!in_array($style, self::ALLOWED_STYLES)) {
            throw new InvalidArgumentException('Invalid style');
        }

        $this->components[] = [
            'type' => 'text',
            'content' => htmlspecialchars($text, ENT_QUOTES, 'UTF-8'),
            'style' => $style
        ];

        return $this;
    }

    public function addVariable($varName) {
        if (!in_array($varName, self::ALLOWED_VARS)) {
            throw new InvalidArgumentException('Invalid variable');
        }

        $this->components[] = [
            'type' => 'variable',
            'name' => $varName
        ];

        return $this;
    }

    public function addSeparator() {
        $this->components[] = ['type' => 'separator'];
        return $this;
    }

    public function render($context) {
        $output = '<div class="email-template">';

        foreach ($this->components as $component) {
            switch ($component['type']) {
                case 'text':
                    $text = $component['content'];
                    if ($component['style'] === 'bold') {
                        $text = '<strong>' . $text . '</strong>';
                    } elseif ($component['style'] === 'italic') {
                        $text = '<em>' . $text . '</em>';
                    } elseif ($component['style'] === 'heading') {
                        $text = '<h2>' . $text . '</h2>';
                    }
                    $output .= '<p>' . $text . '</p>';
                    break;

                case 'variable':
                    $value = $context[$component['name']] ?? '[MISSING]';
                    $output .= '<p><strong>' . htmlspecialchars($value) . '</strong></p>';
                    break;

                case 'separator':
                    $output .= '<hr>';
                    break;
            }
        }

        $output .= '</div>';
        return $output;
    }

    public function toJson() {
        return json_encode($this->components);
    }

    public static function fromJson($json) {
        $builder = new self();
        $data = json_decode($json, true);

        foreach ($data as $component) {
            $builder->components[] = $component;
        }

        return $builder;
    }
}

// API endpoint for building templates
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $actions = json_decode(file_get_contents('php://input'), true)['actions'] ?? [];

    try {
        $builder = new TemplateBuilder();

        foreach ($actions as $action) {
            switch ($action['type']) {
                case 'add_text':
                    $builder->addText($action['text'], $action['style'] ?? 'normal');
                    break;
                case 'add_variable':
                    $builder->addVariable($action['variable']);
                    break;
                case 'add_separator':
                    $builder->addSeparator();
                    break;
            }
        }

        // Save structure to database (not code!)
        $templateJson = $builder->toJson();
        $templateId = 'tpl_' . md5($templateJson);

        // Store in database
        saveTemplate($templateId, $templateJson);

        // Return preview
        $preview = $builder->render([
            'name' => 'John Doe',
            'email' => 'john@example.com',
            'order_id' => '12345',
            'date' => date('Y-m-d'),
            'amount' => '$99.99'
        ]);

        echo json_encode([
            'template_id' => $templateId,
            'preview' => $preview
        ]);

    } catch (Exception $e) {
        http_response_code(400);
        echo json_encode(['error' => $e->getMessage()]);
    }
}

function saveTemplate($id, $json) {
    // Save to database
    // Example: MySQL prepared statement
    global $pdo;
    $stmt = $pdo->prepare('INSERT INTO templates (id, structure) VALUES (?, ?)');
    $stmt->execute([$id, $json]);
}
```

**Key Principle**: Users never write Twig code - they build templates visually using a drag-and-drop UI that generates structured JSON data."""

    conversations = [
        {"from": "human", "value": human_turn_1, "turn": 1},
        {"from": "assistant", "value": assistant_turn_1, "turn": 2},
        {"from": "human", "value": human_turn_2, "turn": 3},
        {"from": "assistant", "value": assistant_turn_2, "turn": 4},
    ]

    validation = {
        "syntax_check": "not_tested",
        "security_review": "not_reviewed",
        "code_execution": "not_tested",
        "encoding_check": "not_tested",
        "duplication_check": "not_tested",
        "reviewed_by": "automated-generator",
        "review_date": str(date.today()),
        "issues": []
    }

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": conversations,
        "validation": validation
    }


def example_003_freemarker():
    """Java/FreeMarker - ObjectConstructor exploitation."""

    example_id = "ssti-000003"
    metadata = create_base_metadata("java", 3, "freemarker")

    context = {
        "real_world_incident": "2022 FreeMarker RCE in Apache OFBiz",
        "impact": "CVE-2020-9496, Pre-auth RCE, used in enterprise ERP systems",
        "attack_vector": "ObjectConstructor builtin exploitation",
        "business_impact": "Complete system compromise, data theft"
    }

    human_turn_1 = """I'm using FreeMarker templates in my Java Spring application. Users can customize report layouts. Is it safe?"""

    assistant_turn_1 = """FreeMarker with user input is extremely dangerous. Here's why:

**VULNERABLE CODE**:

```java
import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateException;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.StringWriter;
import java.util.HashMap;
import java.util.Map;

@RestController
public class ReportController {

    @GetMapping("/report/preview")
    public String previewReport(HttpServletRequest request) throws IOException, TemplateException {
        // DANGER: User-controlled template string
        String templateString = request.getParameter("template");
        String username = request.getParameter("username");

        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);

        // Vulnerable: Creating template from user input
        Template template = new Template("preview", templateString, cfg);

        Map<String, Object> data = new HashMap<>();
        data.put("username", username);
        data.put("date", new java.util.Date());

        StringWriter writer = new StringWriter();
        template.process(data, writer);

        return writer.toString();
    }
}
```

**Why This Is Vulnerable**:
1. `new Template()` with user string compiles arbitrary code
2. FreeMarker has powerful built-ins like `?new` (ObjectConstructor)
3. Can instantiate arbitrary Java classes

**Attack Example**:
```freemarker
<#-- Exploit 1: Execute commands via Runtime -->
<#assign ex="freemarker.template.utility.Execute"?new()>
${ ex("id") }

<#-- Exploit 2: Read files via ObjectConstructor -->
<#assign classLoader=object?api.class.protectionDomain.classLoader>
<#assign clazz=classLoader.loadClass("java.io.File")>
<#assign constructor=clazz.getConstructor(classLoader.loadClass("java.lang.String"))>
<#assign file=constructor.newInstance("/etc/passwd")>

<#-- Exploit 3: JNDI injection -->
<#assign uri=object?api.class.getResource("/").toURI()>
<#assign input=uri?api.create("file:///etc/passwd").toURL().openConnection()>
<#assign is=input?api.getInputStream()>
```

**Result**: Remote code execution, file system access, server compromise"""

    human_turn_2 = """How do I prevent this? Can I configure FreeMarker securely?"""

    assistant_turn_2 = """Yes, with proper configuration. But better: **avoid user templates**:

**SECURE VERSION**:

```java
import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateException;
import freemarker.template.TemplateExceptionHandler;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.io.StringWriter;
import java.util.*;

@RestController
public class SecureReportController {

    private final Configuration freemarkerConfig;
    private final Set<String> allowedTemplates;

    public SecureReportController() {
        this.freemarkerConfig = new Configuration(Configuration.VERSION_2_3_31);

        // Configure to load templates from classpath only
        freemarkerConfig.setClassForTemplateLoading(this.getClass(), "/templates");

        // Security settings
        freemarkerConfig.setNewBuiltinClassResolver(
            TemplateClassResolver.ALLOWS_NOTHING_RESOLVER);  // Block ?new
        freemarkerConfig.setAPIBuiltinEnabled(false);  // Disable ?api
        freemarkerConfig.setLogTemplateExceptions(false);
        freemarkerConfig.setTemplateExceptionHandler(
            TemplateExceptionHandler.RETHROW_HANDLER);

        // Allowlist of templates
        this.allowedTemplates = Set.of(
            "sales_report.ftl",
            "inventory_report.ftl",
            "customer_report.ftl"
        );
    }

    @GetMapping("/report/preview")
    public String previewReport(@RequestParam String templateName,
                               @RequestParam String username) {
        try {
            // Validate against allowlist
            if (!allowedTemplates.contains(templateName)) {
                throw new IllegalArgumentException("Invalid template");
            }

            // Load template from file (not user string!)
            Template template = freemarkerConfig.getTemplate(templateName);

            // Prepare safe data model
            Map<String, Object> dataModel = new HashMap<>();
            dataModel.put("username", escapeHtml(username));
            dataModel.put("reportDate", new Date());
            dataModel.put("reportId", UUID.randomUUID().toString());

            StringWriter writer = new StringWriter();
            template.process(dataModel, writer);

            return writer.toString();

        } catch (IOException | TemplateException e) {
            return "Error generating report";
        }
    }

    private String escapeHtml(String input) {
        return input.replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;")
                   .replace("\"", "&quot;")
                   .replace("'", "&#x27;");
    }
}
```

**Template File** (`templates/sales_report.ftl`):
```freemarker
<#-- FreeMarker auto-escapes with proper config -->
<div class="report">
    <h1>Sales Report</h1>
    <p>Generated for: ${username}</p>
    <p>Date: ${reportDate?date}</p>
    <p>Report ID: ${reportId}</p>
</div>
```

**Why This Is Secure**:
1. **Template files only**: Load from classpath, not user strings
2. **Allowlist**: Only predefined templates accepted
3. **`ALLOWS_NOTHING_RESOLVER`**: Blocks `?new` builtin
4. **`APIBuiltinEnabled=false`**: Disables `?api`
5. **Input escaping**: Extra XSS protection
6. **No dynamic template creation**: No `new Template()` with user input"""

    human_turn_3 = """Can I safely allow limited template customization?"""

    assistant_turn_3 = """Only with extreme restrictions. Here's a hardened approach:

```java
import freemarker.core.TemplateClassResolver;
import freemarker.template.*;
import java.io.StringWriter;
import java.util.*;
import java.util.regex.*;

public class RestrictedFreemarkerRenderer {

    private final Configuration config;
    private final int maxTemplateLength = 1000;
    private final Pattern dangerousPattern;

    public RestrictedFreemarkerRenderer() {
        this.config = new Configuration(Configuration.VERSION_2_3_31);

        // Maximum security settings
        config.setNewBuiltinClassResolver(
            TemplateClassResolver.ALLOWS_NOTHING_RESOLVER);
        config.setAPIBuiltinEnabled(false);
        config.setLogTemplateExceptions(false);
        config.setTemplateExceptionHandler(
            TemplateExceptionHandler.RETHROW_HANDLER);

        // Compile dangerous pattern regex
        this.dangerousPattern = Pattern.compile(
            "\\?new|\\?api|\\?eval|<#import|<#include|freemarker\\.|java\\.|" +
            "Runtime|ProcessBuilder|ClassLoader|System\\.",
            Pattern.CASE_INSENSITIVE
        );
    }

    public void validateTemplate(String templateStr) throws SecurityException {
        if (templateStr == null || templateStr.trim().isEmpty()) {
            throw new SecurityException("Empty template");
        }

        if (templateStr.length() > maxTemplateLength) {
            throw new SecurityException("Template too long");
        }

        // Check for dangerous patterns
        if (dangerousPattern.matcher(templateStr).find()) {
            throw new SecurityException("Dangerous pattern detected");
        }

        // Only allow specific directives
        Set<String> allowedDirectives = Set.of("if", "list", "else", "elseif");
        Pattern directivePattern = Pattern.compile("<#(\\w+)");
        Matcher matcher = directivePattern.matcher(templateStr);

        while (matcher.find()) {
            String directive = matcher.group(1);
            if (!allowedDirectives.contains(directive)) {
                throw new SecurityException("Disallowed directive: " + directive);
            }
        }
    }

    public String renderSafe(String templateStr, Map<String, Object> userContext) {
        try {
            // Validate template
            validateTemplate(templateStr);

            // Create template
            Template template = new Template("safe", templateStr, config);

            // Provide only safe context variables
            Set<String> allowedVars = Set.of("username", "email", "date", "orderId");
            Map<String, Object> safeContext = new HashMap<>();

            for (String key : allowedVars) {
                if (userContext.containsKey(key)) {
                    Object value = userContext.get(key);
                    if (value instanceof String) {
                        safeContext.put(key, escapeHtml((String) value));
                    } else {
                        safeContext.put(key, value);
                    }
                }
            }

            StringWriter writer = new StringWriter();
            template.process(safeContext, writer);

            return writer.toString();

        } catch (Exception e) {
            return "Template error: " + escapeHtml(e.getMessage());
        }
    }

    private String escapeHtml(String input) {
        return input.replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;")
                   .replace("\"", "&quot;")
                   .replace("'", "&#x27;");
    }
}
```

**Security Layers**:
1. Blocks `?new`, `?api`, `?eval`
2. Pattern blacklist for dangerous keywords
3. Directive allowlist (only if, list, else)
4. Variable allowlist
5. Length limits
6. Input escaping

**Still Risky**: New bypasses discovered regularly. Avoid user templates."""

    human_turn_4 = """What's the production-safe alternative?"""

    assistant_turn_4 = """Use a **visual report builder** with structured data, not template strings:

```java
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;

public class ReportBuilder {

    public enum ComponentType { TEXT, VARIABLE, TABLE, SEPARATOR }
    public enum TextStyle { NORMAL, BOLD, ITALIC, HEADING }

    public static class Component {
        private ComponentType type;
        private String content;
        private TextStyle style;
        private List<String> columns;

        // Getters, setters, constructors
    }

    private List<Component> components = new ArrayList<>();
    private static final Set<String> ALLOWED_VARIABLES = Set.of(
        "username", "email", "orderId", "date", "amount"
    );

    public ReportBuilder addText(String text, TextStyle style) {
        Component comp = new Component();
        comp.setType(ComponentType.TEXT);
        comp.setContent(escapeHtml(text));
        comp.setStyle(style);
        components.add(comp);
        return this;
    }

    public ReportBuilder addVariable(String varName) {
        if (!ALLOWED_VARIABLES.contains(varName)) {
            throw new IllegalArgumentException("Invalid variable: " + varName);
        }
        Component comp = new Component();
        comp.setType(ComponentType.VARIABLE);
        comp.setContent(varName);
        components.add(comp);
        return this;
    }

    public ReportBuilder addSeparator() {
        Component comp = new Component();
        comp.setType(ComponentType.SEPARATOR);
        components.add(comp);
        return this;
    }

    public String render(Map<String, Object> context) {
        StringBuilder html = new StringBuilder("<div class=\"report\">");

        for (Component comp : components) {
            switch (comp.getType()) {
                case TEXT:
                    String text = comp.getContent();
                    if (comp.getStyle() == TextStyle.BOLD) {
                        text = "<strong>" + text + "</strong>";
                    } else if (comp.getStyle() == TextStyle.ITALIC) {
                        text = "<em>" + text + "</em>";
                    } else if (comp.getStyle() == TextStyle.HEADING) {
                        text = "<h2>" + text + "</h2>";
                    }
                    html.append("<p>").append(text).append("</p>");
                    break;

                case VARIABLE:
                    Object value = context.get(comp.getContent());
                    String strValue = value != null ? escapeHtml(value.toString()) : "[MISSING]";
                    html.append("<p><strong>").append(strValue).append("</strong></p>");
                    break;

                case SEPARATOR:
                    html.append("<hr>");
                    break;
            }
        }

        html.append("</div>");
        return html.toString();
    }

    public String toJson() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.writeValueAsString(components);
    }

    public static ReportBuilder fromJson(String json) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        ReportBuilder builder = new ReportBuilder();
        builder.components = mapper.readValue(json,
            mapper.getTypeFactory().constructCollectionType(List.class, Component.class));
        return builder;
    }

    private String escapeHtml(String input) {
        return input.replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;");
    }
}

// REST API
@RestController
public class ReportBuilderAPI {

    @PostMapping("/report/build")
    public ResponseEntity<?> buildReport(@RequestBody BuildRequest request) {
        try {
            ReportBuilder builder = new ReportBuilder();

            for (Action action : request.getActions()) {
                switch (action.getType()) {
                    case "add_text":
                        builder.addText(action.getText(), action.getStyle());
                        break;
                    case "add_variable":
                        builder.addVariable(action.getVariable());
                        break;
                    case "add_separator":
                        builder.addSeparator();
                        break;
                }
            }

            String json = builder.toJson();
            String reportId = "rpt_" + UUID.randomUUID();

            // Save structure to database (not code!)
            saveReportTemplate(reportId, json);

            return ResponseEntity.ok(Map.of(
                "reportId", reportId,
                "preview", builder.render(Map.of(
                    "username", "John Doe",
                    "email", "john@example.com",
                    "orderId", "12345"
                ))
            ));

        } catch (Exception e) {
            return ResponseEntity.badRequest()
                .body(Map.of("error", e.getMessage()));
        }
    }

    private void saveReportTemplate(String id, String json) {
        // Save to database using PreparedStatement
    }
}
```

**Key**: Users build reports visually - no FreeMarker code, just structured JSON."""

    conversations = [
        {"from": "human", "value": human_turn_1, "turn": 1},
        {"from": "assistant", "value": assistant_turn_1, "turn": 2},
        {"from": "human", "value": human_turn_2, "turn": 3},
        {"from": "assistant", "value": assistant_turn_2, "turn": 4},
    ]

    validation = {
        "syntax_check": "not_tested",
        "security_review": "not_reviewed",
        "code_execution": "not_tested",
        "encoding_check": "not_tested",
        "duplication_check": "not_tested",
        "reviewed_by": "automated-generator",
        "review_date": str(date.today()),
        "issues": []
    }

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": conversations,
        "validation": validation
    }


def example_004_erb():
    """Ruby/ERB - ERB template injection."""

    example_id = "ssti-000004"
    metadata = create_base_metadata("ruby", 4, "erb")

    context = {
        "real_world_incident": "2020 ERB injection in Ruby on Rails apps",
        "impact": "Multiple Rails applications vulnerable to RCE via ERB",
        "attack_vector": "User-controlled ERB template strings",
        "business_impact": "Server compromise, data theft"
    }

    human_turn_1 = """I'm building a Ruby on Rails app where users can customize email templates using ERB. Is it safe to render user-provided ERB strings?"""

    assistant_turn_1 = """No! ERB with user input is extremely dangerous:

**VULNERABLE CODE**:

```ruby
class EmailPreviewController < ApplicationController
  def preview
    # DANGER: User-controlled ERB template
    template_string = params[:template]
    username = params[:username]

    # Vulnerable: Rendering user ERB string
    erb = ERB.new(template_string)
    context = binding
    @username = username
    @date = Time.now

    render html: erb.result(context).html_safe
  end
end
```

**Why This Is Vulnerable**:
1. `ERB.new()` with user input compiles arbitrary Ruby code
2. `binding` gives access to entire execution context
3. Can execute any Ruby code

**Attack Example**:
```erb
<%# Exploit 1: Execute shell commands %>
<%= `id` %>
<%= system('whoami') %>

<%# Exploit 2: Read files %>
<%= File.read('/etc/passwd') %>

<%# Exploit 3: Instantiate dangerous classes %>
<%= IO.popen('ls -la').read %>

<%# Exploit 4: Access Rails internals %>
<%= Rails.application.secrets.secret_key_base %>
```

**Result**: Remote code execution, file system access, secret key leakage"""

    human_turn_2 = """How do I fix this? Can I sanitize the ERB template?"""

    assistant_turn_2 = """Don't try to sanitize ERB - use **predefined template files** instead:

**SECURE VERSION**:

```ruby
class SecureEmailPreviewController < ApplicationController
  # Allowlist of templates
  ALLOWED_TEMPLATES = {
    'welcome' => 'email_templates/welcome',
    'order_confirm' => 'email_templates/order_confirm',
    'shipping' => 'email_templates/shipping'
  }.freeze

  def preview
    template_name = params[:template]
    username = params[:username]

    # Validate against allowlist
    unless ALLOWED_TEMPLATES.key?(template_name)
      render plain: 'Invalid template', status: :bad_request
      return
    end

    # Sanitize user data
    @username = ERB::Util.html_escape(username)
    @date = Time.now.strftime('%Y-%m-%d')
    @order_id = SecureRandom.uuid

    # Render template file (not user string!)
    render template: ALLOWED_TEMPLATES[template_name]
  end
end
```

**Template File** (`app/views/email_templates/welcome.html.erb`):
```erb
<%# ERB auto-escapes with <%= %> in Rails %>
<div class="email-preview">
  <h2>Welcome <%= @username %>!</h2>
  <p>Your account was created on <%= @date %>.</p>
  <p>Order ID: <%= @order_id %></p>
</div>
```

**Why This Is Secure**:
1. **Template files only**: No `ERB.new()` with user input
2. **Allowlist**: Only predefined templates can be rendered
3. **Auto-escaping**: `<%= %>` escapes HTML by default in Rails
4. **Input sanitization**: `ERB::Util.html_escape()`
5. **No binding exposure**: Limited instance variables only"""

    human_turn_3 = """What if I need some template flexibility? Can ERB be restricted?"""

    assistant_turn_3 = r"""ERB is very difficult to sandbox. Here's a heavily restricted approach:

```ruby
require 'erb'
require 'cgi'

class RestrictedERBRenderer
  MAX_TEMPLATE_LENGTH = 500

  # Only allow these instance variable names
  ALLOWED_VARIABLES = %w[@username @email @date @order_id].freeze

  def initialize
    @dangerous_patterns = [
      /<%[^=]/,          # <% (code execution, not output)
      /`/,               # Backticks (shell execution)
      /system/i,         # system() calls
      /exec/i,           # exec() calls
      /eval/i,           # eval() calls
      /File\./i,         # File operations
      /IO\./i,           # IO operations
      /open/i,           # open() calls
      /require/i,        # require statements
      /load/i,           # load statements
      /Rails\./i,        # Rails internals
      /binding/i,        # binding access
      /__send__/i,       # __send__
      /send/i,           # send method
      /const_get/i,      # const_get
      /class_eval/i,     # class_eval
      /instance_eval/i   # instance_eval
    ]
  end

  def validate_template(template_str)
    # Length check
    if template_str.length > MAX_TEMPLATE_LENGTH
      raise SecurityError, 'Template too long'
    end

    # Check for dangerous patterns
    @dangerous_patterns.each do |pattern|
      if template_str =~ pattern
        raise SecurityError, "Dangerous pattern detected: #{pattern}"
      end
    end

    # Only allow <%= %> tags (output only, no code execution)
    if template_str =~ /<% /
      raise SecurityError, 'Only <%= %> tags allowed (no <% %>)'
    end

    # Extract variable names
    variables = template_str.scan(/@\\w+/).uniq

    # Check if all variables are allowed
    disallowed = variables - ALLOWED_VARIABLES
    if disallowed.any?
      raise SecurityError, "Disallowed variables: #{disallowed.join(', ')}"
    end

    true
  end

  def render_safe(template_str, context_hash)
    validate_template(template_str)

    # Create safe context with only allowed variables
    safe_context = Object.new
    context_hash.each do |key, value|
      if ALLOWED_VARIABLES.include?("@#{key}")
        # Escape all string values
        safe_value = value.is_a?(String) ? CGI.escape_html(value) : value
        safe_context.instance_variable_set("@#{key}", safe_value)
      end
    end

    # Render with restricted binding
    erb = ERB.new(template_str)
    erb.result(safe_context.instance_eval { binding })

  rescue SecurityError => e
    "Template error: #{CGI.escape_html(e.message)}"
  rescue StandardError => e
    'Template rendering failed'
  end
end

# Usage
renderer = RestrictedERBRenderer.new

template = params[:template] || 'Hello <%= @username %>!'
context = {
  'username' => params[:username],
  'email' => params[:email],
  'date' => Time.now.strftime('%Y-%m-%d'),
  'order_id' => SecureRandom.uuid
}

html = renderer.render_safe(template, context)
render html: html.html_safe
```

**Security Layers**:
1. **Output-only tags**: Only `<%= %>` allowed (no `<% %>`)
2. **Variable allowlist**: Only specific instance variables
3. **Pattern blacklist**: Blocks dangerous Ruby methods
4. **Length limit**: Prevents DoS
5. **Isolated binding**: Limited object context
6. **Input escaping**: HTML entity encoding

**Still Risky**: ERB is powerful - avoid user templates if possible."""

    human_turn_4 = """What's the production best practice?"""

    assistant_turn_4 = """Use a **template builder** with structured data instead:

```ruby
class TemplateBuilder
  ALLOWED_VARIABLES = %w[username email order_id date amount].freeze
  ALLOWED_STYLES = %w[normal bold italic heading].freeze

  def initialize
    @components = []
  end

  def add_text(text, style: 'normal')
    raise ArgumentError, 'Invalid style' unless ALLOWED_STYLES.include?(style)

    @components << {
      type: 'text',
      content: CGI.escape_html(text),
      style: style
    }
    self
  end

  def add_variable(var_name)
    raise ArgumentError, 'Invalid variable' unless ALLOWED_VARIABLES.include?(var_name)

    @components << {
      type: 'variable',
      name: var_name
    }
    self
  end

  def add_separator
    @components << { type: 'separator' }
    self
  end

  def render(context)
    html = '<div class="email-template">'

    @components.each do |component|
      case component[:type]
      when 'text'
        text = component[:content]
        text = "<strong>#{text}</strong>" if component[:style] == 'bold'
        text = "<em>#{text}</em>" if component[:style] == 'italic'
        text = "<h2>#{text}</h2>" if component[:style] == 'heading'
        html += "<p>#{text}</p>"

      when 'variable'
        value = context[component[:name]] || '[MISSING]'
        html += "<p><strong>#{CGI.escape_html(value)}</strong></p>"

      when 'separator'
        html += '<hr>'
      end
    end

    html += '</div>'
    html.html_safe
  end

  def to_json
    @components.to_json
  end

  def self.from_json(json_str)
    builder = new
    data = JSON.parse(json_str)
    data.each { |comp| builder.instance_variable_get(:@components) << comp.symbolize_keys }
    builder
  end
end

# API endpoint
class TemplateBuilderController < ApplicationController
  def build
    builder = TemplateBuilder.new

    params[:actions].each do |action|
      case action[:type]
      when 'add_text'
        builder.add_text(action[:text], style: action[:style] || 'normal')
      when 'add_variable'
        builder.add_variable(action[:variable])
      when 'add_separator'
        builder.add_separator
      end
    end

    # Save structure to database (not code!)
    template_json = builder.to_json
    template_id = "tpl_#{Digest::MD5.hexdigest(template_json)}"

    Template.create!(
      template_id: template_id,
      structure: template_json
    )

    # Return preview
    preview = builder.render({
      'username' => 'John Doe',
      'email' => 'john@example.com',
      'order_id' => '12345',
      'date' => Time.now.strftime('%Y-%m-%d'),
      'amount' => '$99.99'
    })

    render json: {
      template_id: template_id,
      preview: preview
    }

  rescue ArgumentError => e
    render json: { error: e.message }, status: :bad_request
  end

  def render_template
    template = Template.find_by!(template_id: params[:id])
    builder = TemplateBuilder.from_json(template.structure)

    html = builder.render(params[:context] || {})
    render html: html
  end
end
```

**Key Principle**: Users never write ERB code - they use a visual builder that generates JSON."""

    conversations = [
        {"from": "human", "value": human_turn_1, "turn": 1},
        {"from": "assistant", "value": assistant_turn_1, "turn": 2},
        {"from": "human", "value": human_turn_2, "turn": 3},
        {"from": "assistant", "value": assistant_turn_2, "turn": 4},
    ]

    validation = {
        "syntax_check": "not_tested",
        "security_review": "not_reviewed",
        "code_execution": "not_tested",
        "encoding_check": "not_tested",
        "duplication_check": "not_tested",
        "reviewed_by": "automated-generator",
        "review_date": str(date.today()),
        "issues": []
    }

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": conversations,
        "validation": validation
    }


def example_005_handlebars():
    """JavaScript/Handlebars - Prototype pollution via templates."""

    example_id = "ssti-000005"
    metadata = create_base_metadata("javascript", 5, "handlebars")

    context = {
        "real_world_incident": "2021 Handlebars prototype pollution vulnerabilities",
        "impact": "CVE-2021-23383, Prototype pollution leading to RCE",
        "attack_vector": "Template injection via Handlebars helpers",
        "business_impact": "Client and server-side compromise"
    }

    human_turn_1 = """I'm using Handlebars.js for email templates in my Node.js app. Users can customize templates. Is this safe?"""

    assistant_turn_1 = """Handlebars with user input is risky. Here's why:

**VULNERABLE CODE**:

```javascript
const Handlebars = require('handlebars');
const express = require('express');
const app = express();

app.get('/preview', (req, res) => {
    // DANGER: User-controlled template string
    const templateString = req.query.template || 'Hello {{name}}!';
    const name = req.query.name || 'User';

    // Vulnerable: Compiling user template
    const template = Handlebars.compile(templateString);

    const result = template({
        name: name,
        date: new Date().toISOString()
    });

    res.send(result);
});

app.listen(3000);
```

**Why This Is Vulnerable**:
1. `Handlebars.compile()` with user input creates executable templates
2. Can use built-in helpers like `{{lookup}}` for property access
3. Prototype pollution possible via helper abuse
4. Can access Node.js globals in some configurations

**Attack Example**:
```handlebars
{{!-- Exploit 1: Lookup helper to access prototype --}}
{{#with (lookup this '__proto__')}}
  {{#with (lookup this 'constructor')}}
    {{#with (lookup this 'prototype')}}
      {{isAdmin}}=true
    {{/with}}
  {{/with}}
{{/with}}

{{!-- Exploit 2: Access process object (if available) --}}
{{lookup (lookup this 'constructor') 'constructor' 'return process.env'}}

{{!-- Exploit 3: Prototype pollution --}}
{{lookup this '__proto__' 'polluted' 'yes'}}
```

**Result**: Prototype pollution, potential RCE, data manipulation"""

    human_turn_2 = """How do I prevent this?"""

    assistant_turn_2 = """Use **predefined template files** and restrict helpers:

**SECURE VERSION**:

```javascript
const Handlebars = require('handlebars');
const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();

// Allowlist of templates
const ALLOWED_TEMPLATES = {
    'welcome': './templates/welcome.hbs',
    'order_confirm': './templates/order_confirm.hbs',
    'shipping': './templates/shipping.hbs'
};

// Configure Handlebars securely
const handlebars = Handlebars.create();

// Disable prototype access
handlebars.JavaScriptCompiler.prototype.nameLookup = function(parent, name) {
    // Block __proto__, constructor, prototype access
    if (name === '__proto__' || name === 'constructor' || name === 'prototype') {
        return 'undefined';
    }
    return handlebars.JavaScriptCompiler.prototype.nameLookup.call(this, parent, name);
};

// Load and compile templates at startup
const compiledTemplates = {};
Object.keys(ALLOWED_TEMPLATES).forEach(name => {
    const templatePath = path.resolve(ALLOWED_TEMPLATES[name]);
    const templateSource = fs.readFileSync(templatePath, 'utf8');
    compiledTemplates[name] = handlebars.compile(templateSource);
});

app.get('/preview', (req, res) => {
    const templateName = req.query.template || 'welcome';
    const name = req.query.name || 'User';

    // Validate template name
    if (!compiledTemplates[templateName]) {
        return res.status(400).send('Invalid template');
    }

    // Escape HTML in user data
    const escapeHtml = (str) => {
        return str.replace(/&/g, '&amp;')
                 .replace(/</g, '&lt;')
                 .replace(/>/g, '&gt;')
                 .replace(/"/g, '&quot;')
                 .replace(/'/g, '&#x27;');
    };

    // Prepare safe context
    const context = {
        name: escapeHtml(name),
        date: new Date().toISOString().split('T')[0],
        orderId: Math.random().toString(36).substr(2, 9)
    };

    // Render precompiled template
    const result = compiledTemplates[templateName](context);

    res.send(result);
});

app.listen(3000);
```

**Template File** (`templates/welcome.hbs`):
```handlebars
<div class="email">
    <h2>Welcome {{name}}!</h2>
    <p>Your account was created on {{date}}.</p>
    <p>Order ID: {{orderId}}</p>
</div>
```

**Why This Is Secure**:
1. **Template files only**: No user-controlled template strings
2. **Precompiled**: Templates compiled at startup, not per-request
3. **Allowlist**: Only predefined templates accepted
4. **Prototype protection**: Custom nameLookup blocks dangerous properties
5. **Input escaping**: HTML entities escaped
6. **No dangerous helpers**: Only safe built-ins available"""

    human_turn_3 = """Can I allow limited template customization safely?"""

    assistant_turn_3 = """Only with strict restrictions. Here's a hardened approach:

```javascript
const Handlebars = require('handlebars');

class RestrictedHandlebarsRenderer {
    constructor() {
        this.handlebars = Handlebars.create();
        this.maxTemplateLength = 500;

        // Disable dangerous helpers
        this.handlebars.registerHelper('lookup', () => 'BLOCKED');
        this.handlebars.registerHelper('with', function() { return ''; });

        // Override nameLookup to block prototype access
        const originalNameLookup = this.handlebars.JavaScriptCompiler.prototype.nameLookup;
        this.handlebars.JavaScriptCompiler.prototype.nameLookup = function(parent, name) {
            const dangerous = ['__proto__', 'constructor', 'prototype', '__defineGetter__',
                             '__defineSetter__', '__lookupGetter__', '__lookupSetter__'];

            if (dangerous.includes(name)) {
                return 'undefined';
            }

            return originalNameLookup.call(this, parent, name);
        };

        this.allowedVariables = new Set(['name', 'email', 'date', 'orderId', 'amount']);
        this.dangerousPatterns = [
            /__proto__/,
            /constructor/,
            /prototype/,
            /lookup/,
            /\\.\\./, // Path traversal
            /require/,
            /process/,
            /global/,
            /eval/
        ];
    }

    validateTemplate(templateStr) {
        if (!templateStr || templateStr.length > this.maxTemplateLength) {
            throw new Error('Invalid template length');
        }

        // Check for dangerous patterns
        for (const pattern of this.dangerousPatterns) {
            if (pattern.test(templateStr)) {
                throw new Error(`Dangerous pattern detected: ${pattern}`);
            }
        }

        // Extract variables from template
        const variablePattern = /\\{\\{\\s*(\\w+)\\s*\\}\\}/g;
        const variables = [];
        let match;

        while ((match = variablePattern.exec(templateStr)) !== null) {
            variables.push(match[1]);
        }

        // Check if all variables are allowed
        const disallowed = variables.filter(v => !this.allowedVariables.has(v));
        if (disallowed.length > 0) {
            throw new Error(`Disallowed variables: ${disallowed.join(', ')}`);
        }

        return true;
    }

    renderSafe(templateStr, userContext) {
        try {
            this.validateTemplate(templateStr);

            // Create safe context with only allowed variables
            const safeContext = {};
            for (const key of this.allowedVariables) {
                if (userContext[key] !== undefined) {
                    const value = userContext[key];
                    safeContext[key] = typeof value === 'string'
                        ? value.replace(/[&<>"']/g, (char) => ({
                            '&': '&amp;',
                            '<': '&lt;',
                            '>': '&gt;',
                            '"': '&quot;',
                            "'": '&#x27;'
                          })[char])
                        : value;
                }
            }

            const template = this.handlebars.compile(templateStr);
            return template(safeContext);

        } catch (error) {
            return `Template error: ${error.message}`;
        }
    }
}

// Usage
const app = require('express')();
const renderer = new RestrictedHandlebarsRenderer();

app.post('/custom-preview', express.json(), (req, res) => {
    const { template, context } = req.body;

    const result = renderer.renderSafe(template, context || {});
    res.send(result);
});

app.listen(3000);
```

**Security Layers**:
1. Blocks `lookup` and `with` helpers
2. Custom nameLookup prevents prototype access
3. Variable allowlist
4. Pattern blacklist
5. Length limits
6. Input escaping

**Still Risky**: New bypasses possible. Avoid user templates."""

    human_turn_4 = """What's the production-safe alternative?"""

    assistant_turn_4 = """Use a **template builder** with structured components:

```javascript
class TemplateBuilder {
    static ALLOWED_VARIABLES = new Set(['name', 'email', 'orderId', 'date', 'amount']);
    static ALLOWED_STYLES = new Set(['normal', 'bold', 'italic', 'heading']);

    constructor() {
        this.components = [];
    }

    addText(text, style = 'normal') {
        if (!TemplateBuilder.ALLOWED_STYLES.has(style)) {
            throw new Error(`Invalid style: ${style}`);
        }

        this.components.push({
            type: 'text',
            content: this.escapeHtml(text),
            style
        });

        return this;
    }

    addVariable(varName) {
        if (!TemplateBuilder.ALLOWED_VARIABLES.has(varName)) {
            throw new Error(`Invalid variable: ${varName}`);
        }

        this.components.push({
            type: 'variable',
            name: varName
        });

        return this;
    }

    addSeparator() {
        this.components.push({ type: 'separator' });
        return this;
    }

    render(context) {
        let html = '<div class="email-template">';

        for (const component of this.components) {
            switch (component.type) {
                case 'text':
                    let text = component.content;
                    if (component.style === 'bold') text = `<strong>${text}</strong>`;
                    if (component.style === 'italic') text = `<em>${text}</em>`;
                    if (component.style === 'heading') text = `<h2>${text}</h2>`;
                    html += `<p>${text}</p>`;
                    break;

                case 'variable':
                    const value = context[component.name] || '[MISSING]';
                    html += `<p><strong>${this.escapeHtml(String(value))}</strong></p>`;
                    break;

                case 'separator':
                    html += '<hr>';
                    break;
            }
        }

        html += '</div>';
        return html;
    }

    escapeHtml(str) {
        return str.replace(/[&<>"']/g, (char) => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;'
        })[char]);
    }

    toJSON() {
        return JSON.stringify(this.components);
    }

    static fromJSON(json) {
        const builder = new TemplateBuilder();
        builder.components = JSON.parse(json);
        return builder;
    }
}

// REST API
const express = require('express');
const app = express();
app.use(express.json());

app.post('/template/build', (req, res) => {
    try {
        const builder = new TemplateBuilder();

        for (const action of req.body.actions || []) {
            switch (action.type) {
                case 'add_text':
                    builder.addText(action.text, action.style || 'normal');
                    break;
                case 'add_variable':
                    builder.addVariable(action.variable);
                    break;
                case 'add_separator':
                    builder.addSeparator();
                    break;
            }
        }

        const templateJson = builder.toJSON();
        const templateId = `tpl_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

        // Save to database (structure, not code!)
        // db.templates.insert({ id: templateId, structure: templateJson });

        const preview = builder.render({
            name: 'John Doe',
            email: 'john@example.com',
            orderId: '12345',
            date: new Date().toISOString().split('T')[0],
            amount: '$99.99'
        });

        res.json({
            templateId,
            preview
        });

    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.listen(3000);
```

**Key**: Users build templates visually - no Handlebars code, just JSON structure."""

    conversations = [
        {"from": "human", "value": human_turn_1, "turn": 1},
        {"from": "assistant", "value": assistant_turn_1, "turn": 2},
        {"from": "human", "value": human_turn_2, "turn": 3},
        {"from": "assistant", "value": assistant_turn_2, "turn": 4},
    ]

    validation = {
        "syntax_check": "not_tested",
        "security_review": "not_reviewed",
        "code_execution": "not_tested",
        "encoding_check": "not_tested",
        "duplication_check": "not_tested",
        "reviewed_by": "automated-generator",
        "review_date": str(date.today()),
        "issues": []
    }

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": conversations,
        "validation": validation
    }


def example_006_mako():
    """Python/Mako - Mako template injection."""

    example_id = "ssti-000006"
    metadata = create_base_metadata("python", 6, "mako")

    context = {
        "real_world_incident": "2019 Mako SSTI in Python web applications",
        "impact": "RCE vulnerabilities in applications using Mako templates",
        "attack_vector": "User-controlled Mako template strings",
        "business_impact": "Server compromise, arbitrary code execution"
    }

    human_turn_1 = """I'm using Mako templates in my Python web app. Users can customize page layouts. Is rendering user templates safe?"""

    assistant_turn_1 = """No! Mako templates with user input allow arbitrary Python code execution:

**VULNERABLE CODE**:

```python
from mako.template import Template
from flask import Flask, request

app = Flask(__name__)

@app.route('/render')
def render_template():
    # DANGER: User-controlled template string
    template_str = request.args.get('template', 'Hello ${name}')
    name = request.args.get('name', 'User')

    # Vulnerable: Rendering user Mako template
    template = Template(template_str)
    result = template.render(name=name)

    return result
```

**Why This Is Vulnerable**:
1. Mako templates can execute arbitrary Python code
2. `${ }` expressions evaluate Python
3. `<% %>` blocks execute statements
4. Access to Python built-ins

**Attack Example**:
```mako
<%# Exploit 1: Execute shell commands %>
${ __import__('os').popen('id').read() }

<%# Exploit 2: Read files %>
${ open('/etc/passwd').read() }

<%# Exploit 3: Import modules %>
<% import subprocess %>
${ subprocess.check_output(['whoami']) }
```

**Result**: Remote code execution, file system access"""

    human_turn_2 = """How do I fix this Mako template injection vulnerability?"""

    assistant_turn_2 = """Use **predefined template files** only:

**SECURE VERSION**:

```python
from mako.lookup import TemplateLookup
from flask import Flask, request, abort
import html

app = Flask(__name__)

# Template lookup from directory (not strings!)
lookup = TemplateLookup(
    directories=['./templates'],
    strict_undefined=True,
    imports=['from markupsafe import escape']
)

ALLOWED_TEMPLATES = {
    'welcome': 'welcome.mako',
    'order': 'order.mako',
    'profile': 'profile.mako'
}

@app.route('/render')
def render_template():
    template_name = request.args.get('template', 'welcome')
    name = request.args.get('name', 'User')

    # Validate template name
    if template_name not in ALLOWED_TEMPLATES:
        abort(400, 'Invalid template')

    # Load template from file
    template = lookup.get_template(ALLOWED_TEMPLATES[template_name])

    # Render with escaped data
    result = template.render(
        name=html.escape(name),
        date=date.today().isoformat()
    )

    return result
```

**Template File** (`templates/welcome.mako`):
```mako
<%! from markupsafe import escape %>
<div class="welcome">
    <h1>Welcome ${escape(name)}!</h1>
    <p>Date: ${date}</p>
</div>
```

**Why This Is Secure**:
1. Template files only (no `Template()` with user strings)
2. Allowlist of templates
3. `strict_undefined=True` catches undefined variables
4. Input escaping with `html.escape()`"""

    human_turn_3 = """Can Mako be sandboxed for user templates?"""

    assistant_turn_3 = r"""Mako is very difficult to sandbox. Here's a restricted approach (still risky):

```python
from mako.template import Template
from mako import exceptions
import html
import re

class RestrictedMakoRenderer:
    def __init__(self):
        self.max_length = 500
        self.allowed_vars = {'name', 'email', 'date', 'order_id'}

        # Dangerous patterns to block
        self.dangerous_patterns = [
            r'<%\s', # Code blocks
            r'__import__',
            r'open\s*\(',
            r'eval\s*\(',
            r'exec\s*\(',
            r'compile\s*\(',
            r'import\s+',
            r'from\s+',
            r'subprocess',
            r'os\.',
            r'sys\.',
            r'\.read\(',
            r'\.write\(',
            r'__.*__'  # Dunder methods
        ]

    def validate(self, template_str):
        if len(template_str) > self.max_length:
            raise ValueError('Template too long')

        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, template_str, re.IGNORECASE):
                raise ValueError(f'Dangerous pattern: {pattern}')

        # Only allow ${ } expressions (not <% %> blocks)
        if '<%' in template_str and not template_str.strip().startswith('<%!'):
            raise ValueError('Code blocks not allowed')

        return True

    def render_safe(self, template_str, context):
        try:
            self.validate(template_str)

            # Filter context to allowed variables only
            safe_context = {
                k: html.escape(str(v)) if isinstance(v, str) else v
                for k, v in context.items()
                if k in self.allowed_vars
            }

            # Render with restricted context
            template = Template(template_str)
            return template.render(**safe_context)

        except exceptions.MakoException as e:
            return f'Template error: {html.escape(str(e))}'
        except ValueError as e:
            return f'Security error: {html.escape(str(e))}'
```

**Warning**: Mako bypasses are possible. Avoid user templates."""

    human_turn_4 = """What's the safe production pattern?"""

    assistant_turn_4 = """Use a **template builder** - no Mako strings from users:

```python
class TemplateBuilder:
    ALLOWED_VARS = {'name', 'email', 'order_id', 'date', 'amount'}
    ALLOWED_STYLES = {'normal', 'bold', 'italic', 'heading'}

    def __init__(self):
        self.components = []

    def add_text(self, text, style='normal'):
        if style not in self.ALLOWED_STYLES:
            raise ValueError(f'Invalid style: {style}')

        self.components.append({
            'type': 'text',
            'content': html.escape(text),
            'style': style
        })
        return self

    def add_variable(self, var_name):
        if var_name not in self.ALLOWED_VARS:
            raise ValueError(f'Invalid variable: {var_name}')

        self.components.append({
            'type': 'variable',
            'name': var_name
        })
        return self

    def render(self, context):
        output = '<div class="template">'

        for comp in self.components:
            if comp['type'] == 'text':
                text = comp['content']
                if comp['style'] == 'bold':
                    text = f'<strong>{text}</strong>'
                elif comp['style'] == 'italic':
                    text = f'<em>{text}</em>'
                elif comp['style'] == 'heading':
                    text = f'<h2>{text}</h2>'
                output += f'<p>{text}</p>'

            elif comp['type'] == 'variable':
                value = context.get(comp['name'], '[MISSING]')
                output += f'<p><strong>{html.escape(str(value))}</strong></p>'

        output += '</div>'
        return output
```

**Key**: Users build templates via UI - no Mako code, just JSON."""

    conversations = [
        {"from": "human", "value": human_turn_1, "turn": 1},
        {"from": "assistant", "value": assistant_turn_1, "turn": 2},
        {"from": "human", "value": human_turn_2, "turn": 3},
        {"from": "assistant", "value": assistant_turn_2, "turn": 4},
    ]

    validation = {
        "syntax_check": "not_tested",
        "security_review": "not_reviewed",
        "code_execution": "not_tested",
        "encoding_check": "not_tested",
        "duplication_check": "not_tested",
        "reviewed_by": "automated-generator",
        "review_date": str(date.today()),
        "issues": []
    }

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": conversations,
        "validation": validation
    }


def example_007_smarty():
    """PHP/Smarty - Smarty template injection."""

    example_id = "ssti-000007"
    metadata = create_base_metadata("php", 7, "smarty")

    context = {
        "real_world_incident": "2018 Smarty SSTI in PHP applications",
        "impact": "RCE via Smarty template injection",
        "attack_vector": "User-controlled Smarty template strings",
        "business_impact": "Server compromise"
    }

    human_turn_1 = """I'm using Smarty templates in PHP. Can users safely provide template strings?"""

    assistant_turn_1 = """No! Smart with user input is dangerous:

**VULNERABLE CODE**:

```php
<?php
require_once 'vendor/autoload.php';

use Smarty\\Smarty;

$smarty = new Smarty();

// DANGER: User-controlled template
$template = $_GET['template'] ?? 'Hello {$name}';
$name = $_GET['name'] ?? 'User';

// Vulnerable: Rendering user string
$smarty->assign('name', $name);
echo $smarty->fetch('string:' . $template);
```

**Attack Example**:
```smarty
{php}system('id');{/php}
{$smarty.now}
{self::getStreamVariable("file:///etc/passwd")}
```

**Result**: RCE, file disclosure"""

    human_turn_2 = """How to fix this Smarty template injection vulnerability?"""

    assistant_turn_2 = """Use **template files** only:

```php
<?php
use Smarty\\Smarty;

$smarty = new Smarty();
$smarty->setTemplateDir('./templates/');
$smarty->setCompileDir('./templates_c/');

// Disable PHP tags in templates
$smarty->php_handling = Smarty::PHP_REMOVE;

$allowed = ['welcome.tpl', 'order.tpl'];
$template = $_GET['template'] ?? 'welcome.tpl';

if (!in_array($template, $allowed)) {
    die('Invalid template');
}

$smarty->assign('name', htmlspecialchars($_GET['name'] ?? 'User'));
$smarty->display($template);
```

**Secure**: Files only, no user strings, PHP disabled."""

    human_turn_3 = """What about sandboxing?"""

    assistant_turn_3 = """Difficult, but possible with heavy restrictions:

```php
<?php
class RestrictedSmartyRenderer {
    private $smarty;
    private $maxLength = 500;

    public function __construct() {
        $this->smarty = new Smarty();
        $this->smarty->php_handling = Smarty::PHP_REMOVE;
        $this->smarty->security = true;

        // Configure security policy
        $this->smarty->enableSecurity();
        $policy = $this->smarty->getSecurity();
        $policy->php_functions = []; // No PHP functions
        $policy->php_modifiers = ['escape'];
        $policy->allowed_tags = ['if', 'foreach'];
    }

    public function renderSafe($templateStr, $data) {
        if (strlen($templateStr) > $this->maxLength) {
            return 'Template too long';
        }

        // Block dangerous patterns
        if (preg_match('/{php}|{literal}|self::|getStreamVariable/i', $templateStr)) {
            return 'Dangerous pattern detected';
        }

        try {
            foreach ($data as $key => $value) {
                $this->smarty->assign($key, htmlspecialchars($value));
            }

            return $this->smarty->fetch('string:' . $templateStr);
        } catch (Exception $e) {
            return 'Template error';
        }
    }
}
```

**Still risky** - avoid user templates."""

    human_turn_4 = """Production alternative?"""

    assistant_turn_4 = """Template builder (no Smarty strings):

```php
<?php
class TemplateBuilder {
    private $components = [];

    public function addText($text, $style = 'normal') {
        $this->components[] = [
            'type' => 'text',
            'content' => htmlspecialchars($text),
            'style' => $style
        ];
        return $this;
    }

    public function addVariable($varName) {
        $allowedVars = ['name', 'email', 'date'];
        if (!in_array($varName, $allowedVars)) {
            throw new Exception('Invalid variable');
        }

        $this->components[] = [
            'type' => 'variable',
            'name' => $varName
        ];
        return $this;
    }

    public function render($context) {
        $html = '<div>';
        foreach ($this->components as $comp) {
            if ($comp['type'] === 'text') {
                $html .= '<p>' . $comp['content'] . '</p>';
            } elseif ($comp['type'] === 'variable') {
                $value = $context[$comp['name']] ?? '[MISSING]';
                $html .= '<p>' . htmlspecialchars($value) . '</p>';
            }
        }
        $html .= '</div>';
        return $html;
    }
}
```

**Key**: Visual builder - no template code."""

    conversations = [
        {"from": "human", "value": human_turn_1, "turn": 1},
        {"from": "assistant", "value": assistant_turn_1, "turn": 2},
        {"from": "human", "value": human_turn_2, "turn": 3},
        {"from": "assistant", "value": assistant_turn_2, "turn": 4},
    ]

    validation = {
        "syntax_check": "not_tested",
        "security_review": "not_reviewed",
        "code_execution": "not_tested",
        "encoding_check": "not_tested",
        "duplication_check": "not_tested",
        "reviewed_by": "automated-generator",
        "review_date": str(date.today()),
        "issues": []
    }

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": conversations,
        "validation": validation
    }


def example_008_velocity():
    """Java/Velocity - Velocity template injection."""

    example_id = "ssti-000008"
    metadata = create_base_metadata("java", 8, "velocity")

    context = {
        "real_world_incident": "2020 Velocity SSTI in Java web apps",
        "impact": "RCE via Velocity template injection",
        "attack_vector": "User-controlled Velocity templates",
        "business_impact": "Server compromise"
    }

    human_turn_1 = """I'm using Apache Velocity. Is it safe to render user template strings?"""

    assistant_turn_1 = """No! Velocity allows dangerous operations:

**VULNERABLE CODE**:

```java
import org.apache.velocity.VelocityContext;
import org.apache.velocity.app.Velocity;
import org.springframework.web.bind.annotation.*;
import java.io.StringWriter;

@RestController
public class VelocityController {
    @GetMapping("/render")
    public String renderTemplate(@RequestParam String template) {
        // DANGER: User template string
        VelocityContext context = new VelocityContext();
        context.put("name", "User");

        StringWriter writer = new StringWriter();
        Velocity.evaluate(context, writer, "template", template);

        return writer.toString();
    }
}
```

**Attack**:
```velocity
#set($runtime = $class.forName('java.lang.Runtime'))
#set($process = $runtime.getRuntime().exec('id'))
$process.getInputStream()
```

**Result**: RCE"""

    human_turn_2 = """How to secure this Velocity template injection?"""

    assistant_turn_2 = """Template files only:

```java
import org.apache.velocity.app.VelocityEngine;
import org.apache.velocity.Template;

public class SecureVelocityRenderer {
    private VelocityEngine engine;
    private Set<String> allowedTemplates;

    public SecureVelocityRenderer() {
        engine = new VelocityEngine();
        engine.setProperty("resource.loader", "file");
        engine.setProperty("file.resource.loader.path", "./templates");
        engine.init();

        allowedTemplates = Set.of("welcome.vm", "order.vm");
    }

    public String render(String templateName, Map<String, Object> data) {
        if (!allowedTemplates.contains(templateName)) {
            throw new IllegalArgumentException("Invalid template");
        }

        Template template = engine.getTemplate(templateName);
        VelocityContext context = new VelocityContext();

        data.forEach((k, v) -> {
            if (v instanceof String) {
                context.put(k, escapeHtml((String) v));
            } else {
                context.put(k, v);
            }
        });

        StringWriter writer = new StringWriter();
        template.merge(context, writer);
        return writer.toString();
    }
}
```

**Secure**: Files, allowlist, escaping."""

    human_turn_3 = """Restricted rendering possible?"""

    assistant_turn_3 = """Very difficult. Here's a heavily restricted approach:

```java
import org.apache.velocity.runtime.RuntimeServices;
import org.apache.velocity.runtime.RuntimeSingleton;
import org.apache.velocity.util.introspection.SecureUberspector;

public class RestrictedVelocityRenderer {
    private VelocityEngine engine;

    public RestrictedVelocityRenderer() {
        engine = new VelocityEngine();

        // Use secure introspector
        engine.setProperty("runtime.introspector.uberspect",
            "org.apache.velocity.util.introspection.SecureUberspector");

        // Block method calls on Class objects
        engine.setProperty("introspector.restrict.packages",
            "java.lang.reflect,java.lang.Runtime");

        engine.init();
    }

    public String renderSafe(String templateStr, Map<String, String> data) {
        // Validate length
        if (templateStr.length() > 500) {
            throw new SecurityException("Template too long");
        }

        // Block dangerous patterns
        if (templateStr.matches(".*\\$(class|runtime|exec).*")) {
            throw new SecurityException("Dangerous pattern");
        }

        VelocityContext context = new VelocityContext();
        data.forEach((k, v) -> context.put(k, escapeHtml(v)));

        StringWriter writer = new StringWriter();
        Velocity.evaluate(context, writer, "safe", templateStr);

        return writer.toString();
    }
}
```

**Still risky** - avoid if possible."""

    human_turn_4 = """Best practice?"""

    assistant_turn_4 = """Template builder (no Velocity code):

```java
public class TemplateBuilder {
    private List<Component> components = new ArrayList<>();

    public TemplateBuilder addText(String text) {
        components.add(new TextComponent(escapeHtml(text)));
        return this;
    }

    public TemplateBuilder addVariable(String varName) {
        if (!ALLOWED_VARS.contains(varName)) {
            throw new IllegalArgumentException("Invalid variable");
        }
        components.add(new VariableComponent(varName));
        return this;
    }

    public String render(Map<String, String> context) {
        StringBuilder html = new StringBuilder("<div>");

        for (Component comp : components) {
            html.append(comp.render(context));
        }

        html.append("</div>");
        return html.toString();
    }
}
```

**Key**: Structured data, not template code."""

    conversations = [
        {"from": "human", "value": human_turn_1, "turn": 1},
        {"from": "assistant", "value": assistant_turn_1, "turn": 2},
        {"from": "human", "value": human_turn_2, "turn": 3},
        {"from": "assistant", "value": assistant_turn_2, "turn": 4},
    ]

    validation = {
        "syntax_check": "not_tested",
        "security_review": "not_reviewed",
        "code_execution": "not_tested",
        "encoding_check": "not_tested",
        "duplication_check": "not_tested",
        "reviewed_by": "automated-generator",
        "review_date": str(date.today()),
        "issues": []
    }

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": conversations,
        "validation": validation
    }


def example_009_tornado():
    """Python/Tornado - Tornado template injection."""

    example_id = "ssti-000009"
    metadata = create_base_metadata("python", 9, "tornado")

    context = {
        "real_world_incident": "2019 Tornado SSTI vulnerabilities",
        "impact": "RCE in Tornado-based web applications",
        "attack_vector": "User-controlled Tornado templates",
        "business_impact": "Server compromise"
    }

    human_turn_1 = """I'm using Tornado templates. Can users provide template strings safely?"""

    assistant_turn_1 = """No! Tornado templates execute Python code:

**VULNERABLE CODE**:

```python
import tornado.template

@tornado.web.RequestHandler
def get(self):
    # DANGER: User template
    template_str = self.get_argument('template', 'Hello {{ name }}')
    name = self.get_argument('name', 'User')

    # Vulnerable
    template = tornado.template.Template(template_str)
    result = template.generate(name=name)

    self.write(result)
```

**Attack**:
```tornado
{% raw __import__('os').popen('id').read() %}
{{ __import__('subprocess').check_output(['whoami']) }}
```

**Result**: RCE"""

    human_turn_2 = """How to fix this Tornado template injection vulnerability?"""

    assistant_turn_2 = """Template files only:

```python
import tornado.template
import html

class SecureTemplateHandler(tornado.web.RequestHandler):
    ALLOWED_TEMPLATES = {
        'welcome': 'welcome.html',
        'order': 'order.html'
    }

    def get(self):
        template_name = self.get_argument('template', 'welcome')
        name = self.get_argument('name', 'User')

        if template_name not in self.ALLOWED_TEMPLATES:
            raise tornado.web.HTTPError(400)

        loader = tornado.template.Loader("./templates")
        template = loader.load(self.ALLOWED_TEMPLATES[template_name])

        result = template.generate(
            name=html.escape(name),
            date=date.today().isoformat()
        )

        self.write(result)
```

**Secure**: Files, allowlist, escaping."""

    human_turn_3 = """Sandboxing possible?"""

    assistant_turn_3 = """Very difficult - no good sandbox for Tornado. Avoid user templates entirely."""

    human_turn_4 = """Best practice?"""

    assistant_turn_4 = """Template builder:

```python
class TemplateBuilder:
    def __init__(self):
        self.components = []

    def add_text(self, text):
        self.components.append({
            'type': 'text',
            'content': html.escape(text)
        })
        return self

    def add_variable(self, var_name):
        if var_name not in ['name', 'email', 'date']:
            raise ValueError('Invalid variable')
        self.components.append({
            'type': 'variable',
            'name': var_name
        })
        return self

    def render(self, context):
        output = '<div>'
        for comp in self.components:
            if comp['type'] == 'text':
                output += f"<p>{comp['content']}</p>"
            elif comp['type'] == 'variable':
                value = context.get(comp['name'], '[MISSING]')
                output += f"<p>{html.escape(str(value))}</p>"
        output += '</div>'
        return output
```

**Key**: Structured builder, no template code."""

    conversations = [
        {"from": "human", "value": human_turn_1, "turn": 1},
        {"from": "assistant", "value": assistant_turn_1, "turn": 2},
        {"from": "human", "value": human_turn_2, "turn": 3},
        {"from": "assistant", "value": assistant_turn_2, "turn": 4},
    ]

    validation = {
        "syntax_check": "not_tested",
        "security_review": "not_reviewed",
        "code_execution": "not_tested",
        "encoding_check": "not_tested",
        "duplication_check": "not_tested",
        "reviewed_by": "automated-generator",
        "review_date": str(date.today()),
        "issues": []
    }

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": conversations,
        "validation": validation
    }


def example_010_go_template():
    """Go/text/template - Go template injection."""

    example_id = "ssti-000010"
    metadata = create_base_metadata("go", 10, "text/template")

    context = {
        "real_world_incident": "2021 Go template injection vulnerabilities",
        "impact": "Information disclosure, potential RCE in Go web apps",
        "attack_vector": "User-controlled Go template strings",
        "business_impact": "Data leakage, server compromise"
    }

    human_turn_1 = """I'm using Go's text/template package. Is it safe to render user-provided templates?"""

    assistant_turn_1 = """No! Go templates can access struct fields and call methods:

**VULNERABLE CODE**:

```go
package main

import (
    "html/template"
    "net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
    // DANGER: User-controlled template
    templateStr := r.URL.Query().Get("template")
    if templateStr == "" {
        templateStr = "Hello {{.Name}}"
    }

    // Vulnerable: Parsing user template
    tmpl, _ := template.New("user").Parse(templateStr)

    data := struct {
        Name string
        Config map[string]string
    }{
        Name: r.URL.Query().Get("name"),
        Config: map[string]string{"secret": "password123"},
    }

    tmpl.Execute(w, data)
}
```

**Attack**:
```go
{{.Config}}
{{.Config.secret}}
{{range .}}{{.}}{{end}}
```

**Result**: Information disclosure, config leakage"""

    human_turn_2 = """How to secure this Go template injection vulnerability?"""

    assistant_turn_2 = """Use **predefined template files** only:

```go
package main

import (
    "html/template"
    "net/http"
    "path/filepath"
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

    // Load template from file
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

**Template File** (`templates/welcome.tmpl`):
```html
<div class="welcome">
    <h1>Welcome {{.Name}}!</h1>
    <p>Date: {{.Date}}</p>
</div>
```

**Why This Is Secure**:
1. Template files only (no user strings)
2. Allowlist of templates
3. Limited data structure (only Name and Date)
4. HTML escaping"""

    human_turn_3 = """Can I restrict user templates safely?"""

    assistant_turn_3 = """Go templates are safer than most, but still risky:

```go
import (
    "html/template"
    "regexp"
    "strings"
)

type RestrictedRenderer struct {
    maxLength int
    allowedFields map[string]bool
}

func NewRestrictedRenderer() *RestrictedRenderer {
    return &RestrictedRenderer{
        maxLength: 500,
        allowedFields: map[string]bool{
            "Name": true,
            "Email": true,
            "Date": true,
        },
    }
}

func (r *RestrictedRenderer) Validate(templateStr string) error {
    if len(templateStr) > r.maxLength {
        return errors.New("template too long")
    }

    // Extract field references
    fieldPattern := regexp.MustCompile(`\\{\\{\\.([A-Z]\\w*)\\}\\}`)
    matches := fieldPattern.FindAllStringSubmatch(templateStr, -1)

    for _, match := range matches {
        if len(match) > 1 {
            field := match[1]
            if !r.allowedFields[field] {
                return fmt.Errorf("disallowed field: %s", field)
            }
        }
    }

    // Block dangerous patterns
    dangerous := []string{
        "{{range",
        "{{with",
        "{{define",
        "{{template",
        "{{block",
    }

    for _, pattern := range dangerous {
        if strings.Contains(templateStr, pattern) {
            return fmt.Errorf("disallowed pattern: %s", pattern)
        }
    }

    return nil
}

func (r *RestrictedRenderer) RenderSafe(templateStr string, data interface{}) (string, error) {
    if err := r.Validate(templateStr); err != nil {
        return "", err
    }

    tmpl, err := template.New("safe").Parse(templateStr)
    if err != nil {
        return "", err
    }

    var buf strings.Builder
    if err := tmpl.Execute(&buf, data); err != nil {
        return "", err
    }

    return buf.String(), nil
}
```

**Still has risks** - better to avoid user templates."""

    human_turn_4 = """What's the production-safe alternative?"""

    assistant_turn_4 = """Use a **template builder** with structured components:

```go
type TemplateBuilder struct {
    components []Component
}

type Component struct {
    Type    string
    Content string
    Style   string
    VarName string
}

var allowedVars = map[string]bool{
    "name": true,
    "email": true,
    "date": true,
}

func (tb *TemplateBuilder) AddText(text, style string) *TemplateBuilder {
    tb.components = append(tb.components, Component{
        Type:    "text",
        Content: template.HTMLEscapeString(text),
        Style:   style,
    })
    return tb
}

func (tb *TemplateBuilder) AddVariable(varName string) error {
    if !allowedVars[varName] {
        return fmt.Errorf("invalid variable: %s", varName)
    }

    tb.components = append(tb.components, Component{
        Type:    "variable",
        VarName: varName,
    })
    return nil
}

func (tb *TemplateBuilder) Render(context map[string]string) string {
    var html strings.Builder
    html.WriteString("<div>")

    for _, comp := range tb.components {
        switch comp.Type {
        case "text":
            text := comp.Content
            if comp.Style == "bold" {
                text = "<strong>" + text + "</strong>"
            }
            html.WriteString("<p>" + text + "</p>")

        case "variable":
            value := context[comp.VarName]
            if value == "" {
                value = "[MISSING]"
            }
            html.WriteString("<p>" + template.HTMLEscapeString(value) + "</p>")
        }
    }

    html.WriteString("</div>")
    return html.String()
}
```

**Key Principle**: Users build templates via UI - no Go template code, just structured JSON."""

    conversations = [
        {"from": "human", "value": human_turn_1, "turn": 1},
        {"from": "assistant", "value": assistant_turn_1, "turn": 2},
        {"from": "human", "value": human_turn_2, "turn": 3},
        {"from": "assistant", "value": assistant_turn_2, "turn": 4},
    ]

    validation = {
        "syntax_check": "not_tested",
        "security_review": "not_reviewed",
        "code_execution": "not_tested",
        "encoding_check": "not_tested",
        "duplication_check": "not_tested",
        "reviewed_by": "automated-generator",
        "review_date": str(date.today()),
        "issues": []
    }

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": conversations,
        "validation": validation
    }


def main():
    """Generate Batch 009: SSTI Part 1."""
    print("Generating Batch 009: Template Injection (SSTI) Part 1")
    print("=" * 60)

    # Generate all 10 examples
    examples = [
        example_001_jinja2_basic(),
        example_002_twig(),
        example_003_freemarker(),
        example_004_erb(),
        example_005_handlebars(),
        example_006_mako(),
        example_007_smarty(),
        example_008_velocity(),
        example_009_tornado(),
        example_010_go_template(),
    ]

    # Write to output file
    output_dir = Path(__file__).parent.parent / 'data'
    output_file = output_dir / 'ssti_batch_009.jsonl'

    with open(output_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"\nGenerated {len(examples)} examples")
    print(f"Output: {output_file}")

    print("\nExamples:")
    for ex in examples:
        print(f"  {ex['id']}: {ex['metadata']['lang']} - {ex['metadata']['template_engine']}")

    return 0


if __name__ == "__main__":
    exit(main())
