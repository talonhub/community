from talon import Module, Context

# --- Tag definition ---
mod = Module()
mod.tag("emoji", desc="Emoji, ascii emoticons and kaomoji")

# Context matching
ctx = Context()
ctx.matches = """
tag: user.emoji
"""

# --- Define and implement lists ---
mod.list("emoticon", desc="Western emoticons (ascii)")
ctx.lists["user.emoticon"] = {
    "broken heart": "</3",
    "cheeky": ":p",
    "cheer": r"\o/",
    "crying": ":'(",
    "happy": ":)",
    "heart": "<3",
    "horror": "D:",
    "laughing": ":D",
    "sad": ":(",
    "salute": "o7",
    "skeptical": ":/",
    "surprised": ":o",
    "wink": ";)",
}

mod.list("emoji", desc="Emoji (unicode)")
ctx.lists["user.emoji"] = {
    "angry": "😠",
    "blushing": "😊",
    "broken heart": "💔",
    "clapping": "👏",
    "cool": "😎",
    "crying": "😭",
    "dancing": "💃",
    "disappointed": "😞",
    "eyes": "👀",
    "happy": "😀",
    "heart": "❤️",
    "heart eyes": "😍",
    "hugging": "🤗",
    "kissing": "😗",
    "monocle": "🧐",
    "party": "🎉",
    "pleading": "🥺",
    "poop": "💩",
    "rofl": "🤣",
    "roll eyes": "🙄",
    "sad": "🙁",
    "shrug": "🤷",
    "shushing": "🤫",
    "star eyes": "🤩",
    "thinking": "🤔",
    "thumbs down": "👎️",
    "thumbs up": "👍️️",
    "worried": "😟",
}

mod.list("kaomoji", desc="Eastern kaomoji (unicode)")
ctx.lists["user.kaomoji"] = {
    "blushing": "(⁄ ⁄•⁄ω⁄•⁄ ⁄)",
    "crying": "(╥﹏╥)",
    "embarrassed": "(⌒_⌒;)",
    "flower girl": "(◕‿◕✿)",
    "happy": "(* ^ ω ^)",
    "kissing": "( ˘ ³˘)♥",
    "lenny": "( ͡° ͜ʖ ͡°)",
    "sad": "(｡•́︿•̀｡)",
    "shrug": r"¯\_(ツ)_/¯",
    "table flip": "(╯°□°)╯︵ ┻━┻",
    "table return": "┬─┬ ノ( ゜-゜ノ)",
}
