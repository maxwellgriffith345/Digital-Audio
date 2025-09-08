""" Plot white noise signal with sounddevice and pyqtgraph"""

import queue
import sys
import threading

import numpy as np
import sounddevice as sd

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

from audio_plots import WavePlot
"""
SYSTEM INFO
sample rate: 44100
bit depth: 24bit integer
2 channels
"""

#frames/samples per second
fs = 44100
#chunk = 1024
#keep the volume between 0 and 1 so I don't blow my speakers
volume = .2
downsample = 10 #amount to downsample
window = 200 #ms visible time
interval = 30 #ms min time between plot updates




#fill an numpy array with the data
def noise_callback(outdata, frames, time, status):
    noise = np.random.normal(0,volume, size=(frames,1)).astype(np.float32)

    try:
        q.put_nowait(noise[::downsample,])
    except queue.Full:
        pass

    outdata[:]=noise.reshape(-1,1)
    """
    q.put is blocking the audio stream causing drops
    graphing function isnt pulling form que fast enough
    blocks the return of noise_callback
    """
def play_audio():
    with sd.OutputStream(samplerate=fs,channels=1,
                        callback=noise_callback):

        while True:
            sd.sleep(1000)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv) #why pass sys.argv?

    #create queue to pass data from callback to graph
    q = queue.Queue(maxsize=10)

    #create seperate audio thread. what is daemon?
    audio_thread = threading.Thread(target=play_audio, daemon=True)
    audio_thread.start()

    #run graph app
    window = WavePlot(q, fs=fs, downsample=downsample, window_ms=window)

    window.setWindowTitle("White Noise Wave")
    window.show()

    sys.exit(app.exec_()) #what dis do?
