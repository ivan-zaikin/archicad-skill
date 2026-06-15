# archicad-skill

Скилл (плагин) Claude Code для работы с проектами **Archicad 25** через
встроенный JSON API. Спрашивайте на русском — Claude сам дёргает API,
считает площади и объёмы, строит ведомости.

## Что умеет

- Экспликация помещений, ведомость отделки, спецификация окон/двери, квартирография, ТЭП
- Объёмы бетона/кладки по типам и конструкциям
- Классификации, пользовательские свойства, навигатор (виды, листы, этажи)
- Кросс-проверка данных зон: `validate-zones`, геометрический fallback через перекрытия
- Документы по ГОСТ 21.501 и СП 54.13330

## Требования

- Archicad 25 запущен, проект открыт
- Python 3.10+ — [скачать с python.org](https://www.python.org/downloads/) или через Microsoft Store: `python3`
  (при установке отметить **«Add Python to PATH»**)
- [Claude Desktop](https://claude.ai/download) — для общения с Claude
- [Claude Code](https://claude.ai/code) (CLI) — для установки плагина и запуска скиллов;
  после установки выполнить `claude` в терминале для первоначальной настройки

## Установка

### Способ 1: плагин (рекомендуется)

В Claude Code:

```
/plugin marketplace add ivan-zaikin/archicad-skill
/plugin install archicad-skill@archicad-skill
```

Обновление: `/plugin marketplace update archicad-skill`.

### Способ 2: вручную

Скачать репозиторий и скопировать папку `skills/archicad` в:
- Windows: `%USERPROFILE%\.claude\skills\archicad`
- macOS/Linux: `~/.claude/skills/archicad`

### Проверка

Попросите Claude: «покажи сводку по элементам проекта Archicad» —
скилл подключится и выведет количество элементов по типам.

Без Claude: `python skills/archicad/scripts/ac.py info`

## Команды `ac.py`

| Команда | Что делает |
|---|---|
| `info` | версия Archicad, проверка соединения |
| `types` | количество элементов по типам |
| `call <API.Команда>` | произвольный вызов API |
| `find-prop <подстрока>` | поиск встроенных свойств |
| `values <Тип> <Свойства>` | выгрузка свойств всех элементов типа |
| `values-for <GUID,..> <Свойства>` | то же для конкретных элементов |
| `stories` | список этажей из отметок стен |
| `validate-zones` | кросс-проверка Zone_NetArea vs CalculatedArea |
| `zone-geometry` | bbox-геометрия зон: fill_ratio, height_mismatch |

## Состав

```
skills/archicad/
├── SKILL.md                    — инструкции для Claude
├── scripts/
│   ├── ac.py                   — CLI-клиент API
│   └── probe_commands.py       — проверка поддерживаемых команд сборки
└── references/
    ├── commands.md             — справочник 46 команд AC25
    ├── recipes.md              — рецепты: зоны, стены, окна/двери, этажи, BIM
    ├── ru-reports.md           — формы ГОСТ 21.501 и СП 54.13330
    ├── builtin-properties.md   — 527 встроенных свойств
    └── supported_commands.json — команды, поддерживаемые AC25 build 5010
```

## Ограничения

- Только чтение + запись свойств/классификаций; геометрию менять нельзя
- Полигон зоны API не отдаёт (только bounding box) — для точных площадей
  нестандартных форм нужен IFC-экспорт
- Поддерживается AC25; часть команд новее AC25 недоступна
