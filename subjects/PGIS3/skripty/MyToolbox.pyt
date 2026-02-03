# -*- coding: utf-8 -*-

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
            displayName="Vybrané pole",
            name="selected_field",
            datatype="Field",
            parameterType="Required",
            direction="Input",
        )

        # závislost na prvním parametru
        param1.parameterDependencies = [param0.name]
        param1.filter.list = ["Short", "Long", "Float"]

        param2 = arcpy.Parameter(
            displayName="Výstupní prvky",
            name="out_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Output",
        )

        return [param0, param1, param2]

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

        layer_desc = arcpy.Describe(inFeatures)

        # chybové zprávy pro dané podmínky
        if layer_desc.shapeType == "Point":
            parameters[0].setErrorMessage("Vrstva neobsahuje bodová data.")
        else:
            parameters[0].clearMessage()
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # načtení parametrů jako textu
        inFeatures = parameters[0].valueAsText
        outFeatureClass = parameters[2].valueAsText
        field = parameters[1].valueAsText

        # messages
        arcpy.AddMessage("Nástroj běží.")
        arcpy.AddMessage(f"Vstupní data {inFeatures}")
        arcpy.AddMessage(f"Výstupní data {outFeatureClass}")

        # zpráva typu warning
        arcpy.AddWarning("Zkušební warning")

        # tělo nástroje, hlavní část kódu
        arcpy.Copy_management(inFeatures, outFeatureClass)

        # chybová zpráva, která ukončí nástroj - zde skrytá za podmínkou, která nemůže nastat
        if False:
            arcpy.AddError("Chyba")

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
