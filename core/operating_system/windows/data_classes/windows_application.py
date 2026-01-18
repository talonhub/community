# This is a list of known "modern" windows applications where we can't access the executable
from dataclasses import dataclass


@dataclass
class windows_application:
    """Class for tracking properties of known applications"""
    display_name: str
    unique_identifier: str
    executable_path: str
    executable_name: str
    is_uwp: bool = False