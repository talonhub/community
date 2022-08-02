from talon import Context, Module

mod = Module()
mod.tag("anaconda", desc="tag for enabling anaconda commands in your terminal")

ctx = Context()
ctx.matches = r"""
tag: user.anaconda
"""
