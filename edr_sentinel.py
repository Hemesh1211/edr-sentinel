
import os
import time
import tkinter as tk
from tkinter import ttk, messagebox
import psutil

# ==========================================
# EDR SENTINEL - CONFIGURATION
# ==========================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BLACKLIST_FILE = os.path.join(SCRIPT_DIR, "blacklist.txt")
SCAN_INTERVAL = 1000

# Only this dedicated test executable may be stopped.
SAFE_TEST_PROCESS = "edr_test_process.exe"


class EDRSentinel:
    def __init__(self, root):
        self.root = root
        self.root.title("EDR Sentinel - Process Monitor")
        self.root.geometry("950x650")
        self.root.minsize(750, 500)

        self.monitoring = False
        self.after_id = None
        self.blacklist = set()

        # Detection identity includes PID and process start time.
        self.detected = {}
        self.alert_items = {}

        self.build_ui()
        self.load_blacklist()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    # ==========================================
    # USER INTERFACE
    # ==========================================

    def build_ui(self):
        header = tk.Frame(
            self.root, bg="#172554", padx=20, pady=18
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="EDR SENTINEL",
            font=("Segoe UI", 23, "bold"),
            fg="white",
            bg="#172554"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Endpoint Detection & Response Simulation",
            font=("Segoe UI", 10),
            fg="#BFDBFE",
            bg="#172554"
        ).pack(anchor="w")

        controls = ttk.Frame(self.root, padding=12)
        controls.pack(fill="x")

        self.start_button = ttk.Button(
            controls,
            text="Start Monitoring",
            command=self.start_monitoring
        )
        self.start_button.pack(side="left", padx=4)

        self.stop_button = ttk.Button(
            controls,
            text="Stop Monitoring",
            command=self.stop_monitoring,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=4)

        ttk.Button(
            controls,
            text="Reload Blacklist",
            command=self.load_blacklist
        ).pack(side="left", padx=4)

        self.status = tk.StringVar(value="Status: Stopped")
        ttk.Label(
            self.root,
            textvariable=self.status,
            padding=(12, 4)
        ).pack(anchor="w")

        ttk.Label(
            self.root,
            text="Detected Processes — select an entry to review",
            padding=(12, 6)
        ).pack(anchor="w")

        columns = ("pid", "name", "status")
        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=8
        )

        self.tree.heading("pid", text="PID")
        self.tree.heading("name", text="Process Name")
        self.tree.heading("status", text="Response Status")

        self.tree.column("pid", width=90, anchor="center")
        self.tree.column("name", width=250)
        self.tree.column("status", width=300)

        self.tree.pack(
            fill="x", padx=12, pady=(0, 8)
        )

        actions = ttk.Frame(self.root, padding=(12, 4))
        actions.pack(fill="x")

        ttk.Button(
            actions,
            text="Review Selected",
            command=self.review_selected
        ).pack(side="left", padx=4)

        self.action_button = ttk.Button(
            actions,
            text="Stop Selected Test Process",
            command=self.stop_test_process
        )
        self.action_button.pack(side="left", padx=4)

        ttk.Label(
            self.root,
            text="Activity Log",
            padding=(12, 6)
        ).pack(anchor="w")

        self.log = tk.Text(
            self.root,
            height=10,
            wrap="word",
            font=("Consolas", 9),
            state="disabled"
        )
        self.log.pack(
            fill="both", expand=True, padx=12, pady=(0, 8)
        )

        ttk.Label(
            self.root,
            text=(
                "Safety: response is restricted to "
                + SAFE_TEST_PROCESS
                + ". Other processes cannot be stopped here."
            ),
            padding=10
        ).pack(fill="x")

    # ==========================================
    # LOGGING
    # ==========================================

    def write_log(self, message):
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    # ==========================================
    # BLACKLIST
    # ==========================================

    def load_blacklist(self):
        try:
            with open(
                BLACKLIST_FILE,
                "r",
                encoding="utf-8-sig"
            ) as file:
                self.blacklist = {
                    line.strip().lower()
                    for line in file
                    if line.strip()
                    and not line.strip().startswith("#")
                }

            self.write_log(
                f"[INFO] Loaded {len(self.blacklist)} blacklist entries."
            )

        except OSError as error:
            self.blacklist = set()
            self.write_log(
                f"[ERROR] Cannot read blacklist: {error}"
            )
            messagebox.showerror(
                "Blacklist Error", str(error)
            )

    # ==========================================
    # MONITORING
    # ==========================================

    def start_monitoring(self):
        if self.monitoring:
            return

        if not self.blacklist:
            messagebox.showwarning(
                "Empty Blacklist",
                "Add process names to blacklist.txt first."
            )
            return

        self.monitoring = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status.set("Status: Monitoring")

        self.write_log("[INFO] Monitoring started.")
        self.scan_processes()

    def stop_monitoring(self):
        self.monitoring = False

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status.set("Status: Stopped")

        self.write_log("[INFO] Monitoring stopped.")

    def scan_processes(self):
        if not self.monitoring:
            return

        current = {}

        try:
            for proc in psutil.process_iter(
                ["pid", "name", "create_time"]
            ):
                try:
                    info = proc.info
                    pid = info["pid"]
                    name = (info["name"] or "").lower()
                    created = info.get("create_time")

                    if name not in self.blacklist:
                        continue

                    key = (pid, created)
                    current[key] = {
                        "pid": pid,
                        "name": name,
                        "created": created
                    }

                    # Only create a new alert once per process instance.
                    if key not in self.detected:
                        self.detected[key] = {
                            **current[key],
                            "reviewed": False
                        }

                        self.add_alert(key)

                        self.write_log(
                            f"[ALERT] Detected {name} (PID: {pid})"
                        )

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                    KeyError,
                    TypeError,
                    ValueError
                ):
                    continue

            # Remove processes that have exited.
            for key in list(self.detected):
                if key not in current:
                    self.detected.pop(key, None)
                    if self.tree.exists(self.alert_items.get(key, "")):
                        self.tree.delete(self.alert_items[key])
                    self.alert_items.pop(key, None)

        except psutil.Error as error:
            self.write_log(f"[ERROR] Scan failed: {error}")

        self.after_id = self.root.after(
            SCAN_INTERVAL, self.scan_processes
        )

    def add_alert(self, key):
        item = self.detected[key]

        status = (
            "Eligible for test response"
            if item["name"] == SAFE_TEST_PROCESS
            else "Review only - response disabled"
        )

        row_id = self.tree.insert(
            "",
            "end",
            values=(item["pid"], item["name"], status)
        )

        self.alert_items[key] = row_id

    # ==========================================
    # REVIEW ACTION
    # ==========================================

    def get_selected(self):
        selection = self.tree.selection()

        if not selection:
            messagebox.showinfo(
                "Select a Process",
                "Select a detected process first."
            )
            return None

        row_id = selection[0]

        for key, item_id in self.alert_items.items():
            if item_id == row_id:
                return key

        return None

    def review_selected(self):
        key = self.get_selected()

        if key is None:
            return

        item = self.detected.get(key)

        if item is None:
            messagebox.showwarning(
                "Process Not Found",
                "This process is no longer being monitored."
            )
            return

        item["reviewed"] = True

        messagebox.showinfo(
            "Process Review",
            f"Process: {item['name']}\n"
            f"PID: {item['pid']}\n\n"
            f"Response status: "
            f"{'Test response eligible' if item['name'] == SAFE_TEST_PROCESS else 'Review only'}\n\n"
            "No process was terminated."
        )

        self.write_log(
            f"[REVIEW] Reviewed {item['name']} (PID: {item['pid']})"
        )

    # ==========================================
    # RESTRICTED TEST RESPONSE
    # ==========================================

    def stop_test_process(self):
        key = self.get_selected()

        if key is None:
            return

        item = self.detected.get(key)

        if item is None:
            messagebox.showwarning(
                "Process Not Found",
                "The selected process is no longer active."
            )
            return

        # Strict allowlist: all other process names are refused.
        if item["name"] != SAFE_TEST_PROCESS:
            messagebox.showwarning(
                "Response Not Allowed",
                "This process cannot be stopped by EDR Sentinel.\n\n"
                f"Only {SAFE_TEST_PROCESS} is eligible."
            )
            self.write_log(
                f"[BLOCKED] Response refused for {item['name']}."
            )
            return

        confirmed = messagebox.askyesno(
            "Confirm Test Response",
            f"Stop the dedicated test process?\n\n"
            f"Process: {item['name']}\n"
            f"PID: {item['pid']}\n\n"
            "This action cannot be undone."
        )

        if not confirmed:
            return

        try:
            # Recheck the process identity immediately before action.
            proc = psutil.Process(item["pid"])

            if proc.name().lower() != SAFE_TEST_PROCESS:
                messagebox.showerror(
                    "Safety Check Failed",
                    "The process identity changed. No action taken."
                )
                return

            if item["created"] is not None:
                if abs(proc.create_time() - item["created"]) > 0.01:
                    messagebox.showerror(
                        "Safety Check Failed",
                        "The PID now belongs to another process."
                    )
                    return

            # Only the explicitly named dedicated test executable
            # can reach this point.
            proc.terminate()

            self.write_log(
                f"[ACTION] Termination requested for test PID {item['pid']}."
            )

            messagebox.showinfo(
                "Response Requested",
                "A termination request was sent to the test process."
            )

        except psutil.NoSuchProcess:
            self.write_log(
                "[INFO] Test process had already exited."
            )

        except psutil.AccessDenied:
            messagebox.showerror(
                "Access Denied",
                "Windows did not allow this action."
            )

        except psutil.Error as error:
            messagebox.showerror(
                "Response Error", str(error)
            )

    # ==========================================
    # EXIT
    # ==========================================

    def close_app(self):
        self.stop_monitoring()
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    app = EDRSentinel(window)
    window.mainloop()
