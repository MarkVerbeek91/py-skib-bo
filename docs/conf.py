"""Sphinx configuration."""
project = "Skip Bo Game"
author = "Mark Verbeek"
copyright = "2023, Mark Verbeek"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
