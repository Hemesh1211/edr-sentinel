<div align="center">

# 🛡️ EDR Sentinel

### 🔎 Endpoint Detection & Response — Python GUI Simulation

*A beginner-friendly cybersecurity project demonstrating process monitoring, blacklist-based detection, and a controlled manual-review workflow.*

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-0F766E?style=for-the-badge)
![Security](https://img.shields.io/badge/Focus-Defensive%20Security-16A34A?style=for-the-badge)
![Project](https://img.shields.io/badge/Type-Educational%20Simulation-7C3AED?style=for-the-badge)

</div>

---

## 🌈 Welcome to EDR Sentinel!

**EDR Sentinel** is a desktop application built with **Python**, **Tkinter**, and **psutil**. It monitors running processes and compares their executable names against a configurable blacklist. Matching processes appear in a graphical dashboard with their process IDs (**PIDs**) and response status.

The project demonstrates a basic defensive-security workflow:

`🔍 Detect` → `🧾 Review` → `🛡️ Restricted Response`

> [!IMPORTANT]
> EDR Sentinel is an educational simulation, not a complete antivirus or production-ready endpoint detection and response (EDR) product.

## 🖼️ Screenshots

### 1. Detection Log — Process Matching

The first screenshot shows the original monitoring view, where EDR Sentinel detects multiple Chrome processes and logs their PIDs.

![EDR Sentinel detection log showing Chrome process matches](screenshots/edr-sentinel-detection-log.png)

### 2. Process Dashboard — Manual Review

The second screenshot shows the process table, response-status column, **Review Selected** button, and restricted **Stop Selected Test Process** action.

![EDR Sentinel process dashboard with manual review controls](screenshots/edr-sentinel-manual-response-dashboard.png)

<sub>These screenshots demonstrate process detection and the review interface. They do not show a completed test-process termination.</sub>

## ✨ Features at a Glance

| Feature | Description |
|---|---|
| 🖥️ **Desktop GUI** | Dashboard built with Tkinter |
| 🔍 **Process monitoring** | Enumerates running processes using `psutil` |
| 📋 **Configurable blacklist** | Reads executable names from `blacklist.txt` |
| 🚨 **Detection alerts** | Displays matching process names and PIDs |
| 🧹 **Duplicate-alert control** | Avoids repeatedly adding the same running process instance |
| 🧾 **Manual review** | Select a detection and click **Review Selected** |
| 🛡️ **Restricted response** | Response action is intended only for the dedicated `edr_test_process.exe` test target |
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
    ├── edr-sentinel-detection-log.png
    └── edr-sentinel-manual-response-dashboard.png
```

## 🚀 Getting Started

### ✅ Requirements

- Windows with Python 3 installed
- `psutil`
- Tkinter (normally included with standard Windows Python installations)

### 📥 1. Install the dependency

Open a terminal in the project folder and run:

```bash
py -m pip install -r requirements.txt
```

If you do not have a `requirements.txt` file yet, run:

```bash
py -m pip install psutil
```

### ⚙️ 2. Configure the blacklist

Edit `blacklist.txt` and add one executable name per line. Example:

```text
chrome.exe
notepad.exe
calc.exe
edr_test_process.exe
```

Save the file and click **Reload Blacklist** in the dashboard.

### ▶️ 3. Launch EDR Sentinel

```bash
py edr_sentinel.py
```

Click **Start Monitoring** in the desktop window.

> 💡 If the `py` command is unavailable, try `python` instead.

## 🧪 How to Test

1. Add a process name to `blacklist.txt`.
2. Save the file and click **Reload Blacklist**.
3. Start monitoring and open the corresponding application.
4. When a match is found, review the process name and PID in the dashboard.
5. Select a row and click **Review Selected** to inspect its response status.

### 📌 Example Log

```text
[INFO] Monitoring started.
[ALERT] Detected chrome.exe (PID: 3828)
[INFO] Detection only; no action taken.
```

*The PID is illustrative; your system will display different values.*

### 🧠 Why can Chrome appear many times?

Chrome uses multiple processes for tabs, extensions, GPU work, and background tasks. Multiple `chrome.exe` entries are normal. Each PID identifies a process instance, not necessarily a separate browser window.

## 🛡️ Manual Response and Safety

The response action is intended **only** for a dedicated test process named `edr_test_process.exe`. Other applications—including Chrome and ordinary Windows processes—should remain **review only**.

For a response demonstration, use a harmless test program that you created and control. Do not rename an unrelated executable to make it eligible for termination. The example checks the process name and recorded creation time, but it is still a learning project and not a production-grade security boundary.

## 🎓 Learning Objectives

- 🧩 Understand operating-system process enumeration
- 🆔 Learn what process IDs represent
- 🗂️ Practice reading configuration files
- 🖱️ Build a desktop GUI with Tkinter
- 🧯 Handle process-access errors
- 🔐 Explore detection, review, and response concepts in defensive security

## ⚠️ Limitations

- A matching filename does **not** prove malicious activity.
- Renaming an executable may evade name-based detection.
- Some process details may be unavailable because of permissions or process exit.
- Applications such as Chrome can create many helper processes.
- This project does not perform malware analysis, file-signature verification, network monitoring, or advanced behavioral analysis.
- It is not a replacement for Windows Security or a commercial EDR product.

## 🔐 Responsible Use

Use this project only on computers you own or are authorized to monitor. Review any response action carefully. This project is intended for education and controlled testing.

## 🗺️ Future Improvements

- 📊 Add summary counters for detected processes
- 🧾 Export activity logs to a file
- 🔎 Add process details to the review panel
- 🎨 Improve dashboard themes and status indicators
- 🧪 Add automated tests for blacklist parsing and detection logic

## 📄 License

Add a `LICENSE` file before distributing the project. Choose a license that matches how you want others to use your code.

---

<div align="center">

**⭐ Built for learning defensive cybersecurity, one process at a time.**

</div>
