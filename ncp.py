#!/usr/bin/env python3

import struct
import time

from PySide import QtCore

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


class HDLCPacket(object):
    """
    Implements a generic packet with command and data parameters.
    """
    FRAME_BOUNDARY = b'\x7e'
    ESCAPE = b'\x7d'

    def __init__(self, command=b'\x00', data=b''):
        """
        Implement HDLC compatible data packet.
        """
        self.command = command
        self.data = data

    def transmission_bytes(self):
        """
        Returns bytes suitable for sending over a serial device, including
        inserting the necessary frame boundaries and escaping frame boundary
        and escape characters as needed.
        """
        data = self.data.replace(b'\x7d', b'\x7d\x5d')
        data = data.replace(b'\x7e', b'\x7d\x5e')
        command = self.command.replace(b'\x7d', b'\x7d\x5d')
        command = command.replace(b'\x7e', b'\x7d\x5e')
        return (HDLCPacket.FRAME_BOUNDARY + command +
                data + HDLCPacket.FRAME_BOUNDARY)

    def __str__(self):
        return 'command: %0.2x, data: %s' % (
            self.command[0],
            ','.join([('0x%0.2x' % b) for b in self.data]))

    def __repr__(self):
        return '<%s %s command=0x%0.2x data=%s>' % (
            self.__class__.__name__, hex(id(self)), self.command[0],
            ','.join([('0x%0.2x' % b) for b in self.data]))


class NCPStepper(QtCore.QThread):
    """
    Implements interface to Thor APT TDC001 stepper motor.
    """

    MSG_HOMED = b'\x04\x44'
    MSG_MOVE_COMPLETED = b'\x04\x64'
    MSG_GET_POS = b'\x04\x12'
    MSG_GET_STEP_SIZE = b'\x04\x47'

    event = QtCore.Signal(object)

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


class NCPController(QtCore.QThread):
    """
    Interface to Neural Circuit Probe Controller.
    """
    GET_SETPOINT = b'\x20'
    SET_SETPOINT = b'\x21'
    GET_PGAIN = b'\x22'
    SET_PGAIN = b'\x23'
    GET_DEFLECTION = b'\x24'
    GET_STATE = b'\x25'
    GET_PIEZO_OUTPUT = b'\x26'
    GET_IGAIN = b'\x27'
    SET_IGAIN = b'\x28'
    START_SURFACE_SEARCH = b'\x30'
    WITHDRAW = b'\x31'
    ENGAGE_FAIL = b'\x40'
    ENGAGE_SUCCESS = b'\x41'
    HOLD_PIEZO = b'\x50'
    RELEASE_PIEZO = b'\x51'

    STATE_CONTROLLING = 0x01
    STATE_HOLDING = 0x03
    STATE_DISCONNECTED = 0x04

    state_desc = {STATE_HOLDING: 'Holding',
                  STATE_CONTROLLING: 'Controlling',
                  STATE_DISCONNECTED: 'Disconnected'}

    event = QtCore.Signal(object)

    def __init__(self, parent=None, port=None):
        super().__init__(parent)
        self._setpoint = 0
        self._pgain = 0.2
        self._igain = 0.2
        self._piezo_hold = False
        self._setpoint_update = False
        self._pgain_update = False
        self._igain_update = False
        self._piezo_hold_update = False
        self._signal = 0
        self._output = 0
        self._state = NCPController.STATE_CONTROLLING

        if port is None:
            # Try to find right port.
            for p in list_ports.comports():
                if 'FTDI' in p[2] or 'FTDI' in p[1]:
                    port = p[0]
                    break
            if port is None:
                # Couldn't find a suitable port.
                self.connected = False

        try:
            self.serial = serial.Serial(port,
                                        baudrate=115200,
                                        timeout=0.1)
            self.serial.flushInput()
            self.serial.flushOutput()
            self.connected = True
            self.set_initial_values()
        except:
            self.connected = False

        self._running = False

    def set_initial_values(self):
        self._send_packet(HDLCPacket(self.GET_STATE))
        self._send_packet(HDLCPacket(self.GET_PGAIN))
        self._send_packet(HDLCPacket(self.GET_IGAIN))

    def run(self):
        self._running = True
        while self._running:
            if self.connected:
                packet = self._get_packet()
                self._handle_packet(packet)
            else:
                self.event.emit(('state', NCPController.STATE_DISCONNECTED))
                time.sleep(0.1)

    def _handle_packet(self, packet):
        data = None
        event_type = None

        if packet is None:
            return

        if packet.command == NCPController.GET_SETPOINT:
            event_type = 'setpoint'
            data = self._get_float(packet)
        elif packet.command == NCPController.GET_PGAIN:
            event_type = 'pgain'
            data = self._get_float(packet)
        elif packet.command == NCPController.GET_IGAIN:
            event_type = 'igain'
            data = self._get_float(packet)
        elif packet.command == NCPController.GET_DEFLECTION:
            event_type = 'signal'
            data = self._get_float(packet)
        elif packet.command == NCPController.GET_PIEZO_OUTPUT:
            event_type = 'output'
            data = self._get_float(packet)
        elif packet.command == NCPController.GET_STATE:
            event_type = 'state'
            data = self._get_byte(packet)
        elif packet.command == NCPController.ENGAGE_FAIL:
            event_type = 'engage_fail'
        elif packet.command == NCPController.ENGAGE_SUCCESS:
            event_type = 'engage_success'

        self.event.emit((event_type, data))

    def _get_packet(self):
        packet = HDLCPacket()

        try:
            while self.serial.read(1) != HDLCPacket.FRAME_BOUNDARY:
                pass

            packet.command = self.serial.read(1)
            if len(packet.command) < 1:
                return HDLCPacket(b'\x00')

            while True:
                val = self.serial.read(1)
                if val == HDLCPacket.FRAME_BOUNDARY:
                    # Frame over
                    return packet
                elif val == HDLCPacket.ESCAPE:
                    val = self.serial.read(1)
                    packet.data += bytes([val[0] ^ (1 << 5)])
                else:
                    packet.data += val
            return packet
        except:
            # Probably a serial read error on exit.
            pass

    def _send_packet(self, packet):
        """
        Returns the packet's response.
        """
        try:
            self.serial.write(packet.transmission_bytes())
        except:
            self.connected = False
        return True

    def _set_float(self, command, value):
        packet = HDLCPacket(command, float32_to_bytes(value))
        self._send_packet(packet)

    def _get_float(self, packet):
        if len(packet.data) != 4:
            return 0
        return struct.unpack('<f', packet.data)[0]

    def _get_byte(self, packet):
        if len(packet.data) != 1:
            return 0
        return packet.data[0]

    def update(self):
        if self.connected:
            self._send_packet(HDLCPacket(NCPController.GET_PIEZO_OUTPUT))
            self._send_packet(HDLCPacket(NCPController.GET_DEFLECTION))
            self._send_packet(HDLCPacket(NCPController.GET_STATE))
            if self._pgain_update:
                self._set_float(NCPController.SET_PGAIN, self._pgain)
                self._pgain_update = False
            if self._igain_update:
                self._set_float(NCPController.SET_IGAIN, self._igain)
                self._igain_update = False
            if self._setpoint_update:
                self._set_float(NCPController.SET_SETPOINT, self._setpoint)
                self._setpoint_update = False
            if self._piezo_hold_update:
                if self._piezo_hold:
                    packet = HDLCPacket(NCPController.HOLD_PIEZO)
                else:
                    packet = HDLCPacket(NCPController.RELEASE_PIEZO)
                self._send_packet(packet)
                self._piezo_hold_update = False

    @property
    def state(self):
        return self._state

    @property
    def setpoint(self):
        return self._setpoint

    @setpoint.setter
    def setpoint(self, setpoint):
        self._setpoint = setpoint
        self._setpoint_update = True

    @property
    def pgain(self):
        return self._pgain

    @pgain.setter
    def pgain(self, pgain):
        self._pgain = pgain
        self._pgain_update = True

    @property
    def igain(self):
        return self._igain

    @igain.setter
    def igain(self, igain):
        self._igain = igain
        self._igain_update = True

    @property
    def signal(self):
        return self._signal

    @property
    def output(self):
        return self._output

    @property
    def piezo_hold(self):
        return self._piezo_hold

    @piezo_hold.setter
    def piezo_hold(self, hold):
        self._piezo_hold = hold
        self._piezo_hold_update = True

    def stop(self, wait=False):
        self._running = False
        self.connected = False
        try:
            self.serial.close()
        except AttributeError:
            pass
        if wait:
            self.wait()
