# gaze-ocr

The `gaze-ocr` package makes easy to apply OCR to wherever the user is looking.
This library is designed for voice control. The following instructions are for
use with Dragonfly. For Talon, see
https://github.com/wolfmanstout/talon-gaze-ocr. See handsfreecoding.org for more
information about this package.

## Installation

1. Follow [instructions for installing
   screen-ocr](https://github.com/wolfmanstout/screen-ocr).
2. Download the [latest
   Tobii.Interaction](https://www.nuget.org/packages/Tobii.Interaction/) package
   from NuGet (these instructions have been tested on 0.7.3).
3. Rename the file extension to .zip and expand the contents.
4. Copy these 3 DLLs to a directory of your choice:
   build/AnyCPU/Tobii.EyeX.Client.dll, lib/net45/Tobii.Interaction.Model.dll,
   lib/net45/Tobii.Interaction.Net.dll.
5. Ensure that the files are not blocked (right-click Properties, and if there
   is a "Security" section at the bottom, check the "Unblock" box.)
6. `pip install gaze-ocr[dragonfly]`

## Usage

Provide the path to the DLL directory when constructing an EyeTracker instance.

Sample Dragonfly grammar:

```python
import gaze_ocr
import gaze_ocr.dragonfly
import gaze_ocr.eye_tracking
import screen_ocr

from dragonfly import (
    Dictation,
    Grammar,
    Key,
    MappingRule,
    Mouse,
    Text
)

# See installation instructions:
# https://github.com/wolfmanstout/gaze-ocr
DLL_DIRECTORY = "c:/Users/james/Downloads/tobii.interaction.0.7.3/"

# Initialize eye tracking and OCR.
tracker = gaze_ocr.eye_tracking.EyeTracker.get_connected_instance(DLL_DIRECTORY,
                                                                  mouse=gaze_ocr.dragonfly.Mouse(),
                                                                  keyboard=gaze_ocr.dragonfly.Keyboard(),
                                                                  windows=gaze_ocr.dragonfly.Windows())
ocr_reader = screen_ocr.Reader.create_fast_reader()
gaze_ocr_controller = gaze_ocr.Controller(ocr_reader,
                                          tracker,
                                          mouse=gaze_ocr.dragonfly.Mouse(),
                                          keyboard=gaze_ocr.dragonfly.Keyboard())


class CommandRule(MappingRule):
    mapping = {
        # Click on text.
        "<text> click": gaze_ocr.dragonfly.MoveCursorToWordAction(gaze_ocr_controller, "%(text)s") + Mouse("left"),

        # Move the cursor for text editing.
        "go before <text>": gaze_ocr.dragonfly.MoveTextCursorAction(gaze_ocr_controller, "%(text)s", "before"),
        "go after <text>": gaze_ocr.dragonfly.MoveTextCursorAction(gaze_ocr_controller, "%(text)s", "after"),

        # Select text starting from the current position.
        "words before <text>": Key("shift:down") + gaze_ocr.dragonfly.MoveTextCursorAction(gaze_ocr_controller, "%(text)s", "before") + Key("shift:up"),
        "words after <text>": Key("shift:down") + gaze_ocr.dragonfly.MoveTextCursorAction(gaze_ocr_controller, "%(text)s", "after") + Key("shift:up"),

        # Select a phrase or range of text.
        "words <text> [through <text2>]": gaze_ocr.dragonfly.SelectTextAction(gaze_ocr_controller, "%(text)s", "%(text2)s"),

        # Select and replace text.
        "replace <text> with <replacement>": gaze_ocr.dragonfly.SelectTextAction(gaze_ocr_controller, "%(text)s") + Text("%(replacement)s"),
    }

    extras = [
        Dictation("text"),
        Dictation("text2"),
        Dictation("replacement"),
    ]

    def _process_begin(self):
        # Start OCR now so that results are ready when the command completes.
        gaze_ocr_controller.start_reading_nearby()


grammar = Grammar("ocr_test")
grammar.add_rule(CommandRule())
grammar.load()


# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
```
