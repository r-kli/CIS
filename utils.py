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
        
        # Check specifically for Level 1 or Level 2 sheets
        benchmark_sheets = ['Level 1', 'Level 2']
        
        def validate_benchmark_sheet(excel_file, sheet_name):
            try:
                df = pd.read_excel(excel_file, sheet_name)
                print(f"Reading sheet: {sheet_name}")
                print(f"Columns found: {df.columns.tolist()}")
                print(f"First few rows of data:\n{df.head(3)}")
                
                if df.empty or len(df.columns) < 1:
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
        
        # Try to validate using any of the benchmark sheets
        for sheet in benchmark_sheets:
            if sheet in xlsx1.sheet_names and sheet in xlsx2.sheet_names:
                file1_valid = validate_benchmark_sheet(xlsx1, sheet)
                file2_valid = validate_benchmark_sheet(xlsx2, sheet)
                if file1_valid and file2_valid:
                    print(f"Both files validated successfully using sheet: {sheet}")
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
