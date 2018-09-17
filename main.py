#!/usr/bin/python3
import sys

from PyQt5.QtWidgets import QApplication

from app.FakeXK24 import FakeXK24
from app.VirtualKeyboard import VirtualKeyboard
from app.XK24 import XK24

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if "--demo" in sys.argv:
        keyboard = FakeXK24()
    else:
        keyboard = XK24()
    gui = VirtualKeyboard(keyboard)
    sys.exit(app.exec_())
