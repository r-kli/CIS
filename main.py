import streamlit as st
import pandas as pd
from excel_processor import ExcelComparator
from utils import validate_files
import io

st.set_page_config(
    page_title="CIS Benchmark Comparison Tool",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("CIS Benchmark Excel Comparison Tool")
    
    st.markdown("""
    ### Instructions:
    1. Upload two Excel files containing CIS benchmark regulations
    2. The files should have similar structure but may contain different versions
    3. The tool will compare regulations based on their numbering (e.g., 1.1, 1.2.4)
    4. Results will highlight differences in green and can be downloaded
    """)

    col1, col2 = st.columns(2)
    
    with col1:
        file1 = st.file_uploader("Upload first Excel file (older version)", type=['xlsx', 'xls'])
    
    with col2:
        file2 = st.file_uploader("Upload second Excel file (newer version)", type=['xlsx', 'xls'])

    if file1 and file2:
        if validate_files(file1, file2):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                comparator = ExcelComparator(file1, file2)
                
                status_text.text("Reading Excel files...")
                progress_bar.progress(20)
                
                status_text.text("Processing sheets...")
                progress_bar.progress(40)
                
                differences_df = comparator.compare_files(
                    lambda progress: progress_bar.progress(40 + int(progress * 40))
                )
                
                status_text.text("Generating output file...")
                progress_bar.progress(90)
                
                if not differences_df.empty:
                    output = comparator.generate_output_excel()
                    progress_bar.progress(100)
                    status_text.text("Comparison completed!")
                    
                    st.success("Files compared successfully! Download the results below.")
                    
                    # Create download button
                    buffer = io.BytesIO()
                    output.save(buffer)
                    buffer.seek(0)
                    
                    st.download_button(
                        label="Download Comparison Results",
                        data=buffer,
                        file_name="cis_benchmark_comparison.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    # Display preview
                    st.subheader("Preview of Differences")
                    st.dataframe(differences_df)
                else:
                    st.info("No differences found between the files.")
                    
            except Exception as e:
                st.error(f"An error occurred during comparison: {str(e)}")
                
        else:
            st.error("Please ensure both files are valid Excel files with CIS benchmark data.")

if __name__ == "__main__":
    main()
