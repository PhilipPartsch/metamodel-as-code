# metamodel-as-code

Here I do want to create a solution to model metamodels for sphinx-needs.

## Content

In the folder:
- scipts - Implementation of scripts to translate from needs.json to conf.py,
  project.toml and schema.json.
- use_datamodel - examples for the scripts developed in scipts folder
- docs - generic configuration for all sphinx builds
- public - root page for github pages.
- metamodel - an example metamodel
- test-project - a project which uses the defined metamodel

## typical commands

sphinx-build -b html ./metamodel ./public/metamodel

python ./scripts/json2conf.py -i ./use_datamodel/needs.json -o ./use_datamodel/output2.txt

sphinx-build -b html ./test-project ./public/test-project

