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

# # Step 3: Extract data from specific tables
# table_names = [
#     "Salary", "Dividend", "Interest from deposit", "Cash payments",
#     "Outward foreign remittance/purchase of foreign currency",
#     "Interest from savings bank", "Sale of securities and units of mutual fund",
#     "Purchase of time deposits", "Purchase of securities and units of mutual funds"
# ]

# table_data = {}

# for table_name in table_names:
#     table_data[table_name] = []
#     for table in tables:
#         found_table = False
#         for row in table:
#             if any(cell and cell.strip() == table_name for cell in row):
#                 found_table = True
#                 continue
#             if found_table:
#                 table_data[table_name].append(row)

# # Step 4: Organize extracted data
# extracted_data = {
#     'Tables': table_data,
#     # Add other extracted data like PAN and Name if needed
# }

# # Print or use the extracted data for each table
# for table_name, table_rows in extracted_data['Tables'].items():
#     print(f"Table: {table_name}")
#     for row in table_rows:
#         print(row)


# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import pytesseract

# # PDF path
# pdf_path = '/home/user/Documents/AIS_2.pdf'


# # Keywords to check for
# master_keywords = [
#     "Salary", "Dividend", "Interest from deposit", "Cash payments",
#     "Outward foreign remittance/purchase of foreign currency",
#     "Interest from savings bank", "Sale of securities and units of mutual fund",
#     "Purchase of time deposits", "Purchase of securities and units of mutual funds"
# ]

# title_keywords = {
#     "Part B1-Information relating to tax deducted or collected at source": [
#         "Salary", "Interest from deposit"
#     ],
#     "Part B2-Information relating to specified financial transaction (SFT)": [
#         "Interest from savings bank", "Interest from deposit",
#         "Sale of securities and units of mutual fund",
#         "Purchase of securities and units of mutual funds"
#     ]
# }

# # Convert the PDF to images
# images = convert_from_path(pdf_path)

# # Initialize the data dictionary
# data_dict = {
#     'AIS_Form': {
#         'name_of_assessee': None,
#         'date_of_birth': None,
#         'mobile_number': None,
#         'email_address': None,
#         'address_of_assignee': None,
#         'pan_employee': None,
#         'assessment_year': None,
#     },
#     'SalaryAISForm': {
#         'information_code': None,
#         'information_description': None,
#         'information_source': None,
#         'count': None,
#         'amount': None,
#         'salary_quarters': []
#     },
#     # Add more sections as needed...
# }

# # Dictionary to store extracted data
# extracted_data = {}

# for image in images:
#     image_np = np.array(image)

#     # Convert the image to grayscale and threshold it for contour detection
#     gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

#     # Find contours
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         height, width, _ = image_np.shape
#         y_expanded = max(0, y - int(0.2 * h))
#         x_expanded = max(0, x)
#         y_end = min(height, y + h)
#         x_end = min(width, x + w)

#         roi = image_np[y_expanded:y_end, x_expanded:x_end]
#         text = pytesseract.image_to_string(roi)

#         found_title = None
#         for title, field_names in title_keywords.items():
#             if title in text:
#                 found_title = title
#                 fields = field_names
#                 break

#         if found_title:
#             table_data = {"Title": found_title}
#             rows = text.strip().split("\n")
#             header_row = rows[0].split("\t")  # Assuming tab-separated columns

#             for row in rows[1:]:
#                 row_data = row.split("\t")
#                 row_dict = {field: value for field, value in zip(fields, row_data)}
#                 table_data[row_data[0]] = row_dict

#             # Store the table data in the extracted_data dictionary
#             if found_title in extracted_data:
#                 extracted_data[found_title].append(table_data)
#             else:
#                 extracted_data[found_title] = [table_data]

# # Process and restructure the Salary table data
# def process_salary_table(table_data):
#     salary_info = {
#         'information_code': None,
#         'information_description': None,
#         'information_source': None,
#         'count': None,
#         'amount': None,
#         'salary_quarters': []
#     }

#     for row_data in table_data.values():
#         if row_data['information_code']:
#             salary_info['information_code'] = row_data['information_code']
#             salary_info['information_description'] = row_data['information_description']
#             salary_info['information_source'] = row_data['information_source']
#             salary_info['count'] = row_data['count']
#             salary_info['amount'] = row_data['amount']
#         else:
#             quarter_data = {
#                 'salary_quater': row_data['Quarters'],
#                 'salary_dop_credit': row_data['Date of Payment/Credit'],
#                 'salary_amount_paid_credited': row_data['Amount Paid/Credited'],
#                 'salary_tds_deducted': row_data['TDS Deducted'],
#                 'salary_tds_deposited': row_data['TDS Deposited'],
#                 'salary_status': row_data['Status']
#             }
#             salary_info['salary_quarters'].append(quarter_data)

#     return salary_info

# processed_salary_data = []
# for title, table_list in extracted_data.items():
#     if title in title_keywords:
#         fields = title_keywords[title]
#         for table_data in table_list:
#             if fields[0] in table_data:
#                 processed_salary_data.append(process_salary_table(table_data))

# for idx, salary_info in enumerate(processed_salary_data, start=1):
#     print(f"Processed Salary Data {idx}:")
#     print(salary_info)
#     print("\n")

import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract

# pdf_path = '/path/to/your/pdf/file.pdf'
pdf_path = '/home/user/Documents/AIS_2.pdf'


# Convert the PDF to images
images = convert_from_path(pdf_path)

# Keywords to check for
keywords = [
    "Salary", "Dividend", "Interest from deposit", "Cash payments",
    "Outward foreign remittance/purchase of foreign currency",
    "Interest from savings bank", "Sale of securities and units of mutual fund",
    "Purchase of time deposits", "Purchase of securities and units of mutual funds"
]

# Initialize the data dictionary
data_dict = {}

# Initialize current section
current_section = None

# Loop through the images
for image in images:
    text = pytesseract.image_to_string(image)
    
    # Check for keywords to identify sections
    for keyword in keywords:
        if keyword in text:
            current_section = keyword
            data_dict[current_section] = []
            break
    
    # Process the extracted text for the current section
    if current_section:
        lines = text.strip().split('\n')
        table_headers = lines[0].split('\t')
        
        for line in lines[1:]:
            data_entry = {}
            values = line.split('\t')
            
            for header, value in zip(table_headers, values):
                data_entry[header] = value
            
            data_dict[current_section].append(data_entry)

# Print the extracted data
for section, data_entries in data_dict.items():
    print(f"Section: {section}")
    for idx, entry in enumerate(data_entries, start=1):
        print(f"Entry {idx}:")
        print(entry)
        print("\n")
