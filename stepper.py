#!/usr/bin/env python3

import struct
import time

from PyQt4 import QtCore

import serial
from serial.tools import list_ports


def float32_to_bytes(float32_value):
    int_val = struct.unpack('!i', struct.pack('!f', float32_value))[0]
    return struct.pack('<i', int_val)


def limit(val, minimum, maximum):
    if val > maximum:
        return maximum
    elif val < minimum:
        return minimum
    else:
        return val


class ThorStepper(QtCore.QThread):
    """
    Implements interface to Thor APT TDC001 stepper motor.
    """

    MSG_HOMED = b'\x04\x44'
    MSG_MOVE_COMPLETED = b'\x04\x64'
    MSG_GET_POS = b'\x04\x12'
    MSG_GET_STEP_SIZE = b'\x04\x47'

    event = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, port=None):
        super().__init__(parent)
        self.counts_per_mm = 34304
        self.homed = False
        self._pos = 0
        self._step_size = 0

        if port is None:
            # Try to find right port.
            for p in list_ports.comports():
                if 'Thorlabs APT' in p[1] or '83823572' in p[2]:
                    port = p[0]
                    break
            if port is None:
                self.connected = False
                return

        try:
            self.serial = serial.Serial(port,
                                        baudrate=115200,
                                        timeout=1)
            self.serial.flushInput()
            self.serial.flushOutput()
            self.set_initial_values()
            self.connected = True
        except:
            self.connected = False

        self._running = False
        time.sleep(0.1)

    def set_initial_values(self):
        step = 0.001
        counts = limit(int(step * self.counts_per_mm),
                       -self.counts_per_mm, self.counts_per_mm)
        self.serial.write(b'\x45\x04\x06\x00\x91\x01\x01\x00' +
                          struct.pack('<i', counts))
        self._step_size = step

    def run(self):
        self._running = True
        while self._running:
            event_type = None
            data = None
            if not self.connected:
                time.sleep(0.1)
                continue
            packet = self.serial.read(6)
            if len(packet) != 6:
                continue
            msg = packet[1::-1]  # first 2 bytes reversed

            if msg == self.MSG_HOMED:
                event_type = 'homed'
                self.homed = True
                data = True
            elif msg == self.MSG_MOVE_COMPLETED:
                event_type = 'move_completed'
                response = self.serial.read(14)
                data = struct.unpack('<i',
                                     response[2:6])[0] / self.counts_per_mm
                self._pos = data
            elif msg == self.MSG_GET_POS:
                event_type = 'pos'
                response = self.serial.read(6)
                data = struct.unpack('<i',
                                     response[-4:])[0] / self.counts_per_mm
                self._pos = data
            elif msg == self.MSG_GET_STEP_SIZE:
                event_type = 'step_size'
                data = struct.unpack('<i',
                                     response[-4:])[0] / self.counts_per_mm
                self._step_size = data

            self.event.emit((event_type, data))

    def home(self):
        """
        Home stage.
        """
        if not self.connected:
            return
        self.serial.write(b'\x43\x04\x00\x00\x11\x01')

    def identify(self):
        if not self.connected:
            return
        self.serial.write(b'\x23\x02\x00\x00\x11\x01')

    def step(self):
        if not self.connected:
            return
        self.serial.write(b'\x48\x04\x01\x00\x11\x01')

    def update(self):
        if not self.connected:
            return
        self.serial.write(b'\x11\x04\x01\x00\x11\x01')  # request pos

    @property
    def pos(self):
        """
        Returns the current position in mm.
        """
        return self._pos

    @pos.setter
    def pos(self, new_pos):
        """
        Moves stage to a new position given in mm.
        """
        if not self.connected:
            return None
        self.serial.flushInput()
        counts = int(limit(new_pos*self.counts_per_mm,
                           0, 12*self.counts_per_mm))
        self.serial.write(b'\x53\x04\x06\x00\x91\x01\x01\x00' +
                          struct.pack('<i', counts))

    @property
    def step_size(self):
        """
        Returns step size in mm.
        """
        return self._step_size

    @step_size.setter
    def step_size(self, step):
        """
        step : num
            Step size in mm. Limited to 1 mm max step size.
        """
        if not self.connected:
            return None
        # 34,304 counts/mm
        self._step_size = step
        counts = limit(int(step * self.counts_per_mm),
                       -self.counts_per_mm, self.counts_per_mm)
        self.serial.write(b'\x45\x04\x06\x00\x91\x01\x01\x00' +
                          struct.pack('<i', counts))

    def stop(self, wait=False):
        self._running = False
        self.connected = False
        try:
            self.serial.close()
        except AttributeError:
            pass
        if wait:
            self.wait()
