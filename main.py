#!/usr/bin/python3
import sys

from PyQt5.QtWidgets import QApplication

from app.Controller import Controller
from app.VirtualKeyboard import VirtualKeyboard
from app.xk24 import XK24

if __name__ == "__main__":
    app = QApplication(sys.argv)
    keyboard = XK24()
    gui = VirtualKeyboard()
    controller = Controller(gui, keyboard)
    sys.exit(app.exec_())
