import queue
import sys
import threading

import numpy as np
import sounddevice as sd

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

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


class Spectrogram(QtWidgets.QMainWindow):

    imgH = 512
    imgW = 512

    def __init__(self, data_queue, fftsize):
        super().__init__()
        self.q = data_queue
        self.n = fftsize

        #number of rows is half the fftsize becuase we drop negative freq
        self.viz_data = np.zeros((self.imgH, self.imgW))
        self.img_widget = pg.GraphicsLayoutWidget()
        self.setCentralWidget(self.img_widget)
        self.p1 = self.img_widget.addPlot(title = '')
        self.img = pg.ImageItem(axisOrder='row-major')
        self.img.setColorMap('turbo')
        self.p1.addItem(self.img)
        self.img.setImage(self.viz_data, autoLevels = True)

        # Timer for updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(30)

        self.new_data = np.zeros(self.n)
        self.new_col = np.zeros(self.imgH)
        self.index = 0

        # self.NextBlockReady = False
        self.skew_scalar = np.exp(np.log(np.arange(1,self.imgH)/self.imgH)*0.2)
        #length = 511
        #run into a divide by zero error
        #print(len(self.skew_scalar))
    def update_data(self):

        #calculate PSD
        A = np.fft.fft(self.new_data, self.n, norm="forward") #only doing a forward transform for viz
        A_pos = A[1: int(self.n/2)] #length = 511
        freq_mag = np.abs(A_pos) #many rows one column



        for pixel in list(range(1, self.imgH+1)):
            skew= 1-np.exp(np.log(pixel/self.imgH)*0.2)
            fft_index = np.clip(int(skew*len(A_pos)),0, len(A_pos)-1) #I think we are off by 1
            level = freq_mag[fft_index]
            self.new_col[self.imgH - (pixel)]=level


        # Add new PSD to visuale data block
        self.viz_data = np.roll(self.viz_data, -1, axis = 1) #roll first col to last
        self.viz_data[:,-1] = self.new_col #replace last column

        self.index = 0

    def update_plot(self):
        while not self.q.empty():
            if self.index == self.n:
                self.update_data()
                self.img.setImage(self.viz_data, autoLevels = True)
                self.index = 0

            self.new_data[self.index]=self.q.get_nowait() #add new sample
            self.index += 1


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
