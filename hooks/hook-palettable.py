# see https://pyinstaller.org/en/stable/hooks.html for info
from PyInstaller.utils.hooks import collect_submodules

# cftscal/psi views import specific palettable submodules (e.g.
# palettable.colorbrewer.qualitative, palettable.tableau) only from inside
# .enaml files, and psi.data.plots.get_color_cycle() resolves a colormap
# module by dotted string at runtime -- both invisible to PyInstaller's
# static analysis.
hiddenimports = collect_submodules('palettable')
