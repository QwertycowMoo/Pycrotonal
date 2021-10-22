"""Main Control Loop for Pycrotonal"""
import pyo
from waveforms.sinewave import SineWave
# First need to initialize sound objects and things to play
# Then initialize gui and add all children to screen or something
# Then call app.MainLoop()

if __name__ == "__main__":
    s = pyo.Server(sr=48000).boot()
    syn = SineWave(440, .5)
    syn.get_synth().out()
    s.gui(locals())
