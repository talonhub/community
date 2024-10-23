from talon import Context, Module

from ..user_settings import track_csv_list

mod = Module()
mod.list("file_extension", desc="A file extension, such as .py")

_file_extensions_defaults = {
    "dot pie": ".py",
    "dot elixir": ".ex",
    "dot talon": ".talon",
    "dot mark down": ".md",
    "dot shell": ".sh",
    "dot vim": ".vim",
    "dot see": ".c",
    "dot see sharp": ".cs",
    "dot com": ".com",
    "dot net": ".net",
    "dot org": ".org",
    "dot us": ".us",
    "dot U S": ".us",
    "dot co dot UK": ".co.uk",
    "dot exe": ".exe",
    "dot bin": ".bin",
    "dot bend": ".bin",
    "dot jason": ".json",
    "dot jay son": ".json",
    "dot J S": ".js",
    "dot java script": ".js",
    "dot TS": ".ts",
    "dot type script": ".ts",
    "dot csv": ".csv",
    "totssv": ".csv",
    "tot csv": ".csv",
    "dot cassie": ".csv",
    "dot text": ".txt",
    "dot julia": ".jl",
    "dot J L": ".jl",
    "dot html": ".html",
    "dot css": ".css",
    "dot sass": ".sass",
    "dot svg": ".svg",
    "dot png": ".png",
    "dot wave": ".wav",
    "dot flack": ".flac",
    "dot doc": ".doc",
    "dot doc x": ".docx",
    "dot pdf": ".pdf",
    "dot tar": ".tar",
    "dot g z": ".gz",
    "dot g zip": ".gzip",
    "dot zip": ".zip",
    "dot toml": ".toml",
    "dot java": ".java",
    "dot class": ".class",
    "dot log": ".log",
}

ctx = Context()


@track_csv_list(
    "file_extensions.csv",
    headers=("File extension", "Name"),
    default=_file_extensions_defaults,
)
def on_update(values):
    ctx.lists["self.file_extension"] = values
