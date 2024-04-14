#!/bin/python

# ::::::::  :::    ::: :::::::::   :::::::  ::::::::: ::::::::::: :::::::::      ::: ::::::::::: ::::::::  
# :+:    :+: :+:    :+: :+:    :+: :+:   :+: :+:    :+:    :+:     :+:    :+:   :+: :+:   :+:    :+:    :+: 
# +:+        +:+    +:+ +:+    +:+ +:+  :+:+ +:+    +:+    +:+     +:+    +:+  +:+   +:+  +:+           +:+ 
# +#++:++#++ +#+    +:+ +#+    +:+ +#+ + +:+ +#++:++#+     +#+     +#++:++#:  +#++:++#++: +#+        +#++:  
#        +#+ +#+    +#+ +#+    +#+ +#+#  +#+ +#+           +#+     +#+    +#+ +#+     +#+ +#+           +#+ 
# #+#    #+# #+#    #+# #+#    #+# #+#   #+# #+#           #+#     #+#    #+# #+#     #+# #+#    #+#    #+# 
#  ########   ########  #########   #######  ###       ########### ###    ### ###     ### ###     ########                                                              

# Date created: 11/04/2024
# Last Revision: 14/04/2024

# Purpose: This script gathers the maximum information possible from a machine with multiple options to chose from or gather everything at once 
# run pip install -r requirements.txt to install all depedencies required

import os
import pwd
import socket
import getpass
import psutil
import platform
import requests
import subprocess
import netifaces

# ANSI escape codes for colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'  # Reset text color to default

# Get system information
def get_system_info(choice):  

    # Initialize an empty string to store the system information
    system_info = ""

    # Append each piece of system information to the system_info string based on user choice

    # User Information
    if choice == '1' or choice == '11':
                    
        # User Information
        system_info += YELLOW + "User Information" + RESET + "\n"
        system_info += "Username: " + getpass.getuser() + "\n"
        system_info += "Home directory: " + os.path.expanduser("~") + "\n"
        system_info += "User ID: " + str(os.getuid()) + "\n"
        system_info += "Group ID: " + str(os.getgid()) + "\n"
        
        # User Preferences
        system_info += YELLOW + "User Preferences" + RESET + "\n"
        system_info += "Default shell: " + pwd.getpwuid(os.getuid()).pw_shell + "\n"
        system_info += "Default text editor: " + os.getenv("EDITOR", "Not set") + "\n"
        system_info += "Default browser: " + os.getenv("BROWSER", "Not set") + "\n"

        system_info += YELLOW + "Recent Activity" + RESET + "\n"
        try:
            history_file = os.path.expanduser("~/.bash_history")
            with open(history_file, "r") as f:
                recent_commands = f.readlines()[-50:]
            system_info += "Last 50 commands:\n" + "".join(recent_commands) + "\n"
        except Exception as e:
            system_info += "Error retrieving recent commands: " + str(e) + "\n"

        # User Files (Example: Display the contents of the user's home directory)
        system_info += YELLOW + "User Files" + RESET + "\n"
        try:
            home_dir_contents = os.listdir(os.path.expanduser("~"))
            system_info += "Contents of home directory:\n" + "\n".join(home_dir_contents) + "\n"
        except Exception as e:
            system_info += "Error retrieving home directory contents: " + str(e) + "\n"

        # User Permissions
        system_info += YELLOW + "User Permissions" + RESET + "\n"
        system_info += "Sudo privileges: " + ("Yes" if os.getuid() == 0 else "No") + "\n"

        # User Environment
        system_info += YELLOW + "User Environment" + RESET + "\n"
        system_info += "Environment variables:\n"
        for key, value in os.environ.items():
            system_info += f"{key}: {value}\n"

        # User History (Example: Display the last 5 login/logout events)
        system_info += YELLOW + "User History" + RESET + "\n"
        try:
            login_history = subprocess.check_output("last -n 5", shell=True).decode("utf-8")
            system_info += "Last 5 login/logout events:\n" + login_history + "\n"
        except Exception as e:
            system_info += "Error retrieving login/logout history: " + str(e) + "\n"

    # Platform Information
    if choice == '2' or choice == '11':
        system_info += YELLOW + "Platform Information:" + RESET + "\n"
        system_info += "OS: " + platform.system() + "\n"
        system_info += "OS Release: " + platform.release() + "\n"
        system_info += "Architecture: " + platform.machine() + "\n"
        system_info += "Python Version: " + platform.python_version() + "\n\n"

    # CPU Information
    if choice == '3' or choice == '11':
        system_info += YELLOW + "CPU Information:" + RESET + "\n"
        system_info += "Physical Cores: " + str(psutil.cpu_count(logical=False)) + "\n"
        system_info += "Total Cores: " + str(psutil.cpu_count(logical=True)) + "\n"
        system_info += "CPU Usage: " + str(psutil.cpu_percent(interval=1)) + "\n\n"

    # Memory Information
    if choice == '4' or choice == '11':
        mem = psutil.virtual_memory()
        system_info += YELLOW + "Memory Information:" + RESET + "\n"
        system_info += "Total Memory: " + str(mem.total) + "\n"
        system_info += "Available Memory: " + str(mem.available) + "\n"
        system_info += "Used Memory: " + str(mem.used) + "\n"
        system_info += "Memory Usage: " + str(mem.percent) + "\n\n"

    # Disk Information
    if choice == '5' or choice == '11':
        system_info += YELLOW + "Disk Information:" + RESET + "\n"
        partitions = psutil.disk_partitions()
        for partition in partitions:
            system_info += "Device: " + partition.device + "\n"
            system_info += "Mountpoint: " + partition.mountpoint + "\n"
            system_info += "Filesystem Type: " + partition.fstype + "\n"
            system_info += "Disk Usage: " + str(psutil.disk_usage(partition.mountpoint)) + "\n\n"

    # Network Information
    if choice == '6' or choice == '11':
        system_info += YELLOW + "Network Information:" + RESET + "\n"
        system_info += "Hostname: " + socket.gethostname() + "\n"
        system_info += "IP Addresses:\n"
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                system_info += f"{interface}: {addrs[netifaces.AF_INET][0]['addr']}\n"
        try:
            public_ip = requests.get('https://api.ipify.org').text
            system_info += "Public IP: " + public_ip + "\n"
        except Exception as e:
            system_info += "Error retrieving public IP: " + str(e) + "\n"
        system_info += "\n"

    # Process Information
    if choice == '7' or choice == '11':
        system_info += YELLOW + "Process Information:" + RESET + "\n"
        for proc in psutil.process_iter(['pid', 'name']):
            system_info += str(proc.info) + "\n"
        system_info += "\n"

    # System Logs
    if choice == '8' or choice == '11':
        system_info += YELLOW + "System Logs:" + RESET + "\n"
        try:
            logs = subprocess.check_output(['journalctl', '-p', '3', '--no-pager']).decode()
            system_info += logs + "\n"
        except Exception as e:
            system_info += "Error retrieving system logs: " + str(e) + "\n"

    # Installed Software
    if choice == '9' or choice == '11':
        system_info += YELLOW + "Installed Software:" + RESET + "\n"
        try:
            if platform.system() == "Linux":
                software = subprocess.check_output(['dpkg', '--list']).decode()
            elif platform.system() == "Windows":
                software = subprocess.check_output(['wmic', 'product', 'get', 'name,version']).decode()
            system_info += software + "\n"
        except Exception as e:
            system_info += "Error retrieving installed software: " + str(e) + "\n"

    # Security Information
    if choice == '10' or choice == '11':
        system_info += YELLOW + "Security Information:" + RESET + "\n"
        try:
            if platform.system() == "Linux":
                security = subprocess.check_output(['sudo', 'unhide', 'sys']).decode()
            elif platform.system() == "Windows":
                security = subprocess.check_output(['whoami', '/all']).decode()
            system_info += security + "\n"
        except Exception as e:
            system_info += "Error retrieving security information: " + str(e) + "\n"

    # Return the system_info string containing the selected information
    return system_info

# Save system information to a file
def save_to_file(system_info, filename="system_info.txt"):
    try:
        with open(filename, "w") as f:
            f.write(system_info)
    except Exception as e:
        print("Error saving system information to file:", e)
        return None

# Clear the terminal for better visibility (only works in some terminals)        
def clearscreen():
    print("\033c", end="")

# Func to print ASCII art menu
def print_menu():
    banner = YELLOW+"""
    
::::    ::::  ::::::::::: ::::    ::: :::::::::: ::::::::   ::::::::  :::::::::      :::     :::::::::  :::::::::  :::::::::: :::::::::  
+:+:+: :+:+:+     :+:     :+:+:   :+: :+:       :+:    :+: :+:    :+: :+:    :+:   :+: :+:   :+:    :+: :+:    :+: :+:        :+:    :+: 
+:+ +:+:+ +:+     +:+     :+:+:+  +:+ +:+       +:+    +:+ +:+        +:+    +:+  +:+   +:+  +:+    +:+ +:+    +:+ +:+        +:+    +:+ 
+#+  +:+  +#+     +#+     +#+ +:+ +#+ :#::+::#  +#+    +:+ :#:        +#++:++#:  +#++:++#++: +#++:++#+  +#++:++#+  +#++:++#   +#++:++#:  
+#+       +#+     +#+     +#+  +#+#+# +#+       +#+    +#+ +#+   +#+# +#+    +#+ +#+     +#+ +#+    +#+ +#+    +#+ +#+        +#+    +#+ 
#+#       #+#     #+#     #+#   #+#+# #+#       #+#    #+# #+#    #+# #+#    #+# #+#     #+# #+#    #+# #+#    #+# #+#        #+#    #+# 
###       ### ########### ###    #### ###        ########   ########  ###    ### ###     ### #########  #########  ########## ###    ### 

    """+RESET
    
    options = """
        1. User Information
        2. Platform Information
        3. CPU Information
        4. Memory Information
        5. Disk Information
        6. Network Information
        7. Process Information
        8. System Logs
        9. Installed Software
        10. Security Information
        11. All Information
        0. Exit
    """

    print(banner)
    print(options)

#------------------------------------------------------------

# Main function
def main():

    while True:
        # Print the menu
        clearscreen()
        print_menu()
        
        # Get user input
        choice = input("Enter your choice: ")

        # Process user choice
        if choice == '0':
            print("bye bye...")
            clearscreen()
            quit()

        output = get_system_info(choice)
        filename = ""

        if choice != '0':
            if choice == '1':
                filename = "User_Info.txt"
                print("User information saved to", GREEN+os.path.abspath(filename)+RESET)
                input("Press Enter to go back: ")
            elif choice == '2':
                filename = "Platform_Info.txt"
                print("PlatformS information saved to", GREEN+os.path.abspath(filename)+RESET)
                input("Press Enter to go back: ")
            elif choice == '3':
                filename = "CPU_Info.txt"
                print("CPU information saved to", GREEN+os.path.abspath(filename)+RESET)
                input("Press Enter to go back: ")
            elif choice == '4':
                filename = "Memory_Info.txt"
                print("Memory information saved to", GREEN+os.path.abspath(filename)+RESET)
                input("Press Enter to go back: ")
            elif choice == '5':
                filename = "Disk_Info.txt"
                print("Disk information saved to", GREEN+os.path.abspath(filename)+RESET)
                input("Press Enter to go back: ")
            elif choice == '6':
                filename = "Network_Info.txt"
                print("Network information saved to", GREEN+os.path.abspath(filename)+RESET)
                input("Press Enter to go back: ")
            elif choice == '7':
                filename = "Process_Info.txt"
                print("Process information saved to", GREEN+os.path.abspath(filename)+RESET)
                input("Press Enter to go back: ")
            elif choice == '8':
                filename = "System_Logs.txt"
                print("System_Logs saved to", GREEN+os.path.abspath(filename)+RESET)
                input("Press Enter to go back: ")
            elif choice == '9':
                filename = "Installed_Software.txt"
                print("Installed Software information saved to", GREEN+os.path.abspath(filename)+RESET)
                input("Press Enter to go back: ")
            elif choice == '10':
                filename = "Security_Info.txt"
                print("Security information saved to", GREEN+os.path.abspath(filename)+RESET)
                input("Press Enter to go back: ")
            elif choice == '11':
                filename = "All_System_Info.txt"
                print("All information saved to", GREEN+os.path.abspath(filename)+RESET)
                input("Press Enter to go back: ")

            if output:
                clearscreen()
                save_to_file(output, filename)

        # Clear the screen
        clearscreen()
        

# Entry point of the program
if __name__ == "__main__":
    main()
