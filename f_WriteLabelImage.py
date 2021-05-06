#!/bin/env python
# -*- coding: utf-8 -*-

from osgeo import gdal, ogr
import numpy as np

def WriteLabelImage( outname, data, Imagemodel ):
    
    Imagemodel_ds = gdal.Open(Imagemodel, gdal.GA_ReadOnly)
    driver=gdal.GetDriverByName('GTiff')
    
    outdataset = driver.Create(outname,Imagemodel_ds.RasterXSize,Imagemodel_ds.RasterYSize,1, gdal.GDT_Byte)
    outdataset.SetGeoTransform(Imagemodel_ds.GetGeoTransform())
    outdataset.SetProjection(Imagemodel_ds.GetProjection())
    outdataset.GetRasterBand(1).WriteArray(data)
    outdataset=None