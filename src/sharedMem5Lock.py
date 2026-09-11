"""
sharedMem5Lock.py
====================================
This is an example of IPC.

| Author: Seth McNeill
| Date: 2026 September 11
"""

import time
from multiprocessing import Event, Lock, Process, Value
from multiprocessing.shared_memory import SharedMemory


def writer(
    writer_id,
    shm_name,
    lock,
    data_ready_event,
    completed_counter,
    total_writers,
):
    shm = SharedMemory(name=shm_name)
    message = f"[Writer {writer_id} payload] ".encode("utf-8")
    msg_len = len(message)

    print(f"[Writer {writer_id}] Attempting to acquire lock...")

    # Compete for lock; only one writer enters this block at a time
    with lock:
        print(f"  --> [Writer {writer_id}] Lock ACQUIRED. Writing...")

        # Read current offset stored in first 4 bytes
        current_offset = int.from_bytes(shm.buf[:4], byteorder="big")
        if current_offset == 0:
            current_offset = 4  # Reserve first 4 bytes for total length header

        # Write chunk and update offset header
        shm.buf[current_offset : current_offset + msg_len] = message
        new_offset = current_offset + msg_len
        shm.buf[:4] = new_offset.to_bytes(4, byteorder="big")

        print(
            f"  <-- [Writer {writer_id}] Write complete. Extended length to {new_offset} bytes. Releasing lock."
        )

    shm.close()

    # Safely increment completed writer counter
    with completed_counter.get_lock():
        completed_counter.value += 1
        # Check if this process was the final writer
        if completed_counter.value == total_writers:
            print(
                f"\n[Writer {writer_id}] I am the LAST writer! Setting data_ready_event."
            )
            data_ready_event.set()


def reader(shm_name, data_ready_event):
    shm = SharedMemory(name=shm_name)

    print("[Reader] Waiting for data_ready_event...")
    data_ready_event.wait()  # Blocks until the last writer calls set()

    # Read total length written from first 4 bytes
    total_length = int.from_bytes(shm.buf[:4], byteorder="big")
    combined_data = bytes(shm.buf[4:total_length]).decode("utf-8")

    print(f"\n[Reader] Event received! Total data ({total_length} bytes):")
    print(f"         \"{combined_data}\"")

    shm.close()


if __name__ == "__main__":
    shm = SharedMemory(create=True, size=256)

    # Initialize offset header to 0
    shm.buf[:4] = (0).to_bytes(4, byteorder="big")

    lock = Lock()
    data_ready_event = Event()
    completed_counter = Value("i", 0)  # Shared integer counter
    num_writers = 3

    # Launch reader first
    p_reader = Process(target=reader, args=(shm.name, data_ready_event))
    p_reader.start()

    # Launch writers concurrently
    writers = [
        Process(
            target=writer,
            args=(
                i + 1,
                shm.name,
                lock,
                data_ready_event,
                completed_counter,
                num_writers,
            ),
        )
        for i in range(num_writers)
    ]

    for w in writers:
        w.start()

    for w in writers:
        w.join()

    p_reader.join()

    shm.close()
    shm.unlink()