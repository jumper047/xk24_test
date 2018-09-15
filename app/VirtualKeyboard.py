from PyQt5.QtCore import QThread, QTimer, pyqtSlot
from PyQt5.QtWidgets import QGridLayout, QWidget

from app.ErrorWindow import ErrorWindow
from app.VirtualKey import VirtualKey

POLL_FREQUENCY = 200


class VirtualKeyboard(QWidget):

    def __init__(self):
        super(VirtualKeyboard, self).__init__()
        self.initUi()
        self.errWin = ErrorWindow()

    def initUi(self):
        self.setWindowTitle("Тест клавиатуры XK24")
        self.setGeometry(400, 150, 200, 400)
        self.keys = []
        layout = QGridLayout()
        buttonNumber = 0
        for column in range(0, 4):
            for row in range(0, 6):
                key = VirtualKey(str(buttonNumber))
                self.keys.append(key)
                layout.addWidget(key, row, column)
                buttonNumber += 1
            buttonNumber += 2
        self.setLayout(layout)

    @pyqtSlot(object)
    def setKeysState(self, data):
        keys_state = []
        for byte in data:
            for place in range(0, 6):
                key_state.append(byte & 1 << place)

        for key, state in zip(self.keys, keys_state):
            key.setDown(bool(state))
