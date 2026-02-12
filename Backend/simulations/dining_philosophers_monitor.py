# backend/simulations/dining_philosophers_monitor.py

import threading
import time
import random

class DiningMonitor:
    def __init__(self, n, log_buffer):
        self.n = n
        self.log = log_buffer
        self.state = ["THINKING"] * n
        self.forks = [threading.Lock() for _ in range(n)]
        self.mutex = threading.Lock()
        self.condition = [threading.Condition(self.mutex) for _ in range(n)]

    def left(self, i):
        return (i + self.n - 1) % self.n

    def right(self, i):
        return (i + 1) % self.n

    def test(self, i):
        if (self.state[i] == "HUNGRY" and
            self.state[self.left(i)] != "EATING" and
            self.state[self.right(i)] != "EATING"):
            self.state[i] = "EATING"
            self.condition[i].notify()

    def pickup_forks(self, i):
        with self.mutex:
            self.state[i] = "HUNGRY"
            self.log.append(f"Philosopher {i} is HUNGRY (monitor).")
            self.test(i)
            while self.state[i] != "EATING":
                self.condition[i].wait()

    def putdown_forks(self, i):
        with self.mutex:
            self.state[i] = "THINKING"
            self.log.append(f"Philosopher {i} put down forks (monitor).")
            self.test(self.left(i))
            self.test(self.right(i))

    def philosopher(self, i, meals=3):
        for _ in range(meals):
            # Thinking
            self.log.append(f"Philosopher {i} is THINKING (monitor).")
            time.sleep(random.uniform(0.5, 1.0))

            # Attempt to eat
            self.pickup_forks(i)
            self.log.append(f"Philosopher {i} is EATING (monitor).")
            time.sleep(random.uniform(0.5, 1.0))
            self.putdown_forks(i)
            self.log.append(f"Philosopher {i} is DONE meal (monitor).")
