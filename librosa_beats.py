#!/usr/bin/python3
# coding: utf-8

#https://librosa.github.io/librosa/tutorial.html

from __future__ import print_function
import vamp
import librosa
#import essentia.standard as es
import matplotlib.pyplot as plt

audio_file = '/home/David/Music/Video/Stitch/maj_min-E.wav'
audio, sr = librosa.load(audio_file, sr=44100, mono=True, offset=0.0, duration=5.0)
# 3. Run the default beat tracker
tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr)

print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

# 4. Convert the frame indices of beat events into timestamps
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

print('Saving output to beat_times.csv')
librosa.output.times_csv('beat_times.csv', beat_times)
# data = vamp.collect(audio, sr, "silvet:silvet")
# # hop, melody = data['vector']
# # print(hop)
# # print(melody)
# print(data)
# a = data['list']
# import numpy as np
# timestamps = 8 * 128/44100.0 + np.arange(len(a)) * (128/44100.0)
# valuess=[]
# timess=[]
# labels=[]
# for note in a:
    # for key in note:
        # print("{}: {}".format(key, note[key]), end='')
    # print("\n")
    # b = note.values()
    # ts, dur, label, values = list(b)
    # valuess.extend(values)
    # timess.append(ts)
    # labels+=[label]

# del valuess[1::2]
# # melody_pos = melody[:]
# # melody_pos[melody<=0] = None
# plt.figure(figsize=(18, 6))
# plt.plot(timess, valuess)
# # plt.plot(timestamps, melody)
# plt.xlabel('Time (s)')
# plt.ylabel('Frequency (Hz)')
# # plt.plot(timestamps, melody_pos)
# plt.show()
