import sounddevice as sd
import numpy as np


"""
SYSTEM INFO
sample rate: 44100
bit depth: 24bit integer
2 channels
"""

"""
Using very basic sd.play() method
"""

#playback length in seconds (6)
length = 6

#frames/samples per second
fs = 44100

#keep the volume between 0 and 1 so I don't blow my speakers
volume = .3

#fill an numpy array with the data
noise = np.random.normal(0,volume, size=(length*fs,)).astype(np.float32)

sd.play(noise, fs)
sd.wait()
