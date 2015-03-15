"""
UAV Toolbox
"""

# Dependencies
import arcpy
import os
import cv2
import numpy as np
import scipy as sp
import sklearn

class Toolbox(object):
    def __init__(self):
        """
	Define the toolbox (the name of the toolbox is the name of the .pyt file).
	"""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool, RGB2HSV]

class Tool(object):
    def __init__(self):
        """
	Define the tool (tool name is the name of the class).
	"""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """
	Define parameter definitions
	"""
        params = None
        return params

    def isLicensed(self):
        """
	Set whether tool is licensed to execute.
	"""
        return True

    def updateParameters(self, parameters):
        """
	Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed.
	"""
        return

    def updateMessages(self, parameters):
        """
	Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation.
	"""
        return

    def execute(self, parameters, messages):
        """
	The source code of the tool.
	"""
        return

class RGB2HSV(object):
    def __init__(self):
        """
	Define the tool (tool name is the name of the class).
	"""
        self.label = "RGB to HSV"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """
	Define parameter definitions
	"""

        # Input
        input_raster = arcpy.Parameter(
            displayName="Input RGB Raster",
            name="in_raster",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input")

        # Output
        output_raster = arcpy.Parameter(
            displayName="Output HSV Raster",
            name="out_raster",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Output")

        output_raster.parameterDependencies = [input_raster.name]
        output_raster.schema.clone = True

        params = [input_raster, output_raster]
        return params

    def isLicensed(self):
        """
	Set whether tool is licensed to execute.
	"""
        return True

    def updateParameters(self, parameters):
        """
	Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed.
	"""
        return

    def updateMessages(self, parameters):
        """
	Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation.
	"""
        return

    def execute(self, parameters, messages):
        """
	The source code of the tool.
	"""
        input_raster = parameters[0].valueAsText
        output_raster = parameters[1].valueAsText
        arcpy.AddMessage("Input Raster: %s" % input_raster)
        arcpy.AddMessage("Output Raster: %s" % output_raster)

        RGB_array = arcpy.RasterToNumPyArray(input_raster)
        R_array = RGB_array[0,:,:]
        G_array = RGB_array[1,:,:]
        B_array = RGB_array[2,:,:]
        RGB_array = np.dstack((R_array, G_array, B_array))
        HSV_array = cv2.cvtColor(RGB_array, cv2.COLOR_RGB2HSV)
        arcpy.AddMessage("Generated HSV")

        Ymin = float(str(arcpy.GetRasterProperties_management(input_raster, "BOTTOM")))  
        Xmin = float(str(arcpy.GetRasterProperties_management(input_raster, "LEFT")))  
        Xmax = float(str(arcpy.GetRasterProperties_management(input_raster, "RIGHT")))  
        Ymax = float(str(arcpy.GetRasterProperties_management(input_raster, "TOP")))  
        Xcell = float(str(arcpy.GetRasterProperties_management(input_raster, "CELLSIZEX")))
        Ycell = float(str(arcpy.GetRasterProperties_management(input_raster, "CELLSIZEY")))
        xymin = arcpy.Point(Xmin, Ymin)  
        HSV_raster = arcpy.NumPyArrayToRaster(HSV_array, xymin, Xcell, Ycell)
        #HSV_raster.save(output_raster)
        #arcpy.CopyRaster_management(HSV_raster, output_raster)
        return
