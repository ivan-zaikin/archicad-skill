# CLI-клиент JSON API Archicad — PowerShell-версия ac.py (без зависимостей).
#
# Команды:
#   ./ac.ps1 info                        — версия Archicad, проверка соединения
#   ./ac.ps1 call <API.Команда> [JSON]   — произвольная команда; параметры —
#                                          JSON-строкой, @файл или '-' (stdin)
#   ./ac.ps1 types                       — количество элементов по типам
#   ./ac.ps1 find-prop <подстрока>       — поиск встроенных свойств по имени
#   ./ac.ps1 values <Тип> <Свойство,..>  — значения встроенных свойств для всех
#                                          элементов типа (JSON в stdout)
#   ./ac.ps1 values-for <guid,..> <Свойство,..>
#                                        — то же для конкретных GUID (список
#                                          одним аргументом, @файл или - из stdin)
#
# Примеры:
#   ./ac.ps1 call API.GetElementsByType '{"elementType": "Wall"}'
#   ./ac.ps1 values Wall General_NetVolume,General_Area > walls.json
#   ./ac.ps1 values-for 'GUID1,GUID2' General_Area,Construction_CompositeName
#
# Выход всегда JSON. Код возврата 1 при ошибке.

$ErrorActionPreference = 'Stop'
$ApiUrl = 'http://127.0.0.1:19723'

$ElementTypes = @(
    'Wall', 'Column', 'Beam', 'Window', 'Door', 'Object', 'Lamp', 'Slab',
    'Roof', 'Mesh', 'Zone', 'CurtainWall', 'Shell', 'Skylight', 'Morph',
    'Stair', 'Railing', 'Opening'
)

function Fail([string]$Message) {
    [Console]::Error.WriteLine((@{ error = $Message } | ConvertTo-Json -Compress))
    exit 1
}

function Out-Json($Data) {
    $Data | ConvertTo-Json -Depth 100
}

function Invoke-Ac([string]$Command, $Parameters = $null) {
    $payload = @{ command = $Command }
    if ($null -ne $Parameters) { $payload.parameters = $Parameters }
    $body = $payload | ConvertTo-Json -Depth 100 -Compress
    try {
        $r = Invoke-RestMethod -Uri $ApiUrl -Method Post -Body $body `
            -ContentType 'application/json; charset=utf-8' -TimeoutSec 300
    } catch {
        Fail "Archicad API недоступен ($($_.Exception.Message)). Archicad запущен?"
    }
    if (-not $r.succeeded) {
        Fail "${Command}: $($r.error | ConvertTo-Json -Compress)"
    }
    return $r.result
}

function Unwrap($Value) {
    # Перечисления приходят как {"type": "nonLocalizedValue", "nonLocalizedValue": ...}
    if ($Value -is [System.Management.Automation.PSCustomObject]) {
        if ($null -ne $Value.nonLocalizedValue) { return $Value.nonLocalizedValue }
        if ($null -ne $Value.displayValue) { return $Value.displayValue }
    }
    return $Value
}

function Cmd-Info { Out-Json (Invoke-Ac 'API.GetProductInfo') }

function Cmd-Call([string[]]$CmdArgs) {
    if (-not $CmdArgs) { Fail 'Укажите команду, например: ac.ps1 call API.GetAllElements' }
    $parameters = $null
    if ($CmdArgs.Count -gt 1) {
        $raw = $CmdArgs[1]
        if ($raw.StartsWith('@')) { $raw = Get-Content -Raw -Encoding utf8 $raw.Substring(1) }
        elseif ($raw -eq '-') { $raw = [Console]::In.ReadToEnd() }
        $parameters = $raw | ConvertFrom-Json
    }
    Out-Json (Invoke-Ac $CmdArgs[0] $parameters)
}

function Cmd-Types {
    $counts = [ordered]@{}
    foreach ($t in $ElementTypes) {
        $elements = (Invoke-Ac 'API.GetElementsByType' @{ elementType = $t }).elements
        if ($elements.Count -gt 0) { $counts[$t] = $elements.Count }
    }
    $sorted = [ordered]@{}
    $counts.GetEnumerator() | Sort-Object -Property Value -Descending |
        ForEach-Object { $sorted[$_.Key] = $_.Value }
    Out-Json $sorted
}

function Cmd-FindProp([string[]]$CmdArgs) {
    if (-not $CmdArgs) { Fail 'Укажите подстроку, например: ac.ps1 find-prop Volume' }
    $needle = $CmdArgs[0]
    $props = (Invoke-Ac 'API.GetAllPropertyNames').properties
    $matched = @($props | Where-Object {
        $_.type -eq 'BuiltIn' -and $_.nonLocalizedName -like "*$needle*"
    } | ForEach-Object { $_.nonLocalizedName } | Sort-Object)
    Out-Json $matched
}

function Resolve-PropertyIds([string[]]$Names) {
    # Распознаёт имена без аварийного выхода: возвращает объект с GoodNames, Ids, Bad.
    $query = @($Names | ForEach-Object { @{ type = 'BuiltIn'; nonLocalizedName = $_ } })
    $result = (Invoke-Ac 'API.GetPropertyIds' @{ properties = $query }).properties
    $goodNames = @(); $ids = @(); $bad = @()
    for ($i = 0; $i -lt $Names.Count; $i++) {
        if ($null -ne $result[$i].propertyId) {
            $goodNames += $Names[$i]
            $ids += $result[$i].propertyId
        } else {
            $bad += $Names[$i]
        }
    }
    [pscustomobject]@{ GoodNames = [string[]]$goodNames; Ids = $ids; Bad = [string[]]$bad }
}

function Get-PropertyIds([string[]]$Names) {
    # Строгий вариант: при любом плохом имени — выход с перечислением СРАЗУ ВСЕХ.
    $r = Resolve-PropertyIds $Names
    if ($r.Bad.Count -gt 0) {
        Fail "Свойства не найдены (проверь через find-prop): $($r.Bad -join ', ')"
    }
    return $r.Ids
}

function Get-RowsFor($Elements, [string[]]$PropNames) {
    # Считывает свойства для элементов; плохие имена пропускает с warning в stderr.
    $r = Resolve-PropertyIds $PropNames
    if ($r.Bad.Count -gt 0) {
        [Console]::Error.WriteLine(
            (@{ warning = "Свойства пропущены (не найдены): $($r.Bad -join ', ')" } | ConvertTo-Json -Compress))
    }
    $goodNames = [string[]]$r.GoodNames
    if ($r.Ids.Count -eq 0) {
        return @($Elements | ForEach-Object { [pscustomobject]@{ guid = $_.elementId.guid } })
    }
    $values = (Invoke-Ac 'API.GetPropertyValuesOfElements' @{
        elements   = $Elements
        properties = @($r.Ids | ForEach-Object { @{ propertyId = $_ } })
    }).propertyValuesForElements

    $rows = for ($i = 0; $i -lt $Elements.Count; $i++) {
        $row = [ordered]@{ guid = $Elements[$i].elementId.guid }
        $pvs = $values[$i].propertyValues
        for ($j = 0; $j -lt $goodNames.Count; $j++) {
            $row[$goodNames[$j]] = Unwrap $pvs[$j].propertyValue.value
        }
        [pscustomobject]$row
    }
    return $rows
}

function Cmd-Values([string[]]$CmdArgs) {
    if ($CmdArgs.Count -lt 2) { Fail 'Формат: ac.ps1 values <Тип> <Свойство1,Свойство2,...>' }
    $elType = $CmdArgs[0]
    $propNames = @($CmdArgs | Select-Object -Skip 1 | ForEach-Object { $_ -split ',' } | Where-Object { $_ })
    $elements = (Invoke-Ac 'API.GetElementsByType' @{ elementType = $elType }).elements
    if ($elements.Count -eq 0) { Out-Json @(); return }
    Out-Json (Get-RowsFor $elements $propNames)
}

function Cmd-ValuesFor([string[]]$CmdArgs) {
    if ($CmdArgs.Count -lt 2) {
        Fail 'Формат: ac.ps1 values-for <guid,guid,...|@файл|-> <Свойство1,Свойство2,...> (список GUID — одним аргументом, в кавычках)'
    }
    $raw = $CmdArgs[0]
    if ($raw.StartsWith('@')) { $raw = Get-Content -Raw -Encoding utf8 $raw.Substring(1) }
    elseif ($raw -eq '-') { $raw = [Console]::In.ReadToEnd() }
    $guids = @($raw -split '[,\r\n]+' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
    $propNames = @($CmdArgs | Select-Object -Skip 1 | ForEach-Object { $_ -split ',' } | Where-Object { $_ })
    if ($guids.Count -eq 0) { Fail 'Укажите хотя бы один GUID' }
    $elements = @($guids | ForEach-Object { @{ elementId = @{ guid = $_ } } })
    Out-Json (Get-RowsFor $elements $propNames)
}

if (-not $args) { Get-Content $PSCommandPath -TotalCount 20 | Select-Object -Skip 1; exit 0 }
# PowerShell сам превращает "A,B" в массив — разворачиваем вложенные массивы
$cmd = $args[0]
$rest = @()
foreach ($a in ($args | Select-Object -Skip 1)) { $rest += $a }
$rest = [string[]]$rest
switch ($cmd) {
    'info'      { Cmd-Info }
    'call'      { Cmd-Call $rest }
    'types'     { Cmd-Types }
    'find-prop'  { Cmd-FindProp $rest }
    'values'     { Cmd-Values $rest }
    'values-for' { Cmd-ValuesFor $rest }
    default      { Fail "Неизвестная команда: $cmd. Доступно: info, call, types, find-prop, values, values-for" }
}
