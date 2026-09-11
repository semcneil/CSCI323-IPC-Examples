"""
semaphoreEx.py
====================================
This is an example of IPC.

| Author: Seth McNeill
| Date: 2026 September 11
"""

import time
from multiprocessing import Process, Semaphore


def worker(semaphore, worker_id):
    with semaphore:
        print(f"[Semaphores] Worker {worker_id} acquired slot.")
        time.sleep(0.05)
        print(f"[Semaphores] Worker {worker_id} releasing slot.")


if __name__ == "__main__":
    # Allow a maximum of 2 processes in the critical section concurrently
    sem = Semaphore(2)

    processes = [Process(target=worker, args=(sem, i)) for i in range(4)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()