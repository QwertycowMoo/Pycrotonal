"""Test for the keyinput class"""
import time
import unittest
import threading

import pynput
from src.keyinput import Keyboard, SCALE_60_EDO
from pynput.keyboard import Key, Controller, KeyCode


class TestKeyboard(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.keyboard = Keyboard(440, 24)
        self.controller = Controller()
        self.keyboard.start_listening()

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
        self.controller.press('d')
        time.sleep(1)
        self.controller.release('d')
        self.assertEqual(self.keyboard.get_freq(), -1)

    def test_press_inside_scale(self):
        self.controller.press('2')
        time.sleep(1)
        self.controller.release('2')
        self.assertAlmostEqual(self.keyboard.get_freq(), 479.8234)
        
    def test_12edo_keyscale(self):
        keyscale = self.keyboard.find_key_scale(12)
        self.assertEqual(
            keyscale,
            [
                Key.f1,
                Key.f2,
                Key.f3,
                Key.f4,
                Key.f5,
                Key.f6,
                Key.f7,
                Key.f8,
                Key.f9,
                Key.f10,
                Key.f11,
                Key.f12,
            ],
        )

    def test_33edo_keyscale(self):
        keyscale = self.keyboard.find_key_scale(33)
        self.assertEqual(
            keyscale,
            [
                Key.f1,
                KeyCode.from_char("1"),
                KeyCode.from_char("q"),
                Key.f2,
                KeyCode.from_char("2"),
                KeyCode.from_char("w"),
                Key.f3,
                KeyCode.from_char("3"),
                KeyCode.from_char("e"),
                Key.f4,
                KeyCode.from_char("4"),
                KeyCode.from_char("r"),
                Key.f5,
                KeyCode.from_char("5"),
                KeyCode.from_char("t"),
                Key.f6,
                KeyCode.from_char("6"),
                KeyCode.from_char("y"),
                Key.f7,
                KeyCode.from_char("7"),
                KeyCode.from_char("u"),
                Key.f8,
                KeyCode.from_char("8"),
                KeyCode.from_char("i"),
                Key.f9,
                KeyCode.from_char("9"),
                KeyCode.from_char("o"),
                Key.f10,
                KeyCode.from_char("0"),
                KeyCode.from_char("p"),
                Key.f11,
                KeyCode.from_char("-"),
                KeyCode.from_char("["),
            ],
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
