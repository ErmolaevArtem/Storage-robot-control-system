import time
import queue
from threading import Thread

from src.robot.gpio_controller import GPIOController


class RobotControl(Thread):

    def __init__(self, command_queue: queue.Queue):
        super().__init__()
        self.gpio_controller = GPIOController()
        self.gpio_controller.set_up()
        self.is_work = True

        self.command_queue = command_queue

        self.movements = {
            'forward': self.move_forward,
            'backward': self.move_backward,
            'right': self.move_right,
            'left': self.move_left,
            'stop': self.stop_move,
        }

    def run(self):
        while self.is_work:
            try:
                commands = self.command_queue.get_nowait()
                print(f'Полученные команды: {commands}')

                for command in commands:
                    self.movements.get(command, self.command_not_found)()

            except queue.Empty:
                pass

    def stop(self):
        self.is_work = False
        self.gpio_controller.clean_up()
        print('Поток робота отключён')

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

    def command_not_found(self):
        print('Command not found')

    def stop_move(self):
        self.gpio_controller.stop()
        time.sleep(0.5)

    def grab(self):
        ...
