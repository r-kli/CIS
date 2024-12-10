import pandas as pd
import re

def validate_files(file1, file2):
    """
    Validate that the uploaded files are valid Excel files containing CIS benchmark data.
    """
    try:
        print("Starting file validation...")
        # Read all sheets to find the one with benchmark data
        xlsx1 = pd.ExcelFile(file1)
        xlsx2 = pd.ExcelFile(file2)
        
        print(f"File 1 sheets: {xlsx1.sheet_names}")
        print(f"File 2 sheets: {xlsx2.sheet_names}")
        
        # Try each sheet until we find one with valid data
        for sheet_name in xlsx1.sheet_names:
            try:
                df1 = pd.read_excel(xlsx1, sheet_name)
                if not df1.empty and len(df1.columns) > 0:
                    print(f"Found valid sheet in file 1: {sheet_name}")
                    break
            except Exception as e:
                print(f"Error reading sheet {sheet_name} in file 1: {str(e)}")
                continue
        
        for sheet_name in xlsx2.sheet_names:
            try:
                df2 = pd.read_excel(xlsx2, sheet_name)
                if not df2.empty and len(df2.columns) > 0:
                    print(f"Found valid sheet in file 2: {sheet_name}")
                    break
            except Exception as e:
                print(f"Error reading sheet {sheet_name} in file 2: {str(e)}")
                continue
        
        if df1.empty or df2.empty:
            print("One or both files contain no valid data")
            return False
            
        # Function to check for any numeric-like patterns in the text
        def has_regulation_format(text):
            if pd.isna(text):
                return False
            text = str(text).strip()
            # More permissive pattern that looks for any number-like structure
            return bool(re.search(r'\d', text))
        
        # Check first few columns for regulation numbers
        def find_regulation_column(df):
            for col_idx in range(min(3, len(df.columns))):
                valid_count = sum(1 for val in df.iloc[:20, col_idx] if has_regulation_format(val))
                if valid_count >= 2:  # Only need 2 matches to consider it valid
                    return True
            return False
        
        file1_valid = find_regulation_column(df1)
        file2_valid = find_regulation_column(df2)
        
        print(f"Validation results - File 1: {file1_valid}, File 2: {file2_valid}")
        return file1_valid and file2_valid
        
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
