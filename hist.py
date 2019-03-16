# coding: utf-8

import vamp
import librosa
import essentia.standard as es
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from __future__ import print_function
import essentia.standard as es
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from __future__ import print_function
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
audio_file = '~/Music/Videos/Stitch/maj-min-E.wav'
audio, sr = librosa.load(audio_file, sr=44100, mono=True)
audio_file
audio, sr = librosa.load(audio_file, sr=44100, mono=True)
audio_file = '/home/David/Music/Videos/Stitch/maj-min-E.wav'
audio, sr = librosa.load(audio_file, sr=44100, mono=True)
audio_file = '/home/David/Music/Videos/Stitch/maj_min-E.wav'
audio, sr = librosa.load(audio_file, sr=44100, mono=True)
audio_file = '/home/David/Music/Video/Stitch/maj_min-E.wav'
audio, sr = librosa.load(audio_file, sr=44100, mono=True)
data = vamp.collect(audio, sr, "mtg-melodia:melodia")
data
hop, melody = data['vector']
print(hop)
print(melody)
plt.figure(figsize=(18,6))
plt.plot(timestamps, melody)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
import numpy as np
timestamps = 8 * 128/44100.0 + np.arange(len(melody)) * (128/44100.0)
plt.plot(timestamps, melody)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.show
plt.show()
plt.plot(timestamps, melody)
plt.show()
get_ipython().run_line_magic('matplotlib', 'gtk')
get_ipython().run_line_magic('matplotlib', '')
get_ipython().run_line_magic("matplotlib('classic')", '')
get_ipython().run_line_magic('matplotlib', '')
help %matplotlib
get_ipython().run_line_magic('matplotlib', '')
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'gtk2')
get_ipython().run_line_magic('matplotlib', 'tk')
get_ipython().run_line_magic('matplotlib', 'py')
get_ipython().run_line_magic('matplotlib', 'pygment')
get_ipython().run_line_magic('matplotlib', 'gtk2')
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'pyglet')
get_ipython().run_line_magic('matplotlib', 'TkAgg')
get_ipython().run_line_magic('matplotlib', 'gtk3agg')
get_ipython().run_line_magic('matplotlib', 'gtk3')
