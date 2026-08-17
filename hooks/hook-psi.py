# see https://pyinstaller.org/en/stable/hooks.html for info
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = collect_data_files('psi', True)

hiddenimports = collect_submodules('psi')
hiddenimports += [
    'cftsdata',
    'palettable',
    'psidata',
    'pyqtgraph',
    'qtpy.compat',
    'zarr',
]
