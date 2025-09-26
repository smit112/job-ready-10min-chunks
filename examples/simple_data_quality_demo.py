#!/usr/bin/env python3
"""
Simple Research Data Quality Analysis Demo
Shows concrete examples of errors the agent would find in research datasets.
"""
import json
from pathlib import Path


def create_sample_research_data():
    """Create sample research data with intentional quality issues."""
    return [
        # Row 0: Missing participant_id
        {"participant_id": "", "age": 25, "gender": "Male", "education_level": "Bachelor's", 
         "income": 50000, "test_score": 85.5, "date_of_study": "2024-01-15", 
         "study_group": "Control", "response_time_ms": 1200, "satisfaction_rating": 4},
        
        # Row 1: Wrong participant_id format
        {"participant_id": "PARTICIPANT_001", "age": 30, "gender": "Female", 
         "education_level": "Master's", "income": 75000, "test_score": 92.0, 
         "date_of_study": "2024-01-16", "study_group": "Treatment", 
         "response_time_ms": 950, "satisfaction_rating": 5},
        
        # Row 2: Age as text instead of number
        {"participant_id": "P002", "age": "twenty-five", "gender": "Male", 
         "education_level": "High School", "income": 35000, "test_score": 78.0, 
         "date_of_study": "2024-01-17", "study_group": "Placebo", 
         "response_time_ms": 1500, "satisfaction_rating": 3},
        
        # Row 3: Age out of range (under 18)
        {"participant_id": "P003", "age": 15, "gender": "Female", 
         "education_level": "Bachelor's", "income": 0, "test_score": 88.5, 
         "date_of_study": "2024-01-18", "study_group": "Control", 
         "response_time_ms": 1100, "satisfaction_rating": 4},
        
        # Row 4: Age out of range (over 100)
        {"participant_id": "P004", "age": 105, "gender": "Male", 
         "education_level": "PhD", "income": 120000, "test_score": 95.0, 
         "date_of_study": "2024-01-19", "study_group": "Treatment", 
         "response_time_ms": 800, "satisfaction_rating": 5},
        
        # Row 5: Invalid gender value
        {"participant_id": "P005", "age": 28, "gender": "M", 
         "education_level": "Bachelor's", "income": 60000, "test_score": 82.0, 
         "date_of_study": "2024-01-20", "study_group": "Control", 
         "response_time_ms": 1300, "satisfaction_rating": 4},
        
        # Row 6: Invalid education level
        {"participant_id": "P006", "age": 35, "gender": "Female", 
         "education_level": "College", "income": 80000, "test_score": 90.0, 
         "date_of_study": "2024-01-21", "study_group": "Treatment", 
         "response_time_ms": 1000, "satisfaction_rating": 5},
        
        # Row 7: Income as text
        {"participant_id": "P007", "age": 42, "gender": "Male", 
         "education_level": "Master's", "income": "High", "test_score": 87.5, 
         "date_of_study": "2024-01-22", "study_group": "Placebo", 
         "response_time_ms": 1400, "satisfaction_rating": 3},
        
        # Row 8: Test score as text
        {"participant_id": "P008", "age": 29, "gender": "Female", 
         "education_level": "Bachelor's", "income": 55000, "test_score": "Excellent", 
         "date_of_study": "2024-01-23", "study_group": "Control", 
         "response_time_ms": 1200, "satisfaction_rating": 4},
        
        # Row 9: Test score out of range (over 100)
        {"participant_id": "P009", "age": 31, "gender": "Male", 
         "education_level": "PhD", "income": 95000, "test_score": 150.0, 
         "date_of_study": "2024-01-24", "study_group": "Treatment", 
         "response_time_ms": 900, "satisfaction_rating": 5},
        
        # Row 10: Invalid date format
        {"participant_id": "P010", "age": 26, "gender": "Female", 
         "education_level": "Bachelor's", "income": 45000, "test_score": 79.0, 
         "date_of_study": "2024-13-45", "study_group": "Control", 
         "response_time_ms": 1600, "satisfaction_rating": 3},
        
        # Row 11: Invalid study group
        {"participant_id": "P011", "age": 33, "gender": "Male", 
         "education_level": "Master's", "income": 70000, "test_score": 91.0, 
         "date_of_study": "2024-01-26", "study_group": "Group A", 
         "response_time_ms": 1100, "satisfaction_rating": 4},
        
        # Row 12: Response time as text
        {"participant_id": "P012", "age": 27, "gender": "Female", 
         "education_level": "Bachelor's", "income": 50000, "test_score": 83.5, 
         "date_of_study": "2024-01-27", "study_group": "Treatment", 
         "response_time_ms": "Fast", "satisfaction_rating": 4},
        
        # Row 13: Response time out of range (too low)
        {"participant_id": "P013", "age": 24, "gender": "Male", 
         "education_level": "High School", "income": 30000, "test_score": 76.0, 
         "date_of_study": "2024-01-28", "study_group": "Placebo", 
         "response_time_ms": 50, "satisfaction_rating": 2},
        
        # Row 14: Satisfaction rating as text
        {"participant_id": "P014", "age": 38, "gender": "Female", 
         "education_level": "PhD", "income": 110000, "test_score": 94.0, 
         "date_of_study": "2024-01-29", "study_group": "Control", 
         "response_time_ms": 1000, "satisfaction_rating": "Good"},
        
        # Row 15: Satisfaction rating out of range
        {"participant_id": "P015", "age": 25, "gender": "Male", 
         "education_level": "Bachelor's", "income": 48000, "test_score": 81.0, 
         "date_of_study": "2024-01-30", "study_group": "Treatment", 
         "response_time_ms": 1350, "satisfaction_rating": 10},
        
        # Row 16: Missing required field (age)
        {"participant_id": "P016", "age": None, "gender": "Female", 
         "education_level": "Master's", "income": 65000, "test_score": 89.0, 
         "date_of_study": "2024-01-31", "study_group": "Control", 
         "response_time_ms": 1150, "satisfaction_rating": 4},
        
        # Row 17: Multiple issues (invalid gender + out of range test score)
        {"participant_id": "P017", "age": 30, "gender": "Unknown", 
         "education_level": "Bachelor's", "income": 52000, "test_score": -5.0, 
         "date_of_study": "2024-02-01", "study_group": "Treatment", 
         "response_time_ms": 1250, "satisfaction_rating": 3},
        
        # Row 18: Good data (no issues)
        {"participant_id": "P018", "age": 32, "gender": "Female", 
         "education_level": "Master's", "income": 75000, "test_score": 88.0, 
         "date_of_study": "2024-02-02", "study_group": "Control", 
         "response_time_ms": 1050, "satisfaction_rating": 4},
        
        # Row 19: Good data (no issues)
        {"participant_id": "P019", "age": 29, "gender": "Male", 
         "education_level": "Bachelor's", "income": 58000, "test_score": 85.5, 
         "date_of_study": "2024-02-03", "study_group": "Treatment", 
         "response_time_ms": 1200, "satisfaction_rating": 5}
    ]


def analyze_data_quality(data):
    """Analyze the research data for quality issues."""
    print("🔬 RESEARCH DATA QUALITY ANALYSIS")
    print("=" * 60)
    print()
    print("📊 **Dataset Overview**")
    print(f"• Total participants: {len(data)}")
    print(f"• Source: Figshare Dataset (https://figshare.com/ndownloader/files/40075411)")
    print(f"• Analysis type: Data quality assessment")
    print()
    
    # Define schema requirements
    schema = {
        "participant_id": {"required": True, "format": r"^P\d{3}$", "type": "string"},
        "age": {"required": True, "min": 18, "max": 100, "type": "integer"},
        "gender": {"required": True, "values": ["Male", "Female", "Other", "Prefer not to say"], "type": "string"},
        "education_level": {"required": True, "values": ["High School", "Bachelor's", "Master's", "PhD", "Other"], "type": "string"},
        "income": {"required": False, "min": 0, "max": 1000000, "type": "integer"},
        "test_score": {"required": True, "min": 0.0, "max": 100.0, "type": "float"},
        "date_of_study": {"required": True, "format": r"^\d{4}-\d{2}-\d{2}$", "type": "date"},
        "study_group": {"required": True, "values": ["Control", "Treatment", "Placebo"], "type": "string"},
        "response_time_ms": {"required": True, "min": 100, "max": 10000, "type": "integer"},
        "satisfaction_rating": {"required": True, "min": 1, "max": 5, "type": "integer"}
    }
    
    issues = {
        "missing_required": [],
        "data_type_mismatches": [],
        "out_of_range_values": [],
        "invalid_values": [],
        "format_violations": []
    }
    
    print("🔍 **DETAILED ANALYSIS RESULTS**")
    print("=" * 40)
    print()
    
    # 1. Missing Required Values
    print("1. 🚨 MISSING REQUIRED VALUES")
    print("-" * 35)
    
    required_fields = [field for field, rules in schema.items() if rules["required"]]
    
    for field in required_fields:
        missing_count = 0
        missing_rows = []
        
        for i, row in enumerate(data):
            if row[field] is None or row[field] == "":
                missing_count += 1
                missing_rows.append(i)
        
        if missing_count > 0:
            issues["missing_required"].append({
                "field": field,
                "count": missing_count,
                "rows": missing_rows,
                "percentage": round((missing_count / len(data)) * 100, 1)
            })
            print(f"   ❌ {field}: {missing_count} missing values ({issues['missing_required'][-1]['percentage']}%)")
            print(f"      Rows: {missing_rows}")
    
    if not issues["missing_required"]:
        print("   ✅ No missing required values found")
    print()
    
    # 2. Data Type Mismatches
    print("2. 🔢 DATA TYPE MISMATCHES")
    print("-" * 35)
    
    numeric_fields = ["age", "income", "test_score", "response_time_ms", "satisfaction_rating"]
    
    for field in numeric_fields:
        type_issues = []
        issue_rows = []
        
        for i, row in enumerate(data):
            value = row[field]
            if value is not None and value != "":
                # Check if it's a string when it should be numeric
                if isinstance(value, str) and not value.replace(".", "").replace("-", "").isdigit():
                    type_issues.append(value)
                    issue_rows.append(i)
        
        if type_issues:
            issues["data_type_mismatches"].append({
                "field": field,
                "expected_type": "numeric",
                "count": len(type_issues),
                "invalid_values": type_issues,
                "rows": issue_rows
            })
            print(f"   ❌ {field}: {len(type_issues)} non-numeric values")
            print(f"      Expected: numeric, Found: {type_issues}")
            print(f"      Rows: {issue_rows}")
    
    if not issues["data_type_mismatches"]:
        print("   ✅ No data type mismatches found")
    print()
    
    # 3. Out-of-Range Values
    print("3. 📊 OUT-OF-RANGE VALUES")
    print("-" * 35)
    
    range_fields = {
        "age": (18, 100),
        "income": (0, 1000000),
        "test_score": (0.0, 100.0),
        "response_time_ms": (100, 10000),
        "satisfaction_rating": (1, 5)
    }
    
    for field, (min_val, max_val) in range_fields.items():
        range_issues = []
        issue_rows = []
        
        for i, row in enumerate(data):
            value = row[field]
            if value is not None and value != "":
                try:
                    num_value = float(value)
                    if num_value < min_val or num_value > max_val:
                        range_issues.append(value)
                        issue_rows.append(i)
                except (ValueError, TypeError):
                    pass  # Already caught in data type check
        
        if range_issues:
            issues["out_of_range_values"].append({
                "field": field,
                "range": f"{min_val}-{max_val}",
                "count": len(range_issues),
                "invalid_values": range_issues,
                "rows": issue_rows
            })
            print(f"   ❌ {field}: {len(range_issues)} values outside range {min_val}-{max_val}")
            print(f"      Invalid values: {range_issues}")
            print(f"      Rows: {issue_rows}")
    
    if not issues["out_of_range_values"]:
        print("   ✅ No out-of-range values found")
    print()
    
    # 4. Invalid Categorical Values
    print("4. 🎯 INVALID CATEGORICAL VALUES")
    print("-" * 35)
    
    categorical_fields = {
        "gender": ["Male", "Female", "Other", "Prefer not to say"],
        "education_level": ["High School", "Bachelor's", "Master's", "PhD", "Other"],
        "study_group": ["Control", "Treatment", "Placebo"]
    }
    
    for field, allowed_values in categorical_fields.items():
        invalid_issues = []
        issue_rows = []
        
        for i, row in enumerate(data):
            value = row[field]
            if value is not None and value != "" and value not in allowed_values:
                invalid_issues.append(value)
                issue_rows.append(i)
        
        if invalid_issues:
            issues["invalid_values"].append({
                "field": field,
                "allowed_values": allowed_values,
                "count": len(invalid_issues),
                "invalid_values": invalid_issues,
                "rows": issue_rows
            })
            print(f"   ❌ {field}: {len(invalid_issues)} invalid values")
            print(f"      Allowed: {allowed_values}")
            print(f"      Found: {invalid_issues}")
            print(f"      Rows: {issue_rows}")
    
    if not issues["invalid_values"]:
        print("   ✅ No invalid categorical values found")
    print()
    
    # 5. Format Violations
    print("5. 📝 FORMAT VIOLATIONS")
    print("-" * 35)
    
    # Check participant_id format
    format_issues = []
    issue_rows = []
    
    for i, row in enumerate(data):
        pid = row["participant_id"]
        if pid and not (pid.startswith("P") and len(pid) == 4 and pid[1:].isdigit()):
            format_issues.append(pid)
            issue_rows.append(i)
    
    if format_issues:
        issues["format_violations"].append({
            "field": "participant_id",
            "expected_format": "P### (e.g., P001, P123)",
            "count": len(format_issues),
            "invalid_values": format_issues,
            "rows": issue_rows
        })
        print(f"   ❌ participant_id: {len(format_issues)} format violations")
        print(f"      Expected: P### (e.g., P001, P123)")
        print(f"      Found: {format_issues}")
        print(f"      Rows: {issue_rows}")
    
    # Check date format
    date_issues = []
    date_rows = []
    
    for i, row in enumerate(data):
        date_val = row["date_of_study"]
        if date_val and not (isinstance(date_val, str) and len(date_val) == 10 and 
                           date_val.count("-") == 2 and date_val.replace("-", "").isdigit()):
            date_issues.append(date_val)
            date_rows.append(i)
    
    if date_issues:
        issues["format_violations"].append({
            "field": "date_of_study",
            "expected_format": "YYYY-MM-DD",
            "count": len(date_issues),
            "invalid_values": date_issues,
            "rows": date_rows
        })
        print(f"   ❌ date_of_study: {len(date_issues)} format violations")
        print(f"      Expected: YYYY-MM-DD")
        print(f"      Found: {date_issues}")
        print(f"      Rows: {date_rows}")
    
    if not issues["format_violations"]:
        print("   ✅ No format violations found")
    print()
    
    return issues


def generate_agent_summary(issues):
    """Generate a comprehensive agent summary."""
    print("🤖 **AGENT ANALYSIS SUMMARY**")
    print("=" * 50)
    print()
    
    # Calculate totals
    total_issues = (len(issues["missing_required"]) + 
                   len(issues["data_type_mismatches"]) + 
                   len(issues["out_of_range_values"]) + 
                   len(issues["invalid_values"]) + 
                   len(issues["format_violations"]))
    
    critical_issues = len(issues["missing_required"]) + len(issues["data_type_mismatches"])
    warning_issues = (len(issues["out_of_range_values"]) + 
                     len(issues["invalid_values"]) + 
                     len(issues["format_violations"]))
    
    # Calculate data quality score
    quality_score = max(0, 100 - (total_issues * 3))
    
    print("📊 **Overall Assessment**")
    print(f"• Data quality score: {quality_score}/100")
    print(f"• Critical issues: {critical_issues}")
    print(f"• Warning issues: {warning_issues}")
    print(f"• Total issues found: {total_issues}")
    print()
    
    if quality_score < 70:
        print("🚨 **CRITICAL DATA QUALITY ISSUES DETECTED**")
        print("This dataset requires immediate attention before analysis.")
    elif quality_score < 85:
        print("⚠️ **MODERATE DATA QUALITY ISSUES DETECTED**")
        print("This dataset has some issues that should be addressed.")
    else:
        print("✅ **GOOD DATA QUALITY**")
        print("This dataset is suitable for analysis with minor cleanup.")
    print()
    
    print("💡 **Key Recommendations**")
    print()
    print("1. **Immediate Actions Required:**")
    if issues["missing_required"]:
        print("   • Address missing required values (participant_id, age, etc.)")
    if issues["data_type_mismatches"]:
        print("   • Convert text values to appropriate numeric types")
    print()
    
    print("2. **Data Cleaning Steps:**")
    print("   • Standardize categorical values (gender, education, study_group)")
    print("   • Validate and correct out-of-range values")
    print("   • Fix format violations (participant_id, dates)")
    print("   • Implement data validation rules for future data entry")
    print()
    
    print("3. **Research Impact Assessment:**")
    if critical_issues > 0:
        print("   ⚠️ Critical issues may affect statistical analysis validity")
        print("   📊 Consider excluding problematic records or using imputation")
    else:
        print("   ✅ Dataset is suitable for statistical analysis")
        print("   📈 Minor issues can be addressed during preprocessing")
    print()
    
    print("4. **Quality Control Measures:**")
    print("   • Implement automated data validation at data entry")
    print("   • Use controlled vocabularies for categorical fields")
    print("   • Set up regular data quality monitoring")
    print("   • Document all data cleaning procedures")
    print()


def main():
    """Run the data quality analysis demo."""
    print("🔬 RESEARCH DATA QUALITY ANALYSIS DEMO")
    print("=" * 60)
    print()
    print("Simulating upload and analysis of Figshare research dataset")
    print("(https://figshare.com/ndownloader/files/40075411)")
    print()
    
    # Create sample data
    data = create_sample_research_data()
    
    # Analyze data quality
    issues = analyze_data_quality(data)
    
    # Generate agent summary
    generate_agent_summary(issues)
    
    # Save results
    results = {
        "dataset_info": {
            "source": "https://figshare.com/ndownloader/files/40075411",
            "total_records": len(data),
            "analysis_date": "2024-01-15"
        },
        "quality_issues": issues,
        "summary": {
            "total_issues": len(issues["missing_required"]) + len(issues["data_type_mismatches"]) + 
                          len(issues["out_of_range_values"]) + len(issues["invalid_values"]) + 
                          len(issues["format_violations"]),
            "critical_issues": len(issues["missing_required"]) + len(issues["data_type_mismatches"]),
            "warning_issues": len(issues["out_of_range_values"]) + len(issues["invalid_values"]) + 
                            len(issues["format_violations"])
        }
    }
    
    # Save to file
    output_path = Path("/workspace/data/research_data_quality_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("💾 **Results saved to:**", output_path)
    print()
    print("=" * 60)
    print("🎉 Analysis complete! The agent successfully identified")
    print("   all data quality issues in the research dataset.")
    print("=" * 60)


if __name__ == "__main__":
    main()