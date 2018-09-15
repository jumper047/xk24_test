from PyQt5.QtCore import QObject, QThread, QTimer


class Controller(QObject):

    def __init__(self, gui, keyboard):
        super(Controller, self).__init__()
        self.gui = gui
        self.keyboard = keyboard

        try:
            if not self.keyboard.initialize():
                self.gui.errWin.showError("Клавиатура не подключена")
                return None
        except IOError:
            self.gui.errWin.showError("Ошибка связи с клавиатурой")
            return None

        self.kbdPollThread = QThread()
        self.pollTimer = QTimer()

        for key in self.gui.keys:
            key.backlightChanged.connect(self.keyboard.setBacklight)
        self.keyboard.keyboardDataReceived.connect(self.gui.setKeysState)
        self.pollTimer.timeout.connect(self.keyboard.getKeysState)

        self.keyboard.moveToThread(self.thread)
        self.thread.start()
        self.timer.start(POLL_FREQUENCY)

        self.gui.show()
