from PyQt5.QtCore import QEvent, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMenu, QPushButton, QSizePolicy


class VirtualKey(QPushButton):

    backlightChanged = pyqtSignal(int, int, int)

    def __init__(self,  number):
        super(VirtualKey, self).__init__(number)
        self.setSizePolicy(QSizePolicy.Minimum,
                           QSizePolicy.Minimum)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.installEventFilter(self)

        self.backlightMenu = QMenu()
        self.backlightMenu.addAction("Синий")
        self.backlightMenu.addAction("Красный")
        self.backlightMenu.addAction("Выкл.")

        self.customContextMenuRequested.connect(self.showBacklightMenu)
        self.backlightMenu.triggered.connect(self.processBacklight)

    @pyqtSlot(object)
    def showBacklightMenu(self, point):
        self.backlightMenu.popup(self.mapToGlobal(point))

    @pyqtSlot(object)
    def processBacklight(self, action):
        colors4Button = {"Синий": 'QPushButton {background-color: #4da6ff;}',
                         "Красный": 'QPushButton {background-color: #ff4d4d;}',
                         "Выкл.": ''}
        colors4USB = {"Синий": [1, 0], "Красный": [0, 1], "Выкл.": [0, 0]}
        key = self.text()
        color = action.text()
        self.setStyleSheet(colors4Button[action.text()])
        self.backlightChanged.emit(int(key), *colors4USB[action.text()])

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonDblClick) and event.button() == Qt.LeftButton:
            return True
        else:
            return super(VirtualKey, self).eventFilter(obj, event)
