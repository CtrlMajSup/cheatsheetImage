#!/bin/env python
# -*- coding: utf-8 -*-

from osgeo import gdal, ogr
import numpy as np

def WriteImage( outname, data, Imagemodel ):
    
    Imagemodel_ds = gdal.Open(Imagemodel, gdal.GA_ReadOnly)
    driver=gdal.GetDriverByName('GTiff')
    print(data.shape)
    outdataset = driver.Create(outname,Imagemodel_ds.RasterXSize,Imagemodel_ds.RasterYSize,1, gdal.GDT_Float32)
    outdataset.SetGeoTransform(Imagemodel_ds.GetGeoTransform())
    outdataset.SetProjection(Imagemodel_ds.GetProjection())
    outdataset.GetRasterBand(1).WriteArray(data)    
    outdataset=None