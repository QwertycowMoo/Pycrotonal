"""Controls the audio server to send Synth output to"""
import pyo


class AudioServer:
    """The main audio server that must be initialized before any sound objects created"""
    def __init__(self):
        """Constructor"""
        self.server = pyo.Server(sr=48000).boot()

    def play(self):
        """Start the server"""
        self.server.start()

    def stop(self):
        """Stop the server"""
        self.server.stop()
