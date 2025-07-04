import sounddevice as sd
import numpy as np


"""
SYSTEM INFO
sample rate: 44100
bit depth: 24bit integer
1 channels
"""

"""
Combine two frequencies
Using Callback method
fixed block size
"""

#playback length in seconds (6)
#length = 6

#frames/samples per second
fs = 44100
chunk = 1024
#keep the volume between 0 and 1 so I don't blow my speakers
volume = .8
freq1 = 220
freq2 = 329.63
angle1 = 0.0
angle2 = 0.0
delta1 = 0.0
delta2 = 0.0

def set_angledelta(freq, fs):
    cyclesPerSample = freq/fs
    angle_delta = cyclesPerSample*2.0*np.pi
    return(angle_delta)

def update_angle(current_angle, angle_delta):
    return(current_angle+angle_delta)

def sine_callback(outdata, frames, time, status):
    for sample in range(frames):
        global angle1
        global angle2
        current_sample = volume*(np.sin(angle1)+np.sin(angle2))
        outdata[sample] = current_sample
        angle1 += delta1
        angle2 += delta2
    """
    frames is the number of audio samples to generate
    why does output need to be in the function defention?
    """
""" MAIN """
delta1 = set_angledelta(freq1, fs)
delta2 = set_angledelta(freq2, fs)

try:
    with sd.OutputStream(
        samplerate=fs, channels=1, callback=sine_callback, blocksize=chunk):

        while True: #what dis do?
            sd.sleep(1000)

except KeyboardInterrupt:
    print("playback stopped by user")


"""
REFRESHER ON TRY/EXCEPT
try: runs the code until/if an except is caught
except ExceptionType: tells the program what to do when an except of
ExceptionType is caught
exceptions are errors, normally the program would break and stopped
which is why you want to "handle" them

REFRESHER ON WITH
it creates a context manager to automatically handle resources

"""
