import sys

from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class ErrorWindow(QWidget):

    def __init__(self):
        super(ErrorWindow, self).__init__()

        layout = QVBoxLayout()
        self.label = QLabel()
        button = QPushButton("Выход")
        layout.addWidget(self.label)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setGeometry(400, 150, 100, 100)

        button.clicked.connect(sys.exit)

    def showError(self, message):
        self.label.setText(message)
        self.show()
