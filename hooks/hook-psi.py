# see https://pyinstaller.org/en/stable/hooks.html for info
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# psiexperiment (imported as `psi`) is cftscal's hardware/experiment engine.
# Like cftscal, its plugin manifests and views live in .enaml files that are
# loaded via enaml's own import hook from the precompiled `__enamlcache__`,
# not PyInstaller's module graph, so drop the raw source -- same reasoning as
# hook-cftscal.py and the other enaml-based hooks in this repo.
datas = collect_data_files('psi', excludes=['**/*.enaml'])

# Exception: psi/templates/io/*.enaml (and psi/templates/config.txt) are not
# manifests to be imported -- they are literal skeleton files that
# `psi-config create-io`/`create` copy out verbatim for a user to edit into
# their own hardware config (see psi/__init__.py and
# psi/application/__init__.py:list_io_templates). Those must ship as real
# .enaml/.txt text, so pull the templates subtree back in without the
# exclusion above (config.txt gets collected twice; harmless).
datas += collect_data_files('psi', subdir='templates')

# psi resolves almost everything by dotted string at runtime rather than
# static import: the hardware engine named in the IO manifest
# (psi.controller.engines.{nidaq,tdt,soundcard,biosemi,...}), data sinks,
# calibration routines, and any manifest reached via
# psi.core.enaml.api.load_manifest() -- none of that is visible to
# PyInstaller's static analysis. Collect every submodule psi ships so the
# hardware backend selected at runtime (which this installer script has no
# way to know in advance) is available. Optional hardware backends whose
# extra dependency isn't installed in this build's venv (pydaqmx/nidaqmx for
# `ni`, tdtpy for `tdt`, sounddevice/rtmixer for `soundcard`, pyactivetwo for
# biosemi) are silently skipped -- add the relevant psiexperiment[...] extra
# to that package's `pip-install` entry in make-installer.py if you need one
# of them bundled.
hiddenimports = collect_submodules('psi')

# `palettable` is only ever reached by dotted-string default (e.g.
# psi/data/plots.py's `'palettable.colorbrewer.qualitative.Dark2_8'`,
# resolved through get_color_cycle()'s importlib.import_module()) or from
# inside cftscal's .enaml files -- never a plain .py import in psi itself.
# A module hook (hook-palettable.py) only runs once something puts that
# module in the graph; nothing does unless it's forced here. Since a
# psi-only installer wouldn't otherwise pull in cftscal's forced import
# (see hook-cftscal.py), force it from psi's side too.
hiddenimports += ['palettable']
