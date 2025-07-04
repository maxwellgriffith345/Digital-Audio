import sounddevice as sd
import numpy as np


"""
SYSTEM INFO
sample rate: 44100
bit depth: 24bit integer
1 channels
"""

"""
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
freq = 440
current_angle = 0.0
angle_delta = 0.0

def update_angledelta():
    cyclesPerSample = freq/fs
    global angle_delta #I think I need to do something here to access a global variable
    angle_delta = cyclesPerSample*2.0*np.pi
#fill an numpy array with the data
def sine_callback(outdata, frames, time, status):
    for sample in range(frames):
        global current_angle
        current_sample = volume*np.sin(current_angle)
        outdata[sample] = current_sample
        current_angle += angle_delta
    """
    frames is the number of audio samples to generate
    why does output need to be in the function defention?
    """
update_angledelta()

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
