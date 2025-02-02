from talon import app
from pathlib import Path
from .application import Application
import glob
import os

if app.platform == "mac":
    from plistlib import load

    mac_application_directories = [
        "/Applications",
        "/Applications/Utilities",
        "/System/Applications",
        "/System/Applications/Utilities",
        f"{Path.home()}/Applications",
        f"{Path.home()}/.nix-profile/Applications",
    ]

    def get_installed_mac_apps() -> list[Application]:
        application_list = []
        application_dict = {}
        for base in mac_application_directories:
            base = os.path.expanduser(base)
            if os.path.isdir(base):
                for name in os.listdir(base):
                    new_app = None
                    path = os.path.join(base, name)
                    display_name = name.rsplit(".", 1)[0]
                    
                    # most, but not all, apps store this here
                    plist_path = os.path.join(path, "Contents/Info.plist")
                    
                    if os.path.exists(plist_path):
                        with open(plist_path, 'rb') as fp:
                            #print(f"found at default: {plist_path}")
                            pl = load(fp)
                            bundle_identifier = pl["CFBundleIdentifier"]
                            executable_name = pl["CFBundleExecutable"] if "CFBundleExecutable" in pl else None
                            use_alternate_name =  display_name.lower() == "utilities" and base in "/System/Applications/Utilities"
                            if use_alternate_name and not executable_name or bundle_identifier in application_dict:
                                continue                         

                            new_app = Application(
                                path=path,
                                display_name=display_name if not use_alternate_name else executable_name,
                                unique_identifier=bundle_identifier, 
                                executable_name=executable_name, 
                                exclude=False,
                                spoken_forms=None,
                                application_group=None)
                                                        
                            application_list.append(new_app)
                            application_dict[bundle_identifier] = True

                    else:
                        files = glob.glob(os.path.join(path, '**/Info.plist'), recursive=True)  

                        for file in files:
                            with open(file, 'rb') as fp:
                                pl = load(fp)
                                if "CFBundleIdentifier" in pl:
                                    #print(f"found at: {file}")
                                    bundle_identifier = pl["CFBundleIdentifier"]
                                    executable_name = pl["CFBundleExecutable"] if "CFBundleExecutable" in pl else None
                                    use_alternate_name =  display_name.lower() == "utilities" and base in "/System/Applications/Utilities"
                                    
                                    if use_alternate_name and not executable_name or bundle_identifier in application_dict:
                                        continue
                                       
                                    new_app = Application(
                                        path=path,
                                        display_name=display_name if not use_alternate_name else executable_name,   
                                        unique_identifier=bundle_identifier, 
                                        executable_name=executable_name, 
                                        exclude=False,
                                        spoken_forms=None)
                                    
                                    application_list.append(new_app)
                                    application_dict[bundle_identifier] = True
        return application_list
else:
    def get_installed_mac_apps() -> list[Application]:
        return []