import queue
import sys
import threading
import numpy as np
import sounddevice as sd


"""
GOAL: wrap all the sine functionality in a class
figure out how to get the sine object accessible in the audio call back

"""

"""
SYSTEM INFO
sample rate: 44100
bit depth: 24bit integer
2 channels
"""

#frames/samples per second
fs = 44100
volume = .8

freq1 = 2200
freq2 = 500

class SineOsc():
    def __init__(self, freq):
        self.current_angle = 0
        self.frequency = freq
        self.delta = 2.0*np.pi*freq/fs

    def get_frames(self, frames):
        angles = self.current_angle + np.arange(frames)*self.delta
        angles = angles.reshape(-1,1)
        signal = volume*np.sin(angles)
        self.current_angle = angles[-1] + self.delta
        return signal

class Synth():
    def __init__(self):
        self.osc1 = SineOsc(500) #this isn't flexible
        self.osc2 = SineOsc(1000)

    def audio_callback(self, outdata, frames, time, status):
            audio1 = self.osc1.get_frames(frames)
            audio2 = self.osc2.get_frames(frames)
            outdata[:] = (audio1+audio2) #better way to mix this?

#How do I wrap this or pass the synth call back?
def play_audio(call_back):
    with sd.OutputStream(samplerate=fs,channels=1, callback=call_back):
        while True:
            sd.sleep(1000)


if __name__ == '__main__':

    sinesynth = Synth()
    #create seperate audio thread. what is daemon?
    audio_thread = threading.Thread(target=play_audio(sinesynth.audio_callback), daemon=True)
    audio_thread.start()
