# backend/simulations/dining_philosophers.py

import threading
import time
import random

class DiningPhilosophers:
    def __init__(self, num_philosophers, log_buffer):
        self.n = num_philosophers
        self.log = log_buffer
        # One semaphore per fork (initial value=1)
        self.forks = [threading.Semaphore(1) for _ in range(self.n)]

    def philosopher(self, i, meal_count=3):
        left = i
        right = (i + 1) % self.n
        for m in range(meal_count):
            # Think
            self.log.append(f"Philosopher {i} is THINKING.")
            time.sleep(random.uniform(0.5, 1.0))

            self.log.append(f"Philosopher {i} is HUNGRY.")

            # Odd-even strategy
            if i % 2 == 0:
                self.forks[left].acquire()
                self.log.append(f"Philosopher {i} picked up LEFT fork {left}.")
                self.forks[right].acquire()
                self.log.append(f"Philosopher {i} picked up RIGHT fork {right}.")
            else:
                self.forks[right].acquire()
                self.log.append(f"Philosopher {i} picked up RIGHT fork {right}.")
                self.forks[left].acquire()
                self.log.append(f"Philosopher {i} picked up LEFT fork {left}.")

            # Eat process
            self.log.append(f"Philosopher {i} is EATING (meal {m + 1}).")
            time.sleep(random.uniform(0.5, 1.0))

            # Release forks
            self.forks[left].release()
            self.log.append(f"Philosopher {i} put down LEFT fork {left}.")
            self.forks[right].release()
            self.log.append(f"Philosopher {i} put down RIGHT fork {right}.")

        self.log.append(f"Philosopher {i} is DONE eating all meals.")
