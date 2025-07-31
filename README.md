# Pydantic 2 Tutorial - Step by Step Guide

This comprehensive tutorial demonstrates how to use Pydantic 2 for data validation and serialization in Python.

## Installation

1. **Install Pydantic 2:**
   ```bash
   pip install pydantic>=2.0.0
   ```

   Or install from requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python -c "import pydantic; print(f'Pydantic version: {pydantic.__version__}')"
   ```

## Running the Tutorial

Execute the tutorial script:
```bash
python pydantic_tutorial.py
```

## What You'll Learn

### Step 1: Installation and Verification
- Check if Pydantic 2 is installed
- Verify the version
- Handle import errors gracefully

### Step 2: Simple BaseModel and Input Data
- Create basic Pydantic models
- Input data from dictionaries and keyword arguments
- Access model attributes
- Convert models back to dictionaries

### Step 3: Field Constraints
- Add validation constraints (min_length, max_length, gt, ge, etc.)
- Use regex patterns for string validation
- Create custom field validators
- Handle optional fields with defaults

### Step 4: Validation Errors
- Trigger validation errors with invalid data
- Parse and display error information
- Handle multiple validation errors
- Understand error structure and location

### Step 5: Nested Models
- Create parent/child relationships
- Validate nested data structures
- Access nested model attributes
- Handle complex data hierarchies

### Step 6: Complex Validation
- Cross-field validation
- Business logic validation
- Complex nested validation scenarios
- Advanced error handling

## Expected Output

The tutorial will show you:

1. **Installation verification** - Confirms Pydantic 2 is working
2. **Simple model creation** - Shows how to create and use basic models
3. **Field constraints** - Demonstrates validation rules and custom validators
4. **Error handling** - Shows detailed validation error messages
5. **Nested models** - Illustrates complex data structures
6. **Complex validation** - Advanced validation scenarios with multiple errors

## Key Pydantic 3 Features Covered

- **BaseModel** - Core model class
- **Field** - Field configuration and constraints
- **ValidationError** - Error handling
- **field_validator** - Custom validation functions
- **Type hints** - Type annotations for validation
- **Nested models** - Complex data structures
- **Model serialization** - Converting to/from dictionaries

## Common Use Cases

- API request/response validation
- Configuration file validation
- Database model validation
- Data transformation and serialization
- Schema documentation generation

## Next Steps

After completing this tutorial, explore:
- Pydantic settings management
- Model configuration options
- Advanced validators and serializers
- Integration with FastAPI
- Custom field types and validators
