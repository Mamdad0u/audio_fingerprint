# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 19:09:57 2021

@author: duwat
"""

import librosa
from pydub import AudioSegment
import os
import numpy as np
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
import warnings



warnings.filterwarnings("ignore")


def get_filename(dir_name):
    filenames_list=[]
    for entry in os.scandir(dir_name):
        filenames_list.append(entry.name)
    return filenames_list
  

def mp3_to_wav(dir_name):
    for entry in os.scandir(dir_name):
        if (entry.path.endswith('.mp3') and entry.is_file()):
            name_wav = str(entry.name[:-4])+'.wav'
            sound = AudioSegment.from_mp3(dir_name+'/'+str(entry.name))
            sound.export(dir_name+'/'+name_wav, format="wav")


def PointsInTargertZone(index,A,delay_time,delta_time,delta_freq):
    "Find the points in the target zone which is associated with the correspondant anchor point"    

    Points = []
    x1 = A[index][1] + delay_time
    x2 = x1 + delta_time
    y1 = A[index][0] - delta_freq/2
    y2 = A[index][0] + delta_freq/2
    
    for i in A:
        if ((i[1]>x1 and i[1]<x2) and (i[0]>y1 and i[0]<y2)):
            Points.append(i)
            
    return Points



def hashPeaks(A,songID):

    #Hash parameters
    delay_time = 100      # 100 * 11 ms = 1 second
    delta_time = 100*5    # 31.25 * 3 * 11 ms = 5 seconds
    delta_freq = 128      # 128 * 7.81Hz = approx 1000Hz

    "Create a matrix of peaks hashed as: [[freq_anchor, freq_other, delta_time], time_anchor, songID]"
    hashMatrix = np.zeros((len(A)*100,5))  #Assume size limitation
    index = 0
    numPeaks = len(A)
    for i in range(0,numPeaks):
        PointsZ = PointsInTargertZone(i,A,delay_time,delta_time,delta_freq)
        NumP=len(PointsZ)
        for j in range(0,NumP):
            hashMatrix[index][0] = A[i][0]
            hashMatrix[index][1] = PointsZ[j][0]
            hashMatrix[index][2] = PointsZ[j][1]-A[i][1]
            hashMatrix[index][3] = A[i][1]
            hashMatrix[index][4] = songID
            index=index+1
    
    hashMatrix = hashMatrix[~np.all(hashMatrix==0,axis=1)]
    hashMatrix = np.sort(hashMatrix,axis=0)
        
    return hashMatrix



def extractFingerprint(song, songID):
    #Creation of the spectrogram
    audio,sr = librosa.load(song, sr=44100, duration =30)
    
    audio_16k = librosa.resample(audio, sr, 16000)
    audio_stft = librosa.stft(audio, n_fft=2048)
    audio_stft_dB = librosa.amplitude_to_db(np.abs(audio_stft),ref=np.max)  

    threshold = np.amin(audio_stft_dB) * (50/100)

    #Creation of the constellation Map
    image_max = ndi.maximum_filter(audio_stft_dB, size=5, mode='constant')
    peaks = peak_local_max(audio_stft_dB, min_distance=30, threshold_abs = threshold)

    # faire un test avec min_distance = 30, threshold_abs=-40
    # faire un test avec min_distance=20, threshold_abs=-60

    #Combinatorial Hash Generation + Hash details
    fingerprint = hashPeaks(peaks,songID)

    return fingerprint



def FingerPrint_Database(Song_database):

    F_database = np.zeros((1,5))

    for i in range(0,len(Song_database)):
        ID = i

        input_file = Song_database[i]

        print('Extraction de lempreinte digitale de', str(Song_database[i]))
        fingerprint = extractFingerprint(input_file,ID)
        F_database = np.concatenate((F_database,fingerprint),axis=0)

    print('Done')
    return F_database



def matching_pairs(hash_database,sample_hash):

    #Matching pairs parameters
    deltaFreq = 1 # -> 7.81 Hz
    deltaTime = 1/4 # -> 11/4 ms  

    "Find the matching pairs between sample audio file and the songs in the database"

    matchingPairs = []

    for i in sample_hash:
        for j in hash_database:
            if(i[0] > (j[0]-deltaFreq) and i[0] < (j[0] + deltaFreq)):
                if(i[1] > (j[1]-deltaFreq) and i[1] < (j[1] + deltaFreq)):
                    if(i[2] > (j[2]-deltaTime) and i[2] < (j[2] + deltaTime)):
                        matchingPairs.append((j[3],i[3],j[4]))
    return matchingPairs


def best_match(songs, matchingPairs):
    numSongs = len(songs)
    songbins= np.zeros(numSongs)
    numOffsets = len(matchingPairs)
    offsets = np.zeros((numOffsets,numSongs))
    index = 0

    for i in matchingPairs:
        offsets[index][int(i[2])]= (i[0]-i[1])/i[1]
        index = index +1
        songbins[int(i[2])] = songbins[int(i[2])] +  1
    
    return songbins,offsets