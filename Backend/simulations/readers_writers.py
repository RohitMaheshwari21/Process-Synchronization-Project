# backend/simulations/readers_writers.py

import threading
import time
import random

class ReadersWriters:
    def __init__(self, log_buffer):
        self.read_count = 0
        self.read_count_mutex = threading.Semaphore(1)
        self.rw_mutex = threading.Semaphore(1)
        self.log = log_buffer

    def reader(self, reader_id, read_times=3):
        for i in range(read_times):
            time.sleep(random.uniform(0.5, 1.0))  # simulate time before requesting
            self.log.append(f"Reader {reader_id} wants to read.")
            # Entry section
            self.read_count_mutex.acquire()
            self.read_count += 1
            if self.read_count == 1:
                self.rw_mutex.acquire()  # first reader locks resource
            self.read_count_mutex.release()

            # Critical section for reading
            self.log.append(f"Reader {reader_id} is READING.")
            time.sleep(random.uniform(0.5, 1.0))
            self.log.append(f"Reader {reader_id} finished READING.")

            # Exit section
            self.read_count_mutex.acquire()
            self.read_count -= 1
            if self.read_count == 0:
                self.rw_mutex.release()  # last reader releases resource
            self.read_count_mutex.release()

    def writer(self, writer_id, write_times=3):
        for i in range(write_times):
            time.sleep(random.uniform(0.5, 1.0))  # simulate time before requesting
            self.log.append(f"Writer {writer_id} wants to write.")
            self.rw_mutex.acquire()
            self.log.append(f"Writer {writer_id} is WRITING.")
            time.sleep(random.uniform(0.5, 1.0))
            self.log.append(f"Writer {writer_id} finished WRITING.")
            self.rw_mutex.release()

