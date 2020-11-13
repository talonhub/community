from talon import actions, Module, speech_system

mod = Module()

macro = []
recording = False


@mod.action_class
class Actions:
    def macro_record():
        """record a new macro"""
        global macro
        global recording

        macro = []
        recording = True

    def macro_stop():
        """stop recording"""
        global recording
        recording = False

    def macro_play():
        """player recorded macro"""
        actions.user.macro_stop()

        # :-1 because we don't want to replay `macro play`
        for words in macro[:-1]:
            print(words)
            actions.mimic(words)


def fn(d):
    if not recording:
        return

    if "parsed" not in d:
        return

    macro.append(d["parsed"]._unmapped)


speech_system.register("pre:phrase", fn)
