"""
messagePassing.py
====================================
This is an example of IPC.

| Author: Seth McNeill
| Date: 2026 September 11
"""

from multiprocessing import Process, SimpleQueue


def worker(queue):
    msg = queue.get()
    print(f"[Message Passing] Worker received: {msg}")


if __name__ == "__main__":
    queue = SimpleQueue()

    p = Process(target=worker, args=(queue,))
    p.start()

    queue.put({"status": "SUCCESS", "code": 200, "payload": "Task Complete"})

    p.join()