import random

def get_value_by_key (value: str, dict: dict) -> str:
    for key in dict:
        if dict[key] == int(value):
            break
    return key
