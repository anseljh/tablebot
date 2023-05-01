"""
sensor_test2
RPi Pico with 2 proximity sensors and a speaker
"""
import board
import digitalio
import time
import pwmio


ir_front_left = digitalio.DigitalInOut(board.GP2)
ir_front_right = digitalio.DigitalInOut(board.GP3)
ir_front_left.direction = digitalio.Direction.INPUT
ir_front_right.direction = digitalio.Direction.INPUT

# 8-ohm speaker
speaker = pwmio.PWMOut(board.GP15, variable_frequency=True)
OFF = 0
ON = 2**15
GOOD_HZ = 500
BEEP_DURATION = 0.15


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
    return (ir_front_left.value, ir_front_right.value)

def main_loop():

    print("Hello, world!")
    beep_times(5, 1000, 0.1)

    while True:
        print("Looping...")
        prox_readings = read_proximity()
        # output sensor state
        print(f"Front: L {prox_readings[0]}, R {prox_readings[1]}")

        # decide what to do
        if sum(prox_readings) > 0:
            print("Got at least one true value from a sensor!")
            for i in range(2):
                if prox_readings[i]:
                    print(f"Sensor {i} triggered.")
                    beep_times(i+1)
                    time.sleep(0.5)


main_loop()
