import asyncio
from bleak import BleakClient
from threading import Thread
from queue import Queue


class BLENotifyThread(Thread):
    def __init__(self, address: str, char_uuid: str, result_queue: Queue, timeout: float = 10.0):
        super().__init__()
        self.address = address
        self.char_uuid = char_uuid
        self.result_queue = result_queue
        self.timeout = timeout
        self._stop_event = asyncio.Event()

    def run(self):
        asyncio.run(self._notification_task())

    async def _notification_task(self):
        def handle_notification(sender, data):
            print(f"[BLE] Notification from {sender}: {data}")
            self.result_queue.put(data)

        try:
            async with BleakClient(self.address) as client:
                print(f"[BLE] Подключено к {self.address}")

                await client.start_notify(self.char_uuid, handle_notification)
                print(f"[BLE] Подписка на {self.char_uuid} активирована")

                try:
                    await asyncio.wait_for(self._stop_event.wait(), timeout=self.timeout)
                except asyncio.TimeoutError:
                    print("[BLE] Таймаут подписки")

                await client.stop_notify(self.char_uuid)
                print("[BLE] Подписка завершена")

        except Exception as e:
            self.result_queue.put(f"[BLE Error] {e}")

    def stop(self):
        # Вызов из внешнего потока для остановки подписки до таймаута
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.call_soon_threadsafe(lambda: self._stop_event.set())
        else:
            self._stop_event.set()