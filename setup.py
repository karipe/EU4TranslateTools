import sys
from cx_Freeze import setup, Executable

build_exe_options = dict(
    includes=["os", "subprocess", "sys", "re", "openpyxl"],
    include_files=[]
)

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="EU4TranslateTool",
    version="1.0",
    author="Styx",
    description="EU4TranslateTool for Europa cafe",
    options={"build_exe": build_exe_options},
    executables=[Executable("EU4Tools.py", base=base, targetName="EU4Tools.exe")]
)