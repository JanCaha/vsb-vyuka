import arcpy

# projekt v daném adresáři
project = arcpy.mp.ArcGISProject(r"C:\Users\user\Documents\ArcGIS\Projects\MyProject2\MyProject2.aprx")

# nalezení prvního layoutu
project_layout = project.listLayouts()[0]

# nalezení textových elementů a uložení prvního do proměnné
texts = project_layout.listElements("TEXT_ELEMENT")
text = texts[0]

# změny v textovém elementu
text.text = "Upravený text"
text.textSize = text.textSize + 5
text.elementPositionX = text.elementPositionX - 150

# export layoutu (upraveného) do PDF - ArcGIS Pro verze 3.x
project_layout.exportToPDF(r"C:\Users\user\Projekty\PGIS3\PDF_output1.pdf", 300, "BEST")

# tvorba nového formátu pro export - ArcGIS Pro verze 3.4 a novější
pdf = arcpy.mp.CreateExportFormat("PDF", r"C:\Users\user\Projekty\PDF_output1.pdf")
project_layout.export(pdf)

# úprava parametrů pro export
pdf.resolution = 300
pdf.filePath = r"C:\Users\user\Projekty\PDF_output2.pdf"

project_layout.export(pdf)

# je otázkou, zda-li chceme změny v projektu uložit
# project.save()
