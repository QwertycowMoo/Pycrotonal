"""Test for the synths"""
import unittest

from pyo.lib.controls import Adsr
from src.waveforms.sinewave import SineWave
from src.waveforms.squarewave import SquareWave
from src.waveforms.trianglewave import TriangleWave
from src.waveforms.sawtoothwave import SawtoothWave
from src.audioserver import AudioServer


class TestSynths(unittest.TestCase):
    """Test cases for the Synth objects"""

    def setUp(self):
        """Setup an audioserver"""
        self.audioserver = AudioServer()

    def test_sine_harmonics(self):
        """Test the sine harmonics, should just be 1"""
        adsr = Adsr()
        sine = SineWave(100, adsr)
        self.assertEqual(sine.get_harmonics(), 100)

    def test_square_harmonics(self):
        """Test the square wave harmonics, should be odd harmonics up until the nyquist limit
        w/amplitude of 1/n"""
        adsr = Adsr()
        square = SquareWave(1000, adsr)
        self.assertEqual(
            square.get_harmonics(),
            (
                [
                    1000,
                    3000,
                    5000,
                    7000,
                    9000,
                    11000,
                    13000,
                    15000,
                    17000,
                    19000,
                    21000,
                    23000,
                ],
                [
                    1.0,
                    0.3333333333333333,
                    0.2,
                    0.14285714285714285,
                    0.1111111111111111,
                    0.09090909090909091,
                    0.07692307692307693,
                    0.06666666666666667,
                    0.058823529411764705,
                    0.05263157894736842,
                    0.047619047619047616,
                    0.043478260869565216,
                ],
            ),
        )

    def test_triangle_harmonics(self):
        """Test the square wave harmonics, should be odd harmonics up until the nyquist limit
        w/amplitude of 1/n^2"""
        adsr = Adsr()
        triangle = TriangleWave(1000, adsr)
        self.assertEqual(
            triangle.get_harmonics(),
            (
                [1000, 3000, 5000, 7000, 9000, 11000, 13000, 15000, 17000, 19000],
                [
                    1.0,
                    0.1111111111111111,
                    0.04,
                    0.02040816326530612,
                    0.012345679012345678,
                    0.008264462809917356,
                    0.005917159763313609,
                    0.0044444444444444444,
                    0.0034602076124567475,
                    0.002770083102493075,
                ],
            ),
        )

    def test_sawtooth_harmonics(self):
        """Test the square wave harmonics, should be all harmonics up until the nyquist limit
        w/amplitude of 1/n"""
        adsr = Adsr()
        saw = SawtoothWave(1000, adsr)
        self.assertEqual(
            saw.get_harmonics(),
            (
                [
                    1000,
                    2000,
                    3000,
                    4000,
                    5000,
                    6000,
                    7000,
                    8000,
                    9000,
                    10000,
                    11000,
                    12000,
                    13000,
                    14000,
                    15000,
                    16000,
                    17000,
                    18000,
                    19000,
                    20000,
                    21000,
                    22000,
                    23000,
                    24000,
                ],
                [
                    1.0,
                    0.5,
                    0.3333333333333333,
                    0.25,
                    0.2,
                    0.16666666666666666,
                    0.14285714285714285,
                    0.125,
                    0.1111111111111111,
                    0.1,
                    0.09090909090909091,
                    0.08333333333333333,
                    0.07692307692307693,
                    0.07142857142857142,
                    0.06666666666666667,
                    0.0625,
                    0.058823529411764705,
                    0.05555555555555555,
                    0.05263157894736842,
                    0.05,
                    0.047619047619047616,
                    0.045454545454545456,
                    0.043478260869565216,
                    0.041666666666666664,
                ],
            ),
        )

    def test_adsr(self):
        """Tests applying an ADSR on the synth"""
        adsr = Adsr()
        sine = SineWave(100, adsr)
        self.assertNotEqual(sine.adsr, None, "Test that adsr is accepted")

    def test_invalid_adsr(self):
        """Tests applying an invalid ADSR"""
        adsr = 5.0
        self.assertRaises(ValueError, SineWave, 100, adsr)

    def test_set_outside_freq(self):
        """Test setting a frequency outside the range"""
        adsr = Adsr()
        sine = SineWave(440, adsr)
        with self.assertRaises(ValueError):
            sine.freq = 400000

        with self.assertRaises(ValueError):
            sine.freq = -100


if __name__ == "__main__":
    unittest.main()
