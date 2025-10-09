import queue
import sys
import threading
import numpy as np
import sounddevice as sd

from math import floor

"""
GOAL: create a sine wave table oscillator based on the JUCE tutorial
https://juce.com/tutorials/tutorial_wavetable_synth/

TODO: create a wavetalbe structure that holds the array and the size of the table
pass a refernce to the oscillator object

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

# Create a buffer to hold the wavetable
"""
waveTable =[] #probably something better to use than a list
tableSize = 128
"""


class WavetableOscillator():
    def __init__(self, tableToUse, tableSize):
        self.wavetable = tableToUse #refernce to wavetable
        self.currentIndex = 0.0 #float
        self.tableDelta = 0.0 #foat
        self.tableSize = tableSize

    def setFrequency(self, freq):
        self.tableDelta = self.tableSize*freq/fs #CHECK THIS IS FLOAT
        """
        fs is in the global app context
        tableSize should be in the synth context?

        before: delta = 2pi*freq/sampleRate
        wave table =    tablesize*freq/SampleRate

        both 2pi and tablesize represent how far the distance
        needed to complete one cycle
        instead radian distance of 2pi it is distance around the
        wave table, kinda makes sense?

        2pi is one cycle a second so to get freq cycles/second we need to multiple
        by 2pi
        likewise
        tablesize is one cycle a second so to get freq cycles/second we need to
        multiple by tablesize
        """

    """
    TODO
    interpolate between the wave table values
    """
    def getNextSample(self):
        current_indx = self.currentIndex #copy so we don't accidently reassign
        index0 = floor(current_indx) #could cast to int but this is more readable IMO

        # Ternary Operator: <true value> if <logic test> else <false value>
        index1 = 0 if index0 == (self.tableSize - 1) else (index0 + 1)

        frac = current_indx - index0 # value between 0 and 1 is the interpolation value

        value0 = self.wavetable[index0]
        value1 = self.wavetable[index1]

        nextSample = value0 + frac * (value1 - value0)

        self.currentIndex += self.tableDelta
        if self.currentIndex > float(self.tableSize):
            self.currentIndex -= self.tableSize

        return nextSample

        """
        Pseudo Code
        currentIndex - index we want the sample value for

        index0,index1 - indexes of wavetable that surround currentIndex
            index1 is the next index after index0

        value0,value1 - table values that surround currentSample

        frac = currentIndex - index0 should be between 0 and 1

        linear interpolate
        y = y1 + (x-x1) * (y2-y1)/(x2-x1)

        in our case x2-x1 will always be 1, or it should be

        """

class SineOsc():
    def __init__(self, freq):
        self.current_angle = 0.0
        self.frequency = freq
        self.delta = 2.0*np.pi*freq/fs #do we need to typecase to float for division

    # def setfreq():
        #need to implement this if we want to change the freq

    def get_frames(self, frames):
        angles = self.current_angle + np.arange(frames)*self.delta
        angles = angles.reshape(-1,1)
        signal = volume*np.sin(angles)
        self.current_angle = angles[-1] + self.delta
        return signal

""" TODO
make waveTable an ndarray
sample array in call back should not be allocated in the callback
move it to a buffer in the synth class
"""
class Synth():
    def __init__(self):
        self.tableSize = 128
        self.waveTable = []
        self.createWavetable()


    def createWavetable(self):
        #divide the 2pi cycle in 127 sections
        angleDelta = 2.0 * np.pi / float(self.tableSize-1) #do we need to type cast for dividion?
        currentAngle = 0.0

        for i in range(self.tableSize):
            sample = np.sin(currentAngle)
            self.waveTable.append(sample)
            currentAngle += angleDelta

    def prepareToPlay(self):
        self.oscillator = WavetableOscillator(self.waveTable, self.tableSize)
        freq = 440
        self.oscillator.setFrequency(freq) #does this have visiblity to tableSize?

    """ Re-write this """
    def audio_callback(self, outdata, frames, time, status):
        samples = [] #needs to ndarray
        for i in range(frames):
            samples.append(self.oscillator.getNextSample())
        samples = np.array(samples).reshape(-1,1)
        outdata[:] = samples

#How do I wrap this or pass the synth call back?
def play_audio(call_back):
    with sd.OutputStream(samplerate=fs,channels=1, callback=call_back):
        while True:
            sd.sleep(1000)


if __name__ == '__main__':

    #waveTable =[] #probably something better to use than a list
    #tableSize = 128

    #createWavetable()

    #print(len(waveTable))
    #print(*waveTable)

    sineSynth = Synth()
    sineSynth.prepareToPlay()
    #create seperate audio thread. what is daemon?
    audio_thread = threading.Thread(target=play_audio(sineSynth.audio_callback), daemon=True)
    audio_thread.start()
