from talon import Context, Module

from ..user_settings import track_csv_list

mod = Module()
mod.list("file_extension", desc="A file extension, such as .py")

_file_extensions_defaults = {
    "dot text": ".txt",
    "dot log": ".log",
    #
    "dot csv": ".csv",
    "totssv": ".csv",
    "tot csv": ".csv",
    "dot cassie": ".csv",
    "dot jason": ".json",
    "dot jay son": ".json",
    "dot toml": ".toml",
    "dot vim": ".vim",
    #
    "dot html": ".html",
    "dot mark down": ".md",
    #
    "dot css": ".css",
    "dot sass": ".sass",
    #
    "dot see": ".c",
    "dot see sharp": ".cs",
    "dot elixir": ".ex",
    "dot java": ".java",
    "dot julia": ".jl",
    "dot J L": ".jl",
    "dot java script": ".js",
    "dot J S": ".js",
    "dot pe es one": ".ps1",
    "dot pie": ".py",
    "dot shell": ".sh",
    "dot talon": ".talon",
    "dot type script": ".ts",
    "dot TS": ".ts",
    #
    "dot doc": ".doc",
    "dot doc x": ".docx",
    "dot oh de tee": ".odt",
    "dot oh de es": ".ods",
    "dot pdf": ".pdf",
    #
    "dot png": ".png",
    "dot svg": ".svg",
    #
    "dot wave": ".wav",
    "dot flack": ".flac",
    #
    "dot exe": ".exe",
    "dot class": ".class",
    "dot bin": ".bin",
    "dot bend": ".bin",
    #
    "dot zip": ".zip",
    "dot tar": ".tar",
    "dot g z": ".gz",
    "dot g zip": ".gzip",
    #
    "dot com": ".com",
    "dot net": ".net",
    "dot org": ".org",
    "dot us": ".us",
    "dot U S": ".us",
    "dot co dot UK": ".co.uk",
}

ctx = Context()


@track_csv_list(
    "file_extensions.csv",
    headers=("File extension", "Name"),
    default=_file_extensions_defaults,
)
def on_update(values):
    ctx.lists["self.file_extension"] = values
