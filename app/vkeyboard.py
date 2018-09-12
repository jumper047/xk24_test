import sys

from PyQt5 import QtCore, QtWidgets

POLL_FREQUENCY = 200


class VirtualKeyboard(QtWidgets.QWidget):

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
        self.thread = QtCore.QThread()
        self.timer = QtCore.QTimer()
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
        layout = QtWidgets.QGridLayout()
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

    @QtCore.pyqtSlot(object)
    def setKeysState(self, data):
        keys_state = []
        for byte in data:
            for place in range(0, 6):
                key_state.append(byte & 1 << place)

        for key, state in zip(self.keys, keys_state):
            key.setDown(bool(state))


class VirtualKey(QtWidgets.QPushButton):

    backlightChanged = QtCore.pyqtSignal(int, int, int)

    def __init__(self,  number):
        super(VirtualKey, self).__init__(number)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                           QtWidgets.QSizePolicy.Minimum)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.installEventFilter(self)

        self.backlightMenu = QtWidgets.QMenu()
        self.backlightMenu.addAction("Синий")
        self.backlightMenu.addAction("Красный")
        self.backlightMenu.addAction("Выкл.")

        self.customContextMenuRequested.connect(self.showBacklightMenu)
        self.backlightMenu.triggered.connect(self.processBacklight)

        self.currentState = "Выкл."

    @QtCore.pyqtSlot(object)
    def showBacklightMenu(self, point):
        self.backlightMenu.popup(self.mapToGlobal(point))

    @QtCore.pyqtSlot(object)
    def processBacklight(self, action):
        colors4Button = {"Синий": 'QPushButton {background-color: #4da6ff;}',
                         "Красный": 'QPushButton {background-color: #ff4d4d;}',
                         "Выкл.": ''}
        colors4USB = {"Синий": [1, 0], "Красный": [0, 1], "Выкл.": [0, 0]}
        key = self.text()
        color = action.text()
        if color != self.currentState:
            self.setStyleSheet(self.colors4Button[action.text()])
            self.backlightChanged.emit(int(key), *colors4USB[action.text()])

    def eventFilter(self, obj, event):
        if event.type() in (QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick) and event.button() == QtCore.Qt.LeftButton:
            return True
        else:
            return super(VirtualKey, self).eventFilter(obj, event)


class ErrorWindow(QtWidgets.QWidget):

    def __init__(self, message):
        super(ErrorWindow, self).__init__()

        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel(message)
        button = QtWidgets.QPushButton("Выход")
        layout.addWidget(label)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setGeometry(400, 150, 100, 100)

        button.clicked.connect(sys.exit)
        self.show()
