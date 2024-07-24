"""
Model exported as python.
Name : LST_Landsat08
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


class Lst_landsat08(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # TIR
        self.addParameter(QgsProcessingParameterRasterLayer('b10', 'B10', defaultValue=None))
        # RED
        self.addParameter(QgsProcessingParameterRasterLayer('b4', 'B4', defaultValue=None))
        # NIR
        self.addParameter(QgsProcessingParameterRasterLayer('b5', 'B5', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('roi', 'ROI', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Ndvi', 'NDVI', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Lst', 'LST', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(9, model_feedback)
        results = {}
        outputs = {}

        # TOABT
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': '(1321.0789 / ( ln ( ( 774.8853 / ( ( "B10@1" * 0.000342 ) + 0.1 ) ) + 1 ) ))- 273.15',
            'EXTENT': None,
            'LAYERS': parameters['b10'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Toabt'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # NDVI
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': ' ( "B5@1" - "B4@1" )  /  ( "B5@1" + "B4@1" ) ',
            'EXTENT': None,
            'LAYERS': [parameters['b4'],parameters['b5']],
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

        # PV
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': '(("\'Output\' from algorithm \'NDVI\'@1"  - 0.2) / (0.8  -  0.2)) ^ 2',
            'EXTENT': None,
            'LAYERS': outputs['Ndvi']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pv'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Set layer style_NDVI
        alg_params = {
            'INPUT': outputs['ClipRasterByMaskLayer_ndvi']['OUTPUT'],
            'STYLE': 'X:\\Master II GISience\\Project Work Finale\\QGIS\\NDVI_style_new.qml'
        }
        outputs['SetLayerStyle_ndvi'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # E
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': '0.004 * "\'Output\' from algorithm \'PV\'@1" + 0.986',
            'EXTENT': None,
            'LAYERS': outputs['Pv']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['E'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # LST
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': '"\'Output\' from algorithm \'TOABT\'@1"/(1+((10.895 *"\'Output\' from algorithm \'TOABT\'@1"/14388)*ln("\'Output\' from algorithm \'E\'@1")))',
            'EXTENT': None,
            'LAYERS': [outputs['E']['OUTPUT'],outputs['Toabt']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Lst'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
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

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Set layer style_LST
        alg_params = {
            'INPUT': outputs['ClipRasterByMaskLayer_lst']['OUTPUT'],
            'STYLE': 'X:\\Master II GISience\\Project Work Finale\\QGIS\\LST_style_new.qml'
        }
        outputs['SetLayerStyle_lst'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'LST_Landsat08'

    def displayName(self):
        return 'LST_Landsat08'

    def group(self):
        return 'Raster calculation for LST and NDVI'

    def groupId(self):
        return 'Raster calculation for LST and NDVI'

    def createInstance(self):
        return Lst_landsat08()
