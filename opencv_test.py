# import cv2
# import pytesseract
# import os

# def pdf_to_image(pdf_path, output_folder):
#     os.system(f"pdftoppm -r 300 {pdf_path} {output_folder}/page -png")

# def ocr_image(image_path):
#     # Load the image with OpenCV
#     image = cv2.imread(image_path)
    
#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     img_bin1 = 255-image
#     # Binarization using Otsu's thresholding
#     _, binary = cv2.threshold(gray,128,255,cv2.THRESH_OTSU)
#     # Set pytesseract configurations for better OCR
#     config = '--psm 6'
#     text = pytesseract.image_to_string(binary, config=config)
    
#     return text

# def post_process(text):
#     # Here you can implement custom post-processing for your text
#     # This is a basic example, adjust as needed.
#     lines = text.split("\n")
#     processed_lines = [line.strip() for line in lines if line.strip() != ""]
#     return "\n".join(processed_lines)

# def main():
#     pdf_path = '/home/user/Documents/AIS_2.pdf'
#     output_folder = 'output_images'
    
#     if not os.path.exists(output_folder):
#         os.mkdir(output_folder)
    
#     # Convert PDF to images
#     pdf_to_image(pdf_path, output_folder)

#     # Iterate over each generated image and apply OCR
#     for image_name in sorted(os.listdir(output_folder)):
#         image_path = os.path.join(output_folder, image_name)
#         raw_text = ocr_image(image_path)
        
#         # Post-process the text
#         processed_text = post_process(raw_text)
        
#         print(processed_text)

# if __name__ == '__main__':
#     main()

# import cv2
# import pytesseract
# import os
# import re

# def pdf_to_image(pdf_path, output_folder):
#     os.system(f"pdftoppm -r 300 {pdf_path} {output_folder}/page -png")

# def ocr_image(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     img_bin1 = 255 - image
#     _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_OTSU)
#     config = '--psm 6'
#     text = pytesseract.image_to_string(binary, config=config)
#     return text
# def post_process(text):
#     lines = text.split("\n")
#     processed_lines = [line.strip() for line in lines if line.strip() != ""]
#     return "\n".join(processed_lines)

# def extract_values(text):
#     categories = ["Salary", "Dividend", "Interest from deposit", "Cash payments", "Outward foreign remittance/purchase of foreign currency"]
#     extracted_values = {category: None for category in categories}
    
#     for category in categories:
#         pattern = re.compile(rf"{category}:\s*(\S+)")
#         match = pattern.search(text)
#         if match:
#             extracted_values[category] = match.group(1)
    
#     return extracted_values

# def main():
#     pdf_path = '/home/user/Documents/AIS_2.pdf'
#     output_folder = 'output_images'
    
#     if not os.path.exists(output_folder):
#         os.mkdir(output_folder)
    
#     pdf_to_image(pdf_path, output_folder)

#     for image_name in sorted(os.listdir(output_folder)):
#         image_path = os.path.join(output_folder, image_name)
#         raw_text = ocr_image(image_path)
#         processed_text = post_process(raw_text)
        
#         # Extract values from processed text
#         extracted_values = extract_values(processed_text)
        
#         # Print the extracted values
#         for category, value in extracted_values.items():
#             print(f"{category}: {value}")
            
# if __name__ == '__main__':
#     main()

import tabula

def extract_tables(pdf_path):
    # Extract tables from the PDF
    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True, lattice=True)
    return tables

def main():
    pdf_path = '/home/user/Documents/AIS_2.pdf'
    
    # Extract tables from the PDF
    tables = extract_tables(pdf_path)
    
    # Iterate through the extracted tables and print their content
    for table_num, table in enumerate(tables, start=1):
        print(f"Table {table_num}:\n{table}\n")

if __name__ == '__main__':
    main()
# import cv2
# import pytesseract
# import os
# import re
# import numpy as np
# def pdf_to_image(pdf_path, output_folder):
#     os.system(f"pdftoppm -r 500 {pdf_path} {output_folder}/page -png")

# # def ocr_image(image_path):
# #     image = cv2.imread(image_path)
# #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# #     img_bin1 = 255 - image
# #     _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_OTSU)
# #     config = '--psm 6'
# #     text = pytesseract.image_to_string(binary, config=config)
# #     return text

# def ocr_image(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # 1. Resize the image
#     scale_factor = 1.0
#     height, width = gray.shape
#     gray_resized = cv2.resize(gray, (int(width*scale_factor), int(height*scale_factor)))

#     # 2. Denoise
#     denoised = cv2.fastNlMeansDenoising(gray_resized, None, 30, 7, 21)

#     # 3. Adaptive thresholding
#     binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#                                    cv2.THRESH_BINARY, 11, 2)

#     # 4. Morphological transformations - Dilation
#     kernel = np.ones((2, 2), np.uint8)
#     dilate = cv2.dilate(binary, kernel, iterations=1)

#     config = '--psm 6'
#     text = pytesseract.image_to_string(dilate, config=config)
    
#     return text

# def post_process(text):
#     lines = text.split("\n")
#     processed_lines = [line.strip() for line in lines if line.strip() != ""]
#     return "\n".join(processed_lines)

# def extract_table_content(text, subkeyword):
#     match = re.search(subkeyword, text, re.IGNORECASE)
#     if match:
#         subkeyword_start = match.start()
#         subkeyword_end = match.end()

#         table_pattern = re.compile(r'((?:\s*.*\s*){2,})', re.MULTILINE)
#         table_match = table_pattern.search(text[subkeyword_end:])

#         if table_match:
#             table_content = table_match.group(1).strip()
#             return table_content

#     return None

# def main():
#     pdf_path = '/home/user/Documents/AIS_2.pdf'
#     output_folder = 'output_images'
#     subkeywords = ["Salary", "Dividend", "Interest from deposit", "Cash payments", "Outward foreign remittance/purchase of foreign currency"]

#     if not os.path.exists(output_folder):
#         os.mkdir(output_folder)

#     pdf_to_image(pdf_path, output_folder)

#     for image_name in sorted(os.listdir(output_folder)):
#         image_path = os.path.join(output_folder, image_name)
#         raw_text = ocr_image(image_path)
#         processed_text = post_process(raw_text)

#         for subkeyword in subkeywords:
#             table_content = extract_table_content(processed_text, subkeyword)
#             if table_content:
#                 print(f"Table content for '{subkeyword}':\n{table_content}\n")

# if __name__ == '__main__':
#     main()
