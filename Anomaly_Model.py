"""
Model exported as python.
Name : Anomaly_model
Group : 
With QGIS : 33601
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterRasterDestination
import processing


class Anomaly_model(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('month', 'Month', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('month_mean', 'Month_mean', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Monthly_anomaly', 'Monthly_Anomaly', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Raster calculator
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTENT_OPT': 0,  # Ignore
            'EXTRA': None,
            'FORMULA': 'A-B',
            'INPUT_A': parameters['month'],
            'INPUT_B': parameters['month_mean'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': None,
            'PROJWIN': None,
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['Monthly_anomaly']
        }
        outputs['RasterCalculator'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Monthly_anomaly'] = outputs['RasterCalculator']['OUTPUT']
        return results

    def name(self):
        return 'Anomaly_model'

    def displayName(self):
        return 'Anomaly_model'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Anomaly_model()
