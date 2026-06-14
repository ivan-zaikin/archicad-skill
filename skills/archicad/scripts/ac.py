"""CLI-клиент JSON API Archicad (стандартная библиотека, без зависимостей).

Команды:
  python ac.py info                       — версия Archicad, проверка соединения
  python ac.py call <API.Команда> [JSON]  — произвольная команда; параметры —
                                            JSON-строкой, @файл или из stdin
  python ac.py types                      — количество элементов по типам
  python ac.py find-prop <подстрока>      — поиск встроенных свойств по имени
  python ac.py values <Тип> <Свойство,..> — значения встроенных свойств для всех
                                            элементов типа (JSON в stdout)
  python ac.py values-for <guid,..> <Свойство,..>
                                          — то же, но для конкретных GUID
                                            (список, @файл или - из stdin)

Примеры:
  python ac.py call API.GetAllElements
  python ac.py call API.GetElementsByType "{\"elementType\": \"Wall\"}"
  python ac.py find-prop Volume
  python ac.py values Wall General_NetVolume,General_Area > walls.json
  python ac.py values-for AAAA-...,BBBB-... General_Area,Construction_CompositeName

Выход всегда JSON (удобно для дальнейшей обработки). Код возврата 1 при ошибке.
"""

import json
import sys
import urllib.error
import urllib.request

API_URL = "http://127.0.0.1:19723"

ELEMENT_TYPES = [
    "Wall", "Column", "Beam", "Window", "Door", "Object", "Lamp", "Slab",
    "Roof", "Mesh", "Zone", "CurtainWall", "Shell", "Skylight", "Morph",
    "Stair", "Railing", "Opening",
]


def call(command: str, parameters: dict | None = None) -> dict:
    payload: dict = {"command": command}
    if parameters is not None:
        payload["parameters"] = parameters
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        fail(f"Archicad API недоступен ({e}). Archicad запущен?")
    if not result.get("succeeded"):
        fail(f"{command}: {json.dumps(result.get('error'), ensure_ascii=False)}")
    return result["result"]


def fail(message: str) -> None:
    print(json.dumps({"error": message}, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)


def out(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_info() -> None:
    out(call("API.GetProductInfo"))


def cmd_call(args: list[str]) -> None:
    if not args:
        fail("Укажите команду, например: ac.py call API.GetAllElements")
    command = args[0]
    parameters = None
    if len(args) > 1:
        raw = args[1]
        if raw.startswith("@"):
            raw = open(raw[1:], encoding="utf-8").read()
        elif raw == "-":
            raw = sys.stdin.read()
        parameters = json.loads(raw)
    out(call(command, parameters))


def cmd_types() -> None:
    counts = {}
    for el_type in ELEMENT_TYPES:
        elements = call("API.GetElementsByType", {"elementType": el_type})["elements"]
        if elements:
            counts[el_type] = len(elements)
    out(dict(sorted(counts.items(), key=lambda kv: -kv[1])))


def cmd_find_prop(args: list[str]) -> None:
    if not args:
        fail("Укажите подстроку, например: ac.py find-prop Volume")
    needle = args[0].lower()
    props = call("API.GetAllPropertyNames")["properties"]
    matches = sorted(
        p["nonLocalizedName"]
        for p in props
        if p.get("type") == "BuiltIn" and needle in p["nonLocalizedName"].lower()
    )
    out(matches)


def resolve_property_ids(names: list[str]) -> tuple[list[str], list[dict], list[str]]:
    """Распознаёт имена свойств без аварийного выхода.

    Возвращает (хорошие_имена, их_propertyId в том же порядке, плохие_имена).
    Удобно, когда часть имён может быть с опечаткой/неприменима — остальные
    всё равно обработаются.
    """
    result = call(
        "API.GetPropertyIds",
        {"properties": [{"type": "BuiltIn", "nonLocalizedName": n} for n in names]},
    )["properties"]
    good_names: list[str] = []
    ids: list[dict] = []
    bad: list[str] = []
    for name, item in zip(names, result):
        if "propertyId" in item:
            good_names.append(name)
            ids.append(item["propertyId"])
        else:
            bad.append(name)
    return good_names, ids, bad


def get_property_ids(names: list[str]) -> list[dict]:
    """Строгий вариант: при любом нераспознанном имени — выход, но с перечислением
    СРАЗУ ВСЕХ плохих имён (а не только первого). Порядок id совпадает с входным.
    """
    good_names, ids, bad = resolve_property_ids(names)
    if bad:
        fail(f"Свойства не найдены (проверь через find-prop): {', '.join(bad)}")
    return ids


def _rows_for(elements: list[dict], prop_names: list[str]) -> list[dict]:
    """Считывает свойства для заданных элементов в строки {guid, prop: value}.

    Нераспознанные имена пропускаются с предупреждением в stderr (а не валят
    весь запрос). Перечисления разворачиваются через unwrap().
    """
    good_names, prop_ids, bad = resolve_property_ids(prop_names)
    if bad:
        print(
            json.dumps(
                {"warning": f"Свойства пропущены (не найдены): {', '.join(bad)}"},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
    if not prop_ids:
        return [{"guid": e["elementId"]["guid"]} for e in elements]
    values = call(
        "API.GetPropertyValuesOfElements",
        {
            "elements": elements,
            "properties": [{"propertyId": pid} for pid in prop_ids],
        },
    )["propertyValuesForElements"]

    rows = []
    for element, value_set in zip(elements, values):
        row = {"guid": element["elementId"]["guid"]}
        for name, pv in zip(good_names, value_set.get("propertyValues", [])):
            row[name] = unwrap(pv.get("propertyValue", {}).get("value"))
        rows.append(row)
    return rows


def _read_guids(raw: str) -> list[str]:
    if raw.startswith("@"):
        raw = open(raw[1:], encoding="utf-8").read()
    elif raw == "-":
        raw = sys.stdin.read()
    return [g.strip() for g in raw.replace("\n", ",").split(",") if g.strip()]


def cmd_values(args: list[str]) -> None:
    if len(args) < 2:
        fail("Формат: ac.py values <Тип> <Свойство1,Свойство2,...>")
    el_type, prop_names = args[0], args[1].split(",")
    elements = call("API.GetElementsByType", {"elementType": el_type})["elements"]
    if not elements:
        out([])
        return
    out(_rows_for(elements, prop_names))


def cmd_values_for(args: list[str]) -> None:
    if len(args) < 2:
        fail(
            "Формат: ac.py values-for <guid,guid,...|@файл|-> <Свойство1,Свойство2,...>"
        )
    guids = _read_guids(args[0])
    prop_names = args[1].split(",")
    if not guids:
        fail("Укажите хотя бы один GUID")
    elements = [{"elementId": {"guid": g}} for g in guids]
    out(_rows_for(elements, prop_names))


def unwrap(value):
    # Перечисления приходят как {"type": "nonLocalizedValue", "nonLocalizedValue": ...}
    if isinstance(value, dict):
        return value.get("nonLocalizedValue", value.get("displayValue", value))
    if isinstance(value, list):
        return [unwrap(v) for v in value]
    return value


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd, args = sys.argv[1], sys.argv[2:]
    handlers = {
        "info": lambda: cmd_info(),
        "call": lambda: cmd_call(args),
        "types": lambda: cmd_types(),
        "find-prop": lambda: cmd_find_prop(args),
        "values": lambda: cmd_values(args),
        "values-for": lambda: cmd_values_for(args),
    }
    if cmd not in handlers:
        fail(f"Неизвестная команда: {cmd}. Доступно: {', '.join(handlers)}")
    handlers[cmd]()


if __name__ == "__main__":
    main()
