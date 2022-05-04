import csv
import os
from pathlib import Path
from typing import Dict, List, Tuple
from talon import resource

from talon import Context, Module, actions

mod = Module()

ctx = Context()

# NOTE: This method requires this module to be one folder below the top-level
#   knausj folder.
SETTINGS_DIR = Path(__file__).parents[1] / "settings"

def add_word_to_additional_words(word: str):
    path = SETTINGS_DIR / "additional_words.csv"

    with resource.open(str(path), "a") as f:
        f.write(word + "\n") #there is a csv writer in user.settings py, should i be using that instead?

@mod.action_class
class Actions:
    def add_custom_vocabulary(word: str):
        """ Adds a word to additional_words.csv"""
        add_word_to_additional_words(word) 
