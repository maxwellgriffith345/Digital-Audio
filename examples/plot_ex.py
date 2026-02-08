""" Examples from the PyQT docs"""

""" Scrolling Plot"""

import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

app = pg.mkQApp("Plotting Example")
#mw = QtWidgets.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

p6 = win.addPlot(title="Updating plot")
curve = p6.plot(pen='y')
data = np.random.normal(size=(10,1000))
ptr = 0
def update():
    global curve, data, ptr, p6
    curve.setData(data[ptr%10])
    if ptr == 0:
        p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
    ptr += 1
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

"""
Various methods of drawing scrolling plots.
"""

from time import perf_counter

import numpy as np

import pyqtgraph as pg

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('pyqtgraph example: Scrolling Plots')


# 1) Simplest approach -- update data in the array such that plot appears to scroll
#    In these examples, the array size is fixed.
p1 = win.addPlot()
p2 = win.addPlot()
data1 = np.random.normal(size=300)
curve1 = p1.plot(data1)
curve2 = p2.plot(data1)
ptr1 = 0
def update1():
    global data1, ptr1
    data1[:-1] = data1[1:]  # shift data in the array one sample left
                            # (see also: np.roll)
    data1[-1] = np.random.normal()
    curve1.setData(data1)

    ptr1 += 1
    curve2.setData(data1)
    curve2.setPos(ptr1, 0)


# 2) Allow data to accumulate. In these examples, the array doubles in length
#    whenever it is full.
win.nextRow()
p3 = win.addPlot()
p4 = win.addPlot()
# Use automatic downsampling and clipping to reduce the drawing load
p3.setDownsampling(mode='peak')
p4.setDownsampling(mode='peak')
p3.setClipToView(True)
p4.setClipToView(True)
p3.setRange(xRange=[-100, 0])
p3.setLimits(xMax=0)
curve3 = p3.plot()
curve4 = p4.plot()

data3 = np.empty(100)
ptr3 = 0

def update2():
    global data3, ptr3
    data3[ptr3] = np.random.normal()
    ptr3 += 1
    if ptr3 >= data3.shape[0]:
        tmp = data3
        data3 = np.empty(data3.shape[0] * 2)
        data3[:tmp.shape[0]] = tmp
    curve3.setData(data3[:ptr3])
    curve3.setPos(-ptr3, 0)
    curve4.setData(data3[:ptr3])


# 3) Plot in chunks, adding one new plot curve for every 100 samples
chunkSize = 100
# Remove chunks after we have 10
maxChunks = 10
startTime = perf_counter()
win.nextRow()
p5 = win.addPlot(colspan=2)
p5.setLabel('bottom', 'Time', 's')
p5.setXRange(-10, 0)
curves = []
data5 = np.empty((chunkSize+1,2))
ptr5 = 0

def update3():
    global p5, data5, ptr5, curves
    now = perf_counter()
    for c in curves:
        c.setPos(-(now-startTime), 0)

    i = ptr5 % chunkSize
    if i == 0:
        curve = p5.plot()
        curves.append(curve)
        last = data5[-1]
        data5 = np.empty((chunkSize+1,2))
        data5[0] = last
        while len(curves) > maxChunks:
            c = curves.pop(0)
            p5.removeItem(c)
    else:
        curve = curves[-1]
    data5[i+1,0] = now - startTime
    data5[i+1,1] = np.random.normal()
    curve.setData(x=data5[:i+2, 0], y=data5[:i+2, 1])
    ptr5 += 1


# update all plots
def update():
    update1()
    update2()
    update3()
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

if __name__ == '__main__':
    pg.exec()


""" CHAT GPT """
import sys
import queue
import threading
import numpy as np
import sounddevice as sd
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg


class NoisePlot(QtWidgets.QMainWindow): #set up plot widget in herit from QMainWindow
    def __init__(self, data_queue, fs, downsample, window_ms): #initializaiton method
        super().__init__() #refers to the base class and uses that __init__ func

        self.q = data_queue #creates refernce to the main data queue so we can pull data from it

        # Setup the plot
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)
        self.plot_widget.setYRange(-1, 1)
        self.plot_widget.showGrid(y=True)

        length = int(window * fs / (1000 * downsample))
        self.plotdata = np.zeros(length)
        self.curve = self.plot_widget.plot(self.plotdata, pen='y') #whats 'curve?'

        # Timer to update plot
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(30)  # update every 30ms

        #why do we use self so many times? becuase it must be passed by any function in the class
        #use self if we want to make it  a variable we can call from the class??
        # use it for the __init__() method
        # instance variable  ie self. are unique to each instance

    def update_plot(self):
        updated = False
        while not self.q.empty():
            try:
                data = self.q.get_nowait().flatten()
                shift = len(data)
                self.plotdata = np.roll(self.plotdata, -shift)
                self.plotdata[-shift:] = data
                updated = True
            except queue.Empty:
                break
        if updated:
            self.curve.setData(self.plotdata)

    # how does the class function have access to 'q'? it doesn't get passed in?
    # is the class able to see the queue q? do we need to pass it into the graph object?
    # if this was in a different Module and que was named something else it wouldn't work?
# ===========================
# Main
# ===========================
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # Start audio in background
    audio_thread = threading.Thread(target=play_audio, daemon=True)
    audio_thread.start()

    window = NoisePlot()
    window.setWindowTitle("White Noise Scope")
    window.show()

    sys.exit(app.exec_())
