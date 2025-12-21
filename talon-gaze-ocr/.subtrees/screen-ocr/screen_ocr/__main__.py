# Simple script to perform OCR on the current screen contents.

import screen_ocr

ocr_reader = screen_ocr.Reader.create_quality_reader()
# To read a cropped region, add bounding_box=(left, top, right, bottom).
results = ocr_reader.read_screen()
print(results.as_string())
