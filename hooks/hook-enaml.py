from PyInstaller.utils.hooks import collect_data_files


datas = collect_data_files('enaml', excludes=['**/*.enaml'])


hiddenimports = [
    'enaml.core',
    'enaml.core.api',
    'enaml.core.compiler_helpers',
    'enaml.core.parser',
    'enaml.core.template_',
    'enaml.layout',
    'enaml.layout.api',
    'enaml.qt',
    'enaml.qt.docking',
    'enaml.stdlib',
    'enaml.widgets',
    'enaml.widgets.api',
    'enaml.winutil',
]
