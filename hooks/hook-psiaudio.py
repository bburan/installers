# see https://pyinstaller.org/en/stable/hooks.html for info
from PyInstaller.utils.hooks import collect_data_files

# psiaudio.calibration loads psiaudio/resources/starship_cal.csv via
# importlib.resources at runtime (used by cftscal's starship plugin).
# PyInstaller has no way to know about it unless told explicitly.
datas = collect_data_files('psiaudio')
