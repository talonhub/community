from talon import Context, Module, actions

ctx = Context()
mod = Module()

# Maps language mode names to the extensions that activate them. Only put things
# here which have a supported language mode; that's why there are so many
# commented out entries. TODO: make this a csv file?
language_extensions = {
    # 'assembly': 'asm s',
    # 'bash': 'bashbook sh',
    'batch': 'bat',
    'c': 'c h',
    # 'cmake': 'cmake',
    # 'cplusplus': 'cpp hpp',
    'csharp': 'cs',
    # 'css': 'css',
    # 'elisp': 'el',
    # 'elm': 'elm',
    'gdb': 'gdb',
    'go': 'go',
    # 'html': 'html',
    'java': 'java',
    'javascript': 'js',
    'javascriptreact': 'jsx',
    # 'json': 'json',
    # 'lua': 'lua',
    'markdown': 'md',
    # 'perl': 'pl',
    # 'powershell': 'ps1',
    'python': 'py',
    'protobuf': 'proto',
    'r': 'r',
    # 'racket': 'rkt',
    'ruby': 'rb',
    'rust': 'rs',
    # 'sass': 'sass',
    'scala': 'scala',
    # 'snippets': 'snippets',
    'talon': 'talon',
    'terraform': 'tf',
    'typescript': 'ts',
    'typescriptreact': 'tsx',
    # 'vba': 'vba',
    'vimscript': 'vim vimrc',
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
}
mod.list("language_mode", desc="Name of a programming language mode.")
ctx.lists["self.language_mode"] = {
    name: language
    for language in language_extensions
    for name in language_name_overrides.get(language, [language])
}

# Maps extension to languages.
extension_lang_map = {
    '.' + ext: language
    for language, extensions in language_extensions.items()
    for ext in extensions.split()
}

# Create a context for each defined language
for lang in language_extensions.keys():
    mod.tag(lang)
    mod.tag(f"{lang}_forced")
    c = Context()
    # Context is active if language is forced or auto language matches
    c.matches = f"""
    tag: user.{lang}_forced
    tag: user.auto_lang
    and code.language: {lang}
    """
    c.tags = [f"user.{lang}"]

# Create a mode for the automated language detection. This is active when no lang is forced.
mod.tag("auto_lang")
ctx.tags = ["user.auto_lang"]


@ctx.action_class("code")
class code_actions:
    def language():
        result = ""
        file_extension = actions.win.file_ext()
        if file_extension and file_extension in extension_lang_map:
            result = extension_lang_map[file_extension]
        return result


@mod.action_class
class Actions:
    def code_set_language_mode(language: str):
        """Sets the active language mode, and disables extension matching"""
        assert language in language_extensions
        ctx.tags = [f"user.{language}_forced"]

    def code_clear_language_mode():
        """Clears the active language mode, and re-enables code.language: extension matching"""
        ctx.tags = ["user.auto_lang"]
