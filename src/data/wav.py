import wave


class WavModule:
    def __init__(self):
        self.num_channels = 1
        self.sample_width = 2
        self.frame_rate = 16000
        self.filename = '../audio_data/test.wav'

    def write_wav_file(self, audio_data):
        with wave.open(self.filename, 'wb') as wav_file:
            wav_file.setnchannels(self.num_channels)  # Моно
            wav_file.setsampwidth(self.sample_width)  # 16 бит = 2 байта
            wav_file.setframerate(self.frame_rate)  # 16 кГц
            wav_file.writeframes(audio_data.tobytes())