import queue
import sys
import threading
import numpy as np
import sounddevice as sd
import time

from math import floor
from rtmidi.midiutil import open_midiinput

"""
GOAL: add MIDI control for pitch and note on/off to wavetable synth

Read in midi events using call back
convert note number to pitch in hertz
reset the oscialtor frequency
implement a gate for note on off
    If note on
        gain = 1
    if note off
        gain = 0

make sure you do these steps in the right order
turn off previous note
reset pitch
start next note


set overall level
"""

"""
SYSTEM INFO
sample rate: 44100
bit depth: 24bit integer
2 channels
"""

#frames/samples per second
fs = 44100

class WavetableOscillator():
    def __init__(self, tableToUse, tableSize):
        self.wavetable = tableToUse #refernce to wavetable
        self.tableSize = tableSize
        self.currentIndex = 0.0 #float
        self.tableDelta = 0.0 #foat
        self.currentNote = 0
        self.IsPlaying = False


    """ TODO set level? """
    def startNote(self, noteNumber, velocity):

        self.currentNote = noteNumber
        freq = 440.0 * 2 ** ((noteNumber - 69) / 12)
        self.tableDelta = self.tableSize*freq/fs
        self.IsPlaying = True

    def stopNote(self):
        self.currentNote = 0
        self.IsPlaying = False
        self.tableDelta = 0
        self.currentIndex = 0


    """ re-write to produce multiple samples """
    def getNextBlock(self, frames, buffer):

        for i in range(frames):
            current_indx = self.currentIndex #copy so we don't accidently reassign
            index0 = floor(current_indx) #could cast to int but this is more readable IMO

            # Ternary Operator: <true value> if <logic test> else <false value>
            index1 = 0 if index0 == (self.tableSize - 1) else (index0 + 1)

            frac = current_indx - index0 # value between 0 and 1 is the interpolation value

            value0 = self.wavetable[index0]
            value1 = self.wavetable[index1]

            nextSample = value0 + frac * (value1 - value0)

            buffer[i]+= nextSample

            self.currentIndex += self.tableDelta
            if self.currentIndex > float(self.tableSize):
                self.currentIndex -= self.tableSize


class MidiHandler():
    def __init__(self, midi_buffer, port):
        self.port = port
        self.midiBuffer = midi_buffer

    #make the instance object call able
    def __call__(self, event, data = None):
            message, deltatime = event
            self.midiBuffer.put(message)

class Synth():
    def __init__(self, midi_buffer):
        self.tableSize = 128
        self.waveTable = np.zeros(self.tableSize)
        self.bufferSize = 1024 #safe assumption for hi latency
        self.buffer = np.zeros(self.bufferSize)
        self.createWavetable()

        self.midiBuffer = midi_buffer

        self.voices = []

        self.activeVoices = 0

    def createWavetable(self):
        #divide the 2pi cycle in 127 sections
        angleDelta = 2.0 * np.pi / float(self.tableSize-1) #do we need to type cast for dividion?
        currentAngle = 0.0

        for i in range(self.tableSize):
            sample = np.sin(currentAngle)
            self.waveTable[i] = sample
            currentAngle += angleDelta

    def prepareToPlay(self):
        self.voices.append(WavetableOscillator(self.waveTable, self.tableSize))

    """ Sketchy but should work"""
    def handleMidi(self, message):
        #probably a better way to parse this
        #note on = 144, note off = 128
        onOff = message[0]
        noteNumb = message[1]
        velocity = message[2]

        #if note on
        if onOff == 144:

            if self.activeVoices == len(self.voices):
                self.voices.append(WavetableOscillator(self.waveTable, self.tableSize))

            #find an open voice and start  note
            for voice in self.voices:
                if not voice.IsPlaying:
                    voice.currentNote = noteNumb
                    voice.startNote(noteNumb, velocity)
                    break

            self.activeVoices += 1
            #what if there are no open voices?
            #allocate another voices
        #note off
        elif onOff == 128:
            for voice in self.voices:
                if voice.currentNote == noteNumb:
                    voice.stopNote()

            self.activeVoices -= 1

    def render_Frames(self, frames):
        self.buffer = np.zeros(self.bufferSize)
        #Do we need to clear the buffer?
        for voice in self.voices:
            if voice.IsPlaying:
                voice.getNextBlock(frames, self.buffer)

        return self.buffer[:frames].reshape(-1,1)



def audio_callback(outdata, frames, time, status):
    # 1. Process pending MIDI events
    while not midi_buffer.empty():
        msg = midi_buffer.get_nowait()
        sineSynth.handleMidi(msg)

    # 2. Generate samples
    outdata[:] = sineSynth.render_Frames(frames)

def midi_callback(self, event, data = None):
        message, deltatime = event
        self.midiBuffer.put(message)
#How do I wrap this or pass the synth call back?
"""
def play_audio(call_back):
    with sd.OutputStream(samplerate=fs,channels=1, callback=call_back):
        while True:
            sd.sleep(1000)
"""

if __name__ == '__main__':

    midi_buffer = queue.Queue()


    sineSynth = Synth(midi_buffer)
    sineSynth.prepareToPlay()

    try:
        midi_in, port_name = open_midiinput(2)
        print(port_name)
    except (EOFError, KeyboardInterrupt):
        print("that port didn't work")


    keyboardState = MidiHandler(midi_buffer, port_name)

    #midi_in = rtmidi.MidiIn()
    #midi_in.open_port(2) #pretty sure this is my keyboard
    midi_in.set_callback(keyboardState)


    # Audio stream setup
    with sd.OutputStream(channels=1, callback=audio_callback, samplerate=fs):
                     input("Press Enter to quit...\n")

    """
    #create seperate audio thread. what is daemon?
    audio_thread = threading.Thread(target=play_audio(sineSynth.audio_callback), daemon=True)
    audio_thread.start()

    #Midi stuff

    try:
        midiin, port_name = open_midiinput(port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    print("Attaching MIDI input callback handler.")
    midiin.set_callback(MidiInputHandler(port_name))

    print("Entering main loop. Press Control-C to exit.")
    try:
        # Just wait for keyboard interrupt,
        # everything else is handled via the input callback.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin
    """
