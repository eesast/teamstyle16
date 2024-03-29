import sys, traceback
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","re"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "teamstyle16",
        version = "1.04",
        description = "Teamstyle Sixteen",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Deep Blue.py", base=base, icon="logo.ico"), Executable("debugger.py"), Executable("ai_battle.py")])
