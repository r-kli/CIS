import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import PatternFill
import re

class ExcelComparator:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
        self.differences_df = pd.DataFrame()
        self.green_fill = PatternFill(start_color='90EE90', end_color='90EE90', fill_type='solid')

    def parse_regulation_number(self, number):
        """Parse regulation numbers into comparable format."""
        if pd.isna(number):
            return []
        # Convert to string and clean up
        number = str(number).strip()
        # Split by dots and convert to integers where possible
        parts = []
        for part in number.split('.'):
            try:
                parts.append(int(part))
            except ValueError:
                parts.append(part)
        return parts

    def compare_files(self, progress_callback=None):
        """Compare two Excel files and identify differences."""
        # Read all sheets from both files
        xlsx1 = pd.ExcelFile(self.file1)
        xlsx2 = pd.ExcelFile(self.file2)
        
        all_differences = []
        total_sheets = len(xlsx1.sheet_names)
        
        for idx, sheet_name in enumerate(xlsx1.sheet_names):
            if sheet_name in xlsx2.sheet_names:
                df1 = pd.read_excel(xlsx1, sheet_name)
                df2 = pd.read_excel(xlsx2, sheet_name)
                
                # Ensure regulation number column exists
                reg_col = df1.columns[0]  # Assuming first column contains regulation numbers
                
                # Create dictionaries for easy lookup
                df1_dict = {str(row[reg_col]): row for _, row in df1.iterrows()}
                df2_dict = {str(row[reg_col]): row for _, row in df2.iterrows()}
                
                # Compare matching regulations
                for reg_num in set(df1_dict.keys()) | set(df2_dict.keys()):
                    if reg_num in df1_dict and reg_num in df2_dict:
                        row1 = df1_dict[reg_num]
                        row2 = df2_dict[reg_num]
                        
                        # Compare each cell
                        for col in df1.columns:
                            if row1[col] != row2[col] and not (pd.isna(row1[col]) and pd.isna(row2[col])):
                                all_differences.append({
                                    'Sheet': sheet_name,
                                    'Regulation': reg_num,
                                    'Column': col,
                                    'Old Value': row1[col],
                                    'New Value': row2[col]
                                })
                    else:
                        # Handle added/removed regulations
                        if reg_num in df1_dict:
                            row = df1_dict[reg_num]
                            all_differences.append({
                                'Sheet': sheet_name,
                                'Regulation': reg_num,
                                'Column': 'Status',
                                'Old Value': 'Present',
                                'New Value': 'Removed'
                            })
                        else:
                            row = df2_dict[reg_num]
                            all_differences.append({
                                'Sheet': sheet_name,
                                'Regulation': reg_num,
                                'Column': 'Status',
                                'Old Value': 'Missing',
                                'New Value': 'Added'
                            })
            
            if progress_callback:
                progress_callback((idx + 1) / total_sheets)
        
        self.differences_df = pd.DataFrame(all_differences)
        return self.differences_df

    def generate_output_excel(self):
        """Generate formatted Excel output with differences highlighted."""
        wb = Workbook()
        ws = wb.active
        ws.title = "Differences"
        
        # Write headers
        headers = ['Sheet', 'Regulation', 'Column', 'Old Value', 'New Value']
        for col, header in enumerate(headers, 1):
            ws.cell(row=1, column=col, value=header)
        
        # Write data and apply formatting
        for row_idx, row in enumerate(self.differences_df.itertuples(), 2):
            ws.cell(row=row_idx, column=1, value=row.Sheet)
            ws.cell(row=row_idx, column=2, value=row.Regulation)
            ws.cell(row=row_idx, column=3, value=row.Column)
            ws.cell(row=row_idx, column=4, value=str(row.Old_Value))
            
            # Highlight new value in green
            new_value_cell = ws.cell(row=row_idx, column=5, value=str(row.New_Value))
            new_value_cell.fill = self.green_fill
        
        # Adjust column widths
        for column in ws.columns:
            max_length = 0
            column = list(column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column[0].column_letter].width = adjusted_width
        
        return wb
