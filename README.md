# archicad-skill

Скилл (плагин) Claude Code для работы с проектами **Archicad 25** через
встроенный JSON API (`http://127.0.0.1:19723`): получение элементов и свойств,
расчёты объёмов и площадей, экспликации помещений, спецификации, классификации.

## Требования

- Archicad 25 запущен, проект открыт (API живёт внутри процесса Archicad)
- Python 3.10+ (скрипты используют только стандартную библиотеку)
- Claude Code

## Установка на другом ПК

### Способ 1: как плагин (рекомендуется)

Репозиторий приватный, поэтому сначала нужен доступ к нему по git
(достаточно один раз выполнить `gh auth login`, либо настроить git-credentials
для github.com). Затем в Claude Code:

```
/plugin marketplace add tnixton/archicad-skill
/plugin install archicad-skill@archicad-skill
```

Обновление: `/plugin marketplace update archicad-skill`.

### Способ 2: вручную, без плагина

```
git clone https://github.com/tnixton/archicad-skill.git
```

и скопировать папку `skills/archicad` в `~/.claude/skills/archicad`
(Windows: `%USERPROFILE%\.claude\skills\archicad`).

### Проверка

В Claude Code попросите: «покажи сводку по элементам проекта Archicad» —
скилл должен подключиться и вывести количество элементов по типам.
Быстрый тест без Claude: `python skills/archicad/scripts/ac.py info`.

## Состав

```
skills/archicad/
├── SKILL.md                        — инструкции скилла
├── scripts/
│   ├── ac.py                       — CLI-клиент API (info, types, call, find-prop, values)
│   └── probe_commands.py           — проверка, какие команды поддерживает сборка
└── references/
    ├── commands.md                 — справочник всех 46 команд AC25
    ├── recipes.md                  — рецепты типовых задач
    ├── builtin-properties.md       — 527 встроенных свойств
    └── supported_commands.json     — результат зондирования AC25 build 5010
tools/                              — генераторы справочников (для разработки скилла)
examples/poc.py                     — первоначальный PoC
```

## Ограничения API Archicad 25

- Только чтение данных + запись свойств/классификаций; создание и изменение
  геометрии через JSON API недоступно.
- Набор команд меньше, чем в свежей документации Graphisoft (46 из ~73);
  точный список — `references/supported_commands.json`.
