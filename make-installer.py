#!/usr/bin/env python3
# adapted from https://stackoverflow.com/questions/63468006

import os
from pathlib import Path
import shutil
import string
import subprocess
import time
import venv

BUILD_FOLDER = Path(__file__).parent / 'build'

MAKENSIS_EXE = "c:/progra~2/NSIS/Bin/makensis.exe"

PKG_CONFIGS = {
    'cochleogram': {
        'name': 'Cochleogram',
        'icon': r'cochleogram\icons\main-icon.ico',
        'scripts': ['cochleogram-main.py'],
        'pip-install': 'cochleogram[lif,czi]',
    },
    'synaptogram': {
        'name': 'Synaptogram',
        'icon': r'synaptogram\icons\main-icon.ico',
        'scripts': ['synaptogram-main.py'],
        'pip-install': 'synaptogram',
    },
    'abr': {
        'name': 'ABR',
        'icon': r'abr\abr-icon.ico',
        'scripts': [
            'abr-main.py',
            'abr-gui.py',
            'abr-batch.py',
            'abr-compare.py',
        ],
    }
}


class EnvBuilder(venv.EnvBuilder):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = None

    def post_setup(self, context):
        self.context = context


def main(package, clean, steps):
    tic = time.time()
    config = PKG_CONFIGS[package]
    env = os.environ.copy()
    env['INSTALLER_NAME'] = package
    env['INSTALLER_SCRIPTS'] = ';'.join(config.get('scripts'))

    if clean and BUILD_FOLDER.exists():
        shutil.rmtree(BUILD_FOLDER)

    venv_folder = BUILD_FOLDER / 'venv' / package

    # Create or obtain context for the venv
    if not venv_folder.exists():
        print(f"Creating virtual env at '{venv_folder}'.")
        venv_builder = EnvBuilder(with_pip=True)
        venv_builder.create(str(venv_folder))
        venv_exe = venv_builder.context.env_exe
        print(venv_exe)
    else:
        venv_exe = str(venv_folder / 'Scripts' / 'python.exe')

    # Install PyInstaller. Do this separately since we don't need to call
    # `--upgrade` for this particular command.
    pip_pyinstaller_install_command = [
        venv_exe,
        '-m',
        'pip',
        'install',
        'PyInstaller',
    ]

    # Now, install the package using `--upgrade` that way we can pull in an
    # updated version of the package if one exists.
    pip_package_install_command = [
        venv_exe,
        '-m',
        'pip',
        'install',
        '--upgrade',
        config.get('pip-install', package),
    ]

    # Now, ensure enaml files are compiled
    enaml_compile_command = [
        venv_exe,
        '-m'
        'enaml.compile_all',
        venv_folder / 'Lib' / 'site-packages'
    ]

    # Running pyinstaller 
    pyinstaller_command = [
        venv_exe,
        '-m',
        'PyInstaller',
        '-y',
        '--distpath',
        str(BUILD_FOLDER / 'pyinstaller'),
        f'template.spec',
    ]

    # Now, get version of package we are creating
    version_command = [
        venv_exe,
        '-c',
        f'import {package}.version; print({package}.version.__version__)'
    ]
    print(' '.join(version_command))

    if 'pip' in steps:
        subprocess.check_call(pip_pyinstaller_install_command)
        subprocess.check_call(pip_package_install_command)
        subprocess.check_call(enaml_compile_command)

    # Get version
    process = subprocess.Popen(version_command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = process.communicate()
    version = out.decode().strip()
    if not version:
        raise ValueError('Could not get version of {package}')
    print(f"Generating pyinstaller for version {version}")

    if 'pyinstaller' in steps:
        subprocess.check_call(pyinstaller_command, env=env)

    if 'nsis' in steps:
        ui_name = config['name']
        icon_path = config['icon']
        install_icon_path = f'build\pyinstaller\{package}\_internal\{icon_path}'
        script = Path(config['scripts'][0]).with_suffix('.exe')
        makensis_command = [
            MAKENSIS_EXE,
            f'/Dversion={version}',
            f'/Dpackage={package}',
            f'/Dui_name={ui_name}',
            f'/Dicon_path={icon_path}',
            f'/Dinstall_icon_path={install_icon_path}',
            f'/Dscript={script}',
            'template.nsi',
        ]
        subprocess.check_call(makensis_command)

    print(f"Total runtime {time.time()-tic:.1f}")
    return


if __name__ == '__main__':
    steps = ['pip', 'pyinstaller', 'nsis']
    import argparse
    parser = argparse.ArgumentParser('make-installer')
    parser.add_argument('package')
    parser.add_argument('-c', '--clean', action='store_true', help='Remove cache')
    parser.add_argument('-s', '--steps', nargs='+', choices=steps, default=steps)
    args = parser.parse_args()
    print(args)
    main(args.package, args.clean, args.steps)
