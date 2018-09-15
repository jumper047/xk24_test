from PyQt5.QtCore import QThread, QTimer, pyqtSlot
from PyQt5.QtWidgets import QGridLayout, QWidget

from app.ErrorWindow import ErrorWindow
from app.VirtualKey import VirtualKey

POLL_FREQUENCY = 200


class VirtualKeyboard(QWidget):

    def __init__(self, keyboard):
        super(VirtualKeyboard, self).__init__()
        self.keyboard = keyboard
        try:
            if not self.keyboard.initialize():
                self.err = ErrorWindow("Клавиатура не подключена.")
                return None
        except IOError:
            self.err = ErrorWindow("Ошибка связи с клавиатурой")
            return None

        self.initUi()
        self.thread = QThread()
        self.timer = QTimer()
        for key in self.keys:
            key.backlightChanged.connect(self.keyboard.setBacklight)
        self.keyboard.keyboardDataReceived.connect(self.setKeysState)
        self.timer.timeout.connect(self.keyboard.getKeysState)

        self.keyboard.moveToThread(self.thread)
        self.thread.start()
        self.timer.start(POLL_FREQUENCY)

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
        self.show()

    @pyqtSlot(object)
    def setKeysState(self, data):
        keys_state = []
        for byte in data:
            for place in range(0, 6):
                key_state.append(byte & 1 << place)

        for key, state in zip(self.keys, keys_state):
            key.setDown(bool(state))
