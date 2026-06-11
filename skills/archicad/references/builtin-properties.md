# Встроенные свойства Archicad 25 (BuiltIn)

Всего: 527. Получено с живого Archicad 25 через `API.GetAllPropertyNames` (доступность зависит от типа элемента).

Использование: `GetPropertyIds` с `{"type": "BuiltIn", "nonLocalizedName": "<имя>"}`, затем `GetPropertyValuesOfElements`.

Самые ходовые: `General_NetVolume` (объём), `General_Area` (площадь), `General_Height`, `General_ElementID`, `General_TypeName`, `Zone_ZoneName`, `Zone_NetArea`, `Zone_ZoneCategoryCode`. Имени этажа среди встроенных свойств нет — вычисляй отметку этажа как `General_BottomElevationToProjectZero` − `General_BottomElevationToHomeStory`.

## AnalyticalModel (14)

- `AnalyticalModel_ConnectionRange`
- `AnalyticalModel_ConnectionRangeLength`
- `AnalyticalModel_CustomEdgeRelease`
- `AnalyticalModel_CustomEndRelease`
- `AnalyticalModel_EccentricityY`
- `AnalyticalModel_EccentricityZ`
- `AnalyticalModel_Generation`
- `AnalyticalModel_HoleFilteringByRules`
- `AnalyticalModel_OffsetByRules`
- `AnalyticalModel_OffsetY`
- `AnalyticalModel_OffsetZ`
- `AnalyticalModel_StretchByRules`
- `AnalyticalModel_UniformEdgeReleases`
- `AnalyticalModel_UniformEndReleases`

## Beam (24)

- `Beam_AnalyticalModelGeneration`
- `Beam_ConnectionRange`
- `Beam_ConnectionRangeLength`
- `Beam_CustomEndRelease`
- `Beam_EccentricityY`
- `Beam_EccentricityZ`
- `Beam_EndSurfaceArea`
- `Beam_HoleHeight`
- `Beam_HoleLevel`
- `Beam_HoleWidth`
- `Beam_HolesEdgeSurfaceArea`
- `Beam_HolesSurfaceArea`
- `Beam_HolesVolume`
- `Beam_LeftSurfaceArea`
- `Beam_LengthLeft`
- `Beam_LengthRight`
- `Beam_Offset`
- `Beam_OffsetByRules`
- `Beam_OffsetY`
- `Beam_OffsetZ`
- `Beam_RightSurfaceArea`
- `Beam_SlantAngle`
- `Beam_StretchByRules`
- `Beam_UniformEndReleases`

## BuildingMaterial (4)

- `BuildingMaterial_Description`
- `BuildingMaterial_ID`
- `BuildingMaterial_Manufacturer`
- `BuildingMaterial_Name`

## Category (4)

- `Category_Position`
- `Category_RenovationStatus`
- `Category_ShowOnRenovationFilter`
- `Category_StructuralFunction`

## Column (33)

- `Column_AnalyticalModelGeneration`
- `Column_ConnectionRange`
- `Column_ConnectionRangeLength`
- `Column_CoreDepth`
- `Column_CoreVolume`
- `Column_CoreWidth`
- `Column_CustomEndRelease`
- `Column_EccentricityY`
- `Column_EccentricityZ`
- `Column_GrossCoreBottomSurfaceArea`
- `Column_GrossCoreSideSurfaceArea`
- `Column_GrossCoreTopSurfaceArea`
- `Column_GrossCoreVolume`
- `Column_GrossVeneerBottomSurfaceArea`
- `Column_GrossVeneerSideSurfaceArea`
- `Column_GrossVeneerTopSurfaceArea`
- `Column_GrossVeneerVolume`
- `Column_MaximumHeight`
- `Column_MinimumHeight`
- `Column_NetCoreBottomSurfaceArea`
- `Column_NetCoreSideSurfaceArea`
- `Column_NetCoreTopSurfaceArea`
- `Column_NetVeneerBottomSurfaceArea`
- `Column_NetVeneerSideSurfaceArea`
- `Column_NetVeneerTopSurfaceArea`
- `Column_OffsetByRules`
- `Column_OffsetY`
- `Column_OffsetZ`
- `Column_PerimeterOfBase`
- `Column_SlantAngle`
- `Column_StretchByRules`
- `Column_UniformEndReleases`
- `Column_VeneerVolume`

## Component (10)

- `Component_ConditionalProjectedArea`
- `Component_ConditionalVolume`
- `Component_CrossSectionArea`
- `Component_CrossSectionHeight`
- `Component_CrossSectionWidth`
- `Component_GrossProjectedArea`
- `Component_GrossVolume`
- `Component_NetProjectedArea`
- `Component_NetVolume`
- `Component_Thickness`

## Construction (5)

- `Construction_CompositeName`
- `Construction_ProfileName`
- `Construction_RoofCropped`
- `Construction_RoofLevelNumber`
- `Construction_StructureType`

## CurtainWall (18)

- `CurtainWall_BoundarySurfaceArea`
- `CurtainWall_Length`
- `CurtainWall_LengthOfContourFrames`
- `CurtainWall_LengthOfCustomFrames`
- `CurtainWall_LengthOfFrames`
- `CurtainWall_LengthOfMainAxisFrames`
- `CurtainWall_LengthOfSecAxisFrames`
- `CurtainWall_PatternAngle`
- `CurtainWall_SlantAngle`
- `CurtainWall_SurfaceAreaOfPanels`
- `CurtainWall_SurfaceAreaOfPanelsE`
- `CurtainWall_SurfaceAreaOfPanelsN`
- `CurtainWall_SurfaceAreaOfPanelsNE`
- `CurtainWall_SurfaceAreaOfPanelsNW`
- `CurtainWall_SurfaceAreaOfPanelsS`
- `CurtainWall_SurfaceAreaOfPanelsSE`
- `CurtainWall_SurfaceAreaOfPanelsSW`
- `CurtainWall_SurfaceAreaOfPanelsW`

## General (73)

- `General_3DLength`
- `General_3DPerimeter`
- `General_Area`
- `General_BottomElevationToFirstReferenceLevel`
- `General_BottomElevationToHomeStory`
- `General_BottomElevationToProjectZero`
- `General_BottomElevationToSeaLevel`
- `General_BottomElevationToSecondReferenceLevel`
- `General_ConditionalBottomSurfaceArea`
- `General_ConditionalTopSurfaceArea`
- `General_ConditionalVolume`
- `General_CrossSectionAreaAtBeginCut`
- `General_CrossSectionAreaAtEndCut`
- `General_CrossSectionHeightAtBeginCut`
- `General_CrossSectionHeightAtBeginPerpendicular`
- `General_CrossSectionHeightAtEndCut`
- `General_CrossSectionHeightAtEndPerpendicular`
- `General_CrossSectionWidthAtBeginCut`
- `General_CrossSectionWidthAtBeginPerpendicular`
- `General_CrossSectionWidthAtEndCut`
- `General_CrossSectionWidthAtEndPerpendicular`
- `General_ElementID`
- `General_ElevationToFirstReferenceLevel`
- `General_ElevationToProjectZero`
- `General_ElevationToSeaLevel`
- `General_ElevationToSecondReferenceLevel`
- `General_ElevationToStory`
- `General_FloorPlanHolesPerimeter`
- `General_FloorPlanPerimeter`
- `General_FromZone`
- `General_FromZoneNumber`
- `General_GrossBottomSurfaceArea`
- `General_GrossEdgeSurfaceArea`
- `General_GrossTopSurfaceArea`
- `General_GrossVolume`
- `General_Height`
- `General_Holes3DPerimeter`
- `General_HomeOffset`
- `General_HotlinkAndElementID`
- `General_HotlinkMasterID`
- `General_InsulationSkinThickness`
- `General_LastIssueID`
- `General_LastIssueName`
- `General_LibraryPartName`
- `General_LinkedChanges`
- `General_Locked`
- `General_NetBottomSurfaceArea`
- `General_NetEdgeSurfaceArea`
- `General_NetTopSurfaceArea`
- `General_NetVolume`
- `General_OpeningNumber`
- `General_OwnerID`
- `General_RelatedZoneName`
- `General_RelatedZoneNumber`
- `General_SlantAngle`
- `General_StructureType`
- `General_SurfaceArea`
- `General_SurveyCoordinateX`
- `General_SurveyCoordinateY`
- `General_SurveyCoordinateZ`
- `General_Thickness`
- `General_ToZone`
- `General_ToZoneNumber`
- `General_TopElevationToFirstReferenceLevel`
- `General_TopElevationToHomeStory`
- `General_TopElevationToProjectZero`
- `General_TopElevationToSeaLevel`
- `General_TopElevationToSecondReferenceLevel`
- `General_TopLinkStory`
- `General_TopOffset`
- `General_Type`
- `General_UniqueID`
- `General_Width`

## Geometry (52)

- `Geometry_ColumnCoreDepth`
- `Geometry_ColumnCoreDiameter`
- `Geometry_ColumnCoreWidth`
- `Geometry_ColumnSlantAngle`
- `Geometry_ColumnVeneerThickness`
- `Geometry_ComponentCrossSectionArea`
- `Geometry_ComponentCrossSectionHeight`
- `Geometry_ComponentCrossSectionWidth`
- `Geometry_ComponentThickness`
- `Geometry_ConditionalBottomSurfaceArea`
- `Geometry_ConditionalTopSurfaceArea`
- `Geometry_CrossSectionAreaAtBeginCut`
- `Geometry_CrossSectionAreaAtEndCut`
- `Geometry_CrossSectionHeightAtBeginCut`
- `Geometry_CrossSectionHeightAtBeginPerpendicular`
- `Geometry_CrossSectionHeightAtEndCut`
- `Geometry_CrossSectionHeightAtEndPerpendicular`
- `Geometry_CrossSectionWidthAtBeginCut`
- `Geometry_CrossSectionWidthAtBeginPerpendicular`
- `Geometry_CrossSectionWidthAtEndCut`
- `Geometry_CrossSectionWidthAtEndPerpendicular`
- `Geometry_CurtainWallPanelOffset`
- `Geometry_CurtainWallSlantAngle`
- `Geometry_General3DLength`
- `Geometry_GeneralEdgeDefaultAngle`
- `Geometry_GeneralHeight`
- `Geometry_GeneralThickness`
- `Geometry_GeneralWidth`
- `Geometry_GrossBottomSurfaceArea`
- `Geometry_GrossEdgeSurfaceArea`
- `Geometry_GrossTopSurfaceArea`
- `Geometry_InvertedHeight`
- `Geometry_NetBottomSurfaceArea`
- `Geometry_NetEdgeSurfaceArea`
- `Geometry_NetTopSurfaceArea`
- `Geometry_ObjectLength`
- `Geometry_OpeningTotalThickness`
- `Geometry_ProfileHeight`
- `Geometry_ProfileWidth`
- `Geometry_RiserSlantAngle`
- `Geometry_RoofEavesOverhang`
- `Geometry_RoofPitch`
- `Geometry_ShellInclineAngle`
- `Geometry_StairDefaultWidth`
- `Geometry_StairGradient`
- `Geometry_StairInvalidHeight`
- `Geometry_StairMinHeadroomHeight`
- `Geometry_WallInsideSlantAngle`
- `Geometry_WallOpeningJambWidthOne`
- `Geometry_WallOpeningJambWidthTwo`
- `Geometry_WallOpeningRevealDepth`
- `Geometry_WallOutsideSlantAngle`

## IdAndCategories (15)

- `IdAndCategories_ElementID`
- `IdAndCategories_HotlinkAndElementID`
- `IdAndCategories_HotlinkMasterID`
- `IdAndCategories_LibraryPartName`
- `IdAndCategories_Locked`
- `IdAndCategories_Name`
- `IdAndCategories_OpeningCutSymbolName`
- `IdAndCategories_OpeningNumber`
- `IdAndCategories_OpeningUncutSymbolName`
- `IdAndCategories_ParentId`
- `IdAndCategories_RelatedZoneName`
- `IdAndCategories_RelatedZoneNumber`
- `IdAndCategories_UniqueID`
- `IdAndCategories_ZoneNumber`
- `IdAndCategories_ZoneStampName`

## Lamp (4)

- `Lamp_ColorBlue`
- `Lamp_ColorGreen`
- `Lamp_ColorRed`
- `Lamp_Intensity`

## Mesh (2)

- `Mesh_HoleSurfaceArea`
- `Mesh_SkirtLevel`

## ModelView (3)

- `ModelView_LayerName`
- `ModelView_LibraryPartMissing`
- `ModelView_MissingAttribute`

## Morph (4)

- `Morph_CastShadow`
- `Morph_FloorPlanAreaByStory`
- `Morph_ReceiveShadow`
- `Morph_VolumeByStory`

## ObjectLamp (2)

- `ObjectLamp_Length`
- `ObjectLamp_RotationAngle`

## Opening (16)

- `Opening_CenterHeight`
- `Opening_CenterHeightToProjectZero`
- `Opening_CenterHeightToWallBottom`
- `Opening_CenterHeightToWallTop`
- `Opening_CutSymbolName`
- `Opening_HeaderHeightToHomeStory`
- `Opening_HeaderHeightToProjectZero`
- `Opening_HeaderHeightToWallBottom`
- `Opening_HeaderHeightToWallTop`
- `Opening_IdOfLinkedElements`
- `Opening_SillHeightToHomeStory`
- `Opening_SillHeightToProjectZero`
- `Opening_SillHeightToWallBottom`
- `Opening_SillHeightToWallTop`
- `Opening_TotalThickness`
- `Opening_UncutSymbolName`

## OpeningFiller (1)

- `OpeningFiller_LibraryPartName`

## Positioning (31)

- `Positioning_BottomElevationToFirstReferenceLevel`
- `Positioning_BottomElevationToHomeStory`
- `Positioning_BottomElevationToProjectZero`
- `Positioning_BottomElevationToSeaLevel`
- `Positioning_BottomElevationToSecondReferenceLevel`
- `Positioning_ElevationToCurrentStory`
- `Positioning_ElevationToFirstReferenceLevel`
- `Positioning_ElevationToProjectZero`
- `Positioning_ElevationToSeaLevel`
- `Positioning_ElevationToSecondReferenceLevel`
- `Positioning_HeadHeight`
- `Positioning_HomeOffset`
- `Positioning_OpeningCenterHeightToHomeFloor`
- `Positioning_OpeningCenterHeightToProjectZero`
- `Positioning_OpeningCenterHeightToWallBottom`
- `Positioning_OpeningCenterHeightToWallTop`
- `Positioning_OpeningHeaderHeightToProjectZero`
- `Positioning_OpeningHeaderHeightToWallBottom`
- `Positioning_OpeningHeaderHeightToWallTop`
- `Positioning_OpeningSillHeightToProjectZero`
- `Positioning_OpeningSillHeightToWallBottom`
- `Positioning_OpeningSillHeightToWallTop`
- `Positioning_OpeningSubfloorThickness`
- `Positioning_SillHeight`
- `Positioning_TopElevationToFirstReferenceLevel`
- `Positioning_TopElevationToHomeStory`
- `Positioning_TopElevationToProjectZero`
- `Positioning_TopElevationToSeaLevel`
- `Positioning_TopElevationToSecondReferenceLevel`
- `Positioning_TopOffset`
- `Positioning_WallOpeningOrientation`

## Railing (1)

- `Railing_ReferenceLine2DLength`

## Revision (2)

- `Revision_LastIssueID`
- `Revision_LastIssueName`

## Roof (28)

- `Roof_AnalyticalModelGeneration`
- `Roof_CustomEdgeRelease`
- `Roof_DomeConnectionLength`
- `Roof_EavesLength`
- `Roof_EccentricityZ`
- `Roof_EndWallConnectionLength`
- `Roof_GablesLength`
- `Roof_GrossBottomSurfaceArea`
- `Roof_GrossEdgeSurfaceArea`
- `Roof_GrossTopSurfaceArea`
- `Roof_HipsLength`
- `Roof_HoleFilteringByRules`
- `Roof_HolesSurfaceArea`
- `Roof_HollowConnectionLength`
- `Roof_NetBottomSurfaceArea`
- `Roof_OffsetByRules`
- `Roof_OffsetZ`
- `Roof_OpeningsSurfaceArea`
- `Roof_PeaksLength`
- `Roof_Pitch`
- `Roof_RidgesLength`
- `Roof_RoofLevel`
- `Roof_SideWallConnectionLength`
- `Roof_StretchByRules`
- `Roof_Thickness`
- `Roof_UniformEdgeReleases`
- `Roof_ValleysLength`
- `Roof_VerticalThickness`

## RulesAndStandards (4)

- `RulesAndStandards_StairMaximumRiserHeightByRule`
- `RulesAndStandards_StairMaximumTreadDepthByRule`
- `RulesAndStandards_StairMinimumRiserHeightByRule`
- `RulesAndStandards_StairMinimumTreadDepthByRule`

## Shell (23)

- `Shell_ConditionalSurfaceAreaOfOppositeSide`
- `Shell_DistortionAngle`
- `Shell_DomeConnectionLength`
- `Shell_EavesLength`
- `Shell_EndAngle`
- `Shell_EndWallConnectionLength`
- `Shell_GablesLength`
- `Shell_GrossSurfaceAreaOfEdges`
- `Shell_GrossSurfaceAreaOfOppositeSide`
- `Shell_GrossSurfaceAreaOfReferenceSide`
- `Shell_HipsLength`
- `Shell_HolesSurfaceArea`
- `Shell_HollowConnectionLength`
- `Shell_NetSurfaceAreaOfEdges`
- `Shell_NetSurfaceAreaOfOppositeSide`
- `Shell_NetSurfaceAreaOfReferenceSide`
- `Shell_OpeningsSurfaceArea`
- `Shell_PeaksLength`
- `Shell_RevolutionAngle`
- `Shell_RidgesLength`
- `Shell_SideWallConnectionLength`
- `Shell_StartAngle`
- `Shell_ValleysLength`

## Skylight (12)

- `Skylight_AcousticRating`
- `Skylight_CurbHeight`
- `Skylight_FireRating`
- `Skylight_HeaderHeight`
- `Skylight_MarkerText`
- `Skylight_OpeningArea`
- `Skylight_OpeningVolume`
- `Skylight_OpeningWHSize`
- `Skylight_OpeningWHTSize`
- `Skylight_SillHeaderValue`
- `Skylight_SillHeight`
- `Skylight_Thickness`

## Slab (18)

- `Slab_AnalyticalModelGeneration`
- `Slab_BottomElevation`
- `Slab_ConditionalTopSurfaceArea`
- `Slab_CustomEdgeRelease`
- `Slab_EccentricityZ`
- `Slab_GrossBottomSurfaceArea`
- `Slab_GrossBottomSurfaceAreaWithHoles`
- `Slab_GrossEdgeSurfaceArea`
- `Slab_GrossEdgeSurfaceAreaWithHoles`
- `Slab_GrossTopSurfaceArea`
- `Slab_GrossTopSurfaceAreaWithHoles`
- `Slab_HoleFilteringByRules`
- `Slab_HolesSurfaceArea`
- `Slab_OffsetByRules`
- `Slab_OffsetZ`
- `Slab_StretchByRules`
- `Slab_TopElevation`
- `Slab_UniformEdgeReleases`

## Stair (12)

- `Stair_DefaultGoing`
- `Stair_DefaultRiserHeight`
- `Stair_DefaultRiserSlantAngle`
- `Stair_FlightWidth`
- `Stair_FrontSurfaceArea`
- `Stair_Gradient`
- `Stair_MaximumGoingByRule`
- `Stair_MaximumRiserHeightByRule`
- `Stair_MinHeadroomHeight`
- `Stair_MinimumGoingByRule`
- `Stair_MinimumRiserHeightByRule`
- `Stair_WalkingLineLength`

## SurfaceAndMaterials (2)

- `SurfaceAndMaterials_ComponentBuildingMaterialID`
- `SurfaceAndMaterials_ComponentBuildingMaterialName`

## Wall (46)

- `Wall_AirThickness`
- `Wall_AnalyticalHoleInsideSurfaceArea`
- `Wall_AnalyticalHoleOutsideSurfaceArea`
- `Wall_AnalyticalHoleVolume`
- `Wall_AnalyticalModelGeneration`
- `Wall_AverageLength`
- `Wall_CenterLength`
- `Wall_ColumnVolumeNotCalculated`
- `Wall_ConditionalInsideLength`
- `Wall_ConditionalInsideSkinVolume`
- `Wall_ConditionalInsideSurfaceArea`
- `Wall_ConditionalOutsideLength`
- `Wall_ConditionalOutsideSkinVolume`
- `Wall_ConditionalOutsideSurfaceArea`
- `Wall_CustomEdgeRelease`
- `Wall_DoorSurfaceArea`
- `Wall_DoorWidth`
- `Wall_EccentricityZ`
- `Wall_EmptyHolesSurfaceArea`
- `Wall_EndThickness`
- `Wall_GrossInsideSurfaceArea`
- `Wall_GrossOutsideSurfaceArea`
- `Wall_HoleFilteringByRules`
- `Wall_InsideLength`
- `Wall_InsideMaximumHeight`
- `Wall_InsideMinimumHeight`
- `Wall_InsideSkinVolume`
- `Wall_InsideSlantAngle`
- `Wall_InsideThickness`
- `Wall_MaximumHeight`
- `Wall_MinimumHeight`
- `Wall_NetInsideSurfaceArea`
- `Wall_NetOutsideSurfaceArea`
- `Wall_OffsetByRules`
- `Wall_OffsetZ`
- `Wall_OutsideLength`
- `Wall_OutsideMaximumHeight`
- `Wall_OutsideMinimumHeight`
- `Wall_OutsideSkinVolume`
- `Wall_OutsideSlantAngle`
- `Wall_OutsideThickness`
- `Wall_ReferenceLineLength`
- `Wall_StretchByRules`
- `Wall_UniformEdgeReleases`
- `Wall_WindowSurfaceArea`
- `Wall_WindowWidth`

## WindowDoor (37)

- `WindowDoor_AcousticRating`
- `WindowDoor_EgressDimension`
- `WindowDoor_FireRating`
- `WindowDoor_GrossSurfaceArea`
- `WindowDoor_GrossVolume`
- `WindowDoor_HeadHeightFromAnchor`
- `WindowDoor_LeafDimension`
- `WindowDoor_MarkerText`
- `WindowDoor_NominalOppositeRevealSideHeight`
- `WindowDoor_NominalOppositeRevealSideSurfaceArea`
- `WindowDoor_NominalOppositeRevealSideWidth`
- `WindowDoor_NominalRevealSideHeight`
- `WindowDoor_NominalRevealSideSurfaceArea`
- `WindowDoor_NominalRevealSideWidth`
- `WindowDoor_OpeningVolume`
- `WindowDoor_OppositeRevealSideHeadHeight`
- `WindowDoor_OppositeRevealSideHeight`
- `WindowDoor_OppositeRevealSideSillHeight`
- `WindowDoor_OppositeRevealSideSurfaceArea`
- `WindowDoor_OppositeRevealSideWidth`
- `WindowDoor_Orientation`
- `WindowDoor_RevealDimension`
- `WindowDoor_RevealSideHeadHeight`
- `WindowDoor_RevealSideHeight`
- `WindowDoor_RevealSideSillHeight`
- `WindowDoor_RevealSideSurfaceArea`
- `WindowDoor_RevealSideWidth`
- `WindowDoor_SillHeaderValueFromAnchor`
- `WindowDoor_SillHeightFromAnchor`
- `WindowDoor_SurfaceArea`
- `WindowDoor_Thickness`
- `WindowDoor_UnitDimension`
- `WindowDoor_WHSize`
- `WindowDoor_WHTSize`
- `WindowDoor_WallFill`
- `WindowDoor_WallHoleDimension`
- `WindowDoor_WallThickness`

## Zone (27)

- `Zone_AreaReducement`
- `Zone_CalculatedArea`
- `Zone_DoorsSurfaceArea`
- `Zone_DoorsWidth`
- `Zone_ExtractedColumnArea`
- `Zone_ExtractedCurtainWallArea`
- `Zone_ExtractedFillArea`
- `Zone_ExtractedLowArea`
- `Zone_ExtractedWallArea`
- `Zone_FloorThickness`
- `Zone_MeasuredArea`
- `Zone_NetArea`
- `Zone_NetPerimeter`
- `Zone_Perimeter`
- `Zone_ReducedArea`
- `Zone_TotalExtractedArea`
- `Zone_UniformSurface`
- `Zone_WallInsetBackSideSurfaceArea`
- `Zone_WallInsetSideSurfaceArea`
- `Zone_WallInsetTopSurfaceArea`
- `Zone_WallsPerimeter`
- `Zone_WallsSurfaceArea`
- `Zone_WindowsSurfaceArea`
- `Zone_WindowsWidth`
- `Zone_ZoneCategoryCode`
- `Zone_ZoneName`
- `Zone_ZoneNumber`
