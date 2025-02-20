import json


def load_json(file_path):
    """Загружает JSON, если он существует, иначе возвращает пустой словарь."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def add_score(name, score):
    """Добавляет имя и очки в JSON-файл, если очков больше 0."""
    json_file = "data/score.json"
    if score == 0:
        return

    data = load_json(json_file)

    if not isinstance(data, list):
        data = []

    data.append({"name": name, "score": score})

    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
