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

## Этажи: надёжный список из отметок стен

```bash
python scripts/ac.py stories
```

Возвращает массив `[{"story": 1, "elevation": 0.0, "wall_count": 142}, ...]`,
отсортированный снизу вверх. Используй `elevation` для группировки любых
элементов по этажу — вместо ненадёжного вычитания отметок на лету.

Привязка элемента к этажу:
```python
from ac import call, _rows_for
import json, subprocess, math

stories_raw = subprocess.check_output(["python", "scripts/ac.py", "stories"])
stories = json.loads(stories_raw)  # [{story, elevation, wall_count}, ...]

def floor_of(z_proj, z_home):
    elev = round(z_proj - z_home, 2)
    # ближайший этаж снизу
    below = [s for s in stories if s["elevation"] <= elev + 0.05]
    return below[-1] if below else stories[0]
```

**Зоны:** если `z_proj - z_home` = 0 у всех зон, используй `z_proj` напрямую
(отметка зоны от нуля проекта совпадает с отметкой этажа).

**Окна/двери:** этаж проёма — этаж несущей стены, а не сам элемент.
Берутся те же отметки (`General_BottomElevationToProjectZero`).

## Кросс-валидация зон (запускай перед любой ведомостью)

```bash
python scripts/ac.py validate-zones
```

Сравнивает `Zone_NetArea` и `Zone_CalculatedArea` по каждой зоне.
Расхождение > 1% → предупреждение: зоны устарели, надо пересчитать
(Документ → Обновить/Перегенерировать → Зоны). Пока расхождение не устранено,
площади зон из модели считаются ненадёжными.

Вывод при проблемах:
```json
{
  "zones_checked": 42,
  "issues_count": 3,
  "warning": "Пересчитайте зоны...",
  "zones_with_issues": [
    {"name": "Гостиная", "Zone_NetArea": 18.52, "Zone_CalculatedArea": 0.0, "diff_pct": 100.0}
  ]
}
```

`Zone_CalculatedArea` = 0 у непересчитанных зон — самый частый случай.

## Проверка суммы стен зоны

После расчёта ведомости отделки автоматически проверяй баланс:

```python
# После выгрузки зон с Zone_WallsSurfaceArea и Zone_WindowsSurfaceArea, Zone_DoorsSurfaceArea
for z in zones:
    total_wall = z.get("Zone_WallsSurfaceArea") or 0
    wins = z.get("Zone_WindowsSurfaceArea") or 0
    doors = z.get("Zone_DoorsSurfaceArea") or 0
    finish = total_wall - wins - doors
    if finish < 0:
        print(f"ПРЕДУПРЕЖДЕНИЕ {z['Zone_ZoneName']}: площадь отделки < 0 "
              f"({total_wall:.2f} − {wins:.2f} − {doors:.2f} = {finish:.2f})")
```

Отрицательный результат — признак незакрытых проёмов или незаданных размеров
окон/дверей в модели. Нулевые значения `Zone_WindowsSurfaceArea` при наличии
окон тоже сигнализируют: окна не привязаны к зоне (зона не покрывает проём).

## Геометрия из bounding boxes: когда свойствам зон нельзя доверять

**Ограничение AC25 API:** полигон зоны (список вершин) API не отдаёт.
Доступны только прямоугольные bounding boxes (`Get2DBoundingBoxes`,
`Get3DBoundingBoxes`). Это не позволяет вычислить точную площадь — но даёт
три полезных инструмента.

### 1. Диагностика зон через zone-geometry

```bash
python scripts/ac.py zone-geometry
```

Для каждой зоны возвращает:
- `bbox_area` — площадь описывающего прямоугольника (всегда ≥ реальной площади)
- `fill_ratio` = Zone_NetArea / bbox_area:
  - 0.7–1.0 — прямоугольная/почти прямоугольная комната (bbox надёжен)
  - 0.4–0.7 — Г-образная или сложная форма (bbox завышен на 30–60%)
  - < 0.35 — зона смещена или нестандартная форма, bbox бесполезен
  - > 1.05 — **Zone_NetArea больше физического bbox**, зона не пересчитана
- `bbox_height` — высота из 3D bbox; сравни с `General_Height`
- `height_mismatch` — флаг расхождения высоты > 5 см (зона задана неправильно)

**Применение:** если `fill_ratio` ≈ 1 (комната прямоугольная), а `Zone_NetArea`
подозрительна (0 или нереальное значение) — `bbox_area` можно использовать как
грубую оценку. Для сложных форм bbox не годится.

### 2. Перекрытие как геометрический fallback для площади

Перекрытие (`Slab`) — чисто геометрический объект. Его `General_NetTopSurfaceArea`
вычисляется из реальной формы, независимо от состояния зон. Если удаётся
сопоставить зону с её перекрытием, площадь перекрытия служит надёжным
геометрическим ориентиром.

**Ограничение:** в типовых жилых проектах перекрытие — одно на весь этаж, а не
отдельное на каждое помещение. Тогда площадь перекрытия = площадь всего этажа,
не конкретной комнаты. Подходит для проверки суммарной площади этажа.

```python
from ac import call, _rows_for
import math

zones  = call("API.GetElementsByType", {"elementType": "Zone"})["elements"]
slabs  = call("API.GetElementsByType", {"elementType": "Slab"})["elements"]

zone_rows = _rows_for(zones, [
    "Zone_ZoneName", "Zone_ZoneNumber", "Zone_NetArea",
    "General_BottomElevationToProjectZero",
])
slab_rows = _rows_for(slabs, [
    "General_NetTopSurfaceArea", "General_Thickness",
    "General_BottomElevationToProjectZero", "Construction_CompositeName",
])

zone_bb = call("API.Get2DBoundingBoxes", {"elements": zones})["boundingBoxes2D"]
slab_bb = call("API.Get2DBoundingBoxes", {"elements": slabs})["boundingBoxes2D"]


def intersect_area(a, b):
    ix = max(0, min(a["xMax"], b["xMax"]) - max(a["xMin"], b["xMin"]))
    iy = max(0, min(a["yMax"], b["yMax"]) - max(a["yMin"], b["yMin"]))
    return ix * iy


for zone_row, zb in zip(zone_rows, zone_bb):
    if "boundingBox2D" not in zb:
        continue
    z_box  = zb["boundingBox2D"]
    z_elev = zone_row.get("General_BottomElevationToProjectZero") or 0
    z_bbox_area = (z_box["xMax"] - z_box["xMin"]) * (z_box["yMax"] - z_box["yMin"])

    best, best_ratio = None, 0.0
    for slab_row, sb in zip(slab_rows, slab_bb):
        if "boundingBox2D" not in sb:
            continue
        s_box  = sb["boundingBox2D"]
        s_elev = slab_row.get("General_BottomElevationToProjectZero") or 0
        thick  = slab_row.get("General_Thickness") or 0
        slab_top = s_elev + thick
        # Верхняя грань перекрытия должна быть вблизи низа зоны (±50 см)
        if abs(slab_top - z_elev) > 0.5:
            continue
        inter = intersect_area(z_box, s_box)
        ratio = inter / z_bbox_area if z_bbox_area > 0 else 0
        if ratio > best_ratio:
            best_ratio, best = ratio, slab_row

    if best and best_ratio > 0.5:
        print(f"{zone_row['Zone_ZoneName']}: Zone_NetArea={zone_row.get('Zone_NetArea'):.2f} "
              f"| slab_area={best.get('General_NetTopSurfaceArea'):.2f} "
              f"| coverage={best_ratio:.2f} ({best.get('Construction_CompositeName')})")
    else:
        print(f"{zone_row['Zone_ZoneName']}: перекрытие не найдено (coverage={best_ratio:.2f})")
```

`coverage` = доля bbox зоны, перекрытая bbox перекрытия. При `coverage ≥ 0.8`
соответствие надёжно. При `coverage ∈ [0.5, 0.8]` — частичное, данные ориентировочны.

### 3. Высота зоны из 3D bounding box

`General_Height` в AC25 — свойство, которое может не совпадать с реальной
геометрией зоны (например, если зону вытянули не через инструмент зон, а
вручную). Геометрически надёжный вариант:

```python
from ac import call
zones = call("API.GetElementsByType", {"elementType": "Zone"})["elements"]
bb3d  = call("API.Get3DBoundingBoxes", {"elements": zones})["boundingBoxes3D"]
for z, b in zip(zones, bb3d):
    if "boundingBox3D" in b:
        box = b["boundingBox3D"]
        geom_height = round(box["zMax"] - box["zMin"], 3)
        # Это независимая от свойства высота — используй для ведомости отделки
        # когда General_Height под вопросом
```

### 4. Суммарная площадь этажа через перекрытия (контроль ТЭП)

Если зоны ненадёжны, сумму площадей этажа можно оценить через перекрытия —
они не зависят от состояния зон:

```bash
python scripts/ac.py values Slab General_NetTopSurfaceArea,Construction_CompositeName,General_BottomElevationToProjectZero,General_BottomElevationToHomeStory,ModelView_LayerName > slabs.json
```

Сгруппируй по этажу (разность отметок), суммируй `General_NetTopSurfaceArea`.
Это геометрическая площадь перекрытий — хорошее приближение к площади этажа
для ТЭП (при условии, что перекрытия охватывают весь план и не задвоены).
Сверяй с суммой `Zone_NetArea` по тому же этажу — расхождение > 5% требует
объяснения.

### Когда обращаться к IFC

Если геометрической точности в рамках JSON API недостаточно (нестандартные
формы, много Г-образных помещений, точная экспликация полов), следующий шаг —
IFC-экспорт из Archicad + парсинг через IfcOpenShell:
- `IfcSpace` содержит точный полигон помещения → точная площадь
- `IfcRelSpaceBoundary` даёт связи пространство ↔ стены с реальными гранями
- Минус: нужен ручной экспорт, данные — снимок на момент экспорта

Это отдельный пайплайн; JSON API остаётся основным.

## BIM: классификации как стабильный идентификатор

Слои проекта (`ModelView_LayerName`) — удобный фильтр, но нестабильный: имена
меняются между проектами и компаниями. Классификации (OmniClass, UniClass,
Uniformat) — семантически стабильны и переносимы.

### Когда нужны классификации

- Нужно отделить **несущие стены** от перегородок безо знания имён слоёв
- Элементы одного типа в разных слоях (стены, разнесённые по слоям корпусов)
- Задача пришла из другого проекта — слои другие, классификация та же

### Рецепт: элементы по классификационному коду

```bash
# 1. Узнать, какие системы классификации есть в проекте
python scripts/ac.py call API.GetAllClassificationSystems

# 2. Дерево позиций нужной системы
python scripts/ac.py call API.GetAllClassificationsInSystem \
  "{\"classificationSystemId\": {\"guid\": \"<guid-системы>\"}}"

# 3. Элементы с конкретной позицией (например, «Несущая стена»)
python scripts/ac.py call API.GetElementsByClassification \
  "{\"classificationItemId\": {\"guid\": \"<guid-позиции>\"}}"

# 4. Проверить, какая классификация назначена конкретным элементам
python scripts/ac.py call API.GetClassificationsOfElements @elements.json
```

### BIM-полнота: элементы без классификации

```python
from ac import call

systems = call("API.GetAllClassificationSystems")["classificationSystems"]
if not systems:
    print("В проекте нет классификационных систем — BIM-фильтрация недоступна")
else:
    # Проверь назначение классификации для ключевых типов
    for el_type in ["Wall", "Slab", "Column"]:
        els = call("API.GetElementsByType", {"elementType": el_type})["elements"]
        cls_data = call("API.GetClassificationsOfElements", {
            "elements": els,
            "classificationSystemIds": [{"classificationSystemId": s["classificationSystemId"]}
                                        for s in systems],
        })["elementClassifications"]
        no_cls = sum(1 for ec in cls_data
                     if all(not c.get("classificationItemId") for c in ec.get("elementClassifications", [])))
        pct = round(no_cls / len(els) * 100) if els else 0
        print(f"{el_type}: {no_cls}/{len(els)} без классификации ({pct}%)")
```

Высокий % без классификации = BIM-модель неполная, фильтрация по классам
ненадёжна → переходи на слои или структуру (`Construction_CompositeName`).

### Практическое правило

| Ситуация | Используй |
|---|---|
| Проект одной компании, слои устоялись | `ModelView_LayerName` — проще |
| Несколько проектов / разные команды | Классификацию |
| Классификация не назначена (> 30% без кода) | `Construction_CompositeName` + `Construction_StructureType` |

## Диагностика

| Симптом | Причина |
|---|---|
| URLError / connection refused | Archicad не запущен (API живёт внутри процесса) |
| error 2002 Command not found | Команды нет в AC25 — см. supported_commands.json |
| error 4002 Invalid parameters | Чаще всего забыта обёртка elementId/propertyId |
| error 4005 Property not found | Опечатка в nonLocalizedName или свойство новее AC25 |
| value отсутствует, status notAvailable | Свойство неприменимо к этому типу элемента |
