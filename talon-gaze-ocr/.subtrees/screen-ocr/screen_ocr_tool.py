import argparse
import glob
import os
import random
import timeit

import imagehash
import pandas as pd
import test_utils
from IPython.display import display
from PIL import Image
from sklearn import model_selection

import screen_ocr

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["debug", "grid_search"])
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--all", action="store_true")
args = parser.parse_args()

# Set seed manually for reproducibility.
random.seed(517548236)

os.chdir(r"C:\Users\james\Documents\OCR")
text_files = set(glob.glob("logs/*.txt"))
average_hashes = set()
color_hashes = set()
success_data = []
failure_data = []
for image_file in glob.glob("logs/*.png"):
    # Skip near-duplicate images. Hash functions and parameters determined
    # experimentally.
    image = Image.open(image_file)
    average_hash = imagehash.average_hash(image, 10)
    if average_hash in average_hashes:
        continue
    average_hashes.add(average_hash)
    color_hash = imagehash.colorhash(image, 5)
    if color_hash in color_hashes:
        continue
    color_hashes.add(color_hash)

    text_file = image_file[:-3] + "txt"
    if text_file not in text_files:
        continue
    base_name = os.path.basename(text_file)
    if base_name.startswith("success"):
        success_data.append((image_file, text_file))
    elif base_name.startswith("failure"):
        failure_data.append((image_file, text_file))
    else:
        raise AssertionError(f"Unexpected file name: {base_name}")

random.shuffle(success_data)
random.shuffle(failure_data)
# Downsample the success data so that it's proportional to the failure data.
# Only reason to do this is to save on compute resources.
labeled_data = failure_data + success_data[: len(failure_data)]

X = []
y = []
for image_file, text_file in labeled_data:
    X.append(Image.open(image_file).convert("RGB"))
    with open(text_file) as f:
        y.append(f.read())


if args.verbose:

    def debug_image_callback(name, image):
        print(f"{name}:")
        display(image)

else:
    debug_image_callback = None
ocr_reader = screen_ocr.Reader.create_reader(
    "winrt", debug_image_callback=debug_image_callback
)


# Run OCR.
if args.mode == "debug":
    debug_filenames = [
        r"logs\failure_1581796330.95.png",
        r"logs\failure_1590973817.17.png",
        r"logs\failure_1590973805.00.png",
        r"logs\failure_1581796274.95.png",
        r"logs\failure_1590901824.09.png",
        r"logs\failure_1590975497.71.png",
        r"logs\failure_1586109111.24.png",
        r"logs\failure_1590974683.00.png",
        r"logs\failure_1586715290.52.png",
        r"logs\failure_1586715287.73.png",
        r"logs\failure_1590975577.31.png",
        r"logs\failure_1580019964.01.png",
        r"logs\failure_1585416092.33.png",
        r"logs\failure_1578856303.59.png",
    ]
    debug_indices = [
        i for i, data in enumerate(labeled_data) if data[0] in debug_filenames
    ]
    indices = range(len(X)) if args.all else debug_indices
    for index in indices:
        print(f"Processing: {labeled_data[index][0]}")
        image = X[index]
        gt_string = y[index]
        print("Unprocessed:")
        display(image)

        # Run OCR.
        print(f"Ground truth: {gt_string}")
        print("------------------")
        ocr_text = None
        ocr_time = timeit.timeit(
            "global ocr_text; ocr_text = ocr_reader.read_image(image).as_string()",
            globals=globals(),
            number=1,
        )
        ocr_cost = test_utils.cost(ocr_text, gt_string)
        print(f"time: {ocr_time:.2f}\tcost: {ocr_cost:.2f}\ntext: {ocr_text}")
elif args.mode == "grid_search":
    grid_search = model_selection.GridSearchCV(
        test_utils.OcrEstimator(),
        {
            "backend": ["winrt"],  # ["tesseract", "easyocr", "winrt"],
            # "threshold_type": ["local_otsu"], # , "local_otsu", "local"],  # , "niblack", "sauvola"],
            # "block_size": [41],
            # "correction_block_size": [31],
            # "margin": [0, 50],
            "resize_factor": [2, 3],
            "resize_method": [
                Image.NEAREST,
                Image.BOX,
                Image.BILINEAR,
                Image.HAMMING,
                Image.BICUBIC,
                Image.LANCZOS,
            ],
            # "convert_grayscale": [True],
            "shift_channels": [False, True],
            # "label_components": [False],
        },
        # Evaluate each example separately so that standard deviation is automatically computed.
        cv=model_selection.LeaveOneOut(),  # model_selection.PredefinedSplit([0] * len(y))
    )
    grid_search.fit(X, y)
    results = pd.DataFrame(grid_search.cv_results_)
    results.set_index("params", inplace=True)
    print(results["mean_test_score"].sort_values(ascending=False))
    print(grid_search.best_params_)
