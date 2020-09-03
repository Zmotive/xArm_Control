import logging
import math
from typing import List, Type
import serial
from dataclasses import dataclass
from cmd_datatypes import CmdTuple


LSC_CMD_DICT = {
    'CMD_SERVO_MOVE': CmdTuple(cmdVal=3, len=2),
    'CMD_ACTION_GROUP_RUN': CmdTuple(cmdVal=6, len=2),
    'CMD_ACTION_STOP': CmdTuple(cmdVal=7, len=2),
    'CMD_ACTION_SPEED': CmdTuple(cmdVal=11, len=2),
    'CMD_GET_BATTERY_VOLTAGE': CmdTuple(cmdVal=15, len=2),
    'CMD_MULTI_SERVO_POWER_OFF': CmdTuple(cmdVal=20, len=2),
    'CMD_MULTI_SERVO_POS_READ': CmdTuple(cmdVal=21, len=2, has_callback=True),
}


@dataclass
class Servo:
    id: int = 0
    lastPos: int = 0
    zeroPos: int = 500
    _pos: int = 0
    _deg: float = 0
    direction: str = ''

    @property
    def pos(self) -> int:
        return int(self._pos)

    @pos.setter
    def pos(self, value: int) -> None:
        if value > 1000 or value < 0:
            raise ValueError(f'Position out of range. ID: {self.id}, Value: {value}')
        self._deg = self._pos2deg(value - self.zeroPos)
        self._pos = int(value)
        logging.info(f'Servo ID: {self.id}, Pos: {self._pos}')

    @property
    def deg(self) -> float:
        return self._deg

    @deg.setter
    def deg(self, value: float) -> None:
        chk_pos = self._deg2pos(value) + self.zeroPos
        if chk_pos > 1000 or chk_pos < 0:
            raise ValueError(f'Position out of range. ID: {self.id}, Value: {value}')
        self._pos = chk_pos
        self._deg = value

    def _pos2deg(self, pos: int) -> float:
        return pos * 0.24

    def _deg2pos(self, deg: float) -> int:
        if self.direction == 'Negate+90':
            return int(((deg * -1) + 90) / 0.24)
        if self.direction == 'Normal-90':
            return int((deg - 90.0) / 0.24)
        if self.direction == 'Negate':
            return int((deg * -1) / 0.24)
        if not self.direction or self.direction == 'Normal':
            return int(deg / 0.24)


class XArm:
    def __init__(self, device: str = '/dev/ttyUSB0', timeout: int = 0.1):
        self.servos = [
            Servo(),
            Servo(),
            Servo(zeroPos=530),
            Servo(zeroPos=480),
            Servo(zeroPos=485, direction='Negate'),
            Servo(direction='Normal-90'),
            Servo(zeroPos=460)
        ]
        self.serial = serial.Serial(device, timeout=timeout)
        self.x = 200.0
        self.z = 100.0
        self.theta = 0.0

    def __del__(self):
        self.serial.close()

    header = b'\x55\x55'

    def make_cmd(self, cmd_dict_element: Type[CmdTuple], params: list) -> bytearray:
        command = cmd_dict_element.cmdVal
        b = self.header
        b += b'%b' % (cmd_dict_element.len + len(params)).to_bytes(1, byteorder='big')
        logging.debug(f'Params length: {len(params)}')
        b += b'%b' % command.to_bytes(1, byteorder='big')
        if params:
            b += bytes(params)
        return b

    def update(self):
        self.command_generator('CMD_MULTI_SERVO_POS_READ', [6, 1, 2, 3, 4, 5, 6])
        for servo in self.servos:
            servo.pos = servo.lastPos

    def move_to_pos(self, servos: List[Servo], ms_time: int):
        if ms_time > 65535:
            print(f'Time too large for move: {ms_time}')
            return
        move_list = bytearray()
        move_list.append(len(servos))
        move_list.extend(ms_time.to_bytes(2, 'little'))
        for servo in servos:
            move_list.append(servo.id)
            if servo.pos < 0 or servo.pos > 1000:
                print(f'Position {servo.id} is commanded out of range: {servo.pos}')
            move_list.extend(servo.pos.to_bytes(2, 'little'))
        self.command_generator('CMD_SERVO_MOVE', move_list)

    def _cmd_multi_servo_pos_read(self, byte_array: bytearray) -> None:
        num_of_servos = byte_array[4]
        for i in range(0, num_of_servos):
            servo_id = byte_array[5 + (i * 3)]
            angle = byte_array[6 + (i * 3)] + (byte_array[7 + (i * 3)] * 256)
            logging.debug(f'Servo ID: {servo_id}, Angle: {angle}')
            self.servos[servo_id].lastPos = angle
            self.servos[servo_id].id = servo_id

    def command_generator(self, cmd_name: str, params: list) -> None:
        logging.debug(f'serial port: {self.serial.name}')  # check which port was really used
        cmd_bytes = self.make_cmd(LSC_CMD_DICT[cmd_name], params)
        print(f'Command Bytes: {cmd_bytes}')
        self.serial.write(cmd_bytes)  # write a string
        cmd_bytes = self.serial.read(3)
        if cmd_bytes:
            length = cmd_bytes[-1] - 1
            logging.debug(f'Length: {length}')
            cmd_bytes += self.serial.read(length)
            print(f'Returned Message: {cmd_bytes}')
            if LSC_CMD_DICT[cmd_name].has_callback:
                getattr(self, '_' + cmd_name.lower())(cmd_bytes)
        else:
            logging.debug('No response')

    def current_position(self):
        d1 = 98  # mm
        d2 = 98  # mm
        d3 = 150  # mm
        a1 = self.servos[5].deg
        a2 = self.servos[4].deg
        a3 = self.servos[3].deg
        theta = a1 + a2 + a3
        x = (d1 * math.cos(math.radians(a1))) + (
                d2 * math.cos(math.radians(a1 + a2))) + (
                    d3 * math.cos(math.radians(a1 + a2 + a3)))
        z = (d1 * math.sin(math.radians(a1))) + (
                d2 * math.sin(math.radians(a1 + a2))) + (
                    d3 * math.sin(math.radians(a1 + a2 + a3)))
        print(f'Theta: {theta}, X: {x}, Z: {z}')
        self.generate_position(x, z, theta)

    def generate_position(self, x: float, z: float, theta: float):
        d1 = 98  # mm
        d2 = 98  # mm
        d3 = 150  # mm
        x3 = x - d3 * math.cos(math.radians(theta))
        z3 = z - d3 * math.sin(math.radians(theta))
        d13 = math.sqrt((x3 ** 2) + (z3 ** 2))
        a2 = math.degrees(2 * math.acos(d13 / (2 * d1))) * -1
        t3 = math.degrees(math.asin(z3 / d13))
        t2 = math.degrees(math.acos((d13 / 2) / d1))
        a1 = t2 + t3
        a3 = theta - a1 - a2
        print(f'A1: {a1}, A2: {a2}, A3: {a3}')
        servo_list = [
            self.servos[5],
            self.servos[4],
            self.servos[3],
        ]
        servo_list[0].deg = a1
        servo_list[1].deg = a2
        servo_list[2].deg = a3
        self.move_to_pos(servo_list, 100)
        print(f'P1: {self.servos[5].deg}, P2: {self.servos[4].deg}, P3: {self.servos[3].deg}')
