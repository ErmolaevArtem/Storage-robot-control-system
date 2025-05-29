import threading
import queue
import socket


class WiFiServerThread(threading.Thread):
    def __init__(self, queue_data: queue.Queue, ip: str = '192.168.4.1', port: int = 12345):
        super().__init__()
        self.sock = None
        self.is_work = True
        self.is_connection = False

        self.ip = ip
        self.port = port
        self.buffer_size: int = 2*1024

        self.queue = queue_data

    def run(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
            self.sock.listen(1)
            print("Подключено к ESP32")
            self.is_connection = True
        except Exception as e:
            print(f"Ошибка при подключении к ESP32: {e}")
            return

        while self.is_work:
            while self.is_connection:
                try:
                    data = self.sock.recv(self.buffer_size)
                    if data:
                        self.queue.put(data)
                except Exception as e:
                    print(f"Ошибка при получении данных: {e}")
                    self.is_connection = False
                    continue
                print(len(data))
            # здесь должна быть проверка на наличие соединения с выставлением self.is_work = False
            # чтобы заново перезайти в run и переподключиться

    def stop(self):
        self.is_work = False

        if self.sock:
            try:
                self.sock.close()
            except Exception as e:
                print(f"Ошибка при закрытии сокета: {e}")
        print("Остановлено")
