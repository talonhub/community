from .user_settings import get_list_from_csv
from talon import Module, Context, actions, app

mod = Module()
mod.list("file_extension", desc="A file extension, such as .py")

_file_extensions_defaults = {
    "dot pie": ".py",
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
}

file_extensions = get_list_from_csv(
    "file_extensions.csv",
    headers=("File extension", "Name"),
    default=_file_extensions_defaults,
)

ctx = Context()
ctx.lists["self.file_extension"] = file_extensions
