# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import pytesseract

# pdf_path = '/home/user/Documents/AIS_1.pdf'

# # Convert the PDF to an image
# images = convert_from_path(pdf_path)

# # Keywords to check for0
# master_keywords = ["Salary", "Dividend", "Interest from deposit", "Cash payments", "Outward foreign remittance/purchase of foreign currency"]

# for image in images:
#     image_np = np.array(image)
    
#     # Create a copy of master_keywords for the current page
#     keywords = master_keywords.copy()

#     # Convert the image to grayscale and threshold it for contour detection
#     gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

#     # Find contours
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     # Sort contours by area in decreasing order
#     sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

#     for contour in sorted_contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         height, width, _ = image_np.shape
#         y_expanded = max(0, y - int(0.2*h)) 
#         x_expanded = max(0, x) 
#         y_end = min(height, y+h)
#         x_end = min(width, x+w)

#         roi = image_np[y_expanded:y_end, x_expanded:x_end]
#         text = pytesseract.image_to_string(roi)

#         for keyword in keywords:
#             if keyword in text:
#                 print(text)
                
#                 # Remove the found keyword from the list for the current page
#                 keywords.remove(keyword)
#                 break

#         # If all keywords are found on the current page, no need to process remaining contours
#         if not keywords:
#             break


# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import pytesseract

# pdf_path = '/home/user/Documents/AIS_1.pdf'

# # Convert the PDF to an image
# images = convert_from_path(pdf_path)

# # Keywords to check for
# master_keywords = [
#     "Salary", "Dividend", "Interest from deposit", "Cash payments", 
#     "Outward foreign remittance/purchase of foreign currency",
#     "Interest from savings bank", "Sale of securities and units of mutual fund",
#     "Purchase of time deposits", "Purchase of securities and units of mutual funds"
# ]

# # Title keywords
# title_keywords = {
#     "Part B1-Information relating to tax deducted or collected at source": ["Salary", "Interest from deposit"],
#     "Part B2-Information relating to specified financial transaction (SFT)": ["Interest from savings bank", 
#                                                                             "Sale of securities and units of mutual fund", 
#                                                                             "Purchase of time deposits", 
#                                                                             "Purchase of securities and units of mutual funds"]
# }

# for image in images:
#     image_np = np.array(image)
    
#     # Convert the image to grayscale and threshold it for contour detection
#     gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

#     # Find contours
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     # Sort contours by area in decreasing order
#     sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

#     for contour in sorted_contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         height, width, _ = image_np.shape
#         y_expanded = max(0, y - int(0.2*h)) 
#         x_expanded = max(0, x) 
#         y_end = min(height, y+h)
#         x_end = min(width, x+w)

#         roi = image_np[y_expanded:y_end, x_expanded:x_end]
#         text = pytesseract.image_to_string(roi)

#         found_title = None
#         for title, keywords in title_keywords.items():
#             if title in text:
#                 found_title = title
#                 break

#         if found_title:
#             for keyword in keywords:
#                 if keyword in text:
#                     print(f"Table with title: {found_title}")
#                     print(text)
#                     break
#         else:
#             for keyword in master_keywords:
#                 if keyword in text:
#                     print(text)
#                     break

import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract

pdf_path = '/home/user/Documents/AIS_1.pdf'

# Convert the PDF to an image
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
            data_dict = {"Title": found_title}
            rows = text.strip().split("\n")
            header_row = rows[0].split("\t")  # Assuming tab-separated columns

            for row in rows[1:]:
                row_data = row.split("\t")
                row_dict = {}
                for field_name, field_value in zip(header_row, row_data):
                    row_dict[field_name] = field_value
                data_dict[row_data[0]] = row_dict

            extracted_data[found_title] = data_dict

# Print the extracted data
for title, data_dict in extracted_data.items():
    print(f"Table with title: {title}")
    print(data_dict)
    print("\n")


# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import pytesseract

# pdf_path = '/home/user/Documents/AIS_1.pdf'

# # Convert the PDF to an image
# images = convert_from_path(pdf_path)

# # Title keywords and their associated table names
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
#         for title, table_names in title_keywords.items():
#             if title in text:
#                 found_title = title
#                 tables = table_names
#                 break

#         if found_title:
#             data_dict = {"Main Title": found_title}

#             for table_name in tables:
#                 table_data = {"Table Name": table_name}

#                 if table_name in ["Salary", "Interest from deposit",
#                                   "Interest from savings bank",
#                                   "Sale of securities and units of mutual fund",
#                                   "Purchase of securities and units of mutual funds"]:
#                     rows = text.strip().split("\n")
#                     header_row = rows[0].split("\t")
#                     data_rows = [row.split("\t") for row in rows[1:]]

#                     table_entries = []
#                     for row_data in data_rows:
#                         entry = {}
#                         for field_name, field_value in zip(header_row, row_data):
#                             entry[field_name] = field_value
#                         table_entries.append(entry)

#                     table_data["Entries"] = table_entries

#                 data_dict[table_name] = table_data

#             extracted_data[found_title] = data_dict

# # Print the extracted data
# for title, data_dict in extracted_data.items():
#     print(f"Main Title: {title}")
#     for table_name, table_data in data_dict.items():
#         if table_name != "Main Title":
#             print(f"Table Name: {table_name}")
#             print(table_data)
#             print("\n")
