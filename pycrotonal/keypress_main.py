"""Main function to test key input"""
import argparse
from src.keyinput import Keyboard

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Change the EDO of the input of the scale"
    )
    parser.add_argument(
        "--roothz", type=int, help="the start of the scale in hz", default=440
    )
    parser.add_argument(
        "--edo", type=int, help="number of equal divisions of the octave", default=12
    )
    args = parser.parse_args()
    keyboard = Keyboard(args.roothz, args.edo)
    keyboard.start_listening()
    while True:
        print(keyboard.get_freq())
