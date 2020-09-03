from time import sleep

from xArm import XArm, Servo
from pynput.keyboard import Listener, Key, KeyCode
from screen import clear

arm = XArm()


def on_press(key):
    servo_list = [
        arm.servos[6],
        arm.servos[2],
        arm.servos[1]
    ]
    linear_move = False
    rotation_move = False
    try:
        if key == Key.up:
            arm.z += 5
            linear_move = True
        if key == Key.down:
            arm.z -= 5
            linear_move = True
        if key == Key.left:
            arm.x -= 5
            linear_move = True
        if key == Key.right:
            arm.x += 5
            linear_move = True
        if key == KeyCode(char='w'):
            arm.theta += 1
            linear_move = True
        if key == KeyCode(char='s'):
            arm.theta -= 1
            linear_move = True
        if key == KeyCode(char='a'):
            servo_list[0].deg += 5
            rotation_move = True
        if key == KeyCode(char='d'):
            servo_list[0].deg -= 5
            rotation_move = True
        if key == KeyCode(char='q'):
            servo_list[1].deg -= 5
            rotation_move = True
        if key == KeyCode(char='e'):
            servo_list[1].deg += 5
            rotation_move = True
        if key == KeyCode(char='o'):
            servo_list[2].deg -= 20
            rotation_move = True
        if key == KeyCode(char='c'):
            servo_list[2].deg += 20
            rotation_move = True
        if key == Key.esc:
            exit(0)
        clear()
        if linear_move:
            arm.generate_position(arm.x, arm.z, arm.theta)
        if rotation_move:
            arm.move_to_pos(servo_list, 100)
    except ValueError:
        print('Cannot move there')


if __name__ == '__main__':
    arm = XArm()

    # Make up a move using servos
    servo_list = [
        Servo(id=1),
        Servo(id=2),
        Servo(id=3),
        Servo(id=4),
        Servo(id=5),
        Servo(id=6)
    ]

    # Set all positions to 0
    # Technically the 0 position for J2 (motor 5) is +90 degrees
    # So it looks like:
    #      //  \\
    #      \\M1//
    #  Wire( M2 -- Note M2 is facing towards the reader
    #  Wire( ||
    #        M3
    #  Wire( ||
    #        M4
    #  Wire( ||
    #      __M5__ -- Note M5 is facing towards the reader
    #      | M6 |
    ######################################
    for i, servo in enumerate(servo_list):
        servo.pos = arm.servos[i + 1].zeroPos

    # Move to 0
    arm.update()
    arm.move_to_pos(servo_list, 1000)
    sleep(2)

    # Get the positions of the servos
    try:
        arm.update()
    except ValueError as e:
        print('Current position not reachable')

    # Manual Control
    with Listener(on_press=on_press) as listener:
        listener.join()
