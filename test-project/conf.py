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

project = 'Test-Project'
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

needs_schema_definitions_from_json = "output2.schema.json"

# added by scripts: json2conf.py

needs_types = [
    dict(directive='aou', title='Assumption of Use', prefix='AOU__', color='#FF0000', style='node'),
    dict(directive='asreq', title='assumed requirement', prefix='ASREQ__', color='#FFA500', style='node'),
    dict(directive='datatype', title='Datatype', prefix='DATATYPE__', color='#FFA500', style='node'),
    dict(directive='unit', title='Port', prefix='PORT__', color='#FFA500', style='node'),
    dict(directive='sw_arch_dec', title='Software Architecture Decision', prefix='ARCH_DEC__', color='#FFA500', style='node'),
    dict(directive='sw_arch_dia', title='Software Architecture Diagram', prefix='ARCH_DIA__', color='#FFA500', style='node'),
    dict(directive='swreq', title='sw requirement', prefix='SWREQ__', color='#FFA500', style='node'),
    dict(directive='sysreq', title='sys requirement', prefix='SYSREQ__', color='#FFA500', style='node'),
    dict(directive='test_specification', title='test_specification', prefix='TESTSPEC__', color='#00FF00', style='node'),
    dict(directive='arch_unit', title='Unit', prefix='UNIT__', color='#FFA500', style='node'),
]

needs_extra_options2 = [
    dict(name='safety', description='safety level', schema={"type": "string", "enum": ["QM", "ASIL-A", "ASIL-B", "ASIL-C", "ASIL-D"]}),
]

needs_extra_options = [
    dict(name='safety', description='safety level', ),
    dict(name='safety2', description='safety level', ),
]

needs_extra_links = [
    dict(option='covered_by', incoming='covers', outgoing='covered by', copy=True, color='#000000', style='#000000', style_part='#000000', style_start='-', style_end='->', allow_dead_links=False),
    dict(option='covers', incoming='covered by', outgoing='covers', copy=True, color='#000000', style='#000000', style_part='#000000', style_start='-', style_end='->', allow_dead_links=False),
    dict(option='satisfies', incoming='satisfied by', outgoing='satisfies', copy=True, color='#000000', style='#000000', style_part='#000000', style_start='-', style_end='->', allow_dead_links=False),
    dict(option='verifies', incoming='verified by', outgoing='verifies', copy=True, color='#000000', style='#000000', style_part='#000000', style_start='-', style_end='->', allow_dead_links=False),
]

