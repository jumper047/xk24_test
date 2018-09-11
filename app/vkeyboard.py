import sys

from PyQt5.QtCore import QEvent, Qt, QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QButtonGroup,
                             QGridLayout, QLabel, QMenu, QPushButton,
                             QSizePolicy, QVBoxLayout, QWidget)


class VirtualKeyboard(QWidget):

    def __init__(self):
        super(VirtualKeyboard, self).__init__()
        self.keyboard = xk24
        try:
            if not self.keyboard.initialize():
                errWindow = NoKeyboardWindow("Клавиатура не подключена.")
                return None
        except IOError:
            errWindow = NoKeyboardWindow("Ошибка связи с клавиатурой")
            return None
        self.initUi()

        self.thread = QThread()
        self.timer = QTimer()
        for key in self.keys.values():
            key.backlightChanged.connect(self.keyboard.setBacklight)
        self.keyboard.keyboardDataReceived.connect(self.setKeyboardState)
        self.timer.timeout.connect(self.XK24.getKeysState)

        self.keyboard.moveToThread(self.thread)
        self.thread.start()
        self.timer.start(200)

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

    def setKeyboardState(self, data):
        keys_state = []
        for byte in data:
            for place in range(0, 6):
                key_state.append(byte & 1 << place)

        for key, state in zip(self.keys, keys_state):
            key.setDown(bool(state))


class VirtualKey(QPushButton):

    backlightChanged = pyqtSignal(int, int, int)

    def __init__(self,  number):
        super(VirtualKey, self).__init__(number)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.installEventFilter(self)

        self.backlightMenu = QMenu()
        self.backlightMenu.addAction("Синий")
        self.backlightMenu.addAction("Красный")
        self.backlightMenu.addAction("Выкл.")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showBacklightMenu)
        self.backlightMenu.triggered.connect(self.processBacklight)

        # self.
        self.currentState = "Выкл."

    def showBacklightMenu(self, point):
        self.backlightMenu.popup(self.mapToGlobal(point))

    def processBacklight(self, action):
        colors4Button = {"Синий": 'QPushButton {background-color: #4da6ff;}',
                         "Красный": 'QPushButton {background-color: #ff4d4d;}',
                         "Выкл.": ''}
        colors4USB = {"Синий": [1, 0], "Красный": [0, 1], "Выкл.": [0, 0]}
        key = self.text()
        color = action.text()
        if color != self.currentState:
            self.setStyleSheet(self.colors[action.text()])
            self.backlightChanged.emit(int(key), *colors4USB[action.text()])

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonDblClick)\
                and event.button() == Qt.LeftButton:
            return True
        else:
            return super(VirtualKey, self).eventFilter(obj, event)


class NoKeyboardWindow(QWidget):

    def __init__(self):
        super(NoKeyboardWindow, self).__init__()

        layout = QVBoxLayout()
        label = QLabel("Клавиатура не подключена")
        button = QPushButton("Выход")
        layout.addWidget(label)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setGeometry(400, 150, 100, 100)

        button.clicked.connect(sys.exit)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window2 = NoKeyboardWindow()
    window = VirtualKeyboard()
    window.show()
    window2.show()
    sys.exit(app.exec_())
