
from robot import Robot
from data.converter import convert


if __name__ == "__main__":
    robot = Robot()
    recognized_list = ['вперёд', 'назад', 'вправо', 'влево', 'вперёд', 'назад', 'вправо', 'влево']
    converted_list = convert(recognized_list)
    print(converted_list)
    robot.move(converted_list)
