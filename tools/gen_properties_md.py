"""Генерирует references/builtin-properties.md — список встроенных свойств AC25,
сгруппированных по префиксу. Источник: живой API (GetAllPropertyNames).

Запуск (Archicad должен быть открыт): python tools/gen_properties_md.py
"""

import json
import urllib.request
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent.parent
OUT = HERE / "skills" / "archicad" / "references" / "builtin-properties.md"


def main() -> None:
    req = urllib.request.Request(
        "http://127.0.0.1:19723",
        data=json.dumps({"command": "API.GetAllPropertyNames"}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
    props = [
        p["nonLocalizedName"]
        for p in result["result"]["properties"]
        if p.get("type") == "BuiltIn"
    ]

    groups: dict[str, list[str]] = defaultdict(list)
    for name in props:
        prefix = name.split("_", 1)[0]
        groups[prefix].append(name)

    lines = [
        "# Встроенные свойства Archicad 25 (BuiltIn)",
        "",
        f"Всего: {len(props)}. Получено с живого Archicad 25 через"
        " `API.GetAllPropertyNames` (доступность зависит от типа элемента).",
        "",
        "Использование: `GetPropertyIds` с"
        ' `{"type": "BuiltIn", "nonLocalizedName": "<имя>"}`,'
        " затем `GetPropertyValuesOfElements`.",
        "",
        "Самые ходовые: `General_NetVolume` (объём), `General_Area` (площадь),"
        " `General_Height`, `General_ElementID`, `General_TypeName`,"
        " `General_HomeStoryName` (этаж), `Zone_ZoneName`, `Zone_CalculatedArea`,"
        " `Zone_NetArea`, `Zone_ZoneCategoryCode`.",
        "",
    ]
    for prefix in sorted(groups):
        names = sorted(groups[prefix])
        lines.append(f"## {prefix} ({len(names)})")
        lines.append("")
        for n in names:
            lines.append(f"- `{n}`")
        lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Свойств: {len(props)}; записано в {OUT}")


if __name__ == "__main__":
    main()
