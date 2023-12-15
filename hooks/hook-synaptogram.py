# see https://pyinstaller.org/en/stable/hooks.html for info
from PyInstaller.utils.hooks import collect_data_files


datas = collect_data_files('synaptogram', excludes=['**/*.enaml'])

hiddenimports = [
    'synaptogram.gui',
    'synaptogram.main',
    'synaptogram.model',
    'synaptogram.presenter',
    'synaptogram.reader',
]
