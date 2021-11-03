"""Sinewave implementation"""
from pyo.lib.generators import Sine

# Trying to run this script by itself will throw an ImportError
# But trying to run this through main.py will work because of relative import
from .synth import Synth


class SineWave(Synth):
    """Sinewave waveform"""

    def __init__(self, freq, amp):
        """Constructor, uses the base harmonic table with 1 harmonic
        Freq is fundemental frequency
        Amp is amplitude (loudness)"""
        self._amp = amp
        self._freq = freq
        self._osc = Sine(freq=freq, mul=self._amp)
        self._distortion = 1
        self._reverb = 0

    def get_harmonics(self):
        """Returns the harmonic spectrum"""
        return self._freq
