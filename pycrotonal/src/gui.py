"""GUI class for wx Frame"""
import wx
from wx.lib.agw.knobctrl import KnobCtrl, EVT_KC_ANGLE_CHANGED

from .waveforms.sinewave import SineWave
from .waveforms.trianglewave import TriangleWave
from .waveforms.squarewave import SquareWave
from .waveforms.sawtoothwave import SawtoothWave

from .audioserver import AudioServer

# TODO: Actually have the audio play based on a button
# TODO: Find out where to start the audio server
# TODO: Stop audio server on frame destruct
WAVEFORMS = ["Sine", "Square", "Triangle", "Saw"]

class PycrotonalFrame(wx.Frame):
    """Main Frame for Pycrotonal"""
    def __init__(self, *args, **kw):
        """Constructor
        Creates a frame and adds all additional objects and frames into it"""
        super().__init__(*args, **kw)
        self.server = AudioServer()
        self.synth = SineWave(440, 0.5)
        self.play_synth()
        self.server.play()
        self.init_ui()
        self.Center()
        self.Show()
        
    
    def __del__(self):
        self.server.stop()

    def init_ui(self):
        """Initialize the static user interface"""
        panel = wx.Panel(self)
        main_box = wx.BoxSizer(wx.VERTICAL)

        # TITLE
        title = wx.StaticText(panel, label="Pycrotonal", style=wx.ALIGN_CENTER)
        main_box.Add(title, 0, wx.ALIGN_CENTER_HORIZONTAL, 20)
        title_font = wx.Font(
            20, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
        )
        title.SetFont(title_font)
        # WAVEFORM SELECTION
        wave_select = wx.Choice(panel, choices=WAVEFORMS)
        main_box.Add(wave_select, 0, wx.ALIGN_CENTER_HORIZONTAL, 10)
        # CONTROLS
        params_box = self.init_params_sizer(panel)

        main_box.Add(params_box, 0, wx.ALL | wx.EXPAND, 10)
        panel.SetSizer(main_box)
        main_box.Layout()

    def init_params_sizer(self, panel):

        params_box = wx.BoxSizer(wx.HORIZONTAL)
        # FM Params
        fm_param_box = wx.BoxSizer(wx.VERTICAL)
        self.lbl_fm_index = wx.StaticText(panel, label="FM Index: 0", style=wx.ALIGN_CENTER)
        ctrl_fm_index = KnobCtrl(panel, size=wx.Size(100, 100))
        ctrl_fm_index.SetTags(
            range(0, 100, 10)
        )  # Index from 0 to 10, maybe make it bigger
        
        ctrl_fm_index.SetAngularRange(-45, 225)
        ctrl_fm_index.SetValue(0)
        self.Bind(EVT_KC_ANGLE_CHANGED, self.handle_fm_index_knob, ctrl_fm_index)

        fm_param_box.Add(self.lbl_fm_index, 0, wx.SHAPED | wx.TOP, 10)
        fm_param_box.Add(ctrl_fm_index, 0, wx.SHAPED | wx.TOP, 20)
        lbl_fm_freq = wx.StaticText(panel, label="FM Freq", style=wx.ALIGN_CENTER)
        ctrl_fm_freq = KnobCtrl(panel, size=(100, 100))
        ctrl_fm_freq.SetTags(
            range(0, 100, 10)
        )  # Index from 0 to 10, maybe make it bigger
        ctrl_fm_freq.SetAngularRange(-45, 225)
        ctrl_fm_freq.SetValue(0)
        fm_param_box.Add(lbl_fm_freq, 0, wx.SHAPED | wx.TOP, 10)
        fm_param_box.Add(ctrl_fm_freq, 0, wx.SHAPED | wx.TOP, 20)
        params_box.Add(fm_param_box, 0, wx.TOP | wx.EXPAND, 10)

        params_box.AddStretchSpacer(1)
        # Reverb and Distortion Params
        rev_dist_param_box = wx.BoxSizer(wx.VERTICAL)
        lbl_reverb = wx.StaticText(panel, label="Reverb", style=wx.ALIGN_CENTER)
        ctrl_reverb = KnobCtrl(panel, size=(100, 100))
        ctrl_reverb.SetTags(
            range(0, 100, 10)
        )  # Index from 0 to 10, maybe make it bigger
        ctrl_reverb.SetAngularRange(-45, 225)
        ctrl_reverb.SetValue(0)
        rev_dist_param_box.Add(lbl_reverb, 0, wx.SHAPED | wx.TOP, 10)
        rev_dist_param_box.Add(ctrl_reverb, 0, wx.SHAPED | wx.TOP, 20)
        lbl_dist = wx.StaticText(panel, label="Distortion", style=wx.ALIGN_CENTER)
        ctrl_dist = KnobCtrl(panel, size=(100, 100))
        ctrl_dist.SetTags(range(0, 100, 10))  # Index from 0 to 10, maybe make it bigger
        ctrl_dist.SetAngularRange(-45, 225)
        ctrl_dist.SetValue(0)
        rev_dist_param_box.Add(lbl_dist, 0, wx.SHAPED | wx.TOP, 10)
        rev_dist_param_box.Add(ctrl_dist, 0, wx.SHAPED | wx.TOP, 20)
        params_box.Add(rev_dist_param_box, 0, wx.TOP | wx.EXPAND, 10)
        return params_box

    def handle_fm_index_knob(self, event):
        """Handles the fm_amplitude knob"""
        value = event.GetValue()
        self.lbl_fm_index.SetLabel("FM Index: " + str(value))
        self.lbl_fm_index.Refresh()
        self.synth.freq = value
        print(self.synth.freq)

    def play_synth(self):
        self.synth.get_synth().out()
