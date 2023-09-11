Usage
-----

To use this script:

* Clone this repository.
* Install NSIS.
* Install Python 3.11+
* Run the script `python make-installer.py`.

This works by:

* Creating a virtual environment.
* Installing the latest version of the program (released on pypi) into the
  virtual environment.
* Using PyInstaller to create a stand-alone folder containing everything
  needed.
* Using NSIS to package up this folder into an installer. The installer will
  also create a start menu shortcut as well as an uninstaller that appears in
  the Windows Add/Remove program.
