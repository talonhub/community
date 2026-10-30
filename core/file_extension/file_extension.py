from talon import Context, Module

from ..user_settings import register_customization_csv

mod = Module()
mod.list("file_extension", desc="A file extension, such as .py")

_file_extensions_defaults = {
    "dot bend": ".bin",
    "dot bin": ".bin",
    "dot cassie": ".csv",
    "dot class": ".class",
    "dot css": ".css",
    "dot csv": ".csv",
    "dot doc x": ".docx",
    "dot doc": ".doc",
    "dot elixir": ".ex",
    "dot exe": ".exe",
    "dot flack": ".flac",
    "dot g z": ".gz",
    "dot g zip": ".gzip",
    "dot go lang": ".go",
    "dot html": ".html",
    "dot J L": ".jl",
    "dot J S": ".js",
    "dot jason": ".json",
    "dot java script": ".js",
    "dot java": ".java",
    "dot jay son": ".json",
    "dot julia": ".jl",
    "dot log": ".log",
    "dot mark down": ".md",
    "dot ods": ".ods",
    "dot odt": ".odt",
    "dot oh de es": ".ods",
    "dot oh de tee": ".odt",
    "dot pdf": ".pdf",
    "dot pie": ".py",
    "dot png": ".png",
    "dot ps one": ".ps1",
    "dot sass": ".sass",
    "dot see sharp": ".cs",
    "dot see": ".c",
    "dot shell": ".sh",
    "dot svg": ".svg",
    "dot talon list": ".talon-list",
    "dot talon": ".talon",
    "dot tar": ".tar",
    "dot text": ".txt",
    "dot toml": ".toml",
    "dot TS": ".ts",
    "dot type script": ".ts",
    "dot vim": ".vim",
    "dot wave": ".wav",
    "dot zip": ".zip",
    "tot csv": ".csv",
    "totssv": ".csv",
}

ctx = Context()


@register_customization_csv(
    "file_extensions.csv",
    headers=("File extension", "Name"),
    default=_file_extensions_defaults,
)
def on_update(values):
    ctx.lists["user.file_extension"] = values
