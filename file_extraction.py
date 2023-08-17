import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract

pdf_path = '/home/user/Documents/AIS_1.pdf'

# Convert the PDF to images
images = convert_from_path(pdf_path)

# Keywords and title mappings
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
    'SalaryAISForm': [],
    'InterestAISForm': [],
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
        # ... (Your existing code to process the table rows)
        print("Check check",text)
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

# Organize the extracted data into the desired structure
for title, table_list in extracted_data.items():
    if title in title_keywords:
        for data_dict_entry in table_list:
            for row_key, row_values in data_dict_entry.items():
                if row_key == "":
                    continue
                if row_key in master_keywords:
                    section = row_key.replace(" ", "")
                    section += "AISForm"  # Form the appropriate section name
                    data_dict[section].append(row_values)
                else:
                    for entry in row_values:
                        section = title.replace(" ", "")
                        section += "AISForm"  # Form the appropriate section name
                        entry["Title"] = row_key
                        data_dict[section].append(entry)

# Print the organized data
for section, entries in data_dict.items():
    print(f"Section: {section}")
    for entry in entries:
        print(entry)
        print("\n")
    print("Section: SalaryAISForm")
    for entry in data_dict["SalaryAISForm"]:
        print(entry)
        print("\n")
