#!/usr/bin/env python3
"""
Expand SQL Injection Batch 001 from 5 to 10 examples.
Adds examples 016-020 with diverse language and framework coverage.
"""

import json
from pathlib import Path
from datetime import date


def create_base_metadata(language, example_num, subcategory="sql_injection"):
    """Create base metadata for SQL injection examples."""
    return {
        "lang": language,
        "category": "injection",
        "subcategory": subcategory,
        "owasp_2021": "A03:2021-Injection",
        "cwe": "CWE-89",
        "severity": "CRITICAL",
        "complexity": "moderate",
        "created": str(date.today()),
        "validated": False
    }


def example_016_csharp_entity_framework():
    """C# Entity Framework - SQL Injection via Raw SQL"""

    user_turn_1 = "I'm using Entity Framework Core in C#. Can I safely use raw SQL queries with user input?"

    assistant_turn_1 = """I'll show you the dangerous pattern first, then the secure implementation with Entity Framework Core.

**VULNERABLE CODE - DO NOT USE:**

```csharp
using Microsoft.EntityFrameworkCore;
using System.Linq;

public class ProductRepository
{
    private readonly AppDbContext _context;

    public ProductRepository(AppDbContext context)
    {
        _context = context;
    }

    public List<Product> SearchProducts(string searchTerm)
    {
        // DANGER: String concatenation in raw SQL
        string sql = "SELECT * FROM Products WHERE Name LIKE '%" +
                     searchTerm + "%' OR Description LIKE '%" + searchTerm + "%'";

        return _context.Products.FromSqlRaw(sql).ToList();
    }

    public Product GetProductById(string productId)
    {
        // DANGER: String interpolation in raw SQL
        return _context.Products
            .FromSqlRaw($"SELECT * FROM Products WHERE ProductId = '{productId}'")
            .FirstOrDefault();
    }
}
```

**Attack Payloads:**

```sql
-- Search: ' OR '1'='1
-- Result: SELECT * FROM Products WHERE Name LIKE '%' OR '1'='1%'

-- Product ID: ' OR '1'='1' --
-- Result: SELECT * FROM Products WHERE ProductId = '' OR '1'='1' --'

-- Union attack: ' UNION SELECT username, password, email FROM Users --
```

**SECURE IMPLEMENTATION:**

```csharp
using Microsoft.EntityFrameworkCore;
using System.Linq;

public class SecureProductRepository
{
    private readonly AppDbContext _context;

    public SecureProductRepository(AppDbContext context)
    {
        _context = context;
    }

    // Method 1: Use LINQ (Preferred)
    public List<Product> SearchProductsLinq(string searchTerm)
    {
        if (string.IsNullOrWhiteSpace(searchTerm))
            return new List<Product>();

        // LINQ automatically parameterizes
        return _context.Products
            .Where(p => EF.Functions.Like(p.Name, $"%{searchTerm}%") ||
                       EF.Functions.Like(p.Description, $"%{searchTerm}%"))
            .ToList();
    }

    // Method 2: Parameterized Raw SQL
    public List<Product> SearchProductsRawSql(string searchTerm)
    {
        if (string.IsNullOrWhiteSpace(searchTerm))
            return new List<Product>();

        // Use parameterized queries with FromSqlRaw
        string sql = "SELECT * FROM Products WHERE Name LIKE {0} OR Description LIKE {0}";
        string parameter = $"%{searchTerm}%";

        return _context.Products
            .FromSqlRaw(sql, parameter)
            .ToList();
    }

    // Method 3: FromSqlInterpolated (EF Core 3.0+)
    public Product GetProductByIdSafe(string productId)
    {
        // FormattableString automatically parameterizes
        return _context.Products
            .FromSqlInterpolated($"SELECT * FROM Products WHERE ProductId = {productId}")
            .FirstOrDefault();
    }
}
```

**Key Security Principles:**

1. **Prefer LINQ**: Automatically parameterized and type-safe
2. **FromSqlInterpolated**: Use for interpolated strings (auto-parameterizes)
3. **FromSqlRaw with params**: Explicitly pass parameters
4. **Never**: String concatenation or manual interpolation in SQL
"""

    user_turn_2 = "What about dynamic filtering with multiple optional search criteria?"

    assistant_turn_2 = """For dynamic queries with optional filters, use LINQ's conditional building pattern:

```csharp
using Microsoft.EntityFrameworkCore;
using System.Linq;

public class ProductSearchCriteria
{
    public string Name { get; set; }
    public decimal? MinPrice { get; set; }
    public decimal? MaxPrice { get; set; }
    public string Category { get; set; }
    public bool? InStock { get; set; }
}

public class AdvancedProductRepository
{
    private readonly AppDbContext _context;

    public AdvancedProductRepository(AppDbContext context)
    {
        _context = context;
    }

    public List<Product> SearchProducts(ProductSearchCriteria criteria)
    {
        // Start with base query
        IQueryable<Product> query = _context.Products;

        // Conditionally add filters (all automatically parameterized)
        if (!string.IsNullOrWhiteSpace(criteria.Name))
        {
            query = query.Where(p => EF.Functions.Like(p.Name, $"%{criteria.Name}%"));
        }

        if (criteria.MinPrice.HasValue)
        {
            query = query.Where(p => p.Price >= criteria.MinPrice.Value);
        }

        if (criteria.MaxPrice.HasValue)
        {
            query = query.Where(p => p.Price <= criteria.MaxPrice.Value);
        }

        if (!string.IsNullOrWhiteSpace(criteria.Category))
        {
            query = query.Where(p => p.Category == criteria.Category);
        }

        if (criteria.InStock.HasValue)
        {
            query = query.Where(p => p.InStock == criteria.InStock.Value);
        }

        // Execute query
        return query.ToList();
    }

    // Alternative: Specification Pattern for complex queries
    public List<Product> SearchWithSpecification(ISpecification<Product> specification)
    {
        return _context.Products
            .Where(specification.ToExpression())
            .ToList();
    }
}

// Specification interface
public interface ISpecification<T>
{
    Expression<Func<T, bool>> ToExpression();
}

// Example specification
public class ProductNameContainsSpecification : ISpecification<Product>
{
    private readonly string _searchTerm;

    public ProductNameContainsSpecification(string searchTerm)
    {
        _searchTerm = searchTerm;
    }

    public Expression<Func<Product, bool>> ToExpression()
    {
        return product => product.Name.Contains(_searchTerm);
    }
}
```

**Best Practices:**

1. **IQueryable Composition**: Build queries conditionally
2. **All filters parameterized**: LINQ handles this automatically
3. **Specification Pattern**: Encapsulates business logic
4. **Input Validation**: Check for null/empty before filtering
5. **Never use raw SQL**: For dynamic queries unless absolutely necessary

```csharp
// API Controller example
public class ProductsController : ControllerBase
{
    private readonly AdvancedProductRepository _repository;

    public ProductsController(AdvancedProductRepository repository)
    {
        _repository = repository;
    }

    public IActionResult Search([FromQuery] ProductSearchCriteria criteria)
    {
        // Validate input
        if (criteria.MinPrice < 0 || criteria.MaxPrice < 0)
            return BadRequest("Prices cannot be negative");

        if (criteria.MinPrice > criteria.MaxPrice)
            return BadRequest("Min price cannot exceed max price");

        var results = _repository.SearchProducts(criteria);
        return Ok(results);
    }
}
```

This approach provides maximum flexibility while maintaining complete SQL injection protection."""

    metadata = create_base_metadata("c#", 16)

    return {
        "id": "sql-injection-000016",
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata,
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


def example_017_ruby_activerecord():
    """Ruby ActiveRecord - SQL Injection Prevention"""

    user_turn_1 = "I'm using Rails ActiveRecord. How do I safely query the database with user input?"

    assistant_turn_1 = """I'll demonstrate vulnerable patterns and secure ActiveRecord usage.

**VULNERABLE CODE - DO NOT USE:**

```ruby
# app/models/user.rb
class User < ApplicationRecord
  def self.search_by_email(email)
    # DANGER: String interpolation in where clause
    where("email = '#{email}'").first
  end

  def self.find_by_role_and_status(role, status)
    # DANGER: Direct string concatenation
    where("role = '" + role + "' AND status = '" + status + "'")
  end

  def self.search_users(search_term)
    # DANGER: Raw SQL with interpolation
    find_by_sql("SELECT * FROM users WHERE name LIKE '%#{search_term}%'")
  end
end
```

**Attack Payloads:**

```ruby
# Email: ' OR '1'='1
# Query: SELECT * FROM users WHERE email = '' OR '1'='1'

# Role: admin' --
# Query: SELECT * FROM users WHERE role = 'admin' --' AND status = 'active'
```

**SECURE IMPLEMENTATION:**

```ruby
# app/models/user.rb
class User < ApplicationRecord
  # Method 1: Hash conditions (preferred)
  def self.search_by_email_safe(email)
    where(email: email).first
  end

  # Method 2: Parameterized conditions
  def self.find_by_role_and_status_safe(role, status)
    where("role = ? AND status = ?", role, status)
  end

  # Method 3: Named parameters
  def self.search_with_criteria(role: nil, status: nil, active_since: nil)
    query = all

    query = query.where("role = :role", role: role) if role.present?
    query = query.where("status = :status", status: status) if status.present?
    query = query.where("created_at >= :date", date: active_since) if active_since.present?

    query
  end

  # Method 4: LIKE queries (parameterized)
  def self.search_users_safe(search_term)
    return none if search_term.blank?

    # Parameterized LIKE query
    where("name LIKE ? OR email LIKE ?", "%#{sanitize_sql_like(search_term)}%",
          "%#{sanitize_sql_like(search_term)}%")
  end

  # Method 5: ARel for complex queries
  def self.advanced_search(criteria)
    query = arel_table

    conditions = []
    conditions << query[:name].matches("%#{criteria[:name]}%") if criteria[:name].present?
    conditions << query[:role].eq(criteria[:role]) if criteria[:role].present?
    conditions << query[:created_at].gteq(criteria[:start_date]) if criteria[:start_date].present?

    where(conditions.reduce(:and))
  end
end
```

**Security Features:**

1. **Hash Conditions**: Automatically escaped
2. **Question Mark Placeholders**: Parameterized queries
3. **Named Placeholders**: Clear parameter binding
4. **sanitize_sql_like**: Escapes LIKE wildcards
5. **ARel**: Type-safe query builder
"""

    user_turn_2 = "How do I handle complex search with multiple optional filters securely?"

    assistant_turn_2 = """For complex dynamic searches, use scope chaining or the ransack gem:

```ruby
# app/models/product.rb
class Product < ApplicationRecord
  # Define reusable scopes
  scope :by_name, ->(name) { where("name LIKE ?", "%#{sanitize_sql_like(name)}%") if name.present? }
  scope :by_category, ->(category) { where(category: category) if category.present? }
  scope :by_price_range, ->(min, max) { where("price BETWEEN ? AND ?", min, max) if min && max }
  scope :in_stock, -> { where("inventory_count > ?", 0) }
  scope :active, -> { where(status: 'active') }

  # Combine scopes dynamically
  def self.advanced_search(params)
    products = all

    products = products.by_name(params[:name])
    products = products.by_category(params[:category])
    products = products.by_price_range(params[:min_price], params[:max_price])
    products = products.in_stock if params[:in_stock] == 'true'
    products = products.active if params[:active_only] == 'true'

    products
  end
end

# app/controllers/products_controller.rb
class ProductsController < ApplicationController
  def search
    # All parameters are safely handled by scopes
    products = Product.advanced_search(search_params)

    render json: products
  end

  private

  def search_params
    params.permit(:name, :category, :min_price, :max_price, :in_stock, :active_only)
  end
end
```

**Production-Grade Search Service:**

```ruby
# app/services/product_search_service.rb
class ProductSearchService
  def initialize(params)
    params = params
    validate_params
  end

  def execute
    query = Product.all

    apply_filters(query)
  end

  private

  def validate_params
    # Validate numeric inputs
    if params[:min_price] && params[:min_price].to_f < 0
      raise ArgumentError, "Min price cannot be negative"
    end

    if params[:max_price] && params[:max_price].to_f < 0
      raise ArgumentError, "Max price cannot be negative"
    end

    # Validate string lengths
    if params[:name] && params[:name].length > 100
      raise ArgumentError, "Search term too long"
    end
  end

  def apply_filters(query)
    query = filter_by_name(query)
    query = filter_by_category(query)
    query = filter_by_price(query)
    query = filter_by_availability(query)
    query
  end

  def filter_by_name(query)
    return query unless params[:name].present?

    sanitized = Product.sanitize_sql_like(params[:name])
    query.where("name LIKE ? OR description LIKE ?", "%#{sanitized}%", "%#{sanitized}%")
  end

  def filter_by_category(query)
    return query unless params[:category].present?

    # Use allowlist for categories
    allowed_categories = ['electronics', 'books', 'clothing', 'home']
    return query unless allowed_categories.include?(params[:category])

    query.where(category: params[:category])
  end

  def filter_by_price(query)
    query = query.where("price >= ?", params[:min_price]) if params[:min_price].present?
    query = query.where("price <= ?", params[:max_price]) if params[:max_price].present?
    query
  end

  def filter_by_availability(query)
    return query unless params[:in_stock] == 'true'

    query.where("inventory_count > 0")
  end
end

# Usage:
# products = ProductSearchService.new(params).execute
```

**Key Principles:**

1. **Scope Composition**: Reusable, testable query segments
2. **Service Objects**: Encapsulate complex search logic
3. **Input Validation**: Validate before querying
4. **Allowlisting**: For categories, statuses, etc.
5. **sanitize_sql_like**: Always escape LIKE patterns
6. **Strong Parameters**: Controller-level input filtering

This approach provides flexible, maintainable, and completely SQL-injection-proof search functionality."""

    metadata = create_base_metadata("ruby", 17)

    return {
        "id": "sql-injection-000017",
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata,
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


def example_018_typescript_typeorm():
    """TypeScript TypeORM - SQL Injection Prevention"""

    user_turn_1 = "I'm using TypeORM with TypeScript. How do I prevent SQL injection in my queries?"

    assistant_turn_1 = """I'll show you vulnerable patterns and secure TypeORM practices.

**VULNERABLE CODE - DO NOT USE:**

```javascript
const express = require('express');
const { getRepository } = require('typeorm');
const { User } = require('./entities/User');

const router = express.Router();

router.get('/users/search', async (req, res) => {
    const email = req.query.email;

    // DANGER: String template in raw query
    const users = await getRepository(User)
        .createQueryBuilder('user')
        .where(`user.email = '${email}'`)
        .getMany();

    res.json(users);
});

router.get('/users/filter', async (req, res) => {
    const role = req.query.role;
    const status = req.query.status;

    // DANGER: String concatenation
    const query = "SELECT * FROM users WHERE role = '" + role +
                  "' AND status = '" + status + "'";

    const users = await getRepository(User).query(query);
    res.json(users);
});

module.exports = router;
```

**Attack Payloads:**

```
GET /users/search?email=' OR '1'='1
GET /users/filter?role=admin' --&status=active
```

**SECURE IMPLEMENTATION:**

```javascript
const express = require('express');
const { getRepository } = require('typeorm');
const { User } = require('./entities/User');

const router = express.Router();

// Method 1: Named parameters (preferred)
router.get('/users/search', async (req, res) => {
    const { email } = req.query;

    const users = await getRepository(User)
        .createQueryBuilder('user')
        .where('user.email = :email', { email })
        .getMany();

    res.json(users);
});

// Method 2: Question mark parameters
router.get('/users/by-role', async (req, res) => {
    const { role, status } = req.query;

    const users = await getRepository(User)
        .createQueryBuilder('user')
        .where('user.role = ? AND user.status = ?', [role, status])
        .getMany();

    res.json(users);
});

// Method 3: Repository methods (safest)
router.get('/users/find', async (req, res) => {
    const { email, role } = req.query;

    const users = await getRepository(User).find({
        where: {
            email: email,
            role: role
        }
    });

    res.json(users);
});

// Method 4: Query builder with andWhere
router.get('/users/advanced', async (req, res) => {
    const { minAge, maxAge, city } = req.query;

    let query = getRepository(User).createQueryBuilder('user');

    if (minAge) {
        query = query.andWhere('user.age >= :minAge', { minAge: parseInt(minAge) });
    }

    if (maxAge) {
        query = query.andWhere('user.age <= :maxAge', { maxAge: parseInt(maxAge) });
    }

    if (city) {
        query = query.andWhere('user.city = :city', { city });
    }

    const users = await query.getMany();
    res.json(users);
});

module.exports = router;
```

**Key Security Features:**

1. **Named Parameters**: `:paramName` with object binding
2. **Positional Parameters**: `?` with array binding
3. **Repository Find**: Object-based queries
4. **Query Builder**: Fluent API with parameterization
"""

    user_turn_2 = "How do I handle LIKE searches and complex filtering securely?"

    assistant_turn_2 = """For LIKE searches and complex filters, use TypeORM's query builder with parameter binding:

```javascript
const express = require('express');
const { getRepository, Brackets } = require('typeorm');
const { Product } = require('./entities/Product');

const router = express.Router();

// Secure LIKE search
router.get('/products/search', async (req, res) => {
    try {
        const { query } = req.query;

        if (!query || query.length > 100) {
            return res.status(400).json({ error: 'Invalid search query' });
        }

        // Parameterized LIKE query
        const products = await getRepository(Product)
            .createQueryBuilder('product')
            .where('product.name LIKE :searchTerm', {
                searchTerm: `%${query}%`
            })
            .orWhere('product.description LIKE :searchTerm', {
                searchTerm: `%${query}%`
            })
            .getMany();

        res.json(products);
    } catch (error) {
        res.status(500).json({ error: 'Search failed' });
    }
});

// Complex filtering with multiple conditions
router.get('/products/filter', async (req, res) => {
    try {
        const filters = validateFilters(req.query);

        const queryBuilder = getRepository(Product)
            .createQueryBuilder('product');

        // Apply filters conditionally
        if (filters.name) {
            queryBuilder.andWhere('product.name LIKE :name', {
                name: `%${filters.name}%`
            });
        }

        if (filters.category) {
            queryBuilder.andWhere('product.category = :category', {
                category: filters.category
            });
        }

        if (filters.minPrice !== undefined) {
            queryBuilder.andWhere('product.price >= :minPrice', {
                minPrice: filters.minPrice
            });
        }

        if (filters.maxPrice !== undefined) {
            queryBuilder.andWhere('product.price <= :maxPrice', {
                maxPrice: filters.maxPrice
            });
        }

        // Complex OR conditions with Brackets
        if (filters.tags && filters.tags.length > 0) {
            queryBuilder.andWhere(new Brackets(qb => {
                filters.tags.forEach((tag, index) => {
                    qb.orWhere(`product.tags LIKE :tag${index}`, {
                        [`tag${index}`]: `%${tag}%`
                    });
                });
            }));
        }

        const products = await queryBuilder.getMany();
        res.json(products);

    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// Helper: Validate and sanitize filters
function validateFilters(queryParams) {
    const filters = {};

    // Validate name
    if (queryParams.name && typeof queryParams.name === 'string') {
        filters.name = queryParams.name.substring(0, 100);
    }

    // Validate category (allowlist)
    const allowedCategories = ['electronics', 'books', 'clothing', 'home'];
    if (queryParams.category && allowedCategories.includes(queryParams.category)) {
        filters.category = queryParams.category;
    }

    // Validate prices
    if (queryParams.minPrice) {
        const minPrice = parseFloat(queryParams.minPrice);
        if (!isNaN(minPrice) && minPrice >= 0) {
            filters.minPrice = minPrice;
        }
    }

    if (queryParams.maxPrice) {
        const maxPrice = parseFloat(queryParams.maxPrice);
        if (!isNaN(maxPrice) && maxPrice >= 0) {
            filters.maxPrice = maxPrice;
        }
    }

    // Validate tags
    if (queryParams.tags) {
        filters.tags = Array.isArray(queryParams.tags)
            ? queryParams.tags.slice(0, 5)
            : [queryParams.tags];
    }

    return filters;
}

module.exports = router;
```

**Production Service Class:**

```javascript
class ProductSearchService {
    constructor(private productRepository) {}

    async search(criteria) {
        this.validateCriteria(criteria);

        const queryBuilder = this.productRepository
            .createQueryBuilder('product');

        this.applyTextSearch(queryBuilder, criteria.searchTerm);
        this.applyFilters(queryBuilder, criteria);
        this.applySorting(queryBuilder, criteria.sortBy, criteria.sortOrder);
        this.applyPagination(queryBuilder, criteria.page, criteria.limit);

        const [products, total] = await queryBuilder.getManyAndCount();

        return {
            products,
            total,
            page: criteria.page,
            limit: criteria.limit
        };
    }

    private applyTextSearch(qb, searchTerm) {
        if (!searchTerm) return;

        qb.andWhere(
            new Brackets(subQb => {
                subQb.where('product.name LIKE :term', { term: `%${searchTerm}%` })
                     .orWhere('product.description LIKE :term', { term: `%${searchTerm}%` });
            })
        );
    }

    private applyFilters(qb, criteria) {
        if (criteria.category) {
            qb.andWhere('product.category = :category', {
                category: criteria.category
            });
        }

        if (criteria.minPrice) {
            qb.andWhere('product.price >= :minPrice', {
                minPrice: criteria.minPrice
            });
        }

        if (criteria.maxPrice) {
            qb.andWhere('product.price <= :maxPrice', {
                maxPrice: criteria.maxPrice
            });
        }

        if (criteria.inStock) {
            qb.andWhere('product.stockQuantity > 0');
        }
    }

    private applySorting(qb, sortBy, sortOrder) {
        const allowedSortFields = ['name', 'price', 'createdAt'];
        const field = allowedSortFields.includes(sortBy) ? sortBy : 'createdAt';
        const order = sortOrder === 'ASC' ? 'ASC' : 'DESC';

        qb.orderBy(`product.${field}`, order);
    }

    private applyPagination(qb, page, limit) {
        const pageNum = Math.max(1, parseInt(page) || 1);
        const limitNum = Math.min(100, Math.max(1, parseInt(limit) || 20));

        qb.skip((pageNum - 1) * limitNum).take(limitNum);
    }

    private validateCriteria(criteria) {
        if (criteria.searchTerm && criteria.searchTerm.length > 200) {
            throw new Error('Search term too long');
        }

        if (criteria.minPrice && criteria.maxPrice &&
            criteria.minPrice > criteria.maxPrice) {
            throw new Error('Min price cannot exceed max price');
        }
    }
}
```

**Best Practices:**

1. **Always Parameterize**: Use named or positional parameters
2. **Validate Input**: Check types, ranges, lengths
3. **Allowlist Values**: For categories, sort fields, etc.
4. **Use Brackets**: For complex OR conditions
5. **Limit Results**: Prevent resource exhaustion
6. **Service Pattern**: Encapsulate query logic

This ensures complete SQL injection protection while maintaining query flexibility."""

    metadata = create_base_metadata("typescript", 18)

    return {
        "id": "sql-injection-000018",
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata,
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


def example_019_kotlin_exposed():
    """Kotlin Exposed Framework - SQL Injection Prevention"""

    user_turn_1 = "I'm using Kotlin with the Exposed SQL framework. How do I prevent SQL injection?"

    assistant_turn_1 = """I'll demonstrate vulnerable patterns and secure Exposed framework usage.

**VULNERABLE CODE - DO NOT USE:**

```kotlin
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction

object Users : Table() {
    val id = integer("id").autoIncrement()
    val email = varchar("email", 255)
    val role = varchar("role", 50)
    val status = varchar("status", 50)

    override val primaryKey = PrimaryKey(id)
}

class UserRepository {
    // DANGER: String interpolation in raw SQL
    fun findByEmail(email: String): User? {
        return transaction {
            exec("SELECT * FROM users WHERE email = '$email'") { rs ->
                if (rs.next()) {
                    User(rs.getInt("id"), rs.getString("email"))
                } else null
            }
        }
    }

    // DANGER: String concatenation
    fun searchUsers(searchTerm: String): List<User> {
        return transaction {
            val sql = "SELECT * FROM users WHERE email LIKE '%" + searchTerm + "%'"
            exec(sql) { rs ->
                val users = mutableListOf<User>()
                while (rs.next()) {
                    users.add(User(rs.getInt("id"), rs.getString("email")))
                }
                users
            }
        }
    }
}
```

**Attack Payloads:**

```kotlin
// Email: ' OR '1'='1
// Search: %' OR '1'='1 --
```

**SECURE IMPLEMENTATION:**

```kotlin
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction

object Users : Table() {
    val id = integer("id").autoIncrement()
    val email = varchar("email", 255)
    val role = varchar("role", 50)
    val status = varchar("status", 50)
    val createdAt = long("created_at")

    override val primaryKey = PrimaryKey(id)
}

data class User(
    val id: Int,
    val email: String,
    val role: String,
    val status: String
)

class SecureUserRepository {
    // Method 1: DSL queries (preferred - automatically parameterized)
    fun findByEmailSafe(email: String): User? {
        return transaction {
            Users.select { Users.email eq email }
                .mapNotNull { rowToUser(it) }
                .singleOrNull()
        }
    }

    // Method 2: Multiple conditions
    fun findByRoleAndStatus(role: String, status: String): List<User> {
        return transaction {
            Users.select {
                (Users.role eq role) and (Users.status eq status)
            }.map { rowToUser(it) }
        }
    }

    // Method 3: LIKE queries (safe)
    fun searchByEmail(searchTerm: String): List<User> {
        return transaction {
            Users.select {
                Users.email like "%$searchTerm%"
            }.map { rowToUser(it) }
        }
    }

    // Method 4: Complex queries with AND/OR
    fun advancedSearch(
        email: String? = null,
        role: String? = null,
        minDate: Long? = null
    ): List<User> {
        return transaction {
            var query = Users.selectAll()

            email?.let { query = query.andWhere { Users.email like "%$it%" } }
            role?.let { query = query.andWhere { Users.role eq it } }
            minDate?.let { query = query.andWhere { Users.createdAt greaterEq it } }

            query.map { rowToUser(it) }
        }
    }

    private fun rowToUser(row: ResultRow): User {
        return User(
            id = row[Users.id],
            email = row[Users.email],
            role = row[Users.role],
            status = row[Users.status]
        )
    }
}
```

**Key Security Features:**

1. **DSL Queries**: Type-safe and automatically parameterized
2. **Infix Functions**: eq, like, and, or - all safe
3. **No Raw SQL**: Unless absolutely necessary
4. **Type Safety**: Kotlin's type system prevents many errors
"""

    user_turn_2 = "How do I build complex dynamic queries with optional filters securely?"

    assistant_turn_2 = """For complex dynamic queries in Exposed, use query composition with conditional building:

```kotlin
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction

data class ProductSearchCriteria(
    val name: String? = null,
    val category: String? = null,
    val minPrice: Double? = null,
    val maxPrice: Double? = null,
    val inStock: Boolean? = null,
    val tags: List<String>? = null
)

object Products : Table() {
    val id = integer("id").autoIncrement()
    val name = varchar("name", 255)
    val category = varchar("category", 100)
    val price = double("price")
    val stockQuantity = integer("stock_quantity")
    val tags = varchar("tags", 500)

    override val primaryKey = PrimaryKey(id)
}

class ProductSearchService {
    fun search(criteria: ProductSearchCriteria): List<Product> {
        validateCriteria(criteria)

        return transaction {
            var query = Products.selectAll()

            // Apply filters conditionally
            criteria.name?.let { name ->
                query = query.andWhere {
                    (Products.name like "%$name%") or
                    (Products.description like "%$name%")
                }
            }

            criteria.category?.let { category ->
                query = query.andWhere { Products.category eq category }
            }

            criteria.minPrice?.let { minPrice ->
                query = query.andWhere { Products.price greaterEq minPrice }
            }

            criteria.maxPrice?.let { maxPrice ->
                query = query.andWhere { Products.price lessEq maxPrice }
            }

            criteria.inStock?.let { inStock ->
                if (inStock) {
                    query = query.andWhere { Products.stockQuantity greater 0 }
                }
            }

            criteria.tags?.let { tagList ->
                if (tagList.isNotEmpty()) {
                    query = query.andWhere {
                        tagList.map { tag ->
                            Products.tags like "%$tag%"
                        }.reduce { a, b -> a or b }
                    }
                }
            }

            query.map { rowToProduct(it) }
        }
    }

    private fun validateCriteria(criteria: ProductSearchCriteria) {
        criteria.name?.let { name ->
            require(name.length <= 100) { "Search term too long" }
        }

        require(
            criteria.minPrice == null ||
            criteria.maxPrice == null ||
            criteria.minPrice <= criteria.maxPrice
        ) { "Min price cannot exceed max price" }

        criteria.tags?.let { tags ->
            require(tags.size <= 10) { "Too many tags" }
        }
    }

    private fun rowToProduct(row: ResultRow): Product {
        return Product(
            id = row[Products.id],
            name = row[Products.name],
            category = row[Products.category],
            price = row[Products.price],
            stockQuantity = row[Products.stockQuantity]
        )
    }
}
```

**Production-Grade Repository Pattern:**

```kotlin
interface ProductRepository {
    fun findById(id: Int): Product?
    fun search(criteria: ProductSearchCriteria): List<Product>
    fun findByCategory(category: String): List<Product>
}

class ExposedProductRepository : ProductRepository {
    override fun findById(id: Int): Product? = transaction {
        Products.select { Products.id eq id }
            .mapNotNull { rowToProduct(it) }
            .singleOrNull()
    }

    override fun search(criteria: ProductSearchCriteria): List<Product> = transaction {
        buildSearchQuery(criteria).map { rowToProduct(it) }
    }

    override fun findByCategory(category: String): List<Product> = transaction {
        // Validate category against allowlist
        val allowedCategories = listOf("electronics", "books", "clothing")
        require(category in allowedCategories) { "Invalid category" }

        Products.select { Products.category eq category }
            .map { rowToProduct(it) }
    }

    private fun buildSearchQuery(criteria: ProductSearchCriteria): Query {
        var query = Products.selectAll()

        criteria.name?.takeIf { it.isNotBlank() }?.let { name ->
            query = query.andWhere { Products.name like "%$name%" }
        }

        criteria.category?.let { category ->
            query = query.andWhere { Products.category eq category }
        }

        applyPriceFilter(query, criteria.minPrice, criteria.maxPrice)

        criteria.inStock?.let { inStock ->
            if (inStock) {
                query = query.andWhere { Products.stockQuantity greater 0 }
            }
        }

        return query
    }

    private fun applyPriceFilter(
        query: Query,
        minPrice: Double?,
        maxPrice: Double?
    ): Query {
        var result = query

        minPrice?.let { result = result.andWhere { Products.price greaterEq it } }
        maxPrice?.let { result = result.andWhere { Products.price lessEq it } }

        return result
    }

    private fun rowToProduct(row: ResultRow): Product {
        return Product(
            id = row[Products.id],
            name = row[Products.name],
            category = row[Products.category],
            price = row[Products.price],
            stockQuantity = row[Products.stockQuantity]
        )
    }
}

// Usage example
fun main() {
    Database.connect(
        "jdbc:postgresql://localhost:5432/mydb",
        driver = "org.postgresql.Driver",
        user = "user",
        password = "password"
    )

    val repository = ExposedProductRepository()

    val criteria = ProductSearchCriteria(
        name = "laptop",
        minPrice = 500.0,
        maxPrice = 2000.0,
        inStock = true
    )

    val products = repository.search(criteria)
    println("Found ${products.size} products")
}
```

**Best Practices:**

1. **Use DSL Always**: Exposed's DSL is completely SQL-injection-proof
2. **Conditional Building**: Apply filters only when present
3. **Validate Input**: Check ranges, lengths, formats
4. **Allowlist Enums**: For categories, statuses, sort fields
5. **Type Safety**: Leverage Kotlin's null-safety
6. **Repository Pattern**: Encapsulate data access logic

This provides maximum SQL injection protection while maintaining Kotlin's expressiveness and type safety."""

    metadata = create_base_metadata("kotlin", 19)

    return {
        "id": "sql-injection-000019",
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata,
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


def example_020_rust_sqlx():
    """Rust sqlx - SQL Injection Prevention"""

    user_turn_1 = "I'm using Rust with sqlx for database queries. How do I prevent SQL injection?"

    assistant_turn_1 = """I'll demonstrate vulnerable patterns and secure sqlx usage in Rust.

**VULNERABLE CODE - DO NOT USE:**

```rust
use sqlx::PgPool;

// DANGER: String formatting in SQL query
async fn find_user_by_email_unsafe(
    pool: &PgPool,
    email: &str
) -> Result<User, sqlx::Error> {
    // DANGER: format! macro with user input
    let query = format!("SELECT * FROM users WHERE email = '{}'", email);

    sqlx::query_as::<_, User>(&query)
        .fetch_one(pool)
        .await
}

// DANGER: String concatenation
async fn search_users_unsafe(
    pool: &PgPool,
    search_term: &str
) -> Result<Vec<User>, sqlx::Error> {
    let query = "SELECT * FROM users WHERE name LIKE '%".to_string() +
                search_term + "%'";

    sqlx::query_as::<_, User>(&query)
        .fetch_all(pool)
        .await
}
```

**Attack Payloads:**

```rust
// Email: ' OR '1'='1
// Search: %' OR '1'='1 --
```

**SECURE IMPLEMENTATION:**

```rust
use sqlx::PgPool;

// Method 1: Positional parameters (safest)
async fn find_user_by_email_safe(
    pool: &PgPool,
    email: &str
) -> Result<User, sqlx::Error> {
    sqlx::query_as::<_, User>("SELECT * FROM users WHERE email = $1")
        .bind(email)
        .fetch_one(pool)
        .await
}

// Method 2: Multiple parameters
async fn find_by_role_and_status(
    pool: &PgPool,
    role: &str,
    status: &str
) -> Result<Vec<User>, sqlx::Error> {
    sqlx::query_as::<_, User>(
        "SELECT * FROM users WHERE role = $1 AND status = $2"
    )
    .bind(role)
    .bind(status)
    .fetch_all(pool)
    .await
}

// Method 3: LIKE queries (parameterized)
async fn search_users_safe(
    pool: &PgPool,
    search_term: &str
) -> Result<Vec<User>, sqlx::Error> {
    let pattern = format!("%{}%", search_term);

    sqlx::query_as::<_, User>(
        "SELECT * FROM users WHERE name LIKE $1 OR email LIKE $1"
    )
    .bind(&pattern)
    .fetch_all(pool)
    .await
}

// Method 4: Compile-time checked queries with query! macro
async fn find_user_by_id(
    pool: &PgPool,
    id: i32
) -> Result<User, sqlx::Error> {
    // Compile-time SQL validation
    sqlx::query_as!(
        User,
        "SELECT id, email, role, status FROM users WHERE id = $1",
        id
    )
    .fetch_one(pool)
    .await
}
```

**Key Security Features:**

1. **Positional Parameters**: $1, $2, etc. - automatically escaped
2. **bind() Method**: Safe parameter binding
3. **query! Macro**: Compile-time SQL validation
4. **Type Safety**: Rust's type system prevents misuse
"""

    user_turn_2 = "How do I build complex dynamic queries with optional filters in Rust?"

    assistant_turn_2 = """For dynamic queries in Rust, use query building with conditional parameter binding:

```rust
use sqlx::{PgPool, Postgres, QueryBuilder};

pub struct ProductSearchCriteria {
    pub name: Option<String>,
    pub category: Option<String>,
    pub min_price: Option<f64>,
    pub max_price: Option<f64>,
    pub in_stock: Option<bool>,
}

impl ProductSearchCriteria {
    pub fn validate(&self) -> Result<(), String> {
        if let Some(ref name) = self.name {
            if name.len() > 100 {
                return Err("Search term too long".to_string());
            }
        }

        if let (Some(min), Some(max)) = (self.min_price, self.max_price) {
            if min > max {
                return Err("Min price cannot exceed max price".to_string());
            }
        }

        Ok(())
    }
}

pub async fn search_products(
    pool: &PgPool,
    criteria: &ProductSearchCriteria
) -> Result<Vec<Product>, sqlx::Error> {
    criteria.validate().map_err(|e| sqlx::Error::Protocol(e))?;

    let mut query_builder = QueryBuilder::<Postgres>::new(
        "SELECT id, name, category, price, stock_quantity FROM products WHERE 1=1"
    );

    // Conditionally add filters
    if let Some(ref name) = criteria.name {
        query_builder.push(" AND (name LIKE ");
        query_builder.push_bind(format!("%{}%", name));
        query_builder.push(" OR description LIKE ");
        query_builder.push_bind(format!("%{}%", name));
        query_builder.push(")");
    }

    if let Some(ref category) = criteria.category {
        query_builder.push(" AND category = ");
        query_builder.push_bind(category);
    }

    if let Some(min_price) = criteria.min_price {
        query_builder.push(" AND price >= ");
        query_builder.push_bind(min_price);
    }

    if let Some(max_price) = criteria.max_price {
        query_builder.push(" AND price <= ");
        query_builder.push_bind(max_price);
    }

    if let Some(in_stock) = criteria.in_stock {
        if in_stock {
            query_builder.push(" AND stock_quantity > 0");
        }
    }

    query_builder
        .build_query_as::<Product>()
        .fetch_all(pool)
        .await
}
```

**Production-Grade Repository Pattern:**

```rust
use async_trait::async_trait;
use sqlx::{PgPool, Postgres, QueryBuilder};

pub trait ProductRepository {
    async fn find_by_id(&self, id: i32) -> Result<Product, sqlx::Error>;
    async fn search(&self, criteria: &ProductSearchCriteria) -> Result<Vec<Product>, sqlx::Error>;
    async fn find_by_category(&self, category: &str) -> Result<Vec<Product>, sqlx::Error>;
}

pub struct SqlxProductRepository {
    pool: PgPool,
}

impl SqlxProductRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }

    fn build_search_query(&self, criteria: &ProductSearchCriteria) -> QueryBuilder<'_, Postgres> {
        let mut builder = QueryBuilder::new(
            "SELECT id, name, category, price, stock_quantity FROM products WHERE 1=1"
        );

        if let Some(ref name) = criteria.name {
            if !name.is_empty() {
                builder.push(" AND name LIKE ");
                builder.push_bind(format!("%{}%", name));
            }
        }

        if let Some(ref category) = criteria.category {
            // Validate against allowlist
            const ALLOWED_CATEGORIES: &[&str] = &["electronics", "books", "clothing", "home"];
            if ALLOWED_CATEGORIES.contains(&category.as_str()) {
                builder.push(" AND category = ");
                builder.push_bind(category);
            }
        }

        if let Some(min_price) = criteria.min_price {
            if min_price >= 0.0 {
                builder.push(" AND price >= ");
                builder.push_bind(min_price);
            }
        }

        if let Some(max_price) = criteria.max_price {
            if max_price >= 0.0 {
                builder.push(" AND price <= ");
                builder.push_bind(max_price);
            }
        }

        if let Some(true) = criteria.in_stock {
            builder.push(" AND stock_quantity > 0");
        }

        builder
    }
}

impl ProductRepository for SqlxProductRepository {
    async fn find_by_id(&self, id: i32) -> Result<Product, sqlx::Error> {
        sqlx::query_as!(
            Product,
            "SELECT id, name, category, price, stock_quantity FROM products WHERE id = $1",
            id
        )
        .fetch_one(&self.pool)
        .await
    }

    async fn search(&self, criteria: &ProductSearchCriteria) -> Result<Vec<Product>, sqlx::Error> {
        criteria.validate()
            .map_err(|e| sqlx::Error::Protocol(e))?;

        self.build_search_query(criteria)
            .build_query_as::<Product>()
            .fetch_all(&self.pool)
            .await
    }

    async fn find_by_category(&self, category: &str) -> Result<Vec<Product>, sqlx::Error> {
        const ALLOWED_CATEGORIES: &[&str] = &["electronics", "books", "clothing", "home"];

        if !ALLOWED_CATEGORIES.contains(&category) {
            return Err(sqlx::Error::Protocol("Invalid category".to_string()));
        }

        sqlx::query_as!(
            Product,
            "SELECT id, name, category, price, stock_quantity FROM products WHERE category = $1",
            category
        )
        .fetch_all(&self.pool)
        .await
    }
}

// Usage example
async fn example_usage() -> Result<(), Box<dyn std::error::Error>> {
    let pool = PgPool::connect("postgresql://user:pass@localhost/db").await?;
    let repo = SqlxProductRepository::new(pool);

    let criteria = ProductSearchCriteria {
        name: Some("laptop".to_string()),
        category: Some("electronics".to_string()),
        min_price: Some(500.0),
        max_price: Some(2000.0),
        in_stock: Some(true),
    };

    let products = repo.search(&criteria).await?;
    println!("Found {} products", products.len());

    Ok(())
}
```

**Best Practices:**

1. **Always Use bind()**: Never string interpolation
2. **QueryBuilder**: For dynamic queries
3. **query! Macro**: Compile-time SQL validation when possible
4. **Validate Input**: Before building queries
5. **Allowlist Values**: For categories, sort fields, etc.
6. **Repository Pattern**: Encapsulate data access
7. **Async/Await**: Leverage Rust's async runtime

Rust's type system combined with sqlx's parameter binding provides the strongest SQL injection protection available."""

    metadata = create_base_metadata("rust", 20)

    return {
        "id": "sql-injection-000020",
        "conversations": [
            {"turn": 1, "from": "human", "value": user_turn_1},
            {"turn": 2, "from": "assistant", "value": assistant_turn_1},
            {"turn": 3, "from": "human", "value": user_turn_2},
            {"turn": 4, "from": "assistant", "value": assistant_turn_2}
        ],
        "metadata": metadata,
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
    """Generate 5 new SQL injection examples to expand Batch 001."""

    examples = [
        example_016_csharp_entity_framework(),
        example_017_ruby_activerecord(),
        example_018_typescript_typeorm(),
        example_019_kotlin_exposed(),
        example_020_rust_sqlx()
    ]

    # Read existing batch 001
    batch_001_file = Path(__file__).parent.parent / 'data' / 'sql_injection_batch_001.jsonl'
    existing_examples = []

    with open(batch_001_file, 'r', encoding='utf-8') as f:
        for line in f:
            existing_examples.append(json.loads(line))

    print(f"Loaded {len(existing_examples)} existing examples from Batch 001")

    # Combine with new examples
    all_examples = existing_examples + examples

    # Write expanded batch
    with open(batch_001_file, 'w', encoding='utf-8') as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"\nExpanded Batch 001 to {len(all_examples)} examples")
    print(f"Output: {batch_001_file}")
    print("\nNew examples added:")
    for ex in examples:
        print(f"  {ex['id']}: {ex['metadata']['lang']}")

    return 0


if __name__ == "__main__":
    exit(main())
