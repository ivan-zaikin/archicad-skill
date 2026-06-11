"""Зондирование: какие JSON API команды поддерживает запущенный Archicad.

Полезно при первом подключении к новой версии/сборке Archicad: документация
Graphisoft описывает только последнюю версию API, а реальный набор команд
зависит от установленной сборки. Код ошибки 2002 = команды нет,
любой другой ответ = команда существует.

Запуск: python probe_commands.py [выходной.json]
"""

import json
import sys
import urllib.request
from pathlib import Path

API_URL = "http://127.0.0.1:19723"

# Полный список команд из документации API (версия 29, 2026 г.)
ALL_KNOWN_COMMANDS = [
    "API.ExecuteAddOnCommand", "API.IsAddOnCommandAvailable",
    "API.CreateAttributeFolders", "API.DeleteAttributeFolders",
    "API.DeleteAttributes", "API.GetActivePenTables", "API.GetAttributeFolders",
    "API.GetAttributeFolderStructure", "API.GetAttributesIndices",
    "API.GetAttributesByType", "API.GetBuildingMaterialAttributes",
    "API.GetCompositeAttributes", "API.GetFillAttributes",
    "API.GetLayerAttributes", "API.GetLayerCombinationAttributes",
    "API.GetLineAttributes", "API.GetPenTableAttributes",
    "API.GetProfileAttributes", "API.GetProfileAttributePreview",
    "API.GetSurfaceAttributes", "API.GetZoneCategoryAttributes",
    "API.MoveAttributesAndFolders", "API.RenameAttributeFolders",
    "API.IsAlive", "API.GetProductInfo",
    "API.GetAllElements", "API.GetSelectedElements", "API.GetElementsByType",
    "API.GetTypesOfElements", "API.GetElementsByClassification",
    "API.GetAllClassificationSystems", "API.GetClassificationSystemIds",
    "API.GetClassificationSystems", "API.GetAllClassificationsInSystem",
    "API.GetDetailsOfClassificationItems", "API.GetClassificationItemAvailability",
    "API.GetClassificationsOfElements", "API.SetClassificationsOfElements",
    "API.GetPropertyIds", "API.GetAllPropertyIds", "API.GetAllPropertyNames",
    "API.GetDetailsOfProperties", "API.GetPropertyDefinitionAvailability",
    "API.GetPropertyGroups", "API.GetAllPropertyGroupIds",
    "API.GetPropertyValuesOfElements", "API.GetAllPropertyIdsOfElements",
    "API.SetPropertyValuesOfElements",
    "API.GetPublisherSetNames", "API.GetNavigatorItemsType",
    "API.GetNavigatorItemTree", "API.DeleteNavigatorItems",
    "API.RenameNavigatorItem", "API.MoveNavigatorItem",
    "API.GetBuiltInContainerNavigatorItems", "API.GetElevationNavigatorItems",
    "API.GetInteriorElevationNavigatorItems", "API.GetDetailNavigatorItems",
    "API.GetWorksheetNavigatorItems", "API.GetSectionNavigatorItems",
    "API.GetStoryNavigatorItems", "API.GetDocument3DNavigatorItems",
    "API.CloneProjectMapItemToViewMap", "API.CreateViewMapFolder",
    "API.CreateLayoutSubset", "API.GetLayoutSettings", "API.CreateLayout",
    "API.SetLayoutSettings",
    "API.Get2DBoundingBoxes", "API.Get3DBoundingBoxes",
    "API.GetElementsRelatedToZones",
    "API.GetComponentsOfElements", "API.GetPropertyValuesOfElementComponents",
]


def call(command: str) -> dict:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({"command": command}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main() -> None:
    supported, missing = [], []
    for cmd in ALL_KNOWN_COMMANDS:
        r = call(cmd)
        if not r.get("succeeded") and r.get("error", {}).get("code") == 2002:
            missing.append(cmd)
        else:
            supported.append(cmd)

    info = call("API.GetProductInfo")["result"]
    print(f"Archicad {info['version']} build {info['buildNumber']}")
    print(f"Поддерживается: {len(supported)}, отсутствует: {len(missing)}")
    for c in missing:
        print(f"  - {c}")

    out_path = Path(sys.argv[1] if len(sys.argv) > 1 else "supported_commands.json")
    out_path.write_text(
        json.dumps(
            {"productInfo": info, "supported": supported, "missing": missing},
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Сохранено в {out_path}")


if __name__ == "__main__":
    main()
