# Справочник команд JSON API — Archicad 25 (build 3000+)

Сгенерировано из официального Python-пакета `archicad` (releases/ac25).
Все запросы: `POST http://127.0.0.1:19723` с телом `{"command": "API.<Имя>", "parameters": {...}}`.
Ответ: `{"succeeded": true, "result": {...}}` либо `{"succeeded": false, "error": {"code": N, "message": ...}}`.

## Ключевые JSON-структуры

Команды принимают/возвращают обёртки — частая причина ошибки 4002 (Invalid command parameters):

```jsonc
// ElementIdArrayItem — элемент списка elements
{ "elementId": { "guid": "..." } }

// PropertyIdArrayItem — элемент списка properties в Get/SetPropertyValuesOfElements
{ "propertyId": { "guid": "..." } }

// PropertyUserId — вход GetPropertyIds (BuiltIn или UserDefined)
{ "type": "BuiltIn", "nonLocalizedName": "General_NetVolume" }
{ "type": "UserDefined", "localizedName": ["Группа", "Имя свойства"] }

// PropertyValuesOrError — ответ GetPropertyValuesOfElements (на каждый элемент)
{ "propertyValues": [ { "propertyValue": { "value": 1.23, "type": "number", "status": "normal" } } ] }

// ClassificationSystemId / ClassificationItemId
{ "guid": "..." }
```

## Оглавление

- **Базовые**: `IsAlive`, `GetProductInfo`
- **Элементы**: `GetAllElements`, `GetElementsByType`, `GetElementsByClassification`, `GetElementsRelatedToZones`, `Get2DBoundingBoxes`, `Get3DBoundingBoxes`
- **Свойства**: `GetPropertyIds`, `GetAllPropertyNames`, `GetDetailsOfProperties`, `GetPropertyValuesOfElements`, `SetPropertyValuesOfElements`
- **Компоненты (слои конструкций)**: `GetComponentsOfElements`, `GetPropertyValuesOfElementComponents`
- **Классификации**: `GetAllClassificationSystems`, `GetAllClassificationsInSystem`, `GetDetailsOfClassificationItems`, `GetClassificationsOfElements`, `SetClassificationsOfElements`
- **Атрибуты**: `GetAttributesByType`, `GetActivePenTables`, `GetBuildingMaterialAttributes`, `GetCompositeAttributes`, `GetFillAttributes`, `GetLayerAttributes`, `GetLayerCombinationAttributes`, `GetLineAttributes`, `GetPenTableAttributes`, `GetProfileAttributes`, `GetProfileAttributePreview`, `GetSurfaceAttributes`, `GetZoneCategoryAttributes`
- **Навигатор и макеты**: `GetNavigatorItemTree`, `GetPublisherSetNames`, `RenameNavigatorItem`, `MoveNavigatorItem`, `DeleteNavigatorItems`, `CloneProjectMapItemToViewMap`, `CreateViewMapFolder`, `CreateLayout`, `CreateLayoutSubset`, `GetLayoutSettings`, `SetLayoutSettings`
- **Команды аддонов**: `ExecuteAddOnCommand`, `IsAddOnCommandAvailable`

## Базовые

### API.IsAlive

Checks if the Archicad connection is alive.

Параметры: нет.

Возвращает: `bool`

### API.GetProductInfo

Accesses the version information from the running Archicad.

Параметры: нет.

Возвращает: `Tuple[int, int, str]`

## Элементы

### API.GetAllElements

Returns the identifier of every element in the current plan.

Параметры: нет.

Возвращает: `List[ElementIdArrayItem]`

### API.GetElementsByType

Returns the identifier of every element of the given type on the plan.

Параметры:
- `elementType`: str

Возвращает: `List[ElementIdArrayItem]`

### API.GetElementsByClassification

Returns the identifier of every element with the given classification identifier.

Параметры:
- `classificationItemId`: ClassificationItemId — The identifier of a classification item.

Возвращает: `List[ElementIdArrayItem]`

### API.GetElementsRelatedToZones

Returns related elements of the given zones. The related elements will be grouped by type. If multiple zones was given, then the order of the returned list is that of the given zones.

Параметры:
- `zones`: List[ElementIdArrayItem]
- `elementTypes`: List[str] (опционально)

Возвращает: `List[ElementsOrError]`

### API.Get2DBoundingBoxes

Get the 2D bounding box of elements identified by their GUIDs. The bounding box is calculated from the global origin on the floor plan view. The output is the array of the bounding boxes respective to the input GUIDs. Only works for elements detailed in <i>Element Information</i>.

Параметры:
- `elements`: List[ElementIdArrayItem]

Возвращает: `List[BoundingBox2DOrError]`

### API.Get3DBoundingBoxes

Get the 3D bounding box of elements identified by their GUIDs. The bounding box is calculated from the global origin in the 3D view. The output is the array of the bounding boxes respective to the input GUIDs. Only works for elements detailed in <i>Element Information</i>.

Параметры:
- `elements`: List[ElementIdArrayItem]

Возвращает: `List[BoundingBox3DOrError]`

## Свойства

### API.GetPropertyIds

Returns the identifiers of property definitions for the requested property names.

Параметры:
- `properties`: List[PropertyUserId] — The unique identifier of a Property, identified by its name. May represent a User-Defined or a Built-In Property.

Возвращает: `List[PropertyIdOrError]`

### API.GetAllPropertyNames

Returns the human-readable names of available Property definitions for debug and development purposes.

Параметры: нет.

Возвращает: `List[PropertyUserId]`

### API.GetDetailsOfProperties

Returns the details of property definitions.

Параметры:
- `properties`: List[PropertyIdArrayItem]

Возвращает: `List[PropertyDefinitionOrError]`

### API.GetPropertyValuesOfElements

Returns the property values of the elements for the given property.

Параметры:
- `elements`: List[ElementIdArrayItem]
- `properties`: List[PropertyIdArrayItem]

Возвращает: `List[PropertyValuesOrError]`

### API.SetPropertyValuesOfElements

Sets the property values of elements.

Параметры:
- `elementPropertyValues`: List[ElementPropertyValue] — A property value with the identifiers of the property and its owner element.

Возвращает: `List[ExecutionResult]`

## Компоненты (слои конструкций)

### API.GetComponentsOfElements

Returns the identifier of every component for a list of elements. The order of the returned list is the same as the given elements.

Параметры:
- `elements`: List[ElementIdArrayItem]

Возвращает: `List[ElementComponentsOrError]`

### API.GetPropertyValuesOfElementComponents

Returns the property values of the components for the given property.

Параметры:
- `elementComponents`: List[ElementComponentIdArrayItem] — An item of a component array.
- `properties`: List[PropertyIdArrayItem]

Возвращает: `List[PropertyValuesOrError]`

## Классификации

### API.GetAllClassificationSystems

Returns the list of available classification systems.

Параметры: нет.

Возвращает: `List[ClassificationSystem]`

### API.GetAllClassificationsInSystem

Returns the tree of classifications in the given classification system.

Параметры:
- `classificationSystemId`: ClassificationSystemId — The identifier of a classification system.

Возвращает: `List[ClassificationItemArrayItem]`

### API.GetDetailsOfClassificationItems

Returns the details of classification items.

Параметры:
- `classificationItemIds`: List[ClassificationItemIdArrayItem]

Возвращает: `List[ClassificationItemOrError]`

### API.GetClassificationsOfElements

Returns the classification of the given elements in the given classification systems.

Параметры:
- `elements`: List[ElementIdArrayItem]
- `classificationSystemIds`: List[ClassificationSystemIdArrayItem]

Возвращает: `List[ElementClassificationOrError]`

### API.SetClassificationsOfElements

Sets the classifications of elements. In order to set the classification of an element to unclassified, omit the classificationItemId field.

Параметры:
- `elementClassifications`: List[ElementClassification] — The classification of an element.

Возвращает: `List[ExecutionResult]`

## Атрибуты

### API.GetAttributesByType

Returns the identifier of every attribute of the given type.

Параметры:
- `attributeType`: str

Возвращает: `List[AttributeIdWrapperItem]`

### API.GetActivePenTables

Returns the model view and layout book pen table identifiers.

Параметры: нет.

Возвращает: `Tuple[AttributeIdOrError, AttributeIdOrError]`

### API.GetBuildingMaterialAttributes

Returns the detailed building material attributes identified by their GUIDs.

Параметры:
- `attributeIds`: List[AttributeIdWrapperItem]

Возвращает: `List[BuildingMaterialAttributeOrError]`

### API.GetCompositeAttributes

Returns the detailed composite attributes identified by their GUIDs.

Параметры:
- `attributeIds`: List[AttributeIdWrapperItem]

Возвращает: `List[CompositeAttributeOrError]`

### API.GetFillAttributes

Returns the detailed fill attributes identified by their GUIDs.

Параметры:
- `attributeIds`: List[AttributeIdWrapperItem]

Возвращает: `List[FillAttributeOrError]`

### API.GetLayerAttributes

Returns the detailed layer attributes identified by their GUIDs.

Параметры:
- `attributeIds`: List[AttributeIdWrapperItem]

Возвращает: `List[LayerAttributeOrError]`

### API.GetLayerCombinationAttributes

Returns the detailed layer combination attributes identified by their GUIDs.

Параметры:
- `attributeIds`: List[AttributeIdWrapperItem]

Возвращает: `List[LayerCombinationAttributeOrError]`

### API.GetLineAttributes

Returns the detailed line attributes identified by their GUIDs.

Параметры:
- `attributeIds`: List[AttributeIdWrapperItem]

Возвращает: `List[LineAttributeOrError]`

### API.GetPenTableAttributes

Returns the detailed pen table attributes (including their pens) identified by their GUIDs.

Параметры:
- `attributeIds`: List[AttributeIdWrapperItem]

Возвращает: `List[PenTableAttributeOrError]`

### API.GetProfileAttributes

Returns the detailed profile attributes identified by their GUIDs.

Параметры:
- `attributeIds`: List[AttributeIdWrapperItem]

Возвращает: `List[ProfileAttributeOrError]`

### API.GetProfileAttributePreview

Returns the preview image of each requested profile attribute in a base64 string format.

Параметры:
- `attributeIds`: List[AttributeIdWrapperItem]
- `imageWidth`: int
- `imageHeight`: int
- `backgroundColor`: RGBColor (опционально) — A color model represented via its red, green and blue components.

Возвращает: `List[ImageOrError]`

### API.GetSurfaceAttributes

Returns the detailed surface attributes identified by their GUIDs.

Параметры:
- `attributeIds`: List[AttributeIdWrapperItem]

Возвращает: `List[SurfaceAttributeOrError]`

### API.GetZoneCategoryAttributes

Returns the detailed zone category attributes identified by their GUIDs.

Параметры:
- `attributeIds`: List[AttributeIdWrapperItem]

Возвращает: `List[ZoneCategoryAttributeOrError]`

## Навигатор и макеты

### API.GetNavigatorItemTree

Returns the tree of navigator items.

Параметры:
- `navigatorTreeId`: NavigatorTreeId — The identifier of a navigator item tree.

Возвращает: `NavigatorTree`

### API.GetPublisherSetNames

Returns the names of available publisher sets.

Параметры: нет.

Возвращает: `List[str]`

### API.RenameNavigatorItem

Renames an existing navigator item by specifying either the name or the ID, or both.

Параметры:
- `navigatorItemId`: NavigatorItemId — The identifier of a navigator item.
- `newName`: str (опционально)
- `newId`: str (опционально)

Возвращает: `None`

### API.MoveNavigatorItem

Moves the given navigator item under the <i>parentNavigatorItemId</i> in the navigator tree. If <i>previousNavigatorItemId</i> is not given then inserts it at the first place under the new parent. If it is given then inserts it after this navigator item.

Параметры:
- `navigatorItemIdToMove`: NavigatorItemId — The identifier of a navigator item.
- `parentNavigatorItemId`: NavigatorItemId — The identifier of a navigator item.
- `previousNavigatorItemId`: NavigatorItemId (опционально) — The identifier of a navigator item.

Возвращает: `None`

### API.DeleteNavigatorItems

Deletes items from navigator tree.

Параметры:
- `navigatorItemIds`: List[NavigatorItemIdWrapper] — Attributes:

Возвращает: `List[ExecutionResult]`

### API.CloneProjectMapItemToViewMap

Clones a project map item to the view map.

Параметры:
- `projectMapNavigatorItemId`: NavigatorItemId — The identifier of a navigator item.
- `parentNavigatorItemId`: NavigatorItemId — The identifier of a navigator item.

Возвращает: `NavigatorItemId`

### API.CreateViewMapFolder

Creates a view folder item at the given position in the navigator tree.

Параметры:
- `folderParameters`: FolderParameters — The parameters of a folder.
- `parentNavigatorItemId`: NavigatorItemId (опционально) — The identifier of a navigator item.
- `previousNavigatorItemId`: NavigatorItemId (опционально) — The identifier of a navigator item.

Возвращает: `NavigatorItemId`

### API.CreateLayout

Creates a new layout.

Параметры:
- `layoutName`: str
- `layoutParameters`: LayoutParameters — The parameters of the layout.
- `masterNavigatorItemId`: NavigatorItemId — The identifier of a navigator item.
- `parentNavigatorItemId`: NavigatorItemId — The identifier of a navigator item.

Возвращает: `NavigatorItemId`

### API.CreateLayoutSubset

Creates a new layout subset.

Параметры:
- `subsetParameters`: Subset — A set of options used to assign IDs to the layouts contained in the subset.
- `parentNavigatorItemId`: NavigatorItemId — The identifier of a navigator item.

Возвращает: `NavigatorItemId`

### API.GetLayoutSettings

Returns the parameters (settings) of the given layout.

Параметры:
- `layoutNavigatorItemId`: NavigatorItemId — The identifier of a navigator item.

Возвращает: `LayoutParameters`

### API.SetLayoutSettings

Sets the parameters (settings) of the given layout.

Параметры:
- `layoutParameters`: LayoutParameters — The parameters of the layout.
- `layoutNavigatorItemId`: NavigatorItemId — The identifier of a navigator item.

Возвращает: `None`

## Команды аддонов

### API.ExecuteAddOnCommand

Executes a command registered in an Add-On.

Параметры:
- `addOnCommandId`: AddOnCommandId — The identifier of an Add-On command.
- `addOnCommandParameters`: AddOnCommandParameters (опционально) — The input parameters of an Add-On command.

Возвращает: `AddOnCommandResponse`

### API.IsAddOnCommandAvailable

Checks if the command is available or not.

Параметры:
- `addOnCommandId`: AddOnCommandId — The identifier of an Add-On command.

Возвращает: `bool`
