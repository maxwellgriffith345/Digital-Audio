""" Plot white noise signal with sounddevice and matplotlib"""

import queue
import sys


from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

"""
SYSTEM INFO
sample rate: 44100
bit depth: 24bit integer
2 channels
"""

"""
Using Callback method
"""
"""TODO: Not a smooth audio output, coming in and out"""
#frames/samples per second
fs = 44100
#chunk = 1024
#keep the volume between 0 and 1 so I don't blow my speakers
volume = .2
downsample = 10 #amount to downsample
window = 200 #ms visible time
interval = 30 #ms min time between plot updates


#create queue to pass data from callback to graph
q = queue.Queue()

#fill an numpy array with the data
def noise_callback(outdata, frames, time, status):
    noise = np.random.normal(0,volume, size=(frames,1)).astype(np.float32)
    q.put(noise[::downsample,])
    outdata[:]=noise.reshape(-1,1)



def update_plot(frame): #why do we need to pass frame?
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata #access plotdata from outside scope of function
    while True: #why do we need a while True here?
        try:
            data = q.get_nowait() #pull audio data form queue
        except queue.Empty:
            break

        """
        roll the new data on to the end of the last data
        while keeping the display length the same
        the graph updates as we move 'forward' in time
         """
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data

    for column, line in enumerate(lines): #what is lines?
        line.set_ydata(plotdata[:, column])

    return lines





try:

    length = int(window * fs / (1000 * downsample))
    plotdata = np.zeros((length, 1))

    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)

    """Graph formatting"""
    ax.axis((0, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)

    stream = sd.OutputStream(
        samplerate=fs,
        channels=1,
        callback=noise_callback
        )

    ani = FuncAnimation(fig, update_plot, interval, blit=True)

    with stream:
        plt.show()
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
