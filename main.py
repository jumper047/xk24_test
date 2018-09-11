#!/usr/bin/python3

import sys

from PyQt5.QtWidgets import QApplication

from app.controller import Controller
from app.vkeyboard import NoKeyboardWindow, VirtualKeyboard
from app.xk24 import XK24

if __name__ == "__main__":
    app = QApplication(sys.argv)
    vk = VirtualKeyboard()
    nk = NoKeyboardWindow()
    xk24 = XK24()
    controller = Controller(vk, nk, xk24)
    sys.exit(app.exec_())
