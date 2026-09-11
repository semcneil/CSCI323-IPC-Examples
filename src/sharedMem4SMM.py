"""
sharedMem4SMM.py
====================================
This is an example of IPC.

| Author: Seth McNeill
| Date: 2026 September 11
"""

from multiprocessing import Process
from multiprocessing.managers import SharedMemoryManager


def writer(s_list):
    s_list[0] = "Dynamic string of arbitrary length"


def reader(s_list):
    # Reader inspects content without needing fixed indices or hardcoded byte counts
    message = s_list[0]
    print(
        f"[SharedMemoryManager] Reader received ({len(message)} chars): '{message}'"
    )


if __name__ == "__main__":
    with SharedMemoryManager() as smm:
        # Create shared list containing 1 string slot up to 64 bytes
        s_list = smm.ShareableList([" " * 64])

        p1 = Process(target=writer, args=(s_list,))
        p2 = Process(target=reader, args=(s_list,))

        p1.start()
        p1.join()  # Ensure writer completes before reader reads

        p2.start()
        p2.join()