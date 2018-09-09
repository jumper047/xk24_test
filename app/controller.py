from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSignal, pyqtSlot


class Controller(QObject):

    setBacklightSignal = pyqtSignal(object)

    def __init__(self, vKeyboard, errWinodw, hidObj):
        super(Controller, self).__init__()
        self.vKeyboard = vKeyboard
        self.errWindow = errWindow
        self.XK24 = hidObj
        self.thread = QThread()
        self.timer = QTimer()

        for button in self.errWindow.keys.values():
            button.backlightSelected.connect(self.setBacklight)
        self.XK24.keyboardDataReceived.connect(self.setKeyboardState)
        self.setBacklightSignal.connect(self.XK24.setBacklight)
        self.timer.timeout.connect(self.XK24.getKeysState)
        if not self.XK24.connectToKeyboard():
            self.errWindow.show()
        else:
            self.XK24.moveToThread(self.thread)
            self.thread.start()
            self.timer.start(200)

    @pyqtSlot(str, str)
    def setBacklight(self, key, action):
        self.setBacklightSignal.emit(data)

    @pyqtSlot(object)
    def setKeyboardState(self, data):
        pass
