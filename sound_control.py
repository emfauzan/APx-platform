from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import customtkinter

#from gui import Myapp

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

root = customtkinter.CTk()

def getCurrentMasterVolume():
    return round(volume.GetMasterVolumeLevelScalar() * 100)

def displayCurrentVolume():
    selection = str(getCurrentMasterVolume()) + "%"

def setMasterVolume(value):
    scalarVolume = value / 100
    volume.SetMasterVolumeLevelScalar(scalarVolume, None)
    displayCurrentVolume()

@staticmethod
def mute(boolMute):
   sessions = AudioUtilities.GetAllSessions()
   for session in sessions:
       volume = session._ctl.QueryInterface(ISimpleAudioVolume)
       print("volume.GetMute(): %s" % volume.GetMute())
       volume.SetMute(boolMute, None)
    