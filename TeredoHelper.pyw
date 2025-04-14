import os
import sys
import ctypes
import subprocess
import tkinter as tk
from tkinter import messagebox

# Function to check if the script is running as Administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

# Function to relaunch the script with Administrator privileges
def run_as_admin():
    script = sys.argv[0]  # Get the script's path
    # Use PowerShell to run the script with administrator privileges and terminate the current process
    subprocess.run(['powershell', '-Command', f'Start-Process python -ArgumentList "{script}" -Verb runAs; exit'], shell=True)
    sys.exit()  # Exit the current process

# Check if the script is running as administrator, and relaunch it if necessary
if not is_admin():
    messagebox.showinfo("Administrator Privileges Required", "This script needs administrator privileges to run.")
    run_as_admin()  # Relaunch the script with elevated privileges

# Function to run system commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout if result.returncode == 0 else result.stderr

# Function to check the Teredo state
def check_teredo_state():
    output = run_command("netsh interface teredo show state")
    messagebox.showinfo("Teredo State", output)

# Function to set Teredo state to EnterpriseClient
def set_teredo_enterprise():
    output = run_command("netsh interface teredo set state type=enterpriseclient")
    messagebox.showinfo("Teredo State", output)

# Function to set Teredo state to Disabled
def set_teredo_disabled():
    output = run_command("netsh interface teredo set state type=disabled")
    messagebox.showinfo("Teredo State", output)

# Function to set Teredo state to Client
def set_teredo_client():
    output = run_command("netsh interface teredo set state type=client")
    messagebox.showinfo("Teredo State", output)

# Function to check IP Configuration
def check_ipconfig():
    output = run_command("ipconfig")
    messagebox.showinfo("IP Configuration", output)

# Function to clear cache (DNS, Winsock, IP reset)
def clear_cache():
    run_command("ipconfig /flushdns")
    run_command("netsh winsock reset")
    run_command("netsh int ip reset")
    run_command("netsh interface teredo reset")
    messagebox.showinfo("Cache Cleared", "Network cache and configurations have been reset.")

# Function to troubleshoot network (Traceroute, nslookup, pathping)
def troubleshoot_network():
    run_command("tracert google.com")
    run_command("nslookup google.com")
    run_command("pathping google.com")
    messagebox.showinfo("Network Troubleshooting", "Network troubleshooting complete.")

# Set up the GUI window
root = tk.Tk()
root.title("Teredo Helper")

# Set up the banner frame
banner_frame = tk.Frame(root, bg="black", padx=10, pady=10)
banner_frame.pack(fill="x")

# Banner text with gradient colors and black background
banner_label1 = tk.Label(banner_frame, text="████████╗███████╗██████╗ ███████╗██████╗  ██████╗     ██╗  ██╗███████╗██╗     ██████╗ ███████╗██████╗", 
                         fg="#FF0000", bg="black", font=("Courier", 12, "bold"))
banner_label1.pack()

banner_label2 = tk.Label(banner_frame, text="╚══██╔══╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔═══██╗    ██║  ██║██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗", 
                         fg="#FF3300", bg="black", font=("Courier", 12, "bold"))
banner_label2.pack()

banner_label3 = tk.Label(banner_frame, text="   ██║   █████╗  ██████╔╝█████╗  ██║  ██║██║   ██║    ███████║█████╗  ██║     ██████╔╝█████╗  ██████╔╝", 
                         fg="#FF6600", bg="black", font=("Courier", 12, "bold"))
banner_label3.pack()

banner_label4 = tk.Label(banner_frame, text="   ██║   ██╔══╝  ██╔══██╗██╔══╝  ██║  ██║██║   ██║    ██╔══██║██╔══╝  ██║     ██╔═══╝ ██╔══╝  ██╔══██╗", 
                         fg="#FF9900", bg="black", font=("Courier", 12, "bold"))
banner_label4.pack()

banner_label5 = tk.Label(banner_frame, text="   ██║   ███████╗██║  ██║███████╗██████╔╝╚██████╔╝    ██║  ██║███████╗███████╗██║     ███████╗██║  ██║", 
                         fg="#FFCC00", bg="black", font=("Courier", 12, "bold"))
banner_label5.pack()

banner_label6 = tk.Label(banner_frame, text="   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝", 
                         fg="#FFFF00", bg="black", font=("Courier", 12, "bold"))
banner_label6.pack()

# Create a title label
title_label = tk.Label(root, text="Teredo Helper - Network and IP Configuration Tool", font=("Arial", 16), pady=10)
title_label.pack()

# Create a credits label
credits_label = tk.Label(root, text="Credits: Developed by CheezzyBoii", font=("Arial", 10), pady=5)
credits_label.pack()

# Set up the buttons for each function
btn_check_teredo = tk.Button(root, text="Check Teredo State", command=check_teredo_state)
btn_check_teredo.pack(pady=5)

btn_set_enterprise = tk.Button(root, text="Set Teredo to EnterpriseClient", command=set_teredo_enterprise)
btn_set_enterprise.pack(pady=5)

btn_set_disabled = tk.Button(root, text="Set Teredo to Disabled", command=set_teredo_disabled)
btn_set_disabled.pack(pady=5)

btn_set_client = tk.Button(root, text="Set Teredo to Client", command=set_teredo_client)
btn_set_client.pack(pady=5)

btn_check_ipconfig = tk.Button(root, text="Check IPConfig", command=check_ipconfig)
btn_check_ipconfig.pack(pady=5)

btn_clear_cache = tk.Button(root, text="Clear Cache", command=clear_cache)
btn_clear_cache.pack(pady=5)

btn_troubleshoot = tk.Button(root, text="Run Network Troubleshooting", command=troubleshoot_network)
btn_troubleshoot.pack(pady=5)

# Start the Tkinter GUI event loop
root.mainloop()
