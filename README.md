<div align="center">

# 🛡️ EDR Sentinel

### 🔎 Endpoint Detection & Response — Python GUI Simulation

*A beginner-friendly cybersecurity project for process monitoring, blacklist-based detection, and controlled manual response.*

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-0F766E?style=for-the-badge)
![Security](https://img.shields.io/badge/Focus-Defensive%20Security-16A34A?style=for-the-badge)
![Status](https://img.shields.io/badge/Project-Educational%20Simulation-7C3AED?style=for-the-badge)

</div>

---

## 🌈 Welcome to EDR Sentinel!

**EDR Sentinel** is a desktop application built with **Python**, **Tkinter**, and **psutil**. It monitors running processes and compares their executable names against a configurable blacklist. When a match is found, it displays the process name and Process ID (**PID**) in a graphical dashboard.

The project demonstrates the basic defensive-security workflow:

`🔍 Detect` → `🧾 Review` → `🛠️ Controlled Response`

> [!IMPORTANT]
> This is an educational simulation—not a complete antivirus product or production-ready EDR system.

## 🖼️ Dashboard Preview

![EDR Sentinel dashboard showing detected Chrome processes, PIDs, response status, and activity log](screenshots/edr-sentinel-dashboard.png)

<sub>Example session showing Chrome process detections and the manual-response safety restriction. This screenshot demonstrates detection, not a completed termination action.</sub>

## ✨ Features at a Glance

| Feature | Description |
|---|---|
| 🖥️ **Desktop GUI** | A simple dashboard built with Tkinter |
| 🔍 **Process monitoring** | Enumerates running processes using `psutil` |
| 📋 **Configurable blacklist** | Loads executable names from `blacklist.txt` |
| 🚨 **Detection alerts** | Shows matching process names and PIDs |
| 🧹 **Duplicate-alert control** | Avoids repeatedly adding the same running process instance |
| 🔎 **Manual review** | Select a detection and choose **Review Selected** |
| 🛡️ **Restricted response** | Response action is limited to the dedicated `edr_test_process.exe` test target |
| 📜 **Activity log** | Records detection and review events |
| ⏯️ **Monitoring controls** | Start, stop, and reload the blacklist from the GUI |

## 🧰 Built With

- 🐍 **Python 3** — application logic
- 🪟 **Tkinter** — desktop graphical interface
- 📊 **psutil** — process enumeration and process information

## 📁 Project Structure

```text
EDR-Sentinel/
├── edr_sentinel.py
├── blacklist.txt
├── requirements.txt
├── README.md
└── screenshots/
    └── edr-sentinel-dashboard.png
```

## 🚀 Getting Started

### ✅ Requirements

- Windows with Python 3 installed
- `psutil`
- Tkinter (normally included with standard Windows Python installations)

### 📥 1. Install the dependency

Open a terminal in the project directory and run:

```bash
py -m pip install -r requirements.txt
```

If you do not have a `requirements.txt` file yet, run:

```bash
py -m pip install psutil
```

### ⚙️ 2. Configure the blacklist

Edit `blacklist.txt`. Add one executable name per line:

```text
chrome.exe
notepad.exe
calc.exe
edr_test_process.exe
```

Save the file. In the dashboard, click **Reload Blacklist** to load your changes.

### ▶️ 3. Launch EDR Sentinel

```bash
py edr_sentinel.py
```

Click **Start Monitoring** in the desktop window.

> 💡 If the `py` command is unavailable, try `python` instead.

## 🧪 Try It Out

1. Add a process name to `blacklist.txt`.
2. Save the file and click **Reload Blacklist**.
3. Start monitoring and open the corresponding application.
4. When a process matches, check its name and PID in the detection table.
5. Select a row and click **Review Selected** to view its response status.

### 📌 Example log

```text
[INFO] Monitoring started.
[ALERT] Detected chrome.exe (PID: 3828)
[INFO] Detection only; no action taken.
```

<sub>The PID above is an example. Your system will show different values.</sub>

### 🧠 Why can Chrome appear many times?

Chrome uses multiple processes for tabs, extensions, GPU work, and background tasks. Multiple `chrome.exe` entries are therefore normal. Each PID represents a process instance, not necessarily a separate browser window.

## 🛡️ Manual Response & Safety

The response button is intended **only** for a dedicated test process named `edr_test_process.exe`. Other applications—including Chrome and ordinary Windows processes—should remain **review only**.

For a response demonstration, use a harmless test program that you created and control. Do not rename an unrelated executable to make it eligible for termination. The example checks the process name and recorded creation time, but it is still a learning project and not a production-grade security boundary.

## 🎓 What You'll Learn

- 🧩 How operating systems expose process information
- 🆔 What process IDs (PIDs) represent
- 🗂️ How to read and parse configuration files
- 🖱️ How to build a Python GUI with Tkinter
- 🧯 How to handle process-access errors
- 🔐 How defensive tools separate detection, review, and response

## ⚠️ Limitations

- A matching filename does **not** prove malicious activity.
- Renaming an executable may evade name-based detection.
- Some process details may be unavailable because of permissions or process exit.
- Applications such as Chrome can spawn many helper processes.
- The project does not perform malware analysis, file-signature verification, network monitoring, or advanced behavioral analysis.
- It is not a replacement for Windows Security or a commercial EDR product.

## 🔐 Responsible Use

Use this project only on computers you own or are authorized to monitor. Carefully review any response action. This project is intended for education and controlled testing.

## 🗺️ Future Improvements

- 📊 Add summary counters for detected processes
- 🧾 Export activity logs to a file
- 🔎 Add process details to the review panel
- 🎨 Improve dashboard themes and status indicators
- 🧪 Add automated tests for blacklist parsing and detection logic

## 📄 License

Add a `LICENSE` file before distributing this project. Choose a license that matches how you want others to use your code.

---

<div align="center">

**⭐ Built for learning defensive cybersecurity, one process at a time.**

</div>
