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
  python ac.py stories                    — список этажей из отметок стен
                                            (elevation м, wall_count, story №)
  python ac.py validate-zones             — кросс-проверка зон: NetArea vs
                                            CalculatedArea; предупреждение >1%
  python ac.py zone-geometry              — зоны + bounding box геометрия:
                                            bbox_area, fill_ratio, height_mismatch

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


def cmd_stories() -> None:
    """Список этажей из отметок стен: elevation (м от нуля проекта), wall_count, story."""
    elements = call("API.GetElementsByType", {"elementType": "Wall"})["elements"]
    if not elements:
        fail("Стены не найдены — невозможно определить этажи")
    rows = _rows_for(elements, [
        "General_BottomElevationToProjectZero",
        "General_BottomElevationToHomeStory",
    ])
    counts: dict[float, int] = {}
    for row in rows:
        z_proj = row.get("General_BottomElevationToProjectZero")
        z_home = row.get("General_BottomElevationToHomeStory")
        if z_proj is None or z_home is None:
            continue
        elev = round(z_proj - z_home, 2)
        counts[elev] = counts.get(elev, 0) + 1
    stories = sorted(counts.items())
    out([{"story": i + 1, "elevation": e, "wall_count": c}
         for i, (e, c) in enumerate(stories)])


def cmd_zone_geometry() -> None:
    """Зоны + геометрия из bounding boxes: bbox_area, fill_ratio, height cross-check."""
    zones = call("API.GetElementsByType", {"elementType": "Zone"})["elements"]
    if not zones:
        out([])
        return
    rows = _rows_for(zones, [
        "Zone_ZoneName", "Zone_ZoneNumber",
        "Zone_NetArea", "Zone_CalculatedArea",
        "Zone_WallsSurfaceArea",
        "General_Height",
        "General_BottomElevationToProjectZero",
    ])
    bb2d = call("API.Get2DBoundingBoxes", {"elements": zones})["boundingBoxes2D"]
    bb3d = call("API.Get3DBoundingBoxes", {"elements": zones})["boundingBoxes3D"]

    results = []
    for row, b2, b3 in zip(rows, bb2d, bb3d):
        entry = dict(row)
        if "boundingBox2D" in b2:
            box = b2["boundingBox2D"]
            w = box["xMax"] - box["xMin"]
            d = box["yMax"] - box["yMin"]
            bbox_area = round(w * d, 4)
            entry["bbox_area"] = bbox_area
            net = row.get("Zone_NetArea") or 0
            if net > 0 and bbox_area > 0:
                fill = round(net / bbox_area, 3)
                entry["fill_ratio"] = fill
                if net > bbox_area * 1.05:
                    entry["warning"] = "Zone_NetArea > bbox — зона не пересчитана"
                elif fill < 0.35:
                    entry["note"] = "fill_ratio<0.35 — нестандартная форма или зона смещена"
        if "boundingBox3D" in b3:
            box3 = b3["boundingBox3D"]
            bbox_h = round(box3["zMax"] - box3["zMin"], 3)
            entry["bbox_height"] = bbox_h
            prop_h = row.get("General_Height") or 0
            if prop_h > 0 and abs(bbox_h - prop_h) > 0.05:
                entry["height_mismatch"] = {
                    "General_Height": round(prop_h, 3),
                    "bbox_height": bbox_h,
                    "diff": round(abs(bbox_h - prop_h), 3),
                }
        results.append(entry)
    out(results)


def cmd_validate_zones() -> None:
    """Валидация зон: NetArea vs CalculatedArea; предупреждение при расхождении >1%."""
    elements = call("API.GetElementsByType", {"elementType": "Zone"})["elements"]
    if not elements:
        out({"ok": True, "zones_checked": 0})
        return
    rows = _rows_for(elements, [
        "Zone_ZoneName", "Zone_ZoneNumber",
        "Zone_NetArea", "Zone_CalculatedArea", "Zone_WallsSurfaceArea",
    ])
    issues = []
    for row in rows:
        net = row.get("Zone_NetArea") or 0
        calc = row.get("Zone_CalculatedArea") or 0
        if net > 0 and calc > 0 and abs(net - calc) / net > 0.01:
            issues.append({
                "guid": row["guid"],
                "name": row.get("Zone_ZoneName"),
                "number": row.get("Zone_ZoneNumber"),
                "Zone_NetArea": round(net, 4),
                "Zone_CalculatedArea": round(calc, 4),
                "diff_pct": round(abs(net - calc) / net * 100, 1),
            })
    result: dict = {"zones_checked": len(rows), "issues_count": len(issues)}
    if issues:
        result["warning"] = "Пересчитайте зоны: Документ → Обновить/Перегенерировать → Зоны"
        result["zones_with_issues"] = issues
    else:
        result["ok"] = True
    out(result)


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
        "stories": lambda: cmd_stories(),
        "validate-zones": lambda: cmd_validate_zones(),
        "zone-geometry": lambda: cmd_zone_geometry(),
    }
    if cmd not in handlers:
        fail(f"Неизвестная команда: {cmd}. Доступно: {', '.join(handlers)}")
    handlers[cmd]()


if __name__ == "__main__":
    main()
