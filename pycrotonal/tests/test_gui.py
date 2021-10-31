import unittest
import wx
from wx.lib.agw.knobctrl import KnobCtrlEvent, EVT_KC_ANGLE_CHANGED
from src.gui import PycrotonalFrame


class TestGUI(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        """Creates an app for the entire test suit to use"""
        self.app = wx.App()
        self.frame = PycrotonalFrame(
            None,
            title="Pycrotonal",
            size=wx.Size(700, 500),
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,
        )

    def tearDown(self):
        """Destroys the frame, but does not shut down audio server"""
        self.frame.Destroy()

    def test_a_init(self):
        """Tests initialization. Has 'a' in it so that it runs first before any 
        modification tests."""

        self.assertEqual(self.frame.reverb, 0, "reverb set to 0")
        self.assertEqual(self.frame.distortion, 0, "distortion set to 0")
        self.assertEqual(self.frame.fm_freq, 100, "fm freq set to 100")
        self.assertEqual(self.frame.fm_index, 1, "fm index is 1")
        self.assertEqual(self.frame.is_playing, False,
                         "Should not play at the beginning")

    def test_change_freq_button(self):
        """Change the fm frequency and click the button"""
        freq_button = self.frame.btn_fm_freq
        self.frame.txt_fm_freq.SetValue("500")
        evt = wx.CommandEvent(wx.EVT_BUTTON.typeId)
        evt.SetEventObject(freq_button)
        evt.SetId(freq_button.GetId())
        freq_button.GetEventHandler().ProcessEvent(evt)
        self.assertEqual(self.frame.fm_freq, 500, "fm freq changed to 500")

    def test_change_freq_knob(self):
        """Change the fm freq using the knob"""
        freq_knob = self.frame.ctrl_fm_freq
        evt = KnobCtrlEvent(EVT_KC_ANGLE_CHANGED.typeId)
        evt.SetEventObject(freq_knob)
        evt.SetId(freq_knob.GetId())
        evt.SetValue(50)
        freq_knob.GetEventHandler().ProcessEvent(evt)
        self.assertEqual(self.frame.fm_freq, 50, "fm freq changed to 50")
        self.assertEqual(self.frame.txt_fm_freq.GetValue(), "50", "textbox also changed")
    
    def test_change_fm_index_knob(self):
        index_knob = self.frame.ctrl_fm_index
        evt = KnobCtrlEvent(EVT_KC_ANGLE_CHANGED.typeId)
        evt.SetEventObject(index_knob)
        evt.SetId(index_knob.GetId())
        evt.SetValue(50)
        index_knob.GetEventHandler().ProcessEvent(evt)
        self.assertEqual(self.frame.fm_index, 50, "fm freq changed to 50")
        self.assertEqual(self.frame.lbl_fm_index.GetLabelText(), "FM Index: 50", "textbox also changed")

    def test_change_reverb_knob(self):
        reverb_knob = self.frame.ctrl_reverb
        evt = KnobCtrlEvent(EVT_KC_ANGLE_CHANGED.typeId)
        evt.SetEventObject(reverb_knob)
        evt.SetId(reverb_knob.GetId())
        evt.SetValue(50)
        reverb_knob.GetEventHandler().ProcessEvent(evt)
        self.assertEqual(self.frame.reverb, .5, "reverb changed to .5 out of 1")
        self.assertEqual(self.frame.lbl_reverb.GetLabelText(), "Reverb: 50", "textbox also changed")
    
    def test_change_distortion_knob(self):
        dist_knob = self.frame.ctrl_dist
        evt = KnobCtrlEvent(EVT_KC_ANGLE_CHANGED.typeId)
        evt.SetEventObject(dist_knob)
        evt.SetId(dist_knob.GetId())
        evt.SetValue(50)
        dist_knob.GetEventHandler().ProcessEvent(evt)
        self.assertEqual(self.frame.distortion, .5, "reverb changed to .5 out of 1")
        self.assertEqual(self.frame.lbl_dist.GetLabelText(), "Distortion: 50", "textbox also changed")

if __name__ == "__main__":
    unittest.main()
