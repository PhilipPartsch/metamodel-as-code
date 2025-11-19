# Configuration file for the Sphinx documentation builder.

import os
import datetime

# -- Print Versions

import sys
print ('python version: ' + str(sys.version))

from sphinx import __version__ as sphinx_version
print ('sphinx version: ' + str(sphinx_version))

from sphinx_needs import __version__ as sphinx_needs_version
print ('sphinx-needs version: ' + str(sphinx_needs_version))

sys.path.append(os.path.abspath('.'))

# -- Project information

import datetime

currentDateTime = datetime.datetime.now()
date = currentDateTime.date()

project = 'Definition of Basic Types'
copyright = f'2025 - {date.year}, PhilipPartsch'
author = 'PhilipPartsch'

release = '1.0'
version = '1.0.0'

# -- General configuration
on_rtd = os.environ.get("READTHEDOCS") == "True"

extensions = [
    'sphinx_needs',
    'sphinxcontrib.plantuml',
]

exclude_patterns = ['_tools/*',]

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
#html_theme = 'alabaster'
#html_theme = 'sphinx_immaterial'

html_css_files = ['custom.css']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# --  sphinxcontrib.plantuml configuration
#local_plantuml_path = os.path.join(os.path.dirname(__file__), "_tools", "plantuml.jar")

# --  sphinx-needs configuration

needs_id_required = true
needs_id_length = 3
needs_id_regex = "^[A-Za-z0-9_]{5,}"
needs_build_json = true
