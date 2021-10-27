"""Implementation of the Square Wave using PYO's RCOsc"""
from pyo import RCOsc
from .synth import Synth

class SquareWave(Synth):
    """Square waveform"""

    def __init__(self, freq, amp):
        """Constructor, uses RCOsc with 1 sharpness"""
        self._freq = freq
        self._amp = amp
        # Sharp determines shape of waveform, 0 = triangle
        self._osc = RCOsc(freq=self._freq, sharp=1, mul=self._amp)

    def get_synth(self):
        """Returns the oscillator to be played"""
        return self._osc