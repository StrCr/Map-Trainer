import json
import os
import sys
from pathlib import Path


def get_user_data_path(filename):
    """Возвращает путь к файлу в папке пользователя."""
    user_data_dir = Path.home() / ".map_trainer"
    user_data_dir.mkdir(exist_ok=True)
    file_path = user_data_dir / filename

    if not file_path.exists():
        original_path = resource_path(f"data/{filename}")
        if os.path.exists(original_path):
            with open(original_path, "r", encoding="utf-8") as src, \
                 open(file_path, "w", encoding="utf-8") as dst:
                dst.write(src.read())

    return str(file_path)


def resource_path(relative_path):
    """Получите абсолютный путь к ресурсу, работает для dev and и для PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_json(file_path):
    """Загружает JSON, если он существует, иначе возвращает пустой список."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def add_score(file_path, name, score):
    """Добавляет имя и очки в JSON-файл, если очков больше 0."""
    if score == 0:
        return

    data = load_json(file_path)

    if not isinstance(data, list):
        data = []

    data.append({"name": name, "score": score})

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
