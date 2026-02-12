let simulationSpeed = 500;
let basicLogArray = [];
let pcLogArray = [];
let dpLogArray = [];
let rwLogArray = [];
let dpMonLogArray = [];

function classifyLog(log) {
  
  
  if (log.includes("waiting") || log.includes("HUNGRY")) return "log-waiting";
  if (log.includes("ENTERED")) return "log-entered";
  if (log.includes("EXITED")) return "log-exited";
  if (log.includes("thinking")) return "log-thinking";
  return "";
}

document.addEventListener("DOMContentLoaded", function () {
  const simSelect = document.getElementById("simSelect");
  const cards = ["basicCard", "pcCard", "dpCard", "rwCard", "dpMonCard"];
  showCard("basicCard");

  simSelect.addEventListener("change", function () {
    const selected = simSelect.value;
    showCard(selected);
  });

  function showCard(cardId) {
    cards.forEach((id) => {
      const card = document.getElementById(id);
      card.style.display = id === cardId ? "block" : "none";
    });
  }

  document.getElementById("speedSlider").addEventListener("input", function (e) {
    simulationSpeed = parseInt(e.target.value);
  });

  // Start Basic Simulation
  document.getElementById("startBasicBtn").addEventListener("click", function () {
    fetch("/start_basic")
      .then((response) => response.json())
      .then((data) => {
        basicLogArray = [];
        const logDiv = document.getElementById("basicLog");
        logDiv.innerHTML = "";
        const interval = setInterval(() => {
          fetch("/get_basic_logs")
            .then((res) => res.json())
            .then((logs) => {
              basicLogArray = logs;
              logDiv.innerHTML = "";
              logs.forEach((log) => {
                const p = document.createElement("p");
                p.className = classifyLog(log);
                p.textContent = log;
                logDiv.appendChild(p);
              });
              if (logs.length >= 9) clearInterval(interval);
            });
        }, simulationSpeed);
      });
  });

  // Start Producer Consumer
  document.getElementById("startPCBtn").addEventListener("click", function () {
    fetch("/start_producer_consumer")
      .then((response) => response.json())
      .then((data) => {
        pcLogArray = [];
        const logDiv = document.getElementById("pcLog");
        logDiv.innerHTML = "";
        const interval = setInterval(() => {
          fetch("/get_pc_logs")
            .then((res) => res.json())
            .then((logs) => {
              pcLogArray = logs;
              logDiv.innerHTML = "";
              logs.forEach((log) => {
                const p = document.createElement("p");
                p.className = classifyLog(log);
                p.textContent = log;
                logDiv.appendChild(p);
              });
              if (logs.length >= 20) clearInterval(interval);
            });
        }, simulationSpeed);
      });
  });

  // Start Dining Philosophers
  document.getElementById("startDPBtn").addEventListener("click", function () {
    fetch("/start_dining_philosophers")
      .then((response) => response.json())
      .then((data) => {
        dpLogArray = [];
        const logDiv = document.getElementById("dpLog");
        logDiv.innerHTML = "";
        const interval = setInterval(() => {
          fetch("/get_dp_logs")
            .then((res) => res.json())
            .then((logs) => {
              dpLogArray = logs;
              logDiv.innerHTML = "";
              logs.forEach((log) => {
                const p = document.createElement("p");
                p.className = classifyLog(log);
                p.textContent = log;
                logDiv.appendChild(p);
              });
              if (logs.length >= 100) clearInterval(interval);
            });
        }, simulationSpeed);
      });
  });

  // Start Readers-Writers
  document.getElementById("startRWBtn").addEventListener("click", function () {
    fetch("/start_readers_writers")
      .then((response) => response.json())
      .then((data) => {
        rwLogArray = [];
        const logDiv = document.getElementById("rwLog");
        logDiv.innerHTML = "";
        const interval = setInterval(() => {
          fetch("/get_rw_logs")
            .then((res) => res.json())
            .then((logs) => {
              rwLogArray = logs;
              logDiv.innerHTML = "";
              logs.forEach((log) => {
                const p = document.createElement("p");
                p.className = classifyLog(log);
                p.textContent = log;
                logDiv.appendChild(p);
              });
              if (logs.length >= 30) clearInterval(interval);
            });
        }, simulationSpeed);
      });
  });

  // Start Dining Philosophers with Monitor
  document.getElementById("startDPMonBtn").addEventListener("click", function () {
    fetch("/start_dining_monitor")
      .then((response) => response.json())
      .then((data) => {
        dpMonLogArray = [];
        const logDiv = document.getElementById("dpMonLog");
        logDiv.innerHTML = "";
        const interval = setInterval(() => {
          fetch("/get_dp_mon_logs")
            .then((res) => res.json())
            .then((logs) => {
              dpMonLogArray = logs;
              logDiv.innerHTML = "";
              logs.forEach((log) => {
                const p = document.createElement("p");
                p.className = classifyLog(log);
                p.textContent = log;
                logDiv.appendChild(p);
              });
              if (logs.length >= 75) clearInterval(interval);
            });
        }, simulationSpeed);
      });
  });

  // Download buttons
  document.getElementById("downloadBasicBtn").addEventListener("click", function () {
    downloadLogs(basicLogArray, "basic_logs.txt");
  });

  document.getElementById("downloadPCBtn").addEventListener("click", function () {
    downloadLogs(pcLogArray, "producer_consumer_logs.txt");
  });

  document.getElementById("downloadDPBtn").addEventListener("click", function () {
    downloadLogs(dpLogArray, "dining_philosophers_logs.txt");
  });

  document.getElementById("downloadRWBtn").addEventListener("click", function () {
    downloadLogs(rwLogArray, "readers_writers_logs.txt");
  });

  document.getElementById("downloadDPMonBtn").addEventListener("click", function () {
    downloadLogs(dpMonLogArray, "dining_monitor_logs.txt");
  });
});

function downloadLogs(logArray, filename) {
  if (logArray.length === 0) {
    alert("No logs to download.");
    return;
  }

  const blob = new Blob([logArray.join("\n")], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
