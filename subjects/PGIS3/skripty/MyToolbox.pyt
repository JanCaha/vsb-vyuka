# -*- coding: utf-8 -*-

from pathlib import Path

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Můj Toolbox"
        self.alias = "toolbox"

        # tools as classes
        self.tools = [Tool]


class Tool:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Můj nástroj"
        self.description = "Nějaký text"

    def getParameterInfo(self):
        """Define the tool parameters."""
        param0 = arcpy.Parameter(
            displayName="Vstupní prvky",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input",
        )

        param1 = arcpy.Parameter(
            displayName="Vybrané pole k vymazání v kopii dat",
            name="selected_field",
            datatype="Field",
            parameterType="Required",
            direction="Input",
        )

        # závislost na prvním parametru
        param1.parameterDependencies = [param0.name]
        param1.filter.list = ["Short", "Long", "Single", "Double"]

        param2 = arcpy.Parameter(
            displayName="Vybrané pole pro vykreslení kategorií",
            name="render_field",
            datatype="Field",
            parameterType="Required",
            direction="Input",
        )

        # závislost na prvním parametru
        param2.parameterDependencies = [param0.name]
        param2.filter.list = ["Short", "Long", "Single", "Double"]

        param3 = arcpy.Parameter(
            displayName="Výstupní prvky",
            name="out_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Output",
        )

        return [param0, param1, param2, param3]

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        inFeatures = parameters[0].valueAsText

        if not inFeatures:
            parameters[0].setErrorMessage("Vstupní prvky nejsou zadány.")
            return

        layer_desc = arcpy.Describe(inFeatures)

        # chybové zprávy pro dané podmínky
        if layer_desc.shapeType != "Point":
            parameters[0].setErrorMessage("Vrstva neobsahuje bodová data.")
        else:
            parameters[0].clearMessage()

        if parameters[1].valueAsText and parameters[2].valueAsText:
            if parameters[1].valueAsText == parameters[2].valueAsText:
                parameters[2].setErrorMessage("Pole pro vykreslení musí být jiné než pole určené ke smazání.")
            else:
                parameters[2].clearMessage()
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # načtení parametrů jako textu
        inFeatures = parameters[0].valueAsText
        field_to_delete = parameters[1].valueAsText
        render_field = parameters[2].valueAsText
        outFeatureClass = parameters[3].valueAsText

        # messages
        arcpy.AddMessage("Nástroj běží.")
        arcpy.AddMessage(f"Vstupní data {inFeatures}")
        arcpy.AddMessage(f"Výstupní data {outFeatureClass}")
        arcpy.AddMessage(f"Pole pro smazání {field_to_delete}")
        arcpy.AddMessage(f"Pole pro vykreslení {render_field}")

        # zpráva typu warning
        arcpy.AddWarning("Zkušební warning")

        # tělo nástroje, hlavní část kódu
        # zde můžou být cykly, podmínky a další logika nástroje - např. iterace přes prvky vrstvy
        try:
            arcpy.management.Copy(inFeatures, outFeatureClass)
        except arcpy.ExecuteError:
            arcpy.AddError(f"Chyba při kopírování dat.\n\n{arcpy.GetMessages(2)}")

        try:
            arcpy.management.DeleteField(outFeatureClass, [field_to_delete])
        except arcpy.ExecuteError:
            arcpy.AddError(f"Chyba při mazání vybraného pole.\n\n{arcpy.GetMessages(2)}")

        # chybová zpráva, která ukončí nástroj - zde skrytá za podmínkou, která nemůže nastat
        if False:
            arcpy.AddError("Chyba")

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        out_feature_class = parameters[3].valueAsText
        render_field = parameters[2].valueAsText

        project = arcpy.mp.ArcGISProject("CURRENT")
        # project netřeba kontrolovat nástroj běží z ArcGIS, takže nějaký projekt bude vždy dostupný

        active_map = project.activeMap
        # kontrola, zda je aktivní mapa dostupná - to už pravda být nemusí, v projektu nemusí nutně existovat
        if not active_map:
            arcpy.AddWarning("Není aktivní mapa. Renderer nelze automaticky nastavit.")
            return

        output_layer_name = Path(out_feature_class).name
        output_layers = active_map.listLayers(output_layer_name)
        if not output_layers:
            arcpy.AddWarning("Výstupní vrstva nebyla v mapě nalezena. Renderer nebyl změněn.")
            return

        output_layer = output_layers[0]
        symbology = output_layer.symbology

        if not hasattr(symbology, "renderer"):
            arcpy.AddWarning("Vrstva nepodporuje renderer. Renderer nelze nastavit.")
            return

        color_ramp = project.listColorRamps("Cyan to Purple")[0]
        if not color_ramp:
            arcpy.AddError("Barevná škála 'Cyan to Purple' nebyla v projektu nalezena.")
            return

        try:
            symbology.updateRenderer("GraduatedColorsRenderer")
            symbology.renderer.classificationField = render_field
            symbology.renderer.breakCount = 5
            symbology.renderer.classificationMethod = "Quantile"
            symbology.renderer.colorRamp = color_ramp
            output_layer.symbology = symbology
            arcpy.AddMessage("Renderer výstupu byl nastaven na Graduated Colors.")
        except arcpy.ExecuteError:
            arcpy.AddError("Chyba při nastavování rendereru výstupní vrstvy.")
            arcpy.AddError(arcpy.GetMessages())
            raise

        return
