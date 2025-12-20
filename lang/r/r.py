from talon import Context, actions, settings

from ..tags.operators import Operators

ctx = Context()

ctx.matches = r"""
code.language: r
"""


ctx.lists["user.code_libraries"] = {
    "bayes plot": "bayesplot",
    "BRMS": "brms",
    "cable": "kable",
    "car": "car",
    "D plier": "dplyr",
    "dev tools": "devtools",
    "future": "future",
    "furr": "furrr",
    "gap minder": "gapminder",
    "gee animate": "gganimate",
    "gee highlight": "gghighlight",
    "gee map": "ggmap",
    "gee repel": "ggrepel",
    "grid extra": "gridExtra",
    "gee gee plot": "ggplot2",
    "GLMM TMB": "glmmTMB",
    "here": "here",
    "knitter": "knitr",
    "LME four": "lme4",
    "LM test": "lmtest",
    "lubridate": "lubridate",
    "margins": "margins",
    "inla": "INLA",
    "NLME": "nlme",
    "psych": "psych",
    "purr": "purrr",
    "R markdown": "rmarkdown",
    "R stan": "rstan",
    "R stan arm": "rstanarm",
    "R color brewer": "RColorBrewer",
    "read R": "readr",
    "stargazer": "stargazer",
    "tidy verse": "tidyverse",
    "tidier": "tidyr",
    "tidy bayes": "tidybayes",
    "TMB": "TMB",
    "vee table": "vtable",
    "viridis": "viridis",
    "viridis light": "viridisLite",
    "shiny alert": "shinyalert",
}

ctx.lists["user.code_parameter_name"] = {
    "alpha": "alpha",
    "breaks": "breaks",
    "colour": "colour",
    "data": "data",
    "fill": "fill",
    "H just": "hjust",
    "keep": ".keep",
    "label": "label",
    "labels": "labels",
    "log": "log",
    "main": "main",
    "mapping": "mapping",
    "method": "method",
    "NA remove": "na.rm",
    "path": "path",
    "position": "position",
    "plex label": "xlab",
    "plex limit": "xlim",
    "scales": "scales",
    "size": "size",
    "show legend": "show.legend",
    "sort": "sort",
    "title": "title",
    "type": "type",
    "vee just": "vjust",
    "width": "width",
    "with ties": "with_ties",
    "why label": "ylab",
    "why limit": "ylim",
    "why max": "ymax",
    "why min": "ymin",
}

operators = Operators(
    # code_operators_assignment
    ASSIGNMENT=" <- ",
    # code_operators_bitwise
    BITWISE_AND=" & ",
    # code_operators_math:
    MATH_SUBTRACT=" - ",
    MATH_ADD=" + ",
    MATH_MULTIPLY=" * ",
    MATH_EXPONENT=" ** ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" %% ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" & ",
    MATH_OR=" | ",
    MATH_IN=" %in% ",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_insert_null():
        actions.auto_insert("NULL")

    def code_insert_is_null():
        actions.user.insert_between("is.null(", ")")

    def code_insert_is_not_null():
        actions.user.insert_between("!is.null(", ")")

    def code_insert_true():
        actions.auto_insert("TRUE")

    def code_insert_false():
        actions.auto_insert("FALSE")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_private_function(text: str):
        result = "{} <- function () {{\n\n}}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.paste(result)
        actions.edit.up()
        actions.edit.up()
        actions.edit.line_end()
        actions.edit.left()
        actions.edit.left()
        actions.edit.left()

    def code_insert_library(text: str, selection: str):
        actions.user.insert_snippet_by_name("importStatement", {"0": text + selection})

    def code_insert_named_argument(parameter_name: str):
        actions.insert(f"{parameter_name} = ")
