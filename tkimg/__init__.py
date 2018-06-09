"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2018 RedFantom
"""
from collections import namedtuple
from contextlib import contextmanager
import os
try:
    from tkinter import Tk  # Python 3
except ImportError:
    from Tkinter import Tk  # Python 2


__version = namedtuple("Version", "major minor patch")
version = __version(1, 4, 7)


@contextmanager
def change_directory(target):
    """
    Change the current directory but always return the old one

    Based on @github:Akuli's contribution to ttkthemes in _utils.py
    """
    old = os.getcwd()
    os.chdir(target)
    try:
        yield
    finally:
        os.chdir(old)


def get_tkimg_path():
    """
    Return an absolute path to the appropriate TkImg binaries

    The TkImg pkgIndex.tcl file should be located in the same folder as
    this package as the files are copied upon running setup.py.
    """
    file_path = os.path.abspath(__file__)
    return os.path.dirname(file_path)


def get_pkgindex_path():
    """Return an absolute path to the pkgIndex.tcl file to load"""
    return os.path.join(get_tkimg_path(), "pkgIndex.tcl").replace("\\", "/")


def load_tkimg(tk):
    """
    Load the TkImg library into a Tk instance

    The TkImg library provides more file formats than plain Tkinter
    supports. However, it has to be loaded manually with a pkgIndex.tcl
    file. The correct files are copied into the same folder as the
    package upon running setup.py.
    """
    if not isinstance(tk, Tk):
        message = "Invalid argument type for load_tkimg: {}".format(repr(tk))
        raise TypeError(message)
    tk = tk.tk
    tkimg = get_tkimg_path()
    with change_directory(tkimg):
        tk.call("lappend", "auto_path", "[{}]".format(tkimg))
        tk.eval("source {}".format(get_pkgindex_path()))
        tk.call("package", "require", "Img")
