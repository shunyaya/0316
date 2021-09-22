import librosa, librosa.display
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal.spectral import spectrogram

file = "media/tetest.wav"

# waveform
signal, sr = librosa.load(file, sr = 22050) #sr * T -> 22050 * T
# librosa.display.waveplot(signal, sr = sr)
# plt.xlabel('Time')
# plt.ylabel('Amplitude')
# plt.show()

# fft -> specture
fft = np.fft.fft(signal)

magnitude = np.abs(fft)
frequency = np.linspace(0, sr, len(magnitude))

left_frequency = frequency[:int(len(frequency)/2)]
left_magnitude= magnitude[:int(len(magnitude)/2)]

# plt.plot (left_frequency, left_magnitude)
# plt.xlabel('Frequency')
# plt.ylabel('Magnitude')
# plt.show()

# stft -> spectrogram
n_fft = 2048 # number of samples per fft
frame_length = 512

stft = librosa.core.stft(signal, hop_length = frame_length, n_fft = n_fft)
spectrogram = np.abs(stft)

log_spectrogram = librosa.amplitude_to_db(spectrogram) 

# librosa.display.specshow(log_spectrogram, sr=sr, hop_length=frame_length)
# plt.xlabel('Time')
# plt.ylabel('db')
# plt.colorbar()
# plt.show()

# MFCCs
MFCCs = librosa.feature.mfcc(signal, n_fft=n_fft, hop_length = frame_length, n_mfcc = 20)

librosa.display.specshow(MFCCs, sr=sr, hop_length=frame_length)
plt.xlabel('Time')
plt.ylabel('MFCC')
plt.colorbar()
plt.show()