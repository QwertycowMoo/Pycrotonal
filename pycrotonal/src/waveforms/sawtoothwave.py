"""Implementation of the Sawtooth Wave using PYO's Saw Table"""
from pyo import SawTable, Osc
from .synth import Synth, SAMPLE_RATE


class SawtoothWave(Synth):
    """Triangle waveform"""

    def __init__(self, freq, amp):
        """Constructor, uses SawTable to avoid aliasing with LinTable"""
        self.order = 25
        self._freq = freq
        self._amp = amp
        self._wavetable = SawTable(order=self.order)
        self._osc = Osc(table=self._wavetable, freq=self._freq, mul=self._amp)

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
