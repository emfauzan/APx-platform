from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def getCurrentMasterVolume():
    return round(volume.GetMasterVolumeLevelScalar() * 100)

def displayCurrentVolume():
    selection = str(getCurrentMasterVolume()) + "%"
    return selection

def setMasterVolume(value):
    scalarVolume = value / 100
    volume.SetMasterVolumeLevelScalar(scalarVolume, None)
    displayCurrentVolume()

def mute(boolMute):
   sessions = AudioUtilities.GetAllSessions()
   for session in sessions:
       volume = session._ctl.QueryInterface(ISimpleAudioVolume)
       print("volume.GetMute(): %s" % volume.GetMute())
       volume.SetMute(boolMute, None)
    