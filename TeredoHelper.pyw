import os
import sys
import ctypes
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox, filedialog

# --- Admin Check ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def run_as_admin():
    script = sys.argv[0]
    subprocess.run(['powershell', '-Command', f'Start-Process python -ArgumentList \'{script}\' -Verb runAs'], shell=True)
    sys.exit()

# --- Command Runner ---
def run_command(command, max_output=4000):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        output = result.stdout if result.returncode == 0 else result.stderr
        return output[:max_output] if output else "No output returned."
    except Exception as e:
        return f"Error: {e}"

# --- Functional Buttons ---
def check_teredo_state(): messagebox.showinfo("Teredo State", run_command("netsh interface teredo show state"))
def set_teredo_enterprise(): messagebox.showinfo("Set to EnterpriseClient", run_command("netsh interface teredo set state type=enterpriseclient"))
def set_teredo_disabled(): messagebox.showinfo("Set to Disabled", run_command("netsh interface teredo set state type=disabled"))
def set_teredo_client(): messagebox.showinfo("Set to Client", run_command("netsh interface teredo set state type=client"))
def check_ipconfig(): messagebox.showinfo("IP Configuration", run_command("ipconfig"))
def clear_cache():
    run_command("ipconfig /flushdns")
    run_command("netsh winsock reset")
    run_command("netsh int ip reset")
    run_command("netsh interface teredo reset")
    messagebox.showinfo("Cache Cleared", "Network cache and configurations have been reset.")

def check_network_connectivity(): messagebox.showinfo("Connectivity Check", run_command("ping 8.8.8.8"))
def list_active_interfaces(): messagebox.showinfo("Active Interfaces", run_command("netsh interface show interface"))
def show_active_ports(): messagebox.showinfo("Active Ports", run_command("netstat -ano")[:4000])
def check_firewall_status(): messagebox.showinfo("Firewall Status", run_command("netsh advfirewall show allprofiles"))
def show_system_info(): messagebox.showinfo("System Info", run_command("systeminfo")[:4000])

def backup_teredo_state():
    output = run_command("netsh interface teredo show state")
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if filepath:
        try:
            with open(filepath, 'w') as file:
                file.write(output)
            messagebox.showinfo("Backup Successful", f"Saved to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

def restore_teredo_state():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        try:
            with open(filepath, 'r') as file:
                content = file.read()
            messagebox.showinfo("Restore Info", f"Backup contents loaded:\n\n{content}\n\nApply manually via 'netsh'.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")

def troubleshoot_network():
    run_command("tracert google.com")
    run_command("nslookup google.com")
    run_command("pathping google.com")
    messagebox.showinfo("Network Troubleshooting", "Network troubleshooting commands executed.")

def reset_network_settings():
    confirm = messagebox.askyesno("Confirm Reset", "This will reset ALL network settings. Are you sure?")
    if confirm:
        run_command("netsh winsock reset")
        run_command("netsh int ip reset")
        run_command("netsh interface teredo reset")
        run_command("netsh advfirewall reset")
        messagebox.showinfo("Network Reset", "Network settings reset to default.")

# --- Main GUI Setup ---
def main():
    if platform.system() != "Windows":
        messagebox.showerror("Unsupported OS", "This tool only works on Windows.")
        sys.exit()

    root = tk.Tk()
    root.title("Teredo Helper")
    root.configure(bg="#1e1e1e")
    root.resizable(False, False)

    # Banner
    banner_frame = tk.Frame(root, bg="black", padx=10, pady=10)
    banner_frame.pack(fill="x")

    banner_colors = ["#FF0000", "#FF3300", "#FF6600", "#FF9900", "#FFCC00", "#FFFF00"]
    banner_lines = [
        "████████╗███████╗██████╗ ███████╗██████╗  ██████╗     ██╗  ██╗███████╗██╗     ██████╗ ███████╗██████╗",
        "╚══██╔══╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔═══██╗    ██║  ██║██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗",
        "   ██║   █████╗  ██████╔╝█████╗  ██║  ██║██║   ██║    ███████║█████╗  ██║     ██████╔╝█████╗  ██████╔╝",
        "   ██║   ██╔══╝  ██╔══██╗██╔══╝  ██║  ██║██║   ██║    ██╔══██║██╔══╝  ██║     ██╔═══╝ ██╔══╝  ██╔══██╗",
        "   ██║   ███████╗██║  ██║███████╗██████╔╝╚██████╔╝    ██║  ██║███████╗███████╗██║     ███████╗██║  ██║",
        "   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝"
    ]
    for i, line in enumerate(banner_lines):
        tk.Label(banner_frame, text=line, fg=banner_colors[i], bg="black", font=("Courier", 12, "bold")).pack()

    tk.Label(root, text="Teredo Helper - Network and IP Configuration Tool", font=("Arial", 16), pady=10, bg="#1e1e1e", fg="white").pack()
    tk.Label(root, text="Credits: Developed by CheezzyBoii", font=("Arial", 10), pady=5, bg="#1e1e1e", fg="#aaaaaa").pack()

    # Button Grid
    button_frame = tk.Frame(root, bg="#1e1e1e", pady=20)
    button_frame.pack()

    buttons = [
        ("Check Teredo State", check_teredo_state),
        ("Set Teredo to EnterpriseClient", set_teredo_enterprise),
        ("Set Teredo to Disabled", set_teredo_disabled),
        ("Set Teredo to Client", set_teredo_client),
        ("Check IP Configuration", check_ipconfig),
        ("Clear Port and Network Cache", clear_cache),
        ("Check Network Connectivity", check_network_connectivity),
        ("List Active Network Interfaces", list_active_interfaces),
        ("Show Active Ports (Netstat)", show_active_ports),
        ("Check Firewall Status", check_firewall_status),
        ("Show Detailed System Info", show_system_info),
        ("Backup Current Teredo State", backup_teredo_state),
        ("Restore Teredo State", restore_teredo_state),
        ("Run Network Troubleshooting Tools", troubleshoot_network),
        ("Reset Network Settings to Default", reset_network_settings),
    ]

    cols = 3
    for index, (text, cmd) in enumerate(buttons):
        row = index // cols
        col = index % cols
        btn = tk.Button(button_frame, text=text, command=cmd, width=30, bg="#2e2e2e", fg="white", activebackground="#444")
        btn.grid(row=row, column=col, padx=10, pady=5)

    root.mainloop()

# --- Start App ---
if __name__ == "__main__":
    if not is_admin():
        messagebox.showinfo("Administrator Privileges Required", "This script needs administrator privileges to run.")
        run_as_admin()
    else:
        main()
