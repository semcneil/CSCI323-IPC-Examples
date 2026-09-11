"""
pipesEx.py
====================================
This is an example of IPC.

| Author: Seth McNeill
| Date: 2026 September 11
"""

import time
from multiprocessing import Pipe, Process


def child_process(conn):
    time.sleep(5)
    msg = conn.recv()
    print(f"[Pipes] Child received: {msg}")
    conn.send("Acknowledged from Child")
    conn.close()


if __name__ == "__main__":
    parent_conn, child_conn = Pipe()

    p = Process(target=child_process, args=(child_conn,))
    p.start()

    parent_conn.send("Hello from Parent")
    print("Sent message to child")
    response = parent_conn.recv()
    print(f"[Pipes] Parent received reply: {response}")

    p.join()
