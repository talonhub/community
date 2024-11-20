class Language:
    id: str
    spoken_forms: list[str]
    extensions: list[str]

    def __init__(self, id: str, spoken_form: str | list[str], extensions: list[str]):
        self.id = id
        self.spoken_forms = (
            [spoken_form] if isinstance(spoken_form, str) else spoken_form
        )
        self.extensions = extensions


# Maps code language identifiers, names and file extensions. Only put languages
# here which have a supported language mode; that's why there are so many
# commented out entries.
code_languages = [
    # Language("assembly", "assembly", ["asm", "s"]),
    # Language("bash", "bash", ["sh", "bashbook"]),
    Language("batch", "batch", ["bat"]),
    Language("c", "see", ["c", "h"]),
    # Language("cmake", "see make", ["cmake"]),
    # Language("cplusplus", "see plus plus", ["cpp", "hpp"]),
    Language("csharp", "see sharp", ["cs"]),
    Language("css", "c s s", ["css"]),
    # Language("elisp", "elisp", ["el"]),
    Language("elixir", "elixir", ["ex"]),
    # Language("elm", "elm", ["elm"]),
    Language("gdb", "g d b", ["gdb"]),
    Language("go", ["go lang", "go language"], ["go"]),
    # html doesn't actually have a language mode, but we do have snippets.
    Language("html", "html", ["html"]),
    Language("java", "java", ["java"]),
    Language("javascript", "java script", ["js"]),
    Language("javascriptreact", "java script react", ["jsx"]),
    # Language("json", "json", ["json"]),
    # Language("jsonl", "json lines", ["jsonl"]),
    Language("kotlin", "kotlin", ["kt"]),
    Language("lua", "lua", ["lua"]),
    Language("markdown", "mark down", ["md"]),
    # Language("perl", "perl", ["pl"]),
    Language("php", "p h p", ["php"]),
    # Language("powershell", "power shell", ["ps1"]),
    Language("protobuf", "proto buf", ["proto"]),
    Language("python", "python", ["py"]),
    Language("r", "are language", ["r"]),
    # Language("racket", "racket", ["rkt"]),
    Language("ruby", "ruby", ["rb"]),
    Language("rust", "rust", ["rs"]),
    Language("scala", "scala", ["scala"]),
    Language("scss", "scss", ["scss"]),
    # Language("snippets", "snippets", ["snippets"]),
    Language("sql", "sql", ["sql"]),
    Language("stata", "stata", ["do", "ado"]),
    Language("talon", "talon", ["talon"]),
    Language("talonlist", "talon list", ["talon-list"]),
    Language("terraform", "terraform", ["tf"]),
    Language("tex", ["tech", "lay tech", "latex"], ["tex"]),
    Language("typescript", "type script", ["ts"]),
    Language("typescriptreact", "type script react", ["tsx"]),
    # Language("vba", "vba", ["vba"]),
    Language("vimscript", "vim script", ["vim", "vimrc"]),
]

# Files without specific extensions but are associated with languages
# Maps full filename to language identifiers
code_special_file_map = {
    "CMakeLists.txt": "cmake",
    "Makefile": "make",
    "Dockerfile": "docker",
    "meson.build": "meson",
    ".bashrc": "bash",
    ".zshrc": "zsh",
    "PKGBUILD": "pkgbuild",
    ".vimrc": "vimscript",
    "vimrc": "vimscript",
}
