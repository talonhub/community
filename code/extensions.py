from talon import Module, Context, actions, app

mod = Module()
mod.list("file_extension", desc="A file extension, such as .py")

ctx = Context()
ctx.lists["self.file_extension"] = {
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