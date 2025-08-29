""" Plot white noise signal with sounddevice and pyqtgraph"""

import queue
import sys
import threading

import numpy as np
import sounddevice as sd

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

from audio_plots import NoisePlot
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
#downsample = 10 #amount to downsample
window = 200 #ms visible time
interval = 30 #ms min time between plot updates


fftOrder = 10 #size of the FFT window
fftSize = 1024 #number of points FFT will operate on 2^fftOrder

#fill an numpy array with the data
def noise_callback(outdata, frames, time, status):
    noise = np.random.normal(0,volume, size=(frames,1)).astype(np.float32)

    #PUSH DATA TO fftq

    #Output data
    outdata[:]=noise.reshape(-1,1)

def play_audio():
    with sd.OutputStream(samplerate=fs,channels=1, callback=noise_callback):
        while True:
            sd.sleep(1000)

"""INSERT CLASS TO ACTUALLY MAKE THE GRAPH HERE"""
class Spectrogram(QtWidgets.QMainWindow):
    def __init__():
        super().__init__()

    """
    Boiler Plate Plot Setup
    Use pyqtgraph ImageItem

    y aixs: frequency AT LOG SCALE
    x axis: each tic is one processed block of fft
    color is strength of frequency

    Update graph
    shift all data left by one tix on the x aixs
    and add the new data to the end, the right most tick
    """


    drawNextLineOfSpectrogram(self):
        #IMPLAMENT HERE

    repaint(self):
        #PROBABLY A BUILT IN FUNCTION FOR THIS

    def update_plot(self):
        if(nextBlockReady):
            drawNextLineOfSpectrogram()
            nextBlockReady = False
            repaint()

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv) #why pass sys.argv?

    #DATA STRUCTURES FOR FFT
    #create queue to load in data for fft FIFO?
    #should we use a queue here? is there a better way to set the size?
    fftq = queue.Queue(maxsize=fftSize)
    fftData = np.zeros(fftSize*2) #why does this need ot be nice the size

    #Helpers
    q_index = 0
    nextBlockReady=False

    #create seperate audio thread. what is daemon?
    audio_thread = threading.Thread(target=play_audio, daemon=True)
    audio_thread.start()

    #run graph app
    window = NoisePlot(q, fs=fs, downsample=downsample, window_ms=window)

    window.setWindowTitle("White Noise Wave")
    window.show()

    sys.exit(app.exec_()) #what dis do?
