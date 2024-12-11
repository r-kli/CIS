import pandas as pd
import re

def validate_files(file1, file2):
    """
    Validate that the uploaded files are valid Excel files containing CIS benchmark data.
    """
    try:
        print("Starting file validation...")
        xlsx1 = pd.ExcelFile(file1)
        xlsx2 = pd.ExcelFile(file2)
        
        print(f"File 1 sheets: {xlsx1.sheet_names}")
        print(f"File 2 sheets: {xlsx2.sheet_names}")
        
        # Check for sheets containing Level 1 or Level 2
        def find_benchmark_sheets(sheet_names):
            level1_sheets = [s for s in sheet_names if 'Level 1' in s]
            level2_sheets = [s for s in sheet_names if 'Level 2' in s]
            return level1_sheets + level2_sheets
        
        def validate_benchmark_sheet(excel_file, sheet_name):
            try:
                print(f"Validating sheet: {sheet_name}")
                df = pd.read_excel(excel_file, sheet_name)
                print(f"Columns found: {df.columns.tolist()}")
                print(f"First few rows of data:\n{df.head(3)}")
                
                if df.empty or len(df.columns) < 1:
                    print(f"Sheet {sheet_name} is empty or has no columns")
                    return False
                
                # Look for any column containing regulation numbers (checking first 3 columns)
                for col_idx in range(min(3, len(df.columns))):
                    # Check first 10 non-empty values in the column
                    values = df.iloc[:20, col_idx].dropna().astype(str).tolist()[:10]
                    print(f"Column {col_idx} values: {values}")
                    
                    # Count values that look like regulation numbers (e.g., "1.2", "1.2.3")
                    valid_count = sum(1 for val in values if bool(re.search(r'\d+\.?\d*', str(val).strip())))
                    if valid_count >= 2:
                        print(f"Found valid regulation column: {col_idx}")
                        return True
                return False
            except Exception as e:
                print(f"Error processing sheet {sheet_name}: {str(e)}")
                return False
        
        # Find and validate benchmark sheets in both files
        sheets1 = find_benchmark_sheets(xlsx1.sheet_names)
        sheets2 = find_benchmark_sheets(xlsx2.sheet_names)
        
        print(f"Found benchmark sheets in file 1: {sheets1}")
        print(f"Found benchmark sheets in file 2: {sheets2}")
        
        if not sheets1 or not sheets2:
            print("No benchmark sheets found in one or both files")
            return False
            
        # Try to validate at least one sheet from each file
        for sheet1 in sheets1:
            file1_valid = validate_benchmark_sheet(xlsx1, sheet1)
            if file1_valid:
                for sheet2 in sheets2:
                    file2_valid = validate_benchmark_sheet(xlsx2, sheet2)
                    if file2_valid:
                        print(f"Files validated successfully using sheets: {sheet1} and {sheet2}")
                        return True
        
        print("No valid benchmark sheets found in both files")
        return False
        
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return False

def format_regulation_number(number):
    """
    Format regulation numbers consistently for comparison.
    """
    if pd.isna(number):
        return ""
    return str(number).strip()
