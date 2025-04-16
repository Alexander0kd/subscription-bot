import os
import json
from functools import lru_cache
from typing import Dict, Any, Optional, Union
from config import DEFAULT_LANGUAGE

CURRENT_LANGUAGE = DEFAULT_LANGUAGE

DEFAULT_TEXT_FILE: str = os.path.join("translation/locale", f"{DEFAULT_LANGUAGE}.json")

@lru_cache(maxsize=10)
def _load_json_file(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Помилка завантаження файлу {file_path}: {e}")
        return {}


def _get_nested_value(data: Dict[str, Any], key_path: str) -> Optional[str]:
    keys = key_path.split('.')
    current = data

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None

    return current if isinstance(current, str) else None


def set_language(language: str = None):
    global CURRENT_LANGUAGE
    CURRENT_LANGUAGE = language or DEFAULT_LANGUAGE


def localize_text(key_path: str, **kwargs: Union[str, int, float]) -> str:
    default_texts = _load_json_file(DEFAULT_TEXT_FILE)

    localized_file = None

    if CURRENT_LANGUAGE:
        if os.path.sep in CURRENT_LANGUAGE or CURRENT_LANGUAGE.endswith('.json'):
            localized_file = CURRENT_LANGUAGE \
                if os.path.isabs(CURRENT_LANGUAGE) \
                else os.path.join("translation/locale", CURRENT_LANGUAGE)
        else:
            localized_file = os.path.join("translation/locale", f"{CURRENT_LANGUAGE}.json")

    default_text = _get_nested_value(default_texts, key_path)

    if localized_file:
        localized_texts = _load_json_file(localized_file)
        localized_res = _get_nested_value(localized_texts, key_path)

        if localized_res:
            try:
                return localized_res.format(**kwargs)
            except (KeyError, ValueError) as e:
                print(f"Помилка форматування тексту '{key_path}': {e}")
                return localized_res

    return default_text or key_path