from dataclasses import dataclass
from .exclusion import ExclusionType, RunningApplicationExclusion

# This is a list of known "modern" windows applications where we can't access the executable
@dataclass
class WindowsApplication:
    """Class for tracking properties of known "modern" windows applications"""
    display_name: str
    unique_identifier: str
    executable_name: str
    uses_application_frame_host: bool = True

windows_applications = [
    WindowsApplication(display_name="3D Viewer", 
                       unique_identifier="Microsoft.Microsoft3DViewer_8wekyb3d8bbwe!Microsoft.Microsoft3DViewer", 
                       executable_name="3DViewer.exe"),    
    WindowsApplication(display_name="Calculator", 
                       unique_identifier="Microsoft.WindowsCalculator_8wekyb3d8bbwe!App", 
                       executable_name="CalculatorApp.exe"),      
    WindowsApplication(display_name="Calendar", 
                       unique_identifier="microsoft.windowscommunicationsapps_8wekyb3d8bbwe!microsoft.windowslive.calendar", 
                       executable_name="HxCalendarAppImm.exe"),
    WindowsApplication(display_name="Camera", 
                       unique_identifier="Microsoft.WindowsCamera_8wekyb3d8bbwe!App", 
                       executable_name="WindowsCamera.exe"), 
    WindowsApplication(display_name="Clock", 
                       unique_identifier="Microsoft.WindowsAlarms_8wekyb3d8bbwe!App", 
                       executable_name="Time.exe"),  
    # cortana's standalone app is deprecated
    WindowsApplication(display_name="Cortana", 
                       unique_identifier="Microsoft.549981C3F5F10_8wekyb3d8bbwe!App", 
                       executable_name=None),  
    WindowsApplication(display_name="Ditto", 
                       unique_identifier="60145ScottBrogden.ditto-cp_n6b029mg40na2!Ditto", 
                       executable_name="DAXUIDolbyAtmos.exe"),                   
    WindowsApplication(display_name="Dolby Atmos", 
                       unique_identifier="DolbyLaboratories.DolbyAtmos_rz1tebttyb220!App", 
                       executable_name="DAXUIDolbyAtmos.exe"),
    WindowsApplication(display_name="Feedback Hub", 
                       unique_identifier="Microsoft.WindowsFeedbackHub_8wekyb3d8bbwe!App", 
                       executable_name="PilotshubApp.exe"), 
    WindowsApplication(display_name="Game Bar", 
                       unique_identifier="Microsoft.XboxGamingOverlay_8wekyb3d8bbwe!App", 
                       executable_name="GameBar.exe"), 
    WindowsApplication(display_name="Get Help", 
                       unique_identifier="Microsoft.GetHelp_8wekyb3d8bbwe!App", 
                       executable_name="GetHelp.exe"), 
    WindowsApplication(display_name="iTunes", 
                       unique_identifier="AppleInc.iTunes_nzyj5cx40ttqa!iTunes", 
                       executable_name="iTunes.exe",
                       uses_application_frame_host=False), 
    WindowsApplication(display_name="Mail", 
                       unique_identifier="microsoft.windowscommunicationsapps_8wekyb3d8bbwe!microsoft.windowslive.mail", 
                       executable_name="olk.exe",
                       uses_application_frame_host=False), 
    WindowsApplication(display_name="Maps", 
                       unique_identifier="Microsoft.WindowsMaps_8wekyb3d8bbwe!App", 
                       executable_name=None), 
    WindowsApplication(display_name="Media Player", 
                       unique_identifier="Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic", 
                       executable_name="Microsoft.Media.Player.exe"), 
    WindowsApplication(display_name="Microsoft Accessory Center", 
                       unique_identifier="Microsoft.MicrosoftAccessoryCenter_8wekyb3d8bbwe!App", 
                       executable_name="AccessoryCenter.ContainerApp.Main.exe"), 
    WindowsApplication(display_name="Microsoft Accessory Center", 
                       unique_identifier="Microsoft.MicrosoftAccessoryCenter_8wekyb3d8bbwe!App", 
                       executable_name=""), 
    WindowsApplication(display_name="Microsoft Defender", 
                       unique_identifier="Microsoft.6365217CE6EB4_8wekyb3d8bbwe!App", 
                       executable_name="MicrosoftSecurityApp.exe"), 
    WindowsApplication(display_name="Microsoft Store", 
                       unique_identifier="Microsoft.WindowsStore_8wekyb3d8bbwe!App", 
                       executable_name="WinStore.App.exe"),  
    WindowsApplication(display_name="Mixed Reality Portal", 
                       unique_identifier="Microsoft.MixedReality.Portal_8wekyb3d8bbwe!App", 
                       executable_name="MixedRealityPortal.exe"), 
    WindowsApplication(display_name="Movies & TV", 
                       unique_identifier="Microsoft.ZuneVideo_8wekyb3d8bbwe!Microsoft.ZuneVideo", 
                       executable_name="Video.UI.exe"), 
    WindowsApplication(display_name="News", 
                       unique_identifier="Microsoft.BingNews_8wekyb3d8bbwe!AppexNews", 
                       executable_name="Microsoft.Msn.News.exe"), 
    WindowsApplication(display_name="Paint 3D", 
                       unique_identifier="Microsoft.MSPaint_8wekyb3d8bbwe!Microsoft.MSPaint", 
                       executable_name="PaintStudio.View.exe"), 
    WindowsApplication(display_name="Phone Link", 
                       unique_identifier="Microsoft.YourPhone_8wekyb3d8bbwe!App", 
                       executable_name="PhoneExperienceHost.exe"), 
    WindowsApplication(display_name="Photos", 
                       unique_identifier="Microsoft.Windows.Photos_8wekyb3d8bbwe!App", 
                       executable_name="Photos.exe"), 
    WindowsApplication(display_name="Skype", 
                       unique_identifier="Microsoft.SkypeApp_kzf8qxf38zg5c!App", 
                       executable_name="Skype.exe"), 
    WindowsApplication(display_name="Snip & Sketch", 
                       unique_identifier="Microsoft.ScreenSketch_8wekyb3d8bbwe!App", 
                       executable_name="ScreenSketch.exe"), 
    WindowsApplication(display_name="Solitaire & Casual Games", 
                       unique_identifier="Microsoft.MicrosoftSolitaireCollection_8wekyb3d8bbwe!App", 
                       executable_name="Solitaire.exe"), 
    WindowsApplication(display_name="Spotify", 
                       unique_identifier="SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify", 
                       executable_name="Spotfy.exe"), 
    WindowsApplication(display_name="Sticky Notes", 
                       unique_identifier="Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe!App", 
                       executable_name=None), 
    WindowsApplication(display_name="", 
                       unique_identifier="", 
                       executable_name=""), 
    WindowsApplication(display_name="Terminal", 
                       unique_identifier="Microsoft.WindowsTerminal_8wekyb3d8bbwe!App", 
                       executable_name="WindowsTerminal.exe"), 
    WindowsApplication(display_name="Tips", 
                       unique_identifier="Microsoft.Getstarted_8wekyb3d8bbwe!App", 
                       executable_name="WhatsNew.Store.exe"), 
    WindowsApplication(display_name="Ubuntu on Windows", 
                       unique_identifier="CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc!ubuntuonwindows", 
                       executable_name="ubuntu.exe"), 
    WindowsApplication(display_name="Voice Recorder", 
                       unique_identifier="Microsoft.WindowsSoundRecorder_8wekyb3d8bbwe!App", 
                       executable_name="SoundRec.exe"), 
    WindowsApplication(display_name="Weather", 
                       unique_identifier="Microsoft.BingWeather_8wekyb3d8bbwe!App", 
                       executable_name="Microsoft.Msn.Weather.exe"), 
    WindowsApplication(display_name="Windows Backup", 
                       unique_identifier="MicrosoftWindows.Client.CBS_cw5n1h2txyewy!WindowsBackup", 
                       executable_name="WindowsBackupClient.exe"), 
    WindowsApplication(display_name="Windows Security", 
                       unique_identifier="Microsoft.Windows.SecHealthUI_cw5n1h2txyewy!SecHealthUI", 
                       executable_name="SecHealthUI.exe"), 
    WindowsApplication(display_name="Xbox Console Companion", 
                       unique_identifier="Microsoft.XboxApp_8wekyb3d8bbwe!Microsoft.XboxApp", 
                       executable_name="XboxApp.exe"), 

]

windows_application_dict = {}
for application in windows_applications:
    unique_identifier = application.unique_identifier

    if application.executable_name:
        executable_name = application.executable_name.lower()
        windows_application_dict[executable_name] = application

    windows_application_dict[unique_identifier.lower()] = application

    
def app_uses_frame_host(key):
    key = key.lower()
    if key in windows_application_dict:
        return windows_application_dict[key].uses_application_frame_host
    return False
        
def is_known_windows_application(uuid):
    known_app = uuid.lower() in windows_application_dict
    if known_app:
        return True, windows_application_dict[uuid.lower()].uses_application_frame_host
    else:
        return False, False
