# ukázka funkcí pro výpis prvků
import arcpy
import utils

# vypis všech env proměnných
env_variables = arcpy.ListEnvironments()
print("Existující proměnné prostředí:")
print(env_variables)
print("")

# nastavení workspace
utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

# výpis konkrétní env proměnné
print("Workspace nastaven na:")
print(arcpy.env["workspace"])
print(arcpy.env.workspace)
print("")

# reset env proměnných
arcpy.ResetEnvironments()
print("Po resetu env proměnných je workspace:")
print(arcpy.env.workspace)
print("")

# znovu nastavení workspace
utils.setup_env("ProgrammingPro/Databases/Trippville_GIS.gdb")

# výpis všech rastrů ve workspace
rasters = arcpy.ListRasters()

print("Existující rastry ve workspace:")
print(rasters)
print("")

# výpis všech vektorů ve workspace se specifickým vzorem v názvu
vectors = arcpy.ListFeatureClasses("*_P*")

print("Existující vektory ve workspace se specifickým vzorem v názvu:")
print(vectors)
print("")
