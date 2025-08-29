"""
toy example to learn how ImageItem works and how to update it
remove the audio processing side to just learn the graphics
"""

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

import sys

#Chat GPT: functio to generate data to add to the plot. normally shpaed around mean value
def gaussian_array(length=100, mean=None, std=10):
    """
    Returns a (1, length) numpy array shaped like a Gaussian curve.
    Peak = 1 at the mean index.
    """
    if mean is None:
        mean = (length - 1) / 2  # center at middle index

    x = np.arange(length)  # indices from 0 to length-1
    # Gaussian formula, scaled so peak = 1
    values = np.exp(-0.5 * ((x - mean) / std) ** 2)
    values /= values.max()  # normalize so peak = 1

    return values.reshape(1, -1)

def update_data(data):
    new_data = gaussian_array()
    data = np.roll(data, -1, axis = 0)
    data[-1] = new_data
    return data

# Example usage
#arr = gaussian_array()


pg.setConfigOptions()
#imageAxisOrder = 'row-major'

"""
col-major, where the shape of the array represents (width, height)
row-major, where the shape of the array represents (height, width)
"""

pg.mkQApp()
win = pg.GraphicsLayoutWidget()
win.setWindowTitle('noise heat plot')
win.show()

p1 = win.addPlot(title='')

#create image object and add to plot
img = pg.ImageItem()
img.setColorMap('turbo')
p1.addItem(img)

#set color map

#add data
#data = np.random.normal(10, 2.5, size = (50,100))
#data[25,:]=0
data = np.zeros((50,100))
img.setImage(data, autoLevels = True)


def update_plot():
    global data
    data = update_data(data)
    img.setImage(data, autoLevels = True)

timer = pg.QtCore.QTimer()
timer.timeout.connect(update_plot)
timer.start(80)

if __name__ == '__main__':

    sys.exit(pg.exec())
