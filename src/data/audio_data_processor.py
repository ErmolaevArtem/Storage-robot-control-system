import queue
import time
from threading import Thread


def audio_filter(data: bytearray) -> bytearray:
    return data


def data_converter(data: bytearray):
    return data


class AudioDataProcessingThread(Thread):
    def __init__(self, raw_data_queue: queue.Queue, data_queue: queue.Queue):
        super().__init__()
        self.is_work = True

        self.raw_data_queue = raw_data_queue
        self.data_queue = data_queue

        self._buffer = bytearray()
        self._last_rx_time = time.time()
        self.timeout = 1
        self.packet_is_ready = False

    def run(self):
        while self.is_work:
            if self.packet_is_ready:
                print(f"audio_data_processor: Получен пакет байт размером: {len(self._buffer)}")

                filtered_data = audio_filter(self._buffer)
                converted_data = data_converter(filtered_data)

                self.data_queue.put(bytes(converted_data))

                self._buffer.clear()
                self.packet_is_ready = False
            try:
                data = self.raw_data_queue.get_nowait()
                self._buffer.extend(data)
                self._last_rx_time = time.time()
            except queue.Empty:
                if self._buffer and (time.time() - self._last_rx_time) > self.timeout:
                    self.packet_is_ready = True

    def stop(self):
        self.is_work = False
        print("Поток преобразования сигнала остановлен")
