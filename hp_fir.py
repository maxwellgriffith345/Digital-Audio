import sounddevice as sd
import numpy as np


"""
SYSTEM INFO
sample rate: 44100
bit depth: 24bit integer
1 channel
"""

"""
Using Callback method
"""

"""
niave finite impulse response highpass filter
y[n] = (0.5*x[n])-(0.5*x[n-1])
implamentation based on The Computer Music Tutorial Chapter 28
works by phase cancelation
what frequency is the cut off?
"""

#frames/samples per second
fs = 44100
chunk = 1024
#keep the volume between 0 and 1 so I don't blow my speakers
volume = .2
last_sample = 0


#fill an numpy array with the data
def noise_callback(outdata, frames, time, status):
    noise = np.random.normal(0,volume, size=(frames+1,)).astype(np.float32)
    hp_noise = 0.5*noise[1:]-0.5*noise[:-1]
    outdata[:]=hp_noise.reshape(-1,1)


try:
    with sd.OutputStream(
        samplerate=fs, channels=1, callback=noise_callback, blocksize=chunk):

        while True: #what dis do?
            sd.sleep(1000)

except KeyboardInterrupt:
    print("playback stopped by user")
