import time

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

import hid

VID = 1523
PID = 1029
# VID = 49395
# PID = 673


class XK24(QObject):

    connected = pyqtSignal()
    finished = pyqtSignal()
    reportReceived = pyqtSignal(object)

    def __init__(self):
        super(XK24, self).__init__()
        self.waitingKeyboard = False
        self.pollingKeyboard = False
        self.backlightQueue = []
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.connect)
        self.connected.connect(self.runRWLoop)
        self.finished.connect(self.thread.quit)
        self.thread.start()

    @pyqtSlot()
    def connect(self):
        self.waitingKeyboard = True
        while self.waitingKeyboard:
            for device in hid.enumerate():
                if device["product_id"] == PID and device["vendor_id"] == VID:
                    self.keyboard = hid.device()
                    self.keyboard.open(VID, PID)
                    self.connected.emit()
                    return None
            time.sleep(1)
        self.finished.emit()

    @pyqtSlot()
    def runRWLoop(self):
        self.pollingKeyboard = True
        while self.pollingKeyboard:
            inputReport = self.keyboard.read(33, 250)
            if inputReport:
                self.reportReceived.emit(inputReport[2:8])
            if len(self.backlightQueue) > 0:
                key, blue, red = self.backlightQueue.pop()
                self.keyboard.write([0, 181, key, blue] + [0] * 32)
                self.keyboard.write([0, 181, key + 32, red] + [0] * 32)
        self.keyboard.close()
        self.finished.emit()

    def closeConnection(self):
        self.pollingKeyboard = False
        self.waitingKeyboard = False
