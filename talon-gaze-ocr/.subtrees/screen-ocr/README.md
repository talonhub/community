# Screen OCR

The `screen-ocr` package makes it easy to perform OCR on portions of the screen.

## Installation

Choose one of the following backends and follow the steps. WinRT is recommended for Windows and Tesseract for all other platforms.

### WinRT

WinRT is a Windows-only backend that is very fast and reasonably accurate. To install screen-ocr with WinRT support, run `pip install screen-ocr[winrt]`

### Tesseract

Tesseract is a cross-platform backend that is much slower and slightly less accurate than WinRT. To install screen-ocr with Tesseract support:

1. Install Tesseract binaries. For Windows, see
   https://github.com/UB-Mannheim/tesseract/wiki.
2. pip install screen-ocr[tesseract]

### EasyOCR

EasyOCR is a very accurate but slow backend and only runs on Python 64-bit, and hence is considered experimental. To install screen-ocr with WinRT support, run `pip install screen-ocr[easyocr]`

## Usage

You can do a simple test by running `python -m screen_ocr` to OCR the current screen contents. See [`__main__.py`](https://github.com/wolfmanstout/screen-ocr/blob/master/screen_ocr/__main__.py) for the code.

If using Tesseract with a custom installation directory on Windows, set
`tesseract_data_path` and `tesseract_command` paths appropriately when
constructing a `Reader` instance.

See also [gaze-ocr](https://github.com/wolfmanstout/gaze-ocr/blob/master/gaze_ocr/_gaze_ocr.py) for more a more involved usage example.
