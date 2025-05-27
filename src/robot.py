import time

from src.gpio_controller import GPIOController


class Robot:
    def __init__(self):
        self.gpio_controller = GPIOController()

    def move_forward(self):
        self.gpio_controller.move_forward()
        time.sleep(10)
        self.gpio_controller.clean_up()

    def move_backward(self):
        ...

    def move_right(self):
        ...

    def move_left(self):
        ...

    def stop(self):
        self.gpio_controller.stop()

    def grab(self):
        ...