#!/bin/env python
# -*- coding: utf-8 -*-

from osgeo import gdal, ogr
import numpy as np

def ReadImage( raster_data_path ):
    
    raster_dataset = gdal.Open(raster_data_path, gdal.GA_ReadOnly)
    geo_transform = raster_dataset.GetGeoTransform()
    proj = raster_dataset.GetProjectionRef()
    
    bands_data = []
    for b in range(1, raster_dataset.RasterCount + 1):
        band = raster_dataset.GetRasterBand(b)
        bands_data.append(band.ReadAsArray())
    
    bands = np.dstack(bands_data)
    return bands
