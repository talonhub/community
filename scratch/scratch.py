# import win32com.client

# def get_app_aumid(app_name):
#     shell = win32com.client.Dispatch("Shell.Application")
#     folder = shell.NameSpace('shell:::{4234d49b-0245-4df3-b780-3893943456e1}')
#     items = folder.Items()
    
#     for item in items:
#         print(str(item))
#         if app_name.lower() in item.Name.lower():
#             return item.Path
#     return None
    
# get_app_aumid("Visual Studio Code")