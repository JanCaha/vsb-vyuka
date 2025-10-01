# ukázka funkcí pro výpis prvků
import arcpy
import utils

# vypis všech env proměnných
env_variables = arcpy.ListEnvironments()
print(env_variables)

# nastavení workspace
utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

# výpis konkrétní env proměnné
print(arcpy.env["workspace"])
print(arcpy.env.workspace)

# reset env proměnných
arcpy.ResetEnvironments()
print(arcpy.env.workspace)

# znovu nastavení workspace
utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

# výpis všech rastrů ve workspace
rasters = arcpy.ListRasters()

print(rasters)

# výpis všech vektorů ve workspace se specifickým vzorem v názvu
vectors = arcpy.ListFeatureClasses("*_P*")

print(vectors)
