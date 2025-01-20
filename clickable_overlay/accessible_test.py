# from typing import List
# from queue import Queue

# from talon import Module, ui, actions, cron

# from user.knausj_talon.clickable_overlay.clickable_overlay import Clickable


# module = Module()


# def crawl_ui_tree(window: ui.Window) -> List:
#     """TODO"""
#     window_rect = window.rect
#     print(dir(window.element))
#     queue = Queue()
#     flattened = []
#     queue.put(window.element)
#     while not queue.empty():
#         current = queue.get()
#         # try:
#         #     rect = current.rect
#         # except OSError:
#         #     rect = None
#         # if not rect or window_rect.intersects(rect):
#         if True:
#             flattened.append(current)
#             for child in current.children:
#                 queue.put(child)
#     return flattened


# @module.action_class
# class Actions:
#     def ui_tree_test():
#         """TODO"""
#         # TODO: Do it with all windows, but only visible windows that are on top
#         window = ui.active_window()
#         window_rect = window.rect
#         clickables = []
        
#         if ui.platform == "windows":
#             CLICKABLE_PATTERNS = {
#                 "Invoke",
#                 "ExpandCollapse",
#                 "SelectionItem",
#                 "TextEdit",
#             }
#         else:
#             raise OSError("Clickable patterns have only bee set up for windows.")
#         for element in crawl_ui_tree(window):
#             try:
#                 rect = element.rect
#             except OSError:
#                 continue
#             if rect.intersects(window_rect):
#                 try:
#                     # print("Pattern:", element.patterns)
#                     if CLICKABLE_PATTERNS.intersection(set(element.patterns)):
#                         clickables.append(Clickable(rect))
#                 except OSError:
#                     pass
#         actions.user.clickable_overlay_show(clickables)


# # def bind():
# #     # TODO: Maybe even extract this to a proper action. Share with Jetbrains?
# #     try:
# #         actions.user.vimfinity_bind_keys({"t": actions.user.ui_tree_test})
# #     except KeyError:
# #         print('Failed to register "ui tree test" keys. Retrying in 1s.')
# #         cron.after("1s", bind)


# # cron.after("1ms", bind)
