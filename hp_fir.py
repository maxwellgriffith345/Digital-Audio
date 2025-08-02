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
finite impulse response highpass filter
y[n] = (0.5*x[n])-(0.5*x[n-1])
y[n]=x[n]-x[n-1]
implamentation based on The Computer Music Tutorial Chapter 28
works by phase cancelation
what frequency is the cut off?

output[1]=x[1]
output[2]=x[2]-x[1]
output[3]=x[3]-[x2]
"""

#frames/samples per second
fs = 44100
chunk = 1024
#keep the volume between 0 and 1 so I don't blow my speakers
volume = .2
last_sample = 0

delay = 0

#fill an numpy array with the data
def noise_callback(outdata, frames, time, status):
    global delay
    noise = np.random.normal(0,volume, size=(frames,)).astype(np.float32)
    for i in range(frames):
        next_delay = noise[i]
        noise[i]=0.5*noise[i]+0.5*delay #but when do we update delay value?
        delay = next_delay
    outdata[:]=noise.reshape(-1,1)


try:
    with sd.OutputStream(
        samplerate=fs, channels=1, callback=noise_callback, blocksize=chunk):

        while True: #what dis do?
            sd.sleep(1000)

except KeyboardInterrupt:
    print("playback stopped by user")
