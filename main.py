from time import sleep
from ESCController import ESCController
from WebController import WebController

PIN_NUMBER = 4


def read_controller_values():
    # TODO Add actual reading of value from joystick
    desired_speed = input("Gimme: ")
    return desired_speed


if __name__ == "__main__":
    controller = ESCController(PIN_NUMBER)
    server = WebController()
    server.run()
    # while True:
    #     desired_speed = read_controller_values()
    #     controller.change_motor_speed(desired_speed)
    #     sleep(1)
