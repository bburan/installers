from importlib.resources import files

# The 'datas' variable is a list of tuples.
# Each tuple is (source_path, destination_in_bundle).
#
# files('my_package') reliably finds the installation directory of 'my_package'.
# We then convert it to a string for PyInstaller.
# The second part of the tuple, 'my_package', tells PyInstaller to create a
# folder named 'my_package' in the root of the bundle and copy the contents there.
datas = [
    (str(files('mne')), 'mne')
]

hiddenimports = [
    'decorator',
    'scipy.io',
]
