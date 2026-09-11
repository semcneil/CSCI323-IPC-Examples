"""
sharedMem3Null.py
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
    # Append null byte delimiter
    data = b"Hello from Writer!" + b"\x00"
    shm.buf[: len(data)] = data
    shm.close()


def reader(shm_name):
    shm = SharedMemory(name=shm_name)
    time.sleep(0.1)

    # Search for the first null byte index
    raw_buf = bytes(shm.buf)
    null_index = raw_buf.find(b"\x00")

    if null_index != -1:
        message = raw_buf[:null_index].decode("utf-8")
        print(
            f"[Null Delimiter] Reader detected length {null_index}: '{message}'"
        )

    shm.close()


if __name__ == "__main__":
    shm = SharedMemory(create=True, size=64)

    p1 = Process(target=writer, args=(shm.name,))
    p2 = Process(target=reader, args=(shm.name,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    shm.close()
    shm.unlink()