"""Implementation of the Triangle Wave using PYO's RCOsc"""
from pyo import Osc, TriangleTable
from .synth import Synth, SAMPLE_RATE


class TriangleWave(Synth):
    """Triangle waveform"""

    def __init__(self, freq, amp):
        """Constructor, uses RCOsc with 0 sharpness
        Freq is fundemental frequency
        Amp is amplitude (loudness)"""
        self._freq = freq
        self._amp = amp
        self._wavetable = TriangleTable(order=20)
        self._osc = Osc(table=self._wavetable, freq=self._freq, mul=self._amp)

    def get_harmonics(self):
        """Return an amplitude spread, 1/n up until nyquist limit"""
        harmonics = []
        amplitudes = []
        for order in range(1, self._wavetable.order):
            if order % 2 == 1:
                if order * self._freq > SAMPLE_RATE:
                    break
                harmonics.append(order * self._freq)
                amplitudes.append(1 / (order * order))
        return harmonics, amplitudes
