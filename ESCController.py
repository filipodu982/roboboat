import sys
import pigpio


class ESCController:
    MIN_WIDTH = 700  # Pulse width in us
    MAX_WIDTH = 2000  # Pulse width in us
    PULSE_RANGE = MAX_WIDTH - MIN_WIDTH

    def __init__(self, pin_number):
        self.pi = pigpio.pi()  # Instance of pigpio class
        self.pin_number = pin_number  # Number of GPIO pin handling a motor

        if not self.pi.connected:
            sys.exit()

    def change_motor_speed(self, speed_percent):
        """Method which converts % of desired motor speed, to pulse width in us"""
        if speed_percent > 100:
            speed_percent = 100
        elif speed_percent < 0:
            speed_percent = 0

        desired_pulse_width = (speed_percent / 100) * self.PULSE_RANGE + self.MIN_WIDTH
        self.pi.set_servo_pulsewidth(self.pin_number, desired_pulse_width)

    def __del__(self):
        self.pi.set_servo_pulsewidth(self.pin_number, 0)
        self.pi.stop()
