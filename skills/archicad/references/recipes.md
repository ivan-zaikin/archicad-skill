# Рецепты: типовые задачи через JSON API Archicad 25

Все примеры — через `scripts/ac.py` (или `from ac import call`).
Проверено на Archicad 25 build 5010.

## Экспликация помещений (зоны)

```bash
python scripts/ac.py values Zone Zone_ZoneName,Zone_ZoneNumber,Zone_NetArea,Zone_CalculatedArea > zones.json
```

Затем агрегируй: группировка по имени/этажу, сумма площадей. Полезные свойства:
`Zone_ReducedArea`, `Zone_ZoneCategoryCode`,
`Zone_WallsSurfaceArea` (площадь стен зоны — для отделки).
Внимание: `Zone_CalculatedArea` бывает 0, если зоны в проекте не пересчитаны —
надёжнее `Zone_NetArea` (выгрузи обе и сравни).

## Ведомость объёмов (стены, перекрытия, колонны...)

```bash
python scripts/ac.py values Wall General_NetVolume,General_Area,Construction_CompositeName,Construction_StructureType > walls.json
python scripts/ac.py values Slab General_NetVolume,General_NetTopSurfaceArea,Construction_CompositeName,ModelView_LayerName,General_Thickness > slabs.json
```

`General_NetVolume` — чистый объём (с вычетом проёмов), `General_GrossVolume` —
брутто. Для расчёта бетона/кладки обычно нужен Net.
Не суммируй всё подряд: сначала сгруппируй по слою (`ModelView_LayerName`),
структуре (`Construction_CompositeName` / `Construction_StructureType`) и
толщине — в реальных проектах попадаются служебные болванки (слои вроде
«скрыт», толщины в несколько метров). Покажи разбивку пользователю и исключи
мусор. У composite-элементов NetVolume включает все слои; чистый бетон
несущего слоя считай через компоненты (см. «Состав конструкций»).

## Окна и двери (спецификация)

```bash
python scripts/ac.py values Window General_ElementID,General_Width,General_Height,WindowDoor_WHSize > windows.json
```

Размеры в метрах (`WindowDoor_WHSize` — готовая строка «ш×в»). Свойств
`WindowDoor_Width/Height` в AC25 **нет** (ошибка 4005) — габариты проёма
бери из `General_Width`/`General_Height`. Группируй по размеру или по
`General_ElementID`/`WindowDoor_MarkerText` для маркировки. Двери — тип
`Door`, свойства те же.

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

⚠️ Список **неполный**: стены, которые Archicad не привязал к зоне, в выборку
не попадут (видели 5 стен вместо ~10). Годится для «какие элементы рядом», но
не для обмеров. Полную поверхность стен зоны бери из `Zone_WallsSurfaceArea`.

## Зоны по секции/блоку (поле «ID»)

Поле «ID» зоны (раздел «ID и Категории» в Archicad) — это свойство
`General_ElementID`. В типовых проектах им метят секцию/блок (А, Б, М…).
Фильтрация и группировка по нему — обычный способ собрать помещения одной
секции:

```bash
python scripts/ac.py values Zone Zone_ZoneName,Zone_ZoneNumber,General_ElementID,Zone_WallsSurfaceArea > zones.json
```

Затем в Python отбери `z["General_ElementID"] == "Б"`. В отличие от
`Zone_ZoneNumber` (часто неуникален и пуст), `General_ElementID` обычно
проставлен и удобен для разрезов отчёта по секциям.

## Колонны в отделке стен

Колонны, выходящие в помещение, входят в ведомость отделки наравне со стенами,
но считаются иначе:

- Материал колонны **не** в `Construction_CompositeName` (там `notAvailable`) —
  смотри группу свойств `Column_*` (`Column_CoreDepth`, `Column_CoreWidth`) и
  строительный материал ядра через атрибуты.
- `Column_NetCoreSideSurfaceArea` — боковая поверхность по **всей** высоте
  колонны (колонна может идти сквозь весь дом, напр. 24 м). Для одного
  помещения бери долю: `периметр_открытых_граней × высота_зоны`
  (`General_Height` зоны).
- API **не знает**, какая грань колонны выходит в комнату, а какая утоплена в
  стену. Число и размер открытых граней уточняй у пользователя.

Пример (помещение «Водоподготовка», 3 колонны 0,3×0,7 м, высота зоны 2,74 м):
открыты соответственно 4 грани (периметр 2,0 м → 5,48 м²), 1 большая грань
(0,7 м → 1,92 м²), 1 малая (0,3 м → 0,82 м²); итого ЖБ-колонны 8,22 м². Эту
площадь вычитают из `Zone_WallsSurfaceArea`, чтобы получить площадь кладки
(см. ru-reports.md, «Разбивка отделки по материалу»).

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

Отдельной команды списка этажей в AC25 нет, и встроенного свойства с
**именем** этажа тоже нет (`General_HomeStoryName` — из более новых версий,
в AC25 даёт ошибку 4005). Практичная привязка элемента к этажу — отметка
его собственного этажа: `General_BottomElevationToProjectZero` −
`General_BottomElevationToHomeStory` (обе в метрах). Группируй по этой
разности; уникальные её значения дают и список этажей проекта.

**Оговорка для зон:** у зон эта разность бывает 0 для всех помещений сразу
(homeStory зоны совпадает с project zero). Если так — группируй зоны по
абсолютной `General_BottomElevationToProjectZero` напрямую: для подвала она
даёт реальную отметку (напр. −3,15), для надземных этажей — 0, 3, 6… Стены же
надёжно разносятся по этажам разностью отметок, как описано выше.

## Конкретный элемент по GUID

GUID — единственный уникальный идентификатор (поле «ИД элемента» НЕ уникально:
оно копируется вместе с элементом, тысячи элементов могут носить один ИД).
Пользователь видит GUID выделенного элемента в Archicad: Окно → Панели →
Информация об элементе. Зная guid, свойства берутся напрямую, тип элемента —
свойство `General_Type` (локализованное: «Стена», «Зона»...; `General_TypeName`
в AC25 нет):

```python
from ac import call, get_property_ids
pids = get_property_ids(['General_Type', 'General_ElementID', 'General_NetVolume'])
call('API.GetPropertyValuesOfElements', {
    'elements': [{'elementId': {'guid': '...'}}],
    'properties': [{'propertyId': p} for p in pids]})
```

## Сколько отдельных зданий в проекте

Понятия «здание/корпус» в API нет. Рабочий приём — пространственная
кластеризация: выгрузи `API.Get2DBoundingBoxes` для всех стен, возьми центры
габаритов, положи их на сетку ~5 м и объедини соседние занятые ячейки
(union-find). Каждый кластер — отдельно стоящее строение; его габарит и число
стен помогают отличить типовые корпуса от сблокированных. Порог 5 м разделяет
дома через разрыв, 10 м — группирует комплексы. Сначала проверь лёгкие пути:
имена слоёв (`GetLayerAttributes`) и hotlink-модули — корпуса могут быть
размечены там.

## Навигатор: виды, макеты, каталоги

`GetNavigatorItemTree` отдаёт дерево навигатора; рабочие значения
`navigatorTreeId.type` в AC25: `ProjectMap` (этажи, разрезы, фасады,
каталоги-schedules), `ViewMap` (карта видов), `LayoutBook` (листы).
`PublisherSets` в AC25 не принимается. Узлы рекурсивные: `navigatorItem`
→ `children`; у узла есть `type`, `prefix`, `name`. Поиск «где в проекте
лист/вид X» — обход дерева по подстроке имени. Содержимое вида (какие
элементы на нём видны) через API получить нельзя — виды хранят настройки,
а не списки элементов; для «посчитай по дому/корпусу» используй
пространственную выборку (см. «Сколько отдельных зданий»).

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
