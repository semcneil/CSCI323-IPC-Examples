"""
messagePassing.py
====================================
This is an example of IPC.

| Author: Seth McNeill
| Date: 2026 September 11
"""

import time
import socket
from multiprocessing import Process


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 65432))
        s.listen()
        conn, _ = s.accept()
        with conn:
            data = conn.recv(1024)
            print(f"[Sockets] Server received: {data.decode()}")
            time.sleep(2)
            conn.sendall(b"Pong from Server")


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 65432))
        time.sleep(2)
        s.sendall(b"Ping from Client")
        response = s.recv(1024)
        print(f"[Sockets] Client received reply: {response.decode()}")


if __name__ == "__main__":
    p_server = Process(target=server)
    p_client = Process(target=client)

    p_server.start()
    p_client.start()

    p_client.join()
    p_server.join()