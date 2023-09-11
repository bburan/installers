#!/usr/bin/env python3
# adapted from https://stackoverflow.com/questions/63468006

import os
import pathlib
import string
import subprocess
import tempfile
import venv


makensis_exe = "c:/progra~2/NSIS/Bin/makensis.exe"

PKG_CONFIGS = {
    'cochleogram': {
        'name': 'Cochleogram',
        'icon': r'cochleogram\icons\main-icon.ico',
        'scripts': ['cochleogram-main.py'],
        'pip-install': 'cochleogram[lif]',
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


def main(package):
    config = PKG_CONFIGS[package]
    env = os.environ.copy()
    env['INSTALLER_NAME'] = package
    env['INSTALLER_SCRIPTS'] = ';'.join(config.get('scripts'))

    with tempfile.TemporaryDirectory() as target_dir_path:
        print(f"Creating virtual env at '{target_dir_path}'.")

        venv_builder = EnvBuilder(with_pip=True)
        venv_builder.create(str(target_dir_path))
        venv_context = venv_builder.context

        pip_install_command = [
            venv_context.env_exe,
            '-m',
            'pip',
            'install',
            config.get('pip-install', package),
            'PyInstaller',
        ]
        subprocess.check_call(pip_install_command)

        version_command = [
            venv_context.env_exe,
            '-c',
            f'import {package}.version; print({package}.version.__version__)'
        ]
        process = subprocess.Popen(version_command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = process.communicate()
        version = out.decode().strip()
        if not version:
            raise ValueError('Could not get version of {package}')

        print(f"Generating pyinstaller for version {version}")

        pyinstaller_command = [
            venv_context.env_exe,
            '-m',
            'PyInstaller',
            '--clean',
            '-y',
            f'template.spec',
        ]
        subprocess.check_call(pyinstaller_command, env=env)

        ui_name = config['name']
        icon = config['icon']
        script = pathlib.Path(config['scripts'][0]).with_suffix('.exe')
        makensis_command = [
            makensis_exe,
            f'/Dversion={version}',
            f'/Dpackage={package}',
            f'/Dui_name={ui_name}',
            f'/Dicon_path={icon}',
            f'/Dscript={script}',
            'template.nsi',
        ]
        subprocess.check_call(makensis_command)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('make-installer')
    parser.add_argument('package')
    args = parser.parse_args()
    main(args.package)
