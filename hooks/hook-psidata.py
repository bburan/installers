# see https://pyinstaller.org/en/stable/hooks.html for info
from PyInstaller.utils.hooks import collect_submodules

# psidata is a plain-Python package (no .enaml of its own), but its
# submodules are reached only via dotted-string/enaml-invisible paths from
# psi and cftscal -- e.g. psi/data/sinks/zarr_store.enaml does
# `from psidata.zarr_tools import ZarrSignal`, which is inside an .enaml
# file and thus invisible to PyInstaller's static analysis. No .py file
# anywhere in psi/cftscal/cftsdata plainly imports psidata.zarr_tools, so
# nothing else puts it in the graph. Same reasoning as hook-psi.py's
# collect_submodules('psi') -- collect everything psidata ships rather than
# hand-list submodules and silently miss the next one.
hiddenimports = collect_submodules('psidata')
