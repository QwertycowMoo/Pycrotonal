"""Main Control Loop for Pycrotonal"""
import wx
from src.gui import PycrotonalFrame
from pyo.lib.analysis import Scope
# First need to initialize sound objects and things to play
# Then initialize gui and add all children to screen or something
# Then call app.MainLoop()

if __name__ == "__main__":
    app = wx.App()
    frame = PycrotonalFrame(
        None,
        title="Pycrotonal",
        size=wx.Size(700, 700),
        style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,
    )
    app.MainLoop()
    # s = pyo.Server().boot()
    # s.start()
    # a = SineWave(440, .5)
    # b = pyo.Disto(a.get_synth(), drive=.9, slope=0.9, mul=0.5).out()
    # s.gui(locals())
