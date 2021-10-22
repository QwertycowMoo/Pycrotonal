from pyo import *
import abc

import pyo
# pyo must start the server before anything else

class Synth(abc.ABC):
    _wavetable: pyo.PyoTableObject
    _fm_amp: float
    _fm_index: float
    _reverb: float
    _distortion: float
    _freq: float
    _amp: float

    @property
    def fm_amp(self):
        return self._fm_amp

    @property
    def fm_index(self):
        return self._fm_index

    @property
    def reverb(self):
        return self._reverb

    @property
    def distortion(self):
        return self._distortion

    @property
    def freq(self):
        return self._freq
    
    @property
    def amp(self):
        return self._amp
    
    @abc.abstractmethod
    def get_synth(self):
        pass



# Design: Likely create a synth object with waveform, FM params, Reverb, Distortion, ADSR
# Then use the object to create a synth on the server
