#!/usr/bin/env python3
"""
Simple Pydantic 2 Examples
==========================

This file contains simple, focused examples of each Pydantic concept.
Run each example individually to understand the concepts better.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator

# Example 1: Basic Model Creation
print("=" * 50)
print("EXAMPLE 1: Basic Model Creation")
print("=" * 50)

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

# Example 2: Field Constraints
print("\n" + "=" * 50)
print("EXAMPLE 2: Field Constraints")
print("=" * 50)

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

# Example 3: Validation Errors
print("\n" + "=" * 50)
print("EXAMPLE 3: Validation Errors")
print("=" * 50)

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
        print()

# Example 4: Nested Models
print("=" * 50)
print("EXAMPLE 4: Nested Models")
print("=" * 50)

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

# Example 5: Complex Validation
print("\n" + "=" * 50)
print("EXAMPLE 5: Complex Validation")
print("=" * 50)

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

print("\n" + "=" * 50)
print("All examples completed successfully!")
print("=" * 50)