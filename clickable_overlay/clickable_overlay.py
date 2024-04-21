import copy
import threading
from enum import Enum
from typing import List, Dict, Tuple, Optional, Callable

from talon import Module, Context, canvas, actions, ui, app, skia
from talon.ui import Rect


VALID_KEYS = "fjdkghtyruievnmcbwopaqzslx"
RELATIVE_FONT_SIZE = 10
MIN_FONT_SIZE = 14
RELATIVE_BOX_STROKE_WIDTH = 1


# TODO: What's the right way of doing this?
class ActionTypes(Enum):
    LEFT_CLICK = 0
    RIGHT_CLICK = 1
    MIDDLE_CLICK = 2
    DOUBLE_LEFT_CLICK = 3
    FOCUS = 4
    HOVER_OVER = 5


# Maps keyboard keys to action types in the overlay
ACTION_KEYS = {
    "'": ActionTypes.LEFT_CLICK,
    ",": ActionTypes.RIGHT_CLICK,
    ";": ActionTypes.DOUBLE_LEFT_CLICK,
    ".": ActionTypes.MIDDLE_CLICK,
    "/": ActionTypes.FOCUS,
    "#": ActionTypes.HOVER_OVER,
}

# Which color should each action type be displayed with?
ACTION_COLORS = {
    ActionTypes.LEFT_CLICK: ("800", "FFF"),
    ActionTypes.RIGHT_CLICK: ("008", "FFF"),
    ActionTypes.MIDDLE_CLICK: ("AAA", "000"),
    ActionTypes.DOUBLE_LEFT_CLICK: ("603", "FFF"),
    ActionTypes.FOCUS: ("084", "FFF"),
    ActionTypes.HOVER_OVER: ("808", "FFF"),
}

candidates_lock = threading.RLock()
active_candidates = []
overlay_closed_callback = None


def draw(c):
    paint = c.paint

    if app.platform == "windows":
        default_font = "Consolas"
    else:
        default_font = "monospace"

    auto_scaling_factor = max(c.width, c.height) / 1920

    # Blend like this so we can have a translucent blackout background, but
    # still have transparent sections for each button.
    paint.blendmode = paint.Blend.SRC
    # ['Blend', 'ClipOp', 'FilterQuality', 'Style', 'TextAlign', 'antialias', 'autohinted', 'blendmode', 'break_text', 'clone', 'color',
    #  'colorfilter', 'dev_kern_text', 'dither', 'embedded_bitmap_text', 'fake_bold_text', 'filter_quality', 'font', 'handle', 'hinting',
    #  'imagefilter', 'lcd_render_text', 'linear_text', 'maskfilter', 'measure_text', 'path_effect', 'shader', 'stroke_cap',
    #  'stroke_join', 'stroke_miter', 'stroke_width', 'style', 'subpixel_text', 'text_align', 'text_scale_x', 'text_skew_x', 'textsize',
    #  'typeface', 'verticaltext']
    # ['CLEAR', 'COLOR', 'COLORBURN', 'COLORDODGE', 'DARKEN', 'DIFFERENCE', 'DST', 'DSTATOP', 'DSTIN', 'DSTOUT', 'DSTOVER', 'EXCLUSION',
    #  'HARDLIGHT', 'HUE', 'LIGHTEN', 'LUMINOSITY', 'MODULATE', 'MULTIPLY', 'OVERLAY', 'PLUS', 'SATURATION', 'SCREEN', 'SOFTLIGHT',
    #  'SRC', 'SRCATOP', 'SRCIN', 'SRCOUT', 'SRCOVER', 'XOR']

    derived_textsize = auto_scaling_factor * RELATIVE_FONT_SIZE
    paint.textsize = int(max(round(derived_textsize), MIN_FONT_SIZE))
    paint.typeface = default_font
    paint.embolden = True
    paint.style = paint.Style.FILL
    text_height = paint.measure_text("pgTlHjhgy")[1].height
    tail_height = paint.measure_text("p")[1].height - paint.measure_text("o")[1].height

    corner_radius = int(max(round(auto_scaling_factor * 3), 4))
    box_stroke_width = max(round(auto_scaling_factor) * RELATIVE_BOX_STROKE_WIDTH, 1)
    bounding_box_offset = int(round(box_stroke_width / 2))
    bounding_box_reduction = int(round(box_stroke_width))
    box_stroke_width = int(box_stroke_width)

    text_offset = max(round(auto_scaling_factor * derived_textsize / 14), 1)
    text_box_expansion = int(round(text_offset * 2))
    text_offset = int(round(text_offset))

    paint.color = "00000088"
    c.draw_rect(c.rect)

    with candidates_lock:
        # TODO: Try batching draw calls with similar paint properties.
        for candidate in active_candidates:
            box_color, text_color = ACTION_COLORS[candidate.action_type]

            bounds = Rect(*candidate.clickable.bounds)
            bounds.x += bounding_box_offset
            bounds.y += bounding_box_offset
            bounds.width -= bounding_box_reduction
            bounds.height -= bounding_box_reduction
            rrect = skia.RoundRect.from_rect(bounds, x=corner_radius, y=corner_radius)
            text = "".join(candidate.label)
            _, text_dims = paint.measure_text(text)

            label_rect = Rect(bounds.x, bounds.y, text_dims.width, text_height)
            label_rect.width += text_box_expansion
            label_rect.height += text_box_expansion

            # TODO: Border, like a drop shadow.
            # paint.stroke_width = int(
            #     round(max(box_stroke_width * 2, box_stroke_width + 2))
            # )
            # c.draw_rrect(rrect)
            # c.draw_rect(label_rect)

            # Override the underlying transparency - make the areas where
            # buttons are highlighted transparent
            paint.style = paint.Style.FILL
            paint.color = "00000000"
            c.draw_rrect(rrect)

            paint.style = paint.Style.STROKE
            paint.color = box_color
            paint.stroke_width = box_stroke_width
            c.draw_rrect(rrect)

            paint.style = paint.Style.STROKE_AND_FILL
            c.draw_rrect(
                rrect=skia.RoundRect.from_rect(
                    label_rect, x=corner_radius, y=corner_radius
                )
            )
            # c.draw_rect(label_rect)

            paint.color = text_color
            paint.style = paint.Style.FILL
            # FIXME: Remove the .85 fudge factor. Derive it precisely.
            c.draw_text(
                text,
                bounds.x + text_offset - text_dims.x,
                bounds.y + text_offset + text_height - tail_height,
            )


def on_key(event):
    if not event.up:
        actions.self.clickable_handle_key(event.key)
        # raise NotImplementedError()


def on_focus(focus_in: bool):
    if not focus_in:
        actions.self.clickable_cancel()


def on_overlay_closed():
    global overlay_closed_callback
    try:
        if overlay_closed_callback:
            overlay_closed_callback()
    except Exception as e:
        # TODO: Logger error
        print(f"Error calling overlay closed callback: {e}")
    finally:
        overlay_closed_callback = None


canvases = []
overlays_active_context = Context()


def create_canvases():
    destroy_canvases()
    for screen in ui.screens():
        c = canvas.Canvas.from_screen(screen)
        # HOTFIX: from_screen not working right on Windows
        if app.platform == "windows":
            hotfix_rect = Rect(*screen.rect)
            hotfix_rect.height -= 1
            c.rect = hotfix_rect
        c.register("draw", draw)
        c.register("focus", on_focus)
        c.freeze()
        canvases.append(c)
    overlays_active_context.tags = ["user.clickable_overlay_active"]
    # canvases[0].focused = True


def destroy_canvases():
    overlays_active_context.tags = []
    for c in canvases:
        c.unregister("draw", draw)
        c.unregister("focus", on_focus)
        c.close()
    canvases.clear()


def redraw_canvases():
    for c in canvases:
        c.resume()
        c.freeze()


class LabelTypes(Enum):
    CLICKABLE = 0
    FOCUSABLE = 1
    OTHER = 2


class CandidateAction:
    """Represents an action that can be performed on a candidate."""

    def __init__(self, shortcut: str, label: str, callback: Callable[[], None]):
        assert shortcut in VALID_SHORTCUT_KEYS
        self.shortcut = shortcut
        self.label = label
        self.callback = callback


class Clickable:
    def __init__(
        self,
        bounds: Rect,
        # TODO: Document the `focus_callback`
        focus_callback: Optional[Callable[[], None]] = None,
        pre_click_callback: Optional[Callable[[], None]] = None,
        post_click_callback: Optional[Callable[[], None]] = None,
    ):
        self.bounds = bounds
        self.focus_callback = focus_callback
        self.pre_click_callback = None
        self.post_click_callback = None


class LabelledCandidate:
    def __init__(self, clickable: Clickable, label: str, action_type: ActionTypes):
        self.clickable = clickable
        self.label = label
        self.action_type = action_type


module = Module()
module.tag(
    "clickable_overlay_active", "Active when the clickable buttons overlay is showing."
)


@module.action_class
class Actions:
    def clickable_get_clickables() -> List[Clickable]:
        """Get all clickable candidates in the current program."""

    def clickable_get_focusables() -> List[Clickable]:
        """Get all focusable candidates in the current program."""

    def clickable_start_clickables():
        """Label all candidates that can be clicked in the current program."""
        actions.self.clickable_overlay_show(
            actions.self.clickable_get_clickables(), LabelTypes.CLICKABLE
        )

    def clickable_start_focusables():
        """Label all candidates that can be focussed in the current program."""
        candidates = actions.self.clickable_get_focusables()
        for candidate in candidates:
            if not callable(candidate.focus_callback):
                raise ValueError(
                    "All focusable candidates must have a `focus` callback."
                )
        actions.self.clickable_overlay_show(candidates, LabelTypes.FOCUSABLE)

    def clickable_overlay_show(
        candidates: List[Clickable],
        # TODO: Should this be optional, to allow different default actions per element?
        label_type: LabelTypes = LabelTypes.CLICKABLE,
        overlay_closed_callback_: Optional[Callable] = None,
    ):
        """Show all candidates in the clickable overlay"""
        global active_candidates, overlay_closed_callback

        # Now assign labels - this currently uses a naive method. Needs improving.
        labels = []
        labelled_candidates = []
        for char_0 in VALID_KEYS:
            child_set = set(VALID_KEYS)
            child_set.remove(char_0)
            for char_1 in child_set:
                labels.append([char_0, char_1])
        for i, candidate in enumerate(candidates):
            if label_type == LabelTypes.FOCUSABLE:
                action_type = ActionTypes.FOCUS
            else:
                action_type = ActionTypes.LEFT_CLICK
            labelled_candidates.append(
                # TODO: Remove label_type. Should I just color based on the
                #   current action? Also narrow based on the current action? No,
                #   do it per item. Ok but then how to arrange?
                LabelledCandidate(candidate, labels[i], action_type)
            )

        with candidates_lock:
            active_candidates = labelled_candidates
            overlay_closed_callback = overlay_closed_callback_

        create_canvases()

    def clickable_handle_key(key: str):
        """Handle a single keypress when the clickable overlay is open."""
        global active_candidates, queued_action

        if key in ACTION_KEYS.keys():
            with candidates_lock:
                action_type = ACTION_KEYS[key]
                for candidate in active_candidates:
                    # TODO: Filter the candidates based on whether they have this action type
                    candidate.action_type = action_type
                redraw_canvases()
        else:
            with candidates_lock:
                active_candidates = list(
                    filter(
                        lambda it: it.label and it.label[0] == key,
                        active_candidates,
                    )
                )
                if len(active_candidates) == 0:
                    # Invalid key - stop narrowing and cancel
                    actions.self.clickable_cancel()
                elif len(active_candidates) == 1:
                    # Final candidate - act on it
                    try:
                        candidate = active_candidates[0]
                        if candidate.clickable.pre_click_callback:
                            candidate.clickable.pre_click_callback()
                        # TODO: Configurable actions. Attach to candidate
                        if candidate.action_type == ActionTypes.FOCUS:
                            # FIXME: Focussing doesn't seem to want to work.
                            # candidate.clickable.focus_callback()
                            actions.mouse_move(*candidate.clickable.bounds.center)
                            actions.mouse_click(button=0)
                        else:
                            actions.mouse_move(*candidate.clickable.bounds.center)
                            # actions.user.shake_mouse(0.05)
                            if candidate.action_type == ActionTypes.LEFT_CLICK:
                                actions.mouse_click(button=0)
                            elif candidate.action_type == ActionTypes.RIGHT_CLICK:
                                actions.mouse_click(button=1)
                            elif candidate.action_type == ActionTypes.MIDDLE_CLICK:
                                actions.mouse_click(button=2)
                            elif candidate.action_type == ActionTypes.DOUBLE_LEFT_CLICK:
                                actions.mouse_click(button=0)
                                actions.sleep("50ms")
                                actions.mouse_click(button=0)
                            elif candidate.action_type == ActionTypes.HOVER_OVER:
                                pass
                            else:
                                raise NotImplementedError(
                                    f"Unrecognized label type: {candidate.action_type}"
                                )
                        if candidate.clickable.post_click_callback:
                            candidate.clickable.post_click_callback()
                    finally:
                        active_candidates.clear()
                        destroy_canvases()
                        on_overlay_closed()
                else:
                    # Now we target the next char in the label
                    for candidate in active_candidates:
                        candidate.label = candidate.label[1:]
                    redraw_canvases()

    def clickable_cancel():
        """Close the current clickable overlay and cancel the operation."""
        global overlay_closed_callback
        destroy_canvases()
        with candidates_lock:
            active_candidates.clear()
            on_overlay_closed()
