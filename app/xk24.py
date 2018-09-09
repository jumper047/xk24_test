import struct

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import hidapi


class XK24(Qobject):

    keyboardDataReceived = pyqtSignal(object)

    def __init__(self):
        super(XK24, self).__init__()
        self.keyboard = None
        self.VID = 1523
        self.PID = 1029

    def connectToKeyboard(self):
        for device in hidapi.enumerate():
            if device.vendor_id == self.VID and device.product_id == self.PID:
                self.keyboard = device
                return True
        return False

    @pyqtSlot()
    def getKeysState(self):
        binreport = self.keyboard.read(33)
        report = struct.unpack('33B', binreport)
        self.keyboardDataReceived.emit(report[3:7])

    @pyqtSlot(int, int)
    def setBacklight(self, key, state):
        report = [0, 181, key, state] + [0] * 32
        binreport = struct.pack('36B', *report)
        self.keyboard.write(binreport, b'\x0b')
