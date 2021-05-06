#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,string,math,string,time

from osgeo import gdal, ogr
import numpy as np
import argparse
import subprocess

from f_ReadImage import*
from f_WriteImage import*
from f_WriteLabelImage import*



import matplotlib.pyplot as plt


import argparse
import subprocess

#======================== PARSER ====================================

parser = argparse.ArgumentParser(description='Remplacer valeur d une image en fonction d une valeur d une autre')
parser.add_argument('-ref','--inputRef',help='Input ref image')
parser.add_argument('-v','--Value',help='Input ref value')
parser.add_argument('-im','--inputImg',help='Input image to clean')
parser.add_argument('-o','--outputValue',help='output value')
parser.add_argument('-out','--outputImage',help='output Image')

args = parser.parse_args()
params = vars(args)

if params['inputImg'] is None:
	parser.print_help()
	sys.exit(1)

mask_path = params['inputRef']
novalue = int(params['Value'])
img_path = params['inputImg']
outvalue = int(params['outputValue'])
outname = params['outputImage']

#===================== TRAITEMENT ====================================

print '----- Work in progress -----'

#================ LECTURE RASTER et INFOS=============================
img = ReadImage(mask_path)
train = ReadImage(img_path)


x = img.shape[0]
y = img.shape[1]

print(x)
print(y)

print(train.shape)

train=train.reshape(x*y)
img = img.reshape(x*y)

indexes = np.where(img==novalue)
train[indexes]=outvalue

train = train.reshape(x,y)

WriteImage( outname, train,mask_path )


print '----- Job Done ! -----'
