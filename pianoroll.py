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

def hz2midi(herz):

    # convert from Hz to midi note

    hz_nonneg = herz.copy()
    idx = hz_nonneg <= 0
    # import ipdb; ipdb.set_trace()
    hz_nonneg[idx] = 1
    midi = 69 + 12*np.log2(hz_nonneg/440.)
    midi[idx] = 0
    # midi = 69 + 12*np.log2(herz/440.)

    # round
    midi = np.round(midi)

    return midi

#load audio with file
audio_file = '/home/David/Music/Video/Stitch/In The Mind of B.B. King_ The Thrill Is Gone Guitar Solo Lesson [360p].mp4'

audio, sr = librosa.load(audio_file, sr=44100, mono=True, offset=5.0, duration=5.0)
#collect silvet data
params = {} # allow A3
# params = {"minFreq" : 220, "maxFreq" : 500} # allow A3
data = vamp.collect(audio, sr, "silvet:silvet", parameters=params)
# mainly serial {{{
# hop, melody = data['vector']
# print(hop)
# print(melody)
# print(data)
print("Silvet data is {} long".format(len(data)))
#silvet returns list dict
silvet_data = data['list']
# jserialized = json.dumps(silvet_data, indent=4, cls=encoder.VampCustomEncoder)
# #import ipdb; ipdb.set_trace()
# print("Done!!")
# print(jserialized)
# junserialized = json.loads(jserialized, object_hook=encoder.vampy_decoder)
# print("Done!!")
# print(junserialized)
# silvet_data = junserialized
print("Silvet silvet_data is {} long".format(len(silvet_data)))
#collect melodia data
params = {"minfqr" : 220} # allow A3
data = vamp.collect(audio, sr, "mtg-melodia:melodia", parameters=params)
print("Melodia data is {} long".format(len(data)))
hop, melody = data['vector']
print("Melodia melody is {} long".format(len(melody)))
print("------- hop ---------")
print(hop)
print("------- melody ---------")
print(melody)
# }}}
timestampsa = 8 * 128/44100.0 + np.arange(len(silvet_data)) * (128/44100.0)
timestampsm = 8 * 128/44100.0 + np.arange(len(melody)) * (128/44100.0)
valuess = []
timess = []
labels = []
# ax = plt.subplots()
oldtime = vamp.vampyhost.RealTime('seconds', -1)
for note in silvet_data:
    for key in note:
        print("{}: {} ".format(key, note[key]), end='')
    print("\n")
    b = note.values()
    # print("b = :{}".format(b))
    ts, dur, label, values = list(b)
    # import ipdb; ipdb.set_trace()
    if ts < oldtime:
        print("*************** time error ****************")

    oldtime = ts
    print(label)
    y = values
    midinote = hz2midi(y)
    print(midinote)
    yy = values[1]
    plt.hlines(y=midinote[0], xmin=ts, xmax=ts+dur, color='r', linewidth=2)
    plt.text(ts, midinote[0], label, ha='left', va='center')
    valuess.append(midinote[0])
    timess.append(ts)
    labels += [label]

# del valuess[1::2]
melody_pos = melody[:]
melody_pos[melody <= 0] = None
# plt.ion()
plt.figure(figsize=(18, 6))
import ipdb; ipdb.set_trace()
plt.plot(timess, valuess, 'b-',)
# plt.plot(timestamps, melody)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
melody_pos= librosa.hz_to_midi(melody_pos)
plt.plot(timestampsm, melody_pos, 'm-', label='melody')
plt.legend()
plt.show()
