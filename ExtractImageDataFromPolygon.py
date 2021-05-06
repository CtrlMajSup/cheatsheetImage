#!/usr/bin/env python
# -*- coding: utf-8 -*-

#======= Extraction de données Raster à partir d'un fichier shape ======

# Expl usage : python ExtractImageDataFromPolygon.py -inImg /161015_PL.tif -inVect /media/train50.shp -f ID_CLASS -t TRUE -out /media/tt.csv

# Construction d'un fichier csv contenant les pixels non nuls d'une image contenus dans les polygones d'un vecteur.
# la sortie contient la class puis les valeurs des pixels de l'image.

# bbeguet@i-sea / 06-03-2017
#======================== IMPORTS ====================================

import os,sys,time

import argparse

import csv
import numpy as np

from osgeo import gdal, ogr

#======================== PARSER =====================================

parser = argparse.ArgumentParser(description='Extraction de données raster à partir fichier vecteur')
parser.add_argument('-inImg','--inputImage',help='Input image')
parser.add_argument('-inVect','--inputVector', help='input vector')
parser.add_argument('-f','--VectorField', help='Vector Field to consider for extraction')
parser.add_argument('-t','--TouchBorder', help='You want all pixels touching polygon : TRUE or FALSE (only exactly inside)')
parser.add_argument('-out', '--outputFile',type=str,help='Fichier .csv en sortie ')

args = parser.parse_args()
params = vars(args)

if params['inputImage'] is None:
	parser.print_help()
	sys.exit(1)

raster_data_path = params['inputImage']
vector_data_path = params['inputVector']
csvfile_path = params['outputFile']
attrib = params['VectorField']
touch = params['TouchBorder']
raster_classes = 'rastclass.tif' # besoin de ça pour la rasterisation, le raster ne sera pas écrit

startTime = time.time()

#===================== TRAITEMENT ====================================

print '----- Work in progress -----'

#================ Get Raster Information ============================

raster_dataset = gdal.Open(raster_data_path, gdal.GA_ReadOnly)
geo_transform = raster_dataset.GetGeoTransform()
proj = raster_dataset.GetProjectionRef()
bands_data = []

for b in range(1, raster_dataset.RasterCount + 1):
    band = raster_dataset.GetRasterBand(b)
    bands_data.append(band.ReadAsArray())

bands = np.dstack(bands_data)
rows, cols, n_bands = bands.shape

#================ Rasterize Vector =================================

pixel_size = geo_transform[1]
NoData_value = 0

vector_dataset = ogr.Open(vector_data_path)
vector_layer = vector_dataset.GetLayer()

target_dataset = gdal.GetDriverByName('GTiff').Create(raster_classes, cols, rows,1, gdal.GDT_Byte)
target_dataset.SetGeoTransform(geo_transform)
target_dataset.SetProjection(raster_dataset.GetProjection())
band = target_dataset.GetRasterBand(1)
band.SetNoDataValue(NoData_value)

gdal.RasterizeLayer(target_dataset, [1], vector_layer, burn_values=[0], options = ['ALL_TOUCHED='+touch,'ATTRIBUTE='+attrib])

classes=target_dataset.ReadAsArray()

#================ Data selection ===================================

data_ok = np.dstack((classes,bands))

dataflat = data_ok.reshape(data_ok.shape[0]*data_ok.shape[1],data_ok.shape[2])

indexes = np.where(dataflat[:,0]!=0)
select = np.array(dataflat[indexes,:])
select =select.reshape(select.shape[1],select.shape[2])

#================ Ecriture fichier sortie ==========================

with open(csvfile_path, 'w') as f:
  writer = csv.writer(f, delimiter='\t')
  writer.writerows(select)

#============ AFFICHAGE TPS EXECUTION ==============================

endTime = time.time()
print 'The script took ' + str(endTime - startTime)+ ' seconds'

print '-------- Job done ! --------'
