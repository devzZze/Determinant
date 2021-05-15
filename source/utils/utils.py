import json


def get_keyboard(filename: str) -> json:
    return json.dumps(json.loads(open(f'source/keyboards/{filename}.json', 'r', encoding='UTF-8').read()))
