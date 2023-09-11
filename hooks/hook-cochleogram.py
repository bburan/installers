# see https://pyinstaller.org/en/stable/hooks.html for info
from PyInstaller.utils.hooks import collect_data_files


datas = collect_data_files('cochleogram', True)

hiddenimports = [
    'cochleogram.model',
    'cochleogram.plot',
    'cochleogram.presenter',
    'cochleogram.readers',
    'cochleogram.util',
]
