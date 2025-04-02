import os
import json
from functools import lru_cache
from typing import Dict, Any, Optional, Union
from config.settings import DEFAULT_LANGUAGE

# Змінна для зберігання поточної мови
CURRENT_LANGUAGE = DEFAULT_LANGUAGE

# Шлях до файла з текстами за замовчуванням
DEFAULT_TEXT_FILE: str = os.path.join("translation/locale", f"{DEFAULT_LANGUAGE}.json")

@lru_cache(maxsize=10)
def _load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Завантажує та кешує JSON-файл.

    Args:
        file_path: Шлях до JSON

    Returns:
        Dict зі вмістом JSON
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Помилка завантаження файлу {file_path}: {e}")
        return {}


def _get_nested_value(data: Dict[str, Any], key_path: str) -> Optional[str]:
    """
    Отримує значення з вкладеного словника за шляхом ключів.

    Args:
        data: Словник даних
        key_path: Шлях до ключа у форматі 'key1.key2.key3'

    Returns:
        Значення за вказаним шляхом або None, якщо шлях не існує
    """
    keys = key_path.split('.')
    current = data

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None

    return current if isinstance(current, str) else None


def set_language(language: str = None):
    """
    Ініціалізує модуль текстів з вказаною мовою.
    Якщо мова не вказана, використовується DEFAULT_LANGUAGE з налаштувань.

    Args:
        language: Код мови або шлях до JSON-файлу з локалізацією
    """
    global CURRENT_LANGUAGE
    CURRENT_LANGUAGE = language or DEFAULT_LANGUAGE


def localize_text(key_path: str, **kwargs: Union[str, int, float]) -> str:
    """
    Отримує текстове повідомлення за вказаним шляхом ключів,
    використовуючи поточну мову.

    Args:
        key_path: Шлях до повідомлення у форматі 'bot.button.next'
        **kwargs: Параметри для форматування тексту

    Returns:
        Текстове повідомлення або ключ
    """
    # Завантажуємо основний файл з текстами
    default_texts = _load_json_file(DEFAULT_TEXT_FILE)

    # Визначаємо шлях до файлу локалізації
    localized_file = None

    if CURRENT_LANGUAGE:
        if os.path.sep in CURRENT_LANGUAGE or CURRENT_LANGUAGE.endswith('.json'):
            # Якщо передано повний шлях або файл з розширенням .json
            localized_file = CURRENT_LANGUAGE \
                if os.path.isabs(CURRENT_LANGUAGE) \
                else os.path.join("translation/locale", CURRENT_LANGUAGE)
        else:
            # Якщо передано лише код мови
            localized_file = os.path.join("translation/locale", f"{CURRENT_LANGUAGE}.json")

    # Отримуємо текст з основного файлу
    default_text = _get_nested_value(default_texts, key_path)

    # Якщо вказано локалізацію, пробуємо отримати локалізований текст
    if localized_file:
        localized_texts = _load_json_file(localized_file)
        localized_res = _get_nested_value(localized_texts, key_path)

        # Повертаємо локалізований текст, якщо він існує
        if localized_res:
            try:
                return localized_res.format(**kwargs)
            except (KeyError, ValueError) as e:
                print(f"Помилка форматування тексту '{key_path}': {e}")
                return localized_res

    # Повертаємо текст за замовчуванням або сам ключ, якщо текст не знайдено
    return default_text or key_path