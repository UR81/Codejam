import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import pygame
import time
import wave


# Function to find the dominant frequency in a signal
def find_dominant_frequency(signal, sample_rate):
    # Perform Fast Fourier Transform (FFT)
    spectrum = np.fft.fft(signal)

    # Get the corresponding frequencies
    frequencies = np.fft.fftfreq(len(signal), 1 / sample_rate)

    # Find the index of the maximum amplitude
    idx = np.argmax(np.abs(spectrum))

    # Return the corresponding frequency
    return np.abs(frequencies[idx])


# Function to record audio from the microphone
def record_audio(duration, sample_rate, save_path=None):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=1024)

    frames = []

    print("Recording...")

    for i in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert frames to a numpy array
    signal = np.frombuffer(b''.join(frames), dtype=np.int16)

    # Save to a WAV file if save_path is provided
    if save_path:
        with wave.open(save_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

    return signal


# Function to visualize the recorded audio signal
def plot_audio_signal(signal, sample_rate):
    time = np.arange(0, len(signal)) / sample_rate
    plt.plot(time, signal)
    plt.title("Recorded Audio Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.show()


# Function to generate a sine wave tone
def generate_tone(frequency, duration, sample_rate):
    t = np.arange(0, duration, 1 / sample_rate)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    # Convert to 2D array with a single channel
    return tone.reshape(-1, 1)


# Function to play a tone
def play_tone(frequency, duration, sample_rate):
    pygame.mixer.init()
    pygame.mixer.set_num_channels(1)  # Set the number of channels to 1 for mono sound

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)

    # Convert the array to a 2D array with a single column
    tone = tone.reshape(-1, 1)

    sound = pygame.sndarray.make_sound((tone * 32767).astype(np.int16))
    channel = sound.play()

    time.sleep(duration)  # Wait for the sound to finish playing
    pygame.mixer.quit()


def tuning_main():
    # Set the duration of the recording (in seconds)
    duration = 3 # 1 minute

    # Set the sample rate
    sample_rate = 44100

    # Set the path to save the recorded sound
    save_path = r'D:\codejam4\aryan_codejam\Codejam\Poo fighters\song.wav'

    # Record audio from the microphone and save to a file
    audio_signal = record_audio(duration, sample_rate, save_path)

    # Visualize the recorded audio signal
    plot_audio_signal(audio_signal, sample_rate)

    # Find the dominant frequency in the signal
    dominant_frequency = find_dominant_frequency(audio_signal, sample_rate)

    print(f"Dominant Frequency: {dominant_frequency} Hz")

    # Play a tone based on the tuning result

    # Print the path to the saved recording
    print(f"Recorded sound saved to: {save_path}")

if __name__ == '__main__':
    tuning_main()
