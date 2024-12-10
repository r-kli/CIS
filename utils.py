import pandas as pd
import re

def validate_files(file1, file2):
    """
    Validate that the uploaded files are valid Excel files containing CIS benchmark data.
    """
    try:
        # Try to read more rows to ensure we catch regulation numbers
        df1 = pd.read_excel(file1, nrows=20)
        df2 = pd.read_excel(file2, nrows=20)
        
        # Check if files have at least one column
        if df1.empty or df2.empty or len(df1.columns) < 1 or len(df2.columns) < 1:
            return False
        
        # Check if the first column contains regulation-like numbers
        def has_regulation_numbers(df):
            first_col = df.iloc[:, 0]
            # More lenient pattern that allows for various regulation number formats
            pattern = re.compile(r'.*\d+(\.\d+)*.*')
            valid_entries = 0
            for val in first_col:
                if isinstance(val, (str, int, float)) and not pd.isna(val):
                    val_str = str(val).strip()
                    if pattern.match(val_str):
                        valid_entries += 1
            # Return True if we find at least 3 valid regulation numbers
            return valid_entries >= 3
        
        return has_regulation_numbers(df1) and has_regulation_numbers(df2)
        
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
