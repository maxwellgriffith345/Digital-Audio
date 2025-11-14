"""
how to handle MIDI input events
how tp ass the midi info from midi call back to the rest of scope

what is the message thread?
what is a listener?
    Receives events from a MidiKeyboardState object.

JUCE example
https://juce.com/tutorials/tutorial_handling_midi_events/

some kind of inter-thread communication is necessary in a MIDI application
but the exact implementation depends on the circumstances

note on/off messages, and these are used to start and stop the voices playing the appropriate sounds

"""
//==============================================================================
#Chat GPT EXAMPLE- you tried to make this too complicated

""" to wrap midi in a class you could pass the synth as a refernce to the
midi instance and pass the midi instance to the synth class """

que midi_que

Synthesiser synth


#pass refernce to midi_que
midiHandler = MidiHandler(midi_que)

#pass refernce to midi_que
synth = Synthesiser(midi_que)


def midi_callback(message, data):
    msg, delta = msg
    midi_que.put(msg)


def audio_callback(frames):

    #if you keep adding midi notes/playing gast will this ever exit?
    while midique isn't empty:
        message = que.get()
        synth.handleMidi(message)

    output[:] = synth.renderFrames(frames)

""" MAIN """
midin, port_name = open_midiinput(port)
midiin.set_callback(midi_callback())

//==============================================================================
#JUCE EXAMPLE

class MainComponent:

    #Objects
    MidiKeybordState keyboardState
    SynthAduioSource synthAudioSource


    def MainComponent():
        synthAudioSource(keyboardState)


    def prepareToPlay(sampleRate):

        synthAudioSource.prepareToPlay(sampleRate)

    """ THIS IS THE TOP LEVEL AUDIO CALLBACK """
    def getNextAduioBlock(bufferToFill):
        synthAudioSource.getNextAduioBlock(bufferToFill)



class SynthAduioSource:
    """
    This class combines the midi and audio handling
    """

    #objects
    Synthesiser synth
    MidiKeyboardState keyState

    """
    create synth object & add voices to synth
    """
    def SynthAduioSource(keyState):
        "add voices to synth object"

    """
    add new midi from keybaordState to midi buffer
    pass midi to synth and generate audio
    """
    def getNextAduioBlock(bufferToFill):

        #fill midi buffer with new midi data
        # this uses a MIDI buffer not a midi callback
        midibuffer newMidi
        keyboardState.precessNextMidiBuffer(newMidi)

        #synth handles midi messages and generates audio
        # how does synth do that?
        synth.rednerNextBlock(bufferToFill, newMidi)


class Synthesiser:
    """"
    handles the MIDI data
    finds a free voice and fills the audio buffer
    """
    #Objects
    array voices


    def addVoice(newVoice):

    """
    it'll try to find a free voice, and use the
        voice to start playing the sound
    """
    def handleMidiEvent(message):
        if message = note on:
            noteOn (message.getNoteNumber, message.velocity)
        if message = note off:
            noteOff(message.getNoteNumber)
        else:


    def noteOn(midiChannel, midiNoteNumber, velocity):
            """ TODO """
            #if any voice is playing note
            stopVoice(voice)

            #find a free voice and start note
            #startVoice( voice = findFreeVoice(), midinutNumber, velocity)

            for voice in voices:
                if not voice.isActive():
                    voice.currentNote = midiNoteNumber
                    voice.startNote(midiNotenumber, velocity)
                    break

"""
    def startVoice(voice, midiNoteNumber, velocity):

        voice.currentNote = midiNoteNumber
        voice.startNote(midiNoteNumber, velocity)

    def findFreeVoice():

"""

    """
    turn off the voice currently playing midiNoteNumber

    """
    def noteOff(midiChannel, midiNoteNumber, velocity):

    def rednerVoices():
        for voice in voices:
            voice.rednerNextBlock(buffer)



    """
    process next audio data from all voices and add to buffer

    midi events are parsed for note and controller events and are used to
    trigger the voices

    Uses a MIDI buffer not sure what to do when using a callback??

    """
    def renderNextBlock(bufferToFill, newMidiBuffer, startSample, numSamples):

        # Generally
        # Will this block?
        if newMidiEvent:
            handleMidiEvent(newMidiBuffer.message)
            renderVoices(bufferToFill, startSample, numSamples)
        else:
            renderVoices()

        """
        while (more samples left)
        {
            figure out when the next MIDI event happens;
            render all currently playing voices until that point;
            apply the MIDI event (start/stop/change notes);
        }

        """

class SineWaveVoice:

    """
    Only dealing with midi messages that are start/stop

    """

    def startNote(midiNoteNumber, velocity):
        """
        set level

        Set frequency
            convert midiNoteNumber to Hertz
            set angleDelta
        """
    def stopNote():
        angleDelta = 0


    """ TODO """
    def getCurrentNote():

    """
    where the auido is acutally generated
    """
    def rednerNextBlock(bufferToFill, startSample, numSamples):
        """
        fill buffer with audio data
        addSample does not overwrite the current sample
        it sum the values to gether ie in the case of multiple voices
        all the data would be summed together
        """
        for number of samples:
            currentSample =
            outputBuffer.addSample(currentSample)
