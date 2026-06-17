import numpy as np
import wave
import subprocess
import tempfile
import os
import time

# ==========================================
# USER SETTINGS
# ==========================================

MODE = "both_0"
# Options:
# "left"
# "right"
# "both_0"
# "both_180"

START_FREQ = 10       # Hz
END_FREQ = 500        # Hz
STEP = 40             # Hz

TONE_DURATION = 5     # seconds
GAP_DURATION = 5      # seconds

AMPLITUDE = 0.9       # 0.0 to 1.0
SAMPLE_RATE = 44100

# Force playback through the 3.5 mm jack
AUDIO_DEVICE = "plughw:1,0"

# ==========================================

frequencies = list(range(START_FREQ, END_FREQ + 1, STEP))

print("\n========================================")
print("Experiment Starting")
print("========================================")
print("Mode:", MODE)
print("Frequencies:", frequencies)
print("Tone Duration:", TONE_DURATION, "seconds")
print("Gap Duration:", GAP_DURATION, "seconds")
print()

for freq in frequencies:

    print("\n========================================")
    print(f"Frequency: {freq} Hz")
    print("Tone ON")
    print("========================================")

    # Generate time vector
    t = np.linspace(
        0,
        TONE_DURATION,
        int(SAMPLE_RATE * TONE_DURATION),
        endpoint=False
    )

    # Generate tone
    tone = AMPLITUDE * np.sin(2 * np.pi * freq * t)

    # Select channel configuration
    if MODE == "left":
        left = tone
        right = np.zeros_like(tone)

    elif MODE == "right":
        left = np.zeros_like(tone)
        right = tone

    elif MODE == "both_0":
        left = tone
        right = tone

    elif MODE == "both_180":
        left = tone
        right = -tone

    else:
        raise ValueError(
            "Invalid MODE. Use left, right, both_0, or both_180."
        )

    # Interleave stereo channels
    stereo = np.column_stack((left, right))

    # Convert to 16-bit PCM
    audio = (stereo * 32767).astype(np.int16)

    # Create temporary WAV file
    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as tmp:
        filename = tmp.name

    # Write WAV file
    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)      # 16-bit
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio.tobytes())

    # Play through the 3.5 mm output
    subprocess.run(
        ["aplay", "-D", AUDIO_DEVICE, filename]
    )

    # Remove temporary file
    os.remove(filename)

    print(f"Silence for {GAP_DURATION} seconds...")
    time.sleep(GAP_DURATION)

print("\n========================================")
print("Experiment Complete.")
print("========================================")
