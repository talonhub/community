# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "knausj_talon"
copyright = "2021, Jeff Knaus, Ryan Hileman, Zach Dwiel, Michael Arntzenius, and others"
author = "Jeff Knaus, Ryan Hileman, Zach Dwiel, Michael Arntzenius, and others"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # Enables support for Markdown
    # https://www.sphinx-doc.org/en/master/usage/markdown.html
    "myst_parser",
    # Enable support for Talon
    "talondoc.sphinx",
]

# -- Options for MyST --------------------------------------------------------

myst_enable_extensions = [
    # Enables colon fence directives
    # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#syntax-colon-fence
    "colon_fence",
    # Enables definition lists
    # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#definition-lists
    "deflist",
]

# -- Options for TalonDoc ----------------------------------------------------

talon_package = {
    "path": ".",
    "name": "user",
    "exclude": [
        "conf.py",
        "test/stubs/talon/__init__.py",
        "test/stubs/talon/grammar.py",
        "test/stubs/talon/experimental/textarea.py",
        "test/test_code_modified_function.py",
        "test/test_create_spoken_forms.py",
        "test/test_dictation.py",
        "test/test_formatters.py",
    ],
    "trigger": "ready",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
