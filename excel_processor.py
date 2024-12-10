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
        self.red_fill = PatternFill(start_color='FF9999', end_color='FF9999', fill_type='solid')

    def create_reg_key(self, row, section_col, rec_col=None):
        """Create a regulation key that handles empty/NaN recommendation values."""
        section = str(row[section_col]).strip()
        rec = ""
        if rec_col is not None and rec_col in row.index:
            rec_value = row[rec_col]
            if pd.notna(rec_value) and str(rec_value).strip():
                rec = str(rec_value).strip()
        return f"{section}_{rec}"

    def compare_files(self, progress_callback=None):
        """Compare two Excel files and identify differences."""
        xlsx1 = pd.ExcelFile(self.file1)
        xlsx2 = pd.ExcelFile(self.file2)
        
        all_differences = []
        total_sheets = len(xlsx1.sheet_names)
        
        for idx, sheet_name in enumerate(xlsx1.sheet_names):
            if sheet_name in xlsx2.sheet_names:
                df1 = pd.read_excel(xlsx1, sheet_name)
                df2 = pd.read_excel(xlsx2, sheet_name)
                
                # Get the section column (required)
                section_col = df1.columns[0]  # 'Section #'
                # Get recommendation column if it exists
                rec_col = df1.columns[1] if len(df1.columns) > 1 else None
                
                # Create dictionaries for easy lookup using combined key
                df1_dict = {}
                df2_dict = {}
                
                # Build dictionaries with safe key creation
                for _, row in df1.iterrows():
                    key = self.create_reg_key(row, section_col, rec_col)
                    df1_dict[key] = row
                
                for _, row in df2.iterrows():
                    key = self.create_reg_key(row, section_col, rec_col)
                    df2_dict[key] = row
                
                # Compare matching regulations
                for reg_key in set(df1_dict.keys()) | set(df2_dict.keys()):
                    if reg_key in df1_dict and reg_key in df2_dict:
                        row1 = df1_dict[reg_key]
                        row2 = df2_dict[reg_key]
                        
                        # Compare each cell
                        for col in df1.columns:
                            if row1[col] != row2[col] and not (pd.isna(row1[col]) and pd.isna(row2[col])):
                                all_differences.append({
                                    'Sheet': sheet_name,
                                    'Regulation': reg_key,
                                    'Column': col,
                                    'Old_Value': row1[col],
                                    'New_Value': row2[col]
                                })
                    else:
                        # Handle added/removed regulations
                        if reg_key in df1_dict:
                            row = df1_dict[reg_key]
                            all_differences.append({
                                'Sheet': sheet_name,
                                'Regulation': reg_key,
                                'Column': 'Status',
                                'Old_Value': 'Present',
                                'New_Value': 'Removed'
                            })
                        else:
                            row = df2_dict[reg_key]
                            all_differences.append({
                                'Sheet': sheet_name,
                                'Regulation': reg_key,
                                'Column': 'Status',
                                'Old_Value': 'Missing',
                                'New_Value': 'Added'
                            })
            
            if progress_callback:
                progress_callback((idx + 1) / total_sheets)
        
        self.differences_df = pd.DataFrame(all_differences)
        return self.differences_df

    def generate_output_excel(self):
        """Generate formatted Excel output maintaining original structure with differences."""
        xlsx1 = pd.ExcelFile(self.file1)
        xlsx2 = pd.ExcelFile(self.file2)
        
        wb = Workbook()
        wb.remove(wb.active)  # Remove default sheet
        
        # Process each sheet
        for sheet_name in xlsx1.sheet_names:
            if sheet_name in xlsx2.sheet_names:
                # Read both sheets
                df1 = pd.read_excel(xlsx1, sheet_name)
                df2 = pd.read_excel(xlsx2, sheet_name)
                
                # Create worksheet
                ws = wb.create_sheet(sheet_name)
                
                # Write headers
                for col_idx, col_name in enumerate(df1.columns, 1):
                    ws.cell(row=1, column=col_idx, value=col_name)
                
                # Get the section column (required)
                section_col = df1.columns[0]  # 'Section #'
                # Get recommendation column if it exists
                rec_col = df1.columns[1] if len(df1.columns) > 1 else None
                
                # Get differences for this sheet
                sheet_differences = self.differences_df[self.differences_df['Sheet'] == sheet_name]
                
                # Track rows that need difference rows
                diff_regulations = set(sheet_differences['Regulation'].unique())
                
                # Write data
                output_row = 2  # Start after headers
                
                # Get sets of regulation keys for comparison
                reg_set1 = set(self.create_reg_key(row, section_col, rec_col)
                             for _, row in df1.iterrows())
                reg_set2 = set(self.create_reg_key(row, section_col, rec_col)
                             for _, row in df2.iterrows())
                
                # Process original file rows
                for _, row in df1.iterrows():
                    reg_key = self.create_reg_key(row, section_col, rec_col)
                    
                    # Write original row
                    for col_idx, value in enumerate(row, 1):
                        cell = ws.cell(row=output_row, column=col_idx, value=value)
                        # Highlight removed regulations in red
                        if reg_key not in reg_set2:
                            cell.fill = self.red_fill
                    
                    # If this regulation exists in both files and has differences
                    if reg_key in diff_regulations and reg_key in reg_set2:
                        output_row += 1
                        # Find matching row in df2 using the reg_key
                        for _, new_row in df2.iterrows():
                            if self.create_reg_key(new_row, section_col, rec_col) == reg_key:
                                # Get columns with differences for this regulation
                                diff_columns = sheet_differences[
                                    sheet_differences['Regulation'] == reg_key
                                ]['Column'].unique()
                                
                                # Write new values row with green highlighting for changed cells
                                for col_idx, value in enumerate(new_row, 1):
                                    cell = ws.cell(row=output_row, column=col_idx, value=value)
                                    if df1.columns[col_idx-1] in diff_columns:
                                        cell.fill = self.green_fill
                                break
                    
                    output_row += 1
                
                # Add new regulations (those in file2 but not in file1)
                new_regs = reg_set2 - reg_set1
                if new_regs:
                    for reg_key in sorted(new_regs):
                        for _, new_row in df2.iterrows():
                            if self.create_reg_key(new_row, section_col, rec_col) == reg_key:
                                # Write new regulation row with all cells in green
                                for col_idx, value in enumerate(new_row, 1):
                                    cell = ws.cell(row=output_row, column=col_idx, value=value)
                                    cell.fill = self.green_fill
                                output_row += 1
                                break
                
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
