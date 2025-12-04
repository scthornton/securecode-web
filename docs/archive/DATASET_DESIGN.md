# SecureCode v2.0 Dataset Design

## Design Philosophy

**Quality over quantity** - 1,000 expert-validated examples beats 4,656 mediocre ones.

**Educational, not just differential** - Models learn WHY code is secure, not just WHAT secure code looks like.

**Modern threat coverage** - Focus on 2023-2025 attack vectors, not just classic vulnerabilities.

**Multi-turn conversations** - Progressive learning with explanations, questions, and refinements.

## Schema Design

```json
{
  "id": "unique-id-000001",
  "metadata": {
    "lang": "python",
    "category": "injection",
    "subcategory": "sql_injection",
    "owasp_2021": "A03:2021-Injection",
    "cwe": "CWE-89",
    "severity": "CRITICAL",
    "complexity": "moderate",
    "created": "2025-01-15",
    "validated": true
  },
  "context": {
    "real_world_incident": "2023 MOVEit Transfer SQL injection - 2,100+ organizations breached",
    "impact": "$9.2B in estimated damages, 77M+ records exposed",
    "attack_vector": "Unauthenticated SQL injection via crafted HTTP requests",
    "cve": "CVE-2023-34362"
  },
  "conversations": [
    {
      "turn": 1,
      "from": "human",
      "value": "I'm building a user login system. Show me how to check credentials against a database."
    },
    {
      "turn": 2,
      "from": "assistant",
      "value": "I'll show you both the vulnerable pattern (what NOT to do) and the secure implementation.\n\n**Vulnerable Code (SQL Injection Risk):**\n```python\ndef login_user(username, password):\n    query = f\"SELECT * FROM users WHERE username='{username}' AND password='{password}'\"\n    cursor.execute(query)\n    return cursor.fetchone()\n```\n\n**Why This Is Dangerous:**\nAn attacker can input `admin' --` as the username, which creates this query:\n```sql\nSELECT * FROM users WHERE username='admin' --' AND password='anything'\n```\nThe `--` comments out the password check, granting access without valid credentials.\n\n**Secure Implementation:**\n```python\nimport hashlib\nfrom psycopg2 import sql\n\ndef login_user(username, password):\n    # Use parameterized queries to prevent SQL injection\n    query = sql.SQL(\"SELECT id, password_hash FROM users WHERE username = %s\")\n    cursor.execute(query, (username,))\n    \n    user = cursor.fetchone()\n    if user is None:\n        return None\n    \n    # Verify password using secure hashing\n    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), user['salt'], 100000)\n    \n    if password_hash == user['password_hash']:\n        return user['id']\n    return None\n```\n\n**Key Security Controls:**\n1. **Parameterized queries** (`%s` placeholder) - database driver handles escaping\n2. **Password hashing** (PBKDF2) - never store plaintext passwords\n3. **Constant-time comparison** - prevents timing attacks\n4. **Separation of concerns** - authentication logic isolated from query construction"
    },
    {
      "turn": 3,
      "from": "human",
      "value": "What if I need to build dynamic WHERE clauses with multiple optional filters?"
    },
    {
      "turn": 4,
      "from": "assistant",
      "value": "Dynamic queries are common but risky. Here's the secure pattern:\n\n```python\nfrom psycopg2 import sql\n\ndef search_users(filters: dict):\n    # Build query dynamically but safely\n    allowed_fields = {'username', 'email', 'status', 'role'}\n    \n    # Validate all filter keys against allowlist\n    if not all(key in allowed_fields for key in filters.keys()):\n        raise ValueError(\"Invalid filter field\")\n    \n    # Build parameterized query dynamically\n    conditions = []\n    params = []\n    \n    for field, value in filters.items():\n        conditions.append(sql.SQL(\"{} = %s\").format(sql.Identifier(field)))\n        params.append(value)\n    \n    query = sql.SQL(\"SELECT * FROM users WHERE {}\").format(\n        sql.SQL(\" AND \").join(conditions)\n    )\n    \n    cursor.execute(query, params)\n    return cursor.fetchall()\n```\n\n**Security Pattern:**\n- Use `sql.Identifier()` for column names (prevents injection via field names)\n- Use `%s` placeholders for values (prevents injection via values)\n- Allowlist validation (only permitted fields can be queried)\n- Clear separation between SQL structure and user data"
    }
  ],
  "validation": {
    "syntax_check": "passed",
    "security_review": "passed",
    "code_execution": "passed",
    "reviewed_by": "security-expert-agent",
    "review_date": "2025-01-15"
  }
}
```

## Target Coverage

### Language Distribution (1,000 examples)
- Python: 200 (20%) - Most common for web/API/ML
- JavaScript/TypeScript: 180 (18%) - Web frontend/backend
- Java: 120 (12%) - Enterprise applications
- Go: 100 (10%) - Cloud-native, microservices
- C/C++: 80 (8%) - Systems programming
- C#: 80 (8%) - Enterprise/.NET
- Rust: 60 (6%) - Modern systems programming
- PHP: 60 (6%) - Legacy web applications
- Ruby: 40 (4%) - Web applications
- Kotlin: 40 (4%) - Android/modern JVM
- Swift: 40 (4%) - iOS/macOS

### Vulnerability Coverage (OWASP Top 10 2021)

| OWASP Category | Examples | Priority |
|----------------|----------|----------|
| A01: Broken Access Control | 150 | CRITICAL |
| A02: Cryptographic Failures | 120 | CRITICAL |
| A03: Injection | 140 | CRITICAL |
| A04: Insecure Design | 80 | HIGH |
| A05: Security Misconfiguration | 100 | HIGH |
| A06: Vulnerable Components | 60 | MEDIUM |
| A07: Auth Failures | 130 | CRITICAL |
| A08: Data Integrity Failures | 70 | HIGH |
| A09: Logging Failures | 50 | MEDIUM |
| A10: SSRF | 40 | MEDIUM |

### Modern Threat Categories (Additional 150 examples)

| Category | Examples | Languages |
|----------|----------|-----------|
| **Cloud Security** | 50 | Python, Go, Java |
| - AWS IAM misconfigurations | 15 | Python, Go |
| - S3 bucket exposure | 10 | Python, Java |
| - Secrets in environment variables | 10 | All |
| - Container escape vulnerabilities | 15 | Go, Python |
| **API Security** | 50 | JS, Python, Go |
| - GraphQL injection | 10 | JS, Python |
| - REST API rate limiting | 10 | All |
| - JWT vulnerabilities | 15 | JS, Python, Java |
| - API key exposure | 15 | All |
| **AI/ML Security** | 50 | Python |
| - Prompt injection defenses | 15 | Python |
| - Model extraction attacks | 10 | Python |
| - Training data poisoning | 10 | Python |
| - Adversarial input detection | 15 | Python |

### Complexity Distribution

- **Simple** (15%): Single vulnerability, obvious fix, beginner-friendly
- **Moderate** (60%): Multiple security controls, realistic scenarios
- **Complex** (20%): Chained vulnerabilities, architecture-level issues
- **Advanced** (5%): Novel attack vectors, research-level defenses

## Quality Standards

### Every Example Must Have:

✅ **Syntactically valid code** (tested with language-specific linters)
✅ **Security explanation** (WHY it's vulnerable, WHY the fix works)
✅ **Real-world context** (actual CVE or incident when available)
✅ **Progressive learning** (2-4 turn conversations minimum)
✅ **Complete fixes** (no partial/weak security patterns)
✅ **Validation metadata** (automated + manual review)

### Validation Pipeline:

1. **Syntax Validation** - Code must parse/compile
2. **Security Review** - Expert validation of vulnerability + fix
3. **Code Execution** - Example must run in isolated environment
4. **Encoding Check** - UTF-8 validation, no corruption
5. **Duplication Check** - No identical or near-identical examples
6. **Taxonomy Validation** - Proper OWASP/CWE mapping

## Example Types

### Type 1: Classic Vulnerability (40%)
- Well-known attack pattern
- Clear vulnerable → secure transformation
- Multi-turn with explanation
- Real-world incident context

### Type 2: Modern Threat (30%)
- 2023-2025 attack vectors
- Cloud/API/container security
- AI/ML specific vulnerabilities
- Emerging threat landscape

### Type 3: Architecture Security (20%)
- Design-level vulnerabilities
- Multiple components interaction
- Defense-in-depth examples
- Secure by design patterns

### Type 4: Edge Cases (10%)
- Subtle vulnerabilities
- Context-dependent security
- Language-specific gotchas
- Advanced attack techniques

## File Organization

```
v2/
├── DATASET_DESIGN.md           # This file
├── schema.json                 # JSON schema for validation
├── taxonomy.yaml               # Complete vulnerability taxonomy
├── generation/
│   ├── generate_examples.py    # Main generation script
│   ├── validators.py           # Validation functions
│   ├── templates/              # Example templates by category
│   └── real_world_incidents.json
├── data/
│   ├── train.jsonl             # Training set (800 examples)
│   ├── validation.jsonl        # Validation set (100 examples)
│   ├── test.jsonl              # Test set (100 examples)
│   └── metadata.json           # Dataset statistics
├── validation/
│   ├── syntax_tests/           # Language-specific syntax checkers
│   ├── security_review/        # Security expert validations
│   └── reports/                # Quality assurance reports
└── docs/
    ├── USAGE.md                # How to use this dataset
    ├── EXAMPLES.md             # Sample high-quality examples
    └── CHANGELOG.md            # Version history
```

## Success Metrics

A successful dataset will:

1. **Zero syntax errors** across all 1,000 examples
2. **100% security validation** by expert review
3. **90%+ multi-turn conversations** (2+ turns)
4. **70%+ with real-world context** (CVE or incident)
5. **Complete OWASP Top 10 coverage** (all categories represented)
6. **Modern threat coverage** (150+ examples from 2023-2025)
7. **Educational value** (explanations in every example)

## Timeline

- **Week 1**: Schema, taxonomy, validation pipeline
- **Week 2**: Generate OWASP Top 10 examples (400)
- **Week 3**: Generate modern threats + AI/ML security (200)
- **Week 4**: Generate architecture & edge cases (200)
- **Week 5**: Validation, testing, documentation (200)

**Total**: 1,000 examples, 5 weeks, expert-validated quality.
