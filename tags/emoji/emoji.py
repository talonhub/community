from pathlib import Path

from talon import Context, Module

# --- Tag definition ---
mod = Module()
mod.tag("emoji", desc="Emoji, ascii emoticons and kaomoji")

# Context matching
ctx = Context()
ctx.matches = """
tag: user.emoji
"""

# --- Define and implement lists ---
path = Path(__file__).parents[0]

mod.list("emoticon", desc="Western emoticons (ascii)")
mod.list("emoji", desc="Emoji (unicode)")
mod.list("kaomoji", desc="Eastern kaomoji (unicode)")
