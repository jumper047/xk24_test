import random

from PyQt5.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot


class FakeXK24(QObject):

    keyboardDataReceived = pyqtSignal(object)

    def __init__(self, vid=0, pid=0):
        super(FakeXK24, self).__init__()
        self.VID = vid
        self.PID = pid
        self.report = []

    def initialize(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateData)
        self.timer.start(10000)
        return True

    @pyqtSlot()
    def updateData(self):
        report = []
        for nbyte in range(0, 4):
            byte = 0
            for nbit in range(0, 8):
                byte += random.randint(0, 1) << nbit
            report.append(byte)
        print(report)
        self.report = report

    @pyqtSlot()
    def getKeysState(self):
        self.keyboardDataReceived.emit(self.report)

    @pyqtSlot(int, int, int)
    def setBacklight(self, key, blue, red):
        return None
