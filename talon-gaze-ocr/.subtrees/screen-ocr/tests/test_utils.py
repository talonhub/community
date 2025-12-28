from rapidfuzz import fuzz
from skimage import filters, morphology
from sklearn.base import BaseEstimator

import screen_ocr


def cost(result, gt):
    return -fuzz.partial_ratio(result.lower(), gt.lower())


class OcrEstimator(BaseEstimator):
    def __init__(
        self,
        backend="tesseract",
        threshold_type=None,
        block_size=None,
        correction_block_size=None,
        margin=None,
        resize_factor=None,
        resize_method=None,
        convert_grayscale=None,
        shift_channels=None,
        label_components=None,
    ):
        self.backend = backend
        self.threshold_type = threshold_type
        self.block_size = block_size
        self.correction_block_size = correction_block_size
        self.margin = margin
        self.resize_factor = resize_factor
        self.resize_method = resize_method
        self.convert_grayscale = convert_grayscale
        self.shift_channels = shift_channels
        self.label_components = label_components

    def fit(self, X=None, y=None):
        if self.threshold_type == "otsu":

            def threshold_function(data):
                return filters.threshold_otsu(data)
        elif self.threshold_type == "local_otsu":

            def threshold_function(data):
                assert self.block_size is not None
                return filters.rank.otsu(data, morphology.square(self.block_size))
        elif self.threshold_type == "local":

            def threshold_function(data):
                assert self.block_size is not None
                return filters.threshold_local(data, self.block_size)
        elif self.threshold_type == "niblack":

            def threshold_function(data):
                assert self.block_size is not None
                return filters.threshold_niblack(data, self.block_size)
        elif self.threshold_type == "sauvola":

            def threshold_function(data):
                assert self.block_size is not None
                return filters.threshold_sauvola(data, self.block_size)
        elif self.threshold_type is None:
            threshold_function = None  # type: ignore[assignment]
        else:
            raise ValueError(f"Unknown threshold type: {self.threshold_type}")
        self.ocr_reader_ = screen_ocr.Reader.create_reader(
            backend=self.backend,
            threshold_function=threshold_function,
            correction_block_size=self.correction_block_size,
            margin=self.margin,
            resize_factor=self.resize_factor,
            resize_method=self.resize_method,
            convert_grayscale=self.convert_grayscale,
            shift_channels=self.shift_channels,
            label_components=self.label_components,
            debug_image_callback=None,
        )

    def score(self, X, y):
        error = 0
        for image, gt_text in zip(X, y, strict=True):
            result = self.ocr_reader_.read_image(image).as_string()
            error += cost(result, gt_text)
        return -error
