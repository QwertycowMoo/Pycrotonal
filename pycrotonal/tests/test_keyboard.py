"""Test for the keyinput class"""
import time
import unittest
from pynput.keyboard import Key, Controller
from src.keyinput import Keyboard, SCALE_12_EDO, SCALE_36_EDO, SCALE_60_EDO



class TestKeyboard(unittest.TestCase):
    """Test the keyboard"""
    @classmethod
    def setUpClass(cls) -> None:
        """Creates a keyboard listener and controller"""
        cls.keyboard = Keyboard(440, 24)
        cls.controller = Controller()
        cls.keyboard.start_listening()

    def test_a_keyinput(self):
        """Test any key input that there is a response"""
        self.controller.press("1")
        self.assertFalse(self.keyboard.get_freq() == -1, "check there is something")

    def test_a440_key(self):
        """Test that the first note is A 440 initialized by the keyboard constructor"""
        self.controller.press(Key.f1)
        time.sleep(1)
        self.controller.release(Key.f1)
        self.assertEqual(self.keyboard.get_freq(), 440)

    def test_press_outside_scale(self):
        """Try to push a key outside the constructed scale"""
        self.controller.press('d')
        time.sleep(1)
        self.controller.release('d')
        self.assertEqual(self.keyboard.get_freq(), -1)

    def test_press_inside_scale(self):
        """Try to press something inside the scale"""
        self.controller.press('2')
        time.sleep(1)
        self.controller.release('2')
        self.assertAlmostEqual(self.keyboard.get_freq(), 479.8234)
      
    def test_12edo_keyscale(self):
        """Create a 12 edo keyscale"""
        keyscale = self.keyboard.find_key_scale(12)
        self.assertEqual(
            keyscale,
            SCALE_12_EDO,
        )

    def test_33edo_keyscale(self):
        """Create a 33 edo keyscale"""
        keyscale = self.keyboard.find_key_scale(33)
        self.assertEqual(
            keyscale,
            SCALE_36_EDO[0:33]
        )

    def test_60edo_keyscale(self):
        """Test entire keyboard"""
        keyscale = self.keyboard.find_key_scale(60)
        self.assertEqual(keyscale, SCALE_60_EDO)

    def test_neg1edo_keyscale(self):
        """Invalid edo keyscale should throw error"""
        self.assertRaises(ValueError, self.keyboard.find_key_scale, -1)

    def test_outside_edo_keyscale(self):
        """Invalid edo keyscale should throw error"""
        self.assertRaises(ValueError, self.keyboard.find_key_scale, 61)

if __name__ == "__main__":
    unittest.main()
