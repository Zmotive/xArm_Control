from cmd_datatypes import CmdTuple

SERVO_CMD_DICT = {
    'SERVO_MOVE_TIME_WRITE': CmdTuple(cmdVal=1, len=7, motorId=0),
    'SERVO_MOVE_TIME_READ': CmdTuple(cmdVal=2, len=3, motorId=0),
    'SERVO_MOVE_TIME_WAIT_WRITE': CmdTuple(cmdVal=7, len=7, motorId=0),
    'SERVO_MOVE_TIME_WAIT_READ': CmdTuple(cmdVal=8, len=3, motorId=0),
    'SERVO_MOVE_START': CmdTuple(cmdVal=11, len=3, motorId=0),
    'SERVO_MOVE_STOP': CmdTuple(cmdVal=12, len=3, motorId=0),
    'SERVO_ID_WRITE': CmdTuple(cmdVal=13, len=4, motorId=0),
    'SERVO_ID_READ': CmdTuple(cmdVal=14, len=3, motorId=254),
    'SERVO_ANGLE_OFFSET_ADJUST': CmdTuple(cmdVal=17, len=4, motorId=0),
    'SERVO_ANGLE_OFFSET_WRITE': CmdTuple(cmdVal=18, len=3, motorId=0),
    'SERVO_ANGLE_OFFSET_READ': CmdTuple(cmdVal=19, len=3, motorId=0),
    'SERVO_ANGLE_LIMIT_WRITE': CmdTuple(cmdVal=20, len=7, motorId=0),
    'SERVO_ANGLE_LIMIT_READ': CmdTuple(cmdVal=21, len=3),
    'SERVO_VIN_LIMIT_WRITE': CmdTuple(cmdVal=22, len=7),
    'SERVO_VIN_LIMIT_READ': CmdTuple(cmdVal=23, len=3),
    'SERVO_TEMP_MAX_LIMIT_WRITE': CmdTuple(cmdVal=24, len=4),
    'SERVO_TEMP_MAX_LIMIT_READ': CmdTuple(cmdVal=25, len=3),
    'SERVO_TEMP_READ': CmdTuple(cmdVal=26, len=3),
    'SERVO_VIN_READ': CmdTuple(cmdVal=27, len=3),
    'SERVO_POS_READ': CmdTuple(cmdVal=28, len=3),
    'SERVO_OR_MOTOR_MODE_WRITE': CmdTuple(cmdVal=29, len=7),
    'SERVO_OR_MOTOR_MODE_READ': CmdTuple(cmdVal=30, len=3),
    'SERVO_LOAD_OR_UNLOAD_WRITE': CmdTuple(cmdVal=31, len=4),
    'SERVO_LOAD_OR_UNLOAD_READ': CmdTuple(cmdVal=32, len=3),
    'SERVO_LED_CTRL_WRITE': CmdTuple(cmdVal=33, len=4),
    'SERVO_LED_CTRL_READ': CmdTuple(cmdVal=34, len=3),
    'SERVO_LED_ERROR_WRITE': CmdTuple(cmdVal=35, len=4),
    'SERVO_LED_ERROR_READ': CmdTuple(cmdVal=36, len=3)
}


def make_checksum(byte_array: bytearray) -> bytes:
    checksum = 0
    for value in byte_array:
        checksum += value
    checksum = 255 ^ ((checksum - 170) % 255)
    print(f'Checksum: {checksum}')
    return bytes([checksum])
