__author__ = "Cristian Guerrero Cordova"
__copyright__ = "Copyright 2018"
__credits__ = ["Cristian Guerrero Cordova"]
__version__ = "0.1"
__email__ = "cguerrerocordova@gmail.com"
__status__ = "Production"

import numpy as np
from osgeo import gdal
from scipy import ndimage
import utilsDEM as utDEM
from settings import *


class HydroDEMProcess(object):

    def __init__(self):
        """
        class constructor
        """

    def start(self):
        """
        starts Report generation
        :param cmd_line: unix command line
        :type cmd_line: list[str]
        """

        print "Converting HSHEDS ADF to TIF file."
        utDEM.uncompress_zip_file(HSHEDS_FILE_INPUT_ZIP)
        adf_to_tif_command = \
            GDAL_TRANSLATE + " " + HSHEDS_FILE_INPUT + " -of GTIFF " + \
            HSHEDS_FILE_TIFF
        utDEM.calling_system_call(adf_to_tif_command)
        print "Getting shape file covering area of interest."
        utDEM.uncompress_zip_file(SRTM_FILE_INPUT_ZIP)
        utDEM.get_shape_over_area(SRTM_FILE_INPUT, SHAPE_AREA_INTEREST_INPUT,
                                  SHAPE_AREA_INTEREST_OVER)
        print "Resampling and cutting TREE file."
        utDEM.uncompress_zip_file(TREE_CLASS_INPUT_ZIP)
        utDEM.resample_and_cut(TREE_CLASS_INPUT, SHAPE_AREA_INTEREST_OVER,
                               TREE_CLASS_AREA)
        print "Resampling and cutting SRTM file."
        utDEM.resample_and_cut(SRTM_FILE_INPUT, SHAPE_AREA_INTEREST_OVER,
                               SRTM_AREA_INTEREST_OVER)
        print "Resampling and cutting HSHEDS file."
        utDEM.resample_and_cut(HSHEDS_FILE_TIFF, SHAPE_AREA_INTEREST_OVER,
                               HSHEDS_AREA_INTEREST_OVER)
        print "Detecting and applying Fourier"
        srtm_fourier = utDEM.detect_apply_fourier(SRTM_AREA_INTEREST_OVER)
        # srtm_fourier = gdal.Open(
        #     "../resources/images/05CorrectedFourierSRTM.tif").ReadAsArray()
        print "Processing SRTM."
        print "Processing SRTM: First Iteration."
        srtm_proc1 = utDEM.process_srtm(srtm_fourier, TREE_CLASS_AREA)
        print "Processing SRTM: Second Iteration."
        srtm_proc2 = utDEM.process_srtm(srtm_proc1, TREE_CLASS_AREA)
        print "Processing SRTM: Third Iteration."
        srtm_proc = utDEM.process_srtm(srtm_proc2, TREE_CLASS_AREA)
        print "Processing HSHEDS."
        hydro_sheds = gdal.Open(HSHEDS_AREA_INTEREST_OVER).ReadAsArray()
        print "Processing HSHEDS: Getting Lagoons."
        hsheds_mask_lagoons_values = utDEM.get_lagoons_hsheds(hydro_sheds)
        hsheds_mask_lagoons = (hsheds_mask_lagoons_values > 0.0) * 1
        print "Processing Rivers."
        rivers_routed_closing = utDEM.process_rivers(RIVERS_SHAPE,
                                                     HSHEDS_AREA_INTEREST_OVER,
                                                     hsheds_mask_lagoons)
        print "Getting terms for final merging."
        first_term_hsheds_canyons = hydro_sheds * rivers_routed_closing
        snd_term_hsheds_lagoons = hsheds_mask_lagoons_values
        mask_canyons_lagoons = rivers_routed_closing + hsheds_mask_lagoons
        not_mask_canyons_lagoons = 1 - mask_canyons_lagoons
        trd_term_srtm_fourier_tree = srtm_proc * not_mask_canyons_lagoons
        print "Combining parts."
        dem_ready = first_term_hsheds_canyons + snd_term_hsheds_lagoons + \
                    trd_term_srtm_fourier_tree
        print "Applying final convolve filter."
        kernel = np.ones((3, 3))
        dem_ready_convolve = ndimage.convolve(np.abs(dem_ready),
                                              weights=kernel)
        dem_ready_smooth = dem_ready_convolve / kernel.size
        utDEM.array2raster(SRTM_AREA_INTEREST_OVER, DEM_READY_SMOOTH_PATH,
                           dem_ready_smooth)
        print "Resampling and cutting with final interest area."
        utDEM.resample_and_cut(DEM_READY_SMOOTH_PATH,
                               SHAPE_AREA_INTEREST_INPUT,
                               DEM_READY_AREA_INTEREST)
        print "Rotating final DEM."
        final_dem = utDEM.rotate_and_trim(DEM_READY_AREA_INTEREST, ANGLE)
        print "Around values."
        final_dem = np.around(final_dem)
        print "DEM Hydrologicaly conditioned ready."
        utDEM.array2raster_simple(FINAL_DEM, final_dem)
