from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import hidapi


class XK24(Qobject):

    keyboardDataReceived = pyqtSignal(object)

    def __init__(self):
        super(XK24, self).__init__()

    @pyqtSlot()
    def getKeysState(self):
        self.keyboardDataReceived.emit(data)

    @pyqtSlot()
    def setBackLight(self, button, state):
        pass
