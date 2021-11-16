"""Keyboard Listener"""
from queue import Queue, Empty
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
from .freqhelper import find_scale

# This was the best way to implement the most amount of flexibility.
# Allows indexing of these "scales" to get EDO scales between 12 and 24
# Example: 7EDO would use f1 to f7. 14EDO would use f1 to f7 and the numerical 1-7 below it

SCALE_12_EDO = [
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
]

SCALE_24_EDO = [
    Key.f1,
    KeyCode.from_char("1"),
    Key.f2,
    KeyCode.from_char("2"),
    Key.f3,
    KeyCode.from_char("3"),
    Key.f4,
    KeyCode.from_char("4"),
    Key.f5,
    KeyCode.from_char("5"),
    Key.f6,
    KeyCode.from_char("6"),
    Key.f7,
    KeyCode.from_char("7"),
    Key.f8,
    KeyCode.from_char("8"),
    Key.f9,
    KeyCode.from_char("9"),
    Key.f10,
    KeyCode.from_char("0"),
    Key.f11,
    KeyCode.from_char("-"),
    Key.f12,
    KeyCode.from_char("="),
]

SCALE_36_EDO = [
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
    Key.f12,
    KeyCode.from_char("="),
    KeyCode.from_char("]"),
]

SCALE_48_EDO = [
    Key.f1,
    KeyCode.from_char("1"),
    KeyCode.from_char("q"),
    KeyCode.from_char("a"),
    Key.f2,
    KeyCode.from_char("2"),
    KeyCode.from_char("w"),
    KeyCode.from_char("s"),
    Key.f3,
    KeyCode.from_char("3"),
    KeyCode.from_char("e"),
    KeyCode.from_char("d"),
    Key.f4,
    KeyCode.from_char("4"),
    KeyCode.from_char("r"),
    KeyCode.from_char("f"),
    Key.f5,
    KeyCode.from_char("5"),
    KeyCode.from_char("t"),
    KeyCode.from_char("g"),
    Key.f6,
    KeyCode.from_char("6"),
    KeyCode.from_char("y"),
    KeyCode.from_char("h"),
    Key.f7,
    KeyCode.from_char("7"),
    KeyCode.from_char("u"),
    KeyCode.from_char("j"),
    Key.f8,
    KeyCode.from_char("8"),
    KeyCode.from_char("i"),
    KeyCode.from_char("k"),
    Key.f9,
    KeyCode.from_char("9"),
    KeyCode.from_char("o"),
    KeyCode.from_char("l"),
    Key.f10,
    KeyCode.from_char("0"),
    KeyCode.from_char("p"),
    KeyCode.from_char(";"),
    Key.f11,
    KeyCode.from_char("-"),
    KeyCode.from_char("["),
    KeyCode.from_char("'"),
    Key.f12,
    KeyCode.from_char("="),
    KeyCode.from_char("]"),
    KeyCode.from_char("\\"),  # \
]

SCALE_60_EDO = [
    Key.f1,
    KeyCode.from_char("1"),
    KeyCode.from_char("q"),
    KeyCode.from_char("a"),
    KeyCode.from_char("z"),
    Key.f2,
    KeyCode.from_char("2"),
    KeyCode.from_char("w"),
    KeyCode.from_char("s"),
    KeyCode.from_char("x"),
    Key.f3,
    KeyCode.from_char("3"),
    KeyCode.from_char("e"),
    KeyCode.from_char("d"),
    KeyCode.from_char("c"),
    Key.f4,
    KeyCode.from_char("4"),
    KeyCode.from_char("r"),
    KeyCode.from_char("f"),
    KeyCode.from_char("v"),
    Key.f5,
    KeyCode.from_char("5"),
    KeyCode.from_char("t"),
    KeyCode.from_char("g"),
    KeyCode.from_char("b"),
    Key.f6,
    KeyCode.from_char("6"),
    KeyCode.from_char("y"),
    KeyCode.from_char("h"),
    KeyCode.from_char("n"),
    Key.f7,
    KeyCode.from_char("7"),
    KeyCode.from_char("u"),
    KeyCode.from_char("j"),
    KeyCode.from_char("m"),
    Key.f8,
    KeyCode.from_char("8"),
    KeyCode.from_char("i"),
    KeyCode.from_char("k"),
    KeyCode.from_char(","),
    Key.f9,
    KeyCode.from_char("9"),
    KeyCode.from_char("o"),
    KeyCode.from_char("l"),
    KeyCode.from_char("."),
    Key.f10,
    KeyCode.from_char("0"),
    KeyCode.from_char("p"),
    KeyCode.from_char(";"),
    KeyCode.from_char("/"),
    Key.f11,
    KeyCode.from_char("-"),
    KeyCode.from_char("["),
    KeyCode.from_char("'"),
    Key.shift_r,  # right shift
    Key.f12,
    KeyCode.from_char("="),  # +
    KeyCode.from_char("]"),
    KeyCode.from_char("\\"),  # \
    Key.backspace,  # backspace
]


class Keyboard:
    """Keyboard Listener class, will listen to keypresses
    Uses the freqhelper class to construct a scale of frequencies and"""

    def __init__(self, root, edo):
        """Constructor, makes a keyboard listener with a root and a scale of freqs"""
        self.root = root
        self.edo = edo
        self.key_scale = self.find_key_scale(edo)
        self.freq_scale = find_scale(root, edo)
        self.msg_queue = Queue()
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )

    def on_press(self, key):
        """on press handler"""
        print("press")
        self.msg_queue.put((key, "start"))

    def on_release(self, key):
        """on release handler"""
        print("release")
        self.msg_queue.put((key, "stop"))
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    def start_listening(self):
        """Listen to keyboard"""
        self.listener.start()

    def stop_listening(self):
        self.listener.stop()
        
    def find_key_scale(self, edo):
        """returns the keys that will be associated with a frequency"""
        if edo < 1:
            raise ValueError("This is not a valid edo")
        if edo <= 12:
            return SCALE_12_EDO[0:edo]
        if edo <= 24:
            return SCALE_24_EDO[0:edo]
        if edo <= 36:
            return SCALE_36_EDO[0:edo]
        if edo <= 48:
            return SCALE_48_EDO[0:edo]
        if edo <= 60:
            return SCALE_60_EDO[0:edo]
        raise ValueError("This is not a valid edo")

    def get_scale(self):
        """Return a list of tuples of keyboard key and frequency"""
        return zip(self.key_scale, self.freq_scale)

    def get_keypress(self):
        """Allows GUI to get frequency associated with keypress in a (kind of) async way
        returns the frequency, index of the keypress in its array, and key actually pressed"""
        try:
            key, msg = self.msg_queue.get(block=True)
        except Empty:
            print("empty")
            return -1
        try:
            index = self.key_scale.index(key)
            return (key, self.freq_scale[index], msg)
        except ValueError:
            raise ValueError("freq doesnt exist")
