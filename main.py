#!/usr/bin/python3

import sys

from PyQt5.QtWidgets import QApplication

from app.vkeyboard import VirtualKeyboard

if __name__ == "__main__":
    app = QApplication(sys.argv)
    vk = VirtualKeyboard()
    sys.exit(app.exec_())
