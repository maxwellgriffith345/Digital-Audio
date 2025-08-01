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
niave infinite impulse response filter aka exponential smoothing filter
y[n] = x[n]+a*y[n-1])
implamentation based on The Computer Music Tutorial Chapter 28
works by phase cancelation
what frequency is the cut off?
output of filter is feed back into the input
recursive implamentation?
a values closer to 1 attenuate frequencies above 0 (DC)
a values closer to -1 more attenuation to frequencies below Nyquist rate
|a|<1 to keep filter stable
"""

#frames/samples per second
fs = 44100
chunk = 1024
#keep the volume between 0 and 1 so I don't blow my speakers
volume = .2
last_sample = 0
delay_vol = .8
delay = 0

""""
Working out how to write the loop or recursion

output[1]=x[1]
delay[1]=output[1]
output[2]=x[2]+[delay1]
delay[2]=output[2]

output[1]=x[1]
output[2]=x[2]+a*output[1]
output[3]=x[3]+a*output[2]

noise_array(len frames) these are the x inputs
output_arry(len frames) need to fill this


global delay = 0
for n in x:
    x[n]=x+delay
    delay = a*x[n]


"""


#fill an numpy array with the data
def noise_callback(outdata, frames, time, status):
    global delay
    noise = np.random.normal(0,volume, size=(frames,)).astype(np.float32)
    for i in range(frames):
        noise[i]=noise[i]+delay
        delay = delay_vol*noise[i]

    outdata[:]=noise.reshape(-1,1)


try:
    with sd.OutputStream(
        samplerate=fs, channels=1, callback=noise_callback, blocksize=chunk):

        while True: #what dis do?
            sd.sleep(1000)

except KeyboardInterrupt:
    print("playback stopped by user")
