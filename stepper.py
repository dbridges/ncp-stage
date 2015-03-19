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


class XYStage:
    """
    Implements interface to two Thor motors creating an x-y stage.
    """

    X_MOTOR_SN = '83823572'
    Y_MOTOR_SN = '83823570'

    def __init__(self, parent=None):
        self.parent = parent
        x_port = None
        y_port = None
        self._y = 0
        self._velocity = 0

        for p in list_ports.comports():
            if self.X_MOTOR_SN in p[2]:
                x_port = p[0]
            elif self.Y_MOTOR_SN in p[2]:
                y_port = p[0]
        if x_port is None:
            raise IOError('X motor not connected.')
        #if y_port is None:
            #raise IOError('Y motor not connected.')

        self.x_motor = ThorStepper(port=x_port)
        self.x_motor.event.connect(self.on_xMotor_event,
                                   QtCore.Qt.QueuedConnection)
        self.x_motor.start()

    @property
    def x(self):
        return self.x_motor.pos

    @x.setter
    def x(self, val):
        """
        val : float
            position in mm
        """
        self.x_motor.pos = limit(val, 0, 10)

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, val):
        self.x_motor.velocity = val

    def home(self):
        self.x_motor.home()

    def on_xMotor_event(self, event):
        event_type, data = event
        #if event_type == 'pos' or event_type == 'move_completed':
            #self.parent.on_xPos_changed(data)
        self.parent.on_xPos_changed(self.x_motor.pos)

    def update(self):
        self.x_motor.update()

    def stop(self):
        try:
            self.x_motor.stop()
            self.y_motor.stop()
        except:
            pass


class ThorStepper(QtCore.QThread):
    """
    Implements interface to Thor APT TDC001 stepper motor.
    """

    MSG_HOMED = b'\x04\x44'
    MSG_MOVE_COMPLETED = b'\x04\x64'
    MSG_MOVE_STOP = b'\x04\x66'
    MSG_GET_POS = b'\x04\x12'
    MSG_GET_STEP_SIZE = b'\x04\x47'

    event = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, port=None):
        super().__init__(parent)
        self.counts_per_mm = 34304
        self.homed = False
        self._pos = 0
        self._step_size = 0
        self._velocity = 0

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
            self.connected = True
            self.serial.flushInput()
            self.serial.flushOutput()
            self.set_initial_values()
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
        self.velocity = 30

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
            elif msg == self.MSG_MOVE_STOP:
                event_type = 'stop'
                response = self.serial.read(14)
                data = struct.unpack('<i',
                                     response[2:6])[0] / self.counts_per_mm
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

    def jog(self, direction):
        if not self.connected:
            return
        if direction == 'backward':
            self.serial.write(b'\x6a\x04\x01\x01\x11\x01')
        else:
            self.serial.write(b'\x6a\x04\x01\x02\x11\x01')

    def stop_move(self):
        if not self.connected:
            return
        self.serial.write(b'\x65\x04\x01\x02\x11\x01')

    def start_move(self, direction):
        if not self.connected:
            return
        if direction == 'backward':
            self.serial.write(b'\x57\x04\x01\x01\x11\x01')
        else:
            self.serial.write(b'\x57\x04\x01\x02\x11\x01')

    def start_status(self):
        self.serial.write(b'\x11\x00\x01\x00\x11\x01')

    def stop_status(self):
        self.serial.write(b'\x12\x00\x00\x00\x11\x01')

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

    @property
    def velocity(self):
        return self._v

    @velocity.setter
    def velocity(self, val):
        """
        val : float
            Velocity in mm/s
        """
        if not self.connected:
            return None
        v = struct.pack('<L', int(val * self.counts_per_mm))
        self.serial.write(b'\x13\x04\x0E\x00\x91\x01\x01\x00' +
                          struct.pack('<L', 0) + struct.pack('<L', 180000) + v)

    def stop(self, wait=False):
        self._running = False
        self.connected = False
        try:
            self.serial.close()
        except AttributeError:
            pass
        if wait:
            self.wait()
