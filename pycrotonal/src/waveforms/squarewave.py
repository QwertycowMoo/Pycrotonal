"""Implementation of the Square Wave using PYO's RCOsc"""
from pyo import Osc
from pyo.lib.tables import SquareTable
from .synth import SAMPLE_RATE, Synth

class SquareWave(Synth):
    """Square waveform"""

    def __init__(self, freq, amp):
        """Constructor, uses RCOsc with 1 sharpness"""
        self._freq = freq
        self._amp = amp
        self._wavetable = SquareTable(order=25)
        # Sharp determines shape of waveform, 0 = triangle
        self._osc = Osc(table=self._wavetable, freq=self._freq, mul=self._amp)

    def get_synth(self):
        """Returns the oscillator to be played"""
        return self._osc
    
    def get_harmonics(self):
        """Return an amplitude spread, 1/n up until nyquist limit"""
        harmonics = []
        amplitudes = []
        for o in range(1, self._wavetable.order):
            if o % 2 == 1:
                if (o * self._freq > SAMPLE_RATE):
                    break
                harmonics.append(o * self._freq)
                amplitudes.append(1/ o)
        return harmonics, amplitudes