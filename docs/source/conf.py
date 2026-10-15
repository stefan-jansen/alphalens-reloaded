# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path
from alphalens import __version__ as version

sys.path.insert(0, Path("../..").resolve(strict=True).as_posix())

extensions = [
    "sphinx.ext.autodoc",
    "numpydoc",
    "m2r2",
    "sphinx_markdown_tables",
    "nbsphinx",
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
]

templates_path = ["_templates"]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

master_doc = "index"

project = "Alphalens"
copyright = "2016, Quantopian, Inc."
author = "Quantopian, Inc."

release = version
language = "en"

exclude_patterns = []

highlight_language = "python"

pygments_style = "sphinx"

todo_include_todos = False

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "github_url": "https://github.com/stefan-jansen/alphalens-reloaded",
    "twitter_url": "https://twitter.com/ml4trading",
    "external_links": [
        {"name": "ML for Trading", "url": "https://ml4trading.io"},
        {"name": "Community", "url": "https://exchange.ml4trading.io"},
    ],
    "analytics": {"google_analytics_id": "UA-74956955-3"},
    "use_edit_page_button": True,
}

html_context = {
    "github_url": "https://github.com",
    "github_user": "stefan-jansen",
    "github_repo": "alphalens-reloaded",
    "github_version": "main",
    "doc_path": "docs/source",
}

html_static_path = []

htmlhelp_basename = "Alphalensdoc"

latex_elements = {}

latex_documents = [
    (
        master_doc,
        "Alphalens.tex",
        "Alphalens Documentation",
        "Quantopian, Inc.",
        "manual",
    )
]

man_pages = [(master_doc, "alphalens", "Alphalens Documentation", [author], 1)]

texinfo_documents = [
    (
        master_doc,
        "Alphalens",
        "Alphalens Documentation",
        author,
        "Alphalens",
        "One line description of project.",
        "Miscellaneous",
    )
]
