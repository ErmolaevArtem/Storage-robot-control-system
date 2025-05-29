import wave
import numpy as np


class WavModule:
    def __init__(self):
        self.num_channels = 1
        self.sample_width = 2
        self.frame_rate = 16000
        self.filename = '../audio_data/test.wav'
        self.data = []

    def write_wav_file(self, audio_data):
        with wave.open(self.filename, 'wb') as wav_file:
            wav_file.setnchannels(self.num_channels)  # Моно
            wav_file.setsampwidth(self.sample_width)  # 16 бит = 2 байта
            wav_file.setframerate(self.frame_rate)  # 16 кГц
            wav_file.writeframes(audio_data.tobytes())

    def read_wav_file(self):
        with wave.open(self.filename, 'rb') as wav_file:
            params = wav_file.getparams()
            frames = wav_file.readframes(params.nframes)

            # Преобразование в numpy array с правильным типом данных
            dtype = np.int16 if params.sampwidth == 2 else np.int8
            self.data = np.frombuffer(frames, dtype=dtype)
