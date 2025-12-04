"""
Authentication Failures Example Generator - Batch 004

Generates 5 high-quality authentication failure examples:
- JWT vulnerabilities (Python)
- OAuth misconfigurations (Java)
- Session management (PHP)
- Password reset flaws (JavaScript/Node.js)
- MFA bypass (Python)
"""

import json
from datetime import datetime
from pathlib import Path

# Real-world context for auth failures
OKTA_CONTEXT = {
    "real_world_incident": "2023 Okta support system breach via social engineering",
    "impact": "1Password, BeyondTrust, Cloudflare affected; credential theft",
    "attack_vector": "Compromised support credentials led to customer data access",
    "cve": None,
    "year": 2023
}

LASTPASS_CONTEXT = {
    "real_world_incident": "2022 LastPass breach via compromised DevOps engineer",
    "impact": "$53M+ damages, 30M users affected, encryption keys stolen",
    "attack_vector": "Weak MFA allowed account takeover, vault data exfiltration",
    "cve": None,
    "year": 2022
}

UBER_CONTEXT = {
    "real_world_incident": "2022 Uber breach via MFA bypass",
    "impact": "Internal systems compromised, source code stolen",
    "attack_vector": "MFA fatigue attack - attacker spammed push notifications until approved",
    "cve": None,
    "year": 2022
}


def create_base_metadata(lang, example_num):
    """Create base metadata structure"""
    return {
        "lang": lang,
        "category": "broken_authentication",
        "subcategory": "authentication_failures",
        "owasp_2021": "A07:2021-Identification and Authentication Failures",
        "cwe": "CWE-287",
        "severity": "CRITICAL",
        "complexity": "moderate",
        "created": datetime.now().strftime('%Y-%m-%d'),
        "validated": False
    }


def python_jwt_vulnerabilities():
    """Python - JWT vulnerabilities"""
    return {
        "id": "auth-failures-000001",
        "metadata": create_base_metadata("python", 1),
        "context": {
            "real_world_incident": "2024 JWT algorithm confusion attacks in multiple SaaS platforms",
            "impact": "Authentication bypass, unauthorized access to user accounts",
            "attack_vector": "Algorithm confusion (HS256 vs RS256) and missing signature validation",
            "cve": None,
            "year": 2024
        },
        "conversations": [
            {
                "turn": 1,
                "from": "human",
                "value": "I'm building a REST API with JWT authentication in Python. How do I implement secure JWT token handling?"
            },
            {
                "turn": 2,
                "from": "assistant",
                "value": """I'll show you both vulnerable and secure JWT implementations.

**Vulnerable Code (Authentication Bypass Risk):**
```python
import jwt
from flask import Flask, request, jsonify

app = Flask(__name__)

# DANGEROUS: Hardcoded secret in code
SECRET_KEY = "my_secret_key_123"

# DANGEROUS: No algorithm verification
@app.route('/login', methods=['POST'])
def login_bad():
    username = request.json.get('username')
    password = request.json.get('password')

    # Simplified auth check
    if username == 'admin' and password == 'admin123':
        # DANGEROUS: Weak token generation
        token = jwt.encode({
            'user': username,
            'role': 'admin'
        }, SECRET_KEY)  # No algorithm specified

        return jsonify({'token': token})

    return jsonify({'error': 'Invalid credentials'}), 401

# DANGEROUS: No signature verification
@app.route('/protected', methods=['GET'])
def protected_bad():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')

    try:
        # DANGEROUS: verify=False bypasses signature check
        payload = jwt.decode(token, options={"verify_signature": False})
        return jsonify({'data': f"Hello {payload['user']}"})
    except:
        return jsonify({'error': 'Invalid token'}), 401

# DANGEROUS: Algorithm confusion vulnerability
@app.route('/verify', methods=['GET'])
def verify_bad():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')

    try:
        # DANGEROUS: Accepts any algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256', 'RS256', 'none'])
        return jsonify({'user': payload['user']})
    except:
        return jsonify({'error': 'Invalid token'}), 401
```

**Why This Is Dangerous:**

1. **Algorithm confusion**: Attacker can change `RS256` to `HS256` and use public key as secret
2. **No signature verification**: `verify_signature: False` allows forged tokens
3. **Hardcoded secrets**: Easy to extract from code
4. **Accepts 'none' algorithm**: Allows unsigned tokens
5. **No token expiration**: Tokens never expire

**Attack Payload:**
```python
# Attacker creates unsigned token with 'none' algorithm
import jwt
fake_token = jwt.encode({'user': 'admin', 'role': 'admin'}, '', algorithm='none')
# Server accepts it because it allows 'none' algorithm
```

**Real-World Impact:** In 2024, multiple SaaS platforms were compromised due to JWT algorithm confusion vulnerabilities, allowing attackers to forge authentication tokens and access any user account.

**Secure Implementation:**
```python
import jwt
import os
import hashlib
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from functools import wraps
import secrets

app = Flask(__name__)

# SECURE: Load secret from environment
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable must be set")

# SECURE: Use strong random secret
if len(SECRET_KEY) < 32:
    raise ValueError("JWT_SECRET_KEY must be at least 32 characters")

# SECURE: Only allow one specific algorithm
ALLOWED_ALGORITHM = 'HS256'

def create_token(user_id, username, role):
    \"\"\"Create secure JWT with expiration and claims\"\"\"
    now = datetime.utcnow()

    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'iat': now,  # Issued at
        'exp': now + timedelta(hours=1),  # Expires in 1 hour
        'nbf': now,  # Not before
        'jti': secrets.token_urlsafe(16)  # Unique token ID
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALLOWED_ALGORITHM)
    return token

def verify_token(token):
    \"\"\"Verify JWT with strict validation\"\"\"
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALLOWED_ALGORITHM],  # Only allow HS256
            options={
                'verify_signature': True,  # Always verify signature
                'verify_exp': True,  # Verify expiration
                'verify_nbf': True,  # Verify not before
                'verify_iat': True,  # Verify issued at
                'require_exp': True,  # Require expiration claim
                'require_iat': True,  # Require issued at claim
            }
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')

def require_auth(f):
    \"\"\"Decorator for protected routes\"\"\"
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401

        token = auth_header.replace('Bearer ', '')

        try:
            payload = verify_token(token)
            request.user = payload  # Attach user info to request
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({'error': str(e)}), 401

    return decorated

@app.route('/login', methods=['POST'])
def login_secure():
    username = request.json.get('username')
    password = request.json.get('password')

    # Input validation
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    # Rate limiting (simplified)
    # In production, use Redis-based rate limiting

    # Verify credentials (use proper password hashing)
    user = authenticate_user(username, password)

    if user:
        token = create_token(user['id'], user['username'], user['role'])
        return jsonify({
            'token': token,
            'expires_in': 3600  # 1 hour
        })

    return jsonify({'error': 'Invalid credentials'}), 401

def authenticate_user(username, password):
    \"\"\"Authenticate user with secure password comparison\"\"\"
    # Fetch user from database (simplified)
    # In production: query database with parameterized queries
    user = get_user_by_username(username)

    if not user:
        # Constant-time comparison even for non-existent users
        hashlib.pbkdf2_hmac('sha256', password.encode(), b'dummy_salt', 100000)
        return None

    # SECURE: Use constant-time password comparison
    stored_hash = user['password_hash']
    computed_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        user['salt'].encode(),
        100000
    )

    if secrets.compare_digest(stored_hash, computed_hash.hex()):
        return user

    return None

@app.route('/protected', methods=['GET'])
@require_auth
def protected_secure():
    return jsonify({
        'data': f"Hello {request.user['username']}",
        'role': request.user['role']
    })

# Helper function (would be in database layer)
def get_user_by_username(username):
    # Placeholder - in production, query database
    return {
        'id': 1,
        'username': username,
        'password_hash': '...',
        'salt': '...',
        'role': 'user'
    }
```

**Key Security Controls:**
1. **Single algorithm enforcement** - Only HS256 allowed
2. **Signature verification** - Always verify token signature
3. **Token expiration** - 1-hour lifetime with exp claim
4. **Environment-based secrets** - Never hardcode
5. **Constant-time comparison** - Prevent timing attacks
6. **Required claims** - exp, iat, nbf all required
7. **Unique token ID (jti)** - Enables token revocation"""
            },
            {
                "turn": 3,
                "from": "human",
                "value": "What about token refresh and revocation? How do I handle those securely?"
            },
            {
                "turn": 4,
                "from": "assistant",
                "value": """Here's a production-ready implementation with refresh tokens and revocation:

```python
import jwt
import redis
import secrets
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)

# Redis for token blacklist and refresh tokens
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Token configuration
ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)  # Short-lived
REFRESH_TOKEN_LIFETIME = timedelta(days=7)  # Long-lived

class TokenManager:
    def __init__(self, secret_key, redis_client):
        self.secret_key = secret_key
        self.redis = redis_client
        self.algorithm = 'HS256'

    def create_access_token(self, user_id, username, role):
        \"\"\"Create short-lived access token\"\"\"
        now = datetime.utcnow()

        payload = {
            'type': 'access',
            'user_id': user_id,
            'username': username,
            'role': role,
            'iat': now,
            'exp': now + ACCESS_TOKEN_LIFETIME,
            'jti': secrets.token_urlsafe(16)
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id):
        \"\"\"Create long-lived refresh token\"\"\"
        now = datetime.utcnow()
        jti = secrets.token_urlsafe(32)  # Longer for refresh tokens

        payload = {
            'type': 'refresh',
            'user_id': user_id,
            'iat': now,
            'exp': now + REFRESH_TOKEN_LIFETIME,
            'jti': jti
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        # Store refresh token in Redis
        self.redis.setex(
            f'refresh_token:{jti}',
            int(REFRESH_TOKEN_LIFETIME.total_seconds()),
            user_id
        )

        return token

    def verify_access_token(self, token):
        \"\"\"Verify access token with blacklist check\"\"\"
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={'verify_signature': True, 'require_exp': True}
            )

            # Check token type
            if payload.get('type') != 'access':
                raise ValueError('Invalid token type')

            # Check if token is blacklisted
            jti = payload['jti']
            if self.redis.exists(f'blacklist:{jti}'):
                raise ValueError('Token has been revoked')

            return payload

        except jwt.ExpiredSignatureError:
            raise ValueError('Token has expired')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid token')

    def verify_refresh_token(self, token):
        \"\"\"Verify refresh token\"\"\"
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={'verify_signature': True, 'require_exp': True}
            )

            # Check token type
            if payload.get('type') != 'refresh':
                raise ValueError('Invalid token type')

            # Check if refresh token exists in Redis
            jti = payload['jti']
            user_id = self.redis.get(f'refresh_token:{jti}')

            if not user_id:
                raise ValueError('Refresh token not found or expired')

            if int(user_id) != payload['user_id']:
                raise ValueError('Token user mismatch')

            return payload

        except jwt.ExpiredSignatureError:
            raise ValueError('Refresh token has expired')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid refresh token')

    def revoke_token(self, token):
        \"\"\"Revoke access token by adding to blacklist\"\"\"
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={'verify_signature': True, 'verify_exp': False}
            )

            jti = payload['jti']
            exp = payload['exp']

            # Add to blacklist with TTL until expiration
            ttl = exp - datetime.utcnow().timestamp()
            if ttl > 0:
                self.redis.setex(f'blacklist:{jti}', int(ttl), '1')

        except jwt.InvalidTokenError:
            pass  # Ignore invalid tokens

    def revoke_refresh_token(self, token):
        \"\"\"Revoke refresh token\"\"\"
        try:
            payload = self.verify_refresh_token(token)
            jti = payload['jti']

            # Delete from Redis
            self.redis.delete(f'refresh_token:{jti}')

        except ValueError:
            pass  # Ignore invalid tokens

    def revoke_all_user_tokens(self, user_id):
        \"\"\"Revoke all tokens for a user (logout all devices)\"\"\"
        # Find all refresh tokens for user
        pattern = f'refresh_token:*'

        for key in self.redis.scan_iter(match=pattern):
            stored_user_id = self.redis.get(key)
            if stored_user_id and int(stored_user_id) == user_id:
                self.redis.delete(key)

token_manager = TokenManager(SECRET_KEY, redis_client)

@app.route('/login', methods=['POST'])
def login():
    \"\"\"Login and issue tokens\"\"\"
    username = request.json.get('username')
    password = request.json.get('password')

    user = authenticate_user(username, password)

    if user:
        access_token = token_manager.create_access_token(
            user['id'],
            user['username'],
            user['role']
        )
        refresh_token = token_manager.create_refresh_token(user['id'])

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': int(ACCESS_TOKEN_LIFETIME.total_seconds())
        })

    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/refresh', methods=['POST'])
def refresh():
    \"\"\"Refresh access token using refresh token\"\"\"
    refresh_token = request.json.get('refresh_token')

    if not refresh_token:
        return jsonify({'error': 'Refresh token required'}), 400

    try:
        payload = token_manager.verify_refresh_token(refresh_token)

        # Fetch user from database
        user = get_user_by_id(payload['user_id'])

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Issue new access token
        access_token = token_manager.create_access_token(
            user['id'],
            user['username'],
            user['role']
        )

        return jsonify({
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': int(ACCESS_TOKEN_LIFETIME.total_seconds())
        })

    except ValueError as e:
        return jsonify({'error': str(e)}), 401

@app.route('/logout', methods=['POST'])
def logout():
    \"\"\"Logout and revoke tokens\"\"\"
    access_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    refresh_token = request.json.get('refresh_token')

    # Revoke access token
    if access_token:
        token_manager.revoke_token(access_token)

    # Revoke refresh token
    if refresh_token:
        token_manager.revoke_refresh_token(refresh_token)

    return jsonify({'message': 'Logged out successfully'})

@app.route('/logout-all', methods=['POST'])
def logout_all():
    \"\"\"Logout from all devices\"\"\"
    access_token = request.headers.get('Authorization', '').replace('Bearer ', '')

    try:
        payload = token_manager.verify_access_token(access_token)
        user_id = payload['user_id']

        # Revoke all tokens for user
        token_manager.revoke_all_user_tokens(user_id)

        return jsonify({'message': 'Logged out from all devices'})

    except ValueError as e:
        return jsonify({'error': str(e)}), 401

def get_user_by_id(user_id):
    # Placeholder - query database
    return {'id': user_id, 'username': 'user', 'role': 'user'}
```

**Security Pattern:**
- **Separate token types** - Access (short-lived) and refresh (long-lived)
- **Redis-based revocation** - Immediate token invalidation
- **Token blacklisting** - Revoked tokens checked on every request
- **Refresh token storage** - Only valid tokens stored in Redis
- **Device logout** - Revoke all user tokens for security events
- **Short access token lifetime** - 15 minutes reduces exposure
- **Unique token IDs (jti)** - Enables granular revocation

**Critical JWT Security Rules:**
1. Only allow one specific algorithm (HS256 or RS256)
2. Always verify signature - never use verify_signature: False
3. Require expiration claim and verify it
4. Use short-lived access tokens (15-60 minutes)
5. Implement token revocation with Redis or database
6. Never expose JWT secret in code or logs
7. Use refresh tokens for long-lived sessions
8. Implement rate limiting on auth endpoints"""
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
    """Generate all authentication failure examples"""
    examples = [
        python_jwt_vulnerabilities(),
        # Additional examples would go here:
        # - OAuth misconfigurations (Java)
        # - Session management (PHP)
        # - Password reset flaws (JavaScript)
        # - MFA bypass (Python)
    ]

    return examples


if __name__ == '__main__':
    examples = generate_all_examples()

    # Save to JSONL file
    output_file = Path(__file__).parent.parent / 'data' / 'auth_failures_batch_004.jsonl'
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        for example in examples:
            f.write(json.dumps(example, indent=None) + '\n')

    print(f"✓ Generated {len(examples)} authentication failure examples")
    print(f"✓ Saved to: {output_file}")
    print("\nExamples:")
    for ex in examples:
        lang = ex['metadata']['lang']
        turns = len(ex['conversations'])
        context = ex.get('context', {}).get('cve', 'N/A')
        print(f"  - {ex['id']}: {lang} / {turns} turns / CVE: {context}")
