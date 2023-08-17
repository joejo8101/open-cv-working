# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import pytesseract

# pdf_path = '/home/user/Documents/AIS_1.pdf'

# # Convert the PDF to images
# images = convert_from_path(pdf_path)

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
#             data_dict = {"Title": found_title}
#             rows = text.strip().split("\n")
#             header_row = rows[0].split("\t")  # Assuming tab-separated columns

#             for row in rows[1:]:
#                 row_data = row.split("\t")
#                 row_dict = {field: value for field, value in zip(fields, row_data)}
#                 data_dict[row_data[0]] = row_dict

#             extracted_data[found_title] = data_dict

# # Print the extracted data
# for title, data_dict in extracted_data.items():
#     print(f"Table with title: {title}")
#     print(data_dict)
#     print("\n")

import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract

pdf_path = '/home/user/Documents/AIS_1.pdf'

# Convert the PDF to images
images = convert_from_path(pdf_path)

# Keywords to check for
master_keywords = [
    "Salary", "Dividend", "Interest from deposit", "Cash payments",
    "Outward foreign remittance/purchase of foreign currency",
    "Interest from savings bank", "Sale of securities and units of mutual fund",
    "Purchase of time deposits", "Purchase of securities and units of mutual funds"
]

title_keywords = {
    "Part B1-Information relating to tax deducted or collected at source": [
        "Salary", "Interest from deposit"
    ],
    "Part B2-Information relating to specified financial transaction (SFT)": [
        "Interest from savings bank", "Interest from deposit",
        "Sale of securities and units of mutual fund",
        "Purchase of securities and units of mutual funds"
    ]
}

# Initialize the data dictionary
data_dict = {
    'AIS_Form': {
        'name_of_assessee': None,
        'date_of_birth': None,
        'mobile_number': None,
        'email_address': None,
        'address_of_assignee': None,
        'pan_employee': None,
        'assessment_year': None,
    },
    'SalaryAISForm': {
        'information_code': None,
        'information_description': None,
        'information_source': None,
        'count': None,
        'amount': None,
        'salary_quater': None,
        'salary_dop_credit': None,
        'salary_amount_paid_credited': None,
        'salary_tds_deducted': None,
        'salary_tds_deposited': None,
        'salary_status': None,
    },
    # Add more sections as needed...
}

# Dictionary to store extracted data
extracted_data = {}

for image in images:
    image_np = np.array(image)

    # Convert the image to grayscale and threshold it for contour detection
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        height, width, _ = image_np.shape
        y_expanded = max(0, y - int(0.2 * h))
        x_expanded = max(0, x)
        y_end = min(height, y + h)
        x_end = min(width, x + w)

        roi = image_np[y_expanded:y_end, x_expanded:x_end]
        text = pytesseract.image_to_string(roi)

        found_title = None
        for title, field_names in title_keywords.items():
            if title in text:
                found_title = title
                fields = field_names
                break

        if found_title:
            table_data = {"Title": found_title}
            print(text)
            rows = text.strip().split("\n")
            header_row = rows[0].split("\t")  # Assuming tab-separated columns

            for row in rows[1:]:
                row_data = row.split("\t")
                row_dict = {field: value for field, value in zip(fields, row_data)}
                table_data[row_data[0]] = row_dict

            # Store the table data in the extracted_data dictionary
            if found_title in extracted_data:
                extracted_data[found_title].append(table_data)
            else:
                extracted_data[found_title] = [table_data]

# Print the extracted data
for title, table_list in extracted_data.items():
    print(f"Table with title: {title}")
    for idx, data_dict in enumerate(table_list, start=1):
        print(f"Table {idx}:")
        print(data_dict)
        print("\n")

# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import pytesseract

# pdf_path = '/home/user/Documents/AIS_1.pdf'

# # Convert the PDF to images
# images = convert_from_path(pdf_path)

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
#         'title': None,
#         'information_code': None,
#         'information_description': None,
#         'information_source': None,
#         'count': None,
#         'amount': None,
#         'salary_quarters': []
#     },
#     'InterestAISForm': {
#         'title': None,
#         'information_code': None,
#         'information_description': None,
#         'information_source': None,
#         'count': None,
#         'amount': None,
#         'interest_transactions': []
#     }
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
#             table_data = {"title": found_title}
#             rows = text.strip().split("\n")
#             header_row = rows[0].split("\t")  # Assuming tab-separated columns

#             for row in rows[1:]:
#                 row_data = row.split("\t")
#                 row_dict = {field: value for field, value in zip(fields, row_data)}
#                 if "Salary" in found_title:
#                     table_data["information_code"] = row_dict.get("INFORMATION CODE")
#                     table_data["information_description"] = row_dict.get("INFORMATION DESCRIPTION")
#                     table_data["information_source"] = row_dict.get("INFORMATION SOURCE")
#                     table_data["count"] = row_dict.get("COUNT")
#                     table_data["amount"] = row_dict.get("AMOUNT")
#                     salary_quarter = row_dict.get("QUARTER")
#                     salary_dop_credit = row_dict.get("DATE OF PAYMENT/CREDIT")
#                     salary_amount_paid_credited = row_dict.get("AMOUNT PAID/CREDITED")
#                     salary_tds_deducted = row_dict.get("TDS DEDUCTED")
#                     salary_tds_deposited = row_dict.get("TDS DEPOSITED")
#                     salary_status = row_dict.get("STATUS")
#                     if salary_quarter and salary_dop_credit and salary_amount_paid_credited and \
#                             salary_tds_deducted and salary_tds_deposited and salary_status:
#                         salary_quarters = {
#                             "salary_quater": salary_quarter,
#                             "salary_dop_credit": salary_dop_credit,
#                             "salary_amount_paid_credited": salary_amount_paid_credited,
#                             "salary_tds_deducted": salary_tds_deducted,
#                             "salary_tds_deposited": salary_tds_deposited,
#                             "salary_status": salary_status,
#                         }
#                         table_data["salary_quarters"].append(salary_quarters)
#                 elif "Interest" in found_title:
#                     table_data["information_code"] = row_dict.get("INFORMATION CODE")
#                     table_data["information_description"] = row_dict.get("INFORMATION DESCRIPTION")
#                     table_data["information_source"] = row_dict.get("INFORMATION SOURCE")
#                     table_data["count"] = row_dict.get("COUNT")
#                     table_data["amount"] = row_dict.get("AMOUNT")
#                     reported_on = row_dict.get("REPORTED ON")
#                     account_number = row_dict.get("ACCOUNT NUMBER")
#                     account_type = row_dict.get("ACCOUNT TYPE")
#                     interest_amount = row_dict.get("INTEREST AMOUNT")
#                     status = row_dict.get("STATUS")
#                     if reported_on and account_number and account_type and interest_amount and status:
#                         interest_transaction = {
#                             "reported_on": reported_on,
#                             "account_number": account_number,
#                             "account_type": account_type,
#                             "interest_amount": interest_amount,
#                             "status": status
#                         }
#                         table_data["interest_transactions"].append(interest_transaction)

#             # Store the table data in the extracted_data dictionary
#             if found_title in extracted_data:
#                 extracted_data[found_title].append(table_data)
#             else:
#                 extracted_data[found_title] = [table_data]

# # Print the extracted data
# for title, table_list in extracted_data.items():
#     print(f"Table with title: {title}")
#     for idx, data_dict in enumerate(table_list, start=1):
#         print(f"Table {idx}:")
#         print(data_dict)
#         print("\n")

# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import pytesseract
# import tabula

# pdf_path = '/home/user/Documents/AIS_1.pdf'

# # Convert the PDF to images
# images = convert_from_path(pdf_path)

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
#         'title': None,
#         'information_code': None,
#         'information_description': None,
#         'information_source': None,
#         'count': None,
#         'amount': None,
#         'salary_quarters': []
#     },
#     'InterestAISForm': {
#         'title': None,
#         'information_code': None,
#         'information_description': None,
#         'information_source': None,
#         'count': None,
#         'amount': None,
#         'interest_transactions': []
#     }
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
#             table_data = {"title": found_title}
#             rows = text.strip().split("\n")
#             header_row = rows[0].split("\t")  # Assuming tab-separated columns

#             for row in rows[1:]:
#                 row_data = row.split("\t")
#                 row_dict = {field: value for field, value in zip(fields, row_data)}
#                 if "Salary" in found_title:
#                     table_data["information_code"] = row_dict.get("INFORMATION CODE")
#                     table_data["information_description"] = row_dict.get("INFORMATION DESCRIPTION")
#                     table_data["information_source"] = row_dict.get("INFORMATION SOURCE")
#                     table_data["count"] = row_dict.get("COUNT")
#                     table_data["amount"] = row_dict.get("AMOUNT")
#                     salary_quarter = row_dict.get("QUARTER")
#                     salary_dop_credit = row_dict.get("DATE OF PAYMENT/CREDIT")
#                     salary_amount_paid_credited = row_dict.get("AMOUNT PAID/CREDITED")
#                     salary_tds_deducted = row_dict.get("TDS DEDUCTED")
#                     salary_tds_deposited = row_dict.get("TDS DEPOSITED")
#                     salary_status = row_dict.get("STATUS")
#                     if salary_quarter and salary_dop_credit and salary_amount_paid_credited and \
#                             salary_tds_deducted and salary_tds_deposited and salary_status:
#                         salary_quarters = {
#                             "salary_quater": salary_quarter,
#                             "salary_dop_credit": salary_dop_credit,
#                             "salary_amount_paid_credited": salary_amount_paid_credited,
#                             "salary_tds_deducted": salary_tds_deducted,
#                             "salary_tds_deposited": salary_tds_deposited,
#                             "salary_status": salary_status,
#                         }
#                         table_data["salary_quarters"].append(salary_quarters)
#                 elif "Interest" in found_title:
#                     table_data["information_code"] = row_dict.get("INFORMATION CODE")
#                     table_data["information_description"] = row_dict.get("INFORMATION DESCRIPTION")
#                     table_data["information_source"] = row_dict.get("INFORMATION SOURCE")
#                     table_data["count"] = row_dict.get("COUNT")
#                     table_data["amount"] = row_dict.get("AMOUNT")
#                     reported_on = row_dict.get("REPORTED ON")
#                     account_number = row_dict.get("ACCOUNT NUMBER")
#                     account_type = row_dict.get("ACCOUNT TYPE")
#                     interest_amount = row_dict.get("INTEREST AMOUNT")
#                     status = row_dict.get("STATUS")
#                     if reported_on and account_number and account_type and interest_amount and status:
#                         interest_transaction = {
#                             "reported_on": reported_on,
#                             "account_number": account_number,
#                             "account_type": account_type,
#                             "interest_amount": interest_amount,
#                             "status": status
#                         }
#                         table_data["interest_transactions"].append(interest_transaction)

#             # Store the table data in the extracted_data dictionary
#             if found_title in extracted_data:
#                 extracted_data[found_title].append(table_data)
#             else:
#                 extracted_data[found_title] = [table_data]

# # Process the PDF using tabula for Salary table
# for title, table_list in extracted_data.items():
#     for table_data in table_list:
#         if "Salary" in table_data.get("title", ""):
#             # Assuming the table is on the first page (adjust as needed)
#             tabula_data = tabula.read_pdf(pdf_path, pages=1, stream=True, multiple_tables=True)
#             salary_df = tabula_data[0]  # Assuming the first table contains the Salary data
#             salary_df = salary_df.dropna()  # Remove rows with NaN values
#             salary_table = salary_df.to_dict(orient='records')

#             # Add the Salary data to the data_dict
#             data_dict['SalaryAISForm']['title'] = title
#             data_dict['SalaryAISForm']['table'] = salary_table

# # Print the extracted data
# for title, table_list in extracted_data.items():
#     print(f"Table with title: {title}")
#     for idx, data_dict in enumerate(table_list, start=1):
#         print(f"Table {idx}:")
#         print(data_dict)
#         print("\n")
