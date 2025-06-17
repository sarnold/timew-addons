# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from datetime import datetime

if sys.version_info < (3, 8):
    from importlib_metadata import version
else:
    from importlib.metadata import version

from semaver import Version
import sphinx_nefertiti

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'timew-addons'
author = 'Stephen Arnold'
copyright = '2024 - ' + str(datetime.now().year) + f' {author}'

_ver_list = version('timew_addons').split(".")

# The X.Y number.
version = ".".join(_ver_list[:2])
# The X.Y.Z number.
release = ".".join(_ver_list[:3])

_ver_last = str(Version(release) - Version('0.0.1'))
if _ver_last.endswith('99'):
    _ver_last = _ver_last[:-2]


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinxcontrib.apidoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.autodoc.typehints',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'myst_parser',
    'sphinx_nefertiti',
    'sphinxcontrib.mermaid',
    'rst2pdf.pdfbuilder',
]

myst_enable_extensions = [
    'amsmath',
    'attrs_block',
    'colon_fence',
    'deflist',
    'dollarmath',
    'fieldlist',
    'tasklist',
    'substitution',
]

myst_suppress_warnings = ["myst.header"]
myst_fence_as_directive = ["mermaid"]

apidoc_module_dir = '../../src/timew_addons'
apidoc_output_dir = 'api'
apidoc_excluded_paths = ['tests', 'scripts']
apidoc_include_private = True
apidoc_separate_modules = True

autodoc_typehints = 'description'

templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.venv']

# The name of the Pygments (syntax highlighting) style to use.
#pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'sphinx_rtd_theme'
#html_logo = 'gh/images/timew.png'

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# The master toctree document.
master_doc = "index"

description = 'Timewarrior addons including an appindicator GUI and report extensions.'

# test nefertiti settings
language = "en"
today_fmt = '%A %d. %B %Y, %H:%M'

html_theme = "sphinx_nefertiti"

html_theme_options = {
    "monospace_font_size": ".90rem",

    "style": "blue",
    "style_header_neutral": True,
    "pygments_light_style": "pastie",
    "pygments_dark_style": "dracula",

    "logo": "timew.svg",
    "logo_width": 36,
    "logo_height": 36,
    "logo_alt": "timew-addons",

    "repository_url": f"https://github.com/sarnold/{project}",
    "repository_name": f"{project}",

    "current_version": "latest",
    "versions": [
        (f"v{release}", f"https://sarnold.github.io/{project}/"),
        (f"v{_ver_last}", f"https://sarnold.github.io/{project}/"),
    ],

    "show_colorset_choices": True,
    # Return user's to 'blue' after a day since color was picked.
    "reset_colorset_choice_after_ms": 1000 * 60 * 60 * 24,
}

html_static_path = ['static',]

# -- Options for PDF output --------------------------------------------------

# Grouping the document tree into PDF files. List of tuples
# (source start file, target name, title, author, options).
#
# If there is more than one author, separate them with \\.
# For example: r'Guido van Rossum\\Fred L. Drake, Jr., editor'
#
# The options element is a dictionary that lets you override
# this config per-document.
# For example,
# ('index', u'MyProject', u'My Project', u'Author Name',
#  dict(pdf_compressed = True))
# would mean that specific document would be compressed
# regardless of the global pdf_compressed setting.

pdf_documents = [
    #('filename', u'output filename', 'Title', 'author(s)'),
    ('index', u'timew_addons', u'Timew Status Indicator and Report Extensions', u"Stephen L Arnold"),
]

# A comma-separated list of custom stylesheets. Example:
pdf_stylesheets = ['pdf']

# Create a compressed PDF
# Use True/False or 1/0
# Example: compressed=True
#pdf_compressed = False

# A colon-separated list of folders to search for fonts. Example:
# pdf_font_path = ['/usr/share/fonts', '/usr/share/texmf-dist/fonts/']

# Language to be used for hyphenation support
#pdf_language = "en_US"

# Mode for literal blocks wider than the frame. Can be
# overflow, shrink or truncate
#pdf_fit_mode = "shrink"

# Section level that forces a break page.
# For example: 1 means top-level sections start in a new page
# 0 means disabled
pdf_break_level = 1

# When a section starts in a new page, force it to be 'even', 'odd',
# or just use 'any'
#pdf_breakside = 'any'

# Insert footnotes where they are defined instead of
# at the end.
#pdf_inline_footnotes = True

# verbosity level. 0 1 or 2
#pdf_verbosity = 0

# If false, no index is generated.
pdf_use_index = True

# If false, no modindex is generated.
pdf_use_modindex = True

# If false, no coverpage is generated.
pdf_use_coverpage = True

# Name of the cover page template to use
#pdf_cover_template = 'sphinxcover.tmpl'

# Documents to append as an appendix to all manuals.
#pdf_appendices = []

# Enable experimental feature to split table cells. Use it
# if you get "DelayedTable too big" errors
#pdf_splittables = False

# Set the default DPI for images
#pdf_default_dpi = 72

# Enable rst2pdf extension modules (default is empty list)
# you need vectorpdf for better sphinx's graphviz support
#pdf_extensions = ['vectorpdf']

# Page template name for "regular" pages
#pdf_page_template = 'cutePage'
