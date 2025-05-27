import time
from queue import Queue

from src.robot import Robot
from src.network.ble_server_thread import BLENotifyThread

BLE_ADDRESS = '3C:71:BF:4D:B3:7A'
SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

##filter_speech = threading.Thread()
##speech_recognition = threading.Thread()

if __name__ == "__main__":
    data_queue = Queue()

    # robot = Robot()
    # robot.move_forward()

    # server_thread = WiFiServerThread(data_queue)
    # server_thread.start()

    ble_notify_thread = BLENotifyThread(BLE_ADDRESS, CHAR_UUID, data_queue, timeout=10)

    ble_notify_thread.start()

    print("[Main] Ожидаем уведомления от BLE...")
    while ble_notify_thread.is_alive():
        while not data_queue.empty():
            data = data_queue.get()
            print("[Main] Получено уведомление:", data)
        time.sleep(0.5)

    print("[Main] Подписка завершена.")