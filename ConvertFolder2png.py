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
from f_BBoxExtractor import*

#/home/isea/Desktop/test_dataset_arcachon/test
#======================== PARSER ====================================

parser = argparse.ArgumentParser(description='Convertir toutes les images d un fichier')
parser.add_argument('-in','--inputFolder',help='Input folder')
parser.add_argument('-out','--outputFolder',help='Output folder')
parser.add_argument('-t','--Type',help='Output Type : uint8/uint16/int16/uint32/int32/float/double')

args = parser.parse_args()
params = vars(args)


if params['inputFolder'] is None:
    parser.print_help()
    sys.exit(1)

folder = params['inputFolder']
outfolder = params['outputFolder']
typ = params['Type']



dirs = os.listdir(folder)

for file in dirs:
    print(folder+file)
    
    radical = file.split("." )[0]
        
    nameout = file.split("." )[0]+'.png'
    ComBase='otbcli_Convert -in '+folder+file+' -out '+outfolder+nameout+""
    print ComBase
    os.system(ComBase)
    
    ComBase='rm '+outfolder+nameout+'.aux.xml'+""
    print ComBase
    os.system(ComBase)






