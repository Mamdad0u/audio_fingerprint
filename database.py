# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 22:12:29 2021

@author: duwat
"""


import os
import warnings

warnings.filterwarnings("ignore")


from functions import get_filename



os.chdir('C:/Users/duwat/Desktop/projet shazam/Album')


# Song database
song_database = get_filename('C:/Users/duwat/Desktop/projet shazam/Album')

print('Les musiques contenues dans la database sont :')



index = 1
for i in song_database:
    print(index, '- ' + i[:-4])
    index = index+1
    
    
    
    
