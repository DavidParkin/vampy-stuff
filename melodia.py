#!/usr/bin/python3
# coding: utf-8

from __future__ import print_function
import vamp
import librosa
#import essentia.standard as es
import matplotlib.pyplot as plt

audio_file = '/home/David/Music/Video/Stitch/maj_min-E.wav'
audio, sr = librosa.load(audio_file, sr=44100, mono=True, duration=5.0)
data = vamp.collect(audio, sr, "mtg-melodia:melodia")
hop, melody = data['vector']
print(hop)
print(melody)
import numpy as np
timestamps = 8 * 128/44100.0 + np.arange(len(melody)) * (128/44100.0)
melody_pos = melody[:]
melody_pos[melody<=0] = None
plt.figure(figsize=(18,6))
#plt.plot(timestamps, melody)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.plot(timestamps, melody_pos)
plt.show()
