import ctypes
import fnmatch

import os
import sys

from distutils.core import setup
import py2exe

if __name__ == "__main__":
    file_name = "autoaccept.py"
    module = __import__(os.path.basename(file_name.split(".")[0]))

    if not "py2exe" in sys.argv:
        sys.argv.append("py2exe")

    sys.path.append(r"C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT")
    sys.path.append(r"C:\Python27\Lib\site-packages")

    setup(options = {
            "py2exe": {
                "compressed": 1,
                "optimize": 2,
                "bundle_files": 1,
                "includes": ["fnmatch", "ctypes"],
                "excludes": [
                    "pywin", "pywin.debugger", "pywin.debugger.dbgcon",
                    "pywin.dialogs", "pywin.dialogs.list", "Tkconstants", "Tkinter", "tcl",
                    "_ssl", "pyreadline", "doctest", "locale", "optparse",
                    "calendar"
                ],
                "dll_excludes": ["oci.dll", "POWRPROF.dll", "msvcr71.dll"]
            }
        },
        zipfile = None,
        windows = [file_name],
        name = "AutoAccept",
        version = module.__version__ if hasattr(module, "__version__") else "1.0.0",
        description = "AutoAccept",
        author = module.__author__ if hasattr(module, "__author__") else "James \"clug\" <clug@clug.xyz>"
    )
