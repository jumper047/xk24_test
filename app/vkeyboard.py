from PyQt5.QtWidgets import QGridLayout, QPushButton, QSizePolicy, QWidget


class VirtualKeyboard(QWidget):

    def __init__(self):
        super(VirtualKeyboard, self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Тест клавиатуры XK24")
        self.createKeyboardLayout()
        self.setGeometry(400, 150, 200, 400)
        self.show()

    def createKeyboardLayout(self):
        layout = QGridLayout()
        buttonNumber = 0
        for column in range(0, 4):
            for row in range(0, 6):
                layout.addWidget(VirtualKey(
                    self, str(buttonNumber)), row, column)
                buttonNumber += 1
            buttonNumber += 2
        self.setLayout(layout)


class VirtualKey(QPushButton):

    def __init__(self, controller, number):
        super(VirtualKey, self).__init__(number)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # self.clicked.connect(controller.button_klicked)
