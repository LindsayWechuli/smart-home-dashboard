document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ script.js is running!");



    // ✅ System Status
    const checkStatusBtn = document.getElementById("checkStatus");
    if (checkStatusBtn) {
        checkStatusBtn.addEventListener("click", function () {
            document.getElementById("system-status").textContent = "System is healthy!";
        });
    }

    // 📅 View Scheduled Devices
    const viewSchedulesBtn = document.getElementById("viewSchedulesBtn");
    if (viewSchedulesBtn) {
        viewSchedulesBtn.addEventListener("click", function () {
            fetch("/get-schedules")
                .then(response => response.json())
                .then(data => {
                    console.log("📦 Schedule data:", data);
                    const list = document.getElementById("scheduleList");
                    list.innerHTML = ""; // Clear previous list

                    if (data.length === 0) {
                        const emptyItem = document.createElement("li");
                        emptyItem.textContent = "No scheduled devices found.";
                        emptyItem.className = "list-group-item";
                        list.appendChild(emptyItem);
                    } else {
                        data.forEach(schedule => {
                            const li = document.createElement("li");
                            li.className = "list-group-item";
                            li.textContent = `${schedule.device_name} → ${schedule.action.toUpperCase()} at ${schedule.schedule_time}`;
                            list.appendChild(li);
                        });
                    }

                    const viewModal = new bootstrap.Modal(document.getElementById("viewSchedulesModal"));
                    viewModal.show();
                })
                .catch(error => {
                    console.error("Error fetching schedules:", error);
                    alert("Failed to load scheduled devices.");
                });
        });
    }

    // 💡 Lights
    const lightsOnBtn = document.getElementById("lightsOn");
    const lightsOffBtn = document.getElementById("lightsOff");

    function toggleLights(state) {
        if (!state) {
            console.error("Error: State is undefined");
            return;
        }

        fetch(`/lights/${state}`, {
            method: "POST",
        })
        .then(response => response.json())
        .then(data => {
            console.log(`Lights ${state}:`, data);
            alert(`Lights turned ${state}`);
            document.getElementById("light-status").textContent = state.toUpperCase();
        })
        .catch(error => console.error("Error toggling lights:", error));
    }

    if (lightsOnBtn) {
        lightsOnBtn.addEventListener("click", () => toggleLights("on"));
    }

    if (lightsOffBtn) {
        lightsOffBtn.addEventListener("click", () => toggleLights("off"));
    }

    // 🔒 Smart Lock
    const lockBtn = document.getElementById("lockBtn");
    const unlockBtn = document.getElementById("unlockBtn"); 
    function toggleLock(state) {
        fetch(`/lock/${state}`, {
            method: "POST",
        })
        .then(response => response.json())
        .then(data => {
            console.log(`Door ${state}:`, data);
            alert(`Door ${state === "lock" ? "locked" : "unlocked"} successfully`);
            document.getElementById("lock-status").textContent = state.toUpperCase();
        })
        .catch(error => console.error("Error controlling lock:", error));
    }

    if (lockBtn) {
        lockBtn.addEventListener("click", () => toggleLock("lock"));
    }
    if (unlockBtn) {
        unlockBtn.addEventListener("click", () => toggleLock("unlock"));
    }

    // 🎤 Voice Command (Alert for now)
    const voiceButton = document.getElementById("voice-command");
    if (voiceButton) {
        voiceButton.addEventListener("click", function () {
            alert("Voice activated! 🎤");
        });
    }

    // ⏰ Device Scheduler (form submission to Flask)
    const schedulerForm = document.getElementById("schedulerForm");
    if (schedulerForm) {
        schedulerForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const device = document.getElementById("deviceName").value;
            const time = document.getElementById("scheduleTime").value;
            const action = document.querySelector('input[name="action"]:checked')?.value;

            if (!device || !time || !action) {
                alert("Please fill in all fields!");
                return;
            }

            fetch("/schedule-device", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    device: device,
                    time: time,
                    action: action,
                }),
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || "Failed to save schedule");
                    });
                }
                return response.json();
            })
            .then(data => {
                alert("✅ " + data.message);
            })
            .catch(error => {
                console.error("Error saving schedule:", error);
                alert("❌ Failed to save schedule.");
            });
        });
    }

    // ⚡ Energy Monitoring
    const energyBtn = document.getElementById("energyMonitorBtn");
    if (energyBtn) {
        energyBtn.addEventListener("click", function () {
            console.log("Energy Monitoring button clicked!");
            const myModal = new bootstrap.Modal(document.getElementById("energyMonitoringModal"));
            myModal.show();
            document.getElementById("energyUsage").textContent = "350W"; // Simulated value
        });
    }

    // 🎤 Real Voice Recognition
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        if (voiceButton) {
            voiceButton.addEventListener("click", function () {
                recognition.start();
                console.log("🎙️ Listening for voice command...");
            });

            recognition.onresult = function (event) {
                const voiceCommand = event.results[0][0].transcript.toLowerCase();
                console.log("✅ Voice input:", voiceCommand);

                if (voiceCommand.includes("turn on the lights")) {
                    toggleLights("on");
                } else if (voiceCommand.includes("turn off the lights")) {
                    toggleLights("off");
                } else if (voiceCommand.includes("check system status")) {
                    checkStatusBtn.click();    
                } else if (voiceCommand.includes("check temperature")) {
                    tempBtn.click(); 
                } else if (voiceCommand.includes("lock the front door")) {
                    toggleLock("lock");
                } else if (voiceCommand.includes("unlock the front door")) {
                    toggleLock("unlock");               
                } else {
                    alert(`Unrecognized command: "${voiceCommand}"`);
                }
            };

            recognition.onerror = function (event) {
                console.error("❌ Voice recognition error:", event.error);
            };
        }
    } else {
        console.warn("🛑 Your browser does not support voice recognition.");
        if (voiceButton) {
            voiceButton.disabled = true;
            voiceButton.textContent = "Voice Unsupported 😢";
        }
    }

      // 🚨 Alarm System Controls
  const alarmStatus = document.getElementById("alarmStatus");
  const armBtn = document.getElementById("armAlarm");
  const disarmBtn = document.getElementById("disarmAlarm");

  let isArmed = false;

  if (armBtn) {
    armBtn.addEventListener("click", () => {
      isArmed = true;
      alarmStatus.textContent = "Armed";
      alarmStatus.classList.remove("text-warning");
      alarmStatus.classList.add("text-danger");
      alert("🚨 Security alarm is now armed!");
    });
  }

  if (disarmBtn) {
    disarmBtn.addEventListener("click", () => {
      isArmed = false;
      alarmStatus.textContent = "Disarmed";
      alarmStatus.classList.remove("text-danger");
      alarmStatus.classList.add("text-warning");
      alert("🔓 Alarm disarmed.");
    });
  }

  // Optional test alarm trigger (simulated intruder)
  setTimeout(() => {
    if (isArmed) {
      alert("⚠️ INTRUDER ALERT! The alarm is going off!");
    }
  }, 10000);


  function lockBedroom(action) {
    const statusElement = document.getElementById("bedroom-lock-status");

    fetch(`/lock-bedroom/${action}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Update the UI based on the response
        if (action === "lock") {
            statusElement.textContent = "LOCKED";
            statusElement.style.color = "red";
        } else if (action === "unlock") {
            statusElement.textContent = "UNLOCKED";
            statusElement.style.color = "green";
        }
        alert(data.message); // Show the backend message (optional)
    })
    .catch(error => {
        console.error("Error locking bedroom:", error);
        alert("Failed to update bedroom lock.");
    });
}


    // Ensure elements are properly referenced
    const cameraBtn = document.getElementById("cameraBtn");
    const cameraModal = new bootstrap.Modal(document.getElementById("cameraModal"));
    const cameraStatusText = document.getElementById("cameraStatus");
    const toggleCameraBtn = document.getElementById("toggleCameraBtn");
  
    let cameraOn = false;
  
    // Check if all elements exist to avoid errors
    if (cameraBtn && cameraModal && cameraStatusText && toggleCameraBtn) {
  
      // Camera button opens the modal
      cameraBtn.addEventListener("click", function() {
        cameraModal.show();
        updateCameraModal();
      });
  
      // Toggle camera state on button click
      toggleCameraBtn.addEventListener("click", function() {
        cameraOn = !cameraOn;
        updateCameraModal();
      });
  
      // Update modal content based on camera state
      function updateCameraModal() {
        if (cameraOn) {
          cameraStatusText.innerText = "on";
          toggleCameraBtn.innerText = "Turn Camera Off";
        } else {
          cameraStatusText.innerText = "off";
          toggleCameraBtn.innerText = "Turn Camera On";
        }
      }
    } else {
      console.error("Some elements are missing in the DOM. Please check your HTML.");
    }

 // 🌡️ Temperature fetching
function getTemperature() {
    fetch('/temperature')
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => {
        document.getElementById('temperature').textContent = `${data.temperature} °C`;
      })
      .catch(err => console.error('Error fetching temperature:', err));
}

const tempBtn = document.getElementById('tempBtn');
if (tempBtn) {
  tempBtn.addEventListener('click', getTemperature);
}

});
