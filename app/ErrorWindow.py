import sys

from PyQt5.QtWidgets import QLabel, QPushButton, QtWidget, QVBoxLayout


class ErrorWindow(QWidget):

    def __init__(self, message):
        super(ErrorWindow, self).__init__()

        layout = QVBoxLayout()
        label = QLabel(message)
        button = QPushButton("Выход")
        layout.addWidget(label)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setGeometry(400, 150, 100, 100)

        button.clicked.connect(sys.exit)
        self.show()
