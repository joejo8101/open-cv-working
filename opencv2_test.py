# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import pytesseract

# pdf_path = '/home/user/Documents/AIS_2.pdf'
# # Convert the PDF to an image
# images = convert_from_path(pdf_path)
# # Assuming there's only one page. If more, iterate over each image
# image = images[0]
# image_np = np.array(image)

# # Convert the image to grayscale and threshold it for contour detection
# gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
# _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# # Find contours
# contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Find the largest contour
# largest_contour = max(contours, key=cv2.contourArea)

# # Calculate the bounding rectangle of the largest contour
# x, y, w, h = cv2.boundingRect(largest_contour)

# # Expand the top of the bounding rectangle by 20%
# y_expanded = int(y - 1*h)

# # Extract text using pytesseract
# roi = image_np[y_expanded:y+h, x:x+w]
# text = pytesseract.image_to_string(roi)

# # Check if the text matches "Salary"
# if "Salary" in text:
#     # Further process the ROI to extract table values
#     # The actual extraction might need more processing, depending on the table's structure
#     print(text)

# # Optionally: Show the image with the largest contour highlighted (for debugging purposes)
# cv2.rectangle(image_np, (x, y_expanded), (x+w, y+h), (0, 255, 0), 2)
# cv2.imshow('Image', image_np)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import pytesseract

# pdf_path = '/home/user/Documents/AIS_2.pdf'

# # Convert the PDF to an image
# images = convert_from_path(pdf_path)

# # Iterate over each page image
# for image in images:
#     image_np = np.array(image)

#     # Convert the image to grayscale and threshold it for contour detection
#     gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

#     # Find contours
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Find the largest contour
#     largest_contour = max(contours, key=cv2.contourArea)

#     # Calculate the bounding rectangle of the largest contour
#     x, y, w, h = cv2.boundingRect(largest_contour)

#     # Expand the top of the bounding rectangle by 20%
#     y_expanded = int(y - 0.2*h)

#     # Extract text using pytesseract
#     roi = image_np[y_expanded:y+h, x:x+w]
#     text = pytesseract.image_to_string(roi)

#     # Check if the text matches "Salary"
#     if "Salary" in text:
#         print(text)

#     # Optionally: Show the image with the largest contour highlighted (for debugging purposes)
#     cv2.rectangle(image_np, (x, y_expanded), (x+w, y+h), (0, 255, 0), 2)
#     output_path = '/home/user/Documents/output_page_{}.png'.format(images.index(image)+1)  # Name it as you like, here I'm naming it based on the page number
#     cv2.imwrite(output_path, image_np)


import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract

pdf_path = '/home/user/Documents/AIS_2.pdf'

# Convert the PDF to an image
images = convert_from_path(pdf_path)

# Keywords to check for0
master_keywords = ["Salary", "Dividend", "Interest from deposit", "Cash payments", "Outward foreign remittance/purchase of foreign currency"]

for image in images:
    image_np = np.array(image)
    
    # Create a copy of master_keywords for the current page
    keywords = master_keywords.copy()

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

        for keyword in keywords:
            if keyword in text:
                print(text)
                # Optionally: Show the image with the contour highlighted (for debugging purposes)
                # cv2.rectangle(image_np, (x_expanded, y_expanded), (x_end, y_end), (0, 255, 0), 2)
                # output_path = '/home/user/Documents/test_folder_img/output_{}_page_{}.png'.format(keyword, images.index(image)+1)  # Name it as you like, here I'm naming it based on the keyword and page number
                # cv2.imwrite(output_path, image_np)
                
                # Remove the found keyword from the list for the current page
                keywords.remove(keyword)
                break

        # If all keywords are found on the current page, no need to process remaining contours
        if not keywords:
            break

