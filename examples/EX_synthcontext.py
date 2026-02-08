"""
Based on wavetable example from JUCE
trying to understand classes and context in simplified format
"""

class WavetableOscillator(): #do you pass var in class def?

    # Members
    buffer wavetable
    float currentIndex
    float tableDelta


    #Functions
    Constructor WavetableOscillator(buffer wavetableToUse):
        wavetable = wavetableToUse

    setFrequency(freq, sampleRate):

    getNextSample():
        #do stuff to generate sample
        return currentSample

#Synth context
class MainAudioComponent():

    # Members
    int tableSize
    float level

    buffer sineTable
    array oscillators #for more than one oscillator

    # Functions
    Constructor MainAudioComponent():
        createWavetable()

    createWavetable():
        fill sineTable with samples

    prepareToPlay(sampleRate):
        """
        Create oscillators
        """
        oscillator = WavetableOscillator(sineTable)

        freq = 440

        oscillator.setFrequency(freq, sampleRate)

        oscillators.add(oscillator)

    #AUDIO CALL BACK
    getNextAudioBlock(bufferToFill):
        #fill audio buffer with data

        for sample in bufferToFill:
            newsample = oscillator.getNextSample * level

def play_audio(call_back):
    with sd.OutputStream(samplerate=fs,channels=1, callback=call_back):
        while True:
            sd.sleep(1000)

//=========MAIN================================================================


synth = MainAudioComponent()

synth.prepareToPlay()


audio_thread = threading.Thread(target=play_audio(synth.getNextAudioBlock), daemon=True)
audio_thread.start()
