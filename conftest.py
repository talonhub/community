"""
Configuration file for pytest

See also https://docs.pytest.org/en/6.2.x/writing_plugins.html#writing-hook-functions
"""

import importlib
import os
import sys


class UnitTestPathFinder(importlib.machinery.PathFinder):
    """
    Makes the knausj_talon repo root directory available under
    knausj_talon_pkg and tests/stubs/talon/ available
    under talon. Activated by the code in pytest_sessionstart()

    A loader is needed since the 'code' folder in knausj conflicts
    with the built in python 'code' module. Renaming the folder
    could cause merge conflicts.
    """

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        curr_dir = os.path.dirname(__file__)
        knausj_prefix = "knausj_talon_pkg"

        if fullname == "talon" or fullname.startswith("talon."):
            # Load talon stubs as talon module
            filepath = os.path.join(curr_dir, "tests", "stubs")
            return super().find_spec(fullname, [filepath])
        elif fullname == knausj_prefix:
            # Load knausj_talon root module
            return importlib.machinery.ModuleSpec(
                name=fullname,
                loader=importlib.machinery.SourceFileLoader(
                    fullname, os.path.join(curr_dir, "tests", "repo_root_init.py")
                ),
                is_package=True,
            )
        elif fullname.startswith(knausj_prefix + "."):
            # Load knausj_talon submodules
            return super().find_spec(fullname, [curr_dir])
        else:
            # Allow normal sys.path stuff to handle everything else
            return None


def pytest_sessionstart():
    """
    Set up test environment. Only invoked when we're in the pytest
    environment so as not to mess with the Talon runtime.
    """

    sys.meta_path.append(UnitTestPathFinder)
