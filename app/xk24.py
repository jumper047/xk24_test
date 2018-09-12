import struct

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import hidapi


class XK24(QObject):

    keyboardDataReceived = pyqtSignal(object)

    def __init__(self):
        super(XK24, self).__init__()
        self.VID = 1523
        self.PID = 1029

    def initialize(self):
        for device in hidapi.enumerate():
            if device.vendor_id == self.VID and device.product_id == self.PID:
                self.keyboard = hidapi.Device(info=device)
                return True
        return False

    @pyqtSlot()
    def getKeysState(self):
        binreport = self.keyboard.read(33)
        report = struct.unpack('33B', binreport)
        self.keyboardDataReceived.emit(report[3:7])

    @pyqtSlot(int, int, int)
    def setBacklight(self, key, blue, red):
        report = [0, 181, key, blue] + [0] * 32
        binreport = struct.pack('36B', *report)
        self.keyboard.write(binreport, b'\x0b')
        report = [0, 181, key + 32, red] + [0] * 32
        binreport = struct.pack('36B', *report)
        self.keyboard.write(binreport, b'\x0b')
