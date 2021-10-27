"""Synth engine for Pycrotonal
This module will apply the sound effects onto the original waveform"""
import abc
from pyo import PyoTableObject
from pyo import PyoObject

# pyo must start the server before anything else


class Synth(abc.ABC):
    """Synth class that can later be subclassed into specific
    Implementation of waveforms"""

    _wavetable: PyoTableObject
    _fm_amp: float
    _fm_index: float
    _reverb: float
    _distortion: float
    _amp: float
    _osc: PyoObject

    @property
    def fm_amp(self):
        """FM amplitude"""
        return self._fm_amp

    @fm_amp.setter
    def fm_amp(self, value):
        """fm_amp setter"""
        self._fm_amp = value

    @property
    def fm_index(self):
        """Fm index of modulation = modulation deviation/fm_freq
        Usually index is given as a ratio and pyo supports taking index directly"""
        return self._fm_index

    @fm_index.setter
    def fm_index(self, value):
        """fm_index setter"""
        self._fm_index = value

    @property
    def reverb(self):
        """Amount of reverb (units tbd)"""
        return self._reverb

    @reverb.setter
    def reverb(self, value):
        """reverb setter"""
        self._reverb = value

    @property
    def distortion(self):
        """dB of gain, likely will use Hard Clip distortion"""
        return self._distortion

    @distortion.setter
    def distortion(self, value):
        """distortion setter"""
        self._distortion = value

    @property
    def freq(self):
        """Base frequency"""
        return self._freq

    @freq.setter
    def freq(self, value):
        """freq setter"""
        if value < 0 or value > 22000:
            raise ValueError("This is outside the range of hearing!")
        self._freq = value
        self._osc.setFreq(self._freq)
        
    @property
    def amp(self):
        """Amplitude (loudness)"""
        return self._amp

    @amp.setter
    def amp(self, value):
        """amp setter, limits at 1"""
        if value > 1:
            raise ValueError("Amplitude cannot be larger than 1!")
        self._amp = value

    @abc.abstractmethod
    def get_synth(self):
        """Gets the pyo synth object, will need to be implemented
        in the subclasses"""


# Design: Likely create a synth object with waveform, FM params, Reverb, Distortion, ADSR
# Then use the object to create a synth on the server
