from talon import Context, Module, actions, clip, imgui, speech_system

mod = Module()

mod.list(
    "saved_macros",
    desc="list of macros that have been saved with the 'macro save' command",
)
ctx = Context()

macros = {}
macro = []
recording = False


@imgui.open(y=0)
def macro_list_gui(gui: imgui.GUI):
    gui.text("macros")
    gui.line()
    for command_name in macros.keys():
        gui.text(command_name)

    if gui.button("macro list close"):
        actions.user.macro_list_close()


@mod.action_class
class Actions:
    def macro_record():
        """Begin recording a new voice command macro."""
        global macro
        global recording

        macro = []
        recording = True

    def macro_stop():
        """Stop recording the macro."""
        global recording
        if recording and len(macro) != 0:
            # Remove the final `macro stop`/`macro play`/`macro save` command
            macro.pop()
        recording = False

    def macro_save(name: str):
        """Save the macro."""
        actions.user.macro_stop()
        macros[name] = macro

        ctx.lists["user.saved_macros"] = macros.keys()

    def macro_list():
        """List all saved macros."""
        macro_list_gui.show()

    def macro_list_close():
        """Closed the saved macros list."""
        macro_list_gui.hide()

    def macro_play(name: str):
        """Execute the commands in the last recorded macro."""
        actions.user.macro_stop()

        selected_macro = macro
        if name in macros:
            selected_macro = macros[name]

        for words in selected_macro:
            print(words)
            actions.mimic(words)

    def macro_copy(name: str):
        """Copied the specified macro to the clipboard as a Talon command."""
        selected_macro = macro

        if not name:
            # No macro name was provided, so we'll copy the most recent command
            # with this default name
            name = "last macro command"
        elif name in macros:
            selected_macro = macros[name]

        l = [name + ":"]

        for words in selected_macro:
            l.append(f'\tmimic("{" ".join(words)}")')

        clip.set_text("\n".join(l))

    def macro_append_command(words: list[str]):
        """Appends a command to the current macro; called when a voice command is uttered while recording a macro."""
        assert recording, "Not currently recording a macro"
        macro.append(words)


def fn(d):
    if not recording or "parsed" not in d:
        return
    actions.user.macro_append_command(d["parsed"]._unmapped)


speech_system.register("pre:phrase", fn)
