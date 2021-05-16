"""
Configuration file for pytest

See also https://docs.pytest.org/en/6.2.x/writing_plugins.html#writing-hook-functions
"""

import os
import sys


def pytest_sessionstart():
    """
    Only modify the path when run via pytest (not in the Talon runtime)
    """

    # Make the talon. stubs available to tests
    curr_dir = os.path.dirname(__file__)
    sys.path.append(os.path.join(curr_dir, "tests", "stubs"))

    # Makes the code/ module available as knausj_code/ for use in tests. pytest uses
    # the builtin python code module which prevents us from importing the knausj one.
    # I've elected not to rename code as this would cause merge errors for forks that
    # have modified it.
    # This implementation just creates a simple symlink. An alternative might be to
    # look at customising the python module loader:
    # https://docs.python.org/3/reference/import.html
    # I've had a go at relative imports without success.
    symlink_src = os.path.join(curr_dir, "code")
    symlink_dest = os.path.join(curr_dir, "knausj_code")
    if not os.path.exists(symlink_dest):
        os.symlink(symlink_src, symlink_dest)


def pytest_sessionfinish():
    """
    Clean up after our test run
    """

    # Remove the knausj_code symlink trick
    curr_dir = os.path.dirname(__file__)
    symlink_dest = os.path.join(curr_dir, "knausj_code")
    if os.path.exists(symlink_dest):
        os.unlink(symlink_dest)
