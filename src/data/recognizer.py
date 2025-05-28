import wave
import json
from vosk import Model, KaldiRecognizer


def recognizer(audio_path, model_path="vosk-model-small-ru"):

    # Загружаем модель
    model = Model(model_path)

    # Открываем аудиофайл
    with wave.open(audio_path, "rb") as wf:
        # Проверяем формат аудио (моно, 16 kHz, 16 бит)
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            raise ValueError("Аудиофайл должен быть в формате WAV: моно, 16 бит, без сжатия.")

        recognizer = KaldiRecognizer(model, wf.getframerate())
        recognizer.SetWords(True)  # Включаем режим вывода слов

        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                # Парсим JSON-ответ и добавляем текст в массив
                result = json.loads(recognizer.Result())
                if 'text' in result and result['text']:
                    results.append(result['text'])

        # Добавляем последний фрагмент (FinalResult)
        final_result = json.loads(recognizer.FinalResult())
        if 'text' in final_result and final_result['text']:
            results.append(final_result['text'])

        # Разбиваем все фразы на отдельные слова
        return [word for phrase in results for word in phrase.split()]