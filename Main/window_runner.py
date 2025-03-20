import socket
import struct
import pickle
import cv2
import numpy as np
from cryptography.fernet import Fernet

def listener(ip, port):
    port = int(port)
    HOST = ip  
    PORT = port

    print(f"[*] Waiting for connection on {HOST}:{PORT}...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    conn, addr = server.accept()
    print(f"[+] Connection received from {addr}")

    # Receive the encryption key from the client
    key = conn.recv(1024)
    cipher = Fernet(key)

    data_buffer = b""
    payload_size = struct.calcsize("Q")

    while True:
        try:
            # Receive and accumulate packet data until we get the payload size
            while len(data_buffer) < payload_size:
                packet = conn.recv(4096)
                if not packet:
                    break
                data_buffer += packet

            packed_msg_size = data_buffer[:payload_size]
            data_buffer = data_buffer[payload_size:]

            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data_buffer) < msg_size:
                data_buffer += conn.recv(4096)

            encrypted_data = data_buffer[:msg_size]
            data_buffer = data_buffer[msg_size:]

            # Decrypt and deserialize the frame
            decrypted_data = cipher.decrypt(encrypted_data)
            frame = pickle.loads(decrypted_data)

            # Ensure frame is a valid 3D NumPy array
            if not isinstance(frame, np.ndarray) or len(frame.shape) != 3:
                print("[!] Received an invalid frame. Not a 3D NumPy array.")
                continue

            # Display the frame
            cv2.imshow(f"{addr} -> Screen", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f"[!] Error processing frame: {e}")
            break

    cv2.destroyAllWindows()
    conn.close()
    server.close()