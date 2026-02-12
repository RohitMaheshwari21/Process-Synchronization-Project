# backend/simulations/producer_consumer.py

import threading
import time
import random

class ProducerConsumer:
    def __init__(self, buffer_size, log_buffer):
        self.buffer_size = buffer_size
        self.buffer = []
        self.log = log_buffer
        self.mutex = threading.Semaphore(1)
        self.empty = threading.Semaphore(buffer_size)
        self.full = threading.Semaphore(0)

    def producer(self, producer_id, produce_count=5):
        for i in range(produce_count):
            time.sleep(random.uniform(0.5, 1.5))  # simulate production time
            self.empty.acquire()  # wait if buffer is full
            self.mutex.acquire()

            item = f"P{producer_id}-Item{i+1}"
            self.buffer.append(item)
            self.log.append(f"Producer {producer_id} produced {item}. Buffer size: {len(self.buffer)}")

            self.mutex.release()
            self.full.release()  # signal that buffer has an item already

    def consumer(self, consumer_id, consume_count=5):
        for i in range(consume_count):
            self.full.acquire()  # wait if buffer is empty
            self.mutex.acquire()

            item = self.buffer.pop(0)
            self.log.append(f"Consumer {consumer_id} consumed {item}. Buffer size: {len(self.buffer)}")

            self.mutex.release()
            self.empty.release()  # signal that buffer has space available currently

            time.sleep(random.uniform(0.5, 1.5))  # simulate consumption time
