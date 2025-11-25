# usage:
# python ./scripts/json2conf.py -i ./use_datamodel/needs.json -o ./use_datamodel/output2.txt

"""
We read a JSON file containing configuration data following the in basic defined
metamodel and convert it into a sphinx-needs configuration format.
"""

import json
from pathlib import Path
import argparse
from typing import Any, Dict, List

from sphinx_needs.config import NeedType, NeedExtraOption, LinkOptionsType

from get_class_variables import typed_dict_fields

from dict2py import dict_to_dictcall, pyvalue_to_code

intendation : str = f"    "


def extract_needs_from_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract 'needs' section from the JSON data.
    """
    current_version = data.get("current_version", {})
    versions = data.get("versions", {})
    current_version_data = versions.get(current_version, {})
    needs = current_version_data.get("needs", {})
    return needs


def types2python(types: List[Dict[str, Any]]) -> List[str]:
    """
    Convert a list of types to a Python-compatible string representation.
    """

    inlude_keys: str = list(typed_dict_fields(NeedType).keys())
    #print("NeedType: " + str(inlude_keys))

    dicts_data = []
    for t in types:
        t_str = intendation
        if "id" in t and len(t["id"]) >= 1 and t["id"][0] == '#':
            t_str += f'# '
        t_str += dict_to_dictcall(t, include=inlude_keys) + ",\n"
        dicts_data.append(t_str)

    return_string = "needs_types = [\n" + "".join(dicts_data) + "]\n"

    #print("Generated needs_types:\n" + return_string)

    needs_types = [
        dict(directive="need", title="Need", prefix="N_", color="#9856a5", style="node")
    ]

    return return_string


def attributes2python(attributes: List[Dict[str, Any]]) -> str:
    """
    Convert a list of attributes to a Python-compatible string representation.
    """

    inlude_keys: str = list(typed_dict_fields(NeedExtraOption).keys())
    #print("NeedExtraOption: " + str(inlude_keys))

    dicts_data = []

    for a in attributes:
        a_str = intendation
        if "id" in a and len(a["id"]) >= 1 and a["id"][0] == '#':
            a_str += f'# '
        a_str += dict_to_dictcall(a, include=inlude_keys) + ",\n"
        dicts_data.append(a_str)

    needs_extra_options = [
        "my_extra_option",
    ]

    return_string = "needs_extra_options = [\n" + "".join(dicts_data) + "]\n"

    #print("Generated needs_extra_options:\n" + return_string)

    return return_string


def links2python(links: List[Dict[str, Any]]) -> str:
    """
    Convert a list of links to a Python-compatible string representation.
    """

    inlude_keys: str = list(typed_dict_fields(LinkOptionsType).keys())
    print("LinkOptionsType: " + str(inlude_keys))

    dicts_data = []

    for l in links:
        l_str = intendation
        if "id" in l and len(l["id"]) >= 1 and l["id"][0] == '#':
            l_str += f'# '
        l_str += dict_to_dictcall(l, include=inlude_keys) + ",\n"
        dicts_data.append(l_str)

    needs_extra_links = [
        dict(option = "checks", incoming = "is checked by", outgoing ="checks",),
    ]

    return_string =  "needs_extra_links = [\n"
    return_string += "".join(dicts_data)
    return_string += "]\n"

    print("Generated needs_extra_links:\n" + return_string)

    return return_string



def json_to_conf(data: Dict[str, Any]) -> str:
    """
    Convert a dictionary to a custom configuration format.
    """

    needs = extract_needs_from_json(data)

    types = needs.keys()
    sn_attributes = []
    sn_links = []

    for need in needs.values():
        print(need["id"] + ": " + need["type"])

    print("---- Filtering needs by type ----")

    # filter list of needs dict by type == "sn_type"
    sn_types = list(filter(lambda need: need.get("type") == "sn_type", needs.values()))
    for value in sn_types:
        print(value["id"] + " : " + value["type"])

    print("---- Filtering needs by option ----")

    sn_attributes = list(filter(lambda need: need.get("type") == "sn_option", needs.values()))
    for value in sn_attributes:
        print(value["id"] + " : " + value["type"])

    print("---- Filtering needs by link ----")

    sn_links = list(filter(lambda need: need.get("type") == "sn_link", needs.values()))
    for value in sn_links:
        print(value["id"] + " : " + value["type"])

    conf_lines = types2python(sn_types)
    conf_lines += "\n"

    conf_lines += attributes2python(sn_attributes)
    conf_lines += "\n"

    conf_lines += links2python(sn_links)
    conf_lines += "\n"

    return conf_lines

def json2schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert JSON data to a schema representation.
    """
    needs = extract_needs_from_json(data)

    schema: Dict[str, Any] = {
        "$defs": {},
        "schemas": [],
    }

    str_defs = {}

    sn_attributes = list(filter(lambda need: need.get("type") == "sn_option", needs.values()))
    # add each sn_attribute to schema $defs
    for attribute in sn_attributes:
        if "schema" not in attribute or not attribute["schema"]:
            attribute_schema = { "type": "string" }
        else:
            attribute_schema = json.loads(attribute["schema"])
        str_attribute = {
            "properties": {
                f"{attribute['name']}": attribute_schema
            }
        }
        str_defs[attribute["id"]] = str_attribute

    sn_types = list(filter(lambda need: need.get("type") == "sn_type", needs.values()))
    # add each sn_type to schema $defs
    for type in sn_types:
        #"required": ["type", "safety"]
        required = ["type"]
        properties = {}
        properties["type"] = { "const": f"{type['directive']}" },
        for mandatory in type.get("mandatory", []):
            if mandatory not in needs:
                continue
            properties[needs[mandatory]["name"]] = { "$ref": f"#/$defs/{mandatory}" }
            required.append(needs[mandatory]["name"])
        for optional in type.get("optional", []):
            if optional not in needs:
                continue
            properties.append({ "$ref": f"#/$defs/{optional}" })
        str_type = {
            "properties": {
                "type": { "const": f"{type['directive']}" },
                "safety": { "$ref": "#/$defs/OPTION__safety" },

            },
            "required": required,
            "unevaluatedProperties": False,
        }
        str_defs[type["id"]] = str_type

    sn_typegroups = list(filter(lambda need: need.get("type") == "sn_typegroup", needs.values()))
    # add each sn_typegroup to schema $defs
    for typegroup in sn_typegroups:
        list_oneOf = []
        for type in typegroup.get("groups_back", []):
            if type not in needs:
                continue
            list_oneOf.append({ "$ref": f"#/$defs/{type}" })

        str_typegroup = {
            "oneOf": list_oneOf
        }
        str_defs[typegroup["id"]] = str_typegroup

    schema["$defs"] = str_defs

    return schema

def main(input_path: Path, output_path: Path) -> None:
    """
    Main function to read JSON input and write configuration output.
    """
    # Read JSON data from input file
    with open(input_path, 'r') as infile:
        data = json.load(infile)

    # Convert JSON data to custom configuration format
    conf_data = json_to_conf(data)

    # Write the configuration data to output file
    with open(output_path, 'w') as outfile:
        outfile.write(conf_data)

    # Convert JSON data to schema
    schema = json2schema(data)

    # Write the schema data to output file
    schema_output_path = output_path.with_suffix('.schema.json')
    with open(schema_output_path, 'w') as schema_outfile:
        json.dump(schema, schema_outfile, indent=4)

if __name__ == "__main__":
      parser = argparse.ArgumentParser(description="Convert JSON to custom configuration format.")
      parser.add_argument("-i", "--input", help="Path to the input json file.", required=True, type=Path)
      parser.add_argument("-o", "--output", help="Path to the output json file.", required=True, type=Path)
      #parser.add_argument("input", help="Path to the input JSON file.")
      #parser.add_argument("output", help="Path to the output configuration file.")
      args = parser.parse_args()

      main(args.input, args.output)

