

import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

"""
Creates a window object with the plot inside

"""
class WavePlot(QtWidgets.QMainWindow):
    def __init__(self, data_queue, fs, downsample, window_ms):
        super().__init__()
        self.q = data_queue  # store reference to the queue

        # Setup the plot
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)
        self.plot_widget.setYRange(-1, 1)
        self.plot_widget.showGrid(y=True)

        length = int(window_ms * fs / (1000 * downsample))
        self.plotdata = np.zeros(length)
        self.curve = self.plot_widget.plot(self.plotdata, pen='y')

        # Timer for updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(30)

    def update_plot(self):
        updated = False
        while not self.q.empty():
            try:
                data = self.q.get_nowait().flatten()
                shift = len(data)
                self.plotdata = np.roll(self.plotdata, -shift) #rolls front data to the end
                self.plotdata[-shift:] = data #replaces shifted values with new data
                updated = True
            except queue.Empty:
                break
        if updated:
            self.curve.setData(self.plotdata)

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

    def update_data(self):
        #calculate Freq Mag
        A = np.fft.fft(self.new_data, self.n, norm="forward") #only doing a forward transform for viz
        freq_mag = np.abs(A[1: int(self.n/2)]) #select only postiive freq

        for pixel in list(range(1, self.imgH+1)):
            skew= 1-np.exp(np.log(pixel/self.imgH)*0.2)
            fft_index = np.clip(int(skew*len(freq_mag)),0, len(freq_mag)-1) #I think we are off by 1
            level = freq_mag[fft_index]
            self.new_col[self.imgH - (pixel)]=level

        # Add new PSD to visuale data block
        self.viz_data = np.roll(self.viz_data, -1, axis = 1) #roll first col to last
        self.viz_data[:,-1] = self.new_col #replace last column

    def update_plot(self):
        while not self.q.empty():
            if self.index == self.n:
                self.update_data()
                self.img.setImage(self.viz_data, autoLevels = True)
                self.index = 0

            self.new_data[self.index]=self.q.get_nowait() #add new sample
            self.index += 1
