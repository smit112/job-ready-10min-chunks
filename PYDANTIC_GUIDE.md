# Complete Pydantic 2 Guide - Step by Step

This guide walks you through all the essential Pydantic 2 concepts with practical examples and expected outputs.

## Prerequisites

- Python 3.7+
- Pydantic 2.x installed

## Installation

```bash
# Create virtual environment
python3 -m venv pydantic_env
source pydantic_env/bin/activate  # On Windows: pydantic_env\Scripts\activate

# Install Pydantic
pip install pydantic>=2.0.0
```

## Step 1: Installation and Verification

**Code:**
```python
import pydantic
print(f"Pydantic version: {pydantic.__version__}")

if pydantic.__version__.startswith('2'):
    print("✓ Pydantic 2 is installed and ready to use!")
```

**Expected Output:**
```
Pydantic version: 2.11.7
✓ Pydantic 2 is installed and ready to use!
```

## Step 2: Simple BaseModel and Input Data

**Code:**
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str
    is_active: bool = True  # Default value

# Create from dictionary
user_data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
user = User(**user_data)
print(f"User: {user}")
print(f"User name: {user.name}")
print(f"User as dict: {user.model_dump()}")
```

**Expected Output:**
```
User: name='Alice' age=30 email='alice@example.com' is_active=True
User name: Alice
User as dict: {'name': 'Alice', 'age': 30, 'email': 'alice@example.com', 'is_active': True}
```

**Key Concepts:**
- `BaseModel` is the core class for creating Pydantic models
- Type hints define the expected data types
- Default values can be specified with `= value`
- Models can be created from dictionaries using `**` unpacking
- `model_dump()` converts the model back to a dictionary

## Step 3: Field Constraints

**Code:**
```python
from pydantic import BaseModel, Field, field_validator

class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0)  # Greater than 0
    quantity: int = Field(..., ge=0)  # Greater than or equal to 0
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v.strip() != v:
            raise ValueError('Name cannot have leading/trailing spaces')
        return v.title()

# Valid product
product = Product(name="laptop", price=999.99, quantity=10)
print(f"Valid product: {product}")
print(f"Name after validation: '{product.name}'")
```

**Expected Output:**
```
Valid product: name='Laptop' price=999.99 quantity=10
Name after validation: 'Laptop'
```

**Key Concepts:**
- `Field()` allows you to specify validation constraints
- `...` means the field is required (no default value)
- `min_length`/`max_length`: String length constraints
- `gt` (greater than), `ge` (greater than or equal), `lt` (less than), `le` (less than or equal)
- `@field_validator` decorator for custom validation logic
- Validators can transform data (like `.title()` in this example)

## Step 4: Validation Errors

**Code:**
```python
from pydantic import BaseModel, Field, ValidationError

class Employee(BaseModel):
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=18)
    salary: float = Field(..., gt=0)

# Invalid data
try:
    employee = Employee(name="", age=16, salary=-1000)
except ValidationError as e:
    print("Validation errors:")
    for error in e.errors():
        print(f"  Field: {error['loc']}")
        print(f"  Error: {error['msg']}")
        print(f"  Input: {error['input']}")
```

**Expected Output:**
```
Validation errors:
  Field: ('name',)
  Error: String should have at least 1 character
  Input: 

  Field: ('age',)
  Error: Input should be greater than or equal to 18
  Input: 16

  Field: ('salary',)
  Error: Input should be greater than 0
  Input: -1000
```

**Key Concepts:**
- `ValidationError` is raised when data doesn't meet constraints
- `e.errors()` returns a list of all validation errors
- Each error contains:
  - `loc`: Field location (tuple)
  - `msg`: Human-readable error message
  - `input`: The invalid input value
  - `type`: Error type identifier

## Step 5: Nested Models

**Code:**
```python
from typing import List
from pydantic import BaseModel, Field

class Address(BaseModel):
    street: str = Field(..., min_length=5)
    city: str = Field(..., min_length=2)
    zip_code: str = Field(..., pattern=r"^\d{5}$")

class Customer(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=2)
    addresses: List[Address] = Field(..., min_length=1)

# Valid nested data
customer_data = {
    "id": 1001,
    "name": "John Doe",
    "addresses": [
        {"street": "123 Main Street", "city": "New York", "zip_code": "10001"},
        {"street": "456 Oak Avenue", "city": "Los Angeles", "zip_code": "90210"}
    ]
}

customer = Customer(**customer_data)
print(f"Customer: {customer.name}")
print(f"Number of addresses: {len(customer.addresses)}")
print(f"First address: {customer.addresses[0].street}, {customer.addresses[0].city}")
```

**Expected Output:**
```
Customer: John Doe
Number of addresses: 2
First address: 123 Main Street, New York
```

**Key Concepts:**
- Models can contain other models as fields
- `List[ModelType]` for lists of nested models
- Nested models are validated recursively
- Access nested data using dot notation: `customer.addresses[0].street`
- `pattern` constraint uses regex for string validation

## Step 6: Complex Validation

**Code:**
```python
from typing import List
from pydantic import BaseModel, Field, field_validator

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)

class Order(BaseModel):
    order_id: str = Field(..., pattern=r"^ORD-\d{6}$")
    items: List[OrderItem] = Field(..., min_length=1)
    total_amount: float = Field(..., gt=0)
    
    @field_validator('total_amount')
    @classmethod
    def validate_total_amount(cls, v, info):
        items = info.data.get('items', [])
        expected_total = sum(item.quantity * item.unit_price for item in items)
        
        if abs(v - expected_total) > 0.01:
            raise ValueError(f'Total amount {v} does not match sum of items {expected_total}')
        return v

# Valid order
order_data = {
    "order_id": "ORD-123456",
    "items": [
        {"product_id": 1, "quantity": 2, "unit_price": 10.0},
        {"product_id": 2, "quantity": 1, "unit_price": 15.0}
    ],
    "total_amount": 35.0  # 2*10 + 1*15 = 35
}

order = Order(**order_data)
print(f"Valid order: {order.order_id}")
print(f"Total amount: ${order.total_amount}")
```

**Expected Output:**
```
Valid order: ORD-123456
Total amount: $35.0
```

**Key Concepts:**
- Cross-field validation using `@field_validator`
- `info.data` contains all the data being validated
- Business logic validation (total amount must match sum of items)
- Complex regex patterns for string validation
- Floating-point comparison with tolerance for precision issues

## Common Field Constraints

| Constraint | Description | Example |
|------------|-------------|---------|
| `min_length` | Minimum string length | `Field(..., min_length=2)` |
| `max_length` | Maximum string length | `Field(..., max_length=100)` |
| `gt` | Greater than | `Field(..., gt=0)` |
| `ge` | Greater than or equal | `Field(..., ge=0)` |
| `lt` | Less than | `Field(..., lt=100)` |
| `le` | Less than or equal | `Field(..., le=100)` |
| `pattern` | Regex pattern | `Field(..., pattern=r"^\d{5}$")` |
| `default` | Default value | `Field(default="unknown")` |
| `default_factory` | Default factory function | `Field(default_factory=list)` |

## Common Use Cases

1. **API Request/Response Validation**
   ```python
   class UserCreate(BaseModel):
       name: str = Field(..., min_length=1)
       email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
   ```

2. **Configuration Validation**
   ```python
   class DatabaseConfig(BaseModel):
       host: str = Field(..., min_length=1)
       port: int = Field(..., ge=1, le=65535)
       database: str = Field(..., min_length=1)
   ```

3. **Data Transformation**
   ```python
   class User(BaseModel):
       name: str
       
       @field_validator('name')
       @classmethod
       def normalize_name(cls, v):
           return v.strip().title()
   ```

## Best Practices

1. **Use type hints** - They provide validation and IDE support
2. **Set appropriate constraints** - Don't be too permissive or restrictive
3. **Handle validation errors gracefully** - Always catch `ValidationError`
4. **Use meaningful field names** - Make your models self-documenting
5. **Test with invalid data** - Ensure your validation works as expected
6. **Use nested models** - Break complex data into logical components

## Running the Examples

1. **Full tutorial:** `python pydantic_tutorial.py`
2. **Simple examples:** `python simple_examples.py`

Both files demonstrate all concepts with detailed output and explanations.