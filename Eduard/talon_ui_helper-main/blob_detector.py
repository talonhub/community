"""
Clickable blob detection logic
"""

from typing import List
import numpy as np

from talon.types import Rect as TalonRect


def calculate_blob_rects(image: 'talon.skia.Image', region: TalonRect, min_gap_size=5) -> List[TalonRect]:
    """
    Finds screen relative rectangles corresponding to clickable blobs in the given image. Region
    is the position on the screen the image corresponds to.
    """

    def _offset_rect(rect, dx, dy):
        return TalonRect(
            rect.x + dx,
            rect.y + dy,
            rect.width,
            rect.height
        )

    image_array = np.array(image)
    rects = calculate_blob_rects_from_numpy(image_array, min_gap_size=min_gap_size)

    return [
        TalonRect(
            rect.x + region.x,
            rect.y + region.y,
            rect.width,
            rect.height
        )

        for rect in rects
    ]


def calculate_blob_rects_from_numpy(image_array: np.ndarray, min_gap_size=5) -> List[TalonRect]:
    """
    Finds likely blobs suitable for clicking in the given numpy array.
    """

    # First column or row of pixels are all considered background colors (depending on dimensions
    # of rectangle)
    if image_array.shape[0] > image_array.shape[1]:
        # Higher than wide, assume we're finding vertically stacked items
        background_colors = np.unique(image_array[:, 0, :], axis=0)
        rollup_axis = 1
        def _vert_rect_builder(blob):
            return TalonRect(
                0,
                blob[0],
                image_array.shape[1],
                blob[1] - blob[0]
            )
        rect_builder = _vert_rect_builder
    else:
        # Wider than high, assume we're finding horizontally stacked items
        background_colors = np.unique(image_array[0, :, :], axis=0)
        rollup_axis = 0
        def _horiz_rect_builder(blob):
            return TalonRect(
                blob[0],
                0,
                blob[1] - blob[0],
                image_array.shape[0]
            )
        rect_builder = _horiz_rect_builder

    height, width, _ = image_array.shape
    # Build a boolean grid where True is foreground and False is background
    mask_array = np.ones((height, width), np.uint8) == 1
    for color_array in background_colors:
        mask_array = mask_array & (image_array != color_array).any(axis=2)

    # Find which elements (rows or columns depending on orientation)
    # have any foreground pixels in them (make a 1d array)
    elements_with_foreground = np.any(mask_array, axis=rollup_axis)

    # Form the 1d array into spans
    spans = []
    start_span_i = 0
    end_span_i = 0
    state = "bg"
    bg_counter = 0
    for i, item in enumerate(elements_with_foreground):
        if item and state == "bg":
            start_span_i = i
            state = "fg"
        elif not item and state == "fg":
            state = "fg_countdown"
            bg_counter = 0
        elif item and state == "fg_countdown":
            # Gap was smaller than our min_gap_size and we just got a foreground,
            # resume including in the span
            state = "fg"
        elif not item and state == "fg_countdown":
            bg_counter += 1
            if bg_counter >= min_gap_size:
                state = "bg"
                end_span_i = i - bg_counter
                spans.append((start_span_i, end_span_i))
        else:
            # Maintaining same state, pass
            pass
    if state == "fg":
        end_span_i = len(elements_with_foreground)
        spans.append((start_span_i, end_span_i))
    elif state == "fg_countdown":
        end_span_i = i - bg_counter
        spans.append((start_span_i, end_span_i))

    return [
        rect_builder(span)

        for span in spans
    ]
