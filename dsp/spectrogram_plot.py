import queue
import sys
import threading

import numpy as np
import sounddevice as sd

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

from audio_plots import Spectrogram

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
volume = .8

fftOrder = 10 #size of the FFT window
fftSize = 1024 #number of points FFT will operate on 2^fftOrder

freq1 = 2200
freq2 = 500
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

#fill an numpy array with the data
def audio_callback(outdata, frames, time, status):
    for sample in range(frames):
        global angle1
        global angle2
        current_sample = volume*(np.sin(angle1)+np.sin(angle2)+np.random.normal())

        try:
            q.put_nowait(current_sample)
        except queue.Full:
            pass

        outdata[sample] = current_sample
        angle1 += delta1
        angle2 += delta2

def play_audio():
    with sd.OutputStream(samplerate=fs,channels=1, callback=audio_callback):
        while True:
            sd.sleep(1000)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv) #why pass sys.argv?
    q = queue.Queue(maxsize=fftSize)

    delta1 = set_angledelta(freq1, fs)
    delta2 = set_angledelta(freq2, fs)
    #create seperate audio thread. what is daemon?
    audio_thread = threading.Thread(target=play_audio, daemon=True)
    audio_thread.start()

    #run graph app
    window = Spectrogram(q, fftSize)

    window.setWindowTitle("Spectrogram Plot")
    window.show()

    sys.exit(app.exec_()) #what dis do?
