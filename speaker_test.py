import numpy as np
import wave

# Parameters
sample_rate = 44100
frequency = 500  # Hz
duration = 10    # seconds
amplitude = 0.5  # 0.0 to 1.0

# Time vector
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate channels
left = np.zeros_like(t)  # silence
right = amplitude * np.sin(2 * np.pi * frequency * t)

# Interleave stereo channels
stereo = np.column_stack((left, right))

# Convert to 16-bit PCM
audio = (stereo * 32767).astype(np.int16)

# Write WAV file
with wave.open("right_500Hz.wav", "w") as wav:
    wav.setnchannels(2)
    wav.setsampwidth(2)  # 16-bit
    wav.setframerate(sample_rate)
    wav.writeframes(audio.tobytes())

print("Created right_500Hz.wav")
