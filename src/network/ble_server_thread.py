import asyncio
from bleak import BleakClient
from threading import Thread
from queue import Queue
import time

class BLEPacketAssemblerThread(Thread):
    def __init__(self, address: str, char_uuid: str, result_queue: Queue, timeout: float = 1.0):
        """
        :param address: BLE адрес устройства
        :param char_uuid: UUID характеристики с уведомлениями
        :param result_queue: очередь для завершённых пакетов
        :param timeout: таймаут бездействия (в секундах), после которого буфер считается завершённым пакетом
        """
        super().__init__()
        self.address = address
        self.char_uuid = char_uuid
        self.result_queue = result_queue
        self.timeout = timeout
        self._buffer = bytearray()
        self._last_rx_time = None
        self._stop_requested = False
        self.buf = 0
    def run(self):
        asyncio.run(self._main())

    async def _main(self):
        def handle_notification(sender, data: bytes):
            self.buf += len(data)
            self._buffer.extend(data)
            self._last_rx_time = time.time()

        try:
            async with BleakClient(self.address) as client:
                print(f"[BLE] Подключено к {self.address}")

                # 📏 Получение MTU (на Windows и Linux)
                try:
                    mtu = await client.get_mtu()
                    print(f"[BLE] Negotiated MTU: {mtu}")
                except Exception as e:
                    print(f"[BLE] Не удалось получить MTU: {e}")

                await client.start_notify(self.char_uuid, handle_notification)

                print(f"[BLE] Подписка активна")

                self._last_rx_time = time.time()

                while not self._stop_requested:
                    now = time.time()
                    if self._buffer and (now - self._last_rx_time) > self.timeout:
                        # Таймаут прошёл, пакет считается завершённым
                        self.result_queue.put(self._buffer[:])  # Копия
                        print(f"[BLE] Пакет размером {len(self._buffer)} байт передан в очередь")
                        self._buffer.clear()
                    await asyncio.sleep(0.1)

                await client.stop_notify(self.char_uuid)
                print("[BLE] Подписка остановлена")

        except Exception as e:
            self.result_queue.put(f"[BLE Error] {e}")

    def stop(self):
        self._stop_requested = True
