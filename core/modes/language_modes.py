from talon import Context, Module, actions, resource

from ..user_settings import get_key_value_pairs_and_spoken_forms_from_three_column_csv, compute_csv_path, compute_spoken_form_to_key_dictionary

mod = Module()

ctx = Context()

ctx_forced = Context()
ctx_forced.matches = r"""
tag: user.code_language_forced
"""


mod.tag("code_language_forced", "This tag is active when a language mode is forced")
mod.list("language_mode", desc="Name of a programming language mode.")

# Maps extension to languages.
extension_lang_map = None

language_ids = None
language_extensions = None

SETTINGS_FILENAME = "language_modes.csv"
settings_filepath = compute_csv_path(SETTINGS_FILENAME)
@resource.watch(settings_filepath)
def load_language_modes(path: str):
    # Maps language mode names to the extensions that activate them. Only put things
    # here which have a supported language mode; that's why there are so many
    # commented out entries. TODO: make this a csv file?
    default_csv_contents = [
        #['assembly', ('asm', 's'),],
        #['bash', ('bashbook', 'sh'),],
        ["batch", ("bat",),],
        ["c", ("c", "h"),],
        #['cmake', ('cmake',),],
        #["cplusplus", ("cpp hpp",), ("see plus plus",)],
        ["csharp", ("cs",), ("see sharp",)],
        ["css", ("css",), ("c s s",)],
        #['elisp', ('el'),],
        #['elm', ('elm'),],
        ["gdb", ("gdb",), ("g d b",)],
        ["go", ("go",), ("go", "go lang", "go language")],
        ["java", ("java",),],
        ["javascript", ("js",),],
        ["javascriptreact", ("jsx",),],
        #["json", ("json",),],
        ["kotlin", ("kt",),],
        ["lua", ("lua",),],
        ["markdown", ("md",),],
        #['perl', ('pl',),],
        ["php", ("php",),],
        #['powershell', ('ps1',),],
        ["python", ("py",),],
        ["protobuf", ("proto",),],
        ["r", ("r"), ("are language",)],
        #['racket', ('rkt,'),],
        ["ruby", ("rb",),],
        ["rust", ("rs",),],
        ["scala", ("scala",),],
        ["scss", ("scss",),],
        #['snippets', ('snippets',),],
        ["sql", ("sql",),],
        ["stata", ("do", "ado"),],
        ["talon", ("talon",),],
        ["talonlist", ("talon-list",),],
        ["terraform", ("tf",),],
        ["tex", ("tex",), ("tech", "lay tech", "latex")],
        ["typescript", ("ts",),],
        ["typescriptreact", ("tsx",),],
        #['vba', ('vba',),],
        ["vimscript", ("vim", "vimrc"),],
        #htm doesn't actually have a language moded, but we do have snippets.
        ["html", ("html",),],
    ]
    
    global language_extensions
    language_extensions, language_spoken_forms = get_key_value_pairs_and_spoken_forms_from_three_column_csv(
        SETTINGS_FILENAME,
        ["language", "extensions", "spoken_forms"],
        default_csv_contents,
    )
    ctx.lists["self.language_mode"] = compute_spoken_form_to_key_dictionary(language_extensions, language_spoken_forms)
    global extension_lang_map
    extension_lang_map = {
        "." + ext: language
        for language, extensions in language_extensions.items()
        for ext in extensions
    }
    global language_ids
    language_ids = set(language_extensions.keys())
load_language_modes(settings_filepath)

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
