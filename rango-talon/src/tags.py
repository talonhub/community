from talon import Module, settings

mod = Module()

mod.tag("rango_disabled", desc="Tag for disabling Rango")

mod.tag(
    "rango_direct_clicking",
    desc="Tag for enabling direct clicking in Rango",
)
mod.tag(
    "rango_explicit_clicking",
    desc="Tag for enabling explicit clicking in Rango. This tag wins over rango_direct_clicking if both are enabled",
)

# These two tags are used for the commands `rango explicit` and `rango direct`
mod.tag(
    "rango_direct_clicking_forced",
    desc="Tag for forcing direct clicking in Rango",
)
mod.tag(
    "rango_explicit_clicking_forced",
    desc="Tag for forcing explicit clicking in Rango.",
)

mod.tag(
    "rango_exclude_singles",
    desc="Tag for excluding hints that contain only one letter",
)

mod.tag(
    "rango_number_hints",
    desc="Tag for enabling using numbers for hints in Rango",
)
