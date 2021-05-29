# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 22:27:25 2021

@author: duwat
"""


import os
import warnings
import librosa
import numpy as np
from scipy import ndimage as ndi
import random

warnings.filterwarnings("ignore")

from functions import get_filename
from functions import FingerPrint_Database
from functions import peak_local_max
from functions import matching_pairs
from functions import hashPeaks
from functions import best_match
from recording import recording

os.chdir('C:/Users/duwat/Desktop/projet shazam/Album')
# Song database
song_database = get_filename('C:/Users/duwat/Desktop/projet shazam/Album')

def show_database():
    print( 'Les musiques contenues dans la database sont :')
    index = 1
    for i in song_database:
        print(index, '- ' + i[:-4])
        index = index+1
    
    return 


F_database=FingerPrint_Database(song_database)


def shazam(sample):
    
    print('Shazam tente de retrouver votre titre ...')
    
    sample_16k = librosa.resample(sample, 44100, 16000)
    sample_stft = librosa.stft(sample, n_fft=2048)
    sample_stft_dB = librosa.amplitude_to_db(np.abs(sample_stft),ref=np.max) 
    
    threshold = np.amin(sample_stft_dB) * (50/100)
    
    image_max = ndi.maximum_filter(sample_stft_dB, size=5, mode='constant')
    peaks = peak_local_max(sample_stft_dB, min_distance=30,threshold_abs=threshold)
    
     
    # Extract the fingerprint of the unknown audio
    sample_fingerprint = hashPeaks(peaks,0)
    
    
    # Find the matching pairs between sample audio file and the songs in the database
    matchingPairs = matching_pairs(F_database, sample_fingerprint)
    
    
    # Identify the song
    songbins,offsets = best_match(song_database,matchingPairs)
    print('Le titre de votre chansion est: '+ song_database[np.argmax(songbins)][:-4], 'une chanson du premier album de The Courthills')
    
    


def shazam_auto():
    
    recording()
    
    sample,sr = librosa.load('Record.wav', sr=44100)
    
    shazam(sample)




    
def shazam_manuel(song, bruit, durée , départ):
       
    x,sr = librosa.load(str(song)+'.wav',sr=44100)
    
    sam=[]
    
    r=départ*sr
    dur= int(sr*durée)
    for i in range (dur):
        
        b=random.uniform(-bruit, bruit)
        sam.append(x[r+i])
        
    
    
    y = np.array(sam)
    sample = y.astype(np.float)
    
    sample = 0.99 * sample / max(abs(sample))
    shazam(sample)
    


    
    
    

def shazam_manuel_famtom(song, bruit, durée , départ):
       
    x,sr = librosa.load(str(song)+'.wav',sr=44100)
    
    sam=[]
    print(len(x))
    r=départ*sr
    dur= int(sr*durée)
    for i in range (dur):
        
#        b=random.uniform(-bruit, bruit)
        sam.append(x[r+i])
        
    
    
    y = np.array(sam)
    sample = y.astype(np.float)
    
    sample = 0.99 * sample / max(abs(sample))
    sample_16k = librosa.resample(sample, 44100, 16000)
    sample_stft = librosa.stft(sample, n_fft=2048)
    sample_stft_dB = librosa.amplitude_to_db(np.abs(sample_stft),ref=np.max) 
    
    threshold = np.amin(sample_stft_dB) * (50/100)
    
    image_max = ndi.maximum_filter(sample_stft_dB, size=5, mode='constant')
    peaks = peak_local_max(sample_stft_dB, min_distance=30,threshold_abs=threshold)
    
     
    # Extract the fingerprint of the unknown audio
    sample_fingerprint = hashPeaks(peaks,0)
    
    
    # Find the matching pairs between sample audio file and the songs in the database
    matchingPairs = matching_pairs(F_database, sample_fingerprint)
    
    
    # Identify the song
    songbins,offsets = best_match(song_database,matchingPairs)
    return song_database[np.argmax(songbins)][:-4]