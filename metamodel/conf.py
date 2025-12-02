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

project = 'Metamodel'
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

#html_theme = 'sphinx_rtd_theme'
#html_theme = 'alabaster'
#html_theme = 'sphinx_immaterial'

html_css_files = ['custom.css']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# --  sphinxcontrib.plantuml configuration
local_plantuml_path = os.path.join(os.path.dirname(__file__), "..", "_tools", "plantuml.jar")
if on_rtd:
    plantuml = f"java -Djava.awt.headless=true -jar {local_plantuml_path}"
else:
    plantuml = f"java -jar {local_plantuml_path}"

print('plantuml path: ' + str(plantuml))

plantuml_output_format = 'svg'

# --  sphinx-needs configuration

needs_id_required = True
needs_id_length = 3
needs_id_regex = "^[A-Za-z0-9_]{5,}"
needs_build_json = True


# added by scripts: json2conf.py

needs_types = [
    dict(directive="sn_association", title="SN_ASSOCIATION", prefix="SN_ASSOCIATION__", color="#BFD8D2", style="node"),
    dict(directive="sn_link", title="SN_LINK", prefix="SN_LINK__", color="#BFD8D2", style="node"),
    dict(directive="sn_option", title="SN_OPTION", prefix="SN_OPTION__", color="#BFD8D2", style="node"),
    dict(directive="sn_type", title="SN_TYPE", prefix="SN_TYPE__", color="#BFD8D2", style="node"),
    dict(directive="sn_typegroup", title="SN_TYPEGROUP", prefix="SN_TYPEGROUP__", color="#BFD8D2", style="node"),
]

needs_extra_options = [
    {"name": "option",},
    {"name": "incoming",},
    {"name": "outgoing",},
    {"name": "copy",},
    {"name": "allow_dead_links",},
    # {"name": "#style",},
    {"name": "style_part",},
    {"name": "style_start",},
    {"name": "style_end",},
    {"name": "name",},
    {"name": "description",},
    {"name": "schema",},
    {"name": "directive",},
    # {"name": "#title",},
    {"name": "prefix",},
    {"name": "color",},
]

needs_extra_links = [
    dict(option = "targets", incoming = "targets_back", outgoing ="targets",),
    dict(option = "link", incoming = "link_back", outgoing ="link", schema={"maxItems": 1,},),
    dict(option = "optinal", incoming = "optinal_back", outgoing ="optinal",),
    dict(option = "mandatory", incoming = "mandatory_back", outgoing ="mandatory",),
    dict(option = "groups", incoming = "groups_back", outgoing ="groups",),
]


