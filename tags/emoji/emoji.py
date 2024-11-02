from talon import Module

mod = Module()

mod.tag("emoji", desc="Emoji, ascii emoticons and kaomoji")

mod.list("emoticon", desc="Western emoticons (ascii)")
mod.list("emoji", desc="Emoji (unicode)")
mod.list("kaomoji", desc="Eastern kaomoji (unicode)")
