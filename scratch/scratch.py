import os
import shlex
import subprocess
import time
from pathlib import Path
import csv
import talon
from talon import Context, Module, actions, app, imgui, ui, resource
from typing import Union
import re
from talon.ui import Rect
from talon.windows.ax import Element
from dataclasses import dataclass

@dataclass
class TaskBarItem:
    title: str
    type: str
    element: Element

def first_matching_child(element, **kw):
    if len(kw) > 1:
        raise Exception("Only one matching attribute supported")
    attr, values = list(kw.items())[0]
    return next(e for e in element.children if getattr(e, attr) in values)

def stest():
    explorer = ui.apps(name="Windows Explorer")[0]
    tray = next(
        window for window in explorer.windows() if window.cls == "TrayNotifyWnd"
    )
    taskbar = next(
        window for window in explorer.windows() if window.cls == "Shell_TrayWnd"
    )
    tray = first_matching_child(taskbar.element, class_name=["TrayNotifyWnd"])
    pager = first_matching_child(tray, class_name=["SysPager"])
    toolbar = first_matching_child(pager, class_name=["ToolbarWindow32"])
    for e in toolbar.children:
        print(f"{e.name}")

#stest()