"""PoC: работа с Archicad 25 через JSON API (http://127.0.0.1:19723).

Что делает:
1. Проверяет соединение (GetProductInfo).
2. Получает все элементы и считает их по типам.
3. Для стен считает суммарный объём через встроенное свойство General_Volume.
"""

import json
import urllib.request

API_URL = "http://127.0.0.1:19723"

# Типы элементов, поддерживаемые API Archicad 25
ELEMENT_TYPES = [
    "Wall", "Column", "Beam", "Window", "Door", "Object", "Lamp", "Slab",
    "Roof", "Mesh", "Zone", "CurtainWall", "Shell", "Skylight", "Morph",
    "Stair", "Railing", "Opening",
]


def ac_request(command: str, parameters: dict | None = None) -> dict:
    payload = {"command": command}
    if parameters is not None:
        payload["parameters"] = parameters
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    if not result.get("succeeded"):
        raise RuntimeError(f"{command} failed: {result.get('error')}")
    return result["result"]


def main() -> None:
    info = ac_request("API.GetProductInfo")
    print(f"Archicad {info['version']} build {info['buildNumber']} ({info['languageCode']})")

    elements = ac_request("API.GetAllElements")["elements"]
    print(f"Всего элементов: {len(elements)}")

    # В Archicad 25 нет GetTypesOfElements — запрашиваем по каждому типу отдельно
    by_type: dict[str, list] = {}
    for el_type in ELEMENT_TYPES:
        try:
            found = ac_request("API.GetElementsByType", {"elementType": el_type})["elements"]
        except RuntimeError:
            continue
        if found:
            by_type[el_type] = found

    print("\nЭлементы по типам:")
    for el_type, els in sorted(by_type.items(), key=lambda kv: -len(kv[1])):
        print(f"  {el_type:20s} {len(els)}")
    typed_total = sum(len(v) for v in by_type.values())
    print(f"  {'(прочие/2D)':20s} {len(elements) - typed_total}")

    # Объём стен через встроенное свойство (в AC25 — General_NetVolume)
    walls = by_type.get("Wall", [])
    if walls:
        volume_id = get_property_id("General_NetVolume")
        values = get_values(walls, [volume_id])
        total, ok = 0.0, 0
        for v in values:
            val = v.get("propertyValues", [{}])[0].get("propertyValue", {}).get("value")
            if isinstance(val, (int, float)):
                total += val
                ok += 1
        print(f"\nСтены: {len(walls)} шт., объём получен для {ok}")
        print(f"Суммарный объём стен: {total:.2f} м³")

    # Сводка по зонам: имя + расчётная площадь
    zones = by_type.get("Zone", [])
    if zones:
        name_id = get_property_id("Zone_ZoneName")
        area_id = get_property_id("Zone_CalculatedArea")
        values = get_values(zones, [name_id, area_id])
        area_by_name: dict[str, list[float]] = {}
        for v in values:
            pvs = v.get("propertyValues", [])
            if len(pvs) < 2:
                continue
            name = pvs[0].get("propertyValue", {}).get("value")
            area = pvs[1].get("propertyValue", {}).get("value")
            if isinstance(name, str) and isinstance(area, (int, float)):
                area_by_name.setdefault(name, []).append(area)
        print(f"\nЗоны: {len(zones)} шт. Топ-10 по суммарной площади:")
        top = sorted(area_by_name.items(), key=lambda kv: -sum(kv[1]))[:10]
        for name, areas in top:
            print(f"  {name:30s} {len(areas):5d} шт.  {sum(areas):10.1f} м²")


def get_property_id(non_localized_name: str) -> dict:
    prop = ac_request(
        "API.GetPropertyIds",
        {"properties": [{"type": "BuiltIn", "nonLocalizedName": non_localized_name}]},
    )["properties"][0]
    if "propertyId" not in prop:
        raise RuntimeError(f"Свойство {non_localized_name} не найдено: {prop}")
    return prop["propertyId"]


def get_values(elements: list, property_ids: list) -> list:
    return ac_request(
        "API.GetPropertyValuesOfElements",
        {
            "elements": elements,
            "properties": [{"propertyId": pid} for pid in property_ids],
        },
    )["propertyValuesForElements"]


if __name__ == "__main__":
    main()
