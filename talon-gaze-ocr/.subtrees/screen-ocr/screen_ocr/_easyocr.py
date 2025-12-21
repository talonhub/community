import easyocr
import numpy as np

from . import _base


class EasyOcrBackend(_base.OcrBackend):
    def __init__(self):
        self._easyocr = easyocr.Reader(["en"])

    def run_ocr(self, image):
        result = self._easyocr.readtext(np.array(image))
        lines = [
            _base.OcrLine(
                [
                    _base.OcrWord(
                        text,
                        box[0][0],
                        box[0][1],
                        box[2][0] - box[0][0],
                        box[2][1] - box[0][1],
                    )
                ]
            )
            for box, text, confidence in result
        ]
        return _base.OcrResult(lines)
