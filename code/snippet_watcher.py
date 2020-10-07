# from talon import app, fs
# import os, csv, re
# from os.path import isfile, join
# from itertools import islice
# from pathlib import Path
# import json
# from jsoncomment import JsonComment

# parser = JsonComment(json)

# pattern = re.compile(r"[A-Z][a-z]*|[a-z]+|\d")

# # todo: should this be an action that lives elsewhere??
# def create_spoken_form(text, max_len=15):
#     return " ".join(list(islice(pattern.findall(text), max_len)))


# class snippet_watcher:
#     directories = {}
#     snippet_dictionary = {}
#     callback_function = None
#     file_snippet_cache = {}

#     def __notify(self):
#         # print("NOTIFY")
#         self.snippet_dictionary = {}
#         for key, val in self.file_snippet_cache.items():
#             self.snippet_dictionary.update(val)

#         # print(str(self.snippet_dictionary))
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

#                 for key, data in jsonDict.items():
#                     self.file_snippet_cache[str(path_obj)][
#                         create_spoken_form(key)
#                     ] = data["prefix"]

#     def __on_fs_change(self, name, flags):
#         self.__process_file(name)

#         # print(str(self.snippet_dictionary))
#         self.__notify()

#     def __init__(self, dirs, callback):
#         self.directories = dirs
#         self.callback_function = callback
#         self.snippet_dictionary = {}
#         self.file_snippet_cache = {}
#         # none = process all directories
#         self.__update_all_snippets()

#         for directory in self.directories.keys():
#             if os.path.isdir(directory):
#                 fs.watch(directory, self.__on_fs_change)
#             # else:
#             #     print(
#             #         "snippet_watcher.py: directory {} does not exist".format(directory)
#             #     )


# # Test = snippet_watcher(
# #     {os.path.expandvars(r"%AppData%\Code\User\snippets"): ["python.json"]},
# #     None
# #     # {os.path.expandvars(r"%USERPROFILE%\.vscode\extensions\ms-dotnettools.csharp-1.22.1\snippets": ["csharp.json"]},
# # )
# # print(str(Test.directories))
