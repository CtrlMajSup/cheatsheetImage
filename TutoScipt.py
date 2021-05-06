#!/bin/env python
# -*- coding: utf-8 -*-


#------ import  des libs utiles ------

import sys,os,string,math,string,time

import numpy as np
import matplotlib.pyplot as plt

import csv

from osgeo import gdal, ogr 

#------ import  des fonctions ------
from f_ReadImage import*
from f_WriteImage import*
from f_WriteLabelImage import*
from f_ReadDataFromCSV import*

#===============================================================
# Expl_1 lire et écrire un fichier texte
#===============================================================

nom_fichier = '/home/herpin/Bureau/pour_stage_dev_2021/PythonTraining/Data/colormap.csv'

list_Data=[] # déclaration d'une liste vide pour stocker la donnée

fichier = open(nom_fichier,'r')

for line in fichier:
    row = list(line.split(','))
    list_Data.append(row)

print (list_Data) #afficher la liste
print (len(list_Data))# afficher la taille de la liste (nombre de lignes du fichier)
print (list_Data[0]) #afficher le premier element de la liste, c'est une liste !, list_Data est donc une liste de listes :)
print (list_Data[len(list_Data)-1]) #afficher le dernier element de la liste (python commence à compter à partir de zero)

print (list_Data[0][0]) # list_Data[0] est une liste, list_Data[0][0] est le premier élement de cette liste


# ici je veux récuperer que les valeurs numériques et écrire un nouveau fichier
# je dois supprimer le dernier element de chaque liste de liste

for i in range(0,len(list_Data)): # ici python va boucler de 0 à  len(list_Data)-1 par défaut
    del list_Data[i][len(list_Data[i])-1] # ici bien capter ce qui se passe

print (list_Data) # tout bon j'ai gardé uniquement mes valeurs numériques

matrix = np.array(list_Data).astype(float) # je peux convertir ma liste en np.array, tableau de nombres ou matrice, je converti le tout en nombre float, tout d'un coup :)

print (matrix.shape) # afficher les dimension de ma matrice

# je peux maintenant faire des calculs ac mon tableau matrix
# je vais calculer la moyenne de chaque ligne et stocker ça dans une variable

mean_vector = matrix.mean(axis=1) # mean_vector est alors un np.array contenant les moyennes de chaque ligne
print (mean_vector)

#je veux ecrire nouveau fichier ac ma matrice et la valaur moyenne à la fin de la ligne
#je vais concaténer ma matrice et mon vecteur

matrix = np.column_stack((matrix,mean_vector))


#je vais écrire mon fichier texte en sortie 

nom_fichier_out ='/home/herpin/Bureau/pour_stage_dev_2021/PythonTraining/Data/maData.csv'

with open(nom_fichier_out, 'w') as f:
    writer = csv.writer(f, delimiter=' ') # ici je choisi l'espace comme delimiteur entre les colonnes
    writer.writerows(matrix)

#Job Done !!


# maintenant je vais lire ce fichier ac ma fonction ReadDataFromCSV, faut que le fichier soit une matrice propre pour qu'elle marche (tous les élements sont numériques et de meme type).
Data = ReadDataFromCSV(nom_fichier_out)
print (Data)
print (Data.shape)


#=================================================================================
#=================================================================================

#=================================================================================
# Expl_2 lire jouer et écrire une image (tif, géoref -> suppose gdal bien installé)
#=================================================================================

nom_image = '/home/herpin/Bureau/pour_stage_dev_2021/PythonTraining/Data/img_25_4.tif'
nom_mask = '/home/herpin/Bureau/pour_stage_dev_2021/PythonTraining/Data/lab_25_4.tif'

img = ReadImage(nom_image)
mask = ReadImage(nom_mask)

mask=mask.reshape(mask.shape[0],mask.shape[1])# ici je reshape le masque pour éliminer la troisième dimension

print (img.shape) # 256lignes*256colonnes*4bandes spectrales

I =img[:,:,0:3] #ici je récupère toutes les lignes toutes les colonnes et que les 3 premières bandes spectrales (RGB)
I = I/255.0 # normalise pour affichage

plt.subplot(121)
plt.imshow(I)
plt.axis('off')
plt.title('Image RGB')

plt.subplot(122)
plt.imshow(mask)
plt.axis('off')
plt.title('Masque')

plt.show()


# ici je veux mettre tous les pixels de toutes les bandes de I à O quand le masque vaut 255
# SANS BOUCLES
# je vais conserver les dimension x et y (nb lignes, nb colonnes) avant de "flat" mon image

x= img.shape[0]
y= img.shape[1]

img_flat=img.reshape(x*y,img.shape[2])
print (img_flat.shape)
mask_flat=mask.reshape(x*y)

img_flat[mask_flat==255] = 0 # j'affecte 0 aux pixels de img_flat pour lesquels mask_flat = 255

img_masked = img_flat.reshape(x,y,img.shape[2])# je redimensionne bien mon image
Im =img_masked[:,:,0:3] #ici je récupère toutes les lignes toutes les colonnes et que les 3 premières bandes spectrales (RGB)
Im = Im/255.0 # normalise pour affichage


plt.subplot(131)
plt.imshow(I)
plt.axis('off')
plt.title('Image RGB')

plt.subplot(132)
plt.imshow(mask)
plt.axis('off')
plt.title('Image masque')

plt.subplot(133)
plt.imshow(Im)
plt.axis('off')
plt.title('Image masquee')

plt.show()



#=================================================================================
#=================================================================================

# ici je vais lire mon image, calculer un ratio de bande et écrire momn image en sortie avec ma fonction WriteImage

nom_image = '/home/herpin/Bureau/pour_stage_dev_2021/PythonTraining/Data/img_25_3.tif'
img = ReadImage(nom_image)

ratio = img[:,:,3]/img[:,:,2] # ratio bande4/bande3 soit PIR/R

nom_ratio_out = '/home/herpin/Bureau/pour_stage_dev_2021/PythonTraining/Data/ratio_25_3.tif'
WriteImage(nom_ratio_out,ratio,nom_image) # cette fonction prend en argument le nom de la sortie, la data, le nom d'une image de reference pour copier metadat (géoreferencement and co)

#=================================================================================
#=================================================================================





#=================================================================================
# Expl_3 parcourir les fichier d'un dossier, boucler sur les élements du dossier etc
#=================================================================================

In_Folder = '/home/herpin/Bureau/pour_stage_dev_2021/PythonTraining/Data/'

file_list = os.listdir(In_Folder)
print (file_list) # la liste contient touts les nom de fichier du dossier

# je ne veux recupérer que les fichier contenant la chaine de caractère "img"

select_list = [s for s in file_list if "img" in s]
print (select_list)

# maintenant je veux calculer le ratio PIR/R pour toutes ces images et écrire l'image ratio en générant son nom automatiquement

for image in select_list :
    #je veux récuperer le sufix du nom de l'image soit '_nb1_nb2.tif'
    print (image)
    sufix = image.split('_',1)[1]# va spliter ma chaine de caractère à la première occurence de '_', et je garde que le deuxième element de la liste
    print(sufix)
    nom_ratio = In_Folder+'ratio_'+sufix# construction de la chaine de caractère du nom de l'output
    print(nom_ratio)
    img = ReadImage(In_Folder+image)
    ratio = img[:,:,3]/img[:,:,2]
    WriteImage(nom_ratio,ratio,In_Folder+image)
    
# Job Done !










































