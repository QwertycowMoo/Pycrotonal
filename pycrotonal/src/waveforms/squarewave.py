"""Implementation of the Square Wave using PYO's RCOsc"""
from pyo import Osc
from pyo.lib.tables import SquareTable
from .synth import SAMPLE_RATE, Synth


class SquareWave(Synth):
    """Square waveform"""

    def __init__(self, freq, adsr):
        """Constructor, uses Squaretable to avoid aliasing
        Freq is fundemental frequency
        adsr is Adsr object to control attack decay sustain release"""
        self._freq = freq
        self._adsr = adsr
        self._wavetable = SquareTable(order=25)
        # Sharp determines shape of waveform, 0 = triangle
        self._osc = Osc(table=self._wavetable, freq=self._freq, mul=self._adsr)

    def get_harmonics(self):
        """Return an amplitude spread, 1/n up until nyquist limit"""
        harmonics = []
        amplitudes = []
        for order in range(1, self._wavetable.order):
            if order % 2 == 1:
                if order * self._freq > SAMPLE_RATE:
                    break
                harmonics.append(order * self._freq)
                amplitudes.append(1 / order)
        return harmonics, amplitudes
