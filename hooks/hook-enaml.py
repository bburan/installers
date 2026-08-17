from PyInstaller.utils.hooks import collect_data_files, collect_submodules


datas = collect_data_files('enaml', excludes=['**/*.enaml'])

# enaml.workbench (and its ui/core sub-plugins) is only ever reached from
# inside .enaml files -- cftscal/psi's own plugin manifests, and enaml's own
# core_manifest.enaml/ui_manifest.enaml loaded via `with enaml.imports():` in
# cftscal/main.py -- which is invisible to PyInstaller's static analysis.
# That's the same problem hook-cftscal.py/hook-psi.py solve for those
# packages' own code; here it's enaml's own library code. The hand-curated
# list below used to work fine for the non-workbench installers in this repo
# (cochleogram, abr, synaptogram, ...), but missed `enaml.workbench.core.api`
# the moment a workbench-based app (cftscal) was added -- and would keep
# missing workbench submodules one ModuleNotFoundError at a time. Collect
# everything enaml ships instead; it's a strict superset of the old list.
hiddenimports = collect_submodules('enaml')
