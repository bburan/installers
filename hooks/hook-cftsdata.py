# see https://pyinstaller.org/en/stable/hooks.html for info
from PyInstaller.utils.hooks import collect_submodules

# cftsdata is forced into the graph as a bare top-level name from
# hook-psi.py's hiddenimports (cftscal/psi reach its submodules, e.g.
# cftsdata.api, only via dotted-string/enaml-invisible paths), so nothing
# else pulls in the actual submodules -- same reasoning as hook-psidata.py.
hiddenimports = collect_submodules('cftsdata')
