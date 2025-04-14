document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ script.js is running!");

    // 🌡️ Temperature
    const tempBtn = document.querySelector('[onclick="getTemperature()"]');
    if (tempBtn) {
        tempBtn.addEventListener("click", function () {
            fetch('/temperature')
                .then(response => response.json())
                .then(data => {
                    document.getElementById("temperature").textContent = `${data.temperature} °C`;
                })
                .catch(error => console.error("Error fetching temperature:", error));
        });
    }

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
                        li.textContent = `${schedule.device} → ${schedule.action.toUpperCase()} at ${schedule.time}`;
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

    // 🎤 Voice Command
    const voiceButton = document.getElementById("voice-command");
    if (voiceButton) {
        voiceButton.addEventListener("click", function () {
            alert("Voice activation feature coming soon! 🎤");
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
});
