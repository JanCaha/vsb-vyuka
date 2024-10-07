# ukázka funkcí pro výpis prvků
import arcpy
import utils

utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

rasters = arcpy.ListRasters()

print(rasters)

vectors = arcpy.ListFeatureClasses("*_P*")

print(vectors)

env_variables = arcpy.ListEnvironments()

print(env_variables)

print(arcpy.env["workspace"])
print(arcpy.env.workspace)

arcpy.ResetEnvironments()
print(arcpy.env.workspace)
