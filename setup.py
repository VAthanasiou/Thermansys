import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os"],
                    "include_files":['optionDB.py','img_alg_enh.py','crop_image.py','GUI.py','Img_path.py','Information.py',
                                    'ir_lock_in_4_dots.py','ir_lock_in_prds.py', 'pulsed_phase.py','READ ME.txt',
                                    'setup.py', 'standard_dev.py','Manual','images','__pycache__'] 
                    }

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Thermansys",
    version="0.1",
    description="Thermal Imaging Toolbox",
    options={"build_exe": build_exe_options},
    executables=[Executable("GUI.py", base=base)],
)

#################### RUN:-> Terminal : python setup.py build ##########################