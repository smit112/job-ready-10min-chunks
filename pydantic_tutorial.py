#!/usr/bin/env python3
"""
Pydantic 2 Tutorial - Step by Step Guide
========================================

This tutorial covers:
1. Installing and verifying Pydantic 2
2. Creating simple BaseModel and input data
3. Adding field constraints
4. Handling and printing validation errors
5. Using nested models for parent/child relationships
"""

import sys
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator
from datetime import datetime

def step1_install_and_verify():
    """Step 1: Install and verify Pydantic 2"""
    print("=" * 60)
    print("STEP 1: Installing and Verifying Pydantic 2")
    print("=" * 60)
    
    try:
        import pydantic
        print(f"✓ Pydantic version: {pydantic.__version__}")
        
        if pydantic.__version__.startswith('2'):
            print("✓ Pydantic 2 is installed and ready to use!")
        else:
            print("⚠ You have Pydantic version", pydantic.__version__)
            print("  To install Pydantic 2, run: pip install pydantic>=2.0.0")
            
    except ImportError:
        print("✗ Pydantic is not installed")
        print("  To install Pydantic 2, run: pip install pydantic>=2.0.0")
        return False
    
    return True

def step2_simple_model():
    """Step 2: Create a simple BaseModel and input data"""
    print("\n" + "=" * 60)
    print("STEP 2: Simple BaseModel and Input Data")
    print("=" * 60)
    
    # Define a simple model
    class User(BaseModel):
        name: str
        age: int
        email: str
        is_active: bool = True  # Default value
    
    # Create instances with different input types
    print("Creating User instances...")
    
    # From dictionary
    user_data = {
        "name": "Alice Johnson",
        "age": 30,
        "email": "alice@example.com"
    }
    user1 = User(**user_data)
    print(f"✓ User from dict: {user1}")
    
    # From keyword arguments
    user2 = User(name="Bob Smith", age=25, email="bob@example.com", is_active=False)
    print(f"✓ User from kwargs: {user2}")
    
    # Access model data
    print(f"✓ User name: {user1.name}")
    print(f"✓ User age: {user1.age}")
    print(f"✓ User email: {user1.email}")
    print(f"✓ User is_active: {user1.is_active}")
    
    # Convert back to dictionary
    user_dict = user1.model_dump()
    print(f"✓ User as dict: {user_dict}")

def step3_field_constraints():
    """Step 3: Add field constraints"""
    print("\n" + "=" * 60)
    print("STEP 3: Field Constraints")
    print("=" * 60)
    
    class Product(BaseModel):
        name: str = Field(..., min_length=2, max_length=100)
        price: float = Field(..., gt=0)  # Greater than 0
        quantity: int = Field(..., ge=0)  # Greater than or equal to 0
        category: str = Field(..., pattern=r"^[A-Za-z\s]+$")  # Letters and spaces only
        description: Optional[str] = Field(None, max_length=500)
        
        @field_validator('name')
        @classmethod
        def validate_name(cls, v):
            if v.strip() != v:
                raise ValueError('Name cannot have leading or trailing spaces')
            return v.title()  # Capitalize first letter of each word
    
    print("Creating Product with valid data...")
    
    # Valid product
    product_data = {
        "name": "laptop computer",
        "price": 999.99,
        "quantity": 10,
        "category": "Electronics",
        "description": "High-performance laptop for work and gaming"
    }
    
    try:
        product = Product(**product_data)
        print(f"✓ Valid product created: {product}")
        print(f"✓ Name after validation: '{product.name}'")  # Should be "Laptop Computer"
    except ValidationError as e:
        print(f"✗ Validation error: {e}")

def step4_validation_errors():
    """Step 4: Handle and print validation errors"""
    print("\n" + "=" * 60)
    print("STEP 4: Handling Validation Errors")
    print("=" * 60)
    
    class Employee(BaseModel):
        name: str = Field(..., min_length=1, max_length=50)
        age: int = Field(..., ge=18, le=65)
        salary: float = Field(..., gt=0)
        department: str = Field(..., min_length=2)
    
    print("Testing validation errors with invalid data...")
    
    # Invalid data that will trigger multiple errors
    invalid_data = {
        "name": "",  # Empty string (min_length=1)
        "age": 16,   # Too young (ge=18)
        "salary": -1000,  # Negative salary (gt=0)
        "department": "A"  # Too short (min_length=2)
    }
    
    try:
        employee = Employee(**invalid_data)
        print(f"✓ Employee created: {employee}")
    except ValidationError as e:
        print("✗ Validation errors occurred:")
        print(f"  Number of errors: {len(e.errors())}")
        
        for i, error in enumerate(e.errors(), 1):
            print(f"  Error {i}:")
            print(f"    Field: {error['loc']}")
            print(f"    Type: {error['type']}")
            print(f"    Message: {error['msg']}")
            print(f"    Input: {error['input']}")
            print()

def step5_nested_models():
    """Step 5: Use nested models for parent/child relationships"""
    print("\n" + "=" * 60)
    print("STEP 5: Nested Models - Parent/Child Relationships")
    print("=" * 60)
    
    # Child model
    class Address(BaseModel):
        street: str = Field(..., min_length=5)
        city: str = Field(..., min_length=2)
        state: str = Field(..., min_length=2, max_length=2)
        zip_code: str = Field(..., pattern=r"^\d{5}(-\d{4})?$")
    
    # Another child model
    class PhoneNumber(BaseModel):
        type: str = Field(..., pattern=r"^(home|work|mobile)$")
        number: str = Field(..., pattern=r"^\d{3}-\d{3}-\d{4}$")
    
    # Parent model with nested children
    class Customer(BaseModel):
        id: int = Field(..., gt=0)
        name: str = Field(..., min_length=2)
        email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
        addresses: List[Address] = Field(..., min_length=1)
        phone_numbers: List[PhoneNumber] = Field(default_factory=list)
        created_at: datetime = Field(default_factory=datetime.now)
    
    print("Creating Customer with nested Address and PhoneNumber models...")
    
    # Valid nested data
    customer_data = {
        "id": 1001,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "addresses": [
            {
                "street": "123 Main Street",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001"
            },
            {
                "street": "456 Oak Avenue",
                "city": "Los Angeles", 
                "state": "CA",
                "zip_code": "90210-1234"
            }
        ],
        "phone_numbers": [
            {
                "type": "mobile",
                "number": "555-123-4567"
            },
            {
                "type": "work",
                "number": "555-987-6543"
            }
        ]
    }
    
    try:
        customer = Customer(**customer_data)
        print(f"✓ Customer created successfully!")
        print(f"✓ Customer ID: {customer.id}")
        print(f"✓ Customer name: {customer.name}")
        print(f"✓ Number of addresses: {len(customer.addresses)}")
        print(f"✓ Number of phone numbers: {len(customer.phone_numbers)}")
        
        # Access nested data
        print(f"✓ Primary address: {customer.addresses[0].street}, {customer.addresses[0].city}")
        print(f"✓ Mobile phone: {customer.phone_numbers[0].number}")
        
        # Convert to dictionary
        customer_dict = customer.model_dump()
        print(f"✓ Customer as dict (first few keys): {list(customer_dict.keys())}")
        
    except ValidationError as e:
        print(f"✗ Validation error: {e}")

def step6_complex_validation_example():
    """Step 6: Complex validation with nested models and errors"""
    print("\n" + "=" * 60)
    print("STEP 6: Complex Validation with Nested Models")
    print("=" * 60)
    
    class OrderItem(BaseModel):
        product_id: int = Field(..., gt=0)
        quantity: int = Field(..., gt=0, le=100)
        unit_price: float = Field(..., gt=0)
    
    class Order(BaseModel):
        order_id: str = Field(..., pattern=r"^ORD-\d{6}$")
        customer_id: int = Field(..., gt=0)
        items: List[OrderItem] = Field(..., min_length=1)
        total_amount: float = Field(..., gt=0)
        
        @field_validator('total_amount')
        @classmethod
        def validate_total_amount(cls, v, info):
            # Calculate expected total from items
            items = info.data.get('items', [])
            expected_total = sum(item.quantity * item.unit_price for item in items)
            
            if abs(v - expected_total) > 0.01:  # Allow small floating point differences
                raise ValueError(f'Total amount {v} does not match sum of items {expected_total}')
            return v
    
    print("Testing complex validation with nested models...")
    
    # Invalid order data
    invalid_order_data = {
        "order_id": "INVALID-123",  # Wrong format
        "customer_id": 0,  # Invalid (gt=0)
        "items": [
            {
                "product_id": 1,
                "quantity": 5,
                "unit_price": 10.0
            },
            {
                "product_id": 2,
                "quantity": 0,  # Invalid (gt=0)
                "unit_price": 15.0
            }
        ],
        "total_amount": 100.0  # Wrong total (should be 5*10 + 0*15 = 50)
    }
    
    try:
        order = Order(**invalid_order_data)
        print(f"✓ Order created: {order}")
    except ValidationError as e:
        print("✗ Complex validation errors:")
        for i, error in enumerate(e.errors(), 1):
            print(f"  Error {i}:")
            print(f"    Location: {' -> '.join(str(loc) for loc in error['loc'])}")
            print(f"    Type: {error['type']}")
            print(f"    Message: {error['msg']}")
            print(f"    Input: {error['input']}")
            print()

def main():
    """Run all tutorial steps"""
    print("Pydantic 2 Tutorial - Complete Guide")
    print("=" * 60)
    
    # Step 1: Install and verify
    if not step1_install_and_verify():
        print("\nPlease install Pydantic 2 first: pip install pydantic>=2.0.0")
        return
    
    # Step 2: Simple model
    step2_simple_model()
    
    # Step 3: Field constraints
    step3_field_constraints()
    
    # Step 4: Validation errors
    step4_validation_errors()
    
    # Step 5: Nested models
    step5_nested_models()
    
    # Step 6: Complex validation
    step6_complex_validation_example()
    
    print("\n" + "=" * 60)
    print("Tutorial Complete! 🎉")
    print("=" * 60)
    print("You've learned:")
    print("✓ How to install and verify Pydantic 2")
    print("✓ Creating simple BaseModel instances")
    print("✓ Adding field constraints and validators")
    print("✓ Handling and displaying validation errors")
    print("✓ Building nested parent/child relationships")
    print("✓ Complex validation scenarios")

if __name__ == "__main__":
    main()