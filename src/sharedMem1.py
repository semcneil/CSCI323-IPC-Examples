"""
sharedMem1.py
====================================
This is an example of IPC.

| Author: Seth McNeill
| Date: 2026 September 11
"""

import time
from multiprocessing import Process
from multiprocessing.shared_memory import SharedMemory


def writer(shm_name):
    # Attach to existing shared memory segment
    shm = SharedMemory(name=shm_name)
    data = b"Hello from Writer process!"
    shm.buf[: len(data)] = data
    shm.close()


def reader(shm_name):
    shm = SharedMemory(name=shm_name)
    time.sleep(0.1)  # Brief wait for writer to write
    message = bytes(shm.buf[:26]).decode("utf-8")
    print(f"[Shared Memory] Reader received: {message}")
    shm.close()


if __name__ == "__main__":
    # Create a 64-byte shared memory block
    shm = SharedMemory(create=True, size=64)

    p1 = Process(target=writer, args=(shm.name,))
    p2 = Process(target=reader, args=(shm.name,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Clean up OS resources
    shm.close()
    shm.unlink()