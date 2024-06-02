from cx_Freeze import setup, Executable
# Packages
from app.core.pyside_or_pyqt import * # Qt

# GUIs
# Modules

# ADD FILES/FOLDERS
files = ['icon.ico', 'settings.json','images/']

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="icon.ico"
)

# SETUP CX FREEZE
setup(
    name = "PyBlackBOX",
    version = "1.0",
    description = "Modern GUI for desktop chat",
    author = "Wanderson M. Pimenta",
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]    
)
