from talon import Module, actions, speech_system

mod = Module()

macro = []
recording = False


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
        recording = False

    def macro_play():
        """Execute the commands in the last recorded macro."""
        actions.user.macro_stop()

        # :-1 because we don't want to replay `macro stop`/`macro play`
        for words in macro[:-1]:
            print(words)
            actions.mimic(words)

    def macro_append_command(words: list[str]):
        """Appends a command to the current macro; called when a voice command is uttered while recording a macro."""
        assert recording, "Not currently recording a macro"
        macro.append(words)


def fn(d):
    if not recording or "parsed" not in d:
        return
    actions.user.macro_append_command(d["parsed"]._unmapped)


speech_system.register("pre:phrase", fn)
