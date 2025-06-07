from talon import actions, speech_system
from talon.grammar import Phrase

from .subtitles import show_subtitle


def on_pre_phrase(phrase: Phrase):
    if skip_phrase(phrase):
        return

    current_phrase = parse_phrase(phrase)
    show_subtitle(current_phrase)


def skip_phrase(phrase: Phrase) -> bool:
    return not phrase.get("phrase") or skip_phrase_in_sleep(phrase)


def skip_phrase_in_sleep(phrase: Phrase) -> bool:
    """Returns true if the rule is <phrase> in sleep mode"""
    return (
        not actions.speech.enabled()
        and len(phrase["parsed"]) == 1
        and phrase["parsed"][0]._name == "___ltphrase_gt__"
    )


def parse_phrase(phrase: Phrase) -> str:
    words = phrase["phrase"]
    return " ".join(words)


speech_system.register("phrase", on_pre_phrase)
