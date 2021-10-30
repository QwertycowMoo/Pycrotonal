"""Implementation of the Triangle Wave using PYO's RCOsc"""
from pyo import Osc, TriangleTable
from .synth import Synth
from .synth import SAMPLE_RATE

class TriangleWave(Synth):
    """Triangle waveform"""

    def __init__(self, freq, amp):
        """Constructor, uses RCOsc with 0 sharpness"""
        self._freq = freq
        self._amp = amp
        self._wavetable = TriangleTable(order=20)
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
                amplitudes.append(1/ (o * o))
        return harmonics, amplitudes