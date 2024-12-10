import pandas as pd
import re

def validate_files(file1, file2):
    """
    Validate that the uploaded files are valid Excel files containing CIS benchmark data.
    """
    try:
        # Try to read the first few rows of each file
        df1 = pd.read_excel(file1, nrows=5)
        df2 = pd.read_excel(file2, nrows=5)
        
        # Check if files have at least one column
        if df1.empty or df2.empty:
            return False
        
        # Check if the first column contains regulation-like numbers
        def has_regulation_numbers(df):
            first_col = df.iloc[:, 0]
            pattern = re.compile(r'^\d+(\.\d+)*$')
            return any(isinstance(val, str) and pattern.match(val.strip()) for val in first_col if isinstance(val, str))
        
        return has_regulation_numbers(df1) and has_regulation_numbers(df2)
        
    except Exception:
        return False

def format_regulation_number(number):
    """
    Format regulation numbers consistently for comparison.
    """
    if pd.isna(number):
        return ""
    return str(number).strip()
