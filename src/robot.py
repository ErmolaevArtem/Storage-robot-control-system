import time

from gpio_controller import GPIOController


class Robot:
    def __init__(self):
        self.gpio_controller = GPIOController()

    def move(self, command_list):
        number_of_actions = command_list[0]
        actions = command_list[1:]
        for action in actions:
            if action == 'forward':
                self.move_forward()
            elif action == 'backward':
                self.move_backward()
            elif action == 'right':
                self.move_right()
            elif action == 'left':
                self.move_left()

    def move_forward(self):
        self.gpio_controller.move_forward()
        time.sleep(5)
        self.gpio_controller.stop()
        time.sleep(0.5)

    def move_backward(self):
        self.gpio_controller.move_backward()
        time.sleep(5)
        self.gpio_controller.stop()
        time.sleep(0.5)

    def move_right(self):
        self.gpio_controller.move_right()
        time.sleep(0.7)
        self.gpio_controller.stop()
        time.sleep(0.5)

    def move_left(self):
        self.gpio_controller.move_left()
        time.sleep(0.7)
        self.gpio_controller.stop()
        time.sleep(0.5)

    def stop(self):
        self.gpio_controller.stop()
        time.sleep(0.5)

    def grab(self):
        ...

    def finish(self):
        self.gpio_controller.clean_up()