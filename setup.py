"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2018 RedFantom
"""
from os.path import dirname, abspath, join, exists
from os import remove, listdir
from platform import architecture, machine
from setuptools import setup
from shutil import copy
import sys


PLATFORMS = {
    "win32": "win",
    "linux2": "linux"
}

X86 = ["x86_64", "AMD64", "i386"]


def read(file_name):
    """Return the contents of a given file"""
    with open(file_name) as fi:
        return fi.read()


def is_x86():
    """Return whether this machine contains an x86 CPU"""
    return "86" in machine() or machine() in X86


def get_bus_width():
    """Return the memory address bus width for this CPU"""
    return int(architecture()[0][:2])


def get_tkimg_binary_path():
    """Return an abspath to the folder with the right binaries"""
    binaries_folder = join(dirname(abspath(__file__)), "binaries")
    platform = sys.platform
    platform = platform if platform not in PLATFORMS else PLATFORMS[platform]
    bus = get_bus_width()
    platform_folder = "{}{}".format(platform, bus)
    return join(binaries_folder, platform_folder)


def get_tkimg_source_path():
    """Return an abspath to the folder with the source for the package"""
    return join(dirname(abspath(__file__)), "tkimg")


if __name__ == '__main__':
    """
    Setup the library to be installed
    
    Perform platform checks and copy over the binary files required for
    running the library.
    """
    if "sdist" in sys.argv[1]:
        raise RuntimeError("This package does not support sdists")
    if not is_x86():
        raise RuntimeError("TkImg is not supported on non-x86 platforms.")
    bpath = get_tkimg_binary_path()
    if not exists(bpath):
        raise RuntimeError("Unsupported platform or architecture")
    spath = get_tkimg_source_path()
    to_copy = listdir(bpath)
    for file in to_copy:
        source = join(bpath, file)
        target = join(spath, file)
        if exists(target):
            remove(target)
        copy(source, target)


setup(
    name="tkimg",
    packages=["tkimg"],
    package_data={"tkimg": ["*.tcl", "*.so", "*.dll"]},
    version="0.0.1",
    description="A Python wrapper to load TkImg into a Tk interpreter",
    author="RedFantom",
    author_email="redfantom@outlook.com",
    url="https://github.com/RedFantom/python-tkimg",
    include_package_data=True,
    zip_safe=False,
    keywords=["tkinter", "gui", "tcl"],
    license="GPLv3",
    long_description=read("README.md"),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Software Development :: Libraries :: Tcl Extensions',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
