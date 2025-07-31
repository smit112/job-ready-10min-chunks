#!/usr/bin/env python3
"""
Pydantic Tutorial: Step-by-Step Guide
=====================================

This script demonstrates:
1. Installation verification
2. Basic BaseModel usage
3. Field constraints
4. Validation error handling
5. Nested models for parent/child relationships
"""

import pydantic
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from datetime import datetime

def print_step(step_number: int, title: str):
    """Helper function to print step headers"""
    print(f"\n{'='*60}")
    print(f"STEP {step_number}: {title}")
    print(f"{'='*60}")

def print_output(description: str, output):
    """Helper function to print expected outputs"""
    print(f"\n🔍 {description}:")
    print(f"   {output}")

# ============================================================================
# STEP 1: Installation and Verification
# ============================================================================

print_step(1, "Installation and Verification")

print(f"✅ Pydantic version: {pydantic.__version__}")
print("✅ Installation successful!")

print_output("Expected output", "Pydantic version: 2.11.7 (or similar)")

# ============================================================================
# STEP 2: Create a Simple BaseModel and Input Data
# ============================================================================

print_step(2, "Create a Simple BaseModel and Input Data")

class User(BaseModel):
    """A simple user model"""
    name: str
    age: int
    email: str

# Creating valid user instances
print("\n📝 Creating User instances:")

# Valid data
user1 = User(name="Alice", age=30, email="alice@example.com")
print(f"User 1: {user1}")
print(f"User 1 name: {user1.name}")
print(f"User 1 age: {user1.age}")

# Using dictionary data
user_data = {"name": "Bob", "age": 25, "email": "bob@example.com"}
user2 = User(**user_data)
print(f"User 2: {user2}")

# Converting to dictionary
print(f"User 2 as dict: {user2.model_dump()}")

print_output("Expected output", """
User 1: name='Alice' age=30 email='alice@example.com'
User 1 name: Alice
User 1 age: 30
User 2: name='Bob' age=25 email='bob@example.com'  
User 2 as dict: {'name': 'Bob', 'age': 25, 'email': 'bob@example.com'}
""")

# ============================================================================
# STEP 3: Add Field Constraints
# ============================================================================

print_step(3, "Add Field Constraints")

class Product(BaseModel):
    """A product model with field constraints"""
    name: str = Field(min_length=2, max_length=50, description="Product name")
    price: float = Field(gt=0, description="Price must be positive")
    quantity: int = Field(ge=0, description="Quantity must be non-negative")
    description: Optional[str] = Field(None, max_length=200)
    tags: List[str] = Field(default_factory=list, max_length=10)

print("\n📝 Creating Product with constraints:")

# Valid product
product1 = Product(
    name="Laptop",
    price=999.99,
    quantity=5,
    description="High-performance laptop",
    tags=["electronics", "computer"]
)
print(f"Valid product: {product1}")

# Product with default values
product2 = Product(name="Mouse", price=29.99, quantity=10)
print(f"Product with defaults: {product2}")

print_output("Expected output", """
Valid product: name='Laptop' price=999.99 quantity=5 description='High-performance laptop' tags=['electronics', 'computer']
Product with defaults: name='Mouse' price=29.99 quantity=10 description=None tags=[]
""")

# ============================================================================
# STEP 4: Handle and Print Validation Errors
# ============================================================================

print_step(4, "Handle and Print Validation Errors")

def demonstrate_validation_errors():
    """Demonstrate various validation errors"""
    
    print("\n📝 Testing validation errors:")
    
    # Test cases with invalid data
    test_cases = [
        {
            "description": "Invalid User - missing required field",
            "model": User,
            "data": {"name": "Charlie", "age": 30}  # missing email
        },
        {
            "description": "Invalid User - wrong type",
            "model": User,
            "data": {"name": "David", "age": "thirty", "email": "david@example.com"}  # age as string
        },
        {
            "description": "Invalid Product - negative price",
            "model": Product,
            "data": {"name": "Book", "price": -10.50, "quantity": 5}
        },
        {
            "description": "Invalid Product - name too short",
            "model": Product,
            "data": {"name": "A", "price": 25.00, "quantity": 3}
        },
        {
            "description": "Invalid Product - negative quantity",
            "model": Product,
            "data": {"name": "Pen", "price": 5.00, "quantity": -1}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🚨 {test_case['description']}:")
        try:
            instance = test_case['model'](**test_case['data'])
            print(f"   Unexpected success: {instance}")
        except ValidationError as e:
            print(f"   ❌ Validation failed (as expected):")
            for error in e.errors():
                field = error['loc'][0] if error['loc'] else 'unknown'
                message = error['msg']
                value = error.get('input', 'N/A')
                print(f"      • Field '{field}': {message} (got: {value})")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")

demonstrate_validation_errors()

print_output("Expected output", """
Each test case will show validation errors with:
- Field name that failed validation
- Error message explaining what went wrong
- The invalid value that was provided
""")

# ============================================================================
# STEP 5: Nested Models for Parent/Child Relationships
# ============================================================================

print_step(5, "Nested Models for Parent/Child Relationships")

class Address(BaseModel):
    """Address model for nested usage"""
    street: str = Field(min_length=5)
    city: str = Field(min_length=2)
    postal_code: str = Field(pattern=r'^\d{5}(-\d{4})?$')  # US ZIP code format
    country: str = Field(default="USA")

class Person(BaseModel):
    """Person model with nested Address"""
    name: str = Field(min_length=2)
    age: int = Field(ge=0, le=150)
    address: Address
    phone: Optional[str] = None

class Company(BaseModel):
    """Company model demonstrating one-to-many relationships"""
    name: str = Field(min_length=2)
    founded_year: int = Field(ge=1800, le=2024)
    headquarters: Address
    employees: List[Person] = Field(default_factory=list)
    
    def add_employee(self, person: Person):
        """Add an employee to the company"""
        self.employees.append(person)
    
    def get_employee_count(self) -> int:
        """Get the number of employees"""
        return len(self.employees)

print("\n📝 Creating nested models:")

# Create addresses
address1 = Address(
    street="123 Main St",
    city="New York",
    postal_code="10001"
)

address2 = Address(
    street="456 Oak Ave",
    city="Los Angeles", 
    postal_code="90210"
)

print(f"Address 1: {address1}")
print(f"Address 2: {address2}")

# Create people with addresses
person1 = Person(
    name="John Doe",
    age=35,
    address=address1,
    phone="555-1234"
)

person2 = Person(
    name="Jane Smith", 
    age=28,
    address=address2
)

print(f"Person 1: {person1}")
print(f"Person 2: {person2}")

# Create company with headquarters and employees
company_address = Address(
    street="789 Business Blvd",
    city="San Francisco",
    postal_code="94105"
)

company = Company(
    name="Tech Innovations Inc",
    founded_year=2020,
    headquarters=company_address
)

# Add employees
company.add_employee(person1)
company.add_employee(person2)

print(f"\nCompany: {company.name}")
print(f"Founded: {company.founded_year}")
print(f"Headquarters: {company.headquarters.city}, {company.headquarters.country}")
print(f"Employee count: {company.get_employee_count()}")

# Access nested data
print(f"\nEmployee details:")
for i, employee in enumerate(company.employees, 1):
    print(f"  {i}. {employee.name} (age {employee.age})")
    print(f"     Lives in: {employee.address.city}")
    print(f"     Phone: {employee.phone or 'Not provided'}")

# Convert to dictionary (shows nested structure)
print(f"\nCompany as dictionary:")
company_dict = company.model_dump()
print(f"Keys: {list(company_dict.keys())}")
print(f"Headquarters keys: {list(company_dict['headquarters'].keys())}")
print(f"First employee keys: {list(company_dict['employees'][0].keys())}")

print_output("Expected output", """
Address 1: street='123 Main St' city='New York' postal_code='10001' country='USA'
Person 1: name='John Doe' age=35 address=Address(...) phone='555-1234'
Company: Tech Innovations Inc
Founded: 2020
Employee count: 2
Employee details show nested access to person and address data
Company dictionary shows full nested structure
""")

# ============================================================================
# STEP 6: Advanced Validation Error Handling for Nested Models
# ============================================================================

print_step(6, "Advanced Validation Error Handling for Nested Models")

def demonstrate_nested_validation_errors():
    """Demonstrate validation errors in nested models"""
    
    print("\n📝 Testing nested validation errors:")
    
    nested_test_cases = [
        {
            "description": "Invalid nested address",
            "data": {
                "name": "Test Person",
                "age": 30,
                "address": {
                    "street": "123",  # too short
                    "city": "NY",
                    "postal_code": "invalid"  # wrong format
                }
            }
        },
        {
            "description": "Missing required nested field",
            "data": {
                "name": "Test Person",
                "age": 25,
                "address": {
                    "street": "123 Valid Street",
                    "city": "Valid City"
                    # missing postal_code
                }
            }
        },
        {
            "description": "Invalid company with bad employee data",
            "data": {
                "name": "Test Company",
                "founded_year": 2020,
                "headquarters": {
                    "street": "123 Business St",
                    "city": "Business City",
                    "postal_code": "12345"
                },
                "employees": [
                    {
                        "name": "A",  # too short
                        "age": 200,   # too old
                        "address": {
                            "street": "123 Employee St",
                            "city": "Employee City",
                            "postal_code": "54321"
                        }
                    }
                ]
            }
        }
    ]
    
    for test_case in nested_test_cases:
        print(f"\n🚨 {test_case['description']}:")
        try:
            if 'employees' in test_case['data']:
                instance = Company(**test_case['data'])
            else:
                instance = Person(**test_case['data'])
            print(f"   Unexpected success: {instance}")
        except ValidationError as e:
            print(f"   ❌ Validation failed (as expected):")
            for error in e.errors():
                # Show the full path to the error (including nested fields)
                field_path = " -> ".join(str(loc) for loc in error['loc'])
                message = error['msg']
                value = error.get('input', 'N/A')
                print(f"      • Path '{field_path}': {message} (got: {value})")

demonstrate_nested_validation_errors()

print_output("Expected output", """
Nested validation errors will show:
- Full path to the failing field (e.g., 'address -> postal_code')
- Clear error messages for each validation failure
- The invalid values that caused the errors
""")

# ============================================================================
# Summary
# ============================================================================

print_step(7, "Summary")

print("""
🎉 Congratulations! You've learned:

1. ✅ How to install and verify Pydantic
2. ✅ Creating BaseModel classes with typed fields
3. ✅ Adding field constraints (min/max length, positive numbers, etc.)
4. ✅ Handling and interpreting validation errors
5. ✅ Creating nested models for complex relationships
6. ✅ Working with one-to-many relationships (Company -> Employees)

Key Pydantic Features Demonstrated:
- Type validation and conversion
- Field constraints with Field()
- Custom validation messages
- Nested model validation
- Dictionary conversion with model_dump()
- Optional fields with defaults
- List fields with constraints

Next Steps:
- Explore custom validators with @field_validator
- Learn about model configuration options
- Try serialization to JSON with model_dump_json()
- Experiment with advanced field types (dates, URLs, etc.)
""")