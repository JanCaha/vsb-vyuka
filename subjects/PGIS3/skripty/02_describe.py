# ukázka použití funkce arcpy.Describe()
import arcpy
import utils

utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

desc = arcpy.Describe(arcpy.env.workspace)

print(desc)

print(desc.baseName)
print(desc.children)
print(desc.dataElementType)
print(desc.dataType)
print(desc.name)
print(desc.path)

print(desc.workspaceType)
print(desc.release)

print("*" * 50)

desc_fc = arcpy.Describe("Wetlands")

print(desc_fc.dataType)
print(desc_fc.name)
print(desc_fc.path)

print(desc_fc.featureType)
print(desc_fc.hasSpatialIndex)
print(desc_fc.shapeType)

if hasattr(desc_fc, "size"):
    print(desc_fc.size)
else:
    print("No size for object.")

print("*" * 50)

desc_raster = arcpy.Describe("DEM")

print(desc_raster.name)
print(desc_raster.path)

print(desc_raster.bandCount)
print(desc_raster.compressionType)
print(desc_raster.format)

print("*" * 50)

desc_raster_band = arcpy.Describe("DEM/Band_1")

print(desc_raster_band.name)
print(desc_raster_band.path)

print(desc_raster_band.height)
print(desc_raster_band.width)
print(desc_raster_band.noDataValue)
print(desc_raster_band.pixelType)
