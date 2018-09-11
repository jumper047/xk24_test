import sys

from PyQt5.QtCore import QEvent, Qt, pyqtSignal
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QButtonGroup,
                             QGridLayout, QLabel, QMenu, QPushButton,
                             QSizePolicy, QVBoxLayout, QWidget)


class VirtualKeyboard(QWidget):

    def __init__(self):
        super(VirtualKeyboard, self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Тест клавиатуры XK24")
        self.setGeometry(400, 150, 200, 400)
        self.keys = []
        self.createKeyboardLayout()

    def createKeyboardLayout(self):
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


class VirtualKey(QPushButton):

    backlightSelected = pyqtSignal(str, str)

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

        self.colors = {"Синий": 'QPushButton {background-color: #4da6ff;}',
                       "Красный": 'QPushButton {background-color: #ff4d4d;}',
                       "Выкл.": ''}
        self.currentState = "Выкл."

    def showBacklightMenu(self, point):
        self.backlightMenu.popup(self.mapToGlobal(point))

    def processBacklight(self, action):
        key = self.text()
        color = action.text()
        if color != self.currentState:
            self.setStyleSheet(self.colors[action.text()])
            self.backlightSelected.emit(key, action.text())

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window2 = NoKeyboardWindow()
    window = VirtualKeyboard()
    window.show()
    window2.show()
    sys.exit(app.exec_())
