import socket
import os

BUF_SIZE = 4096
FFLAG_START = b"<<FILE_START>>"
FFLAG_END   = b"<<FILE_END>>"


def send_file(path, conn: socket.socket):
    try:    
        #TODO: add validation to ensure the data exists!
        with open(path, "rb") as f:
            data = f.read()
        
        conn.sendall(FFLAG_START + data + FFLAG_END)
        
        return f"[+] {path} sent successfully"

    except Exception as e:
        return f"[ERRSER_Utils] Failed to send file ({path}). Reason: {e}"
        
    
def recieve_file(path, conn: socket.socket):
    conn.sendall(b"rd")
    content = b""
    
    while True:
        chunk = conn.recv(BUF_SIZE)
        if FFLAG_END in chunk:
            content += chunk.replace(FFLAG_END, b"")
            break
        content += chunk
    
    try:
        with open(path, "wb") as f:
            f.write(content)
        return f"Server successfully sent data"
    except Exception as e:
        return f"[ERRSER_Utils] Upload Failed. Reason: {e}"


def remove_file(path):
    try:
        os.remove(path)
        return f"[-] File removed: {path}"
    
    except Exception as e:
        return f"[ERRSER_Utils] Failed to remove file ({path}). Reason: {e}"