import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "tkinter-dash"
author = "tkinter-dash contributors"
release = "0.1.4"
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_title = "tkinter-dash documentation"
html_static_path = []

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "tkinter": ("https://tkdocs.com/", None),
}

autodoc_member_order = "bysource"
autodoc_typehints = "description"
add_module_names = False
