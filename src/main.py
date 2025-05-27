import time
from queue import Queue

from src.robot import Robot
from src.network.ble_server_thread import BLEPacketAssemblerThread

BLE_ADDRESS = '3C:71:BF:4D:B3:7A'
CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

##filter_speech = threading.Thread()
##speech_recognition = threading.Thread()

if __name__ == "__main__":
    data_queue = Queue()

    # robot = Robot()
    # robot.move_forward()

    # server_thread = WiFiServerThread(data_queue)
    # server_thread.start()

    result_queue = Queue()
    ble_thread = BLEPacketAssemblerThread(
        address=BLE_ADDRESS,
        char_uuid=CHAR_UUID,
        result_queue=data_queue,
        timeout=2.0  # Если нет новых данных 2 сек — считаем пакет завершённым
    )

    ble_thread.start()

    try:
        while True:
            while not data_queue.empty():
                data = data_queue.get()
                if isinstance(data, bytes) or isinstance(data, bytearray):
                    print(f"[Main] Получен завершённый пакет ({len(data)} байт):", data)
                else:
                    print(f"[Main] Ошибка: {data}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[Main] Завершение...")
        ble_thread.stop()
        ble_thread.join()