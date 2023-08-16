import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract

def extract_quarters(text):
    quarters = []
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Iterate through the lines to extract quarter details
    for line in lines:
        if line.strip().startswith("Q"):
            quarter_data = line.split('|')
            
            # Extract relevant data based on your text format
            if len(quarter_data) >= 5:
                quarter = quarter_data[0].strip()
                dop_credit = quarter_data[1].strip()
                amount_paid_credited = quarter_data[2].strip()
                tds_deducted = quarter_data[3].strip()
                tds_deposited = quarter_data[4].strip()
                
                quarters.append({
                    'quarter': quarter,
                    'dop_credit': dop_credit,
                    'amount_paid_credited': amount_paid_credited,
                    'tds_deducted': tds_deducted,
                    'tds_deposited': tds_deposited,
                    'status': None  # You may need to extract the status from the text as well
                })
    
    return quarters


pdf_path = '/home/user/Documents/AIS_1.pdf'

# Convert the PDF to an image
images = convert_from_path(pdf_path)

# Create dictionaries for different categories
categories = {
    "Part B1-Information relating to tax deducted or collected at source": ["Salary", "Interest from deposit"],
    "Part B2-Information relating to specified financial transaction (SFT)": ["Interest from savings bank", 
                                                                            "Sale of securities and units of mutual fund", 
                                                                            "Purchase of time deposits", 
                                                                            "Purchase of securities and units of mutual funds"]
}

category_data = {category: [] for category in categories.keys()}


for image in images:
    image_np = np.array(image)
    
    # Convert the image to grayscale and threshold it for contour detection
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by area in decreasing order
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in sorted_contours:
        x, y, w, h = cv2.boundingRect(contour)
        height, width, _ = image_np.shape
        y_expanded = max(0, y - int(0.2*h)) 
        x_expanded = max(0, x) 
        y_end = min(height, y+h)
        x_end = min(width, x+w)

        roi = image_np[y_expanded:y_end, x_expanded:x_end]
        text = pytesseract.image_to_string(roi)

        # Print the extracted text
        print("Extracted Text:")
        print(text)

        found_title = None
        for title, keywords in categories.items():
            if title in text:
                found_title = title
                break

        if found_title:
            for keyword in keywords:
                if keyword in text:
                    category_data[found_title].append({
                        'information_code': None,
                        'information_description': None,
                        'information_source': None,
                        'count': None,
                        'amount': None,
                        'quarters': []
                    })

                    # Populate the dictionary with specific information for each quarter
                    quarters = extract_quarters(text)  # Implement this function to extract quarter details
                    category_data[found_title][-1]['quarters'] = quarters

                    break

# Print the final category data
for category, data in category_data.items():
    print(f"{category}: {data}")