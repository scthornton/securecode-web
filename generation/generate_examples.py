"""
SecureCode v2.0 Example Generation Framework

Generates high-quality secure code training examples with:
- Multi-turn conversations
- Security explanations
- Real-world context
- Complete validation
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from validators import DatasetValidator


class ExampleTemplate:
    """Base template for generating examples"""

    def __init__(self, metadata: Dict, context: Dict = None):
        self.metadata = metadata
        self.context = context or {}

    def generate_id(self) -> str:
        """Generate unique ID for example"""
        subcategory = self.metadata['subcategory']
        # Get count from existing examples (would need to track this)
        count = 1  # Placeholder
        return f"{subcategory}-{count:06d}"

    def create_example(self, conversations: List[Dict]) -> Dict:
        """Create complete example structure"""
        example = {
            'id': self.generate_id(),
            'metadata': {
                **self.metadata,
                'created': datetime.now().strftime('%Y-%m-%d'),
                'validated': False
            },
            'conversations': conversations,
            'validation': {
                'syntax_check': 'not_tested',
                'security_review': 'not_reviewed',
                'code_execution': 'not_tested',
                'encoding_check': 'not_tested',
                'duplication_check': 'not_tested',
                'reviewed_by': 'not_reviewed',
                'review_date': datetime.now().strftime('%Y-%m-%d'),
                'issues': []
            }
        }

        if self.context:
            example['context'] = self.context

        return example


class SQLInjectionGenerator:
    """Generates SQL injection examples"""

    LANGUAGES = ['python', 'php', 'java', 'javascript', 'ruby', 'c#']

    REAL_WORLD_CONTEXT = {
        'real_world_incident': '2023 MOVEit Transfer SQL injection - 2,100+ organizations breached',
        'impact': '$9.2B in estimated damages, 77M+ records exposed',
        'attack_vector': 'Unauthenticated SQL injection via crafted HTTP requests',
        'cve': 'CVE-2023-34362',
        'year': 2023
    }

    @staticmethod
    def generate_python_basic() -> Dict:
        """Generate basic Python SQL injection example"""
        metadata = {
            'lang': 'python',
            'category': 'injection',
            'subcategory': 'sql_injection',
            'owasp_2021': 'A03:2021-Injection',
            'cwe': 'CWE-89',
            'severity': 'CRITICAL',
            'complexity': 'moderate'
        }

        conversations = [
            {
                'turn': 1,
                'from': 'human',
                'value': "I'm building a user login system. Show me how to check credentials against a database."
            },
            {
                'turn': 2,
                'from': 'assistant',
                'value': """I'll show you both the vulnerable pattern (what NOT to do) and the secure implementation.

**Vulnerable Code (SQL Injection Risk):**
```python
import mysql.connector

def login_user_vulnerable(username, password):
    conn = mysql.connector.connect(host='localhost', database='myapp', user='root', password='secret')
    cursor = conn.cursor()

    # DANGEROUS: String concatenation in SQL query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return user is not None
```

**Why This Is Dangerous:**
An attacker can input `admin' --` as the username, which creates this query:
```sql
SELECT * FROM users WHERE username='admin' --' AND password='anything'
```
The `--` comments out the password check, granting access without valid credentials. This exact vulnerability type compromised MOVEit Transfer in 2023, affecting 2,100+ organizations and causing $9.2B in damages.

**Secure Implementation:**
```python
import mysql.connector
from hashlib import pbkdf2_hmac
import os

def login_user_secure(username, password):
    conn = mysql.connector.connect(host='localhost', database='myapp', user='root', password='secret')
    cursor = conn.cursor(dictionary=True)

    # SECURE: Use parameterized queries with placeholders
    query = "SELECT id, password_hash, salt FROM users WHERE username = %s"
    cursor.execute(query, (username,))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user is None:
        return False

    # Verify password using secure hashing
    password_hash = pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        user['salt'],
        100000  # PBKDF2 iterations
    )

    return password_hash == user['password_hash']
```

**Key Security Controls:**
1. **Parameterized queries** (`%s` placeholder) - The database driver handles escaping, preventing injection
2. **Password hashing** (PBKDF2 with 100,000 iterations) - Never store plaintext passwords
3. **Salting** - Prevents rainbow table attacks
4. **Separation of concerns** - User lookup and password verification are separate operations"""
            },
            {
                'turn': 3,
                'from': 'human',
                'value': "What if I need to build dynamic WHERE clauses with multiple optional search filters?"
            },
            {
                'turn': 4,
                'from': 'assistant',
                'value': """Dynamic queries are common but risky. Here's the secure pattern:

```python
from mysql.connector import connection
from typing import Dict, List, Tuple

def search_users_secure(filters: Dict[str, str]) -> List[Dict]:
    # Define allowlist of searchable fields
    ALLOWED_FIELDS = {'username', 'email', 'status', 'role', 'department'}

    # Validate all filter keys against allowlist
    if not all(field in ALLOWED_FIELDS for field in filters.keys()):
        raise ValueError("Invalid search field provided")

    conn = connection.MySQLConnection(host='localhost', database='myapp', user='app', password='secret')
    cursor = conn.cursor(dictionary=True)

    # Build parameterized query dynamically
    conditions = []
    params = []

    for field, value in filters.items():
        # Use identifier quoting for field names
        conditions.append(f"`{field}` = %s")
        params.append(value)

    # Construct final query with validated structure
    query = "SELECT id, username, email, role FROM users"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

# Safe usage
results = search_users_secure({
    'status': 'active',
    'role': 'admin'
})
```

**Security Pattern:**
- **Allowlist validation** - Only permitted fields can be queried (prevents injection via column names)
- **Backtick quoting** - Field names are quoted but validated first
- **Parameterized values** - User input goes through `%s` placeholders (prevents injection via values)
- **Clear separation** - SQL structure is controlled by code, not user input

This pattern prevents both classic SQL injection (via values) and second-order injection (via dynamic field names)."""
            }
        ]

        template = ExampleTemplate(metadata, SQLInjectionGenerator.REAL_WORLD_CONTEXT)
        return template.create_example(conversations)

    @staticmethod
    def generate_javascript_nosql() -> Dict:
        """Generate NoSQL injection example"""
        metadata = {
            'lang': 'javascript',
            'category': 'injection',
            'subcategory': 'nosql_injection',
            'owasp_2021': 'A03:2021-Injection',
            'cwe': 'CWE-943',
            'severity': 'CRITICAL',
            'complexity': 'moderate'
        }

        conversations = [
            {
                'turn': 1,
                'from': 'human',
                'value': "Show me how to implement user authentication with MongoDB."
            },
            {
                'turn': 2,
                'from': 'assistant',
                'value': """I'll demonstrate both vulnerable and secure patterns for MongoDB authentication.

**Vulnerable Code (NoSQL Injection Risk):**
```javascript
const express = require('express');
const { MongoClient } = require('mongodb');

app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    const client = await MongoClient.connect('mongodb://localhost:27017');
    const db = client.db('myapp');

    // DANGEROUS: Direct object injection
    const user = await db.collection('users').findOne({
        username: username,
        password: password
    });

    client.close();

    if (user) {
        res.json({ success: true });
    } else {
        res.status(401).json({ success: false });
    }
});
```

**Why This Is Dangerous:**
An attacker can send this payload:
```json
{
  "username": {"$ne": null},
  "password": {"$ne": null}
}
```
This creates a query that matches ANY user where username and password exist, bypassing authentication entirely.

**Secure Implementation:**
```javascript
const express = require('express');
const { MongoClient } = require('mongodb');
const bcrypt = require('bcrypt');

app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    // Input validation - ensure strings only
    if (typeof username !== 'string' || typeof password !== 'string') {
        return res.status(400).json({ error: 'Invalid input types' });
    }

    // Length validation
    if (username.length === 0 || username.length > 100) {
        return res.status(400).json({ error: 'Invalid username length' });
    }

    const client = await MongoClient.connect('mongodb://localhost:27017');
    const db = client.db('myapp');

    try {
        // Safe query with validated strings
        const user = await db.collection('users').findOne({
            username: username  // Now guaranteed to be a string
        });

        if (!user) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }

        // Verify password using bcrypt
        const isValid = await bcrypt.compare(password, user.passwordHash);

        if (isValid) {
            // Generate session token (implementation not shown)
            res.json({ success: true, token: generateToken(user.id) });
        } else {
            res.status(401).json({ error: 'Invalid credentials' });
        }
    } finally {
        client.close();
    }
});
```

**Key Security Controls:**
1. **Type validation** - Ensure inputs are primitive strings, not objects
2. **Length validation** - Prevent excessively long inputs
3. **Password hashing** - Use bcrypt, never store plaintext
4. **Constant-time responses** - Don't reveal whether username exists
5. **Error handling** - Generic error messages prevent enumeration"""
            },
            {
                'turn': 3,
                'from': 'human',
                'value': "What about building dynamic queries for search functionality?"
            },
            {
                'turn': 4,
                'from': 'assistant',
                'value': """For dynamic MongoDB queries, use strict validation and query builders:

```javascript
function buildSafeQuery(filters) {
    // Define allowed fields and operators
    const ALLOWED_FIELDS = new Set(['name', 'email', 'status', 'role', 'created']);
    const ALLOWED_OPERATORS = new Set(['$eq', '$gt', '$lt', '$in']);

    const query = {};

    for (const [field, value] of Object.entries(filters)) {
        // Validate field name
        if (!ALLOWED_FIELDS.has(field)) {
            throw new Error(`Invalid field: ${field}`);
        }

        // Handle operator objects
        if (typeof value === 'object' && value !== null) {
            // Ensure only allowed operators
            const operators = Object.keys(value);
            if (!operators.every(op => ALLOWED_OPERATORS.has(op))) {
                throw new Error(`Invalid operator in field: ${field}`);
            }

            // Validate operator values are primitives
            for (const [op, opValue] of Object.entries(value)) {
                if (typeof opValue === 'object' && !Array.isArray(opValue)) {
                    throw new Error(`Invalid operator value type`);
                }
            }

            query[field] = value;
        } else {
            // Simple equality check
            query[field] = value;
        }
    }

    return query;
}

// Usage
app.get('/users/search', async (req, res) => {
    try {
        const safeQuery = buildSafeQuery(req.query);

        const users = await db.collection('users').find(safeQuery).toArray();

        res.json({ users });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});
```

**Security Pattern:**
- **Allowlist validation** for both field names and operators
- **Type checking** for all values (prevent object injection)
- **Explicit operator control** - Only specific MongoDB operators allowed
- **Input sanitization** - Reject nested objects unless explicitly allowed

This prevents attackers from injecting dangerous operators like `$where` or `$regex`."""
            }
        ]

        template = ExampleTemplate(metadata)
        return template.create_example(conversations)


class DatasetGenerator:
    """Main dataset generation orchestrator"""

    def __init__(self, taxonomy_path: Path, schema_path: Path, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load taxonomy
        with open(taxonomy_path) as f:
            self.taxonomy = yaml.safe_load(f)

        # Initialize validator
        self.validator = DatasetValidator(schema_path)

        # Track generated examples
        self.examples = []
        self.generators = {
            'sql_injection': SQLInjectionGenerator,
            # More generators will be added
        }

    def generate_category(self, category_name: str, target_count: int) -> List[Dict]:
        """Generate examples for a specific category"""
        category = self.taxonomy['categories'][category_name]
        examples = []

        print(f"\nGenerating {category_name} examples (target: {target_count})...")

        for subcategory in category['subcategories']:
            subcat_name = subcategory['name']
            target = subcategory['examples']

            print(f"  - {subcat_name}: {target} examples")

            # Get generator for this subcategory
            generator_class = self.generators.get(subcat_name)

            if generator_class:
                # Generate examples using specialized generator
                # (This is a simplified version - real implementation would generate multiple examples)
                if hasattr(generator_class, f'generate_python_basic'):
                    example = generator_class.generate_python_basic()
                    examples.append(example)

                if hasattr(generator_class, f'generate_javascript_nosql'):
                    example = generator_class.generate_javascript_nosql()
                    examples.append(example)
            else:
                print(f"    ⚠ No generator for {subcat_name} yet")

        return examples

    def validate_and_save(self, examples: List[Dict], split: str = 'train') -> None:
        """Validate examples and save to file"""
        print(f"\nValidating {len(examples)} examples...")

        # Run validation
        summary = self.validator.validate_dataset(examples)

        print(f"\nValidation Summary:")
        print(f"  Total: {summary['total_examples']}")
        print(f"  Passed: {summary['passed']} ({summary['pass_rate']:.1f}%)")
        print(f"  Failed: {summary['failed']}")

        if summary['failed'] > 0:
            print(f"\nFailed examples:")
            for failed in summary['failed_examples'][:5]:  # Show first 5
                print(f"  - {failed['id']}: {len(failed['issues'])} issues")

        # Save validated examples
        output_file = self.output_dir / f'{split}.jsonl'
        with open(output_file, 'w') as f:
            for example in examples:
                f.write(json.dumps(example) + '\n')

        print(f"\n✓ Saved to {output_file}")

        # Save validation report
        report_file = self.output_dir.parent / 'validation' / f'{split}_validation_report.json'
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w') as f:
            json.dumps(summary, indent=2)

        print(f"✓ Validation report saved to {report_file}")

    def generate_dataset(self) -> None:
        """Generate complete dataset"""
        print("=" * 60)
        print("SecureCode v2.0 Dataset Generation")
        print("=" * 60)

        # Generate OWASP Top 10 categories first (priority 1)
        owasp_categories = [
            ('broken_access_control', 150),
            ('cryptographic_failures', 120),
            ('injection', 140),
            ('insecure_design', 80),
            ('security_misconfiguration', 100),
            ('vulnerable_components', 60),
            ('auth_failures', 130),
            ('integrity_failures', 70),
            ('logging_failures', 50),
            ('ssrf', 40),
        ]

        all_examples = []

        for category, target_count in owasp_categories:
            examples = self.generate_category(category, target_count)
            all_examples.extend(examples)

        # Split dataset (80/10/10)
        total = len(all_examples)
        train_size = int(total * 0.8)
        val_size = int(total * 0.1)

        train_examples = all_examples[:train_size]
        val_examples = all_examples[train_size:train_size + val_size]
        test_examples = all_examples[train_size + val_size:]

        # Validate and save each split
        self.validate_and_save(train_examples, 'train')
        self.validate_and_save(val_examples, 'validation')
        self.validate_and_save(test_examples, 'test')

        print("\n" + "=" * 60)
        print("Dataset generation complete!")
        print("=" * 60)


if __name__ == '__main__':
    # Configuration
    base_dir = Path(__file__).parent.parent
    taxonomy_path = base_dir / 'taxonomy.yaml'
    schema_path = base_dir / 'schema.json'
    output_dir = base_dir / 'data'

    # Initialize generator
    generator = DatasetGenerator(taxonomy_path, schema_path, output_dir)

    # Generate dataset
    generator.generate_dataset()
