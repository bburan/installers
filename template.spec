# -*- mode: python ; coding: utf-8 -*-
import os
name = os.environ['INSTALLER_NAME']
scripts = [s.strip() for s in os.environ['INSTALLER_SCRIPTS'].split(';')]

block_cipher = None
collect = []

for script in scripts:
	a = Analysis(
		[f'scripts/{name}/{script}'],
		pathex=[],
		binaries=[],
		datas=[],
		hiddenimports=[],
		hookspath=['hooks'],
		hooksconfig={},
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

	collect.append(a.binaries)
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
