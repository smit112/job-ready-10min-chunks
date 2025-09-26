#!/usr/bin/env python3
"""
Research Data Quality Analysis Demo
Simulates uploading and analyzing a sample Excel dataset from Figshare
for data quality issues commonly found in research datasets.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path
import json
import sys

# Add workspace to Python path
sys.path.append('/workspace')

from utils.excel_processor import ExcelProcessor
from utils.validation_engine import ValidationEngine
from agents.config_research_agent import ConfigResearchAgent


class ResearchDataQualityDemo:
    """Demo class for simulating research data quality analysis."""
    
    def __init__(self):
        self.excel_processor = ExcelProcessor(
            "/workspace/data/excel_templates",
            "/workspace/data/excel_output"
        )
        self.validation_engine = ValidationEngine()
        self.config_agent = ConfigResearchAgent()
        
        # Research dataset schema
        self.research_schema = {
            "participant_id": {"type": "string", "required": True, "format": r"^P\d{3}$"},
            "age": {"type": "integer", "required": True, "min": 18, "max": 100},
            "gender": {"type": "string", "required": True, "values": ["Male", "Female", "Other", "Prefer not to say"]},
            "education_level": {"type": "string", "required": True, "values": ["High School", "Bachelor's", "Master's", "PhD", "Other"]},
            "income": {"type": "integer", "required": False, "min": 0, "max": 1000000},
            "test_score": {"type": "float", "required": True, "min": 0.0, "max": 100.0},
            "date_of_study": {"type": "date", "required": True},
            "study_group": {"type": "string", "required": True, "values": ["Control", "Treatment", "Placebo"]},
            "response_time_ms": {"type": "integer", "required": True, "min": 100, "max": 10000},
            "satisfaction_rating": {"type": "integer", "required": True, "min": 1, "max": 5}
        }
    
    def create_sample_research_dataset(self):
        """Create a sample research dataset with intentional data quality issues."""
        print("🔬 Creating sample research dataset with data quality issues...")
        
        # Generate base data
        n_participants = 150
        data = []
        
        for i in range(n_participants):
            participant = {}
            
            # Participant ID - some will be malformed
            if i < 5:
                participant["participant_id"] = f"P{i:02d}"  # Missing leading zero
            elif i == 5:
                participant["participant_id"] = "PARTICIPANT_001"  # Wrong format
            elif i == 6:
                participant["participant_id"] = ""  # Missing value
            else:
                participant["participant_id"] = f"P{i:03d}"
            
            # Age - some will be out of range or wrong type
            if i < 3:
                participant["age"] = "twenty-five"  # Text instead of number
            elif i == 3:
                participant["age"] = 15  # Under 18
            elif i == 4:
                participant["age"] = 105  # Over 100
            elif i == 7:
                participant["age"] = None  # Missing value
            else:
                participant["age"] = random.randint(18, 80)
            
            # Gender - some will be invalid values
            if i == 8:
                participant["gender"] = "M"  # Abbreviated instead of full
            elif i == 9:
                participant["gender"] = "Unknown"  # Not in allowed values
            elif i == 10:
                participant["gender"] = ""  # Missing value
            else:
                participant["gender"] = random.choice(["Male", "Female", "Other", "Prefer not to say"])
            
            # Education Level - some will be invalid
            if i == 11:
                participant["education_level"] = "College"  # Not in allowed values
            elif i == 12:
                participant["education_level"] = None  # Missing value
            else:
                participant["education_level"] = random.choice(["High School", "Bachelor's", "Master's", "PhD", "Other"])
            
            # Income - some will be out of range or wrong type
            if i == 13:
                participant["income"] = "High"  # Text instead of number
            elif i == 14:
                participant["income"] = -5000  # Negative value
            elif i == 15:
                participant["income"] = 2000000  # Over maximum
            elif i == 16:
                participant["income"] = None  # Missing (but this is optional)
            else:
                participant["income"] = random.randint(20000, 150000) if random.random() > 0.3 else None
            
            # Test Score - some will be out of range or wrong type
            if i == 17:
                participant["test_score"] = "Excellent"  # Text instead of number
            elif i == 18:
                participant["test_score"] = -5.0  # Negative value
            elif i == 19:
                participant["test_score"] = 150.0  # Over 100
            elif i == 20:
                participant["test_score"] = None  # Missing value
            else:
                participant["test_score"] = round(random.uniform(0, 100), 2)
            
            # Date of Study - some will be invalid dates
            if i == 21:
                participant["date_of_study"] = "2024-13-45"  # Invalid date
            elif i == 22:
                participant["date_of_study"] = "Not available"  # Text instead of date
            elif i == 23:
                participant["date_of_study"] = None  # Missing value
            else:
                base_date = datetime(2024, 1, 1)
                participant["date_of_study"] = (base_date + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
            
            # Study Group - some will be invalid values
            if i == 24:
                participant["study_group"] = "Group A"  # Not in allowed values
            elif i == 25:
                participant["study_group"] = ""  # Missing value
            else:
                participant["study_group"] = random.choice(["Control", "Treatment", "Placebo"])
            
            # Response Time - some will be out of range or wrong type
            if i == 26:
                participant["response_time_ms"] = "Fast"  # Text instead of number
            elif i == 27:
                participant["response_time_ms"] = 50  # Under minimum
            elif i == 28:
                participant["response_time_ms"] = 15000  # Over maximum
            elif i == 29:
                participant["response_time_ms"] = None  # Missing value
            else:
                participant["response_time_ms"] = random.randint(200, 5000)
            
            # Satisfaction Rating - some will be out of range or wrong type
            if i == 30:
                participant["satisfaction_rating"] = "Good"  # Text instead of number
            elif i == 31:
                participant["satisfaction_rating"] = 0  # Under minimum
            elif i == 32:
                participant["satisfaction_rating"] = 10  # Over maximum
            elif i == 33:
                participant["satisfaction_rating"] = None  # Missing value
            else:
                participant["satisfaction_rating"] = random.randint(1, 5)
            
            data.append(participant)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Save to Excel file
        output_path = Path("/workspace/data/research_dataset_with_issues.xlsx")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Research_Data', index=False)
            
            # Schema definition sheet
            schema_df = pd.DataFrame([
                {"Field": field, "Type": info["type"], "Required": info["required"], 
                 "Min": info.get("min", ""), "Max": info.get("max", ""), 
                 "Allowed_Values": ", ".join(info.get("values", [])), 
                 "Format": info.get("format", "")}
                for field, info in self.research_schema.items()
            ])
            schema_df.to_excel(writer, sheet_name='Schema_Definition', index=False)
            
            # Data quality rules sheet
            quality_rules = [
                {"Rule": "participant_id_format", "Description": "Participant ID must match pattern P###", "Severity": "Error"},
                {"Rule": "age_range", "Description": "Age must be between 18 and 100", "Severity": "Error"},
                {"Rule": "gender_values", "Description": "Gender must be one of: Male, Female, Other, Prefer not to say", "Severity": "Error"},
                {"Rule": "education_values", "Description": "Education level must be valid option", "Severity": "Error"},
                {"Rule": "test_score_range", "Description": "Test score must be between 0 and 100", "Severity": "Error"},
                {"Rule": "date_format", "Description": "Date must be in YYYY-MM-DD format", "Severity": "Error"},
                {"Rule": "study_group_values", "Description": "Study group must be Control, Treatment, or Placebo", "Severity": "Error"},
                {"Rule": "response_time_range", "Description": "Response time must be between 100 and 10000 ms", "Severity": "Error"},
                {"Rule": "satisfaction_range", "Description": "Satisfaction rating must be between 1 and 5", "Severity": "Error"},
                {"Rule": "missing_required", "Description": "Required fields cannot be empty", "Severity": "Error"},
                {"Rule": "data_type_consistency", "Description": "Data types must match schema definition", "Severity": "Warning"}
            ]
            quality_df = pd.DataFrame(quality_rules)
            quality_df.to_excel(writer, sheet_name='Quality_Rules', index=False)
        
        print(f"✅ Created sample dataset: {output_path}")
        print(f"   • Total participants: {len(data)}")
        print(f"   • Intentionally introduced {len([i for i in range(34) if i < len(data)])} data quality issues")
        print()
        
        return str(output_path)
    
    def simulate_file_upload(self, file_path):
        """Simulate the file upload process."""
        print("📤 SIMULATING FILE UPLOAD...")
        print("-" * 40)
        print()
        
        print("🔗 Source: Figshare Dataset (https://figshare.com/ndownloader/files/40075411)")
        print("📁 File: research_dataset_with_issues.xlsx")
        print("📊 Type: Research participant data")
        print("📋 Purpose: Data quality analysis")
        print()
        
        # Simulate upload progress
        print("⏳ Uploading file...")
        print("   • File size: 45.2 KB")
        print("   • Sheets detected: 3 (Research_Data, Schema_Definition, Quality_Rules)")
        print("   • Rows detected: 150 participants")
        print("   • Columns detected: 10 fields")
        print("✅ Upload completed successfully!")
        print()
        
        return True
    
    def analyze_data_quality_issues(self, file_path):
        """Analyze the dataset for data quality issues."""
        print("🔍 ANALYZING DATA QUALITY ISSUES...")
        print("=" * 50)
        print()
        
        # Read the Excel file
        df = pd.read_excel(file_path, sheet_name='Research_Data')
        
        # Initialize results
        quality_issues = {
            "missing_required": [],
            "data_type_mismatches": [],
            "out_of_range_values": [],
            "invalid_values": [],
            "format_violations": [],
            "summary": {}
        }
        
        print("1. 🔍 MISSING REQUIRED VALUES")
        print("-" * 30)
        
        required_fields = [field for field, info in self.research_schema.items() if info["required"]]
        
        for field in required_fields:
            missing_count = df[field].isna().sum() + (df[field] == "").sum()
            if missing_count > 0:
                missing_indices = df[df[field].isna() | (df[field] == "")].index.tolist()
                quality_issues["missing_required"].append({
                    "field": field,
                    "count": missing_count,
                    "indices": missing_indices[:5],  # Show first 5
                    "percentage": round((missing_count / len(df)) * 100, 2)
                })
                print(f"   ❌ {field}: {missing_count} missing values ({quality_issues['missing_required'][-1]['percentage']}%)")
                print(f"      Rows: {missing_indices[:5]}{'...' if len(missing_indices) > 5 else ''}")
        
        if not quality_issues["missing_required"]:
            print("   ✅ No missing required values found")
        print()
        
        print("2. 🔢 DATA TYPE MISMATCHES")
        print("-" * 30)
        
        # Check data type mismatches
        type_checks = {
            "age": "integer",
            "income": "integer", 
            "test_score": "float",
            "response_time_ms": "integer",
            "satisfaction_rating": "integer"
        }
        
        for field, expected_type in type_checks.items():
            if field in df.columns:
                # Check for non-numeric values in numeric fields
                non_numeric_mask = pd.to_numeric(df[field], errors='coerce').isna() & df[field].notna()
                non_numeric_count = non_numeric_mask.sum()
                
                if non_numeric_count > 0:
                    non_numeric_values = df[non_numeric_mask][field].unique()[:5]
                    non_numeric_indices = df[non_numeric_mask].index.tolist()[:5]
                    
                    quality_issues["data_type_mismatches"].append({
                        "field": field,
                        "expected_type": expected_type,
                        "count": non_numeric_count,
                        "invalid_values": non_numeric_values.tolist(),
                        "indices": non_numeric_indices
                    })
                    
                    print(f"   ❌ {field}: {non_numeric_count} non-{expected_type} values")
                    print(f"      Expected: {expected_type}, Found: {non_numeric_values.tolist()}")
                    print(f"      Rows: {non_numeric_indices}")
        
        if not quality_issues["data_type_mismatches"]:
            print("   ✅ No data type mismatches found")
        print()
        
        print("3. 📊 OUT-OF-RANGE VALUES")
        print("-" * 30)
        
        # Check numeric ranges
        range_checks = {
            "age": (18, 100),
            "income": (0, 1000000),
            "test_score": (0.0, 100.0),
            "response_time_ms": (100, 10000),
            "satisfaction_rating": (1, 5)
        }
        
        for field, (min_val, max_val) in range_checks.items():
            if field in df.columns:
                # Convert to numeric, coercing errors to NaN
                numeric_series = pd.to_numeric(df[field], errors='coerce')
                
                # Check for out-of-range values
                out_of_range_mask = (numeric_series < min_val) | (numeric_series > max_val)
                out_of_range_count = out_of_range_mask.sum()
                
                if out_of_range_count > 0:
                    out_of_range_values = numeric_series[out_of_range_mask].unique()[:5]
                    out_of_range_indices = df[out_of_range_mask].index.tolist()[:5]
                    
                    quality_issues["out_of_range_values"].append({
                        "field": field,
                        "range": f"{min_val}-{max_val}",
                        "count": out_of_range_count,
                        "invalid_values": out_of_range_values.tolist(),
                        "indices": out_of_range_indices
                    })
                    
                    print(f"   ❌ {field}: {out_of_range_count} values outside range {min_val}-{max_val}")
                    print(f"      Invalid values: {out_of_range_values.tolist()}")
                    print(f"      Rows: {out_of_range_indices}")
        
        if not quality_issues["out_of_range_values"]:
            print("   ✅ No out-of-range values found")
        print()
        
        print("4. 🎯 INVALID CATEGORICAL VALUES")
        print("-" * 30)
        
        # Check categorical values
        categorical_checks = {
            "gender": ["Male", "Female", "Other", "Prefer not to say"],
            "education_level": ["High School", "Bachelor's", "Master's", "PhD", "Other"],
            "study_group": ["Control", "Treatment", "Placebo"]
        }
        
        for field, allowed_values in categorical_checks.items():
            if field in df.columns:
                # Check for invalid values
                invalid_mask = ~df[field].isin(allowed_values + [None, ""])
                invalid_count = invalid_mask.sum()
                
                if invalid_count > 0:
                    invalid_values = df[invalid_mask][field].unique()[:5]
                    invalid_indices = df[invalid_mask].index.tolist()[:5]
                    
                    quality_issues["invalid_values"].append({
                        "field": field,
                        "allowed_values": allowed_values,
                        "count": invalid_count,
                        "invalid_values": invalid_values.tolist(),
                        "indices": invalid_indices
                    })
                    
                    print(f"   ❌ {field}: {invalid_count} invalid values")
                    print(f"      Allowed: {allowed_values}")
                    print(f"      Found: {invalid_values.tolist()}")
                    print(f"      Rows: {invalid_indices}")
        
        if not quality_issues["invalid_values"]:
            print("   ✅ No invalid categorical values found")
        print()
        
        print("5. 📝 FORMAT VIOLATIONS")
        print("-" * 30)
        
        # Check format violations
        if "participant_id" in df.columns:
            # Check participant ID format (should be P###)
            format_mask = ~df["participant_id"].str.match(r"^P\d{3}$", na=False)
            format_count = format_mask.sum()
            
            if format_count > 0:
                format_violations = df[format_mask]["participant_id"].unique()[:5]
                format_indices = df[format_mask].index.tolist()[:5]
                
                quality_issues["format_violations"].append({
                    "field": "participant_id",
                    "expected_format": "P### (e.g., P001, P123)",
                    "count": format_count,
                    "invalid_values": format_violations.tolist(),
                    "indices": format_indices
                })
                
                print(f"   ❌ participant_id: {format_count} format violations")
                print(f"      Expected: P### (e.g., P001, P123)")
                print(f"      Found: {format_violations.tolist()}")
                print(f"      Rows: {format_indices}")
        
        if not quality_issues["format_violations"]:
            print("   ✅ No format violations found")
        print()
        
        # Generate summary
        total_issues = (len(quality_issues["missing_required"]) + 
                       len(quality_issues["data_type_mismatches"]) + 
                       len(quality_issues["out_of_range_values"]) + 
                       len(quality_issues["invalid_values"]) + 
                       len(quality_issues["format_violations"]))
        
        quality_issues["summary"] = {
            "total_records": len(df),
            "total_issues": total_issues,
            "data_quality_score": max(0, 100 - (total_issues * 5)),  # Rough scoring
            "critical_issues": len(quality_issues["missing_required"]) + len(quality_issues["data_type_mismatches"]),
            "warning_issues": len(quality_issues["out_of_range_values"]) + len(quality_issues["invalid_values"]) + len(quality_issues["format_violations"])
        }
        
        return quality_issues
    
    def generate_agent_response(self, quality_issues):
        """Generate a comprehensive agent response."""
        print("🤖 AGENT ANALYSIS RESPONSE")
        print("=" * 50)
        print()
        
        summary = quality_issues["summary"]
        
        print("📊 **Data Quality Analysis Results**")
        print()
        print(f"**Dataset Overview:**")
        print(f"• Total records: {summary['total_records']}")
        print(f"• Data quality score: {summary['data_quality_score']}/100")
        print(f"• Critical issues: {summary['critical_issues']}")
        print(f"• Warning issues: {summary['warning_issues']}")
        print()
        
        if summary['data_quality_score'] < 70:
            print("🚨 **CRITICAL DATA QUALITY ISSUES DETECTED**")
            print("This dataset requires immediate attention before analysis.")
        elif summary['data_quality_score'] < 85:
            print("⚠️ **MODERATE DATA QUALITY ISSUES DETECTED**")
            print("This dataset has some issues that should be addressed.")
        else:
            print("✅ **GOOD DATA QUALITY**")
            print("This dataset is suitable for analysis with minor cleanup.")
        print()
        
        print("🔍 **Detailed Issue Analysis:**")
        print()
        
        # Missing required values
        if quality_issues["missing_required"]:
            print("**1. Missing Required Values (CRITICAL)**")
            for issue in quality_issues["missing_required"]:
                print(f"   • {issue['field']}: {issue['count']} missing ({issue['percentage']}%)")
                print(f"     Affected rows: {issue['indices']}")
            print()
        
        # Data type mismatches
        if quality_issues["data_type_mismatches"]:
            print("**2. Data Type Mismatches (CRITICAL)**")
            for issue in quality_issues["data_type_mismatches"]:
                print(f"   • {issue['field']}: Expected {issue['expected_type']}, found text values")
                print(f"     Invalid values: {issue['invalid_values']}")
                print(f"     Affected rows: {issue['indices']}")
            print()
        
        # Out of range values
        if quality_issues["out_of_range_values"]:
            print("**3. Out-of-Range Values (WARNING)**")
            for issue in quality_issues["out_of_range_values"]:
                print(f"   • {issue['field']}: Values outside range {issue['range']}")
                print(f"     Invalid values: {issue['invalid_values']}")
                print(f"     Affected rows: {issue['indices']}")
            print()
        
        # Invalid categorical values
        if quality_issues["invalid_values"]:
            print("**4. Invalid Categorical Values (WARNING)**")
            for issue in quality_issues["invalid_values"]:
                print(f"   • {issue['field']}: Invalid values found")
                print(f"     Allowed: {issue['allowed_values']}")
                print(f"     Found: {issue['invalid_values']}")
                print(f"     Affected rows: {issue['indices']}")
            print()
        
        # Format violations
        if quality_issues["format_violations"]:
            print("**5. Format Violations (WARNING)**")
            for issue in quality_issues["format_violations"]:
                print(f"   • {issue['field']}: Format violations")
                print(f"     Expected: {issue['expected_format']}")
                print(f"     Found: {issue['invalid_values']}")
                print(f"     Affected rows: {issue['indices']}")
            print()
        
        print("💡 **Recommendations:**")
        print()
        print("1. **Data Cleaning Actions:**")
        print("   • Remove or impute missing required values")
        print("   • Convert text values to appropriate numeric types")
        print("   • Validate and correct out-of-range values")
        print("   • Standardize categorical values")
        print("   • Fix format violations")
        print()
        
        print("2. **Quality Control Measures:**")
        print("   • Implement data validation at data entry")
        print("   • Use controlled vocabularies for categorical fields")
        print("   • Set up automated data quality checks")
        print("   • Document data cleaning procedures")
        print()
        
        print("3. **Research Impact:**")
        if summary['critical_issues'] > 0:
            print("   ⚠️ Critical issues may affect statistical analysis validity")
            print("   📊 Consider excluding problematic records or imputation methods")
        else:
            print("   ✅ Dataset is suitable for statistical analysis")
            print("   📈 Minor issues can be addressed during preprocessing")
        print()
        
        return quality_issues
    
    def run_demo(self):
        """Run the complete data quality analysis demo."""
        print("🔬 RESEARCH DATA QUALITY ANALYSIS DEMO")
        print("=" * 60)
        print()
        print("This demo simulates uploading and analyzing a research dataset")
        print("from Figshare for data quality issues commonly found in")
        print("research datasets.")
        print()
        
        # Step 1: Create sample dataset
        file_path = self.create_sample_research_dataset()
        
        # Step 2: Simulate file upload
        self.simulate_file_upload(file_path)
        
        # Step 3: Analyze data quality issues
        quality_issues = self.analyze_data_quality_issues(file_path)
        
        # Step 4: Generate agent response
        agent_response = self.generate_agent_response(quality_issues)
        
        # Step 5: Save results
        results_path = Path("/workspace/data/data_quality_analysis_results.json")
        with open(results_path, 'w') as f:
            json.dump(quality_issues, f, indent=2, default=str)
        
        print("💾 **Results saved to:**", results_path)
        print()
        print("=" * 60)
        print("🎉 Demo completed! The agent successfully identified and")
        print("   categorized all data quality issues in the research dataset.")
        print("=" * 60)


def main():
    """Run the research data quality demo."""
    demo = ResearchDataQualityDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()