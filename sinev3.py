import sounddevice as sd
import numpy as np
from tkinter import *
from tkinter import ttk
import threading

"""
SYSTEM INFO
sample rate: 44100
bit depth: 24bit integer
1 channels
"""

"""
Using Tk to control volume and freq
"""

fs = 44100 #samples per second
volume = .8
freq = 440
current_angle = 0.0
angle_delta = 0.0

def update_angledelta(freq):
    cyclesPerSample = float(freq)/fs
    global angle_delta
    angle_delta = cyclesPerSample*2.0*np.pi

"""
def update_vol(vol):
    global volume
    volume = float(vol)
"""
#I think there is a better wat to bind this to the interface

#fill an numpy array with the data
def sine_callback(outdata, frames, time, status):
        global current_angle
        global volume
        angles = current_angle + np.arange(frames)*angle_delta
        angles = angles.reshape(-1,1) #this will start at current anlge
        outdata[:] = volume*np.sin(angles) #need to reshape
        current_angle = angles[-1] + angle_delta


def play_audio():
    with sd.OutputStream(samplerate=fs, channels=1,
                        callback=sine_callback):

        while True: #what dis do?
            sd.sleep(1000)

""" MAIN """
# set up main window
audio_thread = threading.Thread(target=play_audio, daemon=True)
audio_thread.start()

root = Tk()
root.title("Sine Wave")

# set up a content frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#NEED LABELS FOR VOL AND FREQ VALUES

#Create the Freq and Volume Scales
freq_scale = ttk.Scale(mainframe, orient=HORIZONTAL,
                        length = 200, from_ = 40.0, to=10000.0,
                        command = update_angledelta)
freq_scale.grid(column = 0, row =2, sticky = 'we')
freq_scale.set(440)

"""
vol_scale = ttk.Scale(mainframe, orient=VERTICAL,
                        length = 200, from_ = 0.0, to = 1.0,
                        command = update_vol)
"""
#Create the Play/Pause widget

root.mainloop()
