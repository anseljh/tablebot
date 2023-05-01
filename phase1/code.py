"""
Phase 1 TableBot with a Raspberry Pi Pico & 4 IR proximity sensors
"""

import time
import board
import digitalio
import pwmio
from adafruit_motor.motor import DCMotor

# Pico pinout & how to address pins:
# https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/pinouts

# PWM in CircuitPython:
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-pwm

# Reserve GP0 and GP1 for debug UART

# 4x IR proximity sensors
pin_front_left_ir = board.GP2
pin_front_right_ir = board.GP3
pin_rear_left_ir = board.GP4
pin_rear_right_ir = board.GP5
ir_pins = (pin_front_left_ir, pin_front_right_ir,
           pin_rear_left_ir, pin_rear_right_ir)
ir_front_left = digitalio.DigitalInOut(pin_front_left_ir)
ir_front_right = digitalio.DigitalInOut(pin_front_right_ir)
ir_rear_left = digitalio.DigitalInOut(pin_rear_left_ir)
ir_rear_right = digitalio.DigitalInOut(pin_rear_right_ir)
ir_sensors = (ir_front_left, ir_front_right, ir_rear_left, ir_rear_right)
for sensor in ir_sensors:
    sensor.direction = digitalio.Direction.INPUT

# Tactile swtiches
# pin_front_tactile = board.xx
# pin_rear_tactile = board.xx
# front_tactile = digitalio.DigitalInOut(pin_front_tactile)
# rear_tactile = digitalio.DigitalInOut(pin_rear_tactile)
# for tactile in (front_tactile, rear_tactile):
#     tactile.direction = digitalio.Direction.INPUT

# # TB6612FNG motor driver
pin_tb6612_ain1 = board.GP6
pin_tb6612_ain2 = board.GP7
pin_tb6612_bin1 = board.GP8
pin_tb6612_bin2 = board.GP9
pin_tb6612_stby = board.GP10
# pin_tb6612_pwma = board.GP11
# pin_tb6612_pwmb = board.GP12
tb6612_stby = digitalio.DigitalInOut(pin_tb6612_stby)
tb6612_stby.direction = digitalio.Direction.OUTPUT

# # tb6612 = TB6612(pin_tb6612_ain1, pin_tb6612_ain2, pin_tb6612_pwma,
# #                 pin_tb6612_bin1, pin_tb6612_bin2, pin_tb6612_pwmb, pin_tb6612_stby)
pwm_a1 = pwmio.PWMOut(pin_tb6612_ain1, frequency=5000, duty_cycle=0)
pwm_a2 = pwmio.PWMOut(pin_tb6612_ain2, frequency=5000, duty_cycle=0)
pwm_b1 = pwmio.PWMOut(pin_tb6612_bin1, frequency=5000, duty_cycle=0)
pwm_b2 = pwmio.PWMOut(pin_tb6612_bin2, frequency=5000, duty_cycle=0)
left_motor = DCMotor(pwm_a1, pwm_a2)
right_motor = DCMotor(pwm_b1, pwm_b2)
left_motor.throttle = None
right_motor.throttle = None

# 8-ohm speaker
SPEAKER_PIN = board.GP15
speaker = pwmio.PWMOut(SPEAKER_PIN, variable_frequency=True)
OFF = 0
ON = 2**15
GOOD_HZ = 500
BEEP_DURATION = 0.15


def disable_motors():
    tb6612_stby.value = False
    print("Disabled motors (set STBY to low)")


def enable_motors():
    tb6612_stby.value = True
    print("Enabled motors (set STBY to high)")


def motors_are_enabled():
    return tb6612_stby.value


def drive_forward(throttle: float = 0.5):
    left_motor.throttle = throttle
    right_motor.throttle = throttle


def drive_reverse(throttle: float = 0.5):
    left_motor.throttle = -1 * throttle
    right_motor.throttle = -1 * throttle


def turn_right(throttle: float = 0.5):
    left_motor.throttle = throttle
    right_motor.throttle = -1 * throttle


def turn_left(throttle: float = 0.5):
    left_motor.throttle = -1 * throttle
    right_motor.throttle = throttle


def drive_stop():
    left_motor.throttle = None
    right_motor.throttle = None
    stop_sound()


def read_proximity():
    return (ir_front_left.value, ir_front_right.value, ir_rear_left.value, ir_rear_right.value)


def stop_sound():
    dur = 0.002
    for y in range(1000, 20, -25):
        speaker.frequency = y
        speaker.duty_cycle = ON
        time.sleep(dur)
    speaker.duty_cycle = OFF


def beep(frequency: int = GOOD_HZ, duration: float = 0.2):
    speaker.frequency = frequency
    speaker.duty_cycle = ON
    time.sleep(duration)
    speaker.duty_cycle = OFF


def beep_times(n, frequency: int = GOOD_HZ, duration: float = 0.2):
    for x in range(n):
        beep(frequency, duration)
        time.sleep(duration)


def read_proximity():
    return (ir_front_left.value, ir_front_right.value, ir_rear_left.value, ir_rear_right.value)


def main_loop():
    disable_motors()

    print(f"Left motor: {left_motor}")
    print(f"Right motor: {right_motor}")

    beep_times(5, 1000, 0.1)

    enable_motors()

    print("Stopping")
    drive_stop()
    time.sleep(2)

    print("Forward!")
    drive_forward()
    beep()
    time.sleep(1)
    drive_stop()
    time.sleep(2)

    print("Reverse!")
    drive_reverse()
    beep()
    time.sleep(1)
    drive_stop()
    time.sleep(2)

    print("Left!")
    turn_left()
    beep()
    time.sleep(1)
    drive_stop()
    time.sleep(2)

    print("Right!")
    turn_right()
    beep()
    time.sleep(1)
    drive_stop()
    time.sleep(2)

    while True:
        # check sensors
        prox_readings = read_proximity()

        # output sensor state
        print(f"Front: L {prox_readings[0]}, R {prox_readings[1]}")
        print(f"Rear:  L {prox_readings[2]}, R {prox_readings[3]}")

        # decide what to do
        if sum(prox_readings) > 0:
            print("Got at least one true value from a sensor --> stopping!")
            drive_stop()
            # Beep for each sensor with a true value
            for i in range(4):
                if prox_readings[i]:
                    print(f"Sensor {i} triggered.")
                    beep_times(i+1, duration=0.1)
                    time.sleep(0.2)

        # output decision
        # do it
        pass


main_loop()
