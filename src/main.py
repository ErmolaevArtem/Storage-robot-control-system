import time
from queue import Queue

from src.robot.robot import RobotControl
from src.network.server_thread import WiFiServerThread
from src.data.audio_data_processor import AudioDataProcessingThread
from src.data.recognizer import Recognizer


if __name__ == "__main__":
    raw_data_queue = Queue()
    data_queue = Queue()
    command_queue = Queue()
    status_queue = Queue()

    server_thread = WiFiServerThread(raw_data_queue, status_queue)
    processing_thread = AudioDataProcessingThread(raw_data_queue, data_queue)
    recognizer = Recognizer(data_queue, command_queue, status_queue)
    robot = RobotControl(command_queue)

    try:
        server_thread.start()
        processing_thread.start()
        recognizer.start()
        robot.start()

        while True:
            time.sleep(1)

    except Exception as e:
        print(e)

    finally:
        server_thread.stop()
        processing_thread.stop()
        recognizer.stop()
        robot.stop()

        server_thread.join()
        processing_thread.join()
        recognizer.join()
        robot.join()

        print('Все потоки остановлены. Программа завершена.')
