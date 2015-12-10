"""
csgo-autoaccept

Automatically detects and clicks the accept button in CS:GO matchmaking lobbies.
"""

from __future__ import division

from services import mm as matchmaking

import ctypes
import sys
import webbrowser

from PySide.QtCore import *
from PySide.QtGui import *

__author__ = "James \"clug\" <clug@clug.xyz>"
__version__ = "1.0.0"


def click(x=False, y=False):
    if x and y:
        ctypes.windll.user32.SetCursorPos(int(x), int(y))
    ctypes.windll.user32.mouse_event(0x02 | 0x04, 0, 0, 0, 0)


class AutoAccept_GUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(AutoAccept_GUI, self).__init__(*args, **kwargs)

        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.accept_scan)

        self.initUI()
        self.show()

        if matchmaking.aero_enabled():
            self.warn_aero()

    def initUI(self):
        self.buttons = {}
        self.checkboxes = {}
        self.labels = {}
        self.layouts = {}
        self.widgets = {}

        self.setWindowTitle("AutoAccept")

        self.buttons["scan"] = QPushButton("&Scan")
        self.buttons["scan"].setCheckable(True)
        self.buttons["scan"].clicked[bool].connect(self.scan)

        self.buttons["help"] = QPushButton("&Help")
        self.buttons["help"].clicked.connect(self.help_info)
        self.layouts["buttons"] = QHBoxLayout()
        self.layouts["buttons"].addWidget(self.buttons["scan"])
        self.layouts["buttons"].addWidget(self.buttons["help"])

        """self.checkboxes["mm"] = QCheckBox("MM")
        self.checkboxes["esea"] = QCheckBox("ESEA")
        self.checkboxes["faceit"] = QCheckBox("FaceIT")

        self.layout["checkboxes"] = QHBoxLayout()
        for box in self.checkboxes:
            self.layout["checkboxes"].addWidget(self.checkboxes[box])"""

        self.labels["status"] = QLabel("<center>Scan is not running.</center>")

        self.layouts["main"] = QVBoxLayout()
        self.layouts["main"].addLayout(self.layouts["buttons"])
        #self.layouts["main"].addLayout(self.layout["checkboxes"])
        self.layouts["main"].addWidget(self.labels["status"])
        self.widgets["main"] = QWidget()
        self.widgets["main"].setLayout(self.layouts["main"])

        self.setCentralWidget(self.widgets["main"])

    def accept_scan(self):
        found = matchmaking.get_accept()
        if found:
            self.scan(False)
            click(*found)
            self.set_status("Found accept button.")

    def scan(self, on):
        if on:
            if not matchmaking.exists():
                self.warn_notrunning()
                on = False
            else:
                self.timer.start(1000)
                self.set_status("Scanning for accept button.")
        else:
            self.timer.stop()
            self.set_status("Scan is not running.")

        self.buttons["scan"].setChecked(on)

    def set_status(self, status):
        self.labels["status"].setText("<center>" + status + "</center>")

    def help_info(self):
        return webbrowser.open("http://github.com/clugg/csgo-autoaccept")

    def warn_aero(self):
        return QMessageBox.warning(self, "AutoAccept", "AutoAccept has detected that you have Windows Aero enabled. This will prevent the program from functioning properly if your game is not in windowed mode.", QMessageBox.Ok)

    def warn_notrunning(self):
        return QMessageBox.warning(self, "AutoAccept", "AutoAccept has detected that CS:GO is not running. Please launch CS:GO before starting a scan.", QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication([])
    gui = AutoAccept_GUI()
    sys.exit(app.exec_())
