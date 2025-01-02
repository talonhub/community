# import os

# import win32com.client
# import os

# import winreg

# def get_desktop_path():

#     with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as key:

#         desktop = winreg.QueryValueEx(key, "Desktop")[0]

#     return os.path.expandvars(desktop)



# desktop_path = get_desktop_path()

# print(desktop_path)


# def parse_start_menu_shortcuts():

#     # Paths to Start Menu folders

#     start_menu_folders = [
#         desktop_path, 
#         os.path.expandvars("%AppData%/Microsoft/Windows/Start Menu/Programs"),
#         os.path.expandvars("%ProgramData%/Microsoft/Windows/Start Menu/Programs"),
#         os.path.expandvars("%AppData%/Microsoft/Internet Explorer/Quick Launch/User Pinned/TaskBar"),

#     ]

    

#     shell = win32com.client.Dispatch("WScript.Shell")

    

#     # Iterate over all Start Menu folders

#     for folder in start_menu_folders:

#         print(f"Scanning folder: {folder}")

        

#         for root, _, files in os.walk(folder):

#             for file in files:

#                 if file.endswith(".lnk"):  # Look for shortcut files

#                     shortcut_path = os.path.join(root, file)

                    

#                     try:

#                         # Load the shortcut

#                         shortcut = shell.CreateShortcut(shortcut_path)

                        

#                         # Extract shortcut properties
#                         if True:
                            
#                             print(f"Shortcut Name: {file}")

#                             print(f"Full Path: {shortcut_path}")
                            
#                             print(f"Target Path: {shortcut.TargetPath}")

#                             print(f"Arguments: {shortcut.Arguments}")

#                             print(f"Working Directory: {shortcut.WorkingDirectory}")

#                             print(f"Icon Location: {shortcut.IconLocation}")
                            

#                             print(f"Description: {shortcut.Description}")

#                             print("-------------------------------------------------")

                    

#                     except Exception as e:

#                         print(f"Error parsing {shortcut_path}: {e}")

#                         continue




# parse_start_menu_shortcuts()
# # import win32com.client

# # def stupid_test():
# #     shell = win32com.client.Dispatch("Shell.Application")
# #     folder = shell.NameSpace('shell:::{4234d49b-0245-4df3-b780-3893943456e1}')
# #     items = folder.Items()
    
# #     for item in items:

# #         print(f"name={item.Name} path={item.Path} type={item.Type} link={item.IsLink} IsFolder={item.IsFolder}")
# #     return None
    
# # stupid_test()