#!/usr/bin/env python3
"""
Pydantic Quick Reference Guide
=============================

Essential patterns and examples for Pydantic usage.
"""

from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
import json

# ==============================================================================
# 1. BASIC MODEL
# ==============================================================================

class User(BaseModel):
    name: str
    age: int
    email: str

# Usage:
user = User(name="Alice", age=30, email="alice@example.com")
print(f"User: {user}")
print(f"As dict: {user.model_dump()}")
print(f"As JSON: {user.model_dump_json()}")

# ==============================================================================
# 2. FIELD CONSTRAINTS
# ==============================================================================

class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0, description="Must be positive")
    quantity: int = Field(ge=0, le=1000)
    tags: List[str] = Field(default_factory=list, max_length=5)
    description: Optional[str] = Field(None, max_length=200)

# Common Field constraints:
# - min_length, max_length: for strings and lists
# - gt, ge, lt, le: for numbers (greater than, greater/equal, less than, less/equal)
# - pattern: regex pattern for strings
# - default, default_factory: default values

# ==============================================================================
# 3. VALIDATION ERROR HANDLING
# ==============================================================================

def safe_create_user(data: dict):
    """Safely create a user with error handling"""
    try:
        return User(**data)
    except ValidationError as e:
        print("❌ Validation errors:")
        for error in e.errors():
            field = error['loc'][0]
            message = error['msg']
            value = error.get('input')
            print(f"  • {field}: {message} (got: {value})")
        return None

# Test validation errors:
invalid_data = {"name": "Bob", "age": "not_a_number"}
safe_create_user(invalid_data)

# ==============================================================================
# 4. NESTED MODELS
# ==============================================================================

class Address(BaseModel):
    street: str = Field(min_length=5)
    city: str
    postal_code: str = Field(pattern=r'^\d{5}$')
    country: str = Field(default="USA")

class Person(BaseModel):
    name: str
    age: int = Field(ge=0, le=150)
    address: Address
    friends: List['Person'] = Field(default_factory=list)  # Self-reference

# Usage:
address = Address(street="123 Main St", city="New York", postal_code="10001")
person = Person(name="John", age=30, address=address)

# ==============================================================================
# 5. USEFUL METHODS
# ==============================================================================

# Convert to dictionary
data_dict = person.model_dump()

# Convert to JSON string
json_str = person.model_dump_json(indent=2)

# Create from dictionary
person_copy = Person.model_validate(data_dict)

# Create from JSON string
person_from_json = Person.model_validate_json(json_str)

# ==============================================================================
# 6. COMMON PATTERNS
# ==============================================================================

# Optional fields with defaults
class Config(BaseModel):
    debug: bool = Field(default=False)
    max_connections: int = Field(default=100, ge=1, le=1000)
    timeout: float = Field(default=30.0, gt=0)

# Lists with constraints
class Team(BaseModel):
    name: str
    members: List[Person] = Field(min_length=1, max_length=20)
    
    def add_member(self, person: Person):
        self.members.append(person)

# Computed properties (not serialized)
class Circle(BaseModel):
    radius: float = Field(gt=0)
    
    @property
    def area(self) -> float:
        return 3.14159 * self.radius ** 2

print("\n" + "="*50)
print("Quick Reference Examples Complete!")
print("="*50)