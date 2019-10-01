import gdal

from image import Image
from filters.custom_filters import (LagoonsDetection, ClipLagoonsRivers,
                                    ProcessRivers)
from utils_dem import (resample_and_cut, unzip_resource, rasterize_rivers,
                       clip_lines_vector)
from config_loader import Config


class HSHEDS(Image):

    def __init__(self, area_of_interest):
        super().__init__(area_of_interest)
        self.hsheds_zip = Config.hsheds('HSHEDS_ZIP')
        self.hsheds_adf = Config.hsheds('HSHEDS_ADF')
        self.hsheds_tif = Config.hsheds('HSHEDS_TIF')
        self.hsheds_interest = Config.hsheds('HSHEDS_AREA')
        self.lagoons = Lagoons(self.hsheds_interest)
        self.rivers = Rivers(area_of_interest)

    def _prepare(self):
        unzip_resource(self.hsheds_zip)
        gdt_options = gdal.TranslateOptions(format='GTIFF')
        gdal.Translate(self.hsheds_tif, self.hsheds_adf, options=gdt_options)
        resample_and_cut(self.hsheds_tif, self.aoi, self.hsheds_interest)

    def process(self):
        self._prepare()
        lagoons = self.lagoons.process()
        rivers = self.rivers.process(lagoons)
        return lagoons, rivers


class Lagoons(Image):

    def __init__(self, area_of_interest):
        self.hsheds_interest = area_of_interest

    def process(self):
        hydro_sheds = gdal.Open(self.hsheds_interest).ReadAsArray()
        lagoons = LagoonsDetection()
        lagoons.apply(hydro_sheds)
        return lagoons


class Rivers(Image):

    def __init__(self, area_of_interest):
        super().__init__(area_of_interest)
        self.rivers_zip = Config.rivers('RIVERS_ZIP')
        self.rivers_full = Config.rivers('RIVERS_FULL')
        self.rivers_tif = Config.rivers('RIVERS_TIF')
        self.rivers_interest = Config.rivers('RIVERS_AREA')

    def _prepare(self):
        unzip_resource(self.rivers_zip)
        clip_lines_vector(self.rivers_full, self.aoi, self.rivers_interest)
        rasterize_rivers(self.rivers_interest, self.rivers_tif)

    def process(self, lagoons):
        self._prepare()
        rivers = gdal.Open(self.rivers_tif).ReadAsArray()
        rivers_routed = ProcessRivers(lagoons.hsheds_nan_fixed).apply(rivers)
        return ClipLagoonsRivers(lagoons.mask_lagoons,
                                 rivers_routed).apply(rivers_routed)
