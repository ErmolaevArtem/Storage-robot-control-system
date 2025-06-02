import threading
import queue
import socket
import time


class WiFiServerThread(threading.Thread):
    def __init__(self, raw_data_queue: queue.Queue, status_queue: queue.Queue, ip: str = '192.168.4.1', port: int = 12345):
        super().__init__()
        self.sock = None
        self.is_work = True
        self.is_connection = False

        self.ip = ip
        self.port = port
        self.buffer_size: int = 2 * 1024

        self.queue = raw_data_queue
        self.status_queue = status_queue

    def run(self):
        while self.is_work:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.ip, self.port))
                self.sock.setblocking(False)
                print("Подключено к ESP32")
                self.is_connection = True
            except Exception as e:
                print(f"Ошибка при подключении к ESP32: {e}")
                continue

            while self.is_connection:
                try:
                    status = self.status_queue.get_nowait()
                    self.sock.send(status.encode())
                except queue.Empty:
                    pass

                try:
                    data = self.sock.recv(self.buffer_size)
                    if data:
                        self.queue.put(data)
                except BlockingIOError:
                    pass
                except Exception as e:
                    print(f"Ошибка при получении данных: {e}")
                    self.is_connection = False
                    continue

            self.sock.close()

    def stop(self):
        self.is_work = False

        if self.sock:
            try:
                self.sock.close()
            except Exception as e:
                print(f"Ошибка при закрытии сокета: {e}")
        print("Поток принятия сигналов остановлен")
