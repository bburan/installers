# CLAUDE.md

PyInstaller-based Windows installer builds for several Qt/enaml scientific apps
(cochleogram, cftscal, abr, synaptogram, ...). `make-installer.py` drives the
per-app venv → PyInstaller (`template.spec`) → NSIS pipeline. Package-specific
PyInstaller hooks live in `hooks/`.

## Build & repo layout

- **`make-installer.py`** — entry point. `PKG_CONFIGS` maps each package to its
  UI name, icon, entry scripts, and pip specs. Steps are `pip`, `pyinstaller`,
  `nsis` (`-s` to select a subset); `-c` wipes `build/` (venv included); `-o`
  builds a onefile portable via `onefile-template.spec`.
- **Per-package layout:** venv at `build/venv/<package>/`, entry scripts at
  `scripts/<package>/*.py`, PyInstaller output at
  `build/pyinstaller/<package>/` (onedir: exe at top, everything under
  `_internal/`), final installer in `dist/`.
- **`template.spec` is shared by every package** (the same spec is reused; the
  package is selected via the `INSTALLER_NAME`/`INSTALLER_SCRIPTS` env vars set
  by `make-installer.py`). Consequently PyInstaller's build artifacts are named
  after the spec, not the app: **`build/template/warn-template.txt`** (missing
  modules) and **`xref-template.html`** (import graph) — these reflect the most
  recent build regardless of which package it was. Any spec change affects all
  apps; keep it generic and safe.
- This dev machine's base interpreter is `anaconda3/envs/installers`
  (Python 3.13.15); the per-package venvs are built from it. Extensions are
  cp313 (e.g. `aicspylibczi`). Multiple Pythons (3.11/3.13/3.14) exist on the
  machine — don't assume a bare `python` is the right one; use the package venv.

## Working with the frozen bundles (gotchas)

- **Pure-Python modules live inside the PYZ archive, not loose on disk.** A
  package having no folder under `_internal/` does NOT mean it's missing — only
  C extensions (`.pyd`) and data files are loose. Check `warn-template.txt` /
  `xref-template.html` (or the PYZ) before concluding something wasn't bundled.
- **GUI entry points take the data path as a CLI arg** and route it through the
  same load code as drag-and-drop (e.g. `cochleogram-main.py`'s `path` arg →
  `deferred_call(load_dataset, ...)`). This is the fastest way to reproduce a
  data-loading bug headlessly: run the frozen console exe with the file/folder
  as an argument and read stdout/stderr.
- **Kill lingering exes before rebuilding.** A still-running `*-main.exe` (or a
  hung PyInstaller `python.exe`) holds `_internal/base_library.zip` and DLLs
  open, so `COLLECT`'s clean step fails with `WinError 32 / Device or resource
  busy`. Stop stray processes first.
- **Full builds are slow** (~1.5–2 min to collect the scientific stack). To
  bisect a packaging problem, build a *minimal* throwaway exe that imports only
  the suspect module(s) — those build in seconds and isolate the cause. Add
  `--additional-hooks-dir hooks` to reproduce this repo's hook behavior.
- **Reader backends are imported lazily** inside functions (e.g.
  `from readlif.reader import LifFile`), but PyInstaller's static analysis still
  collects them. Note `util.load_czi`/`load_lif` call
  `importlib.metadata.version('cochleogram')`, so the package `.dist-info`
  metadata must be bundled or a *successful* load raises `PackageNotFoundError`.
- cochleogram pins `QT_API=pyqt5` (its entry script) and was deliberately
  switched PySide6 → PyQt5 for Windows 10 compatibility; don't switch it back
  without cause. cftscal uses Qt6/PySide6.

## Known bug: split MSVC runtime segfaults native extensions (PyQt5 + libCZI)

**Symptom:** A frozen build starts fine and the GUI opens, but exercising a
native C++ code path hard-crashes with a segfault (exit 139) — **no Python
traceback, no error dialog** (a native crash can't be caught by `try/except`).
The same operation works in the venv build. Concretely: cochleogram opens, but
dropping/opening a `.czi` file (which goes through `aicspylibczi`/libCZI)
crashes.

**Cause:** A **split Visual C++ runtime** inside the bundle. The PyQt5 5.15
wheel ships its *own older* VC runtime (e.g. `MSVCP140.dll` 14.26) inside
`PyQt5/Qt5/bin/`, while Python/aicspylibczi contribute the *modern* one (e.g.
14.44) at the bundle root (`_internal/`). PyInstaller keeps both because they
live in different directories. At runtime Qt loads first and pins the old
`MSVCP140.dll`, but `VCRUNTIME140.dll` resolves to the modern root copy — a
mismatched runtime that corrupts C++ heap/exception state. Native code built
against the newer toolset (libCZI) then segfaults. The venv build works because
it uses a single consistent *system* runtime.

**Fix (in `template.spec`):** `a.binaries` is filtered through
`_dedupe_vc_runtime()`, which drops nested duplicate VC runtime DLLs
(`msvcp140*`, `vcruntime140*`, `concrt140`, `vccorlib140`) whenever a top-level
copy exists, so the whole process shares one runtime. It never removes the sole
copy of a DLL (e.g. `MSVCP140_1.dll` stays — no top-level copy exists and libCZI
doesn't import it). This lives in the shared spec, so it also protects the other
Qt installers.

**Requires a clean build.** PyInstaller's `COLLECT` does not prune stale files
from a dirty `dist` dir, so an incremental rebuild over an old output leaves the
bad DLLs behind. Use `make-installer.py -c <package>` or wipe
`build/pyinstaller/<package>` first.

**Diagnosing this class of bug:** The GUI entry points accept the data path as a
CLI arg (e.g. `cochleogram-main.py`'s `path` arg routes through the same
`load_dataset` as drag-and-drop), so you can reproduce headlessly by running the
frozen console exe with the file/folder as an argument. To find a mismatched
DLL, enumerate the crashing process's loaded modules via PowerShell
`(Get-Process).Modules` and check `.VersionInfo.FileVersion` — look for the same
DLL family loading from mixed directories.
