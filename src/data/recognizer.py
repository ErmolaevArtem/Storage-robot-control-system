import json
import queue
from threading import Thread

from vosk import Model, KaldiRecognizer


class Recognizer(Thread):
    def __init__(self, data_queue: queue.Queue, command_queue: queue.Queue, status_queue: queue.Queue):
        super().__init__()
        self.length_frame = 4000
        self.model = Model("src/vosk-model-small-ru")

        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.recognizer.SetWords(True)

        self.is_work = True
        self.data_queue = data_queue
        self.command_queue = command_queue
        self.status_queue = status_queue

        self.commands = {
            'forward': ("вперёд", "перед"),
            'backward': ("назад"),
            'right': ("направо", "вправо", "право", "права", "справа"),
            'left': ("налево", "влево", "лево", "слева"),
            'stop': ('стоп'),
        }

    def run(self):
        while self.is_work:
            try:
                data = self.data_queue.get_nowait()
                print(f"recognizer: Получен пакет байт размером: {len(data)}")

                words = self.recognition(data)
                print(f'Распознанные слова: {words}')

                commands = self.convert(words)

                if len(commands) != 0:
                    self.command_queue.put(commands)
                else:
                    self.status_queue.put('n')

            except queue.Empty:
                pass

    def stop(self):
        self.is_work = False
        print("Поток распознавания речи остановлен")

    def recognition(self, audio_data: bytes) -> list:
        frames = int(len(audio_data) / self.length_frame)
        words: list = []

        for i in range(frames):
            if self.recognizer.AcceptWaveform(audio_data[i * self.length_frame:(i + 1) * self.length_frame]):
                # Парсим JSON-ответ и добавляем текст в массив
                result = json.loads(self.recognizer.Result())
                if 'text' in result and result['text']:
                    words.append(result['text'])

        # Добавляем последний фрагмент (FinalResult)
        final_result = json.loads(self.recognizer.FinalResult())
        if 'text' in final_result and final_result['text']:
            words.append(final_result['text'])

        # Разбиваем все фразы на отдельные слова
        return [word for phrase in words for word in phrase.split()]

    def convert(self, words_list: list) -> list:
        command_list: list = []

        for word in words_list:
            for command, variants in self.commands.items():
                if word in variants:
                    command_list.append(command)

        return command_list
