from typing import Any, List
import json

def pyvalue_to_code(value: Any) -> str:
    """
    Wandelt beliebige Python-Werte in Python-Code um.
    """
    if isinstance(value, str):
        return repr(value) # saubere String-Escapes
    if isinstance(value, (int, float, bool)) or value is None:
        return repr(value)
    if isinstance(value, dict):
        return dict_to_dictcall(value, all=True)
    if isinstance(value, (list, tuple, set)):
        open_, close_ = {
            list: ("[", "]"),
            tuple: ("(", ")"),
            set: ("{", "}")
        }[type(value)]
        inner = ", ".join(pyvalue_to_code(v) for v in value)
        # Sonderfall: 1-Element-Tuple → (x,)
        if isinstance(value, tuple) and len(value) == 1:
            inner += ","
        return f"{open_}{inner}{close_}"
    # Fallback für unbekannte Typen (z.B. eigene Klassen)
    return repr(value)


def dict_to_dictcall(d: dict, include: List[str]=[], all: bool=False)-> str:
    """
    Konvertiert ein dict in einen dict(...)-String.
    include = Menge/Liste von Keys, die gerneriert werden sollen.
    """
    include = (include or [])
    if all:
        include = list(d.keys())
    parts = []

    for k in include:
        if k not in d:
            continue

        if k == "schema":
            if len(str(d[k])) == 0:
                continue
            elif d[k][0] == '{':
                # Handle schema as a json string
                schema_dict = json.loads(d[k])
                value_code = pyvalue_to_code(schema_dict)
            else:
                value_code = pyvalue_to_code(d[k])
        else:
            value_code = pyvalue_to_code(d[k])

        parts.append(f"{k}={value_code}")

    return f"dict({', '.join(parts)})"
