"""
sharedMem2Fixed.py
====================================
This is an example of IPC.

| Author: Seth McNeill
| Date: 2026 September 11
"""

import time
from multiprocessing import Process
from multiprocessing.shared_memory import SharedMemory


def writer(shm_name):
    shm = SharedMemory(name=shm_name)
    data = b"Hello from Writer process with dynamic length! and now there is more"
    data_length = len(data)

    # Store length in the first 4 bytes (big-endian integer)
    shm.buf[:4] = data_length.to_bytes(4, byteorder="big")
    # Store payload right after the header
    shm.buf[4 : 4 + data_length] = data

    shm.close()


def reader(shm_name):
    shm = SharedMemory(name=shm_name)
    time.sleep(0.1)

    # Read the first 4 bytes to determine the dynamic payload length
    data_length = int.from_bytes(shm.buf[:4], byteorder="big")
    # Extract only the written bytes
    message = bytes(shm.buf[4 : 4 + data_length]).decode("utf-8")

    print(f"[Dynamic Read] Reader read {data_length} bytes: '{message}'")
    shm.close()


if __name__ == "__main__":
    shm = SharedMemory(create=True, size=128)

    p1 = Process(target=writer, args=(shm.name,))
    p2 = Process(target=reader, args=(shm.name,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    shm.close()
    shm.unlink()