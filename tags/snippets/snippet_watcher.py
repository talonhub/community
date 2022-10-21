# from talon import app, fs, actions
# import os, csv, re
# from os.path import isfile, join
# from itertools import islice
# from pathlib import Path
# import json
# from jsoncomment import JsonComment

# parser = JsonComment(json)


# class snippet_watcher:
#     directories = {}
#     snippet_dictionary = {}
#     callback_function = None
#     file_snippet_cache = {}
#     create_spoken_forms = False

#     def __notify(self):
#         #print("NOTIFY")
#         self.snippet_dictionary = {}
#         for key, val in self.file_snippet_cache.items():
#             self.snippet_dictionary.update(val)

#         if self.callback_function:
#             self.callback_function(self.snippet_dictionary)

#     def __update_all_snippets(self):
#         for directory, file_list in self.directories.items():
#             if os.path.isdir(directory):
#                 for f in file_list:
#                     path = os.path.join(directory, f)
#                     self.__process_file(path)

#         # print(str(self.snippet_dictionary))
#         self.__notify()

#     def __process_file(self, name):
#         path_obj = Path(name)
#         directory = os.path.normpath(path_obj.parents[0])
#         file_name = path_obj.name
#         file_type = path_obj.suffix
#         self.file_snippet_cache[str(path_obj)] = {}

#         print("{}, {}, {}, {}".format(name, directory, file_name, file_type))
#         if directory in self.directories and file_name in self.directories[directory]:
#             if file_type.lower() == ".json":
#                 jsonDict = {}

#                 if os.path.isfile(name):
#                     with open(name, "r") as f:
#                         jsonDict = parser.load(f)
#                 # else:
#                 #     print("snippet_watcher.py: File {}  does not exist".format(directory))

#                 map_to_process = {}
#                 for key, data in jsonDict.items():
#                     map_to_process[key] = data["prefix"]

#                 if self.create_spoken_forms:
#                     spoken_forms = actions.user.create_spoken_forms_from_map(
#                         map_to_process
#                     )
#                     self.file_snippet_cache[str(path_obj)] = spoken_forms
#                 else:
#                     self.file_snippet_cache[str(path_obj)] = map_to_process

#     def __on_fs_change(self, name, flags):
#         self.__process_file(name)

#         # print(str(self.snippet_dictionary))
#         self.__notify()

#     def __init__(self, dirs, callback, create_spoken_forms=False):
#         self.directories = dirs
#         self.callback_function = callback
#         self.snippet_dictionary = {}
#         self.file_snippet_cache = {}
#         self.create_spoken_forms = create_spoken_forms

#         # on ready is used so we know create_spoken_forms is available.
#         app.register("ready", self.on_ready)

#         # none = process all directories

#         # else:
#         #     print(
#         #         "snippet_watcher.py: directory {} does not exist".format(directory)
#         #     )

#     def on_ready(self):
#         self.__update_all_snippets()
#         for directory in self.directories.keys():
#             if os.path.isdir(directory):
#                 fs.watch(directory, self.__on_fs_change)


# # Test = snippet_watcher(
# #     {os.path.expandvars(r"%AppData%\Code\User\snippets"): ["python.json"]},
# #     None
# #     # {os.path.expandvars(r"%USERPROFILE%\.vscode\extensions\ms-dotnettools.csharp-1.22.1\snippets": ["csharp.json"]},
# # )
# # print(str(Test.directories))
