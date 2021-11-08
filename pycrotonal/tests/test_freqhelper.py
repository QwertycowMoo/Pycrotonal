"""Test for the frequency helper class"""
import unittest
from src.freqhelper import find_scale, find_next_step


class TestScales(unittest.TestCase):
    """Test the frequency scale constructor"""
    def test_find_next_step_12_edo(self):
        """Test the next step in a 12 edo scale"""
        a_sharp = find_next_step(440, 12)
        self.assertAlmostEqual(a_sharp, 466.1637615)

    def test_create_3_edo_scale(self):
        """Test an edo less than 12
        Values found manually and rounded"""
        scale = find_scale(440, 3)
        self.assertEqual(scale, [440.0, 554.3653, 698.4565, 880.0])

    def test_create_31_edo_scale(self):
        """Test an edo greater than 12"""
        scale = find_scale(440, 31)
        self.assertEqual(
            scale,
            [
                440,
                449.949,
                460.123,
                470.527,
                481.1663,
                492.0462,
                503.1721,
                514.5495,
                526.1842,
                538.082,
                550.2488,
                562.6907,
                575.4139,
                588.4248,
                601.7299,
                615.3359,
                629.2495,
                643.4777,
                658.0277,
                672.9067,
                688.1221,
                703.6815,
                719.5927,
                735.8637,
                752.5026,
                769.5178,
                786.9177,
                804.711,
                822.9067,
                841.5138,
                860.5416,
                879.9997,
            ],
        )

    def test_create_1_edo_scale(self):
        """1 EDO edge case"""
        scale = find_scale(440, 1)
        self.assertEqual(scale, [440.0, 880.0])

    def test_create_12_edo_scale(self):
        """Test creating a regular 12 edo scale
        Values found manually"""
        scale = find_scale(130.813, 12)
        correct_12edo = [
                130.813,
                138.5915,
                146.8326,
                155.5637,
                164.8140,
                174.6144,
                184.9975,
                195.9979,
                207.6525,
                220.00,
                233.0818,
                246.94156,
                261.62546,
            ]
        for i in range(len(scale)):
            self.assertAlmostEqual(
                scale[i], correct_12edo[i], 3
            )

    def test_create_3_edo_scale_2_octave(self):
        scale = find_scale(440, 3, 2)
        self.assertEqual(scale, [440, 554.3653, 698.4565, 880.0, 1108.7305, 1396.9129, 1760.0])

    def test_create_invalid_root(self):
        self.assertRaises(ValueError, find_scale, -1, 12, 1)
        
if __name__ == "__main__":
    unittest.main()
