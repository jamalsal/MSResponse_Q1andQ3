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
    sp_index = detectPeak(data) #Systolic peak detection
    plt.plot(data)
    plt.plot(sp_index, [data[i] for i in sp_index],"rx")
    plt.title("Raw signal with detected peaks")
    plt.show()
    segmented_signal = segmentBeat(data, sp_index)
    beat_length = calcBeatDuration(sp_index,fs)
    max_period = max(beat_length)*fs
    R = autoCorrelate(data, 10*math.ceil(max_period)) #Autocorrelation over one cycle
    plt.plot(R)
    plt.title("Autocorrelation")
    plt.show()

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

