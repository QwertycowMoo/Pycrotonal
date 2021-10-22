from pyo.lib.tableprocess import Osc
from pyo.lib.tables import HarmTable
# Trying to run this script by itself will throw an ImportError
# But trying to run this through main.py will work because of relative import
from .synth import Synth

class SineWave(Synth):
    def __init__(self, freq, amp):
        self._freq = freq
        self._amp = amp
        self._wavetable = HarmTable()
        self._osc = Osc(table=self._wavetable, freq=self._freq, mul=self._amp)

    def get_synth(self):
        return self._osc