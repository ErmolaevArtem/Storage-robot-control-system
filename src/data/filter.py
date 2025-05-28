import numpy as np
from scipy.signal import wiener
from scipy.signal import butter, lfilter, medfilt
from numpy.fft import fft, ifft, fftfreq


def wiener_filter(audio_data, sample_rate=16000):
    # Оценка параметров шума (предполагаем, что первые N с - только шум)
    noise_segment = audio_data[:int(0.9 * sample_rate)]
    noise_power = np.mean(noise_segment ** 2)

    # Применение фильтра Винера
    filtered_data = wiener(audio_data, mysize=None, noise=noise_power)

    # Нормализация сигнала
    filtered_data = filtered_data / np.max(np.abs(filtered_data))

    return filtered_data


def butter_bandpass_filter(audio_data, sample_rate=16000):
    # Параметры полосового фильтра
    lowcut = 300.0  # Нижняя граница (Гц)
    highcut = 3400.0  # Верхняя граница (Гц)
    order = 2  # Порядок фильтра (чем выше, тем круче срез)
    nyquist = 0.5 * sample_rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(N=order, Wn=[low, high], btype='band')
    filtered_data = lfilter(b, a, audio_data)
    return filtered_data


def threshold_filter(audio_data):
    threshold = 0.07  # Порог, данные лежат в [-1; 1]
    filtered_data = np.where(np.abs(audio_data) > threshold, audio_data, 0)
    return filtered_data


def soft_bandpass_filter(audio_data, sample_rate=16000, low_cut=300, high_cut=3400, transition_width=300):
    n = len(audio_data)
    freqs = fftfreq(n, d=1 / sample_rate)
    abs_freq = np.abs(freqs)

    # Создание маски
    mask = np.ones_like(abs_freq)
    mask[abs_freq < low_cut - transition_width] = 0
    mask[abs_freq > high_cut + transition_width] = 0

    # Плавный подъём (нижний край)
    trans_low = (abs_freq >= low_cut - transition_width) & (abs_freq < low_cut + transition_width)
    mask[trans_low] = 0.5 * (1 + np.cos(np.pi * (abs_freq[trans_low] - low_cut) / transition_width))

    # Плавный спад (верхний край)
    trans_high = (abs_freq > high_cut - transition_width) & (abs_freq <= high_cut + transition_width)
    mask[trans_high] = 0.5 * (1 + np.cos(np.pi * (abs_freq[trans_high] - high_cut) / transition_width))

    # Преобразование сигнала
    spectrum = fft(audio_data)
    filtered_spectrum = spectrum * mask
    filtered_data = np.real(ifft(filtered_spectrum))

    # Нормализация
    filtered_data = filtered_data / np.max(np.abs(filtered_data))
    return filtered_data


def median_filter(audio_data):
    window_size = 3  # (3, 5, 7...)
    filtered_data = medfilt(audio_data, kernel_size=window_size)
    return filtered_data


def filtration(audio_data):
    filtered_data1 = soft_bandpass_filter(audio_data)
    filtered_data = median_filter(filtered_data1)
    return filtered_data
