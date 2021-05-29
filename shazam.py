# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 22:18:06 2021

@author: duwat
"""


import pyaudio
import numpy as np
import wave
import librosa
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from functions import hashPeaks
from functions import matching_pairs
from functions import best_match
from database import F_database
from database import song_database

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 15
WAVE_OUTPUT_FILENAME = "Record.wav"


p =   pyaudio.PyAudio()

player = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print('Attempting to identify the sample audio clip...')

sample,sr = librosa.load('Record.wav', sr=44100)

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
print('The best match for the song is: '+ song_database[np.argmax(songbins)][:-4])