#!/bin/env python
# -*- coding: utf-8 -*-

import os,sys,time
import numpy as np

# -> We have two function:



def ReadDataFromCSV(X_train_data):
    
    X_train = []
    X_train_file = open(X_train_data,'r')

    for line in X_train_file:
        row = list(line.split())
        X_train.append(row)

    X_train = np.array(X_train).astype(float)
            
    return X_train
