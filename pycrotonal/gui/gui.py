import wx
import pyo

s = pyo.Server(sr=48000).boot()
s.amp = 0.1
s.start()

sine = pyo.Sine(freq=400).out()
sp = pyo.Spectrum(sine)

# Initialization of app and frame must come after sound objects created
app = wx.App()
frame = wx.Frame(None, title="simple app")
frame.Show()
guispec = pyo.PyoGuiSpectrum(frame)
guispec.setAnalyzer(sp)

app.MainLoop()
