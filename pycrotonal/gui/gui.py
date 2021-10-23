import wx
from wx.lib.agw.knobctrl import KnobCtrl, KnobCtrlEvent
import pyo


class PycrotonalFrame(wx.Frame):
    """Main Frame for Pycrotonal"""

    def __init__(self, *args, **kw):
        """Constructor
        Creates a frame and adds all additional objects and frames into it"""
        super(PycrotonalFrame, self).__init__(*args, **kw)

        self.InitUI()
        self.Center()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        main_box = wx.BoxSizer(wx.VERTICAL)

        # TITLE
        title = wx.StaticText(panel, label="Pycrotonal", style=wx.ALIGN_CENTER)
        main_box.Add(title, 0, wx.ALIGN_CENTER_HORIZONTAL, 20)
        
        # CONTROLS
        params_box = wx.BoxSizer(wx.HORIZONTAL)
        # FM Params
        fm_param_box = wx.BoxSizer(wx.VERTICAL)
        lbl_fm_index = wx.StaticText(panel, label="FM Index: 0", style=wx.ALIGN_CENTER) 
        ctrl_fm_index = KnobCtrl(panel, size=(100, 100))
        ctrl_fm_index.SetTags(range(0, 100, 10)) # Index from 0 to 10, maybe make it bigger
        ctrl_fm_index.SetAngularRange(-45, 225)
        ctrl_fm_index.SetValue(0)
        fm_param_box.Add(lbl_fm_index, 0, wx.SHAPED| wx.TOP, 10)
        fm_param_box.Add(ctrl_fm_index, 0, wx.SHAPED| wx.TOP, 20)
        lbl_fm_freq = wx.StaticText(panel, label="FM Freq", style=wx.ALIGN_CENTER)
        ctrl_fm_freq = KnobCtrl(panel, size=(100, 100))
        ctrl_fm_freq.SetTags(range(0, 100, 10)) # Index from 0 to 10, maybe make it bigger
        ctrl_fm_freq.SetAngularRange(-45, 225)
        ctrl_fm_freq.SetValue(0)
        fm_param_box.Add(lbl_fm_freq, 0, wx.SHAPED| wx.TOP, 10)
        fm_param_box.Add(ctrl_fm_freq, 0, wx.SHAPED| wx.TOP, 20)
        params_box.Add(fm_param_box, 0, wx.TOP|wx.EXPAND, 10)
        
        params_box.AddStretchSpacer(1) 
        # Reverb and Distortion Params
        rev_dist_param_box = wx.BoxSizer(wx.VERTICAL)
        lbl_reverb = wx.StaticText(panel, label="Reverb", style=wx.ALIGN_CENTER)
        ctrl_reverb = KnobCtrl(panel, size=(100, 100))
        ctrl_reverb.SetTags(range(0, 100, 10)) # Index from 0 to 10, maybe make it bigger
        ctrl_reverb.SetAngularRange(-45, 225)
        ctrl_reverb.SetValue(0)
        rev_dist_param_box.Add(lbl_reverb, 0, wx.SHAPED| wx.TOP, 10)
        rev_dist_param_box.Add(ctrl_reverb, 0, wx.SHAPED| wx.TOP, 20)
        lbl_dist = wx.StaticText(panel, label="Distortion", style=wx.ALIGN_CENTER)
        ctrl_dist = KnobCtrl(panel, size=(100, 100))
        ctrl_dist.SetTags(range(0, 100, 10)) # Index from 0 to 10, maybe make it bigger
        ctrl_dist.SetAngularRange(-45, 225)
        ctrl_dist.SetValue(0)
        rev_dist_param_box.Add(lbl_dist, 0, wx.SHAPED| wx.TOP, 10)
        rev_dist_param_box.Add(ctrl_dist, 0, wx.SHAPED| wx.TOP, 20)
        params_box.Add(rev_dist_param_box, 0, wx.TOP|wx.EXPAND, 10)

        main_box.Add(params_box, 0, wx.ALL|wx.EXPAND, 10)
        panel.SetSizer(main_box)
        main_box.Layout()
        
# s = pyo.Server(sr=48000).boot()
# s.amp = 0.1
# s.start()

# sine = pyo.Sine(freq=400).out()
# sp = pyo.Spectrum(sine)

# # Initialization of app and frame must come after sound objects created
# app = wx.App()
# frame = wx.Frame(None, title="simple app")
# frame.Show()
# guispec = pyo.PyoGuiSpectrum(frame)
# guispec.setAnalyzer(sp)

# app.MainLoop()
