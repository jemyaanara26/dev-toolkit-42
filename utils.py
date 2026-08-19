import json
from typing import Any, Dict, List, Union

def load_json(file_path: str) -> Union[Dict[str, Any], List[Any]]:
    with open(file_path, 'r') as f:
        return json.load(f)


def save_json(data: Union[Dict[str, Any], List[Any]], file_path: str) -> None:
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict1.copy()  
    merged.update(dict2)  
    return merged


def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    return [item for sublist in nested_list for item in sublist]


def unique_elements(seq: List[Any]) -> List[Any]:
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]
