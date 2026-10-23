import matplotlib.pyplot as plt
import statistics
import math
from pathlib import Path
import numpy as np

parentDir = Path(__file__).parent

def main():
    with open(parentDir.joinpath("Human_example_ppg.txt").resolve()) as myFile:
        data = myFile.read()
    
    data = list(map(float, data.split("\n")))
    fs = 100 #sampling frequency
    plt.plot(data)
    plt.show()
    data_noise = white_noise(data)
    filtered = bandpass(data_noise, 8, 0.5, fs, 5)
    data_peaks = detectPeak(filtered) #Systolic peak detection
    segmented_signal = segmentBeat(filtered, data_peaks)
    beat_length = calcBeatDuration(data_peaks,fs)
    max_period = max(beat_length)*fs
    normalised_signal = normalise(segmented_signal)
    R = autoCorrelate(normalised_signal, 10*math.ceil(max_period)) #Autocorrelation over one cycle
    plt.plot(R)
    plt.title("Autocorrelation")
    plt.show()

def white_noise(signal):
    noise = np.random.normal(0, 0.1, len(signal))
    noisy_signal = signal + noise
    return noisy_signal

def bandpass(data,ub,lb,fs,order):
    sos = signal.butter(order, [lb, ub], fs=fs, btype='bandpass', output='sos') #second order section
    filtered_signal = signal.sosfiltfilt(sos, data)
    return filtered_signal
def normalise(signal):
    signal_n = []
    for i in range(len(signal)):
        if len(signal[i]) > 1:
            mx = statistics.mean(signal[i])
            std = statistics.stdev(signal[i])
            for j in range(len(signal[i])):
                    signal_n.append((signal[i][j] - mx) / std)
        else:
            signal_n.append(None)

    return np.array(signal_n)

def detectPeak(signal):
    threshold = 0.70*max(signal) #minimum threshold for systolic peak detection
    index = 0
    peaks = []
    
    while index < len(signal):
        if (index == 0):
            index += 1
        elif (signal[index] >= signal[index-1] and signal[index] >= signal[index+1] and signal[index] >= threshold):
            peaks.append(index)
            index += 1
        else:
            index += 1
    return peaks

def segmentBeat(signal, peaks):#Segments continuous beat signal into a 2D array
    segments = []
    i = 0
    while i < len(peaks) - 1:
        segment = signal[peaks[i]: peaks[i + 1]]
        segments.append(segment)
        i += 1
    return segments


def calcBeatDuration(signal, fs):
    dy = np.diff(signal) #difference between consecutive beats
    dt = dy/fs #length of each beat
    return dt


def autoCorrelate(signal, max_lag):
    mx = statistics.mean(signal)
    n = len(signal)
    R = []

    for k in range(max_lag + 1):
        sum_1 = 0
        sum_2 = 0
        for i in range(n - k):
            sum_1 += (signal[i + k] - mx) * (signal[i] - mx)
            sum_2 += (signal[i] - mx) ** 2
        R.append(sum_1 / sum_2)

    return R

if __name__ == "__main__":
    main()

