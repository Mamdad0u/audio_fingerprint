# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 22:25:09 2021

@author: duwat
"""



import librosa
from main import shazam_manuel_famtom
from main import song_database
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.pyplot import figure

def graph(durée_max, itérations):
    C=[]
    bruit=0
    labels=[]
    long=len(song_database)
    
    for n in range(0,itérations):
        c=0
        
        for j in range (long):
            for u in range (3):
                x,sr = librosa.load(song_database[j],sr=44100)
            
                départ= int(random.uniform(20, (len(x)-(20+durée_max)*sr)/sr))
            
                print(départ)
                print(song_database[j][:-4])
            
                nom=shazam_manuel_famtom(str(song_database[j][:-4]), bruit, 1+5*n , départ)+'.WAV'
            
                print(nom)
            
                if nom==song_database[j]:
                    c=c+1
                
        C.append(c)
        
        
        labels.append(durée_max- 5*n)
    print(labels)
    print(C)
    
labels=[1,6,11,16,21] 
C=[100*4/15,100*4/15,100*9/15,100*11/15,100*13/15]  
plt.bar(labels, C,align='center', alpha=0.5)
plt.xlabel("durée de l'enregistrement")
plt.ylabel("taux de succès (%)")
plt.title("taux de réussite selon la durée de l'enregistrement")
plt.show()
    
    
    
    