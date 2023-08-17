# import pdfplumber
# import fitz
# import re

# pdf_path = '/home/user/Documents/AIS_2.pdf'

# # Step 1: Text Extraction using PyMuPDF (you already have this part)
# def extract_text_from_pdf(pdf_path):
#     pdf_document = fitz.open(pdf_path)
#     text = ""
#     for page_num in range(pdf_document.page_count):
#         page = pdf_document[page_num]
#         text += page.get_text()
#     return text

# pdf_text = extract_text_from_pdf(pdf_path)

# # Step 2: Table Extraction using pdfplumber
# tables = []
# with pdfplumber.open(pdf_path) as pdf:
#     for page in pdf.pages:
#         extracted_table = page.extract_table()
#         tables.append(extracted_table)

# # Step 3: Text Parsing (you'll need to customize this based on your PDF's structure)
# # Example: Extract PAN and Name using regular expressions
# pan_pattern = re.compile(r"Permanent Account Number \(PAN\)(.*?)Name of Assessee", re.DOTALL)
# name_pattern = re.compile(r"Name of Assessee\n(.*?)Date of Birth", re.DOTALL)

# pan_match = pan_pattern.search(pdf_text)
# name_match = name_pattern.search(pdf_text)

# if pan_match:
#     pan = pan_match.group(1).strip()
# else:
#     pan = None

# if name_match:
#     name = name_match.group(1).strip()
# else:
#     name = None

# # Step 4: Organize extracted data
# extracted_data = {
#     'PAN': pan,
#     'Name': name,
#     'Tables': tables,  # Add other extracted data as needed
# }

# # Print or use the extracted data
# print(extracted_data)

import pdfplumber
import fitz
import re

pdf_path = '/home/user/Documents/AIS_2.pdf'

# Step 1: Text Extraction using PyMuPDF (you already have this part)
def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()
    return text

pdf_text = extract_text_from_pdf(pdf_path)

# Step 2: Table Extraction using pdfplumber
tables = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        extracted_table = page.extract_table()
        tables.append(extracted_table)

# Step 3: Extract data from specific tables
table_names = [
    "Salary", "Dividend", "Interest from deposit", "Cash payments",
    "Outward foreign remittance/purchase of foreign currency",
    "Interest from savings bank", "Sale of securities and units of mutual fund",
    "Purchase of time deposits", "Purchase of securities and units of mutual funds"
]

table_data = {}

for table_name in table_names:
    table_data[table_name] = []
    for table in tables:
        found_table = False
        for row in table:
            if any(cell and cell.strip() == table_name for cell in row):
                found_table = True
                continue
            if found_table:
                table_data[table_name].append(row)

# Step 4: Organize extracted data
extracted_data = {
    'Tables': table_data,
    # Add other extracted data like PAN and Name if needed
}

# Print or use the extracted data for each table
for table_name, table_rows in extracted_data['Tables'].items():
    print(f"Table: {table_name}")
    for row in table_rows:
        print(row)

