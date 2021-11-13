"""GUI class for wx Frame"""
import sys
import threading
from pynput import keyboard
from pynput.keyboard import Key
from pyo.lib.controls import Adsr
from pyo.lib._core import Mix
from pyo.lib.generators import FM, Sine
from pyo.lib.effects import Disto, Freeverb
import wx
from wx.core import EVT_SCROLL_CHANGED, EVT_SLIDER, SL_INVERSE, SL_VERTICAL
from wx.lib.agw.knobctrl import KnobCtrl, EVT_KC_ANGLE_CHANGED
from wx import EVT_CHOICE, EVT_BUTTON, TE_PROCESS_ENTER
from musx import rescale
from .waveforms.sinewave import SineWave
from .waveforms.trianglewave import TriangleWave
from .waveforms.squarewave import SquareWave
from .waveforms.sawtoothwave import SawtoothWave

from .audioserver import AudioServer
from .keyinput import Keyboard

# TODO: Apply FM modulation with a button, FM currently not working right now
WAVEFORMS = ["Sine", "Square", "Triangle", "Saw"]
SINE_INDEX = 0
SQUARE_INDEX = 1
TRIANGLE_INDEX = 2
SAW_INDEX = 3
FM_MAX_FREQ = 9000


class PycrotonalFrame(wx.Frame):
    """Main Frame for Pycrotonal"""

    def __init__(self, *args, **kw):
        """Constructor
        Creates a frame and adds all additional objects and frames into it
        Also creates the base synth, FM synthesizer, Reverb, and Distortion.
        While I would like for the reverb and distortion to be within the synth class,
        The knobs update the values and the AudioServer must be started before
        any PyoObjects can be made, so they must be instantiated after.

        *args and **kw are there to extend the wx.Frame object, currently using
        title, size, and style. The c++ implementation uses flags, which is disgusting but workable.
        """
        super().__init__(*args, **kw)
        self.server = AudioServer()
        # How do we have polyphony
        # If have all synths in array, then call adsr play() on them, they are always running
        # Don't have to dynamically create synths, only have to call stop() on the synth itself to save CPU
        self.edo = 60
        self.keyboard = Keyboard(440, self.edo)
        self.keyboard.start_listening()

        # mix can mix a list of pyoObjects to save reverb/dist computation cost

        # Distortion has set params, can only control drive amount and not clip function
        self.distortion = 0
        # Reverb has set params, can only control dry/wet for now
        self.reverb = 0
        self.fm_freq = 100
        self.apply_fm = False

        # Have array of independent adsr so that each note has its own envelope
        self.adsr_arr = [
            Adsr(attack=0.01, decay=0.01, release=0.01, mul=0.2)
            for _ in range(self.edo)
        ]
        # Create all synths and so when the key is pressed, it starts the synth associated with the key
        self.synths = {
            key: SineWave(freq, self.adsr_arr[i])
            for i, (key, freq) in enumerate(self.keyboard.get_scale())
        }
        # TODO: apply mix onto all synths so it can be reverb and distortioned
        # TODO: Allow change of waveforms
        raw_synths = [synth.get_synth() for synth in self.synths.values()]
        self.mix = Mix(raw_synths, 2)
        self.fm_ratio = self.fm_freq / 440
        self.fm_index = 1
        if self.apply_fm:
            # Putting fm synthesis on hold for right now
            self.fm_synth = FM(carrier=Sine())
            # So there's sound if you really listen hard but not usable
            self.dist_effect = Disto(self.fm_synth, drive=self.distortion, slope=0.8)
            self.final_output = Freeverb(
                self.fm_synth, size=0.8, damp=0.7, bal=self.reverb
            )
        else:
            self.dist_effect = Disto(self.mix, drive=self.distortion, slope=0.8)
            self.final_output = Freeverb(self.mix, size=0.8, damp=0.7, bal=self.reverb)

        self.is_playing = False
        self.server.play()
        self.final_output.out()
        self.init_ui()

        self.Bind(wx.EVT_CLOSE, self.on_exit)
        self.Center()
        self.Show()

        # Start a new thread to get keypresses
        # Has daemon=True so it also shuts down when main loop stops
        thrd_keypress = threading.Thread(target=self.get_keypress, daemon=True)
        thrd_keypress.start()

    def on_exit(self, event):
        """Stops the audio server on exit"""
        self.server.stop()
        sys.exit(0)

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
        wave_select.SetSelection(0)
        main_box.Add(wave_select, 0, wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(EVT_CHOICE, self.handle_waveform_change, wave_select)
        # CONTROLS
        params_box = self.init_params_sizer(panel)

        main_box.Add(params_box, 0, wx.ALL | wx.EXPAND, 10)

        self.lbl_frequency = wx.StaticText(
            panel, label="Frequency:", style=wx.ALIGN_CENTER
        )
        main_box.Add(self.lbl_frequency, 0, wx.ALIGN_CENTER_HORIZONTAL, 20)
        frequency_font = wx.Font(
            15, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
        )
        title.SetFont(frequency_font)

        # Waveform oscilloscope
        # self.osc_scope = PyoGuiScope(panel)
        # main_box.Add(self.osc_scope, 0, wx.ALIGN_CENTER_HORIZONTAL, 2)
        panel.SetSizer(main_box)
        main_box.Layout()

    def init_params_sizer(self, panel):
        """Initialize the parameters box with FM, reverb, and distortion"""
        params_box = wx.BoxSizer(wx.HORIZONTAL)
        # FM Params
        # FM Index
        fm_param_box = wx.BoxSizer(wx.VERTICAL)
        self.lbl_fm_index = wx.StaticText(
            panel, label="FM Index: 0", style=wx.ALIGN_CENTER
        )
        self.ctrl_fm_index = KnobCtrl(panel, size=wx.Size(100, 100))
        self.ctrl_fm_index.SetTags(
            range(0, 100, 10)
        )  # Index from 0 to 100, maybe make it bigger
        self.ctrl_fm_index.SetAngularRange(-45, 225)
        self.ctrl_fm_index.SetValue(0)
        # Add listener
        self.Bind(EVT_KC_ANGLE_CHANGED, self.handle_fm_index_knob, self.ctrl_fm_index)

        # FM Freq
        fm_param_box.Add(self.lbl_fm_index, 0, wx.SHAPED | wx.TOP, 10)
        fm_param_box.Add(self.ctrl_fm_index, 0, wx.SHAPED | wx.TOP, 20)
        self.lbl_fm_freq = wx.StaticText(
            panel, label="FM Freq:", style=TE_PROCESS_ENTER
        )
        self.txt_fm_freq = wx.TextCtrl(panel, value="100")
        self.btn_fm_freq = wx.Button(panel, label="Set FM Freq")
        # Button listener
        self.Bind(EVT_BUTTON, self.handle_fm_freq_input, self.btn_fm_freq)
        self.ctrl_fm_freq = KnobCtrl(panel, size=(100, 100))
        self.ctrl_fm_freq.SetTags(
            range(0, FM_MAX_FREQ + 1, 1000)
        )  # Index from 0 to 100, maybe make it bigger
        self.ctrl_fm_freq.SetAngularRange(-45, 225)
        self.ctrl_fm_freq.SetValue(100)
        # Knob input listener
        self.Bind(EVT_KC_ANGLE_CHANGED, self.handle_fm_freq_knob, self.ctrl_fm_freq)
        fm_param_box.Add(self.lbl_fm_freq, 0, wx.SHAPED | wx.TOP, 10)
        fm_param_box.Add(self.txt_fm_freq, 0, wx.SHAPED | wx.TOP, 5)
        fm_param_box.Add(self.btn_fm_freq, 0, wx.SHAPED | wx.TOP, 2)
        fm_param_box.Add(self.ctrl_fm_freq, 0, wx.SHAPED | wx.TOP, 20)
        params_box.Add(fm_param_box, 0, wx.TOP | wx.EXPAND, 10)

        params_box.AddStretchSpacer(1)

        # ADSR
        adsr_param_box = wx.BoxSizer(wx.HORIZONTAL)
        # Sliders will look linear but handlers will map onto exponential values
        lbl_attack = wx.StaticText(
            panel, label="Attack", style=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        adsr_param_box.Add(lbl_attack, 0, wx.SHAPED | wx.RIGHT, 3)
        self.attack_slider = wx.Slider(panel, value=0, style=SL_VERTICAL | SL_INVERSE)
        adsr_param_box.Add(self.attack_slider, 0, wx.SHAPED | wx.RIGHT, 3)
        self.Bind(EVT_SLIDER, self.handle_attack_change, self.attack_slider)

        lbl_decay = wx.StaticText(
            panel, label="Decay", style=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        adsr_param_box.Add(lbl_decay, 0, wx.SHAPED | wx.RIGHT, 3)
        self.decay_slider = wx.Slider(panel, value=0, style=SL_VERTICAL | SL_INVERSE)
        adsr_param_box.Add(self.decay_slider, 0, wx.SHAPED | wx.RIGHT, 3)
        self.Bind(EVT_SLIDER, self.handle_decay_change, self.decay_slider)

        lbl_sustain = wx.StaticText(
            panel, label="Sustain", style=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        adsr_param_box.Add(lbl_sustain, 0, wx.SHAPED | wx.RIGHT, 3)
        self.sustain_slider = wx.Slider(panel, value=0, style=SL_VERTICAL | SL_INVERSE)
        adsr_param_box.Add(self.sustain_slider, 0, wx.SHAPED | wx.RIGHT, 3)
        self.Bind(EVT_SLIDER, self.handle_sustain_change, self.sustain_slider)

        lbl_release = wx.StaticText(
            panel, label="Release", style=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        adsr_param_box.Add(lbl_release, 0, wx.SHAPED | wx.RIGHT, 3)
        self.release_slider = wx.Slider(panel, value=0, style=SL_VERTICAL | SL_INVERSE)
        adsr_param_box.Add(self.release_slider, 0, wx.SHAPED | wx.RIGHT, 3)
        self.Bind(EVT_SLIDER, self.handle_release_change, self.release_slider)

        params_box.Add(adsr_param_box, 0, wx.TOP | wx.EXPAND, 10)
        params_box.AddStretchSpacer(1)

        # Reverb and Distortion Params
        # Reverb
        rev_dist_param_box = wx.BoxSizer(wx.VERTICAL)
        self.lbl_reverb = wx.StaticText(panel, label="Reverb: 0", style=wx.ALIGN_CENTER)
        self.ctrl_reverb = KnobCtrl(panel, size=(100, 100))
        self.ctrl_reverb.SetTags(range(0, 100, 10))
        self.ctrl_reverb.SetAngularRange(-45, 225)
        self.ctrl_reverb.SetValue(0)
        # Add listener
        self.Bind(EVT_KC_ANGLE_CHANGED, self.handle_reverb_knob, self.ctrl_reverb)

        # Distortion
        rev_dist_param_box.Add(self.lbl_reverb, 0, wx.SHAPED | wx.TOP, 10)
        rev_dist_param_box.Add(self.ctrl_reverb, 0, wx.SHAPED | wx.TOP, 20)
        self.lbl_dist = wx.StaticText(
            panel, label="Distortion: 0", style=wx.ALIGN_CENTER
        )
        self.ctrl_dist = KnobCtrl(panel, size=(100, 100))
        self.ctrl_dist.SetTags(range(0, 100, 10))
        self.ctrl_dist.SetAngularRange(-45, 225)
        self.ctrl_dist.SetValue(0)
        # Add listener
        self.Bind(EVT_KC_ANGLE_CHANGED, self.handle_distortion_knob, self.ctrl_dist)
        rev_dist_param_box.Add(self.lbl_dist, 0, wx.SHAPED | wx.TOP, 10)
        rev_dist_param_box.Add(self.ctrl_dist, 0, wx.SHAPED | wx.TOP, 20)

        params_box.Add(rev_dist_param_box, 0, wx.TOP | wx.EXPAND, 10)
        return params_box

    def handle_fm_index_knob(self, event):
        """Handles the fm_index knob"""
        value = event.GetValue()
        self.fm_index = value
        self.lbl_fm_index.SetLabel("FM Index: " + str(value))
        self.lbl_fm_index.Refresh()

    def handle_fm_freq_knob(self, event):
        """Handles the fm_freq knob"""
        value = event.GetValue()
        self.fm_freq = value
        self.txt_fm_freq.SetValue(str(value))
        self.txt_fm_freq.Refresh()

    def handle_fm_freq_input(self, event):
        """Handles the fm_freq text input"""

        try:
            value = int(self.txt_fm_freq.GetValue())
            if value > 0 & value < FM_MAX_FREQ:
                self.fm_freq = value
                self.ctrl_fm_freq.SetValue(int(value))
                self.ctrl_fm_freq.Refresh()
        except ValueError:
            print("This is not an integer")

    def handle_reverb_knob(self, event):
        """Handles the reverb knob"""
        value = event.GetValue()
        self.reverb = value / 100
        # Update the reverb PyoObject
        self.final_output.setBal(self.reverb)
        self.lbl_reverb.SetLabel("Reverb: " + str(value))
        self.lbl_reverb.Refresh()

    def handle_distortion_knob(self, event):
        """Handles the distortion knob"""
        value = event.GetValue()
        self.distortion = value / 100
        # Update the distortion effect and reverb effect PyoObjects
        self.dist_effect.setDrive(self.distortion)
        self.final_output.setInput(self.dist_effect)
        self.lbl_dist.SetLabel("Distortion: " + str(value))
        self.lbl_dist.Refresh()

    def handle_toggle_synth(self, event):
        """Toggle whether the synth is playing, also reconstructs microtonal synth array"""
        if self.is_playing:
            self.stop_synth()
            self.is_playing = False
        else:
            self.start_synth()
            self.is_playing = True

    def handle_waveform_change(self, event):
        """Handles the waveform selection change and creates new synth objects"""
        if event.GetSelection() == SINE_INDEX:
            self.synths = {
                key: SineWave(freq, self.adsr_arr[i])
                for i, (key, freq) in enumerate(self.keyboard.get_scale())
            }
        elif event.GetSelection() == SQUARE_INDEX:
            self.synths = {
                key: SquareWave(freq, self.adsr_arr[i])
                for i, (key, freq) in enumerate(self.keyboard.get_scale())
            }
        elif event.GetSelection() == TRIANGLE_INDEX:
            self.synths = {
                key: TriangleWave(freq, self.adsr_arr[i])
                for i, (key, freq) in enumerate(self.keyboard.get_scale())
            }
        elif event.GetSelection() == SAW_INDEX:
            self.synths = {
                key: SawtoothWave(freq, self.adsr_arr[i])
                for i, (key, freq) in enumerate(self.keyboard.get_scale())
            }

        # Mix all together
        raw_synths = [synth.get_synth() for synth in self.synths.values()]
        self.mix = Mix(raw_synths, 2)
        self.dist_effect = Disto(self.mix, drive=self.distortion, slope=0.8)
        self.final_output = Freeverb(self.mix, size=0.8, damp=0.7, bal=self.reverb)
        # Have out send so effects are applied again
        self.final_output.out()

    def handle_attack_change(self, event):

        attack = self.attack_slider.GetValue()
        attack = rescale(attack, 0, 100, 0, 10, mode="exp")
        for adsr in self.adsr_arr:
            adsr.setAttack(attack)

    def handle_decay_change(self, event):
        decay = self.decay_slider.GetValue()
        decay = rescale(decay, 0, 100, 0, 10, mode="exp")
        for adsr in self.adsr_arr:
            adsr.setDecay(decay)

    def handle_sustain_change(self, event):
        sustain = self.sustain_slider.GetValue()
        sustain = rescale(sustain, 0, 100, 0, 10, mode="exp")
        for adsr in self.adsr_arr:
            adsr.setSustain(sustain)

    def handle_release_change(self, event):
        release = self.release_slider.GetValue()
        release = rescale(release, 0, 100, 0, 10, mode="exp")
        for adsr in self.adsr_arr:
            adsr.setRelease(release)

    def get_keypress(self):
        while True:
            # Also need wxpython input for edo
            try:
                key, freq, msg = self.keyboard.get_keypress()
                if msg == "start":
                    self.lbl_frequency.SetLabel("Key: " + str(key) + "Frequency: " + str(freq))
                    self.synths[key].play()
                elif msg == "stop":
                    self.synths[key].stop()
            except ValueError as e:
                print(e)
