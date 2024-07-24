"""
Model exported as python.
Name : LST_Landsat_7
Group : Raster calculation for LST and NDVI
With QGIS : 33601
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterDestination
import processing


class Lst_landsat_7(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # RED
        self.addParameter(QgsProcessingParameterRasterLayer('b3', 'B3', defaultValue=None))
        # NIR
        self.addParameter(QgsProcessingParameterRasterLayer('b4', 'B4', defaultValue=None))
        # TIR
        self.addParameter(QgsProcessingParameterRasterLayer('b6', 'B6', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('roi', 'ROI', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Lst', 'LST', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Ndvi', 'NDVI', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        results = {}
        outputs = {}

        # L
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': '((12.650 - 3.200) / (255 -  1)) * ("B6@1" -  1) + 3.200',
            'EXTENT': None,
            'LAYERS': parameters['b6'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['L'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # NDVI
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': ' ( "B4@1" - "B3@1" )  /  ( "B4@1" + "B3@1" ) ',
            'EXTENT': None,
            'LAYERS': [parameters['b3'],parameters['b4']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Clip raster by mask layer_NDVI
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': None,
            'INPUT': outputs['Ndvi']['OUTPUT'],
            'KEEP_RESOLUTION': False,
            'MASK': parameters['roi'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': None,
            'SET_RESOLUTION': False,
            'SOURCE_CRS': 'ProjectCrs',
            'TARGET_CRS': 'ProjectCrs',
            'TARGET_EXTENT': None,
            'X_RESOLUTION': None,
            'Y_RESOLUTION': None,
            'OUTPUT': parameters['Ndvi']
        }
        outputs['ClipRasterByMaskLayer_ndvi'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Ndvi'] = outputs['ClipRasterByMaskLayer_ndvi']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Set layer style
        alg_params = {
            'INPUT': outputs['Ndvi']['OUTPUT'],
            'STYLE': 'X:\\Master II GISience\\Project Work Finale\\QGIS\\NDVI_style_new.qml'
        }
        outputs['SetLayerStyle'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # LST
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': '(1282.71 / ln (666.09 / "\'Output\' from algorithm \'L\'@1") + 1)  -  273.15',
            'EXTENT': None,
            'LAYERS': outputs['L']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Lst'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Clip raster by mask layer_LST
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': None,
            'INPUT': outputs['Lst']['OUTPUT'],
            'KEEP_RESOLUTION': False,
            'MASK': parameters['roi'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': None,
            'SET_RESOLUTION': False,
            'SOURCE_CRS': 'ProjectCrs',
            'TARGET_CRS': 'ProjectCrs',
            'TARGET_EXTENT': None,
            'X_RESOLUTION': None,
            'Y_RESOLUTION': None,
            'OUTPUT': parameters['Lst']
        }
        outputs['ClipRasterByMaskLayer_lst'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Lst'] = outputs['ClipRasterByMaskLayer_lst']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Set layer style
        alg_params = {
            'INPUT': outputs['Lst']['OUTPUT'],
            'STYLE': 'X:\\Master II GISience\\Project Work Finale\\QGIS\\LST_style_new.qml'
        }
        outputs['SetLayerStyle'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'LST_Landsat_7'

    def displayName(self):
        return 'LST_Landsat_7'

    def group(self):
        return 'Raster calculation for LST and NDVI'

    def groupId(self):
        return 'Raster calculation for LST and NDVI'

    def createInstance(self):
        return Lst_landsat_7()
