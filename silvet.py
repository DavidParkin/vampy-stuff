#!/usr/bin/python3
# coding: utf-8

# from __future__ import print_function
import json
import librosa
import vamp
#import essentia.standard as es
import matplotlib.pyplot as plt
import numpy as np
import encoder
#load audio with file
audio_file = '/home/David/Music/Video/Stitch/maj_min-E.wav'
audio, sr = librosa.load(audio_file, sr=44100, mono=True, offset=0.0, duration=5.0)
#collect silvet data
data = vamp.collect(audio, sr, "silvet:silvet")
# hop, melody = data['vector']
# print(hop)
# print(melody)
print(data)
print("Silvet data is {} long".format(len(data)))
#silvet returns list dict
silvet_data = data['list']
jserialized = json.dumps(silvet_data, indent=4, cls=encoder.VampCustomEncoder)
#import ipdb; ipdb.set_trace()
print("Done!!")
print(jserialized)
junserialized = json.loads(jserialized, object_hook=encoder.vampy_decoder)
print("Done!!")
print(junserialized)
silvet_data = junserialized
print("Silvet silvet_data is {} long".format(len(silvet_data)))
#collect melodia data
params = {"minfqr" : 220} # allow A3
data = vamp.collect(audio, sr, "mtg-melodia:melodia", parameters = params)
print("Melodia data is {} long".format(len(data)))
hop, melody = data['vector']
print("Melodia melody is {} long".format(len(melody)))
print(hop)
print(melody)

timestampsa = 8 * 128/44100.0 + np.arange(len(silvet_data)) * (128/44100.0)
timestampsm = 8 * 128/44100.0 + np.arange(len(melody)) * (128/44100.0)
valuess = []
timess = []
labels = []
for note in silvet_data:
    for key in note:
        print("{}: {}".format(key, note[key]), end='')
    print("\n")
    b = note.values()
    print("b = :{}".format(b))
    ts, dur, label, values = list(b)
    valuess.extend(values)
    timess.append(ts)
    labels += [label]

del valuess[1::2]
melody_pos = melody[:]
melody_pos[melody<=0] = None
# plt.ion()
plt.figure(figsize=(18, 6))
plt.plot(timess, valuess)
# plt.plot(timestamps, melody)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.plot(timestampsm, melody_pos)
plt.show()
