from docx import Document

def find_subtotal_in_docx(docx_path, keyword="SUBTOTAL"):
    # Load the existing Word document
    doc = Document(docx_path)
    
    # Iterate over tables
    for table_idx, table in enumerate(doc.tables):
        # Iterate over rows in the current table
        for row_idx, row in enumerate(table.rows):
            # Iterate over cells in the current row
            for idx,cell in enumerate(row.cells):
                if keyword in cell.text:
                    print(f"Keyword '{keyword}' found in Table {table_idx}, Row {row_idx}, cell number {idx}.")
                    return table_idx, row_idx
    
    print(f"Keyword '{keyword}' not found in any table.")
    return None, None

# Usage
docx_file_path = r'media\invoices\template.docx'
find_subtotal_in_docx(docx_file_path,keyword='INVOICE NO.')
