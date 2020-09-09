from talon import Module, Context, actions, ui, imgui, clip, settings

ctx = Context()

ctx.matches = r"""
mode: user.r
mode: command
and code.language: r
"""

ctx.lists["user.code_functions"] = {
    "anti join": "anti_join",
    "arrange": "arrange",
    "as character": "as.character",
    "as date": "as.Date",
    "as data frame": "as.data.frame",
    "as tibble": "as_tibble",
    "as double": "as.double",
    "as factor": "as.factor",
    "as numeric": "as.numeric",
    "bind rows": "bind_rows",
    "cable": "kable",
    "case when": "case_when",
    "count": "count",
    "covariance": "cov",
    "correlation": "cor",
    "distinct": "distinct",
    "describe": "describe",
    "drop NA": "drop_na",
    "eigen": "eigen",
    "everything": "everything",
    "filter": "filter",
    "full join": "full_join",
    "gather": "gather",
    "get working directory": "getwd",
    "set working directory": "setwd",
    "gather": "gather",
    "glimpse": "glimpse",
    "group by": "group_by",
    "head": "head",
    "if else": "ifelse",
    "inner join": "inner_join",
    "install packages": "install.packages",
    "is NA": "is.na",
    "not NA": "!is.na",
    "left join": "left_join",
    "length": "length",
    "library": "library",
    "list": "list",
    "list files": "list.files",
    "lm": "lm",
    "log": "log",
    "M table": "mtable",
    "make directory": "dir.create",
    "map": "map",
    "margins": "margins",
    "max": "max",
    "min": "min",
    "mean": "mean",
    "mutate": "mutate",
    "names": "names",
    "nest": "nest",
    "print": "print",
    "read CSV": "read_csv",
    "read E views": "readEViews",
    "read excel": "read_xlsx",
    "read RDS": "read_rds",
    "rename": "rename",
    "rename all": "rename_all",
    "repeat": "rep",
    "reorder": "reorder",
    "right join": "right_join",
    "sequence": "seq",
    "semi join": "semi_join",
    "select": "select",
    "select all": "select_all",
    "scale": "scale",
    "starts with": "starts_with",
    "string contains": "str_detect",
    "string detect": "str_detect",
    "string replace": "str_replace",
    "string replace all": "str_replace_all",
    "subset": "subset",
    "sum": "sum",
    "summarise": "summarise",
    "summary": "summary",
    "tail": "tail",
    "tidy": "tidy",
    "tibble": "tibble",
    "trim white space": "trimws",
    "type": "typeof",
    "ungroup": "ungroup",
    "unique": "unique",
    "vector": "c",
    "view": "View",
    "vee table": "vtable",
    "write RDS": "write_rds",
    "write CSV": "write_csv",
    "ex table": "xtable",
    "un nest": "unnest",
    # Shiny
    "shine ui": "shinyUI",
    "title panel": "titlePanel",
    "main panel": "mainPanel",
    "tab panel": "tabPanel",
    "navigation list panel": "navlistPanel",
    "conditional panel": "conditionalPanel",
    "input panel": "inputPanel",
    "ui output": "uiOutput",
    "text output": "textOutput",
    "table output": "tableOutput",
    "data table output": "dataTableOutput",
    "select size input": "selectizeInput",
    "action button": "actionButton",
    "download button": "downloadButton",
    "render ui": "renderUI",
    "observe event": "observeEvent",
    # Base
    "paste": "paste0",
    "sort": "sort",
}

ctx.lists["user.code_libraries"] = {
    "cable": "kable",
    "car": "car",
    "dev tools": "devtools",
    "gap minder": "gapminder",
    "gee animate": "gganimate",
    "gee highlight": "gghighlight",
    "gee map": "ggmap",
    "gee repel": "ggrepel",
    "grid extra": "gridExtra",
    "knitter": "knitr",
    "LM test": "lmtest",
    "margins": "margins",
    "psych": "psych",
    "stargazer": "stargazer",
    "tidy verse": "tidyverse",
    "vee table": "vtable",
    "viridis": "viridis",
    "shiny alert": "shinyalert",
}

@ctx.action_class("user")
class user_actions:
    def code_insert_function(text: str, selection: str):
        if selection:
            text = text + "({})".format(selection)
        else:
            text = text + "()"
        actions.user.paste(text)
        actions.edit.left()

    def code_private_function(text: str):
        result = "{} <- function ()\n{{\n\n}}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )

        actions.user.paste(result)
        actions.edit.up()

    def code_insert_library(text: str, selection: str):
        actions.clip.set_text(text + "{}".format(selection))
        actions.edit.paste()
