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
TODO: have freq slider be log scale
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

def on_feq_change(logfreq):
    freq = 10 ** float(logfreq)
    update_angledelta(freq)

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
        angles = angles.reshape(-1,1)
        outdata[:] = volume*np.sin(angles)
        current_angle = angles[-1] + angle_delta


def play_audio():
    #Port Audio OutputStream
    #context manager for a real time audio stream
    with sd.OutputStream(samplerate=fs, channels=1,
                        callback=sine_callback):

        #the stream will automatically close when we reach the end of the "with"
        #block so we need to keep a loop going so the stream stays alive
        while True:
            sd.sleep(1000) #what dis do?

""" MAIN """
# set up audio thread
# need to put audio stuff on a different thread otherwise the
#program wont advance past invoking play_audio()
#need to keep going to use the UI
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
#log scale log10(40)=1.60 log10(5000)~3.7
freq_scale = ttk.Scale(mainframe, orient=HORIZONTAL,
                        length = 200, from_ = 1.60, to=3.7,
                        command = on_feq_change)
freq_scale.grid(column = 0, row =2, sticky = 'we')
freq_scale.set(2.643)

"""
vol_scale = ttk.Scale(mainframe, orient=HORIZONTAL,
                        length = 200, from_ = 0.0, to = 1.0,
                        command = update_vol)

vol_scale.grid(column = 0, row =3, sticky = 'we')
vol_scale.set(.5)
"""
#Create the Play/Pause widget

root.mainloop()
