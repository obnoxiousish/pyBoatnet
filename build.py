from distutils.core import setup
import py2exe

setup(
    options={
        "py2exe": {
            "bundle_files": 1,  # create a single-file executable
            "compressed": True,  # compress the library archive
            "optimize": 2,  # enable all available optimizations
            "dll_excludes": ["w9xpopen.exe"],  # exclude this DLL from the distribution
        }
    },
    console=["boatnet.py"],  # the main script to be converted to an executable
    zipfile=None,  # don't create a separate library archive
)