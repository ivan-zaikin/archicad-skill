"""Генерирует справочник команд AC25 (references/commands.md) из официального
пакета archicad (releases/ac25/b3000commands.py) — это авторитетный источник
сигнатур именно для Archicad 25.

Запуск: python tools/gen_commands_md.py
"""

import ast
import json
import re
import textwrap
from pathlib import Path

import archicad.releases.ac25.b3000commands as cmds_module
import archicad.releases.ac25.b3000types as types_module

HERE = Path(__file__).parent.parent
OUT = HERE / "skills" / "archicad" / "references" / "commands.md"

CATEGORIES = {
    "Базовые": ["IsAlive", "GetProductInfo"],
    "Элементы": ["GetAllElements", "GetElementsByType", "GetElementsByClassification",
                 "GetElementsRelatedToZones", "Get2DBoundingBoxes", "Get3DBoundingBoxes"],
    "Свойства": ["GetPropertyIds", "GetAllPropertyNames", "GetDetailsOfProperties",
                 "GetPropertyValuesOfElements", "SetPropertyValuesOfElements"],
    "Компоненты (слои конструкций)": ["GetComponentsOfElements", "GetPropertyValuesOfElementComponents"],
    "Классификации": ["GetAllClassificationSystems", "GetAllClassificationsInSystem",
                      "GetDetailsOfClassificationItems", "GetClassificationsOfElements",
                      "SetClassificationsOfElements"],
    "Атрибуты": ["GetAttributesByType", "GetActivePenTables", "GetBuildingMaterialAttributes",
                 "GetCompositeAttributes", "GetFillAttributes", "GetLayerAttributes",
                 "GetLayerCombinationAttributes", "GetLineAttributes", "GetPenTableAttributes",
                 "GetProfileAttributes", "GetProfileAttributePreview", "GetSurfaceAttributes",
                 "GetZoneCategoryAttributes"],
    "Навигатор и макеты": ["GetNavigatorItemTree", "GetPublisherSetNames", "RenameNavigatorItem",
                           "MoveNavigatorItem", "DeleteNavigatorItems", "CloneProjectMapItemToViewMap",
                           "CreateViewMapFolder", "CreateLayout", "CreateLayoutSubset",
                           "GetLayoutSettings", "SetLayoutSettings"],
    "Команды аддонов": ["ExecuteAddOnCommand", "IsAddOnCommandAvailable"],
}


def parse_methods(path: Path) -> dict[str, dict]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    commands_cls = next(
        n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Commands"
    )
    out = {}
    for node in commands_cls.body:
        if not isinstance(node, ast.FunctionDef) or node.name.startswith("_"):
            continue
        doc = ast.get_docstring(node) or ""
        args = []
        for a in node.args.args[1:]:  # пропускаем self
            ann = ast.unparse(a.annotation) if a.annotation else "Any"
            args.append((a.arg, ann))
        ret = ast.unparse(node.returns) if node.returns else "None"
        out[node.name] = {"doc": doc, "args": args, "returns": ret}
    return out


def parse_type_docs(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docs = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node) or ""
            docs[node.name] = doc.split("\n")[0]
    return docs


def first_line(doc: str) -> str:
    return doc.split("\n")[0].strip() if doc else ""


def clean_type(ann: str) -> str:
    return re.sub(r"\bOptional\[(.+)\]", r"\1 (опционально)", ann)


def main() -> None:
    methods = parse_methods(Path(cmds_module.__file__))
    type_docs = parse_type_docs(Path(types_module.__file__))

    categorized = {name for names in CATEGORIES.values() for name in names}
    uncategorized = sorted(set(methods) - categorized)
    if uncategorized:
        CATEGORIES["Прочее"] = uncategorized

    lines = [
        "# Справочник команд JSON API — Archicad 25 (build 3000+)",
        "",
        "Сгенерировано из официального Python-пакета `archicad` (releases/ac25).",
        "Все запросы: `POST http://127.0.0.1:19723` с телом"
        ' `{"command": "API.<Имя>", "parameters": {...}}`.',
        "Ответ: `{\"succeeded\": true, \"result\": {...}}` либо"
        " `{\"succeeded\": false, \"error\": {\"code\": N, \"message\": ...}}`.",
        "",
        "## Ключевые JSON-структуры",
        "",
        "Команды принимают/возвращают обёртки — частая причина ошибки 4002"
        " (Invalid command parameters):",
        "",
        "```jsonc",
        "// ElementIdArrayItem — элемент списка elements",
        '{ "elementId": { "guid": "..." } }',
        "",
        "// PropertyIdArrayItem — элемент списка properties в Get/SetPropertyValuesOfElements",
        '{ "propertyId": { "guid": "..." } }',
        "",
        "// PropertyUserId — вход GetPropertyIds (BuiltIn или UserDefined)",
        '{ "type": "BuiltIn", "nonLocalizedName": "General_NetVolume" }',
        '{ "type": "UserDefined", "localizedName": ["Группа", "Имя свойства"] }',
        "",
        "// PropertyValuesOrError — ответ GetPropertyValuesOfElements (на каждый элемент)",
        '{ "propertyValues": [ { "propertyValue": { "value": 1.23, "type": "number",'
        ' "status": "normal" } } ] }',
        "",
        "// ClassificationSystemId / ClassificationItemId",
        '{ "guid": "..." }',
        "```",
        "",
        "## Оглавление",
        "",
    ]
    for cat, names in CATEGORIES.items():
        present = [n for n in names if n in methods]
        if not present:
            continue
        lines.append(f"- **{cat}**: " + ", ".join(f"`{n}`" for n in present))
    lines.append("")

    for cat, names in CATEGORIES.items():
        present = [n for n in names if n in methods]
        if not present:
            continue
        lines.append(f"## {cat}")
        lines.append("")
        for name in present:
            m = methods[name]
            lines.append(f"### API.{name}")
            lines.append("")
            desc = first_line(m["doc"])
            if desc:
                lines.append(desc)
                lines.append("")
            if m["args"]:
                lines.append("Параметры:")
                for arg, ann in m["args"]:
                    t = clean_type(ann)
                    base = re.sub(r"List\[|\]|\s|\(опционально\)", "", t)
                    hint = type_docs.get(base, "")
                    if hint.upper() == "EMPTY STRING":
                        hint = ""
                    suffix = f" — {hint}" if hint else ""
                    lines.append(f"- `{arg}`: {t}{suffix}")
            else:
                lines.append("Параметры: нет.")
            lines.append("")
            lines.append(f"Возвращает: `{m['returns']}`")
            lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Команд: {len(methods)}; записано в {OUT}")


if __name__ == "__main__":
    main()
