import socket
from controller import send_cmd


def start_comm(conn: socket.socket):
    try:
        
        while True:
            cmd = input("CMD>> ").strip()
            if not cmd:
                continue
            
            if cmd == "exit":
                conn.sendall("exit".encode())
                print("[-] Closing connection :^")
                break
            
            resp = send_cmd(cmd, conn)
            print(resp)
            
    except Exception as e:
        print(f"[!] Disconnected. Reason: {e}")


def conn_target():
    
    while True:
        s = socket.socket(
            socket.AF_INET, # IPv4
            socket.SOCK_STREAM, # TCP        
        )

        HOST_TARGET = input("IP HOST TARGET: ")
        PORT = 12345   

        if HOST_TARGET == "exit":
            print("Exit program :^")
            break
        
        try:
            s.connect((HOST_TARGET, PORT))
            print(f"[+] Connected to {HOST_TARGET}:{PORT}")        
            start_comm(conn=s)
            
        except Exception as e:
            print(f"Unable to connect {HOST_TARGET}:{PORT}\n[Err]: {e}")
        

if __name__ == "__main__":
    conn_target()