# Leap Angle Debugger

This repository contains a lightweight system to calculate and print index finger joint angles (MCP, PIP, DIP) using Ultraleap hand tracking data over a TCP connection.

## 📁 Contents

- `server.py`: A TCP server that reads Ultraleap tracking data using the LeapC SDK and sends it as a comma-separated string.
- `live_joint_angles.py`: A client script that receives the tracking data and computes the index finger joint angles.

## 🛠 Requirements

- Python 3.12
- Ultraleap LeapC SDK (Linux)
- NumPy

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔌 Installing the Ultraleap SDK on Linux

1. **Download the SDK**  
   Go to the [Ultraleap Downloads page](https://developer.ultraleap.com/tracking/downloads) and download the **Ultraleap Tracking SDK for Linux (LeapC)**.

2. **Extract the SDK**
   ```bash
   tar -xvzf Ultraleap_Tracking_SDK_Linux_*.tar.gz
   cd Ultraleap_Tracking_SDK_Linux*/LeapSDK
   ```

3. **Install the Python bindings**
   ```bash
   cd lib
   pip install .
   ```

4. **Start the Leap Service**
   ```bash
   sudo cp daemon/leapd.service /etc/systemd/system/
   sudo systemctl daemon-reexec
   sudo systemctl daemon-reload
   sudo systemctl enable leapd.service
   sudo systemctl start leapd.service
   ```

5. **(Optional) Check service status**
   ```bash
   sudo systemctl status leapd.service
   ```

6. **(Optional) View the Ultraleap Control Panel**
   ```bash
   ./bin/UltraleapControlPanel
   ```

---

## ▶️ How to Run

### Terminal 1: Start the server

```bash
python3 server.py
```

### Terminal 2: Start the joint angle debugger

```bash
python3 live_joint_angles.py
```

Make sure the Ultraleap device is connected and working properly before running the scripts.

# 🧠 System Overview

## `server.py` – Ultraleap TCP Server
This script connects to the Ultraleap LeapC API and continuously streams hand tracking data over a TCP socket. Specifically, it sends:

- **20 landmarks** (one for each joint segment on thumb, index, middle, and ring fingers – 4 per finger)
- **1 palm landmark** (the hand's central palm position)
- **1 wrist landmark** 

Each landmark includes `(x, y, z)` coordinates, resulting in a total of `22 * 3 = 66` float values. These are serialized as a comma-separated string and sent once per frame, ending with a newline (`\n`), e.g.:

```
x0,y0,z0,x1,y1,z1,...,x21,y21,z21\n
```

> 💡 The 21st landmark (index 20) corresponds to the **palm position**, used as a reference for angle calculations.
> 💡 The 22nd landmark (index 21) corresponds to the **wrist position**, used as a reference for angle calculations.


---

## `live_joint_angles.py` – Index Finger Joint Angle Debugger
This script connects to the TCP server, receives the 63 float values, reshapes them into a `21x3` array of landmarks, and performs vector-based calculations to estimate joint angles on the **index finger only**:

- **MCP (Metacarpophalangeal) Joint**  
  Calculated as the angle between:
  ```
  MCP → PIP and MCP → Palm center
  ```

- **PIP (Proximal Interphalangeal) Joint**  
  Calculated as the angle between:
  ```
  PIP → DIP and MCP → PIP
  ```

- **DIP (Distal Interphalangeal) Joint**  
  Calculated as the angle between:
  ```
  DIP → Tip and PIP → DIP
  ```

These angles are printed live to the console every 0.2 seconds.

> ⚠️ Notes:
> - Tracking accuracy depends on Ultraleap's USB 3.0 performance.
> - If hand tracking fails or values appear inconsistent, confirm that the palm landmark is being correctly included at index 20.


