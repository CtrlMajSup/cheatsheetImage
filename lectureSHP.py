#!/bin/env python
# -*- coding: utf-8 -*-
#======================== IMPORTS ====================================

import os,sys,time
import argparse
import csv
import numpy as np
import geopandas as gpd
import pandas as pd


from osgeo import gdal, ogr
data=gpd.GeoDataFrame.from_file('/home/herpin/polygone.shp') #lecture du shape file

print(data['geometry'].head())
for index, row in data.iterrows():
	poly_area=row['geometry'].area
	print('Polygon area at index {index} is : {area:.3f}'.format(index=index, area=poly_area))


new_field.to_csv('/home/herpin/Bureau/shapefile2poly.csv')
