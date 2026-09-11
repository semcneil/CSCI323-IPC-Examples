"""
messageQueueEx.py
====================================
This is an example of IPC.

| Author: Seth McNeill
| Date: 2026 September 11
"""

import time
from multiprocessing import Process, Queue


def producer(queue):
    items = ["item_1", "item_2", "item_3"]
    for item in items:
        time.sleep(1)
        queue.put(item)
    queue.put(None)  # Sentinel value to signal completion


def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        print(f"[Message Queue] Consumer processed: {item}")


if __name__ == "__main__":
    q = Queue()

    p_prod = Process(target=producer, args=(q,))
    p_cons = Process(target=consumer, args=(q,))

    p_prod.start()
    p_cons.start()

    p_prod.join()
    p_cons.join()