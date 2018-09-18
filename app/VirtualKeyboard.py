from PyQt5.QtCore import QThread, QTimer, pyqtSlot
from PyQt5.QtWidgets import QGridLayout, QWidget

from app.VirtualKey import VirtualKey


class VirtualKeyboard(QWidget):

    def __init__(self, keyboard):
        super(VirtualKeyboard, self).__init__()
        self.keyboard = keyboard
        self.initUi()

        for key in self.keys:
            key.backlightChanged.connect(self.setBacklight)
        self.keyboard.reportReceived.connect(self.setKeysState)

        self.show()

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
                keys_state.append(byte & 1 << place)

        for key, state in zip(self.keys, keys_state):
            key.setDown(bool(state))

    def setBacklight(self, key, blue, red):
        self.keyboard.backlightQueue.insert(0, [key, blue, red])

    def closeEvent(self, event):
        self.keyboard.closeConnection()
        self.keyboard.thread.wait(2000)
        super(VirtualKeyboard, self).closeEvent(event)
