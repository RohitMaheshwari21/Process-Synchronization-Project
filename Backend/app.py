

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading
import time

# ✅ Import simulation classes
from simulations.producer_consumer import ProducerConsumer
from simulations.dining_philosophers import DiningPhilosophers 
from simulations.readers_writers import ReadersWriters
from simulations.dining_philosophers_monitor import DiningMonitor



app = Flask(

    __name__,
    static_folder="../frontend/static",   # point to frontend/static
    template_folder="../frontend/templates"  # index.html here
)
CORS(app)  

# Shared data structures
log_buffer = []
lock = threading.Semaphore(1)

# Producer-Consumer logs
pc_log_buffer = []
pc_threads = []

# Dining Philosophers logs
dp_log_buffer = []
dp_threads = []

# Critical Section Simulation 
def simulate_basic(process_id):
    global log_buffer
    log_buffer.append(f"Process {process_id} waiting...")
    lock.acquire()
    log_buffer.append(f"Process {process_id} ENTERED critical section.")
    time.sleep(1)
    log_buffer.append(f"Process {process_id} EXITED critical section.")
    lock.release()

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/start_basic")
def start_basic_sim():
    global log_buffer
    log_buffer = []
    threads = []
    for i in range(3):
        t = threading.Thread(target=simulate_basic, args=(i + 1,))
        threads.append(t)
        t.start()
    return jsonify({"status": "Basic simulation started"})

@app.route("/get_basic_logs")
def get_basic_logs():
    return jsonify(log_buffer)

# Producer–Consumer Simulation 
@app.route("/start_producer_consumer")
def start_pc():
    global pc_log_buffer, pc_threads
    pc_log_buffer = []
    buffer_size = 5
    produce_count = 5

    sim = ProducerConsumer(buffer_size, pc_log_buffer)

    pc_threads = []
    for pid in [1, 2]:
        t = threading.Thread(target=sim.producer, args=(pid, produce_count))
        pc_threads.append(t)
        t.start()
    for cid in [1, 2]:
        t = threading.Thread(target=sim.consumer, args=(cid, produce_count))
        pc_threads.append(t)
        t.start()

    return jsonify({"status": "Producer-Consumer simulation started"})

@app.route("/get_pc_logs")
def get_pc_logs():
    return jsonify(pc_log_buffer)

# Dining Philosophers Simulation
@app.route("/start_dining_philosophers")
def start_dining_philosophers():
    global dp_log_buffer, dp_threads
    dp_log_buffer = []

    sim = DiningPhilosophers(5, dp_log_buffer)

    dp_threads = []
    for philosopher_id in range(5):  # philosophers range
        t = threading.Thread(target=sim.philosopher, args=(philosopher_id,))

        dp_threads.append(t)
        t.start()

    return jsonify({"status": "Dining Philosophers simulation started"})

@app.route("/get_dp_logs")
def get_dp_logs():
    return jsonify(dp_log_buffer)


   # Shared data for Readers-Writers problem
rw_log_buffer = []
rw_threads = []

@app.route("/start_readers_writers")
def start_rw():
    global rw_log_buffer, rw_threads
    rw_log_buffer = []
    sim = ReadersWriters(rw_log_buffer)

    rw_threads = []
    # Example
    for rid in range(1, 4):
        t = threading.Thread(target=sim.reader, args=(rid, 3))
        rw_threads.append(t)
        t.start()
    for wid in range(1, 3):
        t = threading.Thread(target=sim.writer, args=(wid, 3))
        rw_threads.append(t)
        t.start()

    return jsonify({"status": "Readers-Writers simulation started"})

@app.route("/get_rw_logs")
def get_rw_logs():
    return jsonify(rw_log_buffer)


# Monitor-based Dining Philosopher
dp_mon_log = []
dp_mon_threads = []

@app.route("/start_dining_monitor")
def start_dining_monitor():
    global dp_mon_log, dp_mon_threads
    dp_mon_log = []
    n = 5
    meals = 3
    sim = DiningMonitor(n, dp_mon_log)

    dp_mon_threads = []
    for i in range(n):
        t = threading.Thread(target=sim.philosopher, args=(i, meals))
        dp_mon_threads.append(t)
        t.start()
    return jsonify({"status": "Dining Monitor simulation started"})

@app.route("/get_dp_mon_logs")
def get_dp_mon_logs():
    return jsonify(dp_mon_log)




if __name__ == "__main__":
    app.run(debug=True)


 

