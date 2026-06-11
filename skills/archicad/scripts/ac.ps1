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
#
# Примеры:
#   ./ac.ps1 call API.GetElementsByType '{"elementType": "Wall"}'
#   ./ac.ps1 values Wall General_NetVolume,General_Area > walls.json
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

function Get-PropertyIds([string[]]$Names) {
    $query = @($Names | ForEach-Object { @{ type = 'BuiltIn'; nonLocalizedName = $_ } })
    $result = (Invoke-Ac 'API.GetPropertyIds' @{ properties = $query }).properties
    $ids = @()
    for ($i = 0; $i -lt $Names.Count; $i++) {
        if ($null -eq $result[$i].propertyId) {
            Fail "Свойство $($Names[$i]): $($result[$i].error | ConvertTo-Json -Compress)"
        }
        $ids += $result[$i].propertyId
    }
    return $ids
}

function Cmd-Values([string[]]$CmdArgs) {
    if ($CmdArgs.Count -lt 2) { Fail 'Формат: ac.ps1 values <Тип> <Свойство1,Свойство2,...>' }
    $elType = $CmdArgs[0]
    $propNames = @($CmdArgs | Select-Object -Skip 1 | ForEach-Object { $_ -split ',' } | Where-Object { $_ })
    $elements = (Invoke-Ac 'API.GetElementsByType' @{ elementType = $elType }).elements
    if ($elements.Count -eq 0) { Out-Json @(); return }
    $propIds = Get-PropertyIds $propNames
    $values = (Invoke-Ac 'API.GetPropertyValuesOfElements' @{
        elements   = $elements
        properties = @($propIds | ForEach-Object { @{ propertyId = $_ } })
    }).propertyValuesForElements

    $rows = for ($i = 0; $i -lt $elements.Count; $i++) {
        $row = [ordered]@{ guid = $elements[$i].elementId.guid }
        $pvs = $values[$i].propertyValues
        for ($j = 0; $j -lt $propNames.Count; $j++) {
            $row[$propNames[$j]] = Unwrap $pvs[$j].propertyValue.value
        }
        [pscustomobject]$row
    }
    Out-Json $rows
}

if (-not $args) { Get-Content $PSCommandPath -TotalCount 17 | Select-Object -Skip 1; exit 0 }
# PowerShell сам превращает "A,B" в массив — разворачиваем вложенные массивы
$cmd = $args[0]
$rest = @()
foreach ($a in ($args | Select-Object -Skip 1)) { $rest += $a }
$rest = [string[]]$rest
switch ($cmd) {
    'info'      { Cmd-Info }
    'call'      { Cmd-Call $rest }
    'types'     { Cmd-Types }
    'find-prop' { Cmd-FindProp $rest }
    'values'    { Cmd-Values $rest }
    default     { Fail "Неизвестная команда: $cmd. Доступно: info, call, types, find-prop, values" }
}
