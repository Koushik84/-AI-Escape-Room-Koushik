"""
create_game_assets.py
Generates visual SVGs and web-audio sound effects for the escape room UI.
"""

import base64
import os
import wave
import struct
import math

# Generate audio wav files (Chime, Error buzzer, Key click)
def generate_wav(filepath, tone_seq, sample_rate=22050):
    """tone_seq: list of (freq_hz, duration_sec, amplitude)"""
    n_channels = 1
    sampwidth = 2
    frames = bytearray()
    
    for freq, duration, amp in tone_seq:
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = float(i) / sample_rate
            # Add subtle envelope
            envelope = math.sin(math.pi * (i / max(1, n_samples)))
            sample = int(amp * envelope * 32767.0 * math.sin(2.0 * math.pi * freq * t))
            frames.extend(struct.pack('<h', max(-32768, min(32767, sample))))
            
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sample_rate)
        wf.writeframes(frames)

def make_assets():
    os.makedirs("assets", exist_ok=True)
    
    # 1. Success chime (two ascending bells: 523Hz -> 659Hz -> 784Hz)
    generate_wav("assets/chime.wav", [(523.25, 0.15, 0.4), (659.25, 0.15, 0.4), (783.99, 0.35, 0.5)])
    
    # 2. Error buzzer (low buzz: 130Hz)
    generate_wav("assets/buzzer.wav", [(130.81, 0.2, 0.4), (110.0, 0.25, 0.4)])
    
    # 3. Mechanical click / lock turn
    generate_wav("assets/click.wav", [(1200, 0.03, 0.5), (600, 0.05, 0.3)])
    
    # 4. Victory fanfare (triumph arpeggio)
    generate_wav("assets/victory.wav", [(523.25, 0.15, 0.4), (659.25, 0.15, 0.4), (783.99, 0.15, 0.4), (1046.50, 0.6, 0.6)])

    print("Audio assets generated in assets/")

if __name__ == "__main__":
    make_assets()
