# Рецепты: типовые задачи через JSON API Archicad 25

Все примеры — через `scripts/ac.py` (или `from ac import call`).
Проверено на Archicad 25 build 5010.

## Экспликация помещений (зоны)

```bash
python scripts/ac.py values Zone Zone_ZoneName,Zone_ZoneNumber,Zone_CalculatedArea,General_HomeStoryName > zones.json
```

Затем агрегируй: группировка по имени/этажу, сумма площадей. Полезные свойства:
`Zone_NetArea`, `Zone_ReducedArea`, `Zone_ZoneCategoryCode`,
`Zone_WallsSurfaceArea` (площадь стен зоны — для отделки).

## Ведомость объёмов (стены, перекрытия, колонны...)

```bash
python scripts/ac.py values Wall General_NetVolume,General_Area,General_HomeStoryName > walls.json
python scripts/ac.py values Slab General_NetVolume,General_NetTopSurfaceArea > slabs.json
```

`General_NetVolume` — чистый объём (с вычетом проёмов), `General_GrossVolume` —
брутто. Для расчёта бетона/кладки обычно нужен Net.

## Окна и двери (спецификация)

```bash
python scripts/ac.py values Window General_ElementID,WindowDoor_Width,WindowDoor_Height,General_HomeStoryName > windows.json
```

Размеры в метрах. Группируй по (ширина, высота) или по `General_ElementID`
для маркировки. Двери — тип `Door`, те же свойства WindowDoor_*.

## Состав конструкций (слои многослойных стен)

`GetComponentsOfElements` возвращает компоненты (слои) элементов,
`GetPropertyValuesOfElementComponents` — их свойства (например, объём
каждого слоя — для раздельного подсчёта утеплителя и кладки):

```bash
python scripts/ac.py call API.GetComponentsOfElements @elements.json
```

где elements.json: `{"elements": [{"elementId": {"guid": "..."}}, ...]}`.
Компонент адресуется парой guid элемента + guid компонента
(`{"elementComponentId": {"elementGuid": ..., "componentGuid": ...}}`).

## Какие элементы в какой зоне

```bash
python scripts/ac.py call API.GetElementsRelatedToZones "{\"zones\": [{\"elementId\": {\"guid\": \"...\"}}], \"elementTypes\": [\"Wall\", \"Door\"]}"
```

## Классификации

```bash
# Системы классификации в проекте
python scripts/ac.py call API.GetAllClassificationSystems
# Дерево позиций системы
python scripts/ac.py call API.GetAllClassificationsInSystem "{\"classificationSystemId\": {\"guid\": \"...\"}}"
# Элементы с данной позицией классификации
python scripts/ac.py call API.GetElementsByClassification "{\"classificationItemId\": {\"guid\": \"...\"}}"
# Классификация конкретных элементов
python scripts/ac.py call API.GetClassificationsOfElements @params.json
```

## Пользовательские свойства

`values` работает со встроенными (BuiltIn). Для пользовательских свойств
вызывай `GetPropertyIds` с
`{"type": "UserDefined", "localizedName": ["Группа", "Имя"]}` —
имена локализованные, как в интерфейсе Archicad (в русской версии — русские).
Список всех свойств: `API.GetAllPropertyNames`.

## Запись свойств (меняет проект — предупреди пользователя!)

```bash
python scripts/ac.py call API.SetPropertyValuesOfElements @set.json
```

set.json:
```json
{
  "elementPropertyValues": [
    {
      "elementId": {"guid": "..."},
      "propertyId": {"guid": "..."},
      "propertyValue": {"value": "новое значение"}
    }
  ]
}
```

Работает только с редактируемыми (UserDefined) свойствами.

## Этажи

Отдельной команды списка этажей в AC25 нет. Практичный способ — выгрузить
`General_HomeStoryName` (имя) и `General_TopLinkStory`/`General_BottomElevationToHomeStory`
по элементам, либо собрать уникальные значения имён этажей из выгрузки.

## Атрибуты (слои, материалы, поверхности)

```bash
# Все слои проекта (вернёт attributeId)
python scripts/ac.py call API.GetAttributesByType "{\"attributeType\": \"Layer\"}"
# Детали слоёв по id
python scripts/ac.py call API.GetLayerAttributes @ids.json
# Строительные материалы
python scripts/ac.py call API.GetBuildingMaterialAttributes @ids.json
```

ids.json: `{"attributeIds": [{"attributeId": {"guid": "..."}}, ...]}`.
Типы атрибутов: Layer, BuildingMaterial, Composite, Fill, Line, PenTable,
Profile, Surface, ZoneCategory, LayerCombination.

## Диагностика

| Симптом | Причина |
|---|---|
| URLError / connection refused | Archicad не запущен (API живёт внутри процесса) |
| error 2002 Command not found | Команды нет в AC25 — см. supported_commands.json |
| error 4002 Invalid parameters | Чаще всего забыта обёртка elementId/propertyId |
| error 4005 Property not found | Опечатка в nonLocalizedName или свойство новее AC25 |
| value отсутствует, status notAvailable | Свойство неприменимо к этому типу элемента |
