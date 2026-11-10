from talon import Context, Module, actions, settings

mod = Module()
ctx = Context()

mod.setting(
    "paste_to_insert_threshold",
    type=int,
    default=-1,
    desc="""Use paste to insert text longer than this many characters.
Zero means always paste; -1 means never paste. Note: some contexts (e.g. the terminal tag) may override this global setting.
""",
)

# forces text to be typed and not pasted
must_type_text: bool = False


@ctx.action_class("main")
class MainActions:
    def insert(text):
        threshold = settings.get("user.paste_to_insert_threshold")
        if 0 <= threshold < len(text) and not must_type_text:
            actions.user.paste(text)
            return
        actions.next(text)


@mod.action_class
class Actions:
    def type_text_bypassing_paste_to_insert(text: str):
        """Forces the text to be typed instead of pasted even if the paste_to_insert_threshold is used"""
        global must_type_text
        must_type_text = True
        actions.insert(text)
        must_type_text = False
