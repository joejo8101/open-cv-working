# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import pytesseract
# import re
# import tabula

# def extract_table(pdf_path, page_num):
#     tables = tabula.read_pdf(pdf_path, pages=page_num, multiple_tables=True, lattice=True)
#     return tables

# def main():
#     pdf_path = '/home/user/Documents/AIS_2.pdf'
#     images = convert_from_path(pdf_path)

#     target_keyword = "Salary"
#     table_found = False

#     for page_num, image in enumerate(images, start=1):
#         image_np = np.array(image)
#         gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
#         _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
#         contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

#         for contour in sorted_contours:
#             x, y, w, h = cv2.boundingRect(contour)
#             height, width, _ = image_np.shape
#             y_expanded = max(0, y - int(0.2 * h))
#             x_expanded = max(0, x)
#             y_end = min(height, y + h)
#             x_end = min(width, x + w)

#             roi = image_np[y_expanded:y_end, x_expanded:x_end]
#             text = pytesseract.image_to_string(roi)

#             if target_keyword in text:
#                 print(f"Found keyword '{target_keyword}' on page {page_num}")
#                 table_found = True
#             elif table_found:
#                 print(f"Extracting table on page {page_num}")
#                 tables = extract_table(pdf_path, page_num)
#                 if tables:
#                     print(f"Table for '{target_keyword}':\n{tables[0]}\n")
#                 table_found = False
#                 break

# if __name__ == '__main__':
#     main()

