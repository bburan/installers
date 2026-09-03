# -*- mode: python ; coding: utf-8 -*-
import os
name = os.environ['INSTALLER_NAME']
scripts = [s.strip() for s in os.environ['INSTALLER_SCRIPTS'].split(';')]

block_cipher = None
collect = []

# The Visual C++ runtime DLLs (MSVCP140/VCRUNTIME140/etc.) must be loaded as a
# single matched set for the whole process. The PyQt5 wheel ships its own
# *older* copy inside PyQt5/Qt5/bin (e.g. 14.26), while Python/aicspylibczi
# contribute the modern one (e.g. 14.44) at the bundle root. PyInstaller keeps
# both because they live in different directories. At runtime Qt loads first
# and pins the old MSVCP140.dll, but VCRUNTIME140.dll still resolves to the
# modern root copy -- a split runtime that corrupts C++ heap/exception state.
# This segfaults native extensions built against the newer toolset: notably
# libCZI (aicspylibczi), which crashes when reading a .czi file even though the
# GUI itself starts fine. Drop the nested duplicates so only the root copy
# remains and every module shares one runtime. Never remove the sole copy of a
# DLL (only a nested one when a top-level one also exists).
_VC_RUNTIME_DLLS = {
    'vcruntime140.dll', 'vcruntime140_1.dll',
    'msvcp140.dll', 'msvcp140_1.dll', 'msvcp140_2.dll',
    'concrt140.dll', 'vccorlib140.dll',
}


def _dedupe_vc_runtime(binaries):
    # A top-level entry has no directory component in its destination name.
    top_level = {
        os.path.basename(dest).lower()
        for dest, src, typ in binaries
        if os.path.basename(dest).lower() in _VC_RUNTIME_DLLS
        and os.path.dirname(dest) == ''
    }
    kept = []
    for dest, src, typ in binaries:
        base = os.path.basename(dest).lower()
        if base in _VC_RUNTIME_DLLS and os.path.dirname(dest) != '' and base in top_level:
            print(f'template.spec: dropping duplicate VC runtime {dest} (using top-level copy)')
            continue
        kept.append((dest, src, typ))
    return kept

for script in scripts:
    a = Analysis(
        [f'scripts/{name}/{script}'],
        pathex=[],
        binaries=[],
        datas=[],
        hiddenimports=[],
        hookspath=['hooks'],
        hooksconfig={
            "matplotlib": { "backends": ["QtAgg", "PDF"] },
        },
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher,
        noarchive=False,
    )

    pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=script[:-3],
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=True,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )

    collect.append(_dedupe_vc_runtime(a.binaries))
    collect.append(a.zipfiles)
    collect.append(a.datas)
    collect.append(exe)

coll = COLLECT(
    *collect, 
    strip=False,
    upx=True,
    upx_exclude=[],
    name=name,
)

