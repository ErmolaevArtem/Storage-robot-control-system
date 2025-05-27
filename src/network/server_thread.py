import threading
import queue
import socket


class WiFiServerThread(threading.Thread):
    def __init__(self, queue_data: queue.Queue, ip: str = '0.0.0.0', port: int = 12345):
        super().__init__()
        self.is_work = True
        self.is_connection = False

        self.ip = ip
        self.port = port
        self.buffer_size: int = 16*1024

        self.queue = queue_data

    def run(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.ip, self.port))
            self.sock.listen(1)
            print(f"TCP сервер запущен на {self.ip}:{self.port}")
        except Exception as e:
            print(f"Ошибка при создании TCP сервера: {e}")
            return

        while self.is_work:
            print(f"[*] Ожидание подключения...")
            conn, addr = self.sock.accept()
            print(f"[+] Подключено: {addr}")
            self.is_connection = True

            with conn:
                while self.is_connection:
                    try:
                        data = self.sock.recv(self.buffer_size)
                        if data:
                            self.queue.put(data)
                    except Exception as e:
                        print(f"Ошибка при получении данных: {e}")
                        self.is_connection = False
                        continue

    def stop(self):
        self.is_work = False

        if self.sock:
            try:
                self.sock.close()
            except Exception as e:
                print(f"Ошибка при закрытии сокета: {e}")
        print("TCP сервер остановлен")
