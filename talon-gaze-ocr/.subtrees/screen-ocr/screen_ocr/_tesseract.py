import numpy as np
import pytesseract
import six
from PIL import Image
from skimage import filters, morphology, transform

from . import _base


class TesseractBackend(_base.OcrBackend):
    def __init__(
        self,
        tesseract_data_path=None,
        tesseract_command=None,
        threshold_function=None,
        threshold_block_size=None,
        correction_block_size=None,
        convert_grayscale=False,
        shift_channels=False,
        debug_image_callback=None,
    ):
        self.tesseract_data_path = (
            tesseract_data_path or r"C:\Program Files\Tesseract-OCR\tessdata"
        )
        self.tesseract_command = (
            tesseract_command or r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )
        if threshold_function == "otsu":
            self.threshold_function = lambda data: filters.threshold_otsu(data)
        elif threshold_function == "local_otsu":
            self.threshold_function = lambda data: filters.rank.otsu(
                data, morphology.square(threshold_block_size)
            )
        else:
            self.threshold_function = threshold_function
        self.correction_block_size = correction_block_size
        self.convert_grayscale = convert_grayscale
        self.shift_channels = shift_channels
        self.debug_image_callback = debug_image_callback

    def run_ocr(self, image):
        image = self._preprocess(image)
        tessdata_dir_config = rf'--tessdata-dir "{self.tesseract_data_path}"'
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_command
        results = pytesseract.image_to_data(
            image, config=tessdata_dir_config, output_type=pytesseract.Output.DATAFRAME
        )
        lines = []
        words = []
        for _, box in results.iterrows():
            # Word
            if box.level == 5:
                text = box.text
                text = (
                    six.text_type(text, encoding="utf-8")
                    if isinstance(text, six.binary_type)
                    else six.text_type(text)
                )
                words.append(
                    _base.OcrWord(text, box.left, box.top, box.width, box.height)
                )
            # End of line
            if box.level == 4:
                if words:
                    lines.append(_base.OcrLine(words))
                words = []
        if words:
            lines.append(_base.OcrLine(words))
        lines.sort(key=lambda line: (line.words[0].top, line.words[0].left))
        return _base.OcrResult(lines)

    def _preprocess(self, image):
        data = np.array(image)
        if self.shift_channels:
            channels = [self._shift_channel(data[:, :, i], i) for i in range(3)]
            data = np.stack(channels, axis=-1)

        if self.threshold_function:
            if self.convert_grayscale:
                image = Image.fromarray(data)
                image = image.convert("L")
                data = np.array(image)
                data = self._binarize_channel(data, None)
            else:
                channels = [self._binarize_channel(data[:, :, i], i) for i in range(3)]
                data = np.stack(channels, axis=-1)
                data = np.all(data, axis=-1)

        image = Image.fromarray(data)
        # Ensure consistent performance measurements.
        image.load()
        if self.debug_image_callback:
            self.debug_image_callback("debug_final", image)
        return image

    def _binarize_channel(self, data, channel_index):
        if self.debug_image_callback:
            self.debug_image_callback(
                f"debug_before_{channel_index}", Image.fromarray(data)
            )
        # Necessary to avoid ValueError from Otsu threshold.
        if data.min() == data.max():
            threshold = np.uint8(0)
        else:
            threshold = self.threshold_function(data)
        if self.debug_image_callback:
            if threshold.ndim == 2:
                self.debug_image_callback(
                    f"debug_threshold_{channel_index}",
                    Image.fromarray(threshold.astype(np.uint8)),
                )
            else:
                self.debug_image_callback(
                    f"debug_threshold_{channel_index}",
                    Image.fromarray(np.ones_like(data) * threshold),
                )
        data = data > threshold
        white_sums = self._window_sums(data, self.correction_block_size)
        black_sums = self._window_sums(~data, self.correction_block_size)
        background_colors = white_sums > black_sums
        if self.debug_image_callback:
            self.debug_image_callback(
                f"debug_background_{channel_index}",
                Image.fromarray(background_colors == True),  # noqa: E712
            )
        # Make the background consistently white (True).
        data = data == background_colors
        if self.debug_image_callback:
            self.debug_image_callback(
                f"debug_after_{channel_index}", Image.fromarray(data)
            )
        return data

    @staticmethod
    def _window_sums(image, window_size):
        integral = transform.integral_image(image)
        radius = int((window_size - 1) / 2)
        top_left = np.zeros(image.shape, dtype=np.uint16)
        top_left[radius:, radius:] = integral[:-radius, :-radius]
        top_right = np.zeros(image.shape, dtype=np.uint16)
        top_right[radius:, :-radius] = integral[:-radius, radius:]
        top_right[radius:, -radius:] = integral[:-radius, -1:]
        bottom_left = np.zeros(image.shape, dtype=np.uint16)
        bottom_left[:-radius, radius:] = integral[radius:, :-radius]
        bottom_left[-radius:, radius:] = integral[-1:, :-radius]
        bottom_right = np.zeros(image.shape, dtype=np.uint16)
        bottom_right[:-radius, :-radius] = integral[radius:, radius:]
        bottom_right[-radius:, :-radius] = integral[-1:, radius:]
        bottom_right[:-radius, -radius:] = integral[radius:, -1:]
        bottom_right[-radius:, -radius:] = integral[-1, -1]
        return bottom_right - bottom_left - top_right + top_left

    @staticmethod
    def _shift_channel(data, channel_index):
        """Shifts each channel based on actual position in a typical LCD. This reduces
        artifacts from subpixel rendering. Note that this assumes RGB left-to-right
        ordering and a subpixel size of 1 in the resized image.
        """
        channel_shift = channel_index - 1
        if channel_shift != 0:
            data = np.roll(data, channel_shift, axis=1)
            if channel_shift == -1:
                data[:, -1] = data[:, -2]
            elif channel_shift == 1:
                data[:, 0] = data[:, 1]
        return data
