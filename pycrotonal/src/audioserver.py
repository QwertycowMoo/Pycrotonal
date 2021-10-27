import pyo


class AudioServer():
    def __init__(self):
        self.server = pyo.Server(sr=48000).boot()

    def play(self):
        self.server.start()

    def stop(self):
        self.server.stop()
