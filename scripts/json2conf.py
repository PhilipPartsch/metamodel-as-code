# usage:
# python ./scripts/json2conf.py -i ./use_datamodel/input.json -o ./use_datamodel/output.txt

"""
We read a JSON file containing configuration data and convert it into a custom
configuration format.
"""
import json
from pathlib import Path
import argparse
from typing import Any, Dict, List

def extract_needs_from_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract 'needs' section from the JSON data.
    """
    current_version = data.get("current_version", {})
    versions = data.get("versions", {})
    current_version_data = versions.get(current_version, {})
    needs = current_version_data.get("needs", {})
    return needs

def types2python(types: List[Any]) -> List[str]:
    """
    Convert a list of types to a Python-compatible string representation.
    """

    dicts_data = []
    for t in types:
        t_str = f'    dict(directive="{t}", title="{t}", prefix="{t}_", color="#BFD8D2", style="node"),\n'
        dicts_data.append(t_str)

    return_string = "needs_types = [\n" + "".join(dicts_data) + "]\n"

    needs_types = [dict(directive="req", title="Requirement", prefix="R_", color="#BFD8D2", style="node"),
               dict(directive="spec", title="Specification", prefix="S_", color="#FEDCD2", style="node"),
               dict(directive="impl", title="Implementation", prefix="I_", color="#DF744A", style="node"),
               dict(directive="test", title="Test Case", prefix="T_", color="#DCB239", style="node"),
               # Kept for backwards compatibility
               dict(directive="need", title="Need", prefix="N_", color="#9856a5", style="node")
           ]

    return return_string

def attributes2python(attributes: List[str]) -> str:
    """
    Convert a list of attributes to a Python-compatible string representation.
    """
    dicts_data = []
    for a in attributes:
        a_str = f'    "{a}",\n'
        dicts_data.append(a_str)


    needs_extra_options = [
        "my_extra_option",
    ]

    return_string = "needs_extra_options = [\n" + "".join(dicts_data) + "]\n"

    return return_string

def links2python(links: List[str]) -> str:
    """
    Convert a list of links to a Python-compatible string representation.
    """
    dicts_data = []
    for l in links:
        l_str = f'    dict(option = "{l}", incoming = "{l}_back", outgoing ="{l}",),\n'
        dicts_data.append(l_str)

    needs_extra_links = [
        dict(option = "checks", incoming = "is checked by", outgoing ="checks",),
    ]

    return_string =  "needs_extra_options = [\n"
    return_string += "".join(dicts_data)
    return_string += "]\n"

    return return_string



def json_to_conf(data: Dict[str, Any]) -> str:
    """
    Convert a dictionary to a custom configuration format.
    """

    needs = extract_needs_from_json(data)

    types = needs.keys()
    sn_attributes = []
    sn_links = []

    for key, value in needs.items():
        if isinstance(value, dict):
            if value["sn_attributes"]:
                if isinstance(value["sn_attributes"], list):
                    for l in value["sn_attributes"]:
                        sn_attributes.append(l)
                else:
                    sn_attributes.append(value["sn_attributes"])
            if value["sn_links"]:
                if isinstance(value["sn_links"], list):
                    for l in value["sn_links"]:
                        sn_links.append(l)
                else:
                    sn_links.append(value["sn_links"])

    conf_lines = types2python(types)
    conf_lines += "\n"

    conf_lines += attributes2python(sn_attributes)
    conf_lines += "\n"

    conf_lines += links2python(sn_links)
    conf_lines += "\n"

    #conf_lines.append(sn_attributes)
    #conf_lines.append(sn_links)

    return conf_lines

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

if __name__ == "__main__":
      parser = argparse.ArgumentParser(description="Convert JSON to custom configuration format.")
      parser.add_argument("-i", "--input", help="Path to the input json file.", required=True, type=Path)
      parser.add_argument("-o", "--output", help="Path to the output json file.", required=True, type=Path)
      #parser.add_argument("input", help="Path to the input JSON file.")
      #parser.add_argument("output", help="Path to the output configuration file.")
      args = parser.parse_args()

      main(args.input, args.output)

