from PyInstaller.utils.hooks import collect_data_files


datas = collect_data_files('biosemi_enaml', excludes=['**/*.enaml'])



hiddenimports = [
    'biosemi_enaml.channel_maps',
    'biosemi_enaml.electrode_coords',
    'biosemi_enaml.electrode_selector',
    'biosemi_enaml.electrode_selector_view',
    'biosemi_enaml.modifier_button',
]
