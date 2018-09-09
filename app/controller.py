from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSignal, pyqtSlot


class Controller(QObject):

    setBacklightSignal = pyqtSignal(int, int)

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
        key_b = int(key)
        key_r = int(key) + 32
        if action == "Синий":
            action_b = 1
            action_r = 0
        elif action == "Красный":
            action_b = 0
            action_r = 1
        elif action == "Выкл.":
            action_b = 0
            action_r = 0
        self.setBacklightSignal.emit(key_b, action_b)
        self.setBacklightSignal.emit(key_r, action_r)

    @pyqtSlot(object)
    def setKeyboardState(self, data):
        keys_state = []
        for byte in data:
            for place in range(0, 6):
                keys_state.append(byte & 1 << place)

        for key, state in zip(self.vKeyboard.keys, keys_state):
            key.setDown(bool(state))
