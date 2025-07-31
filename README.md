# Pydantic Tutorial: Complete Step-by-Step Guide

This repository contains a comprehensive tutorial for learning **Pydantic 2.x** (the latest stable version), covering everything from basic installation to advanced nested model validation.

## 🚀 Quick Start

### 1. Setup Virtual Environment
```bash
# Create virtual environment
python3 -m venv pydantic_env

# Activate it
source pydantic_env/bin/activate  # Linux/Mac
# or
pydantic_env\Scripts\activate     # Windows

# Install Pydantic
pip install pydantic
```

### 2. Verify Installation
```python
import pydantic
print(f"Pydantic version: {pydantic.__version__}")
```

## 📚 Tutorial Contents

### Step 1: Installation and Verification
- Setting up virtual environment
- Installing Pydantic 2.x
- Verifying the installation

### Step 2: Basic BaseModel Usage
- Creating simple models with typed fields
- Instantiating models with data
- Converting models to dictionaries and JSON
- Accessing model attributes

**Example:**
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

user = User(name="Alice", age=30, email="alice@example.com")
print(user.model_dump())  # Convert to dict
```

### Step 3: Field Constraints
- Adding validation rules with `Field()`
- Numeric constraints (gt, ge, lt, le)
- String constraints (min_length, max_length, pattern)
- Optional fields with defaults
- List constraints

**Example:**
```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0, description="Must be positive")
    quantity: int = Field(ge=0, le=1000)
```

### Step 4: Validation Error Handling
- Catching `ValidationError` exceptions
- Parsing error messages
- Understanding error structure
- Creating user-friendly error handling

**Example:**
```python
from pydantic import ValidationError

try:
    user = User(name="Bob", age="invalid")
except ValidationError as e:
    for error in e.errors():
        print(f"Field: {error['loc'][0]}, Error: {error['msg']}")
```

### Step 5: Nested Models
- Creating models with nested relationships
- One-to-one relationships (Person -> Address)
- One-to-many relationships (Company -> Employees)
- Self-referencing models
- Accessing nested data

**Example:**
```python
class Address(BaseModel):
    street: str
    city: str
    postal_code: str

class Person(BaseModel):
    name: str
    address: Address  # Nested model
```

### Step 6: Advanced Validation
- Nested validation errors
- Error path tracking
- Complex validation scenarios
- Custom error handling for nested structures

## 🏃‍♂️ Running the Tutorial

### Full Tutorial
```bash
source pydantic_env/bin/activate
python pydantic_tutorial.py
```

### Quick Reference
```bash
source pydantic_env/bin/activate
python pydantic_quick_reference.py
```

## 🔑 Key Pydantic Features Covered

### Core Features
- ✅ Type validation and automatic conversion
- ✅ Field constraints and validation rules
- ✅ Comprehensive error handling
- ✅ Nested model support
- ✅ Optional fields with defaults
- ✅ List and collection validation

### Common Field Constraints
```python
from pydantic import Field

# String constraints
name: str = Field(min_length=2, max_length=50)
email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')

# Numeric constraints  
age: int = Field(ge=0, le=150)  # greater/equal, less/equal
price: float = Field(gt=0)      # greater than
rating: float = Field(ge=1, le=5)

# List constraints
tags: List[str] = Field(max_length=10)
items: List[int] = Field(min_length=1)

# Optional with defaults
active: bool = Field(default=True)
created_at: datetime = Field(default_factory=datetime.now)
```

### Useful Model Methods
```python
# Convert to dictionary
data = model.model_dump()

# Convert to JSON string
json_str = model.model_dump_json(indent=2)

# Create from dictionary
model = MyModel.model_validate(data_dict)

# Create from JSON
model = MyModel.model_validate_json(json_string)
```

## 🎯 Expected Outputs

Each step in the tutorial shows:
- ✅ **Working code examples**
- 🔍 **Expected output** for each operation
- ❌ **Validation error examples** with clear explanations
- 📝 **Best practices** and common patterns

## 🚀 Next Steps

After completing this tutorial, explore:
- Custom validators with `@field_validator`
- Model configuration options
- Advanced field types (URLs, dates, UUIDs)
- Serialization customization
- Integration with FastAPI
- Performance optimization techniques

## 📖 Additional Resources

- [Official Pydantic Documentation](https://docs.pydantic.dev/)
- [Pydantic GitHub Repository](https://github.com/pydantic/pydantic)
- [FastAPI + Pydantic Integration](https://fastapi.tiangolo.com/)

---

**Note:** This tutorial uses Pydantic 2.x (currently 2.11.7), which is the latest stable version. Pydantic 3.x is not yet released, but all concepts covered here represent the modern, current approach to using Pydantic.
