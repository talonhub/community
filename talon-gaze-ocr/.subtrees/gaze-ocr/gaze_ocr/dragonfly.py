import dragonfly


class Mouse:
    def move(self, coordinates):
        dragonfly.Mouse("[{}, {}]".format(*coordinates)).execute()

    def click(self):
        dragonfly.Mouse("left").execute()

    def click_down(self):
        dragonfly.Mouse("left:down").execute()

    def click_up(self):
        dragonfly.Mouse("left:up").execute()

    def scroll_down(self, n=1):
        dragonfly.Mouse(f"wheeldown:{n}").execute()

    def scroll_up(self, n=1):
        dragonfly.Mouse(f"wheelup:{n}").execute()


class Keyboard:
    def __init__(self):
        self._shift = False

    def type(self, text):
        dragonfly.Text(text.replace("%", "%%")).execute()

    def shift_down(self):
        dragonfly.Key("shift:down").execute()
        self._shift = True

    def shift_up(self):
        dragonfly.Key("shift:up").execute()
        self._shift = False

    def is_shift_down(self):
        return self._shift

    def left(self, n=1):
        dragonfly.Key(f"left:{n}").execute()

    def right(self, n=1):
        dragonfly.Key(f"right:{n}").execute()


class Windows:
    def get_monitor_size(self):
        primary = dragonfly.Monitor.get_all_monitors()[0]
        return (primary.rectangle.dx, primary.rectangle.dy)

    def get_foreground_window_center(self):
        window_position = dragonfly.Window.get_foreground().get_position()
        return (window_position.x_center, window_position.y_center)


class MoveCursorToWordAction(dragonfly.ActionBase):
    def __init__(self, controller, word, cursor_position="middle", *args, **kwargs):
        self.controller = controller
        self.word = word
        self.cursor_position = cursor_position
        super().__init__(*args, **kwargs)

    def _execute(self, data=None):
        dynamic_word = self.word
        if data:
            dynamic_word = self.word % data
        # On Windows, works best if cursor is slightly offset to the right.
        return (
            self.controller.move_cursor_to_word(
                dynamic_word, self.cursor_position, click_offset_right=1
            )
            or False
        )


class MoveTextCursorAction(dragonfly.ActionBase):
    def __init__(self, controller, word, cursor_position="middle", *args, **kwargs):
        self.controller = controller
        self.word = word
        self.cursor_position = cursor_position
        super().__init__(*args, **kwargs)

    def _execute(self, data=None):
        dynamic_word = self.word
        if data:
            dynamic_word = self.word % data
        # On Windows, works best if cursor is slightly offset to the right.
        return (
            self.controller.move_text_cursor_to_word(
                dynamic_word, self.cursor_position, click_offset_right=1
            )
            or False
        )


class SelectTextAction(dragonfly.ActionBase):
    def __init__(
        self, controller, start_word, end_word=None, for_deletion=False, *args, **kwargs
    ):
        self.controller = controller
        self.start_word = start_word
        self.end_word = end_word
        self.for_deletion = for_deletion
        super().__init__(*args, **kwargs)

    def _execute(self, data=None):
        dynamic_start_word = self.start_word
        dynamic_end_word = self.end_word
        if data:
            dynamic_start_word = self.start_word % data
            if self.end_word:
                try:
                    dynamic_end_word = self.end_word % data
                except KeyError:
                    dynamic_end_word = None
        # On Windows, works best if cursor is slightly offset to the right.
        return (
            self.controller.select_text(
                dynamic_start_word,
                dynamic_end_word,
                for_deletion=self.for_deletion,
                click_offset_right=1,
            )
            or False
        )
