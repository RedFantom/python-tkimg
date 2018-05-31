"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2018 RedFantom
"""
# Testing dependencies
from os.path import abspath, dirname, join, exists
from os import listdir
try:
    from tkinter import Tk, PhotoImage, Label
except ImportError:
    from Tkinter import Tk, PhotoImage, Label
from unittest import TestCase
# Library to test
import tkimg


def get_assets_directory():
    """Return an absolute path to the assets directory"""
    return abspath(join(dirname(abspath(__file__)), "..", "assets"))


class TestTkImg(TestCase):
    """
    Run tests on TkImg

    Tests include:
    - Testing TkImg library path finding
    - Testing TkImg library loading into a Tk instance
    - Testing TkImg functionality by loading different types of files
    """

    def setUp(self):
        """Initialize a window to do testing on"""
        self.window = Tk()

    def test_tkimg_path(self):
        """Test whether the TkImg files are properly detected"""
        self.assertTrue(exists(tkimg.get_pkgindex_path()))
        self.assertTrue(exists(tkimg.get_tkimg_path()))

    def test_load_tkimg(self):
        """Test basic TkImg loading"""
        tkimg.load_tkimg(self.window)
        version = self.window.tk.eval("package require Img")
        for rep, real in zip(map(int, version.split(".")), tkimg.version):
            self.assertEqual(rep, real)

    def test_load_image(self):
        """Load TkImg into a Tk instance and then try to open some files"""
        tkimg.load_tkimg(self.window)
        assets = get_assets_directory()
        for file in listdir(assets):
            path = join(assets, file)
            img = PhotoImage(path)
            Label(self.window, image=img)

    def tearDown(self):
        self.window.destroy()
