import numpy as np
import wave
import subprocess
import tempfile
import os
import time

# ==========================
# USER SETTINGS
# ==========================
MODE = "both_0"       # left, right, both_0, both_180

START_FREQ = 10       # Hz
END_FREQ = 500        # Hz
STEP = 40             # Hz

TONE_DURATION = 5     # seconds
GAP_DURATION = 5      # seconds

AMPLITUDE = 0.9       # 0 to 1
SAMPLE_RATE = 44100

# FORCE OUTPUT TO 3.5 mm JACK
AUDIO_DEVICE = "plughw:1,0"
# ==========================

subprocess.run(
    ["aplay", "-D", AUDIO_DEVICE, filename],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# ==========================

frequencies = list(range(START_FREQ, END_FREQ + 1, STEP))

print("\nExperiment Starting")
print("Mode:", MODE)
print("Frequencies:", frequencies)
print()

for freq in frequencies:

    print("=" * 40)
    print(f"Frequency: {freq} Hz")
    print("Tone ON")
    print("=" * 40)

    t = np.linspace(
        0,
        TONE_DURATION,
        int(SAMPLE_RATE * TONE_DURATION),
        endpoint=False
    )

    tone = AMPLITUDE * np.sin(2 * np.pi * freq * t)

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
        raise ValueError("Invalid MODE")

    stereo = np.column_stack((left, right))
    audio = (stereo * 32767).astype(np.int16)

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as tmp:

        filename = tmp.name

    with wave.open(filename, "w") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(audio.tobytes())

    subprocess.run(
        ["aplay", "-D", "plughw:1,0", filename],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    os.remove(filename)

    print(f"Silence for {GAP_DURATION} seconds...")
    time.sleep(GAP_DURATION)

print("\nExperiment Complete.")
