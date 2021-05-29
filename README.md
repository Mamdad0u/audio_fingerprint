# audio_fingerprint
Algorithm that allow you to find the Title, and the singer of a song thanks to a 15 seconds recording.

### Explication
This algorithm is comparable to the one from Shazam. To recognize a song, we analyse its spectrogram thanks a Short Time Fourier Transform (STFT). When the spectrogram is obtained, a constellation of local points is made. This constellation is the audio fingerprint.
Then, the algorithm will compare the audio fingerprint with the other fingerprints that are in the data base.

