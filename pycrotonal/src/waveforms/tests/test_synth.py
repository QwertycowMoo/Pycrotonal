"""Test for the synths"""
from src.waveforms.synth import Synth
from src.waveforms.sinewave import SineWave
from src.waveforms.squarewave import SquareWave
from src.waveforms.trianglewave import TriangleWave
from src.waveforms.sawtoothwave import SawtoothWave


def test_sine_harmonics():
    """Test the sine harmonics, should just be 1"""
    sine = SineWave(100)
    assert sine.get_harmonics() == 100


def test_square_harmonics():
    """Test the square wave harmonics, should be odd harmonics up until the nyquist limit
    w/amplitude of 1/n"""
    square = SquareWave(100)
    print(square.get_harmonics())
    assert square.get_harmonics() == 100
