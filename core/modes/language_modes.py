from talon import Context, Module, actions

# Maps language mode names to the extensions that activate them. Only put things
# here which have a supported language mode; that's why there are so many
# commented out entries. TODO: make this a csv file?
language_extensions = {
    # 'assembly': 'asm s',
    # 'bash': 'bashbook sh',
    "batch": "bat",
    "c": "c h",
    # 'cmake': 'cmake',
    # "cplusplus": "cpp hpp",
    "csharp": "cs",
    "css": "css",
    # 'elisp': 'el',
    # 'elm': 'elm',
    "gdb": "gdb",
    "go": "go",
    "java": "java",
    "javascript": "js",
    "javascriptreact": "jsx",
    # "json": "json",
    "kotlin": "kt",
    "lua": "lua",
    "markdown": "md",
    # 'perl': 'pl',
    "php": "php",
    # 'powershell': 'ps1',
    "python": "py",
    "protobuf": "proto",
    "r": "r",
    # 'racket': 'rkt',
    "ruby": "rb",
    "rust": "rs",
    "scala": "scala",
    "scss": "scss",
    # 'snippets': 'snippets',
    "sql": "sql",
    "stata": "do ado",
    "talon": "talon",
    "talonlist": "talon-list",
    "terraform": "tf",
    "tex": "tex",
    "typescript": "ts",
    "typescriptreact": "tsx",
    # 'vba': 'vba',
    "vimscript": "vim vimrc",
    # html doesn't actually have a language mode, but we do have snippets.
    "html": "html",
}

# Override speakable forms for language modes. If not present, a language mode's
# name is used directly.
language_name_overrides = {
    "cplusplus": ["see plus plus"],
    "csharp": ["see sharp"],
    "css": ["c s s"],
    "gdb": ["g d b"],
    "go": ["go", "go lang", "go language"],
    "r": ["are language"],
    "tex": ["tech", "lay tech", "latex"],
}

mod = Module()

ctx = Context()

ctx_forced = Context()
ctx_forced.matches = r"""
tag: user.code_language_forced
"""


mod.tag("code_language_forced", "This tag is active when a language mode is forced")
mod.list("language_mode", desc="Name of a programming language mode.")

ctx.lists["self.language_mode"] = {
    name: language
    for language in language_extensions
    for name in language_name_overrides.get(language, [language])
}

# Maps extension to languages.
extension_lang_map = {
    "." + ext: language
    for language, extensions in language_extensions.items()
    for ext in extensions.split()
}

language_ids = set(language_extensions.keys())

forced_language = ""


@ctx.action_class("code")
class CodeActions:
    def language():
        file_extension = actions.win.file_ext()
        return extension_lang_map.get(file_extension, "")


@ctx_forced.action_class("code")
class ForcedCodeActions:
    def language():
        return forced_language


@mod.action_class
class Actions:
    def code_set_language_mode(language: str):
        """Sets the active language mode, and disables extension matching"""
        global forced_language
        assert language in language_extensions
        forced_language = language
        # Update tags to force a context refresh. Otherwise `code.language` will not update.
        # Necessary to first set an empty list otherwise you can't move from one forced language to another.
        ctx.tags = []
        ctx.tags = ["user.code_language_forced"]

    def code_clear_language_mode():
        """Clears the active language mode, and re-enables code.language: extension matching"""
        global forced_language
        forced_language = ""
        ctx.tags = []
