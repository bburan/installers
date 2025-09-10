# see https://pyinstaller.org/en/stable/hooks.html for info
from PyInstaller.utils.hooks import collect_data_files


datas = collect_data_files('ncrar_eeg_viewer', excludes=['**/*.enaml'])

hiddenimports = [
    'ncrar_eeg_viewer.gui',
    'ncrar_eeg_viewer.io',
    'ncrar_eeg_viewer.main',
    'ncrar_eeg_viewer.presenter',
    'ncrar_eeg_viewer.version',
]
