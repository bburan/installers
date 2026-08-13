# see https://pyinstaller.org/en/stable/hooks.html for info
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# cftscal is a UIWorkbench app built almost entirely out of enaml manifests
# (plugins/*/manifest.enaml, plugins/*/view.enaml, paradigms/*.enaml). Those
# are loaded by enaml's own import hook from the precompiled `__enamlcache__`
# next to each source file (produced by `enaml.compile_all` during the
# build), not by PyInstaller's module graph. So, as with the other
# enaml-based hooks in this repo, drop the raw .enaml source: shipping it
# would make enaml try to recompile from source at runtime, which fails once
# installed under Program Files (no write access), and it isn't needed since
# the cache is already fresh.
datas = collect_data_files('cftscal', excludes=['**/*.enaml'])

# cftscal.plugins.manifest.TO_REGISTER loads every calibration plugin
# (microphone, speaker, starship, in-ear, ...) by dotted string via
# importlib.import_module() at runtime (main.py / reload_plugins()), and the
# individual plugin modules (settings.py, objects.py, workspace.py, ...) are
# otherwise only ever imported from inside .enaml manifests/views -- both
# invisible to PyInstaller's static analysis. Rather than hand-list every
# plugin module (and silently miss one whenever a plugin is added), pull in
# everything cftscal ships.
hiddenimports = collect_submodules('cftscal')

# `palettable` (e.g. cftscal/plugins/widgets.enaml's
# `from palettable.tableau import Tableau_20`) is used *only* from inside
# .enaml files, never from a plain .py import anywhere in cftscal/psi/
# psiaudio. hook-palettable.py in this repo collects its submodules, but a
# module hook only runs once PyInstaller's Analysis has already decided that
# module belongs in the graph -- and nothing else puts `palettable` there.
# List it explicitly here (cftscal is always in the graph, via the entry
# script) so hook-palettable.py actually gets a chance to run.
hiddenimports += ['palettable']
