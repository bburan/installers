# -*- mode: python ; coding: utf-8 -*-
import os
name = os.environ['INSTALLER_NAME']
scripts = [s.strip() for s in os.environ['INSTALLER_SCRIPTS'].split(';')]
if len(scripts) > 1:
    raise ValueError('Cannot handle more than one script')
script = scripts[0]
exe_name = os.environ['PYINSTALLER_EXE_NAME']

block_cipher = None

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
    a.binaries,
    a.zipfiles,
    a.datas,
    name=exe_name,
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,
)
