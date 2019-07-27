import os
import configparser as conf

BASEDIR = os.path.dirname(__file__)

config = conf.ConfigParser()
config.optionxform = str
config_ini = os.path.join(BASEDIR, "config_tests.ini")
config.read(config_ini)
RESOURCES_FOLDER = os.path.join(BASEDIR, config['COMMON']['RESOURCES_FOLDER'])
EXPECTED_FOLDER = os.path.join(BASEDIR, config['COMMON']['EXPECTED_FOLDER'])
OUTPUT_FOLDER = os.path.join(BASEDIR, config['COMMON']['OUTPUT_FOLDER'])

GEO_IMAGE = os.path.join(RESOURCES_FOLDER,
                         config['COMMON']['GEO_IMAGE'])
OUTPUT_GEO_IMAGE = os.path.join(RESOURCES_FOLDER,
                                config['COMMON']['OUTPUT_GEO_IMAGE'])

# Test Majority Filter
HSHEDS_INPUT_MAJORITY = os.path.join(RESOURCES_FOLDER,
                                     config['INPUTS']['HSHEDS_MAJORITY'])
MAJORITY_OUTPUT = os.path.join(EXPECTED_FOLDER,
                               config['EXPECTED']['MAJORITY_FILTER'])

# Test Expand Filter
INPUT_EXPAND = os.path.join(RESOURCES_FOLDER,
                            config['INPUTS']['EXPAND_INPUT'])
EXPAND_OUTPUT = os.path.join(EXPECTED_FOLDER,
                             config['EXPECTED']['EXPAND_FILTER'])
# Test River Routing
HSHEDS_INPUT_RIVER_ROUTING = os.path.join(RESOURCES_FOLDER,
                                          config['INPUTS'][
                                              'HSHEDS_RIVER_ROUTING'])
MASK_INPUT_RIVER_ROUTING = os.path.join(RESOURCES_FOLDER,
                                        config['INPUTS'][
                                            'MASK_RIVERS_ROUTING'])
RIVER_ROUTING_EXPECTED = os.path.join(EXPECTED_FOLDER,
                                      config['EXPECTED']['RIVERS_ROUTED'])

# Test Quadratic Filter
SRTM_INPUT_QUADRATIC = os.path.join(RESOURCES_FOLDER,
                                    config['INPUTS']['SRTM_FOURIER_QUADRATIC'])

QUADRATIC_FILTER_EXPECTED = os.path.join(EXPECTED_FOLDER,
                                         config['EXPECTED'][
                                             'QUADRATIC_FILTER'])
# Test Nan Values Correction
HSHEDS_INPUT_NAN = os.path.join(RESOURCES_FOLDER,
                                config['INPUTS']['HSHEDS_INPUT_NAN'])
HSHEDS_NAN_CORRECTED = os.path.join(EXPECTED_FOLDER,
                                    config['EXPECTED']['HSHEDS_NAN_CORRECTED'])
# Test Isolated Pixels Filter
MASK_ISOLATED = os.path.join(RESOURCES_FOLDER,
                             config['INPUTS']['MASK_ISOLATED'])
MASK_ISOLATED_FILTERED = os.path.join(EXPECTED_FOLDER,
                                      config['EXPECTED'][
                                          'MASK_ISOLATED_FILTERED'])

# Test Filter Blanks Fourier

QUARTER_FOURIER = os.path.join(RESOURCES_FOLDER,
                               config['INPUTS']['QUARTER_FOURIER'])
FILTERED_FOURIER_1 = os.path.join(EXPECTED_FOLDER,
                                  config['EXPECTED']['FILTERED_FOURIER_1'])
FILTERED_FOURIER_2 = os.path.join(EXPECTED_FOLDER,
                                  config['EXPECTED']['FILTERED_FOURIER_2'])

# Test Mask Fourier Quarter
FIRST_QUARTER = os.path.join(RESOURCES_FOLDER,
                             config['INPUTS']['FIRST_QUARTER'])
FIRST_MASK_FOURIER = os.path.join(EXPECTED_FOLDER,
                                  config['EXPECTED']['FIRST_MASK_FOURIER'])

# Test Detect And Apply Fourier
SRTM_STRIPPED = os.path.join(RESOURCES_FOLDER,
                             config['INPUTS']['SRTM_STRIPPED'])
SRTM_WITHOUT_STRIPS = os.path.join(EXPECTED_FOLDER,
                                   config['EXPECTED']['SRTM_WITHOUT_STRIPS'])
SRTM_CORRECTED = os.path.join(OUTPUT_FOLDER,
                              config['OUTPUTS']['SRTM_CORRECTED'])
# Test Process SRTM
MASK_TREES = os.path.join(RESOURCES_FOLDER, config['INPUTS']['TREE_MASK'])
SRTM_PROCESSED = os.path.join(EXPECTED_FOLDER,
                              config['EXPECTED']['SRTM_PROCESSED'])

# Test Resample and Cut
HSHEDS_FILE_TIFF = os.path.join(RESOURCES_FOLDER,
                                config['INPUTS']['HSHEDS_FILE_TIFF'])
SHAPE_AREA_INTEREST_OVER = os.path.join(RESOURCES_FOLDER,
                                        config['INPUTS'][
                                            'SHAPE_AREA_INTEREST_OVER'])
HSHEDS_AREA_INTEREST = os.path.join(EXPECTED_FOLDER,
                                    config['EXPECTED']['HSHEDS_AREA_INTEREST'])
HSHEDS_AREA_INTEREST_OUTPUT = os.path.join(OUTPUT_FOLDER,
                                           config['OUTPUTS'][
                                               'HSHEDS_AREA_INTEREST_OUTPUT'])

# Test Get Shape Over Area
IMAGE_TEMP = os.path.join(RESOURCES_FOLDER, config['INPUTS']['IMAGE_TEMP'])
SHAPE_AREA_OVER = os.path.join(EXPECTED_FOLDER,
                               config['EXPECTED']['SHAPE_AREA_OVER'])
SHAPE_AREA_OVER_CREATED = os.path.join(OUTPUT_FOLDER,
                                       config['OUTPUTS'][
                                           'SHAPE_AREA_OVER_CREATED'])

# Test Get Lagoons
HYDRO_SHEDS = os.path.join(RESOURCES_FOLDER, config['INPUTS']['HYDRO_SHEDS'])
LAGOONS_DETECTED = os.path.join(EXPECTED_FOLDER,
                                config['EXPECTED']['LAGOONS_DETECTED'])

# Test Clipping Rivers Vector
RIVERS_VECTOR = os.path.join(RESOURCES_FOLDER,
                             config['INPUTS']['RIVERS_VECTOR'])
SHAPE_AREA_INTEREST_OVER = os.path.join(RESOURCES_FOLDER,
                                        config['INPUTS'][
                                            'SHAPE_AREA_INTEREST_OVER'])
RIVERS_CLIPPED = os.path.join(OUTPUT_FOLDER,
                              config['OUTPUTS']['RIVERS_CLIPPED'])
RIVERS_AREA = os.path.join(EXPECTED_FOLDER,
                           config['EXPECTED']['RIVERS_AREA'])

# Test Process Rivers
MASK_LAGOONS = os.path.join(RESOURCES_FOLDER, config['INPUTS']['MASK_LAGOONS'])
HSHEDS_NAN_CORRECTED = os.path.join(EXPECTED_FOLDER,
                                    config['EXPECTED']['HSHEDS_NAN_CORRECTED'])
RIVERS_AREA = os.path.join(EXPECTED_FOLDER, config['EXPECTED']['RIVERS_AREA'])

RIVERS_ROUTED_CLOSING = os.path.join(EXPECTED_FOLDER,
                                     config['EXPECTED'][
                                         'RIVERS_ROUTED_CLOSING'])
