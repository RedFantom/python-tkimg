# TkImg for Python
[![Build Status](https://travis-ci.com/RedFantom/python-tkimg.svg?branch=master)](https://travis-ci.org/RedFantom/python-tkimg)
[![Build status](https://ci.appveyor.com/api/projects/status/49k2xqvu7x52ul36?svg=true)](https://ci.appveyor.com/project/RedFantom/python-tkimg)
[![codecov](https://codecov.io/gh/RedFantom/python-tkimg/branch/master/graph/badge.svg)](https://codecov.io/gh/RedFantom/python-tkimg)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![PyPI version](https://badge.fury.io/py/tkimg.svg)](https://pypi.python.org/pypi/tkimg)

Python wrapper around TkImg to support more image formats in Tkinter

## Usage
This wrapper uses the binary distributions of `TkImg` (because compiling
them as C-extensions at installation time would be quite difficult on 
the different platforms) and loads them dynamically into a 
Tcl-interpreter instance (belonging to a `Tk` instance) by evaluating
a `pkgIndex.tcl` file.

After the evaluation of this file, the built-in `PhotoImage` class can
be used to open files of all the file types supported by `TkImg`, 
including PNG and TIFF.

```python
import tkinter as tk
from tkimg import load_tkimg

window = tk.Tk()
load_tkimg(window)
tk.PhotoImage('path_to_file.png')
```

## License

    python-tkimg: A Python wrapper to load TkImg into a Tcl-interpreter
    Copyright (C) 2018 RedFantom

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

The `tkimg` project and the files that belong to it, located in
`/binaries`, are under a separate license, described in
`binaries/LICENSE`. This license allows distribution under another 
license, and is thus GNU GPLv3 compatible, as long as the `LICENSE` file
is included.
