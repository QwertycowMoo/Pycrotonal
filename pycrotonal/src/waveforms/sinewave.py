"""Sinewave implementation"""
from pyo import Sine
from pyo.lib.tables import HarmTable

# Trying to run this script by itself will throw an ImportError
# But trying to run this through main.py will work because of relative import
from .synth import Synth


class SineWave(Synth):
    """Sinewave waveform"""

    def __init__(self, freq, amp):
        """Constructor, uses the base harmonic table with 1 harmonic"""
        self._amp = amp
        self._osc = Sine(freq=freq, mul=self._amp)

    def get_synth(self):
        """Returns the oscillator to be played"""
        return self._osc