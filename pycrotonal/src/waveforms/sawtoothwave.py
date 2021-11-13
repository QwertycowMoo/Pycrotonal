"""Implementation of the Sawtooth Wave using PYO's Saw Table"""
from pyo import SawTable, Osc
from .synth import Synth, SAMPLE_RATE


class SawtoothWave(Synth):
    """Triangle waveform"""

    def __init__(self, freq, adsr):
        """Constructor, uses SawTable to avoid aliasing with LinTable
        Freq is fundemental frequency
        adsr is Adsr object to control attack decay sustain release"""
        self.order = 25
        self.freq = freq
        self.adsr = adsr
        self._wavetable = SawTable(order=self.order)
        self._osc = Osc(table=self._wavetable, freq=self._freq, mul=self._adsr)

    def get_harmonics(self):
        """Return an amplitude spread, 1/n up until nyquist limit"""
        harmonics = []
        amplitudes = []
        for order in range(1, self._wavetable.order):
            if order * self._freq > SAMPLE_RATE:
                break
            harmonics.append(order * self._freq)
            amplitudes.append(1 / order)
        return harmonics, amplitudes
