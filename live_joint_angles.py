#!/usr/bin/env python3

import socket
import time
import numpy as np

# TCP settings
HOST = '127.0.0.1'
PORT = 60002

def angle_between(v1, v2):
    v1_u = v1 / (np.linalg.norm(v1) + 1e-6)
    v2_u = v2 / (np.linalg.norm(v2) + 1e-6)
    dot = np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)
    return np.degrees(np.arccos(dot))

def process_line(line):
    try:
        values = [float(x) for x in line.split(',')]
        if len(values) != 66:
            print(f"Expected 66 floats (22 landmarks), got {len(values)}")
            return
        landmarks = np.array(values).reshape((22, 3))

        palm = landmarks[20]
        wrist = landmarks[21]     
        mcp = landmarks[4]       # MCP
        pip = landmarks[5]       # PIP
        dip = landmarks[6]       # DIP
        tip = landmarks[7]       # Tip

        vec_palm = mcp - palm
        vec_wrist = mcp - wrist
        vec_mcp = pip - mcp
        mcp_angle = angle_between(vec_wrist, vec_mcp)

        vec_pip = dip - pip
        pip_angle = angle_between(vec_mcp, vec_pip)

        vec_dip = tip - dip
        dip_angle = angle_between(vec_pip, vec_dip)

        print(f"[INDEX ANGLES] MCP: {mcp_angle:.2f}°, PIP: {pip_angle:.2f}°, DIP: {dip_angle:.2f}°")
    except Exception as e:
        print(f"[ERROR] {e}")

def main():
    print(f"Connecting to {HOST}:{PORT}...")
    sock = None
    while sock is None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            sock.setblocking(False)
            print("Connected.")
        except Exception as e:
            print(f"[TCP ERROR] {e}. Retrying in 2s...")
            time.sleep(2)

    buffer = ''
    while True:
        try:
            data = sock.recv(4096).decode('utf-8')
            if not data:
                print("[INFO] Connection lost. Exiting.")
                break
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                process_line(line.strip())
        except (BlockingIOError, socket.error):
            pass
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            break
        time.sleep(0.1)

if __name__ == '__main__':
    main()
