# from talon import ui
# import debugpy
import sys


def _temp_trace(frame, event, arg):
    return None


sys.settrace(_temp_trace)
# debugpy.listen(("localhost", 5679))
# debugpy.wait_for_client()


# def main():
#     debugpy.listen(("localhost", 5679))
#     debugpy.wait_for_client()
#     for app in ui.apps():
#         print(app.name)


# print("I'm okay")
# main()
