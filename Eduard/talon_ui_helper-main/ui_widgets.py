"""
Simple widget system for use with Talon's canvas.
"""

from typing import Tuple, Dict, Any
from talon.skia.paint import Paint

def render_text(canvas, formatted_text, x, y):
    """
    Renders formatted_text from layout_text() to canvas at the given coordinates. The
    paint style is contained within the formatted_text data structure.
    """

    for i, line in enumerate(formatted_text["output_lines"]):
        calc_y = y + i * formatted_text["line_height"]
        canvas.draw_text(line, x, calc_y, formatted_text["paint"])

def layout_text(
        text: str,
        paint: Paint,
        max_width: int) -> Tuple[Tuple[float, float], Dict[str, Any]]:
    """
    Works out the layout of the given plain text (maybe with newlines)
    rendered with the style described by paint constrained to fit within the given width.

    Returns the width/height bounding box that is used by the text.
    This will be the same or a smaller width than max_width. Also returns a data
    structure that can be used by render_text() to draw the text at an arbitrary position
    on a canvas.
    """

    paint = paint.clone()
    line_height = int(paint.textsize * 1.2)
    space_width = paint.measure_text(" ")[0]

    # Break newlines out into their own chunks
    # IDEA: The output of this function could be made into a monoid of a width/height tuple
    # and a class that knows how to render itself at a position. Then we could handle multi
    # element layouts (e.g. headers, indented areas) easily, and also the newlines code here.
    chunks = []
    for chunk in text.split(" "):
        if "\n" in chunk:
            for bit in chunk.split("\n"):
                if bit == "":
                    additions = ["\n"]
                else:
                    additions = [bit, "\n"]
                chunks += additions
            # Remove trailing newline
            chunks = chunks[:-1]

        else:
            chunks.append(chunk)

    max_output_width = 0
    current_width = 0
    output_lines = []
    current_line = []
    for chunk in chunks:
        if chunk == "\n":
            output_lines.append(" ".join(current_line))
            current_line = []
            current_width = 0
            continue

        chunk_width = paint.measure_text(chunk)[0]
        new_width = current_width + space_width + chunk_width

        if new_width > max_width:
            output_lines.append(" ".join(current_line))
            current_line = [chunk]
            current_width = chunk_width
        else:
            current_line.append(chunk)
            current_width = new_width
            max_output_width = max(new_width, max_output_width)

    if len(current_line) > 0:
        output_lines.append(" ".join(current_line))

    return (
        (max_output_width, line_height * len(output_lines)),
        {
            "line_height": line_height,
            "paint": paint,
            "output_lines": output_lines
        }
    )
