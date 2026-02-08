import sounddevice as sd
import numpy as np


"""
SYSTEM INFO
sample rate: 44100
bit depth: 24bit integer
2 channels
"""

"""
Using Callback method
"""

#playback length in seconds (6)
#length = 6

#frames/samples per second
fs = 44100
chunk = 1024
#keep the volume between 0 and 1 so I don't blow my speakers
volume = .2

#fill an numpy array with the data
def noise_callback(outdata, frames, time, status):
    noise = np.random.normal(0,volume, size=(frames,)).astype(np.float32)
    outdata[:]=noise.reshape(-1,1)

    """
    frames is the number of audio samples to generate
    why does output need to be in the function defention?
    """
try:
    with sd.OutputStream(
        samplerate=fs, channels=1, callback=noise_callback, blocksize=chunk):

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
