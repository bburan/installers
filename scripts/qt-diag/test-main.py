import os
import sys
import platform
import traceback


def print_env_info():
    print(f"Python:       {sys.version}")
    print(f"Executable:   {sys.executable}")
    print(f"Platform:     {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    print()
    print("--- sys.path ---")
    for p in sys.path:
        print(f"  {p}")
    print()
    relevant_vars = [
        'PATH', 'PYTHONPATH', 'PYTHONHOME',
        'QT_PLUGIN_PATH', 'QT_QPA_PLATFORM_PLUGIN_PATH',
        'QT_DEBUG_PLUGINS', 'QT_QPA_PLATFORM',
        'SYSTEMROOT', 'WINDIR',
    ]
    print("--- environment ---")
    for var in relevant_vars:
        val = os.environ.get(var)
        if val is not None:
            print(f"  {var}={val}")
    print()


def wait_for_keypress():
    print()
    input("Press Enter to exit...")


try:
    from PySide6 import QtCore, QtGui, QtWidgets
except Exception:
    print("=" * 60)
    print("FAILED to import PySide6")
    print("=" * 60)
    print()
    traceback.print_exc()
    print()
    print_env_info()
    wait_for_keypress()
    sys.exit(1)


class DiagWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt Diagnostic")
        layout = QtWidgets.QVBoxLayout(self)

        text = QtWidgets.QTextEdit()
        text.setReadOnly(True)
        text.setFontFamily("Courier New")
        text.setPlainText(self._gather_info())
        layout.addWidget(text)

        btn = QtWidgets.QPushButton("Close")
        btn.clicked.connect(self.close)
        layout.addWidget(btn)

        self.resize(640, 420)

    def _gather_info(self):
        lines = []
        lines.append(f"Python:           {sys.version}")
        lines.append(f"Platform:         {platform.platform()}")
        lines.append(f"Architecture:     {platform.machine()}")
        lines.append("")
        lines.append(f"Qt version:       {QtCore.qVersion()}")
        lines.append(f"PySide6 version:  {QtCore.__version__}")
        lines.append("")

        app = QtWidgets.QApplication.instance()
        screen = app.primaryScreen()
        geom = screen.geometry()
        lines.append(f"Platform plugin:  {app.platformName()}")
        lines.append(f"Screen:           {geom.width()}x{geom.height()} @ {screen.devicePixelRatio():.1f}x")
        lines.append(f"Screen name:      {screen.name()}")
        lines.append("")

        fmt = QtGui.QSurfaceFormat.defaultFormat()
        lines.append(f"OpenGL version:   {fmt.majorVersion()}.{fmt.minorVersion()}")
        lines.append(f"OpenGL profile:   {fmt.profile()}")

        return "\n".join(lines)


def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
        win = DiagWindow()
        win.show()
        sys.exit(app.exec())
    except Exception:
        print("=" * 60)
        print("FAILED to start Qt application")
        print("=" * 60)
        print()
        traceback.print_exc()
        print()
        print_env_info()
        wait_for_keypress()
        sys.exit(1)


if __name__ == '__main__':
    main()
