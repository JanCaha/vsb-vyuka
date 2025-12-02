import arcpy

# projekt v daném adresáři
project = arcpy.mp.ArcGISProject(r"C:\Users\user\Documents\ArcGIS\Projects\MyProject2\MyProject2.aprx")

# informace o projektu
print(project.dateSaved)
print(project.filePath)
print(project.activeMap)
print(project.defaultGeodatabase)

# výběr první mapy
project_map = project.listMaps()[0]

# informace o mapě
print(project_map.name)
# vrstvy v mapě
layers = project_map.listLayers()

# informace o vrstvách
for layer in layers:
    print(f"{layer.name} - " f"raster: {layer.isRasterLayer}, vector: {layer.isFeatureLayer}")

# extrakce první vrstvy - očekáváme vektorová data
vector_layer = layers[0]
# extrakce symbologie vrstvy
sym = vector_layer.symbology

# pokud existuje renderer a není typu GraduatedColorsRenderer, tak ho změníme na GraduatedColorsRenderer
if hasattr(vector_layer.symbology, "renderer"):
    if vector_layer.symbology.renderer.type != "GraduatedColorsRenderer":
        print("Updating renderer")
        # úprava parametrů rendereru
        sym.updateRenderer("GraduatedColorsRenderer")
        sym.renderer.classificationField = "Shape_Area"
        sym.renderer.breakCount = 10
        sym.renderer.classificationMethod = "Quantile"
        sym.renderer.colorRamp = project.listColorRamps("Cyan to Purple")[0]
        # vložení symbologie zpět do vrstvy
        vector_layer.symbology = sym
    else:
        print("Render already set to graduated colors")

# uložení upraveného projektu
project.save()
