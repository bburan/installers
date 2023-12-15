# see https://pyinstaller.org/en/stable/hooks.html for info
from PyInstaller.utils.hooks import collect_data_files


datas = collect_data_files('ndimage_enaml', excludes=['**/*.enaml'])

hiddenimports = [
    'ndimage_enaml.model',
    'ndimage_enaml.gui',
    'ndimage_enaml.presenter',
    'ndimage_enaml.util',
]
