

import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

"""
Creates a window object with the plot inside

"""
class NoisePlot(QtWidgets.QMainWindow):
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
