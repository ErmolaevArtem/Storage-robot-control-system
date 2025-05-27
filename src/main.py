import time

from src.server_thread import WiFiServerThread
from queue import Queue

##filter_speech = threading.Thread()
##speech_recognition = threading.Thread()

if __name__ == "__main__":
    data_queue = Queue()
    server_thread = WiFiServerThread(data_queue)
    server_thread.start()
    time.sleep(2)
