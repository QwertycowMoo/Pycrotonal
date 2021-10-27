"""Implementation of the Sawtooth Wave using PYO's Saw Table"""
from pyo import SawTable, Osc
from .synth import Synth

class SawtoothWave(Synth):
    """Triangle waveform"""

    def __init__(self, freq, amp):
        """Constructor, uses SawTable to avoid aliasing with LinTable"""
        self._freq = freq
        self._amp = amp
        self._wavetable = SawTable(order=25)
        self._osc = Osc(table=self._wavetable, freq=self._freq, mul=self._amp)

    def get_synth(self):
        """Returns the oscillator to be played"""
        return self._osc