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

selector_prefix : str = 'select_'

def get_selector(need: Dict[str, Any]) -> str:
    """
    Generate a selector string for a given need.
    """
    if "id" not in need:
        raise ValueError("Provided type is not a need element.")

    selector = selector_prefix + str(need["id"])
    if need.get("type", "") == "sn_type" and "directive" in need:
        selector = selector_prefix + str(need["directive"])
    return selector

schema_prefix : str = 'schema_'

def get_schema_name(need: Dict[str, Any]) -> str:
    """
    Generate a schema name string for a given need.
    """
    if "id" not in need:
        raise ValueError("Provided type is not a need element.")

    schema_name = schema_prefix + str(need["id"])
    return schema_name

def needs2defs_attributes(needs: Dict[str, Any]) -> Dict[str, Any]:
    dict_defs = {}
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
        dict_defs[attribute["id"]] = attribute_schema

    return dict_defs

def needs2defs_types_typegroups(needs: Dict[str, Any], need: Dict[str, Any]) -> Dict[str, Any]:

    if True:

        required = []
        properties = {}
        for mandatory in need.get("mandatory", []):
            if mandatory not in needs:
                continue
            properties[needs[mandatory]["name"]] = { "$ref": f"#/$defs/{mandatory}" }
            required.append(needs[mandatory]["name"])
        for optional in need.get("optional", []):
            if optional not in needs:
                continue
            properties[needs[optional]["name"]] = { "$ref": f"#/$defs/{optional}" }

        added_a_link = False
        # links from associations
        for child in need.get("parent_needs_back", []):
            if child not in needs:
                continue
            if not "sn_association" == needs[child]["type"]:
                continue
            association_need = needs[child]
            link = association_need.get("link", None)
            if not link or len(link) != 1 or link[0] not in needs:
                # todo: warn about missing link
                continue
            link_need = needs[link[0]]

            properties[link_need["option"]] = {
                "type": "array",
                "items": {"type": "string"}
            }
            added_a_link = True

        if added_a_link:
            properties["links"] = {
                "type": "array",
                "items": {"type": "string"}
            }

    dict_defs ={
        "properties": properties,
        "required": required,
    }
    return dict_defs

def needs2defs_types(needs: Dict[str, Any]) -> Dict[str, Any]:
    dict_defs = {}
    sn_types = list(filter(lambda need: need.get("type") == "sn_type", needs.values()))
    # add each sn_type to schema $defs
    for current_type in sn_types:
        # - def selector
        str_type = {
            "properties": {
                "type": { "const": f"{current_type['directive']}" },
            },
        }
        dict_defs[get_selector(current_type)] = str_type

        # - def type with extended properties
        dict_defs[current_type["id"]] = needs2defs_types_typegroups(needs, current_type)

    return dict_defs

def needs2defs_typegroups(needs: Dict[str, Any]) -> Dict[str, Any]:
    dict_defs = {}

    sn_typegroups = list(filter(lambda need: need.get("type") == "sn_typegroup", needs.values()))
    # add each sn_typegroup to schema $defs
    for typegroup in sn_typegroups:
        # - def selector
        list_anyOf = []
        for type in typegroup.get("groups_back", []):
            if type not in needs:
                continue
            list_anyOf.append({ "$ref": f"#/$defs/{get_selector(needs[type])}" })

        str_typegroup = {
            "anyOf": list_anyOf
        }
        dict_defs[get_selector(typegroup)] = str_typegroup

        # - def typegroup with extended properties
        dict_defs[typegroup["id"]] = needs2defs_types_typegroups(needs, typegroup)

    return dict_defs

def needs2defs(needs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert needs to schema definitions.
    """
    dict_defs = {}

    dict_defs |= needs2defs_attributes(needs)

    dict_defs |= needs2defs_types(needs)

    dict_defs |= needs2defs_typegroups(needs)

    return dict_defs

def needs2schemas_types(needs: Dict[str, Any]) -> List[Dict[str, Any]]:

    list_schemas = []

    sn_types = list(filter(lambda need: need.get("type") == "sn_type", needs.values()))
    for current_type in sn_types:
        selector = get_selector(current_type)

        # for the local validation, we do need the current type and all its groups
        allOf_list = [
            {
                "$ref": f"#/$defs/{current_type['id']}"
            }
        ]
        for group in current_type.get("groups", []):
            new_ref = { "$ref": f"#/$defs/{group}" }
            allOf_list.append(new_ref)

        validate_network = {}
        additional_added_links = []
        # for the network validation, we need to evaluate the associations
        for child in current_type.get("parent_needs_back", []):
            if child not in needs:
                continue
            if not "sn_association" == needs[child]["type"]:
                continue
            association_need = needs[child]
            link = association_need.get("link", None)
            if not link or len(link) != 1 or link[0] not in needs:
                continue

            link_need = needs[link[0]]

            targets = association_need.get("targets", [])
            if len(targets) == 0 or targets[0] not in needs:
                continue

            list_targets = []
            for t in targets:
                if t not in needs:
                    continue
                target_need = needs[t]
                if "type" in target_need and target_need["type"] == "sn_type":
                    list_targets.append(target_need["directive"])
                elif "type" in target_need and target_need["type"] == "sn_typegroup":
                    for group_type in target_need.get("groups_back", []):
                        if group_type not in needs:
                            continue
                        group_type_need = needs[group_type]
                        list_targets.append(group_type_need["directive"])

            local_list_of_types = {
                "properties": {
                    "type": {
                            "type": "string",
                            "enum": list_targets
                    }
                }
            }


            my_dict = {
                    "contains": {
                        "local": local_list_of_types
                    },
                    "minContains": 0
            }

            if link_need["option"] not in validate_network:
                validate_network[link_need["option"]] = my_dict
            else:
                additional_added_links.append((link_need["option"], my_dict))


        schema_entry = {
            "id": get_schema_name(current_type),
            "select": {
                "$ref": f"#/$defs/{selector}"
            },
            "validate": {
                "local": {
                    "allOf": allOf_list,
                    "unevaluatedProperties": False
                },
                "network": validate_network
            }
        }
        if not schema_entry["validate"]["network"]: # no network validations
            del schema_entry["validate"]["network"]
        list_schemas.append(schema_entry)

        if additional_added_links:
            for add_link in additional_added_links:
                new_schema_entry = schema_entry.copy()
                new_schema_entry["id"] = f"[{schema_entry['id']}]_with_additional_[{add_link[0]}]"
                # remove previous local validation to avoid duplication
                new_schema_entry["validate"] = {}
                new_schema_entry["validate"]["network"] = {}
                new_schema_entry["validate"]["network"][add_link[0]] = add_link[1]
                list_schemas.append(new_schema_entry)

    return list_schemas

def needs2schemas(needs: Dict[str, Any]) -> List[Dict[str, Any]]:

    list_schemas = []

    list_schemas += needs2schemas_types(needs)

    return list_schemas

def json2schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert JSON data to a schema representation.
    """
    needs = extract_needs_from_json(data)

    schema: Dict[str, Any] = {
        "$defs": needs2defs(needs),
        "schemas": needs2schemas(needs),
    }

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

